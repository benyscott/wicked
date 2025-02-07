import requests
import sqlite3
import json

# GraphQL endpoint
url = 'https://ra.co/graphql'

# GraphQL query
query = """
query GET_EVENT_LISTINGS($filters: FilterInputDtoInput, $filterOptions: FilterOptionsInputDtoInput, $page: Int, $pageSize: Int, $sort: SortInputDtoInput) {
  eventListings(
    filters: $filters
    filterOptions: $filterOptions
    pageSize: $pageSize
    page: $page
    sort: $sort
  ) {
    data {
      id
      listingDate
      event {
        ...eventListingsFields
        artists {
          id
          name
          __typename
        }
        __typename
      }
      __typename
    }
    filterOptions {
      genre {
        label
        value
        count
        __typename
      }
      eventType {
        value
        count
        __typename
      }
      location {
        value {
          from
          to
          __typename
        }
        count
        __typename
      }
      __typename
    }
    totalResults
    __typename
  }
}

fragment eventListingsFields on Event {
  id
  date
  startTime
  endTime
  title
  contentUrl
  flyerFront
  isTicketed
  interestedCount
  isSaved
  isInterested
  queueItEnabled
  newEventForm
  images {
    id
    filename
    alt
    type
    crop
    __typename
  }
  pick {
    id
    blurb
    __typename
  }
  venue {
    id
    name
    contentUrl
    live
    __typename
  }
  __typename
}
"""

# Variables to pass with the query
variables = {
    "filters": {
        "areas": {"eq": 20},
        "listingDate": {"gte": "2024-09-19", "lte": "2024-09-20"}
    },
    "filterOptions": {
        "genre": True,
        "eventType": True
    },
    "pageSize": 20,
    "page": 1,
    "sort": {
        "listingDate": {"order": "ASCENDING"},
        "score": {"order": "DESCENDING"},
        "titleKeyword": {"order": "ASCENDING"}
    }
}

# Headers (including the user-agent)
headers = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

# Step 1: Make the POST request to the GraphQL endpoint
response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

# Step 2: Check if the request was successful
if response.status_code == 200:
    # Step 3: Parse the response
    data = response.json()
    
    # Optional: Print the JSON data to inspect it
    print(json.dumps(data, indent=2))

    # Step 4: Connect to an SQLite database (or create it)
    conn = sqlite3.connect('events-ra.db')
    cursor = conn.cursor()

    # Step 5: Create a table to store event listings
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events_ra (
        id TEXT PRIMARY KEY,
        event_name TEXT,
        event_date TEXT,
        event_url TEXT,
        start_time TEXT,
        end_time TEXT,
        venue_name TEXT,
        venue_url TEXT,
        genre TEXT
    )
    ''')

    domainName = 'https://ra.co'

    # Step 6: Insert event data into the table
    for item in data['data']['eventListings']['data']:
        event_id = item['event']['id']
        event_name = item['event']['title']
        event_date = item['event']['date']  # Event date
        event_url = domainName + (item['event'].get('contentUrl') or '')  # Event URL
        start_time = item['event'].get('startTime', None)  # Start time (if exists)
        end_time = item['event'].get('endTime', None)  # End time (if exists)
        venue_name = item['event']['venue']['name']  # Venue name
        venue_url = domainName + (item['event']['venue'].get('contentUrl') or '')
        genre = ', '.join([g['label'] for g in item.get('filterOptions', {}).get('genre', [])])  # Event genre

        cursor.execute('''
        INSERT OR IGNORE INTO events_ra (id, event_name, event_date, event_url, start_time, end_time, venue_name, venue_url, genre)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (event_id, event_name, event_date, event_url, start_time, end_time, venue_name, venue_url, genre))

    # Step 7: Commit the transaction and close the connection
    conn.commit()
    conn.close()

else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
