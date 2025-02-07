import requests
import sqlite3
import json

# GraphQL endpoint
url = 'https://ra.co/graphql'

# GraphQL query
query = """
query GET_EVENT_DETAIL($id: ID!, $isAuthenticated: Boolean!, $canAccessPresale: Boolean!) {\n  event(id: $id) {\n    id\n    title\n    flyerFront\n    flyerBack\n    content\n    minimumAge\n    cost\n    contentUrl\n    embargoDate\n    date\n    time\n    startTime\n    endTime\n    interestedCount\n    lineup\n    isInterested\n    isSaved\n    isTicketed\n    isFestival\n    dateUpdated\n    resaleActive\n    newEventForm\n    datePosted\n    hasSecretVenue\n    live\n    canSubscribeToTicketNotifications\n    images {\n      id\n      filename\n      alt\n      type\n      crop\n      __typename\n    }\n    venue {\n      id\n      name\n      address\n      contentUrl\n      live\n      area {\n        id\n        name\n        urlName\n        country {\n          id\n          name\n          urlCode\n          isoCode\n          __typename\n        }\n        __typename\n      }\n      location {\n        latitude\n        longitude\n        __typename\n      }\n      __typename\n    }\n    promoters {\n      id\n      name\n      contentUrl\n      live\n      hasTicketAccess\n      tracking(types: [PAGEVIEW]) {\n        id\n        code\n        event\n        __typename\n      }\n      __typename\n    }\n    artists {\n      id\n      name\n      contentUrl\n      urlSafeName\n      __typename\n    }\n    pick {\n      id\n      blurb\n      author {\n        id\n        name\n        imageUrl\n        username\n        contributor\n        __typename\n      }\n      __typename\n    }\n    promotionalLinks {\n      title\n      url\n      __typename\n    }\n    tracking(types: [PAGEVIEW]) {\n      id\n      code\n      event\n      __typename\n    }\n    admin {\n      id\n      username\n      __typename\n    }\n    tickets(queryType: AVAILABLE) {\n      id\n      title\n      validType\n      onSaleFrom\n      priceRetail\n      isAddOn\n      currency {\n        id\n        code\n        __typename\n      }\n      __typename\n    }\n    standardTickets: tickets(queryType: AVAILABLE, ticketTierType: TICKETS) {\n      id\n      validType\n      __typename\n    }\n    userOrders @include(if: $isAuthenticated) {\n      id\n      rAOrderNumber\n      __typename\n    }\n    playerLinks {\n      id\n      sourceId\n      audioService {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    childEvents {\n      id\n      date\n      isTicketed\n      __typename\n    }\n    genres {\n      id\n      name\n      slug\n      __typename\n    }\n    setTimes {\n      id\n      lineup\n      status\n      __typename\n    }\n    area {\n      ianaTimeZone\n      __typename\n    }\n    presaleStatus\n    isSignedUpToPresale @include(if: $canAccessPresale)\n    ticketingSystem\n    __typename\n  }\n}\n
"""

# Variables to pass with the query
variables =  {
        "id": "1989292",
        "isAuthenticated": False,
        "canAccessPresale": False
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

else:
    print(f"Request failed with status code {response.status_code}: {response.text}")

def incase():
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
