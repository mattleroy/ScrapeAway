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
        while index < 3:
            table = parsed_html.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
            try:
                details = [item.find('tbody') for item in table][index]     # Grabs whatever table the index passed gets from the list above
                table_items = details.find_all('tr')                        # Creates list of rows from Model table
                # Strings MUST be exactly matching Newegg table (Line below)
                search_list = ["Brand", "# of Cores", "# of Threads", "Operating Frequency", "Max Turbo Frequency", "CPU Socket Type", "Name"]
                for ind, model_item in enumerate(table_items):              # Gets index and item from "table_items"
                    model_item = model_item.find('th').get_text()           # Gets plain-text of row item (Cores, Brand, Socket Type, Threads, etc)
                    for term in search_list:                                # Uses the search_list to find the items we want from the site
                        if term == cls.space_stripper(
                                model_item):                                # Compares our search_list term to the website term and pulls if matching
                            attribute_list.append(table_items[ind].find('td').get_text())  # Append to list
            except IndexError:
                print("Trouble grabbing tables")


            index += 1
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
    def get_link(cls, cell):
        link = [item.find('a', href=True)['href'] for item in cell]
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