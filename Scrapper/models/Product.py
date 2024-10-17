class Product:
    def __init__(self, name: str, url: str, manufacturer: str, price: float, volume: float, abv: float):
        self.name = name
        self.url = url
        self.manufacturer = manufacturer
        self.price = price
        self.volume = volume
        self.abv = abv
        self.currency = "MDL"

    def with_currency(self, currency: str):
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
        return f"Product(name={self.name}, url={self.url}, manufacturer={self.manufacturer}, price={self.price}, volume={self.volume}, abv={self.abv}, currency={self.currency})"
