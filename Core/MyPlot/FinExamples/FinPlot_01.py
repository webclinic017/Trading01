# https://pypi.org/project/finplot/
# https://github.com/highfestiva/finplot
from datetime import datetime

import finplot as fplt
import pandas as pd
import numpy as np
import talib

from ConfigDbSing import ConfigDbSing
from Db_form_data import Db_form_data
from Ticker import Ticker

if __name__ == '__main__':
  df = Db_form_data() # timeframe='1min'
  # fplt.candlestick_ochl(df[['open', 'close', 'high', 'low']])  # , 'volume'
  ax, axv, axstoch = fplt.create_plot(' -- SBRF -- ', rows=3, init_zoom_periods=300)
  ax.set_visible(xgrid=True, ygrid=True)
  axv.set_visible(xgrid=True, ygrid=True)
  df[['open', 'close', 'high', 'low']].plot(ax=ax, kind='candle')
  df[['open', 'close', 'volume']].plot(ax=axv, kind='volume')

  d = np.array(df['close'])
  sma = talib.SMA(d, 10)
  kama = talib.KAMA(d, timeperiod=25)
  stoch0, stoch1 = talib.STOCHRSI(d, 25, 10, 5, 0)

  df['sma'] = sma
  df['kama'] = kama
  df['stoch0'] = stoch0
  df['stoch1'] = stoch1

  fplt.plot(df.sma, legend='SMA', ax=ax)
  fplt.plot(df.kama, legend='KAMA', ax=ax)
  fplt.plot(df.stoch0, legend='stoch0', ax=axstoch)
  fplt.plot(df.stoch1, legend='stoch1', ax=axstoch)
  fplt.autoviewrestore()
  fplt.show()
  j=1