# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from jianshu02.items import Jianshu02Item


class Jianshu03Spider(CrawlSpider):
    name = 'jianshu03'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[a-z1-9]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):

        try:
            title = response.xpath("//div[@class='article']/h1/text()").get()
            #处理url
            url = response.url.split("?")[0]
            articleid = url.split("/")[-1]
            content = response.xpath("//div[@class='show-content-free']").get()
            author =  response.xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/span/a/text()").get()
            publicdate = response.xpath("//span[@class='publish-time']/text()").get()
            if publicdate:
                publicdate =  publicdate.replace("*","").strip()
            else:
                publicdate = "2000-10-10 20:20:20"

            text_num = response.xpath("//span[@class='wordage']/text()").get().split(" ")[1]
            read_num = response.xpath("//span[@class='views-count']/text()").get().split(" ")[1]
            comment_num = response.xpath("//span[@class='comments-count']/text()").get().split(" ")[1]
            like_num = response.xpath("//span[@class='likes-count']/text()").get().split(" ")[1]

            stars = "".join(response.xpath("//span[@class='jsd-meta']/text()").getall()).strip()
            cated = ",".join(response.xpath("/html/body/div[2]/div[1]/div/div[2]//a/div/text()").getall())

            item = Jianshu02Item(
                title = title,
                url = url,
                content = content,
                articleid = articleid,
                author = author,
                publicdate = publicdate,
                text_num = text_num,
                read_num = read_num,
                comment_num = comment_num,
                like_num = like_num,
                cated = cated,
                stars = stars
            )
            yield item

        except Exception as e:
            print("=============="+str(e.args))