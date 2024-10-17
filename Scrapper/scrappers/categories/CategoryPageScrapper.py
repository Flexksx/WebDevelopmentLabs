from bs4 import BeautifulSoup


class CategoryPageScrapper:
    def __init__(self, html: str):
        print("Initializing CategoryPageScrapper")
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")

    def get_products_urls(self):
        product_urls = []
        a_tags = self.soup.find_all("a", class_='product__image')
        for a_tag in a_tags:
            href = a_tag.get("href", "").strip()
            if href:
                product_urls.append(f'https://alcomarket.md{href}')
        return product_urls
