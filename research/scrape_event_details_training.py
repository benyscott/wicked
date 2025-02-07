from autoscraper import AutoScraper

# Creates data to train the AutoScraper, you feed it a URL and an array of items you want to scrape
data = [
   ('https://www.barcelona-metropolitan.com/events/roger-padros/', ['Roger Padrós','Casa Batlló Gaudi Museum Barcelona','https://www.barcelona-metropolitan.com/locations/casa-batll%C3%B3-gaudi-museum-barcelona/','Passeig de Gràcia 43, 08007 Barcelona','Sep 12, 2024 8:00 PM to 10:00 PM','Concerts & Live Music','https://www.casabatllo.es/en/magic-nights/roger/','Lose yourself in the voice, piano and guitar of this Barcelona-born artist who performs hits by Coldplay, Muse, Bruno Mars, Pablo López and Los Ronaldos, as well as songs written by himself.']),
   ('https://www.barcelona-metropolitan.com/events/summer-nights-at-casa-rocamora/', ['Summer Nights at Casa Rocamora','Casa Rocamora','https://www.barcelona-metropolitan.com/locations/casa-rocamora/','Carrer de Ballester 12, 08023 Barcelona','Sep 12, 2024 7:00 PM','Art & Exhibitions, Arts & Culture, Kids & Family','https://www.casessingulars.com/en/visits/casa-rocamora/','This Spanish-Elizabethan palazzo in El Putxet neighborhood houses one of the most highly prized collections of Alcora pottery, and 19th- and 20th-century drawings, paintings and sculptures.']),
   ('https://www.barcelona-metropolitan.com/events/new-urban-imaginaries/', ['New Urban Imaginaries','Centre de Cultura Contemporània de Barcelona (CCCB)','https://www.barcelona-metropolitan.com/locations/centre-de-cultura-contempor%C3%A0nia-de-barcelona-%28cccb%29-/','Carrer de Montalegre 5, 08001 Barcelona','Sep 5, 2024 6:30 PM to 8:00 PM','Art & Exhibitions','https://www.cccb.org/en/activities/file/teresa-caldeira-gautam-bhan-and-nzinga-biegueng-mboup/245568','In this context of profound transformation, the CCCB opens a strategic line on the metropolises of the Global South, the cities that are the home to most of the world\'s population, help to understand the postcolonial present.']),
   ('https://www.barcelona-metropolitan.com/events/massa-critica-bcn/', ['Massa Crítica BCN','l\'Arc de Triomf','https://www.barcelona-metropolitan.com/locations/l%27arc-del-triomf/','Passeig de Sant Joan 1, 08018 Barcelona','Oct 4, 2024 8:00 PM to 10:30 PM','Fitness','http://barcelona.bicicritica.com/en/when-where-critical-mass-barcelona/','Join Critical Mass Barcelona every first Friday of the month and cycle throughout Barcelona!']),
   ('https://www.barcelona-metropolitan.com/events/the-birds/', ['"The Birds"','Filmoteca de Catalunya','https://www.barcelona-metropolitan.com/locations/filmoteca-de-catalunya/','Plaça Salvador Seguí 1-9, 08001 Barcelona','Sep 8, 2024 9:00 PM to 11:40 PM','Film, Film Screenings','https://www.filmoteca.cat/web/ca/film/birds','In Bodega Bay the birds, in an inexplicable way, begin to attack people; they are attacks that call into question the very survival of the human species.']),
   ('https://www.barcelona-metropolitan.com/events/the-sherlock-holmes-collection-at-biblioteca-arus/', ['The Sherlock Holmes Collection at Biblioteca Arús','Biblioteca Pública Arús','https://www.barcelona-metropolitan.com/locations/biblioteca-publica-arus/','Passeig de Sant Joan 26, 08010 Barcelona','Sep 10, 2024 7:00 PM','Education & Learning, History, Kids & Family','https://www.casessingulars.com/en/visits/arus-library/','Enjoy a tour of Joan Proubasta\'s Sherlock Holmes collection. This collection is currently considered the private collection dedicated to the most important figure of Sherlock Holmes in Spain.']),
   ('https://www.barcelona-metropolitan.com/events/festa-de-la-filloxera', ['Festa de la Fil·loxera','Sant Sadurní d\'Anoia','https://www.barcelona-metropolitan.com/locations/sant-sadurni-d-anoia/','Sant Sadurní d\'Anoia','Sep 7, 2024 to Sep 8, 2024','Festivals & Fairs','https://www.festadelafiloxera.cat/','The festival is a popular celebration that recreates the town\'s victory, in 1887, over the terrible phylloxera epidemic that wiped out all the vineyards in the Penedès region.']),
   ('https://www.barcelona-metropolitan.com/events/festa-major-horta/', ['Festa Major d\'Horta 2024','Horta neighborhood, various locations','https://www.barcelona-metropolitan.com/locations/horta-neighborhood-various-locations/','Barcelona','Sep 6, 2024 to Sep 15, 2024','Concerts & Live Music, Festivals & Fairs, Food & Drink, Kids & Family','http://www.festamajor.org/index.html','Horta\'s Festa Major offers activities of all kinds, including dances, concerts, children\'s activities, community meals, sporting events and more!'])
]

