# coding=utf-8

import requests
from urllib.parse import urlparse
from search.utils.utils import DESAdapter


class Request:
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Referer": "https://s.1688.com/",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(self._headers)

    def request(self, method, url, headers=None, params=None, data=None, json=None):
        url_parse = urlparse(url)
        adapter_url = "{}://{}".format(url_parse.scheme, url_parse.netloc)
        self._session.mount(adapter_url, DESAdapter())
        if method == "GET":
            resp = self._session.get(url, headers=headers, params=params)
        else:
            resp = self._session.post(url, headers=headers, params=params, data=data, json=json)
        return resp

    @property
    def cookies(self):
        return self._session.cookies
