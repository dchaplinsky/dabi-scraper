from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.utils.gz import gunzip
from scrapy.contrib.httpcache import DummyPolicy


class MetaDummyPolicy(DummyPolicy):
    def is_cached_response_fresh(self, response, request):
        return not request.meta.get("invalidate_cache", False)


class ItemNumbersMetaDummyPolicy(MetaDummyPolicy):
    def is_cached_response_fresh(self, response, request):
        if super(ItemNumbersMetaDummyPolicy, self).is_cached_response_fresh(
                response, request):

            body = gunzip(response.body)

            h = HtmlResponse(url=response.url, body=body)
            s = Selector(h)
            return len(s.xpath("//table[contains(@class, 'listTable')]"
                               "//tr[not(@class)][not(@id)]")) == 50
        else:
            return False
