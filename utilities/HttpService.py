import requests

class HttpService:

    def __init__(self, headers=None, auth=None):
        self._headers = headers
        self._auth = auth


    def get(self, url: str) -> str | Exception:
        response = requests.get(url, headers=self._headers, auth=self._auth)
        response.raise_for_status()
        return response.json()
    

    def check_connectivity(self, url) -> None | Exception:
        response = requests.head(url, headers=self._headers, auth=self._auth)
        response.raise_for_status()
       

