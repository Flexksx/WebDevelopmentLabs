class Product:
    def __init__(self, name: str, url: str, manufacturer: str, price: float, volume: float, abv: float):
        """
        Initializes a new Product instance.

        :param name: The name of the product.
        :param url: The URL of the product.
        :param manufacturer: The manufacturer of the product.
        :param price: The price of the product.
        :param volume: The volume of the product.
        :param abv: The alcohol by volume (ABV) percentage.
        """
        if price < 0 or volume < 0 or abv < 0:
            raise ValueError("Price, volume, and ABV must be non-negative.")

        self.name = name
        self.url = url
        self.manufacturer = manufacturer
        self.price = float(price)
        self.volume = float(volume)
        self.abv = float(abv)
        self.currency = "MDL"

    def with_currency(self, currency: str):
        """
        Sets the currency of the product.

        :param currency: The currency code (e.g., 'USD', 'EUR').
        :return: The current Product instance for chaining.
        """
        self.currency = currency
        return self

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return (self.name == other.name
                and self.url == other.url
                and self.manufacturer == other.manufacturer
                and self.price == other.price
                and self.volume == other.volume
                and self.abv == other.abv
                and self.currency == other.currency)

    def __str__(self) -> str:
        return (f"Product(name={self.name}, url={self.url}, manufacturer={self.manufacturer}, "
                f"price={self.price}, volume={self.volume}, abv={self.abv}, currency={self.currency})")
