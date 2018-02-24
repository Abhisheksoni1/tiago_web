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
    item = {'dates': dates,
            'prices': prices,
            'today': (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            }
    return HttpResponse(json.dumps(item), content_type='application/json')