import json

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from bitfinex.utils import Bitfinex


def home(request):
    btf = Bitfinex()
    symbols = btf.get_symbols()
    return render(request, 'home.html', {'symbols': symbols})


def candle(request, symbol):
    btf = Bitfinex()
    dates, prices = btf.get_candle(symbol)
    data = btf.get_ticker(symbol)
    item = {'dates': dates,
            'prices': prices,
            'today': (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
            'price': data['last_price'],
            'volume': data['volume'],
            'high': data['high'],
            'low': data['low'],
            'ask': data['ask'],
            'bid': data['bid'],
            'sub_currency': symbol[3:].upper(),
            'main_currency': symbol[:3].upper()
            }
    return HttpResponse(json.dumps(item), content_type='application/json')


def update_data(request, symbol):
    btf = Bitfinex()
    try:
        data = btf.get_ticker(symbol)
        item = {
            'last_price': float(data['last_price']),
            'volume': data['volume'],
            'high': data['high'],
            'low': data['low'],
            'ask': data['ask'],
            'bid': data['bid'],
            'price': data['last_price'],
            'timestamp': datetime.fromtimestamp(int(float(data['timestamp']))).strftime('%Y-%m-%d %H:%M:%S'),
            'sub_currency': symbol[3:].upper(),
            'main_currency': symbol[:3].upper()
        }
        return HttpResponse(json.dumps(item), content_type='application/json')
    except KeyError:
        return HttpResponse(json.dumps({'error': 'hit exceed'}), content_type='application/json')