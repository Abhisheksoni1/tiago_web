import json

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
import threading
from bitfinex import bot
# Create your views here.
from bitfinex.utils import Bitfinex


def home(request):
    btf = Bitfinex()
    symbols = btf.get_symbols()
    return render(request, 'home.html', {'symbols': symbols})


def candle(request, symbol, interval='1m'):
    btf = Bitfinex()
    dates, prices = btf.get_candle(symbol, interval=interval)
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
        f = open("indicator.txt", 'r')
        data = f.read().split("@")
        ma = []
        for indicator in data:
            if "MA" in indicator:
                ma_list = indicator.split(":")[1]
                ma_list = ma_list.split(" ")
                for i in ma_list:
                    i = i.replace(" ", "").replace("[", "").replace("]", "").replace("\n", "")
                    if i == "":
                        pass
                    else:
                        ma.append(eval(i))
        # print(ma)
        item['ma_list'] = ma
        return HttpResponse(json.dumps(item), content_type='application/json')
    except KeyError:
        return HttpResponse(json.dumps({'error': 'hit exceed'}), content_type='application/json')


def stop(request):
    try:
        f = open("status.txt", 'w')
        f.write("stop")
        f.close()
        return HttpResponse(json.dumps({"status": 200}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({"status": 404}), content_type='application/json')


def start(request, id, symbol, interval):
    try:
        f = open("status.txt", 'w')
        id = int(id)
        if id == 1:
            f.write("start:backtest")
        elif id == 2:
            f.write("start:backtest")
        f.close()
        f = open("bot_config.txt", 'w')
        f.write("SYMBOL:{}#".format(symbol))
        f.write("INTERVAL:{}#".format(interval))
        f.close()
        threading.Thread(target=bot.start).start()
        return HttpResponse(json.dumps({"status": 200}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({"status": 404}), content_type='application/json')

