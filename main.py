import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
from openpyxl import Workbook
from pandas import ExcelWriter
import openpyxl
from WebFunctions import NWF
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Accept-Language": "en",
}

"""
Next task:
Detect if there is data in cell 1, if there is - drop data
If there isn't scrape data.
"""

"""if not pd.isnull(df.loc[1, 'Title']):  # This checks if cell 1 has a value
    print("It is populated")
else:
    print("It is empty")"""

def scrape_data():
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

        with ExcelWriter('ComputerPartsData.xlsx', mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            dataset.to_excel(writer, startrow=writer.sheets['Sheet1'].max_row, index=False, sheet_name='Sheet1')  # arg: startrow=writer.sheets['Sheet1'].max_row is hugely important for appending to the END of the sheet. Without it, it will not work.
            print(dataset.head(10))
            #time.sleep(10)
            page_cap += 1

def drop_data():  # This function drops all data within the Excel sheet.
    df = pd.read_excel("ComputerPartsData.xlsx", header=None)
    df.drop(columns=[0, 1, 2], inplace=True, axis=1)
    with ExcelWriter("ComputerPartsData.xlsx") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")

