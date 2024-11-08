from models.Product import Product
from requestlib.StandardRequester import Requester
from requestlib.CustomRequester import CustomRequester
from scrappers.categories.CategoryMenuScrapper import CategoryMenuScrapper
from serializers.my_serializer.CustomSerializer import CustomSerializer
from serializers.json_serializers.JSONSerializer import JSONSerializer
requester = CustomRequester()
catalogue_response = requester.get_html("https://alcomarket.md/ro/catalog")
category_menu_scrapper = CategoryMenuScrapper(
    catalogue_response, "div", "mini-catalog__wrapper", requests_module=requester)
category_scrappers = category_menu_scrapper.get_category_scrappers()

print("Proceeding on scrapping category pages")

vodka = category_scrappers[4]
print(vodka)


products = vodka.get_products()

vodka_category = vodka.get_model()
processed_products = vodka_category.process_products((100, 200))
serializer = CustomSerializer()
# product = processed_products.get("filtered_products")[0]

test_dict = {
    "name": "Test Product",
    "price": 100,
    "available": True,
    "tags": ["test", "product"]
}

serialized = serializer.serialize(test_dict)
print(serialized)
deserialized = serializer.deserialize(serialized)
print(deserialized)
