from autoscraper import AutoScraper

url = 'https://www.barcelona-metropolitan.com/search/event/upcoming-events/#page=1'
wanted_list = ["https://www.barcelona-metropolitan.com/events/the-sea-a-global-common-good/?occ_dtstart=2024-09-09T18:30","https://www.barcelona-metropolitan.com/events/barcelona-guitar-trio-dance/?occ_dtstart=2024-09-09T20:00"]
               #,"https://www.barcelona-metropolitan.com/events/nika-mills-trio/?occ_dtstart=2024-09-09T20:00","https://www.barcelona-metropolitan.com/events/exploring-the-spaces-between-city-and-sea/?occ_dtstart=2024-09-10T09:30","https://www.barcelona-metropolitan.com/events/barcelona-venice-amsterdam-three-stories-of-city-and-sea/?occ_dtstart=2024-09-10T18:30","https://www.barcelona-metropolitan.com/events/the-sherlock-holmes-collection-at-biblioteca-arus/?occ_dtstart=2024-09-10T19:00","https://www.barcelona-metropolitan.com/events/oriol-valles-quartet/?occ_dtstart=2024-09-10T19:00","https://www.barcelona-metropolitan.com/events/summer-lovers-casa-batllo/?occ_dtstart=2024-09-10T20:00","https://www.barcelona-metropolitan.com/events/oriol-valles-quartet/?occ_dtstart=2024-09-10T20:30","https://www.barcelona-metropolitan.com/events/arte-flamenco/?occ_dtstart=2024-09-10T21:00"]

scraper = AutoScraper()
result = scraper.build(url, wanted_list)
scraper.save('bcn-met-list')

print(result)