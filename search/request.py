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


def get_ciphers():
    random.shuffle(ciphers_ls)
    return ciphers + ':'.join(ciphers_ls[:random.randint(12, 17)])


class DESAdapter(HTTPAdapter):

    def __init__(self, *args, **kwargs):
        self.ciphers = get_ciphers()
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
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Referer": "https://s.1688.com/",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(self._headers)

    def request(self, method, url, headers=None, params=None, data=None, json=None):
        self._session.mount('http://', DESAdapter())
        self._session.mount('https://', DESAdapter())
        try:
            if method == "GET":
                resp = self._session.get(url, headers=headers, params=params)
            else:
                resp = self._session.post(url, headers=headers, params=params, data=data, json=json)
            if resp.status_code // 100 not in [2, 3]:
                raise StatusError(resp.status_code, url)
            return resp
        except StatusError:
            raise
        except Exception as exc:
            logger.error("Request Error", exc_info=exc)
            raise RequestError(url)

    @property
    def cookies(self):
        return self._session.cookies
