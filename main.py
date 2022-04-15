import csv

from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
from WebFunctions import NWF, Switcher
import time



url_list = ['https://www.newegg.com/Processors-Desktops/SubCategory/ID-343?Tid=7671', 'https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709']

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Accept-Language": "en",
}

for url in url_list: # This will need to be modified to fit other websites, currently working with Newegg

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    cell = soup.find_all(class_='item-cell') # This is a list

    dataset = pd.DataFrame(
    {
            'Title': NWF.get_title(cell),
            'Link': NWF.get_link(cell),
            'Price': NWF.get_price(cell),
        })
    dataset.to_csv('dataset.csv')
    dataset.to_excel(r'C:\Users\Exo\Documents\Excel\ComputerPartsData.xlsx', index=False)
    print(dataset.head(10))


#file = pd.read_csv("dataset.csv")
#print(file)
"""
for item in cell:
    title = [item.find(class_="item-title").get_text().split('-')[0]]
    link = [item.find('a', href=True)['href']]
    price = []
    try:
        price.append(item.find('li', {'class': 'price-current'}).strong.get_text())
    except AttributeError:
        print("No Price Found")
    print(title, link, price)


title = [item.find(class_="item-title").get_text().split('-')[0] for item in cell] # List comprehension here gets all (full) titles
link = [item.find('a', href=True)['href'] for item in cell]
price = [item.find('li', {'class': 'price-current'}).strong.get_text() for item in cell]



for item in cell:
    link = item.find('a', href=True)
    print(link['href'])

    title = item.find('a', {'class': 'item-title'})
    print(title.text)

    price = item.find('li', {'class': 'price-current'})
    print(price.find('strong').text)
"""