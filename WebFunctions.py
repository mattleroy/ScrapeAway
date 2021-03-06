import requests
from bs4 import BeautifulSoup

# TODO Make "Exclude" command so user can feed in some commands to hide certain products that don't match
# https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709  Graphics cards


class NWF:  # Newegg
    def __init__(self, cell):
        self.cell = cell

    @classmethod
    def page_changer(cls, url):
        page = requests.get(NWF.url_changer(), headers=headers)             # This changes PAGES, NOT items
        soup = BeautifulSoup(page.text, "html.parser")
        cell = soup.find_all(class_='item-cell')                            # This is a list of item listings

    @classmethod
    def item_switcher(cls):
        dictionary_switcher = {
            "CPU": {"cpu_search_list": ["Brand", "# of Cores", "# of Threads", "Operating Frequency", "Max Turbo Frequency", "CPU Socket Type", "Name"]},
            "GPU": {"gpu_search_list": ["Brand", "GPU", "Memory Size", "Memory Type", "HDMI", "DisplayPort", "Max Resolution"]},
        }  # Access nested dict like this: dict[first_key][second_key]

    @classmethod
    def get_item_attribute(cls, parsed_html):
        index = 1
        attribute_list = []
        try:
            price = parsed_html.find(class_='price-current').strong.get_text()
        except AttributeError:
            price = "DNE"
        while index < 3:
            table = parsed_html.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables as html (Model, Details, etc)
            if index == 1:
                search_list = ["Brand", "Name"]
            else:
                search_list = ["# of Cores", "# of Threads", "Operating Frequency", "Max Turbo Frequency", "CPU Socket Type"]
            try:
                details = [item.find('tbody') for item in table][index]     # This grabs the table (Models/Details) as a big html string
                table_items = details.find_all('tr')  # Creates list of rows from above string (still html)
                comparison_list = {}
                for ind, key in enumerate(table_items):
                    key = key.find('th').get_text()
                    value = table_items[ind].find('td').get_text()
                    comparison_list.update({cls.space_stripper(key): value})
                for i in comparison_list.keys():
                    # TODO Somewhere here, figure out how to lessen the amount of items is in the comparison list
                    for j in search_list:
                        if not search_list:  # Is list empty? If so, stop searching.
                            break
                        if i == j:
                            search_list.remove(i)
                            attribute_list.append(comparison_list[j])
                            print('asdasd')
                """for ind, model_item in enumerate(comparison_list):              # Gets index and item from "table_items"
                    if not search_list:  # Is list empty? If so, stop searching.
                        break
                    for term in search_list:                                # Uses the search_list to find the items we want from the site
                        if term ==           # Compares our search_list term to the website term and pulls if matching
                            search_list.remove(term)                        # Removes matching item, so it isn't used again in next search (efficiency)
                            attribute_list.append(table_items[ind].find('td').get_text())  # Append to list"""
            except IndexError:
                print("Trouble grabbing tables")  # This error means the "Details/Models" etc. tables do not exist

            index += 1
        attribute_list.insert(2, price)

        return attribute_list

    @classmethod
    def space_stripper(cls, word):  # Function created because trailing spaces in HTML text were preventing program from running
        word = word.split(' ')
        word.pop()
        word = ' '.join(word)
        return word

    @classmethod
    def page_data(cls, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup  # Returns WHOLE page of HTML, needs further processing to single out more specific data

    @classmethod
    def get_link(cls, cell):  # This takes in a list, and returns a modified one
        link = [item.find('a', href=True)['href'] for item in cell]
        return link

    @classmethod  # UNUSED
    def new_get_link(cls, cell):  # Remember, find will return a result
        link = cell.find('a', href=True)['href']
        return link

    @classmethod
    def get_price(cls, cell):
        try:
            price = [item.find('li', {'class': 'price-current'}).strong.get_text() for item in cell]
        except AttributeError:
            return "DNE"
        return price

    @classmethod
    def url_changer(cls, url, page_num):
        s_url = url.split('/')
        url = s_url[0] + f"/page-{page_num}"
        return url

    @classmethod    # UNUSED METHOD, KEPT FOR REFERENCE
    def get_brand(cls, url):
        soup = cls.page_data(url)                                       # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][1]             # Grabs the "Details" table to process
        brand = details.find_all('td')[0].get_text()                    # Returns "Series" (Ryzen 5, Ryzen 7, etc)
        return brand

    @classmethod    # UNUSED METHOD, KEPT FOR REFERENCE
    def get_name(cls, url):
        soup = cls.page_data(url)                                       # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][1]             # Grabs the "Model" table to process
        table_items = details.find_all('tr')                            # Creates list of rows in Model table
        for ind, model_item in enumerate(table_items):                  # Gets index and item from "table_items"
            model_item = model_item.find('th').get_text()               # Gets text of row item (Brand, Series, Name, etc)
            if "Name" in model_item:                                    # Finds where "Name" appears in that loop
                return table_items[ind].find('td').get_text()           # Returns the CPU that matches the "Name"

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

    """    for item_attr, price in zip(dictionary_data, prices):
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
                data["Max Operating Frequency"].append("DNE")"""