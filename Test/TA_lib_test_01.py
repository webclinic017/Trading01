import talib
import yfinance
import yfinance as yf
import mplfinance as mpf
from talib import abstract
import numpy as np
for it in talib.get_function_groups().keys():
  print(it)

print("---------------------------------------------")
# for it in talib.get_function_groups():
#   print(it)
print(talib.get_function_groups())

for it in talib.get_function_groups().values():
  print(it)

data=yf.download('SPY', start='2021-01-01', end='2021-12-31')
data.rename(columns={'Open':'open',
                     'High':'high',
                     'Low':'low',
                     'Adj Close':'close',
                     'Volume':'volune'}, inplace=True)
print(data)
d=np.array(data['close'])
sma = talib.SMA(d)
k=11