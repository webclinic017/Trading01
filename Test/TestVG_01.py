
import finplot as fplt
import pandas as pd
import ViewGraph01 as vg
from Db_form_data import Db_form_data
from Indicstor_01 import indicator01

if __name__ == '__main__':
  df = Db_form_data() # timeframe='1min'
  df, _config = indicator01(df)
  _test_vg = vg.VG01(df, config = _config)
  # _test_vg = vg.VG01(df)
  _test_vg.run()
  k1=1