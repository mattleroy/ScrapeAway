import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import ExcelWriter
import openpyxl
from WebFunctions import NWF
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Accept-Language": "en",
}

page_cap = 1

while page_cap != 6:
    page = requests.get(NWF.url_changer(page_cap), headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    cell = soup.find_all(class_='item-cell')  # This is a list

    dataset = pd.DataFrame(
    {
            'Title': NWF.get_title(cell),
            'Link': NWF.get_link(cell),
            'Price': NWF.get_price(cell),
    })

    dataset["Price"].fillna("No Price", inplace=True)  # Fill in Null/None values in the Excel sheet

    with ExcelWriter(r'C:\Users\Exo\Documents\Excel\ComputerPartsData.xlsx', mode='a', if_sheet_exists='overlay') as writer:
        dataset.to_excel(writer, startrow=0, header=None, index=False, sheet_name='Sheet1')
    print(dataset.head(10))
    time.sleep(10)
    page_cap += 1
