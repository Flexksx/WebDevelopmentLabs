from bs4 import BeautifulSoup


class Category:
    def __init__(self, html) -> None:
        self.html = html
        self.name = self.__initialize_name()
        self.url = self.__initialize_url()

    def __initialize_name(self) -> str:
        soup = BeautifulSoup(self.html, "html.parser")
        spans = soup.find_all("span")
        if len(spans) == 0:
            raise Exception(
                "Could not initialize Category. No span elements found")
        name = spans[0].text
        return name

    def __initialize_url(self) -> str:
        soup = BeautifulSoup(self.html, "html.parser")
        a_tags = soup.find_all("a")
        if len(a_tags) == 0:
            raise Exception(
                "Could not initialize Category. No a elements found")
        href = a_tags[0].get("href", "")

        if href and "javascript:;" not in href:
            url = f'https://linella.md{href}'
        else:
            raise Exception("Invalid href: contains 'javascript:;'")

        return url

    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f'Category: {self.name} with url: {self.url}'
