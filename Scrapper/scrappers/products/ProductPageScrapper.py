from bs4 import BeautifulSoup
from models.Product import Product


class ProductPageScrapper:
    def __init__(self, html: str, url: str) -> None:
        self.html = html
        self.url = url
        self.soup = BeautifulSoup(html, "html.parser")

    def get_product(self) -> Product:
        product_name = self.__scrap_name()
        product_price = self.__scrap_price()
        product_volume = self.__scrap_volume()
        product_abv = self.__scrap_abv()
        product_manufacturer = self.__scrap_manufacturer()
        product = Product(
            name=product_name,
            url=self.url,
            manufacturer=product_manufacturer,
            price=product_price,
            volume=product_volume,
            abv=product_abv
        )
        return product

    def __scrap_name(self):
        h_one_tags = self.soup.find_all(
            "h1", class_='info-card__title product__title')
        if len(h_one_tags) == 0:
            raise ValueError(f"Could not find name for product {self.url}")
        name = h_one_tags[0].text.strip()
        return name

    def __scrap_price(self):
        price_divs = self.soup.find_all("div", class_='info-card__price')
        if len(price_divs) == 0:
            raise ValueError(f"Could not find price for product {self.url}")

        spans_in_price_div = price_divs[0].find_all("span")
        price = None
        if len(spans_in_price_div) == 1:
            price = spans_in_price_div[0].text.strip()
        elif len(spans_in_price_div) > 1:
            spans_with_new_price = price_divs[0].find_all(
                "span", class_="_now")
            if len(spans_with_new_price) == 0:
                raise ValueError(
                    f"Could not find price for product {self.url}")
            price = spans_with_new_price[0].text.strip()

        if price is None:
            raise ValueError(f"Could not find price for product {self.url}")

        return float(price.replace(" ", "").replace(",", ".").replace("mdl", "").replace("MDL", ""))

    def __scrap_volume(self):
        volume_li = self.soup.find_all(
            "li", class_="characteristic-details-card__item")
        for li in volume_li:
            name_span = li.find(
                "span", class_="characteristic-details-card__name")
            value_span = li.find(
                "span", class_="characteristic-details-card__value")
            if name_span and value_span and "Volum" in name_span.text:
                volume = value_span.text.strip()
                if "ml" in volume.lower():
                    volume = volume.lower().replace("ml", "").replace(" ", "").replace(",", ".")
                    return float(volume) / 1000
                elif "l" in volume.lower():
                    volume = volume.lower().replace("l", "").replace(" ", "").replace(",", ".")
                    return float(volume)

        raise ValueError(f"Could not find volume for product {self.url}")

    def __scrap_abv(self):
        abv_li = self.soup.find_all(
            "li", class_="characteristic-details-card__item")
        for li in abv_li:
            name_span = li.find(
                "span", class_="characteristic-details-card__name")
            value_span = li.find(
                "span", class_="characteristic-details-card__value")
            if name_span and value_span and "Tărie" in name_span.text:
                abv = value_span.text.strip().replace("%", "").replace(" ", "")
                return float(abv.replace(",", "."))

        raise ValueError(f"Could not find ABV for product {self.url}")

    def __scrap_manufacturer(self):
        manufacturer_li = self.soup.find_all(
            "li", class_="characteristic-details-card__item")
        for li in manufacturer_li:
            name_span = li.find(
                "span", class_="characteristic-details-card__name")
            value_span = li.find(
                "span", class_="characteristic-details-card__value")
            if name_span and value_span and "Producător" in name_span.text:
                return value_span.text.strip()

        raise ValueError(f"Could not find manufacturer for product {self.url}")
