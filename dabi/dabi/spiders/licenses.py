# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Field, Selector, Request, log


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
    allowed_domains = ["asdev.com.ua"]

    def start_requests(self):
        for page in range(1, 1228):
            yield Request(url="http://asdev.com.ua/license/list.php?&&page=%s" % page)

    def parse(self, response):
        s = Selector(response)
        trs = s.xpath("//table[contains(@class, 'listTable')]//tr[not(@class)][not(@id)]")

        if len(trs) != 50:
            log.msg("ALARM: %s has %s items, not 50" % (response.url, len(trs)))

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
