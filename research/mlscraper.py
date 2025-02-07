import requests
from mlscraper.html import Page
from mlscraper.samples import Sample, TrainingSet
from mlscraper.training import train_scraper

# fetch the page to train
metro1_url = 'https://www.barcelona-metropolitan.com/events/roger-padros/'
resp = requests.get(metro1_url)
assert resp.status_code == 200

# create a sample for Albert Einstein
# please add at least two samples in practice to get meaningful rules!
training_set = TrainingSet()
page = Page(resp.content)

sample = Sample(page, {'title': 'Roger Padrós', 'venue': 'Casa Batlló Gaudi Museum Barcelona', 'address': 'Passeig de Gràcia 43, 08007 Barcelona', 'date-time': 'Sep 5, 2024 8:00 PM to 10:00 PM', 'type': 'Concerts & Live Music'})
training_set.add_sample(sample)

# train the scraper with the created training set
scraper = train_scraper(training_set)

# fetch the page to train
metro2_url = 'https://www.barcelona-metropolitan.com/events/summer-nights-at-casa-rocamora/'
resp = requests.get(metro2_url)
assert resp.status_code == 200

# create a sample for Albert Einstein
# please add at least two samples in practice to get meaningful rules!
training_set2 = TrainingSet()
page2 = Page(resp.content)

sample2 = Sample(page, {'title': 'Summer Nights at Casa Rocamora', 'venue': 'Casa Rocamora', 'address': 'Carrer de Ballester 12, 08023 Barcelona', 'date-time': 'Sep 5, 2024 7:00 PM', 'type': 'Art & Exhibitions, Arts & Culture, Kids & Family'})
training_set2.add_sample(sample2)

# train the scraper with the created training set
scraper = train_scraper(training_set2)

# scrape another page
resp = requests.get('https://www.barcelona-metropolitan.com/events/new-urban-imaginaries/')
result = scraper.get(Page(resp.content))
print(result)
# returns {'name': 'J.K. Rowling', 'born': 'July 31, 1965'}