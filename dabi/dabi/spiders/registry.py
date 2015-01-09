# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Field, Selector, FormRequest


class Entry(Item):
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
        for region in range(1, 28) + [99]:
            for year in range(2011, 2016):
                for month in range(1, 13):
                    yield self._build_request(region, year, month, page=1)

    def _build_request(self, region, year, month, page):
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
                "region": region
            },
            callback=self.parse)

    def parse(self, response):
        s = Selector(response)
        for tr in s.xpath("//table[contains(@class, 'listTable')]//tr[not(@class)][not(@id)]"):
            item = Entry()
            item["number"] = tr.xpath("./td[1]/text()").extract()
            item["idabk"] = tr.xpath("./td[2]/text()").extract()
            item["document"] = tr.xpath("./td[3]/text()").extract()
            item["obj"] = tr.xpath("./td[4]/text()").extract()
            item["cat"] = tr.xpath("./td[5]/text()").extract()
            item["customer"] = tr.xpath("./td[6]/text()").extract()
            item["tech_oversee"] = tr.xpath("./td[7]/text()").extract()
            item["year"] = response.meta["year"]
            item["month"] = response.meta["month"]

            yield item

        for x in s.xpath("//div[@id='pages']/a/@href").re("page=(\d*)"):
            yield self._build_request(
                region=response.meta["region"],
                year=response.meta["year"],
                month=response.meta["month"],
                page=x
            )
