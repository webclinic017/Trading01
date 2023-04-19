# https://pypi.org/project/finplot/
# https://github.com/highfestiva/finplot
from datetime import datetime

import finplot as fplt
import pandas as pd
import numpy as np

from ConfigDbSing import ConfigDbSing
from Ticker import Ticker


# import yfinance

def form_data():
  _connect_db = ConfigDbSing().get_config()
  pref_comp = _connect_db["comp_pref"]
  _connect_db['timeframe'] = "4H"  # "1min" "4H"
  _connect_db['TickerName'] = "SBRF"

  if pref_comp == "E:\\":
    _connect_db['dt0'] = datetime(2007, 8, 1, 0, 0)
    _connect_db['dt1'] = datetime(2008, 12, 31, 0, 0)

  _ticker = Ticker(_connect_db)

  return _ticker.get_ohlcv(formatd=0) #  0 в формате datefrane --  по умолчанию 1 dict

  # volume

if __name__ == '__main__':
  df = form_data()  # df = yfinance.download('AAPL')
  fplt.candlestick_ochl(df[['open', 'close', 'high', 'low']])  # , 'volume'
  fplt.show()
  j=1