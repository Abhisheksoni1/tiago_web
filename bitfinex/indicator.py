import numpy as np


class BotIndicators(object):
    def __init__(self):
        pass

    def moving_average(self, prices, period):
        num_prices = len(prices)

        if num_prices < period:
            # show error message
            raise SystemExit('Error: num_prices < period')

        sma_range = num_prices - period + 1

        smas = np.zeros(sma_range)

        for idx in range(sma_range):
            smas[idx] = np.mean(prices[idx:idx + period])

        return smas

    def price_oscillator(self, prices):
        po = []
        for i, price in enumerate(prices):
            if i == 0:
                po.append(0)
            else:
                po.append(float((price-prices[i-1])/prices[i-1])*100)
        return po

    def momentum(self, dataPoints, period=14):
        if (len(dataPoints) > period - 1):
            return dataPoints[-1] * 100 / dataPoints[-period]

    def EMA(self, prices, period):
        x = np.asarray(prices)
        weights = None
        weights = np.exp(np.linspace(-1., 0., period))
        weights /= weights.sum()

        a = np.convolve(x, weights, mode='full')[:len(x)]
        a[:period] = a[period]
        return a

    def MACD(self, prices, nslow=26, nfast=12):
        emaslow = self.EMA(prices, nslow)
        emafast = self.EMA(prices, nfast)
        return emaslow, emafast, emafast - emaslow

    def RSI(self, prices, period=14):
        try:
            deltas = np.diff(prices)
            seed = deltas[:period + 1]
            up = seed[seed >= 0].sum() / period
            down = -seed[seed < 0].sum() / period
            if down > 0:
                rs = up / down
                rsi = np.zeros_like(prices)
                rsi[:period] = 100. - 100. / (1. + rs)

            for i in range(period, len(prices)):
                delta = deltas[i - 1]  # cause the diff is 1 shorter
                if delta > 0:
                    upval = delta
                    downval = 0.
                else:
                    upval = 0.
                    downval = -delta

                up = (up * (period - 1) + upval) / period
                down = (down * (period - 1) + downval) / period
                if down >0 :
                    rs = up / down
                    rsi[i] = 100. - 100. / (1. + rs)
            if len(prices) > period:
                return rsi
            else:
                return 0  # output a neutral amount until enough prices in list to calculate RSI
        except Exception as e:
            return None