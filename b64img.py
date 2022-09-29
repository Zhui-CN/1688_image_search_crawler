# -*- coding: utf-8 -*-

from base64 import b64encode

img = "img.jpg"

with open(img, "rb") as f:
    b64img = b64encode(f.read()).decode()
    print(b64img)
