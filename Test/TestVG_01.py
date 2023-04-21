
import finplot as fplt
import pandas as pd
import ViewGraph01 as vg
from Db_form_data import Db_form_data
from Indicator_01 import indicator01
from IndicatorsBasa import IndicatorsBasa
import talib


if __name__ == '__main__':
  df = Db_form_data() # timeframe='1min'
  # df, _config = indicator01(df)
  # _test_vg = vg.VG01(df, config = _config)
  # # _test_vg = vg.VG01(df)
  # _test_vg.run()

  _indi = IndicatorsBasa(df, config_plot =  {"point": 300, "color": 0, "name": "--- SBRF ---"})
  # _cx = _indi.get(['close'], 1)['close']
  _cx = df['close'].to_numpy()
  d, _ax = {}, 0
  d["kama"] = {"d": talib.KAMA(_cx, timeperiod=25), 'ax': _ax}
  _ax=+1

  # d["volume"]={"d":None, 'ax':_ax}
  # _ax=+1

  d["rsi"] = {"d": talib.RSI(_cx, timeperiod=25), 'ax': _ax}

  _indi.add_indicator(d)

  _test_vg = vg.VG01(_indi.df, config = _indi.cplot)
  _test_vg.run()
  k1=1


  # dan0 =_indi.get(['open', 'low', 'kama'])
  # dan1 =_indi.get(['open', 'low', 'close'], 1)
  k1=1