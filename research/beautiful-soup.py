import requests
import sqlite3
from bs4 import BeautifulSoup

# Connect to the database (it creates the DB if it doesn't exist)
conn = sqlite3.connect('events-soup.db')
cursor = conn.cursor()

# Create the events table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT,
    date TEXT,
    venue TEXT,
    event_url TEXT,
    description TEXT,
    category TEXT,
    UNIQUE(event_name, date)
)
''')

# Send a request to fetch the HTML content
response = requests.get(input("Barcelona Met URL to scrape data from: "))

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Scrape all events
    events = soup.find_all('div', class_='event_result')

    for event in events:
        # Extract the event details
        event_date = event.find('p', class_='event_date').text.strip()

        # Find the h4 tag with class 'event_title'
        event_title_tag = event.find('h4', class_='event_title')

        event_title = event_title_tag.text.strip()
        event_url = event_title_tag.find('a')['href']

        # Find the next <a> tag, which is the venue link
        venue_tag = event_title_tag.find_next('a', href=True)

        # Extract the venue name and link
        venue = venue_tag.text.strip()
        venue_url = venue_tag['href']

        description = event.find('p', class_='description').text.strip()
        category = event.find('p', class_='cats').text.strip()

        # Insert into the database if it's not a duplicate
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO events (event_name, date, venue, description, category, event_url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (event_title, event_date, venue, description, category, event_url))
            conn.commit()
        except Exception as e:
            print(f"Error inserting event: {e}")
else:
    print(f'Failed to retrieve page. Status code: {response.status_code}')


# Close the connection
conn.close()
