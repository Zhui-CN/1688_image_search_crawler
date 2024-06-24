# -*- coding: utf-8 -*-

class CrawlerError(Exception):

    def __init__(self, url, proxies):
        self.url = url
        self.proxies = proxies

    def __str__(self):
        return f"url:{self.url}, proxies:{self.proxies}"


class RequestError(CrawlerError):

    def __init__(self, url, proxies, exc):
        super().__init__(url, proxies)
        self.exc = exc

    def __str__(self):
        return f"RequestError: {super().__str__()}, exc:{str(self.exc)}"


class BannedError(CrawlerError):

    def __init__(self, url, proxies):
        super().__init__(url, proxies)

    def __str__(self):
        return f"BannedError: {super().__str__()}"


class StatusError(CrawlerError):

    def __init__(self, url, proxies, code):
        super().__init__(url, proxies)
        self.code = code

    def __str__(self):
        return f"StatusError: {super().__str__()}, code:{self.code}"
