import requests


class IRequester:
    def __init__(self) -> None:
        pass

    def get(self, url: str) -> requests.Response:
        pass

    def __response_is_html(self, response: requests.Response) -> bool:
        pass

    def get_html(self, url: str) -> str:
        pass
