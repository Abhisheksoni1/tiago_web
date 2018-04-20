import json

import requests
from django.http import HttpResponse

# Create your views here.

SYMBOLS = [
    "btcusd",
    "ltcusd",
    "ltcbtc",
    "ethusd",
    "ethbtc",
    "etcbtc",
    "etcusd",
    "rrtusd",
    "rrtbtc",
    "zecusd",
    "zecbtc",
    "xmrusd",
    "xmrbtc",
    "dshusd",
    "dshbtc",
    "btceur",
    "btcjpy",
    "xrpusd",
    "xrpbtc",
    "iotusd",
    "iotbtc",
    "ioteth",
    "eosusd",
    "eosbtc",
    "eoseth",
    "sanusd",
    "sanbtc",
    "saneth",
    "omgusd",
    "omgbtc",
    "omgeth",
    "bchusd",
    "bchbtc",
    "bcheth",
    "neousd",
    "neobtc",
    "neoeth",
    "etpusd",
    "etpbtc",
    "etpeth",
    "qtmusd",
    "qtmbtc",
    "qtmeth",
    "avtusd",
    "avtbtc",
    "avteth",
    "edousd",
    "edobtc",
    "edoeth",
    "btgusd",
    "btgbtc",
    "datusd",
    "datbtc",
    "dateth",
    "qshusd",
    "qshbtc",
    "qsheth",
    "yywusd",
    "yywbtc",
    "yyweth",
    "gntusd",
    "gntbtc",
    "gnteth",
    "sntusd",
    "sntbtc",
    "snteth",
    "ioteur",
    "batusd",
    "batbtc",
    "bateth",
    "mnausd",
    "mnabtc",
    "mnaeth",
    "funusd",
    "funbtc",
    "funeth",
    "zrxusd",
    "zrxbtc",
    "zrxeth",
    "tnbusd",
    "tnbbtc",
    "tnbeth",
    "spkusd",
    "spkbtc",
    "spketh",
    "trxusd",
    "trxbtc",
    "trxeth",
    "rcnusd",
    "rcnbtc",
    "rcneth",
    "rlcusd",
    "rlcbtc",
    "rlceth",
    "aidusd",
    "aidbtc",
    "aideth",
    "sngusd",
    "sngbtc",
    "sngeth",
    "repusd",
    "repbtc",
    "repeth",
    "elfusd",
    "elfbtc",
    "elfeth",
    "btcgbp",
    "etheur",
    "ethjpy",
    "ethgbp",
    "neoeur",
    "neojpy",
    "neogbp",
    "eoseur",
    "eosjpy",
    "eosgbp",
    "iotjpy",
    "iotgbp",
    "iosusd",
    "iosbtc",
    "ioseth",
    "aiousd",
    "aiobtc",
    "aioeth",
    "requsd",
    "reqbtc",
    "reqeth",
    "rdnusd",
    "rdnbtc",
    "rdneth",
    "lrcusd",
    "lrcbtc",
    "lrceth",
    "waxusd",
    "waxbtc",
    "waxeth",
    "daiusd",
    "daibtc",
    "daieth",
    "cfiusd",
    "cfibtc",
    "cfieth",
    "agiusd",
    "agibtc",
    "agieth",
    "bftusd",
    "bftbtc",
    "bfteth",
    "mtnusd",
    "mtnbtc",
    "mtneth",
    "odeusd",
    "odebtc",
    "odeeth"
]


def config(request):
    data = {
        'supported_resolutions': ["1",
                                  "5",
                                  "15",
                                  "60",
                                  "240",
                                  "1D"],
        'supports_group_request': False,
        'supports_marks': False,
        'supports_search': True,
        'supports_time': True,
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


def symbols(request):
    results = {}
    symbol = request.GET['symbol'].upper()
    # print(request.symbol)
    if symbol.lower() in SYMBOLS:
        results["name"] = symbol
        results["ticker"] = symbol
        results["description"] = symbol
        results["type"] = ""
        results["session"] = "24x7"
        results["exchange"] = ""
        results["listed_exchange"] = ""
        results["timezone"] = "America/Chicago"
        results["minmov"] = 0.1
        results["pricescale"] = 1000000
        results["minmove2"] = 0
        results["fractional"] = False
        results["has_intraday"] = True
        results["supported_resolutions"] = "1", "5", "15", "60", "240", "1D",
        results["intraday_multipliers"] = ""
        results["has_seconds"] = False
        results["seconds_multipliers"] = ""
        results["has_daily"] = True
        results["has_weekly_and_monthly"] = False
        results["has_empty_bars"] = True
        results["force_session_rebuild"] = ""
        results["has_no_volume"] = False
        results["volume_precision"] = ""
        results["data_status"] = ""
        results["expired"] = ""
        results["expiration_date"] = ""
        results["sector"] = ""
        results["industry"] = ""
        results["currency_code"] = symbol
    return HttpResponse(json.dumps(results), content_type='application/json')


def search(request):
    # /search?query=<query>&type=<type>&exchange=<exchange>&limit=<limit>
    query = request.GET['query']
    type = request.GET['type']
    exchange = request.GET['exchange']
    limit = request.GET['limit']
    result = []
    if exchange == '':
        for symbol in SYMBOLS:
            if query in symbol:
                data = {
                        "description": symbol.upper(),
                        "exchange": "",
                        "full_name": symbol.upper(),
                        "symbol": symbol.upper(),
                        "ticker": symbol.upper(),
                        "type": ""
                        }
                result.append(data)
        if len(result) > int(limit):
            result = result[:30]
    return HttpResponse(json.dumps(result), content_type='application/json')


def history(request):
    try:
        symbol = request.GET['symbol']
        from_date = request.GET['from']
        to_date = request.GET['to']
        resolution = request.GET['resolution']
        r_dict = {
                '1': '1m',
                '5': '5m',
                '15': '15m',
                '30': '30m',
                '60': '1h',
                '1D': '1D'
         }
        # print(symbol,from_date,to_date,resolution)
        #/history?symbol=<ticker_name>&from=<unix_timestamp>&to=<unix_timestamp>&resolution=<resolution>

        data = {
            'limit': "500",
            'start': str(from_date),
            'end': str(to_date),
            'sort': "-1"}
        url = 'https://api.bitfinex.com/v2/candles/trade:{}:t{}/hist'.format(r_dict[resolution], symbol.upper())
        content = json.loads(requests.get(url, headers=data).text)[::-1]
        result = {
            's': "ok",
            't': [],
            'c': [],
            'o': [],
            'h': [],
            'l': [],
            'v': []
        }
        # print(content)
        for item in content:
            result['t'].append(int(float(item[0])/1000))
            result['o'].append(item[1])
            result['c'].append(item[2])
            result['h'].append(item[3])
            result['l'].append(item[4])
            result['v'].append(item[5])
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as e:
        # print(e)
        pass
    return HttpResponse(json.dumps({'s': "no_data"}), content_type='application/json')


def time(request):
    data = json.loads(requests.get("https://api.bitfinex.com/v1/pubticker/btcusd").text)
    server_time = int(float(data['timestamp']))
    return HttpResponse(server_time, content_type='application/json')