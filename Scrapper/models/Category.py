from .Product import Product


class Category:
    def __init__(self, name: str, url: str, pages_urls: list[str], products: list[Product]) -> None:
        self.name = name
        self.url = url
        self.pages_urls = pages_urls
        self.products = products
