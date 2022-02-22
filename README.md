## 1688_image_search_crawler

**实现上传图片文件或图片地址到1688接口,搜索同款竞品(包含全部或跨境)**

**仅学术研究学习, 勿违规使用, 侵权联系立删**

**微: Zhui_S**

```python
# pip install requests

# ImgSearch 是具体实现
from search.search import ImgSearch

# img 可以是图片路径或者网络url
# kuangjing 是否启用跨境搜索
# max_page 搜索最大页数
# search_gen是generator
img_search = ImgSearch()
for product in img_search.search_gen(img, kuajing=False, max_page=1):
    print(product)
```

**研究不易, 给个star再走呗~**