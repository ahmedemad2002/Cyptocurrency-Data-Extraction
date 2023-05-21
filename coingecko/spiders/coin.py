import scrapy
import json


class CoinSpider(scrapy.Spider):
    name = "coin"
    

    custom_settings = {
                'FEED_EXPORTERS': {
                    'csv': 'coingecko.settings.NoHeaderCsvItemExporter'
                },
                'LOG_LEVEL': 'INFO'
            }
    
    

    start_urls = ["https://api.coingecko.com/api/v3/coins/list?include_platform=false"]

    def parse(self, response):
        # print('response BODY: ', response.body)
        for item in eval(response.body):
            id = item['id']
            request = scrapy.Request(f'https://api.coingecko.com/api/v3/coins/{id}?localization=false&sparkline=true', callback=self.parsecoin)
            yield request

    def parsecoin(self, response):
        data = response.body
        data = json.loads(data)
        yield data
