# -*- coding: utf-8 -*-

class CrawlerError(Exception):
    pass


class RequestError(CrawlerError):

    def __init__(self, url, *args, **kwargs):
        self.url = url
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "RequestError: {}".format(self.url)


class StatusError(CrawlerError):

    def __init__(self, code, url, *args, **kwargs):
        self.url = url
        self.code = code
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "StatusError: {} {}".format(self.code, self.url)
