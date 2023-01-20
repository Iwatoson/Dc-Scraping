import scrapy
import re
from tcolor_scrapy.items import TcolorScrapyItem


class GetcolorSpider(scrapy.Spider):
    name = "getcolor"
    allowed_domains = ["irocore.com"]
    start_urls = ["http://irocore.com/"]

    def parse(self, response):
        # print(response.css("#intro2 > ul > li > a::attr(title)"))
        titles_css: list = response.css("#intro2 > ul > li > a::attr(title)")
        hrefs_css: list = response.css("#intro2 > ul > li > a::attr(href)")
        for title, href in zip(titles_css, hrefs_css):
            print(title.get())
            item = TcolorScrapyItem()
            item["category"] = href.get()[len("/category/") : -1]
            item["categoryJPName"] = title.get()
            yield item
        # return
        # for href in response.css("#intro2 > ul > li > a::attr(href)"):
        #     item = TcolorScrapyItem()
        #     url = "http://irocore.com" + href.get()

        #     category = href.get()[len("/category/") : -1]
        #     item["category"] = category
        #     item["categoryJPName"]

        #     # yield scrapy.Request(url, callback=self.parse_colors, meta={"item": item})
        #     # yield item
        #     return

    def parse_colors(self, response):
        hrefs = response.css(
            "#content > article > div.news10 > ul > li > a::attr(href)"
        )
        for href in hrefs:
            url = href.get()

            item = response.meta["item"]
            # item["url"] = url

            # yield item
            yield scrapy.Request(
                url, callback=self.parse_item, meta={"item": item, "url": url}
            )

    def parse_item(self, response):
        name = "".join(
            response.css(
                "#content > article > div > table > tbody > tr:nth-child(1) > td::text"
            ).getall()
        )
        colorcode = "".join(
            response.css(
                "#content > article > div > table > tbody > tr:nth-child(5) > td > input::attr(value)"
            ).getall()
        )

        text: str = "".join(
            response.css("#content > article > div.entry-content").getall()
        )
        text = re.sub(re.compile("<.*?>"), "", text)
        text = re.sub(re.compile("\s"), "", text)

        want_parse_string: str = text
        ads_id = want_parse_string.find("(ads")
        delete_ads_string: str = want_parse_string
        if ads_id >= 0:
            delete_ads_string: str = want_parse_string[:ads_id]

        other_id = delete_ads_string.rfind("色見本")
        delete_other_string: str = delete_ads_string
        if other_id >= 0:
            delete_other_string: str = delete_ads_string[: other_id + len("色見本")]

        # print(string[string.find("9") + len("h") :])
        head_id = delete_other_string.find("色の説明")
        delete_head_string: str = delete_other_string
        if head_id >= 0:
            delete_head_string: str = delete_other_string[head_id + len("色の説明") :]
        description = delete_head_string

        item = response.meta["item"]
        url = response.meta["url"]

        item["name"] = name
        item["url"] = url
        item["colorcode"] = colorcode
        item["description"] = description

        yield item
