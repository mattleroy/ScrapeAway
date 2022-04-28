class NWF:  # Newegg
    def __init__(self, cell):
        self.cell = cell

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
    def get_brand(cls, cell):
        brand = [cell.find_all('td')[1].get_text()]
        return brand

    @classmethod
    def get_series(cls, cell):
        series = [cell.find_all('td')[3].get_text()]
        return series

    @classmethod
    def get_socket(cls, cell):
        socket = [cell.find_all('td')[0].get_text()]
        return socket

    @classmethod
    def get_cores(cls, cell):
        cores = [cell.find_all('td')[1].get_text()]
        return cores

    @classmethod
    def get_threads(cls, cell):
        threads = [cell.find_all('td')[2].get_text()]
        return threads

    @classmethod
    def get_max_freq(cls, cell):
        frequency = [cell.find_all('td')[2].get_text()]
        return frequency

    @classmethod
    def url_changer(cls, page):
        url = "https://www.newegg.com/Processors-Desktops/SubCategory/ID-343?Tid=7671"
        s_url = url.split('?')

        #for i in range(5):
        url = s_url[0] + f"/page-{page}"
        page += 1
        return url

    @classmethod
    def clean_string(cls, string):
        string = string.split(' ')
        return string