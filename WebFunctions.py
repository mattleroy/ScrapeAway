import requests
from bs4 import BeautifulSoup


class NWF:  # Newegg
    def __init__(self, cell):
        self.cell = cell

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
        soup = cls.page_data(url)  # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][1]             # Grabs the "Details" table to process
        brand = [details.find_all('td')[0].get_text()]                  # Returns "Series" (Ryzen 5, Ryzen 7, etc)
        return brand

    @classmethod
    def get_series(cls, url):
        soup = cls.page_data(url)  # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][1]             # Grabs the "Details" table to process
        series = details.find_all('td')[3].get_text()                   # Returns "Series" (Ryzen 5, Ryzen 7, etc)
        return series

    @classmethod
    def get_socket(cls, url):
        soup = cls.page_data(url)  # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][2]             # Grabs the "Details" table to process
        if "Socket" in details.find("th").get_text():                   # Looks for matching "Socket" text to grab that item and pull the text
            socket = details.find('td').get_text()
            return socket
        else:
            return "Socket Not Found"

    # th holds brand
    # td holds AMD

    @classmethod
    def get_cores(cls, url):
        soup = cls.page_data(url)  # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][2]             # Grabs the "Details" table to process
        if "of Cores" in details.find("th").get_text():                   # Looks for matching "Cores" text to grab that item and pull the text
            cores = details.find('td').get_text()
            return cores
        else:
            return "Cores Not Found"

    @classmethod
    def get_threads(cls, url):
        soup = cls.page_data(url)  # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][2]             # Grabs the "Details" table to process
        if "of Threads" in details.find("th").get_text():               # Looks for matching "Threads" text to grab that item and pull the text
            threads = details.find('td').get_text()
            return threads
        else:
            return "Threads Not Found"

    @classmethod
    def get_max_freq(cls, url):
        soup = cls.page_data(url)  # Calling function to grab new URL for scraping the 'Specs' tables.
        table = soup.find_all('table', {'class': 'table-horizontal'})   # Returns a list of the tables (Model, Details, etc)
        details = [item.find('tbody') for item in table][2]             # Grabs the "Details" table to process
        if "Turbo" in details.find("th").get_text():                    # Looks for matching "Turbo" text to grab that item and pull the text
            max_frequency = details.find('td').get_text()
            return max_frequency
        else:
            return "Frequency Not Found"

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