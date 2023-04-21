
import finplot as fplt
import pandas as pd

class VG01:
  def __init__(self, *args, **kwds):
    print("  ____ class VG ---> View Graph ____ ")

    # if 'self.df' in locals():
    #   print('Variable exist.')
    # else:
    #   print('Variable don\'t exist.')

    if args.__len__()==0:
      raise Exception(' Нет данных для обработки ')

    # if str(type(args[0])).find('pandas') >=0:
    if 'pandas'in str(type(args[0])):
        self.df = args[0]
    else:
      raise Exception(' Первый аргумент не pandas ')

    self._config = kwds.get("config", None)


  def run(self):
    if self._config == None:
      fplt.candlestick_ochl(self.df[['open', 'close', 'high', 'low']])
      fplt.autoviewrestore()
      fplt.show()
      return
    __config =  self._config.get('config', None)
    _ = self._config.pop('config', None)
    _count_ax = len(self._config)

    if __config == None:
      ax = fplt.create_plot(' -- not name -- ', rows = _count_ax, init_zoom_periods = 300)
    else:
      __name =   __config.get('name', ' -- not name -- ')
      __point =  __config.get('point', 300)
      ax = fplt.create_plot(__name, rows = _count_ax, init_zoom_periods = __point)

    for key, val in self._config.items():
      _ls_val = list(val.keys())
      for it in _ls_val:
        if 'candle' in it:
          self.df[['open', 'close', 'high', 'low']].plot(ax=ax[key], kind='candle')
          continue

        if 'volume' in it:
          self.df[['open', 'close', 'volume']].plot(ax=ax[key], kind='volume')
          continue

        fplt.plot(self.df[it], legend=it, ax=ax[key])
        k=1
      k=1

    fplt.autoviewrestore()
    fplt.show()

'''

      # _pkeys['config'] = {"point": 300, "color": 0, "name": "--- SBRF ---"}
      # _pkeys[0] = {"candle": 0, "kama": 0, "sma": 0}
      # df['sma'] = talib.SMA(df.close, 10)
      #
      # df['kama'] = talib.KAMA(df.close, timeperiod=25)
      #
      # stoch = talib.STOCHRSI(df.close, 25, 10, 5, 0)
      # df['stoch0'] = stoch[0]
      # df['stoch1'] = stoch[1]
      # _pkeys[1] = {'volume': 0}
      # _pkeys[2] = {'stoch0': 0, 'stoch1': 0}
      #
      # return df, _pkeys
      #
      # pass


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


'''