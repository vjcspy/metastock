import requests

from metastock.modules.core.logging.logger import Logger


class HttpClient:
    instance = None

    def get(self, url, config = None):
        if config is None:
            config = {}
        response = requests.get(url)

        return response

    def post(self, url, data: dict, config: dict = None):
        response = requests.post(url, json = data)
        # response.raise_for_status()
        return response


def http_client() -> HttpClient:
    if HttpClient.instance is None:
        HttpClient.instance = HttpClient()
    return HttpClient.instance
