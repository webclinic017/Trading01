import finplot as fplt
import pandas as pd
import talib


def indicator01(df: pd, *args, **kwds):
  _candle = df.columns.values.tolist()
  if ('open' in _candle) & ('close' in _candle) & ('high' in _candle) & ('low' in _candle) & ('volume' in _candle):
    pass
  else:
    raise Exception(' Нет данных по свечам и объему ')

  _pkeys = {}
  _pkeys['config'] = {"point": 300, "color": 0}
  _pkeys[0] = {"candle": 0, "kama": 0, "sma": 0}
  df['sma'] = talib.SMA(df.close, 10)

  df['kama'] = talib.KAMA(df.close, timeperiod=25)

  stoch = talib.STOCHRSI(df.close, 25, 10, 5, 0)
  df['stoch0'] = stoch[0]
  df['stoch1'] = stoch[1]
  _pkeys[1] = {'volume': 0}
  _pkeys[2] = {'stoch0': 0, 'stoch1': 0}

  return df, _pkeys
