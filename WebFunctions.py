url_list = ['https://www.newegg.com/Processors-Desktops/SubCategory/ID-343?Tid=7671', 'https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709']

class Switcher:  # Switches between websites when finished scraping

    def __init__(self, new_url):
        self.new_url = new_url

    @classmethod
    def url_switcher(cls):  # Switches between URLS
        for url in url_list:
            return url


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
        price = [item.find('li', {'class': 'price-current'}).strong.get_text() for item in cell]
        return price

    @classmethod
    def url_changer(cls):
        url = "https://www.newegg.com/Processors-Desktops/SubCategory/ID-343?Tid=7671"
        s_url = url.split('?')
        page = 1

        for i in range(5):
            url = s_url[0] + f"/page-{page}"
            page += 1
            return url