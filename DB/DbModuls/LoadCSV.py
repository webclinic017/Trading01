import os
import pandas as pd

from datetime import datetime, time
from PSQLCommand import PSQLCommand
from Ticker import Ticker


# from TickerBasa import TickerBasa


class LoadCSV(PSQLCommand):
  def __init__(self, *args, **kwargs):
    if args.__len__() > 0:
      self._ticker: Ticker = args[0]
    else:
      self._ticker = None

  def ReadOneFile(self, path):
    print(f" Чтение файла и преобразование для Postgresql \n  {path}")
    _data = self._convert_to_postgre(self.readDb(path))
    # print("  Запись данных в базу  ")
    # self._ticker.Update(_data)
    # print("  Данные записанны в базу  ")
    return _data

  def readDb(self, _path: str) -> object:
    _tr0 = pd.read_csv(_path)
    print(f" Данные из файла прочитанны ")
    return {
      'date': _tr0["<DATE>"], 'time': _tr0["<TIME>"],
      'open': _tr0["<OPEN>"].values.astype(float), 'high': _tr0["<HIGH>"].values.astype(float),
      'low': _tr0["<LOW>"].values.astype(float), "close": _tr0["<CLOSE>"].values.astype(float),
      "volume": _tr0["<VOL>"].values.astype(float)
    }

  def _convert_to_postgre(self, _z: dict):
    print(f" Конвертирую ")
    j = len(_z['date'])
    #        _ls = []
    _sourse = dict()
    for i in range(j):
      _md, _h, _ms = _z['date'][i] % 10000, _z['time'][i] // 10000, _z['time'][i] % 10000
      d = {'datetime': datetime(_z['date'][i] // 10000, _md // 100, _md % 100, _h, _ms // 100)}
      d.update({'ohlcv': [_z['open'][i], _z['high'][i], _z['low'][i], _z['close'][i], _z['volume'][i]]})
      _sourse[i] = d

    print(f" Закончил конвертацию ")
    return _sourse  # _ls

  # def _convert_to_date_time(self, d0: int, d1: int):
  #     _md, _h, _ms = d0 % 10000, d1 // 10000, d1 % 10000
  #     return {'datetime': datetime(d0 // 10000, _md // 100, _md % 100, _h, _ms // 100)}

  def ReadAllFiles(self, pathdir: str):
    if not (os.path.isdir(pathdir)):
      return
    _lsdir = [pathdir+"\\" + x for x in os.listdir(path=pathdir)]
    _lsdir.sort()
    for item in _lsdir:
        _dancsv = self.ReadOneFile(item)
        self._ticker.write_db_ohlsv(_dancsv)
