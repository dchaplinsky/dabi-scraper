# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Field, Selector, Request
from scrapy.contrib.loader.processor import TakeFirst


class LicenseEntry(Item):
    # №     Вид     Ліцензія    ЄДРПОУ  Ліцензіат   Адреса  Дата    Дійсна до
    number = Field(input_processor=unicode.strip, output_processor=TakeFirst())
    kind = Field(input_processor=unicode.strip, output_processor=TakeFirst())
    license = Field(
        input_processor=unicode.strip, output_processor=TakeFirst())
    edrpou = Field(input_processor=unicode.strip, output_processor=TakeFirst())
    obj = Field(input_processor=unicode.strip, output_processor=TakeFirst())
    address = Field(
        input_processor=unicode.strip, output_processor=TakeFirst())
    start_date = Field(
        input_processor=unicode.strip, output_processor=TakeFirst())
    end_date = Field(
        input_processor=unicode.strip, output_processor=TakeFirst())


class LicensesSpider(Spider):
    name = "licenses"
    allowed_domains = ["asdev.com.ua"]

    def start_requests(self):
        yield Request(
            url="http://asdev.com.ua/license/list.php?&page=1",
            meta={
                "invalidate_cache": True
            }
        )

    def parse(self, response):
        s = Selector(response)
        trs = s.xpath("//table[contains(@class, 'listTable')]"
                      "//tr[not(@class)][not(@id)]")

        for tr in trs:
            item = LicenseEntry()

            item["number"] = tr.xpath("./td[1]/text()").extract()
            item["kind"] = tr.xpath("./td[2]/text()").extract()
            item["license"] = tr.xpath("./td[3]/text()").extract()
            item["edrpou"] = tr.xpath("./td[4]/text()").extract()
            item["obj"] = tr.xpath("./td[5]/text()").extract()
            item["address"] = tr.xpath("./td[6]/text()").extract()
            item["start_date"] = tr.xpath("./td[7]/text()").extract()
            item["end_date"] = tr.xpath("./td[8]/text()").extract()

            yield item

        max_page = int(
            s.xpath("//div[@id='pages']/a/@href").re("page=(\d*)")[-1])

        for page in range(2, max_page + 1):
            yield Request(
                url="http://asdev.com.ua/license/list.php?&page=%s" % page,
                meta={
                    "invalidate_cache": page == max_page
                }
            )
