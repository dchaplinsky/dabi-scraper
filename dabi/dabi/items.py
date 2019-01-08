from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose


class TakeFirstItemLoader(ItemLoader):
    default_output_processor = Join()
    default_input_processor = MapCompose(unicode.strip)
