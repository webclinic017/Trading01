from IndicatorsBasa import IndicatorsBasa
import finplot as fplt


class VG02(IndicatorsBasa):
  def __init__(self, *args, **kwds):
    print("  ____ class VG02 ---> View Graph ____ ")
    IndicatorsBasa.__init__(self, *args, **kwds)
    if args.__len__()==0:
      raise Exception(' Нет данных для обработки ')

    # if str(type(args[0])).find('pandas') >=0:
    if 'pandas'in str(type(args[0])):
        self.df = args[0]
    else:
      raise Exception(' Первый аргумент не pandas ')

    # self.cplot = kwds.get("config", None)

  def run(self):
    if self.cplot == None:
      fplt.candlestick_ochl(self.df[['open', 'close', 'high', 'low']])
      fplt.autoviewrestore()
      fplt.show()
      return
    __config =  self.cplot.get('config', None)
    _ = self.cplot.pop('config', None)
    _count_ax = len(self.cplot)

    if __config == None:
      ax = fplt.create_plot(' -- not name -- ', rows = _count_ax, init_zoom_periods = 300)
    else:
      __name =   __config.get('name', ' -- not name -- ')
      __point =  __config.get('point', 300)
      ax = fplt.create_plot(__name, rows = _count_ax, init_zoom_periods = __point)

    for key, val in self.cplot.items():
      _ls_val = list(val.keys())
      for it in _ls_val:
        if 'candle' in it:
          self.df[['open', 'close', 'high', 'low']].plot(ax=ax[key], kind='candle')
          continue

        if 'volume' in it:
          self.df[['open', 'close', 'volume']].plot(ax=ax[key], kind='volume')
          continue

        fplt.plot(self.df[it], legend=it, ax=ax[key])

    fplt.autoviewrestore()
    fplt.show()
