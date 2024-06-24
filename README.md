## 1688_image_search_crawler

**实现上传图片文件或图片地址到1688接口,搜索同款竞品**

**仅学术研究学习, 勿违规使用, 侵权联系立删**

**微: Zhui_S**

**研究不易, 给个star再走呗~**

```python
# pip install httpx httpx[http2]
# ImgSearch  是具体实现
# ImgSearch.init_for_url  用网络图片url初始化
# ImgSearch.init_for_file 用图片文件初始化
# ImgSearch.init_for_b64  用图片编码的base64初始化
# api                     是否使用api接口爬取(不推荐使用,会触发验证,请设置代理) 默认值false,可不传。只爬一页商品推荐为false,翻页才考虑需要true
# max_page                搜索最大页数, 不设置默认一页
# max_size                搜索最大个数, 不设置默认一页
# 使用参考 main.py
```

```json
  {
  "brand": "小羊嘟嘟",
  "image_url": "https://cbu01.alicdn.com/img/ibank/O1CN01cx6aTj1SDbAo0DOIy_!!2200651792213-0-cib.jpg",
  "offer_id": 645493882755,
  "category_id": 1037003,
  "subject": "2023春秋新款婴儿连体衣男女宝宝哈衣爬服纯棉安阳婴幼童服装",
  "city": "安阳市",
  "province": "河南",
  "company_name": "汤阴凯锐达制衣有限公司",
  "shop_url": "https://shop697d4j0475c16.1688.com?tracelog=p4p",
  "credit_level": 1,
  "credit_text": "AAA",
  "reg_capital": 200.0,
  "reg_capital_unit": "万",
  "position_labels": [
    "7×24H响应",
    "深度验厂",
    "先采后付"
  ],
  "price": 26.0,
  "quantity_begin": 1,
  "quantity_begin_unit": "件",
  "gmv_price": 2000,
  "repurchase_rate": "45.45%",
  "quantity_prices": [
    {
      "quantity": "2~11",
      "price": 26.0
    },
    {
      "quantity": "≥12",
      "price": 24.0
    }
  ],
  "scores": {
    "composite": 4.5,
    "consultation": 4.0,
    "goods": 3.0,
    "logistics": 4.0,
    "return": 3.0,
    "dispute": 5.0
  },
  "shop_tag": {
    "title": "源头工厂、平台优选、闪电发货",
    "img": "https://img.alicdn.com/imgextra/i3/O1CN01LcOfhW1QrmfmYQ66J_!!6000000002030-2-tps-112-112.png",
    "year": 6
  },
  "ali_talk_name": "凯锐达婴童"
}
```