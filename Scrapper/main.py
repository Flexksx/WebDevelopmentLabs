from calendar import c
from unicodedata import category
from requestlib import Requester
from scrapper.category.CategoryMenuScrapper import CategoryMenuScrapper
requester = Requester()
response = requester.get_html("https://linella.md/ro")
category_scrapper = CategoryMenuScrapper(response, "ul", "catalog__body_index")
category_scrapper.get_categories()
