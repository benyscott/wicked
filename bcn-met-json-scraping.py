import sqlite3
import json
import requests
from bs4 import BeautifulSoup

# Connect to SQLite database
conn = sqlite3.connect('events-json.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    lat REAL,
    lng REAL,
    event_url TEXT,
    venue TEXT,
    date TEXT,
    description TEXT,
    category TEXT,
    UNIQUE(title, date)
)
''')

url = input("Barcelona Met URL to scrape data from: ")

# Send a request to fetch the HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = json.loads(response.text)

    # Iterate through the events in the JSON and insert them into the SQLite database
    for event in data['results']:
        # Extract event details
        title = event['title']
        lat = event['lat']
        lng = event['lng']
        
        # Extract HTML for description, venue, and event date
        html_content = event['html']
        
        # For simplicity, we'll use BeautifulSoup to extract details from the HTML part (if needed)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract the event details
        date = soup.find('p', class_='event_date').text.strip()

        # Find the h4 tag with class 'event_title'
        event_title_tag = soup.find('h4', class_='event_title')

        event_url = event_title_tag.find('a')['href']

        # Find the next <a> tag, which is the venue link
        venue_tag = event_title_tag.find_next('a', href=True)

        # Extract the venue name and link
        venue = venue_tag.text.strip()
        venue_url = venue_tag['href']

        description = soup.find('p', class_='description').text.strip() if soup.find('p', class_='description') else ''
        category = soup.find('p', class_='cats').text.strip() if soup.find('p', class_='cats') else ''
        
        # Insert data into SQLite
        cursor.execute('''
        INSERT OR IGNORE INTO events (title, event_url, venue, date, description, category, lat, lng)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, event_url, venue, date, description, category, lat, lng))
else:
    print(f'Failed to retrieve page. Status code: {response.status_code}') 


# Commit and close the connection
conn.commit()
conn.close()