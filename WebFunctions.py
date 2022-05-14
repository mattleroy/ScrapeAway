import requests
from bs4 import BeautifulSoup


class NWF:  # Newegg
    def __init__(self, cell):
        self.cell = cell

    def get_item_attribute2(cls):
        index = 1
        while index < 3:
            page = requests.get("https://www.newegg.com/amd-ryzen-5-5600-ryzen-5-5000-series/p/N82E16819113736")
            soup = BeautifulSoup(page.text, "html.parser")
            table = soup.find_all('table',
                                  {'class': 'table-horizontal'})  # Returns a list of the tables (Model, Details, etc)
            details = [item.find('tbody') for item in table][index]  # Grabs the "Details" table to process
            table_items = details.find_all('tr')  # Creates list of rows in Model table

            attribute_list = []
            search_list = ["Brand", "# of Cores", "# of Threads", "Frequency", "Socket", "Name"]
            for ind, model_item in enumerate(table_items):  # Gets index and item from "table_items"
                model_item = model_item.find('th').get_text()  # Gets plain-text of row item (Cores, Socket Type, Threads, etc)
                for term in search_list:
                    if term == model_item:
                        attribute_list.append(table_items[ind].find('td').get_text())

            index = 2
            print(attribute_list)

    def space_stripper(cls, word):  # Function created because trailing spaces in HTML text were preventing program from running
        print(word)
        word = word.split(' ')[-1]
        # list[-1] returns last item
        # list.pop() removes last item
        print(word)

    @classmethod
    def get_item_attribute(cls, url, string, ind):
        tb_ind = ind
        soup = cls.page_data(url)                                       # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][tb_ind]           # Grabs the "Details" table to process
        table_items = details.find_all('tr')                            # Creates list of rows in Model table
        for ind, model_item in enumerate(table_items):                  # Gets index and item from "table_items"
            model_item = model_item.find('th').get_text()               # Gets text of row item (Brand, Series, Name, etc)
            if string.capitalize() in model_item:                       # Converts string argument to actual string to search for in HTML
                return table_items[ind].find('td').get_text()           # Returns the description of the string that was passed

    @classmethod
    def page_data(cls, link):
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup  # Returns WHOLE page of HTML, needs further processing to single out more specific data

    @classmethod
    def get_title(cls, cell):
        title = [item.find(class_="item-title").get_text().split('-')[0] for item in cell]
        return title

    @classmethod
    def get_link(cls, cell):
        link = [item.find('a', href=True)['href'] for item in cell]
        return link

    @classmethod
    def get_price(cls, cell):
        price = [item.find('li', {'class': 'price-current'}).get_text() for item in cell]
        return price

    @classmethod
    def get_brand(cls, url):
        soup = cls.page_data(url)                                       # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][1]             # Grabs the "Details" table to process
        brand = details.find_all('td')[0].get_text()                    # Returns "Series" (Ryzen 5, Ryzen 7, etc)
        return brand

    @classmethod
    def get_name(cls, url):
        soup = cls.page_data(url)                                       # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][1]             # Grabs the "Model" table to process
        table_items = details.find_all('tr')                            # Creates list of rows in Model table
        for ind, model_item in enumerate(table_items):                  # Gets index and item from "table_items"
            model_item = model_item.find('th').get_text()               # Gets text of row item (Brand, Series, Name, etc)
            if "Name" in model_item:                                    # Finds where "Name" appears in that loop
                return table_items[ind].find('td').get_text()           # Returns the CPU that matches the "Name"

    @classmethod
    def get_socket(cls, url):
        soup = cls.page_data(url)                                       # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][2]             # Grabs the "Details" table to process
        table_items = details.find_all('tr')                            # Creates list of rows in Model table
        for ind, model_item in enumerate(table_items):                  # Gets index and item from "table_items"
            model_item = model_item.find('th').get_text()               # Gets text of row item (Brand, Series, Name, etc)
            if "Socket" in model_item:                                  # Finds where "Socket" appears in that loop
                return table_items[ind].find('td').get_text()           # Returns the CPU that matches the "Socket"

    @classmethod
    def get_cores(cls, url):
        soup = cls.page_data(url)                                       # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][2]             # Grabs the "Details" table to process
        table_items = details.find_all('tr')                            # Creates list of rows in Model table
        for ind, model_item in enumerate(table_items):                  # Gets index and item from "table_items"
            model_item = model_item.find('th').get_text()               # Gets text of row item (Brand, Series, Name, etc)
            if "Cores" in model_item:                                   # Finds where "Cores" appears in that loop
                return table_items[ind].find('td').get_text()           # Returns the CPU that matches the "Cores"

    @classmethod
    def get_threads(cls, url):
        soup = cls.page_data(url)                                       # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][2]             # Grabs the "Details" table to process
        table_items = details.find_all('tr')                            # Creates list of rows in Model table
        for ind, model_item in enumerate(table_items):                  # Gets index and item from "table_items"
            model_item = model_item.find('th').get_text()               # Gets text of row item (Brand, Series, Name, etc)
            if "Threads" in model_item:                                 # Finds where "Threads" appears in that loop
                return table_items[ind].find('td').get_text()           # Returns the CPU that matches the "Threads"

    @classmethod
    def get_max_freq(cls, url):
        soup = cls.page_data(url)                                       # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][2]             # Grabs the "Details" table to process
        table_items = details.find_all('tr')                            # Creates list of rows in Model table
        for ind, model_item in enumerate(table_items):                  # Gets index and item from "table_items"
            model_item = model_item.find('th').get_text()               # Gets text of row item (Brand, Series, Name, etc)
            if "Frequency" in model_item:                               # Finds where "Frequency" appears in that loop
                return table_items[ind].find('td').get_text()           # Returns the CPU that matches the "Frequency"

    @classmethod
    def url_changer(cls, page):
        url = "https://www.newegg.com/Processors-Desktops/SubCategory/ID-343?Tid=7671"
        s_url = url.split('?')
        url = s_url[0] + f"/page-{page}"
        page += 1
        return url

    @classmethod
    def clean_string(cls, string):
        string = string.split(' ')
        return string