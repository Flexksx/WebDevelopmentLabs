from bs4 import BeautifulSoup


class CategoryPageScrapper:
    def __init__(self, url) -> None:
        self.url = url
