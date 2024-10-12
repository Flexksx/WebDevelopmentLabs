from bs4 import BeautifulSoup

from requestlib.Requester import IRequester
from CategoryPageScrapper import CategoryPageScrapper

class CategoryScrapper:
    def __init__(self, html: str, request_module: IRequester) -> None:
        self.html = html
        self.request_module = request_module
        self.name = self.__initialize_name()
        self.url = self.__initialize_url()
        self.pages_urls = []
        # print(f"Initialized Category: {self.name} with url: {self.url}")

    def __initialize_name(self) -> str:
        soup = BeautifulSoup(self.html, "html.parser")
        a_tags = soup.find_all("a")
        if len(a_tags) == 0:
            raise Exception(
                f"Could not initialize Category. No a elements found")
        name = a_tags[0].text.strip()
        return name

    def __initialize_url(self) -> str:
        soup = BeautifulSoup(self.html, "html.parser")
        a_tags = soup.find_all("a")
        if len(a_tags) == 0:
            raise Exception(
                f"Could not initialize Category {self.name}. No a elements found")
        href = a_tags[0].get("href", "").strip()

        if href and "javascript:;" not in href:
            url = f'https://alcomarket.md/{href}'
        else:
            raise Exception(f"Invalid href for {self.name}: contains {
                            href}. Full html: {self.html}")
        return url

    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"Category: {self.name} with url: {self.url}"

    def get_products(self):
        products_list = []
        for page_url in self.pages_urls:
            page_scrapper = CategoryPageScrapper(page_url, self.name)
            products = page_scrapper.get_products()
            products_list.extend(products)

    def get_nr_of_pages(self) -> int:
        return len(self.pages_urls)

    def get_pages_urls(self) -> list[str]:
        response = self.request_module.get_html(self.url)
        soup = BeautifulSoup(response, "html.parser")
        paging_list = soup.find_all("ul", class_="pagging__list")
        if not paging_list:
            raise Exception(
                f"Could not find pagging list for {self.name}")
        paging_list = paging_list[0]
        pages = paging_list.find_all("li")
        if not pages:
            raise Exception(
                f"Could not find pages for {self.name}")
        last_page = pages[-1].text.strip()
        pages_urls = [f"{self.url}?page={
            i}" for i in range(1, int(last_page)+1)]
        return pages_urls
