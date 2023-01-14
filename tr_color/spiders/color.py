import scrapy
import re
import json

# d = {"category":"",}
d = dict()
result = []

def append_key(name,init):
    d[name] = init

def append_list_value(name,value):
    d[name].append(value)

def reset():
    d = dict()

def red_append(value):
    d["red"]["colors"].append(value)

category = ""

class ColorSpider(scrapy.Spider):
    name = 'color'
    allowed_domains = ['irocore.com']
    start_urls = ['https://irocore.com/']
    def parse(self, response):
        
        for href in response.css('#intro2 > ul > li > a::attr(href)'):
            # d = dict()
            reset()
            url = 'http://irocore.com'+href.get()
            # print("url:"+url)
            cname = href.get()
            # print(cname[len("/category/"):-1])
            d["category"]=cname[len("/category/"):-1]
            global category
            category = cname[len("/category/"):-1]
            
            print("\n\n\ncategory")
            print(category)
            print("\n\n\n")
            yield scrapy.Request(url,callback=self.parse_items)
        with open('cccolor.json', mode='w',encoding='utf-8') as f:
            json.dump(result,f,ensure_ascii=False,indent=2)

    def parse_items(self,responce):
        d["colors"] = []
        # print(responce.css('#content > article > div.news10 > ul > li > a::attr(href)'))
        for href in responce.css('#content > article > div.news10 > ul > li > a::attr(href)'):
            url = href.get()
            # print("curl:"+url)
            yield scrapy.Request(url,callback=self.parse_item)
            break
        global result
        result.append(d)

    
    def parse_item(self,response):
        # a = response.css('#content > article > div > table > tbody > tr:nth-child(1) > td::text').get()
        # print(a)
        name = ''.join(response.css('#content > article > div > table > tbody > tr:nth-child(1) > td::text').getall())
        colorcode = ''.join(response.css('#content > article > div > table > tbody > tr:nth-child(5) > td > input::attr(value)').getall())
        text = ''.join(response.css('#content > article > div.entry-content').getall())
        # text = re.sub(re.compile('<style>.*</style>'),'',text)
        # text = re.sub(re.compile('<s.*?t>).*?</s.*?t>'),'',text)
        text = re.sub(re.compile('<.*?>'),'',text)
        text = re.sub(re.compile('\s'),'',text)
        color = dict()
        color["name"] = name
        color["colorcode"] = colorcode
        color["description"] = text
        global category
        d["colors"].append(color)
        # print("\n\n\ncolor\n")
        # print(color)
        # print("\n")
        # with open('test.json', mode='w',encoding='utf-8') as f:
        #     cj = json.dumps(color)
        #     print(cj)
        #     print("\n")
        #     ccjj = json.loads(cj,)
        #     print(ccjj)
        #     print("\nend\n")
        #     print("\n\n\n")
        #     json.dump(ccjj,f,ensure_ascii=False,indent=2,)
        

        
        yield{
            'name':name,
            'colorcode':colorcode,
            'description':text
        }
