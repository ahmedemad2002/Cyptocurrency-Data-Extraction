import scrapy
import json
import pandas as pd


class CoincolumnsSpider(scrapy.Spider):
    name = "coincolumns"
    part2 = pd.read_json('columnsdatapart2.json')
    ids = part2.id

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
            if id not in self.ids:
                request = scrapy.Request(f'https://api.coingecko.com/api/v3/coins/{id}?localization=false&sparkline=true', callback=self.parsecoin)
                yield request

    def parsecoin(self, response):
        coin = response.body
        coin = str(json.loads(coin))
        coin = eval(coin)

        all_dates = list(coin['market_data']['atl_date'].values())
        all_dates.extend(list(coin['market_data']['ath_date'].values()))
        try:
            added_date = min(all_dates)
        except:
            added_date = ''
        yield {
            'coingecko_rank': coin['coingecko_rank'],
            'market_cap_rank': coin['market_cap_rank'],
            'name': coin['name'],
            'symbol': coin['symbol'],
            'id': coin['id'],
            'categories': coin['categories'],
            'description': coin['description']['en'],
            'coingecko_score': coin['coingecko_score'],
            'developer_score': coin['developer_score'],
            'community_score': coin['community_score'],
            'community_data': coin['community_data']['twitter_followers'],
            'liquidity_score': coin['liquidity_score'],
            'total_value_locked': coin['market_data']['total_value_locked'],
            'current_price': coin['market_data']['current_price'].get('usd'),
            'mcap_to_tvl_ratio': coin['market_data']['mcap_to_tvl_ratio'],
            'fdv_to_tvl_ratio': coin['market_data']['fdv_to_tvl_ratio'],
            'market_cap': coin['market_data']['market_cap'].get('usd'),
            'total_volume': coin['market_data']['total_volume'].get('usd'),
            'fully_diluted_valuation': coin['market_data']['fully_diluted_valuation'].get('usd'),
            'price_change_percentage_30d': coin['market_data']['price_change_percentage_30d'],
            'total_supply': coin['market_data']['total_supply'],
            'max_supply': coin['market_data']['max_supply'],
            'circulating_supply': coin['market_data']['circulating_supply'],
            'country_origin': coin['country_origin'],
            'main_url': coin['links'].get('homepage'),
            'added_date': added_date
            }
