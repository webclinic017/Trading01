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
    __params = self.cplot.pop('params', None)

    if __config == None:
      ax = fplt.create_plot(' -- not name -- ', rows = _count_ax, init_zoom_periods = 300)
    else:
      __name =   __config.get('name', ' -- not name -- ')
      __point =  __config.get('point', 300)
      ax = fplt.create_plot(__name, rows = _count_ax, init_zoom_periods = __point)

    _count_x = 0
    for key, val in self.cplot.items():
      _ls_val = list(val.keys())
      for it in _ls_val:
        if 'candle' in it:
          self.df[['open', 'close', 'high', 'low']].plot(ax=ax[key], kind='candle')
          _count_x = len(self.df['close']) - 1
          continue

        if 'volume' in it:
          self.df[['open', 'close', 'volume']].plot(ax=ax[key], kind='volume')
          continue


        fplt.plot(self.df[it], legend=it, color='#000000', width=1, ax=ax[key])   #6335
        if len(val[it])<=0:
          continue
        else:
          __params = val[it]
          __level = __params.get('level', None)
          __band = __params.get('band', None)
          if not(__level is None):
            # fplt.add_band(-5, 0, color='#6335', ax=ax[key])
            for _it_level in __level:
              fplt.add_line((0, _it_level), (_count_x, _it_level), color='#205536', ax=ax[key])

          if not(__band is None):
            fplt.add_band(__band[0], __band[1],  ax=ax[key])  # color='#6335',


        kkkk=1
        # fplt.plot(self.df[it], legend=it, ax=key)

    fplt.autoviewrestore()
    fplt.show()
    kkkk=1