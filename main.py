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

    #TODO Fix pagination. Program currently does not change pages correctly - or it overwrites data from the newest page
    while page_num != 2:

        # This block grabs the initial webpage of all the products
        page = requests.get(NWF.url_changer(url, page_num), headers=headers)    # This changes pages
        soup = BeautifulSoup(page.text, "html.parser")
        cell = soup.find_all(class_='item-cell')                                # This is a list
        prices = NWF.get_price(cell)  # This is a list of prices

        # This block grabs all the links of the products on the page, and feeds it into a list to loop through
        link_list = NWF.get_link(cell)                              # List of links to loop through
        dictionary_data = []                                        # Declaring list we will be appending data to (Brand, Cores, Threads, etc..)

        # This block loops through individual product pages and appends data to our list which is used to create a dict
        for url in link_list:                                       # Looping through our list of links established above with link_list
            html = NWF.page_data(url)                               # page_data returns soup of a given url
            dictionary_data.append(NWF.get_item_attribute(html))    # get_item_attribute returns a list of all relevant data

        # The data we gathered above is placed into the dictionary declared here
        # But we are just creating the dict here
        data = {"Brand": [],
                "Name": [],
                "Price": [],
                "Socket": [],
                "Cores": [],
                "Threads": [],
                "Operating Frequency": [],
                "Max Operating Frequency": [],
                }

        # This block appends all the data from dictionary_data to our new data dict above. This is for use in a DataFrame
        # Using the zip method to loop through both the price list and the dictionary data.
        for item_attr, price in zip(dictionary_data, prices):
            try:
                data["Brand"].append(item_attr[0])
                data["Name"].append(item_attr[1])
                data["Price"].append("$" + price)
                data["Socket"].append(item_attr[2])
                data["Cores"].append(item_attr[3])
                data["Threads"].append(item_attr[4])
                data["Operating Frequency"].append(item_attr[5])
                data["Max Operating Frequency"].append(item_attr[6])
            except IndexError:
                data["Max Operating Frequency"].append("DNE")

        page_num += 1   # Increment page
        dataset = pd.DataFrame(data)  # dataset is the dataframe, data is the dictionary

        # Write DataFrame to Excel sheet
        with ExcelWriter('ComputerPartsData.xlsx', mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            dataset.to_excel(writer, index=False, sheet_name='Sheet1')
            # arg: startrow=writer.sheets['Sheet1'].max_row is hugely important for appending to the END of the sheet.
            # Without it, it will not work. #startrow=writer.sheets['Sheet1'].max_row
            # That line, did however cause an empty row at the top of XL sheet

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
"""

        #dataset.insert(0, "Brand", data['Brand'])
        #dataset["Price"].fillna("No Price", inplace=True)  # Fill in Null/None values in the Excel sheet

def drop_data():  # This function drops all data within the Excel sheet.
    df = pd.read_excel("ComputerPartsData.xlsx")
    column_count = df.shape                                 # Returns tuple of ordered pair of (rows, columns) This is for the next line
    cols = [i for i in range(0, column_count[1])]           # Comprehension to set how many columns exist in sheet
    df.drop(df.columns[cols], inplace=True, axis=1)         # Drops the number of columns specified by cols
    with ExcelWriter("ComputerPartsData.xlsx") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        # This ExcelWriter is writing "nothing" to the Excel sheet to erase all existing data.

if df.notnull().values.any():   # This checks if the Excel sheet has existing content, if True, drops all of it.
    drop_data()
else:                           # This will populate data if empty.
    scrape_data()

