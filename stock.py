import pandas as pd
import yfinance as yf
import pandas_ta as ta


class Stock:
    tic = None
    period = None
    intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    interval = None
    long_response = None
    short_response = None
    stocks = pd.DataFrame()
    
    def crossing(self):
        if (self.interval == '1m'):
            self.period = '7d'
        elif (self.interval in ('2m', '5m', '15m', '30m', '60m', '90m', '1h')):
            self.period = '60d'
        elif (self.interval in ('1d', '5d', '1wk')):
            self.period = '5y'
        elif (self.interval in ('1mo', '3mo')):
            self.period = 'max'

        ticker = yf.Ticker(self.tic)
        ticker_history = ticker.history(period=f"{self.period}", interval=f"{self.interval}")
        ticker_history.index.names = ['Datetime']
        ticker_history.reset_index(inplace=True)
        ticker_ohlc = ticker_history.loc[:, ['Datetime', 'Open', 'High', 'Low', 'Close']]
        ticker_ohlc.set_index('Datetime')

        # Adding EMAs to dataframe:
        ticker_ohlc.ta.ema(close='Close', length=9, append=True)
        ticker_ohlc.ta.ema(close='Close', length=21, append=True)
        ticker_ohlc.ta.ema(close='Close', length=200, append=True)

        # Reversing the dataframe:
        ticker_rev = ticker_ohlc
        ticker_rev = ticker_rev.dropna(axis=0)
        # print(ticker_rev.tail(5))

        # Looking for crossing:
        for i in range(1, len(ticker_rev.Close)):
            if (ticker_rev.iloc[i, 5] > ticker_rev.iloc[i, 6] and  
                ticker_rev.iloc[i, 5] > ticker_rev.iloc[i, 7] and
                ticker_rev.iloc[i, 6] > ticker_rev.iloc[i, 7] and
                ((ticker_rev.iloc[i-1, 5] <= ticker_rev.iloc[i-1, 6] and
                ticker_rev.iloc[i-1, 5] > ticker_rev.iloc[i-1, 7] and
                ticker_rev.iloc[i-1, 6] > ticker_rev.iloc[i-1, 7]) 
                or
                (ticker_rev.iloc[i-1, 5] <= ticker_rev.iloc[i-1, 6] and
                ticker_rev.iloc[i-1, 5] < ticker_rev.iloc[i-1, 7] and
                ticker_rev.iloc[i-1, 6] < ticker_rev.iloc[i-1, 7]))):
                self.long_response = f"Последнее актуальное время открытия длинной позиции для интервала {self.interval}: {str(ticker_rev.iloc[i]['Datetime'])}"
                # print(ticker_rev.iloc[[i]])
                # print(ticker_rev.iloc[[i-1]])
                break
            else:
                self.long_response = f"Последнее актуальное время открытия длинной позиции для интервала {self.interval} не найдено."

        for i in range(1, len(ticker_rev.Close)):
            if (ticker_rev.iloc[i, 5] < ticker_rev.iloc[i, 6] and  
                ticker_rev.iloc[i, 5] < ticker_rev.iloc[i, 7] and
                ticker_rev.iloc[i, 6] < ticker_rev.iloc[i, 7] and
                (ticker_rev.iloc[i-1, 5] >= ticker_rev.iloc[i-1, 6] and
                ticker_rev.iloc[i-1, 5] < ticker_rev.iloc[i-1, 7] and
                ticker_rev.iloc[i-1, 6] < ticker_rev.iloc[i-1, 7])):
                self.short_response = f"Последнее актуальное время открытия короткой позиции для интервала {self.interval}: {str(ticker_rev.iloc[i]['Datetime'])}"
                # print(ticker_rev.iloc[[i]])
                # print(ticker_rev.iloc[[i-1]])
                break
            else:
                self.short_response = f"Последнее актуальное время открытия короткой позиции для интервала {self.interval} не найдено."

        # print(self.long_response)
        # print(self.short_response)
        return(self.long_response, self.short_response)