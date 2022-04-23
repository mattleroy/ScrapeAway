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
        price = [item.find('li', {'class': 'price-current'}).strong for item in cell]
        return price

    @classmethod
    def url_changer(cls, page):
        url = "https://www.newegg.com/Processors-Desktops/SubCategory/ID-343?Tid=7671"
        s_url = url.split('?')

        for i in range(5):  # Only scraping 5 pages
            url = s_url[0] + f"/page-{page}"
            page += 1
            return url


