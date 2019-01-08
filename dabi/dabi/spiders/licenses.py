# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Field, Selector, Request
from dabi.items import TakeFirstItemLoader


class LicenseEntry(Item):
    # №     Вид     Ліцензія    ЄДРПОУ  Ліцензіат   Адреса  Дата    Дійсна до
    number = Field()
    kind = Field()
    license = Field()
    edrpou = Field()
    obj = Field()
    address = Field()
    start_date = Field()
    end_date = Field()


class LicensesSpider(Spider):
    name = "licenses"
    allowed_domains = ["dabi.gov.ua"]   

    def start_requests(self):
        yield Request(
            url="https://dabi.gov.ua/license/list.php?&&page=1",
            meta={
                "invalidate_cache": True
            }
        )

    def parse(self, response):
        s = Selector(response)
        trs = s.xpath("//table[contains(@class, 'listTable')]"
                      "//tr[not(@class)][not(@id)]")

        for tr in trs:
            item = TakeFirstItemLoader(item=LicenseEntry(), selector=tr)

            item.add_xpath("number", "./td[1]/text()")
            item.add_xpath("kind", "./td[2]/text()")
            item.add_xpath("license", "./td[3]/text()")
            item.add_xpath("edrpou", "./td[4]/text()")
            item.add_xpath("obj", "./td[5]/text()")
            item.add_xpath("address", "./td[6]/text()")
            item.add_xpath("start_date", "./td[7]/text()")
            item.add_xpath("end_date", "./td[8]/text()")

            yield item.load_item()

        max_page = int(
            s.xpath("//div[@id='pages']/a/@href").re("page=(\d*)")[-1])

        for page in range(2, max_page + 1):
            yield Request(
                url="https://dabi.gov.ua/license/list.php?&&page=%s" % page,
                meta={
                    "invalidate_cache": page in [max_page - i for i in range(50)]
                }
            )
