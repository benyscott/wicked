import sqlite3
from autoscraper import AutoScraper

# Connect to SQLite database (or create it)
conn = sqlite3.connect('events.db')
cursor = conn.cursor()

# Create table for events if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_name TEXT, 
                    venue TEXT, 
                    address TEXT, 
                    date TEXT, 
                    category TEXT, 
                    url TEXT, 
                    description TEXT
                    UNIQUE(event_name, date)
                 )''')

# Data to scrape
data = []

scraper = AutoScraper()
scraper.load('bcn-met-3')

for url in data:
    # Extract the data (modify the list index based on the correct fields)
    result = scraper.get_result_exact(url, grouped=True)

    print(result)

    # Assuming the first match is correct for this example
    event_name = result.get('rule_i41t')[0] if result.get('rule_i41t') else ''
    venue = result.get('rule_kyr1')[0] if result.get('rule_kyr1') else ''
    address = result.get('rule_mq31')[0] if result.get('rule_mq31') else ''
    date = result.get('rule_3yod')[0] if result.get('rule_3yod') else ''
    category = result.get('rule_lw6h')[0] if result.get('rule_lw6h') else ''
    event_url = result.get('rule_ysx1')[0] if result.get('rule_ysx1') else ''
    description = result.get('rule_8hgs')[0] if result.get('rule_8hgs') else ''

    # Assuming we're printing each rule and its value in the result
    print(f"Scraping results for URL: {url}")
    for rule, values in result.items():
        print(f"Rule: {rule}")
        for value in values:
            print(f" - {value}")

    print("\n")  # Add space between different URL results

    # Insert into database
    cursor.execute('''INSERT OR IGNORE INTO events (event_name, venue, address, date, category, url, description) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                      (event_name, venue, address, date, category, event_url, description))
    

# Commit and close the database connection
conn.commit()
conn.close()