from functools import reduce
from datetime import datetime, timezone
from .Product import Product


class Category:
    def __init__(self, name: str, url: str, products: list[Product] = None) -> None:
        self.name = name
        self.url = url
        self.products = products or []

    def set_products(self, products: list[Product]):
        self.products = products

    def get_products(self) -> list[Product]:
        return self.products

    def __convert_price(self, product: Product, mdl_to_eur_rate: float = 20) -> float:
        return round(product.price / mdl_to_eur_rate, 2)

    def process_products(self, price_range: tuple[float, float], product_currency: str = "MDL", mdl_to_eur_rate: float = 20) -> dict:
        if product_currency == "MDL":
            price_range = tuple(
                map(lambda p: round(p / mdl_to_eur_rate, 2), price_range))

        """
        This map function will take self.products as iteratee
        and apply the lambda function to each element of the list.
        the lambda function takes as argument a product p and returns a new Product object 
        with converted price.
        """
        mapped_products = list(
            map(lambda p: Product(
                p.name, p.url, p.manufacturer,
                self.__convert_price(p), p.volume, p.abv).with_currency("EUR"),
                self.products
                )
        )

        """
        As above, the filter function will take the mapped_products list as iteratee
        and apply the lambda function to each element of the list.
        The lambda function takes as argument a product p and returns a boolean value
        if the price of the product is in the price range.
        """
        filtered_products = list(
            filter(lambda p: price_range[0] <= p.price <=
                   price_range[1], mapped_products)
        )

        """
        The reduce function will take the filtered_products list as iteratee
        and apply the lambda function to each element of the list.
        The lambda function takes as arguments an accumulator acc and a product p
        and returns the sum of the accumulator and the price of the product.
        """
        total_price = reduce(lambda acc, p: acc + p.price,
                             filtered_products, 0)

        result = {
            "filtered_products": filtered_products,
            "total_price": total_price,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        return result
