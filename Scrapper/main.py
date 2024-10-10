from calendar import c
from unicodedata import category
from requestlib import Requester
from scrapper.category.menu.CategoryMenuScrapper import CategoryMenuScrapper
requester = Requester()
response = requester.get_html("https://linella.md/ro")
category_scrapper = CategoryMenuScrapper(response, "ul", "catalog__body_index")
categories = category_scrapper.get_categories()
print("Proceeding on scrapping category pages")
for category in categories:
    print(category)
    break
