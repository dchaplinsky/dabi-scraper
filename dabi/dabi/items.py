from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose


class TakeFirstItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(unicode.strip)
