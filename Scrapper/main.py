from calendar import c
from unicodedata import category
from requestlib.StandardRequester import Requester
from category.menu.CategoryMenuScrapper import CategoryMenuScrapper
requester = Requester()
response = requester.get_html("https://alcomarket.md/")
catalogue_response = requester.get_html("https://alcomarket.md/ro/catalog")
category_scrapper = CategoryMenuScrapper(
    catalogue_response, "div", "mini-catalog__wrapper")
categories = category_scrapper.get_categories()

print("Proceeding on scrapping category pages")

# for category in categories:
#     print(category)
#     break

vodka = categories[4]
print(vodka)
vodka.get_products(request_module=requester)
