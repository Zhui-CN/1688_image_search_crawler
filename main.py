# coding=utf-8

from search.search import ImgSearch


def main(img, kuajing, max_page):
    gen = ImgSearch().search_gen(img, kuajing=kuajing, max_page=max_page)
    for product in gen:
        data = {
            "item_id": product["id"],
            "title": product["information"]["subject"],
            "price": product["tradePrice"]["offerPrice"]["priceInfo"]["price"],
        }
        print(data)


def not_kuajing():
    main(img="img.jpg", kuajing=False, max_page=1)


def kuajing():
    main(img="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimg.alicdn.com%2Fi3%2F725677994%2FO1CN01JpzjZn28vIqeoy4tm_%21%21725677994.jpg_200x200.jpg&refer=http%3A%2F%2Fimg.alicdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1648118281&t=ea26e293b501cfa32bf8976f19252ef9", kuajing=True, max_page=1)


if __name__ == '__main__':
    kuajing()
    not_kuajing()
