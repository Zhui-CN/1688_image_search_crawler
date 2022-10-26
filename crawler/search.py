# -*- coding: utf-8 -*-

import os
import re
import time
import json
import base64
from hashlib import md5
from utils import logger, Request
from urllib.parse import urlencode


def is_b64_str(s):
    try:
        return base64.b64encode(base64.b64decode(s)).decode() == s
    except Exception:
        return False


def get_b64img_str(img: str) -> str:
    if is_b64_str(img):
        b64img = img
    elif img.startswith("http"):
        s = Request()
        content = s.request("GET", img).content
        b64img = base64.b64encode(content).decode()
        s.close()
    elif os.path.exists(img):
        with open(img, "rb") as f:
            b64img = base64.b64encode(f.read()).decode()
    else:
        raise ValueError("img有误")
    return b64img


class ImgSearch:
    data_reg = re.compile(r"window.data.offerresultData\s?=\s?successDataCheck\((.*?})\);", re.S | re.I)

    tag_config = {
        "memberTagIds": {"isShiliDangKou": "3910593", "isSuperFactory": "3938689"},
        "tagIds": {
            "isPinZhiBaoZhang": "3951041",
            "deliveryHours48": "286402",
            "deliveryHours24": "286466",
            "superNewProduct": "277762",
            "isImallExpert": "3981057"
        }
    }

    tag_info_map = {
        "a": {
            "title": "源头工厂、平台优选、闪电发货",
            "img": "https://img.alicdn.com/imgextra/i3/O1CN01LcOfhW1QrmfmYQ66J_!!6000000002030-2-tps-112-112.png"
        },
        "b": {
            "title": "阿里巴巴建议您优先选择诚信通会员",
            "img": "https://img.alicdn.com/tfs/TB1xPJdjXT7gK0jSZFpXXaTkpXa-112-112.png"
        },
        "c": {
            "title": "实力商家：更品质、更可靠、更贴心",
            "img": "https://img.alicdn.com/tfs/TB1ObNfjlv0gK0jSZKbXXbK2FXa-112-112.png"
        },
        "d": {
            "title": "工业品牌：品牌正品，品质服务",
            "img": ""
        }
    }

    def __init__(self, img, kj=False, api=False, task_id=None, max_size=None, max_page=None):
        self.b64img = get_b64img_str(img)
        self.img_id = None
        self.req_id = None
        self.session_id = None
        self.kj = kj
        self.api = api
        self.task_id = task_id
        self.upload_success = False
        self.req = Request()
        self.upload_data = {
            "data": {
                "imageBase64": self.b64img,
                "appName": "searchImageUpload",
                "appKey": "pvvljh1grxcmaay2vgpe9nb68gg9ueg2"
            }
        }
        self.max_size = max_size
        self.max_page = max_page or 1 if not self.max_size else None
        self.offset = 0
        self.page = 1

    def __str__(self):
        return f"TaskId:{self.task_id} kj:{self.kj} api:{self.api}"

    def __iter__(self):
        return self

    def __next__(self):
        if not self.upload_success:
            if not self.upload_img():
                self.req.close()
                raise StopIteration
        if self.max_size and self.offset >= self.max_size or self.max_page and self.page > self.max_page:
            self.req.close()
            raise StopIteration
        if self.api:
            offer_list = self.request_api_offer_list()
        else:
            self.max_page = 1
            offer_list = self.request_web_offer_list()
        item_ls = self.parse_offer_list(offer_list)
        self.page += 1
        return item_ls

    def get_params(self, token=""):
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

    def get_shop_tag_info(self, offer):
        def tag_find_for_ary(data: dict, ary: list):
            if not ary or not data:
                return {}
            result = {}
            for i in data:
                if data[i] in ary:
                    result[i] = True
                else:
                    result[i] = False
            return result

        tag_info = {"title": "", "img": ""}
        try:
            offer_tag_data = offer.get("marketOfferTag") or {}
            for k, v in self.tag_config.items():
                if not offer.get("feMapping"):
                    offer["feMapping"] = {}
                offer["feMapping"][k] = tag_find_for_ary(v, offer_tag_data.get(k))
        except:
            logger.error("tag数据格式异常")
            return tag_info
        m = (offer.get("offerSource") or {}).get("fromShili")
        f = (offer.get("tradeService") or {}).get("tpMember")
        g = (offer.get("brand") or {}).get("industrialGoods")
        w = ((offer.get("feMapping") or {}).get("memberTagIds") or {}).get("isSuperFactory")
        if w:
            tag_info.update(self.tag_info_map["a"])
        else:
            if g:
                if f:
                    tag_info.update(self.tag_info_map["b"])
                else:
                    tag_info.update(self.tag_info_map["d"])
            else:
                if m:
                    tag_info.update(self.tag_info_map["c"])
                else:
                    if f:
                        tag_info.update(self.tag_info_map["b"])
        return tag_info

    def upload_img(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        post_data = urlencode(self.upload_data).replace("%27", "%22").replace("+", "")
        api = "https://h5api.m.1688.com/h5/mtop.1688.imageservice.putimage/1.0/"
        logger.info(f"正在上传图片:{self}")
        self.req.request("POST", api, headers=headers, data=post_data, params=self.get_params())
        token = self.req.cookies.get("_m_h5_tk").split("_")[0]
        resp = self.req.request("POST", api, headers=headers, data=post_data, params=self.get_params(token=token))
        resp_json = resp.json()
        if not resp_json.get("data"):
            logger.error("上传图片失败")
            return
        self.img_id = resp_json["data"]["imageId"]
        self.req_id = resp_json["data"]["requestId"]
        self.session_id = resp_json["data"]["sessionId"]
        self.upload_success = True
        return True

    def request_api_offer_list(self):
        params = dict(filter(lambda x: x[1] is not None, [
            ("tab", "imageSearch"),
            ("imageAddress", ""),
            ("imageId", self.img_id),
            ("imageIdList", self.img_id),
            # ("pailitaoCategoryId", "0"),
            ("beginPage", self.page),
            ("pageSize", 40),
            ("requestId", self.req_id),
            ("pageName", "CrossBorderPCFindImage" if self.kj else "image"),
            ("sessionId", self.session_id),
            ("_bx", "1.1.20"),
        ]))
        api = f"https://search.1688.com/service/imageSearchOfferResultViewService?{urlencode(params)}"
        logger.info(f"正在爬取:{self} ImgId:{self.img_id} page:{self.page}")
        json_data = self.req.request("GET", api).json()
        offer_list = []
        if ((json_data.get("data") or {}).get("data") or {}).get("offerList"):
            offer_list = json_data["data"]["data"]["offerList"]
        if not offer_list:
            logger.warning(f"无结果集:{self} ImgId:{self.img_id} page:{self.page}")
        return offer_list

    def request_web_offer_list(self):
        params = dict(filter(lambda x: x[1] is not None, [
            ("tab", "imageSearch"),
            ("imageAddress", ""),
            ("imageId", self.img_id),
            ("imageIdList", self.img_id),
        ]))
        api = "https://s.1688.com/kuajing/image_search.htm" if self.kj else "https://s.1688.com/youyuan/index.htm"
        url = f"{api}?{urlencode(params)}"
        logger.info(f"正在爬取:{self} ImgId:{self.img_id}")
        body = self.req.request("GET", url).text
        data_reg = self.data_reg.search(body)
        offer_list = []
        if data_reg:
            json_data = json.loads(data_reg.group(1))
            if (json_data.get("data") or {}).get("offerList"):
                offer_list = json_data["data"]["offerList"]
        if not offer_list:
            logger.warning(f"无结果集:{self} ImgId:{self.img_id}")
        return offer_list

    def parse_offer_list(self, offer_list):
        item_ls = []
        for offer in offer_list:
            item = {}
            self.offset += 1
            company = offer.get("company") or {}
            information = offer.get("information") or {}
            trade_service = offer.get("tradeService") or {}
            trade_quantity = offer.get("tradeQuantity") or {}
            offer_price = (offer.get("tradePrice") or {}).get("offerPrice") or {}

            item["imageUrl"] = (offer.get("image") or {}).get("imgUrl")
            item["offerId"] = offer.get("id")
            item["categoryId"] = information.get("categoryId")
            item["subject"] = information.get("subject")
            item["city"] = company.get("city")
            item["province"] = company.get("province")
            item["companyName"] = company.get("name")
            item["shopUrl"] = company.get("url")

            item["oldPrice"] = float((offer_price.get("priceInfo") or {}).get("price") or 0)  # 面板价格
            item["quantityBegin"] = trade_quantity.get("quantityBegin")  # 起订量
            item["unit"] = trade_quantity.get("unit")  # 起订量单位
            item["gmvPrice"] = (trade_quantity.get("gmvValue") or {}).get("integer")  # 成交价

            purchase_rate = str(information.get("rePurchaseRate") or "")
            if purchase_rate and "%" not in purchase_rate:
                purchase_rate = round(float(purchase_rate) * 100, 2)
                purchase_rate = f"{purchase_rate}%" if purchase_rate else ""
            item["rePurchaseRate"] = purchase_rate  # 复购率  rePurchaseRate

            item["quantityPrices"] = [
                {"quantity": q.get("quantity"), "price": float(q.get("valueString") or 0)}
                for q in offer_price.get("quantityPrices") or []
            ]  # 批发数量价格

            item["scores"] = {
                "compositeNewScore": round(float(trade_service.get("compositeNewScore") or 0), 1),  # 综合服务
                "consultationScore": round(float(trade_service.get("consultationScore") or 0), 1),  # 采购咨询
                "goodsScore": round(float(trade_service.get("goodsScore") or 0), 1),  # 品质体验
                "logisticsScore": round(float(trade_service.get("logisticsScore") or 0), 1),  # 物流时效
                "returnScore": round(float(trade_service.get("returnScore") or 0), 1),  # 退货体验
                "disputeScore": round(float(trade_service.get("disputeScore") or 0), 1),  # 纠纷解决
            }
            item["shopTag"] = self.get_shop_tag_info(offer)
            item["shopTag"]["year"] = trade_service.get("tpYear")
            item["aliTalkName"] = (offer.get("aliTalk") or {}).get("loginId") or ""

            item_ls.append(item)

        return item_ls
