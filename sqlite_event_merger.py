import pandas as pd
from datetime import datetime
import sqlite3
from typing import Dict, List
from dataclasses import dataclass
import logging
import json
import openai
import os
from transformers import pipeline
import gc
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Event:
    id: int
    name: str
    start_datetime: datetime
    end_datetime: datetime
    description: str
    url: str
    venue: str
    source: str  # 'ra' for Resident Advisor or 'bcn' for Barcelona Metropolitan

class EventDatabaseMerger:
    def __init__(self, ra_db_path: str, bcn_db_path: str, output_db_path: str):
        self.ra_db_path = ra_db_path
        self.bcn_db_path = bcn_db_path
        self.output_db_path = output_db_path

    def read_ra_events(self) -> pd.DataFrame:
        """Read events from Resident Advisor SQLite database"""
        with sqlite3.connect(self.ra_db_path) as conn:
            query = """
            SELECT 
                id,
                event_name as name,
                start_time as start_datetime,
                end_time as end_datetime,
                event_url as url,
                venue_name as venue
            FROM events_ra
            """
            df = pd.read_sql(query, conn)
            df['source'] = 'ra'
            return df

    def read_bcn_events(self) -> pd.DataFrame:
        """Read events from Barcelona Metropolitan SQLite database"""
        with sqlite3.connect(self.bcn_db_path) as conn:
            query = """
            SELECT 
                id,
                title as name,
                date as start_datetime,
                date as end_datetime,
                description,
                event_url as url,
                venue as venue
            FROM events
            """
            df = pd.read_sql(query, conn)
            df['source'] = 'bcn'
            return df

    def standardize_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure datetime fields are in consistent format"""
        for col in ['start_datetime', 'end_datetime']:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        return df

    def merge_dataframes(self) -> pd.DataFrame:
        """Merge and standardize both event sources"""
        logger.info("Reading events from Resident Advisor database...")
        ra_df = self.read_ra_events()
        
        logger.info("Reading events from Barcelona Metropolitan database...")
        bcn_df = self.read_bcn_events()
        
        logger.info("Standardizing datetime fields...")
        ra_df = self.standardize_datetime(ra_df)
        bcn_df = self.standardize_datetime(bcn_df)
        
        logger.info("Merging dataframes...")
        merged_df = pd.concat([ra_df, bcn_df], ignore_index=True)
        return merged_df

class LocalEventClassifier:
    def __init__(self, model_name="cross-encoder/nli-deberta-v3-small"):
        """Initialize the classifier with a smaller, more efficient model"""
        logger.info(f"Loading model: {model_name}")
        
        # Set smaller batch size for inference
        self.batch_size = 1
        
        # Manually set torch to use CPU
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        
        try:
            self.classifier = pipeline("zero-shot-classification",
                                     model=model_name,
                                     device=-1,  # Force CPU usage
                                     model_kwargs={"low_cpu_mem_usage": True})
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
        
        # Define classification categories with simpler options
        self.categories = {
            "environment": ["outdoor", "indoor"],
            "activity_level": ["active", "calm"],
            "price_category": ["free", "paid"],
            "social_setting": ["solo", "group"],
            "event_type": ["music", "theatre", "art", "sports", "food", "cultural", "workshop"]
        }

    def cleanup(self):
        """Clean up memory"""
        if hasattr(self, 'classifier'):
            del self.classifier
        torch.cuda.empty_cache()
        gc.collect()

    def classify_aspect(self, text: str, category: str, labels: List[str]) -> str:
        """Classify a single aspect of an event with error handling"""
        try:
            # Truncate text to prevent memory issues
            text = text[:512] if text else ""
            
            result = self.classifier(
                text,
                labels,
                hypothesis_template="This event is {}.",
                batch_size=self.batch_size
            )
            return result['labels'][0]
        except Exception as e:
            logger.error(f"Error classifying {category}: {str(e)}")
            return "unknown"

    def classify_event(self, event: Event) -> Dict[str, str]:
        """Classify all aspects of a single event"""
        # Combine relevant text for classification
        text = f"{event.name}. {event.description}. Location: {event.venue}"
        
        classifications = {}
        try:
            for category, labels in self.categories.items():
                classifications[category] = self.classify_aspect(text, category, labels)
                gc.collect()  # Regular garbage collection
                
        except Exception as e:
            logger.error(f"Error in classify_event: {str(e)}")
            return {category: "unknown" for category in self.categories.keys()}
            
        return classifications

    def batch_classify_events(self, events: List[Event], batch_size: int = 1) -> List[Dict[str, str]]:
        """Classify events one at a time to prevent memory issues"""
        classifications = []
        total_events = len(events)
        
        for i, event in enumerate(events):
            try:
                logger.info(f"Classifying event {i+1} of {total_events}")
                result = self.classify_event(event)
                classifications.append(result)
                
                # Regular cleanup
                gc.collect()
                
            except Exception as e:
                logger.error(f"Error processing event {i+1}: {str(e)}")
                classifications.append({category: "unknown" for category in self.categories.keys()})
                
            # More aggressive cleanup every 10 events
            if (i + 1) % 10 == 0:
                self.cleanup()
                
        return classifications

class EventClassifier:
    def __init__(self, api_key: str):
        self.client = openai.Client(api_key=api_key)
        
    def classify_event(self, event: Event) -> Dict[str, str]:
        """Classify a single event using AI"""
        prompt = f"""
        Analyze this event and classify it according to these categories:
        Event: {event.name}
        Description: {event.description}
        Venue: {event.venue}

        Please classify into these categories:
        1. Environment (outdoor/indoor)
        2. Activity Level (active/calm)
        3. Price Category (free/paid)
        4. Social Setting (solo/group)
        5. Event Type (music/theatre/art/sports/food/cultural/workshop/other)

        Provide classification in JSON format with these exact keys:
        environment, activity_level, price_category, social_setting, event_type
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an event classifier. Respond only with JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error classifying event {event.name}: {str(e)}")
            return {}

    def batch_classify_events(self, events: List[Event], batch_size: int = 100) -> List[Dict[str, str]]:
        """Classify events in batches"""
        classifications = []
        total_events = len(events)
        
        for i in range(0, total_events, batch_size):
            batch = events[i:i + batch_size]
            logger.info(f"Classifying batch {i//batch_size + 1} of {(total_events + batch_size - 1)//batch_size}")
            batch_results = [self.classify_event(event) for event in batch]
            classifications.extend(batch_results)
            
        return classifications

class SQLiteManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    def create_merged_table(self):
        """Create the merged events table with classification columns"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS merged_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_id INTEGER,
                name TEXT,
                start_datetime TEXT,
                end_datetime TEXT,
                description TEXT,
                url TEXT,
                venue TEXT,
                source TEXT,
                environment TEXT,
                activity_level TEXT,
                price_category TEXT,
                social_setting TEXT,
                event_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

    def save_classified_events(self, events_df: pd.DataFrame, classifications: List[Dict[str, str]]):
        """Save the merged and classified events to the SQLite database"""
        # Add classification results to dataframe
        for i, classification in enumerate(classifications):
            for key, value in classification.items():
                events_df.loc[i, key] = value
        
        # Save to database
        with sqlite3.connect(self.db_path) as conn:
            events_df.to_sql('merged_events', conn, if_exists='append', index=False)

def main():
    # File paths for SQLite databases
    ra_db_path = "db/events-ra.db"
    bcn_db_path = "db/events-json.db"
    output_db_path = "db/merged_events.db"
    
    # Initialize components
    merger = EventDatabaseMerger(
        ra_db_path=ra_db_path,
        bcn_db_path=bcn_db_path,
        output_db_path=output_db_path
    )
    
     # Initialize the local classifier
    classifier = LocalEventClassifier()
    db_manager = SQLiteManager(output_db_path)
    
    try:
        # Merge databases
        logger.info("Starting database merge process...")
        merged_df = merger.merge_dataframes()
        
        # Convert to Event objects
        events = [
            Event(
                id=row['id'],
                name=row['name'],
                start_datetime=row['start_datetime'],
                end_datetime=row['end_datetime'],
                description=row['description'],
                url=row['url'],
                venue=row['venue'],
                source=row['source']
            )
            for _, row in merged_df.iterrows()
        ]
        
        # Classify events
        logger.info("Starting event classification...")
        classifications = classifier.batch_classify_events(events)
        
        # Create and save to database
        logger.info("Creating output database...")
        db_manager.create_merged_table()
        
        logger.info("Saving classified events...")
        db_manager.save_classified_events(merged_df, classifications)
        
        logger.info(f"Process completed successfully! Output saved to {output_db_path}")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()