import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

headers = {'Accept-Language':'fr-FR,fr;q=0.5'}
url = 'https://www.imdb.com/search/title/?title_type=feature&primary_language=fr'
page = requests.get(url, headers=headers)
Soupe = BS(page.text, 'lxml')

Titles = list()
Year = list()
Time = list()
Genre = list()
Classification = list()
Rate_metascore = list()

counter = 0
while counter < 50:
    block = Soupe.find_all('div', class_ = 'article')[0]
    block_films = block.find('div', class_ = 'lister list detail sub-list')
    list_films = block_films.find('div', class_ = 'lister-list')
    content = list_films.find_all('div', class_ = 'lister-item-content')
    for j in content:
        title_bar = j.find_all('h3')[0]
        Titles.append(title_bar.find('a').text)
        Year.append(j.find_all('span', class_ = 'lister-item-year text-muted unbold')[0].text)
        details = j.find_all('p', class_ = 'text-muted')[0]
        rating_bar = j.find('div', class_ = 'ratings-bar')
        try:
            metascore = rating_bar.find('div', class_='inline-block ratings-metascore')
            Rate_metascore.append((metascore.find('span').text).strip())
        except:
            Rate_metascore.append('')
        try:
            Classification.append(rating_bar.find('strong').text)
        except:
            Classification.append('')
        try:
            Time.append((details.find('span', class_ = 'runtime').text).strip())
        except:
            Time.append('')
        try:
            Genre.append((details.find('span', class_='genre').text).strip())
        except:
            Genre.append('')

    next_page = block.find_all('div', class_ = 'desc')[0]
    button = next_page.find('a', class_ = 'lister-page-next next-page').get('href')
    next_website = ('https://www.imdb.com'+ button)
    page = requests.get(next_website)
    Soupe = BS(page.text, 'lxml')

    counter += 1

df = pd.DataFrame({'Titles': Titles,
                  'Year': Year,
                   'Time': Time,
                   'Genre': Genre,
                   'Classification': Classification,
                   'Rate_metascore': Rate_metascore})
print(df)
df.to_csv('WebScrapingTable/IMDB_français.csv')