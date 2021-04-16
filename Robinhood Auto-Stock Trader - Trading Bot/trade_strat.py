# Create your own personal trading strategy to trade with
import pandas as pd

import robin_stocks.helper as helper
import robin_stocks.urls as urls

class trader():
    def __init__(self, stocks):
        self.stocks = stocks

        self.sma_hour = {stocks[i]: 0 for i in range(0, len(stocks))}
        self.run_time = 0
        self.buffer = 0.002 #0.2%

        self.price_sma_hour = {stocks[i]: 0 for i in range(0, len(stocks))}

    def get_historical_prices(self, stock, span):
        span_interval = {'day': '5minute', 'week': '10minute', 'month': 'hour', '3month': 'hour', 'year': 'day', '5year': 'week'}
        interval = span_interval[span]

        symbols = helper.inputs_to_set(stock)
        url = urls.historicals()
        payload = { 'symbols' : ','.join(symbols),
                    'interval' : interval,
                    'span' : span,
                    'bounds' : 'regular'}

        data = helper.request_get(url,'results',payload)

        historical_data = []
        for item in data:
            for subitem in item['historicals']:
                historical_data.append(subitem)

        df = pd.DataFrame(historical_data)

        dates_times = pd.to_datetime(df.loc[:, 'begins_at'])
        close_prices = df.loc[:, 'close_price'].astype('float')

        df_price = pd.concat([close_prices, dates_times], axis=1)
        df_price = df_price.rename(columns={'close_price': stock})
        df_price = df_price.set_index('begins_at')

        return(df_price)

    def get_sma(self, stock, df_prices, window=12):
        sma = df_prices.rolling(window=window, min_periods=window).mean()
        sma = round(float(sma[stock].iloc[-1]), 4)
        return(sma)

    def get_price_sma(self, price, sma):
        price_sma = round(price/sma, 4)
        return(price_sma)

    def trade_option(self, stock, price):
        # gets new sma_hour every 5min
        if self.run_time % (5) == 0:
            df_historical_prices = self.get_historical_prices(stock, span='day')
            self.sma_hour[stock] = self.get_sma(stock, df_historical_prices[-12:], window=12)

        self.price_sma_hour[stock] = self.get_price_sma(price, self.sma_hour[stock])
        p_sma = self.price_sma_hour[stock]

        i1 = "BUY" if self.price_sma_hour[stock]<(1.0-self.buffer) else "SELL" if self.price_sma_hour[stock]>(1.0+self.buffer) else "NONE"
        if i1 == "BUY":
            trade = "BUY"
        elif i1 == "SELL":
            trade = "SELL"
        else:
            trade = "HOLD"

        return(trade)
