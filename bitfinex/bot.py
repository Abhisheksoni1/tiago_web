from bitfinex.utils import Bitfinex
from time import sleep
import sys
from bitfinex.indicator import BotIndicators


def start():
    f = open("status.txt", 'r')
    data = f.read()
    mode = data.split(":")[1]
    f.close()
    f = open('bot_config.txt', 'r')
    data = f.read().split("#")
    for item in data:
        if "SYMBOL" in item:
            symbol = item.split(":")[1]
        elif "INTERVAL" in item:
            interval = item.split(":")[1]
    bot = Bitfinex()
    indicators = BotIndicators()
    f.close()

    # if mode == 'live':
    while True:
        f = open("status.txt", 'r')
        data = f.read()

        if data == "stop":
            print("bot closes...")
            sys.exit(1)
        f.close()
        data = bot.get_candle_close(symbol, interval)
        ma_list = indicators.moving_average(data, 20)
        f = open("indicator.txt", 'w')
        f.write("MA:{}@".format(ma_list))

        po_list = list(map(lambda i: round(i, 2), indicators.price_oscillator(data)))
        f.write("PO:{}@".format(po_list))
        rsi_list = indicators.RSI(data, 14)
        f.write("RSI:{}@".format(rsi_list))
        f.close()
        sleep(5)