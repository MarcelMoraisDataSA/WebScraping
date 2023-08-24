import requests
from bs4 import BeautifulSoup as BS
import re
import pandas as pd
from collections.abc import Iterable

#PREMIER LEAGUE TABLE WEBSCRAPING (2023/2024)#:


#Getting URL:
url = 'https://www.premierleague.com/tables?co=1&se=489&ha=-1'
html = requests.get(url)
Soupe = BS(html.text, 'lxml')

#Getting where the table is located on HTML:
Table = Soupe.find_all('table')[0]
Head = Soupe.find('thead')
Titles = Head.find('tr')
kalimaat = Titles.find_all('th')

#Headers (attributes of the table():
headers = list()
for n in kalimaat:
    grands = n.find_all('div', class_ = 'league-table__thFull thFull')
    for j in grands:
        if re.search('\w', j.text):
            headers.append(j.text)
    petits = n.find_all('abbr')
    for p in petits:
        headers.append(p.text)
    if n.text == 'Form':
        headers.append(n.text)

df = pd.DataFrame(columns = headers)

#Tranforing nested list into lists:
def flattering(liste):
    for item in liste:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for l in flattering(item):
                yield(l)
        else:
            yield(item)

#Data of table(rows)
row = list()
Body = Table.find_all('tbody', class_ = 'league-table__tbody')[0]
data = Body.find_all('tr', {'data-filtered-entry-size':'20'})
for q in data:
    row.append(q.find_all('span', class_='league-table__value value')[0].text)
    row.append(q.find_all('span', class_ = 'league-table__team-name league-table__team-name--long long')[0].text)
    infos = q.find_all('td', string=True)
    row.append([i.text for i in infos])
#Addind row into de dataframe
    row = list(flattering(row))
    position_index = row[0]
    df.loc[position_index] = row
    row = list()
print(df)

#Converting data frame into xlsx and csv:
df.to_csv('WebScrapingTable/PremierLeagueTable.xlsx')
df.to_csv('WebScrapingTable/PremierLeagueTable.csv')

#                         Made by:
#                                  Marcelo Santos de Morais
#                         GitHub:
#                                  https://github.com/MarcelMoraisDataSA
#                         email:
#                                  marcelmoraisdatasa@gmail.com