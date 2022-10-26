# -*- coding: utf-8 -*-

import random
import requests
from .log import logger
from requests.adapters import HTTPAdapter
from .error import StatusError, RequestError
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

ciphers_str = "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA:AES128-SHA:DES-CBC3-SHA"
ciphers_ls = ciphers_str.split(':')
ciphers = "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:"

ua_ls = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"]


class DESAdapter(HTTPAdapter):

    def __init__(self, *args, **kwargs):
        random.shuffle(ciphers_ls)
        self.ciphers = ciphers + ':'.join(ciphers_ls[:random.randint(12, 17)])
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.ciphers)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.ciphers)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)


class Request:

    def __init__(self, random_ua=False):
        proxy = ''
        self.default_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        self._proxy = {"http": proxy, "https": proxy}
        self._session = requests.Session()
        self.random_ua = random_ua
        self.ua = ""

    @property
    def cookies(self):
        return self._session.cookies

    def close(self):
        self._session.close()

    def get_default_headers(self):
        if not self.ua:
            self.ua = random.choice(ua_ls) if self.random_ua else self.default_ua
        return {
            "User-Agent": self.ua,
            "Referer": "https://s.1688.com/",
        }

    def request(self, method, url, headers=None, params=None, data=None, json_data=None, without_proxy=True):
        self._session.mount('https://', DESAdapter())
        _headers = self.get_default_headers()
        _headers.update(headers or {})
        self._session.headers = _headers
        try:
            resp = self._session.request(method, url, params=params, allow_redirects=True,
                                         data=data, json=json_data, timeout=60,
                                         proxies=self._proxy if not without_proxy else None)
            status_code = resp.status_code
            if status_code // 100 not in [2, 3]:
                raise StatusError(status_code, url)
            return resp
        except StatusError:
            raise
        except Exception as exc:
            logger.error("Request Error", exc_info=exc)
            raise RequestError(url)
