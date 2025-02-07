from autoscraper import AutoScraper

url = input('Enter Barcelona Metropolitan event: ')

scraper = AutoScraper()
scraper.load('bcn-met-2')

result = scraper.get_result_exact(url)
print(result)
