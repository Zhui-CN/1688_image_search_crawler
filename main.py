# coding=utf-8

from crawler import ImgSearch
from utils import logger, RequestError


def main(data):
    status = True
    message = ""
    item_ls = []
    try:
        page = ImgSearch(**data)
    except Exception as exc:
        message = str(exc)
        status = False
        logger.error("page process error", exc_info=exc)
    while status:
        try:
            for page_ls in page:
                item_ls.extend(page_ls)
            break
        except RequestError:
            continue
        except Exception as exc:
            message = str(exc)
            status = False
            logger.error("page process error: {}".format(page), exc_info=exc)
            break
    logger.info(f"{page} status:{status} msg:{message} items:{len(item_ls)}")
    return {"status": status, "message": message, "data": item_ls}


def file():
    data = {
        "img": "img.jpg",
        "kj": False,
        "api": False,
    }
    print(main(data))


def url():
    img_url = "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimg.alicdn.com%2Fi3%2F725677994%2FO1CN01JpzjZn28vIqeoy4tm_%21%21725677994.jpg_200x200.jpg&refer=http%3A%2F%2Fimg.alicdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1648118281&t=ea26e293b501cfa32bf8976f19252ef9"
    data = {
        "img": img_url,
        "kj": True,
        "api": True,
        "max_page": 2
    }
    print(main(data))


def b64str():
    b64img = "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"
    data = {
        "img": b64img,
        "kj": False,
        "api": True,
        "max_size": 80
    }
    print(main(data))


if __name__ == '__main__':
    file()
    url()
    b64str()
