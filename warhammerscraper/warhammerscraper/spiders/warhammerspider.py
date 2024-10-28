import scrapy
import json
import copy
import requests
from warhammerscraper.items import WarhammerItem  
from dotenv import load_dotenv
import os

class BaseSpider(scrapy.Spider):

    url = f'https://m5ziqznq2h-1.algolianet.com/1/indexes/*/queries'

    load_dotenv('../../../.env') 

    API_ID = os.getenv('X-Algolia-Application-Id')
    API_KEY = os.getenv('X-Algolia-Api-Key')

    headers = {
        'Host': 'm5ziqznq2h-2.algolianet.com',
        'Sec-Ch-Ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
        'X-Algolia-Application-Id': API_ID,
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Algolia-Api-Key': API_KEY,
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.warhammer.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.warhammer.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': 'u=4, i',
        'Connection': 'keep-alive'
    }

    expansions = [
        r"Warhammer%2040%2C000",
        r"Age%20of%20Sigmar",
        r"The%20Horus%20Heresy",
        r"The%20Old%20World",
        r"Middle-Earth",
    ]

    data = {
        "requests":[
            {"indexName":"prod-lazarus-product-en-us",
                "params":r"clickAnalytics=true&facetFilters=%5B%5B%22GameSystemsRoot.lvl0%3Aputexpansionhere%22%5D%5D&facets=%5B%22GameSystemsRoot.lvl0%22%2C%22GameSystemsRoot.lvl1%22%2C%22brushType%22%2C%22format%22%2C%22genre%22%2C%22isAvailableWhileStocksLast%22%2C%22isLastChanceToBuy%22%2C%22isMadeToOrder%22%2C%22isNewRelease%22%2C%22isPreOrder%22%2C%22isPrintOnDemand%22%2C%22isWebstoreExclusive%22%2C%22material%22%2C%22paintColourRange%22%2C%22paintType%22%2C%22productType%22%2C%22series%22%5D&filters=GameSystemsRoot.lvl0%3A%22putexpansionhere%22&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=36&maxValuesPerFacet=101&page=0&query=&tagFilters="
            },
            {"indexName":"prod-lazarus-product-en-us",
                "params":r"analytics=false&clickAnalytics=false&facets=%5B%22GameSystemsRoot.lvl0%22%5D&filters=GameSystemsRoot.lvl0%3A%22putexpansionhere%22&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=0&maxValuesPerFacet=101&page=0&query="
            }
        ]
    }

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'output/warhammer.csv',
        'FEED_EXPORT_ENCODING': 'ANSI',
    }

    # Currency Conversion
    conversion_api_url = 'https://v6.exchangerate-api.com/v6/1ac9f55826bdbe40e572718f/latest/USD'

    # Making our request
    api_response = requests.get(conversion_api_url)
    api_data = api_response.json()

    # Your JSON object
    USDtoMYR = api_data['conversion_rates']['MYR']
    USDtoGBP = api_data['conversion_rates']['GBP']

    def __init__(self):
        self.page_counter = 0
        self.data_copy = copy.deepcopy(self.data)

    def start_requests(self):
        # Set expansion
        for i in range(len(self.data_copy['requests'])):
            self.data_copy['requests'][i]['params'] = self.data['requests'][i]['params'].replace("putexpansionhere", f"{self.expansions[self.expansionIndex]}")
        yield scrapy.Request(self.url, method='POST', headers=self.headers, body=json.dumps(self.data_copy), callback=self.parse)

    def parse(self, response):
        products = json.loads(response.text)

        # If page return empty results, end it
        if len(products['results'][0]['hits']) == 0:
            return

        else:
            # Get all products from the page
            for product in products['results'][0]['hits']:
                yield self.parse_product(product)
            
            # Go to next page
            self.data_copy['requests'][0]['params'] = self.data_copy['requests'][0]['params'].replace(f"page={self.page_counter}", f"page={self.page_counter+1}")
            self.page_counter += 1

        yield scrapy.Request(self.url, method='POST', headers=self.headers, body=json.dumps(self.data_copy), callback=self.parse)

    def parse_product(self, product):
        item = WarhammerItem()
        item['productType'] = product['productType']
        item['name'] = product['name'].replace("–", "-")
        item['price_USD'] = "$" + str(product['price'])
        item['price_GBP'] = "£" + str(round(product['price'] * self.USDtoGBP, 2))
        item['price_RM'] = "RM" + str(round(product['price'] * self.USDtoMYR, 2))
        item['expansion'] = product['GameSystemsRoot']['lvl0'][0]
        item['isInStock'] = product['isInStock']
        # item['currency'] = product['ctPrice']['currencyCode']
        # item['quantityLimits'] = product['quantityLimits']
        # item['statusCode'] = product['statusCode']
        # item['isWebstoreExclusive'] = product['isWebstoreExclusive']
        # item['isAvailable'] = product['isAvailable']
        # item['isAvailableWhileStocksLast'] = product['isAvailableWhileStocksLast']
        # item['isLastChanceToBuy'] = product['isLastChanceToBuy']
        # item['shipsFromAbroad'] = product['shipsFromAbroad']
        # item['isMadeToOrder'] = product['isMadeToOrder']
        return item

class Warhammer40k(BaseSpider):
    expansionIndex = 0
    name = "Warhammer_40K"

class WarhammerAOS(BaseSpider):
    expansionIndex = 1
    name = "Warhammer_AOS"

class WarhammerTHH(BaseSpider):
    expansionIndex = 2
    name = "Warhammer_THH"

class WarhammerTOW(BaseSpider):
    expansionIndex = 3
    name = "Warhammer_TOW"

class WarhammerME(BaseSpider):
    expansionIndex = 4
    name = "Warhammer_ME"