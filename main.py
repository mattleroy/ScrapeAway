import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
from openpyxl import Workbook
from pandas import ExcelWriter
import openpyxl
from WebFunctions import NWF
import time
from itertools import zip_longest

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Accept-Language": "en",
}
df = pd.read_excel("ComputerPartsData.xlsx")  # Read included Excel sheet to start program.

def scrape_data():

    #  Base url that will be altered at the bottom of while to change pages
    url = "https://www.newegg.com/Processors-Desktops/SubCategory/ID-343?Tid=7671"
    page_num = 1


    while page_num != 2:

        page = requests.get(NWF.url_changer(url, page_num), headers=headers)    # This changes PAGES, NOT items
        soup = BeautifulSoup(page.text, "html.parser")
        cell = soup.find_all(class_='item-cell')                                # This is a list of item listings

        link_list = NWF.get_link(cell)  # List of links to loop through


        dictionary_data = []            # List of lists of data - (AMD, Ryzen 5 5600, Socket AM4, etc....)

        for url in link_list:           # page_data finds entire page html, get_item_attribute finds item specific html
            html = NWF.page_data(url)
            dictionary_data.append(NWF.get_item_attribute(html))

        data = {"Brand": [],
                "Name": [],
                "Socket": [],
                "Cores": [],
                "Threads": [],
                "Operating Frequency": [],
                "Max Operating Frequency": [],
                }


        for item_attr in dictionary_data:
            try:
                data["Brand"].append(item_attr[0])
                data["Name"].append(item_attr[1])
                data["Socket"].append(item_attr[2])
                data["Cores"].append(item_attr[3])
                data["Threads"].append(item_attr[4])
                data["Operating Frequency"].append(item_attr[5])
                data["Max Operating Frequency"].append(item_attr[6])
            except IndexError:
                data["Max Operating Frequency"].append("DNE")



        page_num += 1

scrape_data()
"""
        
        data = pd.DataFrame({
            "a":[1,2,3,4],
            "b":[5,6,7,8],
            })
        
        data2 = pd.DataFrame({
            'c':[12,2414141414143,34,45],
            'd':[56,67,78,89],
            })
        
        data.insert(0,'column_name',data2['c'])
        

        # Declare dataframe outside of loop. Just add dictionary data to dataframe.

        #dataset.insert(0, "Brand", data['Brand'])

        In other words, do not form a new DataFrame for each row. Instead,
        collect all the data in a list of dicts, and then call 
        df = pd.DataFrame(data) once at the end, outside the loop.
        
        https://stackoverflow.com/questions/31674557/how-to-append-rows-in-a-pandas-dataframe-in-a-for-loop
        

        #dataset["Price"].fillna("No Price", inplace=True)  # Fill in Null/None values in the Excel sheet

        with ExcelWriter('ComputerPartsData.xlsx', mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            dataset.to_excel(writer, startrow=writer.sheets['Sheet1'].max_row, index=False, sheet_name='Sheet1')
            # arg: startrow=writer.sheets['Sheet1'].max_row is hugely important for appending to the END of the sheet.
            # Without it, it will not work.

            print(dataset.head(10))     # Can be deleted, just visualizes if data is printing.
            #time.sleep(10)             # Sleep here so website isn't throttled with requests.
            page_cap += 1               # Adding 1 to page_cap so while loop ends.

def drop_data():  # This function drops all data within the Excel sheet.
    df = pd.read_excel("ComputerPartsData.xlsx", header=None)
    df.drop(columns=[0, 1, 2, 3, 4, 5, 6, 7], inplace=True, axis=1)        # Dropping all specified rows (first 3).
    with ExcelWriter("ComputerPartsData.xlsx") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        # This ExcelWriter is writing "nothing" to the Excel sheet to erase all existing data.

if df.notnull().values.any():   # This checks if the Excel sheet has existing content, if True, drops all of it.
    drop_data()
else:                           # This will populate data if empty.
    scrape_data()

"""