from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from tqdm import tqdm
from scrappers.products.ProductPageScrapper import ProductPageScrapper
from requestlib.Requester import IRequester
from .CategoryPageScrapper import CategoryPageScrapper
from models.Category import Category


class CategoryScrapper:
    def __init__(self, html: str, request_module: IRequester) -> None:
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")
        self.request_module = request_module
        self.name = self.__scrap_name()
        self.url = self.__scrap_url()
        self.category = Category(self.name, self.url)
        self.pages_urls = []
        self.product_urls = []

    def __scrap_name(self) -> str:
        a_tags = self.soup.find_all("a")
        if len(a_tags) == 0:
            raise Exception(
                f"Could not initialize Category. No a elements found")
        name = a_tags[0].text.strip()
        return name

    def __scrap_url(self) -> str:
        a_tags = self.soup.find_all("a")
        if len(a_tags) == 0:
            raise Exception(f"Could not initialize Category {
                            self.name}. No a elements found")
        href = a_tags[0].get("href", "").strip()

        if href and "javascript:;" not in href:
            url = f'https://alcomarket.md/{href}'
        else:
            raise Exception(f"Invalid href for {self.name}: contains {
                            href}. Full html: {self.html}")
        return url

    def get_product_urls(self):
        if len(self.pages_urls) == 0:
            self.pages_urls = self.get_pages_urls()
        products_list = []
        for page_url in self.pages_urls:
            category_page_html = self.request_module.get_html(page_url)
            print(f"Scraping page {page_url}")
            category_page_scrapper = CategoryPageScrapper(category_page_html)
            products = category_page_scrapper.get_products_urls()
            products_list.extend(products)
        self.product_urls = products_list
        return products_list

    def get_products(self):
        if len(self.product_urls) == 0:
            self.product_urls = self.get_product_urls()

        products = []

        max_workers = 20

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(
                self.scrape_product, url): url for url in self.product_urls}
            with tqdm(total=len(self.product_urls), desc="Scraping products") as progress_bar:
                for future in as_completed(future_to_url):
                    product_url = future_to_url[future]
                    try:
                        product_info = future.result()
                        if product_info:
                            products.append(product_info)
                    except Exception as e:
                        print(f"Error processing product {product_url}: {e}")
                    progress_bar.update(1)

        print(f"Successfully scraped {len(products)} products out of {
              len(self.product_urls)}")
        self.category.set_products(products)
        return products

    def scrape_product(self, product_url: str):
        product_html = self.request_module.get_html(product_url)
        product_page_scrapper = ProductPageScrapper(product_html, product_url)
        return product_page_scrapper.get_product()

    def get_nr_of_pages(self) -> int:
        return len(self.pages_urls)

    def get_pages_urls(self) -> list[str]:
        response = self.request_module.get_html(self.url)
        soup = BeautifulSoup(response, "html.parser")
        paging_list = soup.find_all("ul", class_="pagging__list")
        if not paging_list:
            raise Exception(f"Could not find pagging list for {self.name}")
        paging_list = paging_list[0]
        pages = paging_list.find_all("li")
        if not pages:
            raise Exception(f"Could not find pages for {self.name}")
        last_page = pages[-1].text.strip()
        pages_urls = [f"{self.url}?page={
            i}" for i in range(1, int(last_page) + 1)]
        self.pages_urls = pages_urls
        return pages_urls

    def get_model(self) -> Category:
        return self.category
