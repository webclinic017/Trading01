
import finplot as fplt
import pandas as pd

class VG01:
  def __init__(self, *args, **kwds):
    print("  ____ class VG ---> View Graph ____ ")
    if args.__len__()==0:
      raise Exception(' Нет данных для обработки ')

    # if str(type(args[0])).find('pandas') >=0:
    if 'pandas'in str(type(args[0])):
        self._df = args[0]
    else:
      raise Exception(' Первый аргумент не pandas ')

    self._config = kwds.get("config", None)

  def run(self):
    if self._config == None:
      fplt.candlestick_ochl(self._df[['open', 'close', 'high', 'low']])
      fplt.autoviewrestore()
      fplt.show()
      return
    else:
      pass