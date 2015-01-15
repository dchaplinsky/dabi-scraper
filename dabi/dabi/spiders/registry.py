# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Field, Selector, FormRequest
from dabi.items import TakeFirstItemLoader
import datetime


class RegistryEntry(Item):
    # №   ІДАБК   Документ    Об`єкт  Кат.    Замовник    Технічний нагляд
    number = Field()
    idabk = Field()
    document = Field()
    obj = Field()
    cat = Field()
    customer = Field()
    tech_oversee = Field()
    year = Field()
    month = Field()


class RegistrySpider(Spider):
    name = "registry"
    allowed_domains = ["asdev.com.ua"]

    def start_requests(self):
        now = datetime.datetime.now()

        for region in range(1, 28) + [99]:
            for year in range(2011, 2016):
                for month in range(1, 13):
                    invalidate = (year == now.year and month == now.month)
                    yield self._build_request(
                        region, year, month, page=1,
                        invalidate_cache=invalidate
                    )

    def _build_request(self, region, year, month, page, invalidate_cache):
        return FormRequest(
            url="http://asdev.com.ua/dabi/list.php?sort=num&order=DESC&page=%s" % page,
            formdata={
                'filter[regob]': str(region),
                'filter[date]': str(year),
                'filter[date2]': "%02d" % month,
            },
            meta={
                "year": year,
                "month": month,
                "page": page,
                "region": region,
                "invalidate_cache": invalidate_cache
            },
            callback=self.parse)

    def parse(self, response):
        s = Selector(response)
        for tr in s.xpath("//table[contains(@class, 'listTable')]//tr[not(@class)][not(@id)]"):
            item = TakeFirstItemLoader(item=RegistryEntry(), selector=tr)

            item.add_xpath("number", "./td[1]/text()")
            item.add_xpath("idabk", "./td[2]/text()")
            item.add_xpath("document", "./td[3]/text()")
            item.add_xpath("obj", "./td[4]/text()")
            item.add_xpath("cat", "./td[5]/text()")
            item.add_xpath("customer", "./td[6]/text()")
            item.add_xpath("tech_oversee", "./td[7]/text()")

            item.add_value("year", unicode(response.meta["year"]))
            item.add_value("month", unicode(response.meta["month"]))

            yield item.load_item()

        pages = s.xpath("//div[@id='pages']/a/@href").re("page=(\d*)")

        if pages:
            max_page = int(pages[-1])

            for page in range(2, max_page + 1):
                yield self._build_request(
                    region=response.meta["region"],
                    year=response.meta["year"],
                    month=response.meta["month"],
                    page=page,
                    invalidate_cache=False
                )
