from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import ExcelWriter
from fake_useragent import UserAgent
from WebFunctions import NWF
import time
import random
from itertools import zip_longest

# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Original UA
ua = UserAgent().chrome

headers = {
    "User-Agent": ua,
    "Accept-Language": "en",
}
df = pd.read_excel("ComputerPartsData.xlsx")  # Read included Excel sheet to start program.

cpu_url = "https://www.newegg.com/Processors-Desktops/SubCategory/ID-343/page-1"
gpu_url = "https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709"

# 1) choose CPU
# 2) set page_url to cpu_url
# 3)     grab first page, append data to dictionary_data
# 4)     (loop here) repeat until pages are finished
# 5)     append all to DataFrame
# 6)   write DataFrame to Excel
# 7) switch to GPU
# 8) set page_url to gpu_url

def scrape_data():

    page_num = 1
    page_url = cpu_url
    dictionary_data = []  # Declaring list we will be appending data to (Brand, Cores, Threads, etc..)
    prices = []
    link_list = []
    # TODO link_list here?
    # Base url that will be altered at the bottom of while to change pages

    while page_num != 3:

        # This block grabs the initial webpage of all the products
        page = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        cell = soup.find_all(class_='item-cell')                # This is a list
        print("Page Inc: " + str(page_num))

        # This block grabs all the links and prices of the products on the page
        # Used += so that it appends to the link_list var
        prices += NWF.get_price(cell)                            # This is a list of prices
        link_list += NWF.get_link(cell)                         # List of links to loop through

        # This block loops through individual product pages and appends data to our list which is used to create a dict
        page_num += 1   # Increment page
        split_list = page_url.split('/')[:-1]  # TODO Maybe just change this to a string?
        page_url = '/'.join(split_list) + f"/page-{page_num}"

    for url in link_list:                                       # Looping through our list of links established above with link_list
        #time.sleep(random.randrange(2,9))
        html = NWF.page_data(url)                               # page_data returns soup of a given url
        dictionary_data.append(NWF.get_item_attribute(html))    # get_item_attribute returns a list of all relevant data (list of lists, 1 list per item)


    # The data we gathered above is placed into the dictionary declared here
    # But we are just creating the dict here
    # TODO Create dictionary switcher
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


    # TODO Fix ValueError "All arrays must be the same length". The data dictionary has all values equal to 74.
    # TODO However one value (Operating Frequency) equals 71. This causes program to fail.
    dataset = pd.DataFrame(data)  # dataset is the dataframe, data is the dictionary
    # Write DataFrame to Excel sheet
    with ExcelWriter('ComputerPartsData.xlsx', mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        dataset.to_excel(writer, index=False, sheet_name='Sheet1')
        # arg: startrow=writer.sheets['Sheet1'].max_row is hugely important for appending to the END of the sheet.
        # Without it, it will not work. #startrow=writer.sheets['Sheet1'].max_row
        # That line, did however cause an empty row at the top of XL sheet

    # TODO Product changer down here (CPU --> GPU)

"""def drop_data():  # This function drops all data within the Excel sheet.
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

"""
scrape_data()
