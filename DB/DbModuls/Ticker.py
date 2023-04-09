from datetime import datetime, timedelta  # time
from PSQLCommand import PSQLCommand
import pandas as pd
from TPref import TPref
from TDateTime import TDateTime
import re


def dt_min_max(data):
  return min(data, key=lambda x: x['datetime'])['datetime'], max(data, key=lambda x: x['datetime'])['datetime']


class Ticker(PSQLCommand):
  # общий метод, который будут использовать все наследники этого класса
  def __init__(self, *args, **kwargs):
    PSQLCommand.__init__(self, *args, **kwargs)

    _tickerName = args[0].get("TickerName", None)

    if _tickerName is None:
      return

    _tickerName = str(_tickerName).lower()
    self.__set_attr({'TickerName': _tickerName})

    self._tpref = TPref(*args, **kwargs)
    self._tdt = TDateTime(*args, **kwargs)

    self._get_timeframe()

    if not (self.is_tabl(_tickerName)):
      send = f"CREATE TABLE {_tickerName}" \
             "(Id bigserial PRIMARY KEY, " \
             "Pref_Id INTEGER, " \
             "TDT_id  INTEGER, " \
             "FOREIGN KEY (Pref_Id) REFERENCES pref (Id) ON DELETE CASCADE, " \
             "FOREIGN KEY (TDT_id) REFERENCES TDT (Id) ON DELETE CASCADE,	" \
             "ohlcv real[]);"
      self.fcommand_execute(send)
      # id = self.__getattribute__('timeframeid')
      # db_min, db_max = self.db_min_max(id)
      self.__set_attr({"dtmin": datetime.now(), "dtmax": datetime.now()})
      return

    self.set_min_max_dt()

    self.dt0 = args[0].get('dt0', self.dtmin)
    self.dt1 = args[0].get('dt1', self.dtmax)

    self.TickerName_idx = f"{self.TickerName}_idx"

    if self.find_index_count(self.TickerName, self.TickerName_idx) == 0:
      self.create_index(f"{self.TickerName}  (Pref_Id, TDT_id)", self.TickerName_idx)
    else:
      self.reindex(self.TickerName_idx)

    kkk = 1

  def _get_timeframe(self):
    timeframeName = self._tpref.__getattribute__('timeframeName')
    timeframeid = self._tpref.__getattribute__('timeframeid')
    self.__set_attr({'timeframeName': timeframeName, 'timeframeid': timeframeid})

  def __set_attr(self, d0: dict):
    for key, val in d0.items():
      self.__setattr__(key, val)

  def set_min_max_dt(self):
    db_min, db_max = self.db_min_max()

    if db_min is None:
      self.__set_attr({"dtmin": datetime.now(), "dtmax": datetime.now()})
    else:
      self.__set_attr({"dtmin": db_min, "dtmax": db_max})

  def db_min_max(self, _id_pref=-1):
    if _id_pref <= 0:
      _id_pref = self.__getattribute__('timeframeid')

    _send = f"select min(tdt.datetime), max(tdt.datetime) " \
            f"from {self.TickerName}, tdt  " \
            f"where {self.TickerName}.Pref_Id={_id_pref} and {self.TickerName}.tdt_id=tdt.id"
    _dt = self.fcommand_fetchone(_send)
    return _dt[0], _dt[1]

  def __setattr__(self, key, value):
    self.__dict__[key] = value

  def __getitem__(self, key):
    return self.__dict__[key]

  def clear(self):
    self.clear_table(self.TickerName)

  def create_xtick(self):
    if self.is_tabl("xtick"):
      self.del_table("xtick")

    send = "CREATE TABLE xtick (DATETIME timestamp, ohlcv real[]);"
    self.fcommand_execute(send)

  def write_db_ohlsv(self, lsd: list):
    self.create_xtick()
    _dtls = [lsd[i]['datetime'] for i in range(lsd.__len__())]
    self._tdt.insert(_dtls)
    self.insert_dan_new('xtick', lsd)

    # self.id_pref = self._tpref.get_index(self.nametime)
    _send = f"select xtick.datetime, xtick.ohlcv from xtick where datetime NOT IN " \
            f"(select DISTINCT xtick.datetime from tdt, {self.TickerName}, xtick " \
            f"where {self.TickerName}.Pref_Id={self.timeframeid} " \
            f" and {self.TickerName}.tdt_id=tdt.id " \
            f" and tdt.datetime = xtick.datetime)"

    _dt_ohlcv = self.fcommand_fetchall(_send)

    if _dt_ohlcv is None:
      self.del_table("xtick")
      return

    _id_dt = self._tdt.get(_dtls)

    _sourse = dict()
    for i in range(_dt_ohlcv.__len__()):
      _sourse[i] = dict(pref_id=self.timeframeid, tdt_id=_id_dt[_dt_ohlcv[i][0]], ohlcv=_dt_ohlcv[i][1])

    self.insert_dan_new(self.TickerName, _sourse)
    self.del_table("xtick")

  def __convert_prefId(self, s):
    return s if "int" in str(type(s)) else self._tpref.get_index(s)

  def __convert_prefName(self, s):
    return s if "str" in str(type(s)) else self._tpref.get_name(s)

  def ConvertTimeToTime(self, timeframe0, timeframe1):

    self.repeat_dan_new(timeframe0=timeframe0,
                        timeframe1=timeframe1,
                        fun_loc=self.SaveNewTimeframe)
    kk = 1

  def repeat_dan_new(self, **kwargs):  # fun_loc, params=None,
    self._kwargs = kwargs
    #        _db_min, _db_max = self.db_min_max()
    _dt0 = kwargs.get('dt0', self.dtmin)
    _dt1 = kwargs.get('dt1', self.dtmax)

    _func = kwargs.get('fun_loc', None)

    for it in range(_dt0.year, _dt1.year):
      if it == _dt0.year:
        self._dt0_convert = datetime(it, _dt0.month, _dt0.day, 0, 0)
        self._dt1_convert = datetime(it, 12, 31, 23, 59)
      else:
        self._dt0_convert = datetime(it, 1, 1, 0, 0)
        self._dt1_convert = datetime(it, 12, 31, 23, 59)

      print(f" обрабатываем даты _dt0- {self._dt0_convert}   _dt1 {self._dt1_convert}")
      if _func is None:
        _func()
      else:
        _func()

    self._dt0_convert = max(datetime(_dt1.year, 1, 1, 0, 0), _dt0)
    self._dt1_convert = min(datetime(_dt1.year, _dt1.month, _dt1.day, 23, 59), _dt1)
    print(f" обрабатываем даты _dt0- {self._dt0_convert}   _dt1 {self._dt1_convert}")
    if _func is None:
      _func()
    else:
      _func()
    kkkk=1

  def SaveNewTimeframe(self):
    # self._kwargs
    timeframe0 = self._kwargs.get('timeframe0', None)
    timeframe1 = self._kwargs.get('timeframe1', None)

    if (timeframe1 is None) or (timeframe0 is None):
        return

    timeframe0 = self.__convert_prefId(timeframe0)
    timeframe1 = self.__convert_prefId(timeframe1)
    _dan = self.read_db_pandas(dt0=self._dt0_convert, dt1=self._dt1_convert, id_pref=timeframe0)
    _dan.index = pd.to_datetime(_dan.datetime)
    print(' --  запускаеи преобразование времени')
    _dan1 = _dan.resample(self.__convert_prefName(timeframe1)).agg({
      'datetime': 'first', 'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})

    if _dan1.__len__() <= 0:
      return

    _dan1.index.name = None
    _dan1 = _dan1.dropna()
    print(_dan1.tail(50))

    _dtls = [row.to_dict()['datetime'] for i, row in _dan1.iterrows()]

    self._tdt.insert(_dtls)
    _id_dt = self._tdt.get(_dtls)
    _sourse = {}
    i = 0
    print("  формируем данные для записи")
    for i1, row in _dan1.iterrows():  # print(f"Index: {i}")  print(f"{row}\n")
      xx = row.to_dict()
      _sourse[i] = dict(pref_id=timeframe1,
                        tdt_id=_id_dt[xx['datetime']],
                        ohlcv=[xx['open'], xx['high'], xx['low'], xx['close'], xx['volume']])
      i += 1
    print(f"  пишем в  {self.TickerName} запись")
    #        self.insert_dan(_sourse)
    self.insert_dan_new(self.TickerName, _sourse)
    self.set_min_max_dt()

  def read_db_pandas(self, *args, **kwargs):  # #self, dt0: datetime, dt1: datetime, id_nametime="", sid="", session=2):
    dbmin = kwargs.get('dt0', self.dtmin)
    dbmax = kwargs.get('dt1', self.dtmax)
    _id_pref = kwargs.get('id_pref', None)
    if _id_pref == None:
      return

    _nt = self.TickerName  # f" {self._tdt._dbname}.id,"
    _ntdt = self._tdt._dbname
    _send = f"select DISTINCT {_nt}.id, {_ntdt}.datetime,  " \
            f" {_nt}.ohlcv[1], {_nt}.ohlcv[2], {_nt}.ohlcv[3], {_nt}.ohlcv[4], {_nt}.ohlcv[5] from tdt, {_nt} " \
            f" where {_nt}.Pref_Id={_id_pref} " \
            f" and (tdt.datetime >= '{dbmin}' and tdt.datetime <= '{dbmax}')  " \
            f" and {_nt}.tdt_id=tdt.id ORDER BY tdt.datetime"
    return self.read_db_to_pandas(_send, ['id', 'datetime', 'open', 'high', 'low', 'close', 'volume'])

  def get_ohlcv(self, *args, **kwargs):
    print('  Грузим данные для обработеи !')

    ls = args[0]
#    self._dt_begin, self._dt_end = self.db_min_max(self.id_pref)

    # __dt0 = kwargs.get('dt0', self.dtmin)
    # __dt1 = kwargs.get('dt1', self.dtmax)

    _dan = self.read_db_pandas(dt0= self.dt0, dt1=self.dt1, id_pref=self.timeframeid)  #self.id_pref

    if 'ohl' in ls:
      _dan['ohl'] = (_dan['open'] + _dan['high'] + _dan['low']) / 3.0
    if 'hlc' in ls:
      _dan['hlc'] = (_dan['close'] + _dan['high'] + _dan['low']) / 3.0
    if 'ohlc' in ls:
      _dan['ohlc'] = (_dan['open'] + _dan['high'] + _dan['low'] + _dan['close']) / 4.0

    if not ('open' in ls):
      _dan.drop(columns=['open'], axis=1, inplace=True)
    if not ('high' in ls):
      _dan.drop(columns=['high'], axis=1, inplace=True)
    if not ('low' in ls):
      _dan.drop(columns=['low'], axis=1, inplace=True)
    if not ('close' in ls):
      _dan.drop(columns=['close'], axis=1, inplace=True)
    if not ('volume' in ls):
      _dan.drop(columns=['volume'], axis=1, inplace=True)

    return _dan.to_dict()

  def get_dan(self, dan: dict, t: int = 0):
    print(f"  Конверт данных {self.timeframeName} и вывод в формате  xx: LIST !")

    _ls_key = list(dan.keys())
    if t == 0:
      _ls_key.remove('id')
    _dan = {key: [] for key in _ls_key}

    for item_key in _ls_key:
      _dan[item_key] = [val for key, val in dan[item_key].items()]

    return _dan

  # -----------------------------------------------------------------------------------------------------------------
  # -----------------------------------------------------------------------------------------------------------------


  def repeat_dan(self, nametime, fun_loc, params=None):
    _db_min, _db_max = self.db_min_max(nametime)
    year0 = _db_min.year
    year1 = _db_max.year
    for it in range(year0, year1):
      if it == year0:
        self._dt_begin = datetime(it, _db_min.month, _db_min.day, 0, 0)
        self._dt_end = datetime(it, 12, 31, 23, 59)
      else:
        self._dt_begin = datetime(it, 1, 1, 0, 0)
        self._dt_end = datetime(it, 12, 31, 23, 59)
      print(f" обрабатываем даты _dt_begin- {self._dt_begin}   _dt_end {self._dt_end}")
      if params == None:
        fun_loc()
      else:
        fun_loc(params)
    #            self.SaveNewTimeframe(timeframe1)
    self._dt_begin = datetime(year1, 1, 1, 0, 0)
    self._dt_end = datetime(_db_max.year, _db_max.month, _db_max.day, 23, 59)
    print(f" обрабатываем даты  _dt_begin- {self._dt_begin}   _dt_end {self._dt_end}")
    if params == None:
      fun_loc()
    else:
      fun_loc(params)
    #        self.SaveNewTimeframe(timeframe1)

