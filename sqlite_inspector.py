import pandas as pd
import sqlite3
from datetime import datetime
import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def inspect_database(db_path: str):
    """Inspect SQLite database structure"""
    try:
        with sqlite3.connect(db_path) as conn:
            # Get list of tables
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                logger.info(f"\nTable: {table_name}")
                
                # Get column info
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                logger.info("Columns:")
                for col in columns:
                    logger.info(f"  {col[1]} ({col[2]})")
                
                # Show sample data
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                sample = cursor.fetchone()
                if sample:
                    logger.info("\nSample data:")
                    for col, val in zip([col[1] for col in columns], sample):
                        logger.info(f"  {col}: {val}")
    except sqlite3.Error as e:
        logger.error(f"Error inspecting database {db_path}: {str(e)}")

class EventDatabaseMerger:
    def __init__(self, ra_db_path: str, bcn_db_path: str, output_db_path: str):
        self.ra_db_path = ra_db_path
        self.bcn_db_path = bcn_db_path
        self.output_db_path = output_db_path
        
        # These will be set after inspection
        self.ra_datetime_col = None
        self.ra_end_datetime_col = None
        self.bcn_datetime_col = None
        self.bcn_end_datetime_col = None
        
        # Inspect and set column names
        self.inspect_and_set_columns()

    def inspect_and_set_columns(self):
        """Inspect databases and set correct column names"""
        logger.info("Inspecting Resident Advisor database structure...")
        inspect_database(self.ra_db_path)
        
        logger.info("\nInspecting Barcelona Metropolitan database structure...")
        inspect_database(self.bcn_db_path)
        
        # After seeing the output, please set these column names manually
        logger.info("\nPlease update the column mappings in the code based on the inspection results")

    def read_ra_events(self) -> pd.DataFrame:
        """Read events from Resident Advisor SQLite database"""
        with sqlite3.connect(self.ra_db_path) as conn:
            # Get all tables in the database
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if not tables:
                raise ValueError("No tables found in Resident Advisor database")
            
            # Use the first table found (you might want to modify this)
            table_name = tables[0][0]
            logger.info(f"Reading from table: {table_name}")
            
            # Get all columns from the table
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            logger.info(f"Columns found: {df.columns.tolist()}")
            
            df['source'] = 'ra'
            return df

    def read_bcn_events(self) -> pd.DataFrame:
        """Read events from Barcelona Metropolitan SQLite database"""
        with sqlite3.connect(self.bcn_db_path) as conn:
            # Get all tables in the database
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if not tables:
                raise ValueError("No tables found in Barcelona Metropolitan database")
            
            # Use the first table found (you might want to modify this)
            table_name = tables[0][0]
            logger.info(f"Reading from table: {table_name}")
            
            # Get all columns from the table
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            logger.info(f"Columns found: {df.columns.tolist()}")
            
            df['source'] = 'bcn'
            return df

def main():
    # File paths for SQLite databases
    ra_db_path = "db/events-ra.db"
    bcn_db_path = "db/events-json.db"
    output_db_path = "db/merged_events.db"
    
    try:
        # Create merger instance
        merger = EventDatabaseMerger(
            ra_db_path=ra_db_path,
            bcn_db_path=bcn_db_path,
            output_db_path=output_db_path
        )
        
        # After running this, you'll see the database structure
        # and can provide the correct column names for the merger
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()