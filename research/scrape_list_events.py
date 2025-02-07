from autoscraper import AutoScraper

scraper = AutoScraper()
scraper.load('bcn-met-list')

result = scraper.get_result_similar(input('Enter Barcelona Metropolitan list of events: '))

print(result)