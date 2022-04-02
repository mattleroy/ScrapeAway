from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.newegg.com/p/pl?Submit=StoreIM&Category=34&Depa=1"

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

cell = soup.find_all(class_='item-cell') # This is a list

brand = cell[0].find(class_='item-title').get_text().split(' ')


for item in cell:
    title = item.find(class_="item-title").get_text().split('-')[0]
    link = item.find('a', href=True)['href']
    price = item.find('li', {'class': 'price-current'}).strong.get_text()
    print(title, link, price)





"""
title = [item.find(class_="item-title").get_text() for item in cell] # List comprehension here gets all (full) titles
link = [item.find('a', href=True)['href'] for item in cell]
price = [item.find('li', {'class': 'price-current'}).strong.get_text() for item in cell]

dataset = pd.DataFrame(
    {
        'Title': title,
        'Link': link,
        'Price': price,
    })

dataset.to_csv('CPU.csv')

#if "Ryzen" in brand:
#    ryzen = brand.index("Ryzen")
#elif "Intel" in brand:
#    intel = brand.index("Intel")

for item in cell:
    link = item.find('a', href=True)
    print(link['href'])

    title = item.find('a', {'class': 'item-title'})
    print(title.text)

    price = item.find('li', {'class': 'price-current'})
    print(price.find('strong').text)
"""