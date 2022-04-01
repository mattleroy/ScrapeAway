from bs4 import BeautifulSoup
import requests

url = "https://www.newegg.com/p/pl?Submit=StoreIM&Category=34&Depa=1"

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

cell = soup.find_all(class_='item-cell') # This is a list

title = cell.find(class_='item-title')
link = [cell.find('a', href=True) for li in cell]
price = [cell.find('li', {'class': 'price-current'}) for pr in cell]

print(title)
print(link)
print(price)






"""
for item in cell:
    link = item.find('a', href=True)
    print(link['href'])

    title = item.find('a', {'class': 'item-title'})
    print(title.text)

    price = item.find('li', {'class': 'price-current'})
    print(price.find('strong').text)
"""