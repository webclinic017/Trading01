from IndicatorsBasa import IndicatorsBasa
from ViewGraph01 import VG01


class VG02(IndicatorsBasa, VG01):
  def __init__(self, *args, **kwds):
    print("  ____ class VG02 ---> View Graph ____ ")
    IndicatorsBasa.__init__(self, args, kwds)
    _indi.df, config = _indi.cplot
    if args.__len__()==0:
      raise Exception(' Нет данных для обработки ')
