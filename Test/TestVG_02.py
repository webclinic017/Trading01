
import finplot as fplt
import numpy as np
import pandas as pd
import ViewGraph01 as vg
from Db_form_data import Db_form_data
from Indicator_01 import indicator01
from IndicatorsBasa import IndicatorsBasa
import talib

from ViewGraph02 import VG02

if __name__ == '__main__':
  df = Db_form_data() # timeframe='1min'

  _indi = VG02(df, config_plot =  {"point": 300, "color": 0, "name": "--- SBRF ---"})
  _cx = df['close'].to_numpy()
  d, _ax = {}, 0
  _n_kama = 25
  _kama = talib.KAMA(_cx, timeperiod=_n_kama)
  d["kama"] = {"d": _kama, 'ax': _ax}
  _std = 2*talib.stream_STDDEV(_cx, timeperiod=_n_kama)
  _kama_p = _kama+_std
  _kama_m = _kama-_std
  d["kama_p"] = {"d": _kama_p, 'ax': _ax}
  d["kama_m"] = {"d": _kama_m, 'ax': _ax}
  _ax+=1

  _count=len(_kama)
  # _n_kama=5
  __array=np.zeros(_n_kama)
  _kama_moment = _kama- (np.concatenate([__array, _kama])[:_count])
  d["kama_moment"] = {"d": _kama_moment, 'ax': _ax, 'level':[0]}
  _ax+=1
  # fplt.set_y_range(0, 100, ax=ax)
  # fplt.add_band(30, 70, ax=ax)

  # d["volume"]={"d":None, 'ax':_ax}
  # _ax+=1

  d["rsi"] = {"d": talib.RSI(_cx, timeperiod=15), 'ax': _ax}

  _indi.add_indicator(d)

  # _test_vg = vg.VG01(_indi.df, config = _indi.cplot)
  # _test_vg.run()
  _indi.run()
  k1=1


  # dan0 =_indi.get(['open', 'low', 'kama'])
  # dan1 =_indi.get(['open', 'low', 'close'], 1)
  k1=1