# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WarhammerscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class WarhammerItem(scrapy.Item):
      productType = scrapy.Field()
      name = scrapy.Field()
      price_USD = scrapy.Field()
      price_GBP = scrapy.Field()
      price_RM = scrapy.Field()
      setting = scrapy.Field()
      isInStock = scrapy.Field()
   #    currency = scrapy.Field()
   #    quantityLimits = scrapy.Field()
   #    statusCode = scrapy.Field()
   #    isWebstoreExclusive = scrapy.Field()
   #    isAvailable = scrapy.Field()
   #    isAvailableWhileStocksLast = scrapy.Field()
   #    isLastChanceToBuy = scrapy.Field()
   #    shipsFromAbroad = scrapy.Field()
   #    isMadeToOrder = scrapy.Field()