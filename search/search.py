# coding=utf-8

import os
import time
import json
import base64
from hashlib import md5
from .log import logger
from .request import Request
from urllib.parse import urlencode


def is_b64_str(s):
    try:
        return base64.b64encode(base64.b64decode(s)).decode() == s
    except Exception:
        return False


class ImgSearch:

    def __init__(self, img, kj=False, max_size=None, max_page=None):
        self._req = Request()
        self._img_id = None
        self._req_id = None
        self._session_id = None
        self.offset = 0
        self.page = 1
        self.b64img = self.get_b64img_str(img)
        self.kj = kj
        self.max_size = max_size
        self.max_page = max_page or 1 if not self.max_size else None
        self.upload_data = {
            "data": {
                "imageBase64": self.b64img,
                "appName": "searchImageUpload",
                "appKey": "pvvljh1grxcmaay2vgpe9nb68gg9ueg2"
            }
        }
        self.upload_success = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.max_size and self.offset >= self.max_size or self.max_page and self.page > self.max_page:
            raise StopIteration
        if not self.upload_success:
            self.upload_img()
        item_ls = self.request_item_ls()
        self.page += 1
        return item_ls

    def _other_page(self, kuajing):
        # TODO other_page
        params = dict(filter(lambda x: x[1] is not None, [
            ("tab", "imageSearch"),
            ("imageAddress", ""),
            ("imageId", self._img_id),
            ("imageIdList", self._img_id),
        ]))
        if kuajing:
            api = "https://s.1688.com/kuajing/image_search.htm"
        else:
            api = "https://s.1688.com/youyuan/index.htm"
        api = f"{api}?{urlencode(params)}"

    def get_b64img_str(self, img: str) -> str:
        if os.path.exists(img):
            with open(img, "rb") as f:
                b64img = base64.b64encode(f.read()).decode()
        elif img.startswith("http"):
            resp = self._req.request("GET", img)
            b64img = base64.b64encode(resp.content).decode()
        elif is_b64_str(img):
            b64img = img
        else:
            raise ValueError("img有误")
        return b64img

    def upload_params(self, token=""):
        app_key = "12574478"
        timestamp = str(round(time.time() * 1000))
        s = json.dumps(self.upload_data["data"], separators=(',', ':'))
        t = token + "&" + timestamp + "&" + app_key + "&" + s
        sign = md5(t.encode()).hexdigest()
        return {
            "jsv": "2.4.11",
            "appKey": app_key,
            "t": timestamp,
            "sign": sign,
            "api": "mtop.1688.imageService.putImage",
            "ecode": "0",
            "v": "1.0",
            "type": "originaljson",
            "dataType": "jsonp",
            "_bx-v": "1.1.20"
        }

    def upload_img(self):
        api = "https://h5api.m.1688.com/h5/mtop.1688.imageservice.putimage/1.0/"
        post_data = urlencode(self.upload_data).replace("%27", "%22").replace("+", "")
        self._req.request("POST", api, data=post_data, params=self.upload_params())
        token = self._req.cookies.get("_m_h5_tk").split("_")[0]
        resp = self._req.request("POST", api, data=post_data, params=self.upload_params(token=token))
        resp_json = resp.json()
        if not resp_json.get("data"):
            logger.error("上传图片失败")
            return
        self._img_id = resp_json["data"]["imageId"]
        self._req_id = resp_json["data"]["requestId"]
        self._session_id = resp_json["data"]["sessionId"]
        self.upload_success = True

    def request_item_ls(self):
        page_name = "CrossBorderPCFindImage" if self.kj else "image"
        params = dict(filter(lambda x: x[1] is not None, [
            ("tab", "imageSearch"),
            ("imageAddress", ""),
            ("imageId", self._img_id),
            ("imageIdList", self._img_id),
            # ("pailitaoCategoryId", "0"),
            ("beginPage", self.page),
            ("pageSize", "40"),
            ("requestId", self._req_id),
            ("pageName", page_name),
            ("sessionId", self._session_id),
            ("_bx", "1.1.20"),
        ]))
        api = f"https://search.1688.com/service/imageSearchOfferResultViewService?{urlencode(params)}"
        logger.info(f"imgid:{self._img_id}, page:{self.page}")
        resp = self._req.request("GET", api)
        data_json = resp.json()["data"]["data"]
        offer_list = data_json.get("offerList") or []
        item_ls = []
        for item in offer_list:
            self.offset += 1
            information = item.get("information") or {}
            company = item.get("company") or {}
            trade_quantity = item.get("tradeQuantity") or {}
            item_ls.append({
                "category_id": information.get("categoryId"),
                "subject": information.get("subject"),
                "city": company.get("city"),
                "province": company.get("province"),
                "img_url": (item.get("image") or {}).get("imgUrl"),
                "offer_id": item.get("id"),
                "price": float((((item.get("tradePrice") or {}).get("offerPrice") or {}).get("priceInfo") or {}).get(
                    "price") or 0),
                "quantity_begin": trade_quantity.get("quantityBegin"),
                "unit": trade_quantity.get("unit")
            })
        return item_ls
