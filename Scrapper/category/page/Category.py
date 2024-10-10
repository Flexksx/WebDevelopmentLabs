from bs4 import BeautifulSoup

from ...requestlib.Requester import IRequester


class Category:
    def __init__(self, html) -> None:
        self.html = html
        self.name = self.__initialize_name()
        self.url = self.__initialize_url()
        # print(f"Initialized Category: {self.name} with url: {self.url}")

    def __initialize_name(self) -> str:
        soup = BeautifulSoup(self.html, "html.parser")
        a_tags = soup.find_all("a")
        if len(a_tags) == 0:
            raise Exception(
                f"Could not initialize Category. No a elements found")
        name = a_tags[0].text.strip()
        return name

    def __initialize_url(self) -> str:
        soup = BeautifulSoup(self.html, "html.parser")
        a_tags = soup.find_all("a")
        if len(a_tags) == 0:
            raise Exception(
                f"Could not initialize Category {self.name}. No a elements found")
        href = a_tags[0].get("href", "").strip()

        if href and "javascript:;" not in href:
            url = f'https://alcomarket.md/{href}'
        else:
            raise Exception(f"Invalid href for {self.name}: contains {
                            href}. Full html: {self.html}")
        return url

    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"Category: {self.name} with url: {self.url}"

    def get_products(self, request_module: IRequester):
        response = request_module.get_html(self.url)
        print(response)
