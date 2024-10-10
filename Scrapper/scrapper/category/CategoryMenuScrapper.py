from time import sleep
from bs4 import BeautifulSoup
from .Category import Category
import tqdm


class CategoryMenuScrapper:
    def __init__(self, html, html_tag: str, tag_class: str) -> None:
        soup = html = BeautifulSoup(html, "html.parser")
        elements = soup.find_all(html_tag, class_=tag_class)
        if len(elements) == 0:
            raise Exception(
                "Could not initialize Category Scrapper. No elements found with the specified tag and class")
        self.html = str(elements)
        self.html_tag = html_tag
        self.tag_class = tag_class

    def get_categories(self) -> list[Category]:
        soup = BeautifulSoup(self.html, "html.parser")
        categories = soup.find_all("li")
        categories_list = []
        with tqdm.tqdm(total=len(categories), desc="Scraping categories") as progress_bar:
            for category in categories:
                try:
                    category_obj = Category(str(category))
                    categories_list.append(category_obj)
                except Exception as e:
                    print(f"Error processing category: {e}")
                finally:
                    progress_bar.update(1)
        print(f"Successfully scraped {len(categories_list)} out of {
              len(categories)} categories")
        return categories_list
