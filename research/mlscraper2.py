from mlscraper import MultiItemScraper
from mlscraper.training import MultiItemPageSample

# the items found on the training page
items = [
    {'title': 'Roger Padrós', 'venue': 'Casa Batlló Gaudi Museum Barcelona', 'date-time': 'Sep 5, 2024 8:00 PM to 10:00 PM', 'type': 'Concerts & Live Music','excerpt':'Lose yourself in the voice, piano and guitar of this Barcelona-born artist who performs hits by Coldplay, Muse, Bruno Mars, Pablo López and Los Ronaldos, as well as songs written by himself.'},
    {'title': 'The Mystery Man', 'venue': 'Basílica Santa Maria del Pi', 'date-time': 'Sep 5, 2024 - Dec 8, 2024', 'type': 'Art & Exhibitions, Arts & Culture, Religion & Spirituality','excerpt':'The exhibition offers a comprehensive exploration of the Shroud of Turin and breaks down the most important aspects of one of history’s great enigmas: Who was the man in the Holy Shroud?'},
    {'title': 'The Wave Pictures', 'venue': 'Sala Razzmatazz', 'date-time': 'Sep 5, 2024 8:30 PM - 10:30 PM', 'type': 'Concerts & Live Music','excerpt':'The British band The Wave Pictures will review their extensive discography, full of milestones of lo-fi rock, full of attitude and inoculated against fleeting trends.'}
]

html = "https://www.barcelona-metropolitan.com/search/event/upcoming-events/#page=1"
new_html="https://www.barcelona-metropolitan.com/search/event/upcoming-events/#page=2"

# training the scraper with the items
sample = MultiItemPageSample(html, items)
scraper = MultiItemScraper.build([sample])
scraper.scrape(html)  # will produce the items above
scraper.scrape(new_html)  # will apply the learned rules and extract new itemsx