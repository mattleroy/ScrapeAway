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
Next Task:
Inside scrape data, need to add pagination for hopping between products, and product pages.
This way we can gather main data - (title, price, link) and sub data - (brand, series, cores, threads, etc)

Format new get_functions in WebFunctions.py to get them working with new product pages.
"""

df = pd.read_excel("ComputerPartsData.xlsx")  # Read included Excel sheet to start program.

"""
Series
Cores
Threads
Brand
Max Turbo
Operating Turbo
Socket
"""

def scrape_data():
    page_cap = 1
    while page_cap != 2:
        page = requests.get(NWF.url_changer(page_cap), headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        cell = soup.find_all(class_='item-cell')  # This is a list

        dataset = pd.DataFrame({
            'Title': NWF.get_title(cell),   # There is no loop happening here, remember the dataframe data is gathered via
            'Link': NWF.get_link(cell),     # method within WebFunctions that prints out a list of items from one request
            'Price': NWF.get_price(cell),   # This creates the whole Excel sheet in one go
        })

        def generate_dataframe_data():  # Move function to WebFunctions?
            data = {"Brand": [NWF.get_brand(url) for url in dataset['Link']],
                    "Series": [NWF.get_series(url) for url in dataset['Link']],
                    "Socket": [NWF.get_socket(url) for url in dataset['Link']],
                    "Cores": [NWF.get_cores(url) for url in dataset['Link']],
                    "Threads": [NWF.get_threads(url) for url in dataset['Link']],
                    "Max Frequency": [NWF.get_max_freq(url) for url in dataset['Link']]}
            return data

        dataset2 = pd.DataFrame(generate_dataframe_data())   # Declare dataframe outside of loop. Just add dictionary data to dataframe.
        dataset2.to_csv("oi")

        """In other words, do not form a new DataFrame for each row. Instead,
        collect all the data in a list of dicts, and then call 
        df = pd.DataFrame(data) once at the end, outside the loop.
        
        https://stackoverflow.com/questions/31674557/how-to-append-rows-in-a-pandas-dataframe-in-a-for-loop
        """
        #TODO Work on appending dataset2 to dataset1 in correct locations
        #TODO Continue debugging get_... WebFunctions
        #TODO Get other get_functions operational to pull other sub-data (brand, cores, threads, etc)

        dataset["Price"].fillna("No Price", inplace=True)  # Fill in Null/None values in the Excel sheet

        with ExcelWriter('ComputerPartsData.xlsx', mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            dataset.to_excel(writer, startrow=writer.sheets['Sheet1'].max_row, index=False, sheet_name='Sheet1')
            # arg: startrow=writer.sheets['Sheet1'].max_row is hugely important for appending to the END of the sheet.
            # Without it, it will not work.

            print(dataset.head(10))     # Can be deleted, just visualizes if data is printing.
            #time.sleep(10)             # Sleep here so website isn't throttled with requests.
            page_cap += 1               # Adding 1 to page_cap so while loop ends.


def drop_data():  # This function drops all data within the Excel sheet.
    df = pd.read_excel("ComputerPartsData.xlsx", header=None)
    df.drop(columns=[0, 1, 2], inplace=True, axis=1)        # Dropping all specified rows (first 3).
    with ExcelWriter("ComputerPartsData.xlsx") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        # This ExcelWriter is writing "nothing" to the Excel sheet to erase all existing data.

if df.notnull().values.any():   # This checks if the Excel sheet has existing content, if True, drops all of it.
    drop_data()
else:                           # This will populate data if empty.
    scrape_data()

