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
  # ax, axv, axstoch = fplt.create_plot(' -- SBRF -- ', rows=3, init_zoom_periods=300)
  axx = fplt.create_plot(' -- SBRF -- ', rows=3, init_zoom_periods=300)
  axx[0].set_visible(xgrid=True, ygrid=True)
  axx[1].set_visible(xgrid=True, ygrid=True)
  df[['open', 'close', 'high', 'low']].plot(ax=axx[0], kind='candle')
  df[['open', 'close', 'volume']].plot(ax=axx[1], kind='volume')

  d = np.array(df['close'])
  stoch = talib.STOCHRSI(d, 25, 10, 5, 0)

  df['sma'] = talib.SMA(d, 10)
  fplt.plot(df.sma, legend='SMA', ax=axx[0])

  df['kama'] = talib.KAMA(d, timeperiod=25)
  fplt.plot(df.kama, legend='KAMA', ax=axx[0])

  df['stoch0'] = stoch[0]
  df['stoch1'] = stoch[1]
  fplt.plot(df.stoch0, legend='stoch0', ax=axx[2])
  fplt.plot(df.stoch1, legend='stoch1', ax=axx[2])
  fplt.autoviewrestore()
  fplt.show()
  j=1