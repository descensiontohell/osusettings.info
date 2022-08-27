from requests import Response, Session, request

from tests.config import config


class Client:
    def __init__(self) -> None:
        self.session = Session()
        self.acquire_cookie()

    def acquire_cookie(self) -> None:
        self.request("/su/login", "POST", json={"name": config.LOGIN, "password": config.PASSWORD})

    def request(self, path: str, method: str, params: dict = None, json: dict = None) -> Response:
        return self.session.request(method=method, url=config.BASE_URL + path, params=params, json=json)

    def unauthorized_request(self, path: str, method: str, params: dict = None, json: dict = None) -> Response:
        return request(method=method, url=config.BASE_URL + path, params=params, json=json)


client = Client()
