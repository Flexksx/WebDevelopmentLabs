import requests

from requestlib.Requester import IRequester


class Requester(IRequester):
    def __init__(self) -> None:
        pass

    def get(self, url: str) -> requests.Response:
        return requests.get(url)

    def __response_is_html(self, response: requests.Response) -> bool:
        if response.headers.get("Content-Type") is None:
            raise Exception("Response has no Content-Type header")
        return "text/html" in response.headers["Content-Type"]

    def get_html(self, url: str) -> str:
        response = self.get(url)
        if self.__response_is_html(response):
            return response.text
        raise Exception("Response is not HTML")
