# coding=utf-8

import os
import time
import json
from hashlib import md5
from base64 import b64encode
from urllib.parse import urlencode
from search.utils.request import Request


class ImgSearch:

    def __init__(self):
        self._req = Request()
        self._img_id = None
        self._req_id = None
        self._session_id = None

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
        resp = self._req.request("GET", api)

    def _get_upload_params(self, data, token=""):
        timestamp = str(round(time.time() * 1000))
        app_key = "12574478"
        s = json.dumps(data["data"], separators=(',', ':'))
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

    def _upload_img(self, img):
        b64img = None
        if os.path.exists(img):
            with open(img, "rb") as f:
                b64img = b64encode(f.read()).decode()
        elif isinstance(img, str) and img.startswith("http"):
            resp = self._req.request("GET", img)
            if resp.status_code == 200:
                b64img = b64encode(resp.content).decode()
        if not b64img:
            print("img有误")
            return False
        api = "https://h5api.m.1688.com/h5/mtop.1688.imageservice.putimage/1.0/"
        data = {
            "data": {
                "imageBase64": b64img,
                "appName": "searchImageUpload",
                "appKey": "pvvljh1grxcmaay2vgpe9nb68gg9ueg2"
            }
        }
        post_data = urlencode(data).replace("%27", "%22").replace("+", "")
        self._req.request("POST", api, data=post_data, params=self._get_upload_params(data=data))
        token = self._req.cookies.get("_m_h5_tk").split("_")[0]
        resp_json = self._req.request("POST", api, data=post_data,
                                      params=self._get_upload_params(data=data, token=token)).json()
        if not resp_json.get("data"):
            print("上传图片失败")
            return False
        self._img_id = resp_json["data"]["imageId"]
        self._req_id = resp_json["data"]["requestId"]
        self._session_id = resp_json["data"]["sessionId"]
        return True

    def _get_product_api_info(self, page, kuajing):
        page_name = "CrossBorderPCFindImage" if kuajing else "image"
        params = dict(filter(lambda x: x[1] is not None, [
            ("tab", "imageSearch"),
            ("imageAddress", ""),
            ("imageId", self._img_id),
            ("imageIdList", self._img_id),
            ("pailitaoCategoryId", "0"),
            ("beginPage", page),
            ("pageSize", "40"),
            ("requestId", self._req_id),
            ("pageName", page_name),
            ("sessionId", self._session_id),
            ("_bx", "1.1.20"),
        ]))
        api = f"https://search.1688.com/service/imageSearchOfferResultViewService?{urlencode(params)}"
        resp_json = self._req.request("GET", api).json()
        return resp_json["data"]

    def search_gen(self, img, kuajing=False, max_page=1):
        """
        :param img: str 图片地址或者图片url
        :param kuajing: bool 是否搜索跨境
        :param max_page: int 最大页数
        """
        if self._upload_img(img):
            for page in range(1, max_page + 1):
                print(f"第{page}页")
                resp_json = self._get_product_api_info(page, kuajing)
                offer_list = resp_json["data"]["offerList"]
                for offer in offer_list:
                    yield offer
