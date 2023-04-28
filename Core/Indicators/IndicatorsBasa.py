import pandas as pd
import talib


class IndicatorsBasa():
  def __init__(self, *args, **kwargs):
    print("  ____ class IndicatorsBasa --->  ____ ")
    if args.__len__() == 0:
      raise Exception(' Нет данных для обработки ')

    # if str(type(args[0])).find('pandas') >=0:
    if 'pandas' in str(type(args[0])):
      self.df = args[0]
    else:
      raise Exception(' Первый аргумент не pandas ')

    _candle = self.df.columns.values.tolist()
    if not (
        ('open' in _candle) & ('close' in _candle) & ('high' in _candle) & ('low' in _candle) & ('volume' in _candle)):
      raise Exception(' Нет данных по свечам и объему ')

    ''' Это база для свечей '''
    self.cplot = {}
    self.cplot['config'] = kwargs.get('config_plot', {})
    self.cplot[0] = {"candle": 0}

  def add_indicator(self, indicators: dict):
    if indicators.__len__() == 0:
      print("-- Нет индикатора --")
      return

    for key, val in indicators.items():
      if key == 'volume':
        pass
      else:
        self.df[key] = val['d']

      __dx = self.cplot[val['ax']] if val['ax'] in self.cplot else {}
      _ = val.pop('d')
      n = val.pop('ax')
      __params = {}

      if len(val) == 0:
        pass
      else:
        __params['params'] = val

      # __dx[key] = __params
      __dx[key] = val
      # __dx['params'] = val
      # __dx[key]= n #val['ax']
      # __dx['params'] = val
      # self.cplot[val['ax']]= __dx
      self.cplot[n] = __dx
      kkk = 1
    hhh=1



  def get(self, ls_indicator: list = [], typeour=0):  # pandas = 0, 1-dict
    if ls_indicator.__len__() == 0:
      return self.df

    ls = self.df.columns.values.tolist()
    result = list(set(ls_indicator) & set(ls))
    if typeour == 0:
      return self.df[result]

    d = {}
    for it in result:
      d[it] = self.df[it].to_numpy()
    return d
