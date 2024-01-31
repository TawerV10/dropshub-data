import scrapy

class ScrapingItem(scrapy.Item):
    title = scrapy.Field()
    tags = scrapy.Field()
    invest = scrapy.Field()
    network = scrapy.Field()
    status = scrapy.Field()
    description = scrapy.Field()
    strategy = scrapy.Field()
    website = scrapy.Field()
    discord = scrapy.Field()
    logo = scrapy.Field()