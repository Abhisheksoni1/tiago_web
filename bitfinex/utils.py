import requests
import json
from time import  mktime
import datetime


class Bitfinex(object):
    BASE_URL = 'https://api.bitfinex.com/v1/'

    def get_symbols(self):
        end_point = 'symbols'
        symbols = json.loads(requests.get(self.BASE_URL + end_point).text)
        return symbols

    def get_ticker(self, symbol):
        end_point = 'pubticker/{}'.format(symbol)
        data = json.loads(requests.get(self.BASE_URL + end_point).text)
        return data

    def get_candle(self, symmbol, interval='5m'):
        data = {
            'limit': "500",
            'start': str(mktime((datetime.datetime.now() - datetime.timedelta(hours=24)).timetuple())),
            'end': str(mktime(datetime.datetime.now().timetuple())),
            'sort': "1"}
        url = 'https://api.bitfinex.com/v2/candles/trade:{}:t{}/hist'.format(interval, symmbol.upper())
        data = json.loads(requests.get(url, headers=data).text)
        date_array, prices = [], []

        for item in data:
            date_array.append(datetime.datetime.fromtimestamp(int(item[0]/1000)).strftime('%Y-%m-%d %H:%M:%S'))
            prices.append(item[2])
        return date_array[::-1], prices[::-1]