scraper = AutoScraper()

# Goes through the training data and builds
for url, wanted_list in data:
   scraper.build(url=url, wanted_list=wanted_list, update=True)

# Saves model locally for future use
scraper.save('bcn-met-3')

### The code commented below is in a Python command line, I can call get_result_exact with a different URL from the same websites, and it tries to pull the right information
# >>> scraper.get_result_exact('https://www.barcelona-metropolitan.com/events/sala-bcn/?occ_dtstart=2024-09-05T20:00', grouped=True)

# Adding grouped=True at the command above ouputs the line below
# {'rule_9b6c': ['Sala BCN'], 'rule_uw8m': ['Sala BCN'], 'rule_vbnj': ['Sala BCN'], 'rule_ghbo': ['Castell de Montjuïc'], 'rule_7yju': ['Castell de Montjuïc'], 'rule_jjpe': ['Carretera de Montjuïc 66, 08038 Barcelona'], 'rule_vofp': ['Carretera de Montjuïc 66, 08038 Barcelona'], 'rule_dapv': ['Concerts & Live Music'], 'rule_08n8': ['2024-08-01T12:55:14.385592'], 'rule_6nak': ['https://salabarcelona.cat/sala-bcn?lang=es'], 'rule_4ws7': ['Enjoy a relaxing evening of outdoor concerts in the Patio de Armas in the Castell de Montjuc!'], 'rule_q81w': ['Enjoy a relaxing evening of outdoor concerts in the Patio de Armas in the Castell de Montjuc!'], 'rule_992j': ['Sala BCN'], 'rule_8n0m': ['Enjoy a relaxing evening of outdoor concerts in the Patio de Armas in the Castell de Montjuc!'], 'rule_3iaz': ['Sala BCN'], 'rule_1m2u': ['Enjoy a relaxing evening of outdoor concerts in the Patio de Armas in the Castell de Montjuc!'], 'rule_hj6x': ['Sep 5, 2024 8:00 PM to 11:00 PM'], 'rule_x96b': ['Concerts & Live Music']}

# Without grouped=True, the ouput is the line below
# ['Sala BCN', 'Metro PublisherTM', 'Castell de Montjuïc', 'Carretera de Montjuïc 66, 08038 Barcelona', 'Concerts & Live Music', 'Festivals & Fairs', 'https://salabarcelona.cat/sala-bcn?lang=es', 'Enjoy a relaxing evening of outdoor concerts in the Patio de Armas in the Castell de Montjuc!', 'article', 'Sep 5, 2024 8:00 PM to 11:00 PM', 'Music']

# In the case below 'rule_9b6c', 'rule_uw8m' and 'rule_vbnj' are the event name
# 'rule_ghbo' and 'rule_7yju' are the event venue
# 'rule_jjpe' and 'rule_vofp' is the venue address 
# 'rule_6nak' is the event URL
# 'rule_4ws7' is the event description
# 'rule_hj6x' is the event date

# How can I scrape multiple URLs at once and push each information in a database?