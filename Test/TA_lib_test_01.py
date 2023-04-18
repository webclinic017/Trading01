# https://github.com/matplotlib/mplfinance
import talib
import yfinance
import yfinance as yf
import mplfinance as mpf
from talib import abstract
import numpy as np

for it in talib.get_function_groups().keys():
  print(it)

print("---------------------------------------------")

print(talib.get_function_groups())

for it in talib.get_function_groups().values():
  print(it)

data=yf.download('SPY', start='2021-01-01', end='2021-12-31')
data.rename(columns={'Open':'open',
                     'High':'high',
                     'Low':'low',
                     'Adj Close':'close',
                     # 'Close':'close',
                     'Volume':'volume'}, inplace=True)
print(data)
d=np.array(data['close'])
sma = talib.SMA(d)
# mpf.plot(data)
# mpf.plot(data,type='candle',mav=(3,6,9),volume=True)
# mpf.plot(data,type='candle',mav=(7,12))
mpf.plot(data)
k=11