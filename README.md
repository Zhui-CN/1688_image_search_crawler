## 1688_image_search_crawler

**实现上传图片文件或图片地址到1688接口,搜索同款竞品(包含全部或跨境)**

**仅学术研究学习, 勿违规使用, 侵权联系立删**

**微: Zhui_S**

**研究不易, 给个star再走呗~**

```python
# pip install requests
# ImgSearch  是具体实现
# img        可以是图片路径或者网络url或者是图片编码的base64字符串
# task_id    用来做任务的标识,可以用图片base64编码后的md5值,可不传
# kj         是否搜跨境，默认值false  可不传
# api        是否使用api接口爬取(不推荐使用,会触发验证,请设置代理) 默认值false,可不传。只爬一页商品推荐为false,翻页才考虑需要true
# max_size   搜索最大个数, 不设置默认一页
# max_page   搜索最大页数, 不设置默认一页
# 使用参考main.py
```
```json
{
    "status": true,
    "message": "",
    "data": [
        {
            "imageUrl": "https://cbu01.alicdn.com/img/ibank/O1CN018JlDFC2EYIbrOU6nl_!!2734178756-0-cib.jpg",
            "offerId": 636717772130,
            "categoryId": 1042611,
            "subject": "巴仔兔 婴幼儿纯棉双层春秋四季通用宝宝防踢被分腿夏季儿童睡袋",
            "city": "荆州市沙市区",
            "province": "湖北",
            "companyName": "荆州市集美针织有限公司",
            "shopUrl": "https://jingzhoujimei.1688.com?tracelog=p4p",
            "oldPrice": 30.53,
            "quantityBegin": 2,
            "unit": "件",
            "gmvPrice": 20000,
            "rePurchaseRate": "8.27%",
            "quantityPrices": [
                {
                    "quantity": "≥2",
                    "price": 30.53
                }
            ],
            "scores": {
                "compositeNewScore": 4.5,
                "consultationScore": 5.0,
                "goodsScore": 3.0,
                "logisticsScore": 3.0,
                "returnScore": 3.5,
                "disputeScore": 5.0
            },
            "shopTag": {
                "title": "实力商家：更品质、更可靠、更贴心",
                "img": "https://img.alicdn.com/tfs/TB1ObNfjlv0gK0jSZKbXXbK2FXa-112-112.png",
                "year": 7
            },
            "aliTalkName": "布布乐婴童服"
        }
    ]
}
```