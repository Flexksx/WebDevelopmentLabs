from bs4 import BeautifulSoup


class CategoryPageScrapper:
    def __init__(self, html:str) -> None:
        self.html = html
        

    def get_products(self):
        response = self.request_module.get_html(self.url)
        print(response)
        