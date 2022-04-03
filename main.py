from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

# TODO: add list of websites to switch between when one website finishes
# TODO: add list of urls to switch between on a website when one execution finishes

url_list = ['https://www.newegg.com/CPUs-Processors/Category/ID-34', 'https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709']

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Accept-Language": "en",
}

url = "https://www.newegg.com/CPUs-Processors/Category/ID-34"

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")
cell = soup.find_all(class_='item-cell') # This is a list

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
"""

title = [item.find(class_="item-title").get_text().split('-')[0] for item in cell] # List comprehension here gets all (full) titles
link = [item.find('a', href=True)['href'] for item in cell]
price = [item.find('li', {'class': 'price-current'}).strong.get_text() for item in cell]

dataset = pd.DataFrame(
    {
        'Title': title,
        'Link': link,
        'Price': price,
    })

dataset.to_excel(r'C:\Users\Exo\Documents\Excel\ComputerPartsData.xlsx', index=False)
print(dataset)

"""
for item in cell:
    link = item.find('a', href=True)
    print(link['href'])

    title = item.find('a', {'class': 'item-title'})
    print(title.text)

    price = item.find('li', {'class': 'price-current'})
    print(price.find('strong').text)
"""