import sys
from datetime import datetime, timedelta
from PSQLCommand import *

import re
import numpy as np
import copy
import threading
import LoadSavePickle
from Ticker import Ticker


class NormVSAP(threading.Thread, Ticker, LoadSavePickle.LoadSavePickle):  # , TDateTimeNew
  def __init__(self, *args, **kwargs):
    threading.Thread.__init__(self)
    Ticker.__init__(self, *args)
    LoadSavePickle.LoadSavePickle.__init__(self, *args, **kwargs)
    self.norm_cof = {}
    self.norm = {}
    self._d_candels = None
    if args.__len__() == 0:
      return

    self.__args = args

    # ===   Инициализируем коэффициеты  ===
    self.timeframe = args[0].get('timeframe', None)

    if self.timeframe is None:
      sys.exit(-2)
    print(f"-- normVSA --  {self.timeframe}")

  def calc_coefficient(self):
    self._id_timeframe = None
    self._dtWeekId = None

    self._pref_kof0, self._pref_kof1, self._pref_norm = None, None, None

    self._dt0_begin_test, self._dt1_end_test = \
        self.__args[0].get('dt0', self.__getattribute__('dtmin')), \
        self.__args[0].get('dt1', self.__getattribute__('dtmax'))


    self._dt0 = copy.deepcopy(self._dt0_begin_test)
    self._dt1 = copy.deepcopy(self._dt1_end_test)

    _dt0file = str(self._dt0.date())
    _dt1file = str(self._dt1.date())

    self._dt0_begin_test = self._dt0_begin_test - timedelta(days=30)
    self._dt0_begin_test = max(self.__getattribute__('dtmin'), self._dt0_begin_test)

    self._dt1_end_test = self._dt1_end_test + timedelta(days=8)

    self._dt1_end_test = min(self.__getattribute__('dtmax'), self._dt1_end_test)
    self.get_week()

    self.dtweeks_start, self.dtweeks_end = self.find_dt_start_end(self._dt0, self._dt1)
    self._candels = ['open', 'high', 'low', 'close', 'volume']
    # 1 - c индексом как db
    _db_all = self.get_dan(self.get_ohlcv(self._candels, dt0=self.dtweeks_start, dt1=self.dtweeks_end), 1)
    kwargs = {}
    kwargs['session'] = [0]
    self._calc_coef(**kwargs)
    kwargs['session'] = [1]
    self._calc_coef(**kwargs)

    _skey = "norm_cof.pkl"
    _path = [self.name_tick, self.timeframe, 'Normalization', _dt0file, _dt1file, _skey]
    self.norm_cof['path'] = _path
    self.norm_cof['dt0'] = self._dt0
    self.norm_cof['dt1'] = self._dt1
    self.norm_cof['prefid'] = self.__getattribute__('prefid')
    self.norm_cof['ticker'] = self.name_tick

    self.save_pickle(self.norm_cof)

  def loads(self, path):
    # zzz = self.load_pickle(path)
    self.__setattr__('norm_cof' if path.find('norm_cof') > 0 else 'norm', self.load_pickle(path))

  def run(self):
    i = 1

  def get_week(self):
    _dt_n = self._tdt._dbname
    _send = f"select DISTINCT {_dt_n}.id, {_dt_n}.datetime  " \
            f"from {_dt_n} " \
            f"where {_dt_n}.session = 100  and {_dt_n}.datetime >= '{self._dt0_begin_test}' and {_dt_n}.datetime <= '{self._dt1_end_test}' " \
            f"ORDER BY {_dt_n}.datetime"

    _dan = self.fcommand_fetchall(_send)
    self.knorm = {"id": [x[0] for x in _dan], "date": [x[1] for x in _dan], "koef": [{} for _ in _dan]}
    self.knorm["daten"] = np.array(self.knorm["date"])

  def find_dt_start_end(self, dt0, dt1):
    try:
      _x = np.max(self.knorm["daten"][self.knorm["daten"] < dt0])
    except:
      _x = np.min(self.knorm["daten"])

    iddtweeks = self.knorm["date"].index(_x)
    iddtweeks = iddtweeks if iddtweeks == 0 else iddtweeks - 1
    x0 = self.knorm["daten"][iddtweeks]
    try:
      x1 = np.min(self.knorm["daten"][self.knorm["daten"] > dt1])
    except:
      x1 = np.max(self.knorm["daten"][self.knorm["daten"] < dt1])
    return x0, x1

  def find_dt_min(self, _dtx: datetime):
    try:
      _x0 = max([x for x in self.norm_cof['dt'] if x < _dtx])
    except:
      _x0 = min( self.norm_cof['dt'])
    return _x0

  def finds_dt(self, lsdt):
    _dtls = []
    for it in lsdt:
      _dtls += [np.min(self.knorm["daten"][self.knorm["daten"] > it])]
    return _dtls

  def _calc_coef(self, *args, **kwargs):
    session = kwargs.get('session', [0])
    _id_session = session[0] if session.__len__() > 0 else 0
    _sid_session = str(_id_session)
    timeframe_end = kwargs.get('timeframe_end', "1W")  # По умолчанию 1 неделя

    _dan0 = self.read_db_pandas(dt0=self.dtweeks_start, dt1=self.dtweeks_end, session=session)

    _d = re.match(r'\d*', self.timeframe).group(0)
    _pref_kof = _d + self.timeframe[len(_d)] + "Nk" + str(_id_session)

    _dan0.index = pd.to_datetime(_dan0.datetime)

    _dan0['oc'] = abs(_dan0['close'] - _dan0['open'])
    _dan0['hl'] = abs(_dan0['high'] - _dan0['low'])
    _dan0['th'] = _dan0.high - _dan0[["open", "close"]].max(axis=1)
    _dan0['tl'] = _dan0[["open", "close"]].min(axis=1) - _dan0.low
    _dan0['doc'] = _dan0['oc']
    _dan0['dhl'] = _dan0['hl']
    _dan0['dth'] = _dan0['th']
    _dan0['dtl'] = _dan0['tl']
    _dan0['dvol'] = _dan0['volume']

    _dan1 = _dan0.resample(timeframe_end).agg({
      'datetime': 'last',
      'oc': 'max', 'hl': 'max', 'th': 'max', 'tl': 'max', 'volume': 'max',
      'doc': 'std', 'dhl': 'std', 'dth': 'std', 'dtl': 'std', 'dvol': 'std'})  #

    _z = _dan1.to_dict()
    _lskey = list(_z.keys())
    _lskey.remove('datetime')
    self.norm_cof['dt' + _sid_session] = [key for key, val in _z[_lskey[0]].items()]
    for it in _lskey:
      print(it)
      #      self.norm_cof[it + _sid_session] = [val for key, val in _z[it].items()]
      self.norm_cof[it + _sid_session] = _z[it]
    jjjj=1

  def Calc_ohlcv(self, *args, **kwargs):
    print(f"   Нормируем данные по времени {self.timeframe} ")
    self.repeat_dan(self.timeframe, self.SaveNormal)

  def SaveNormal(self):
    _dt0 = self.norm_cof['dt0']
    _dt1 = self.norm_cof['dt1']
    _prefid = self.norm_cof['prefid']
    _name_ticker = self.norm_cof['ticker']
    _dan = self.read_db_pandas(dt0=_dt0, dt1=_dt1, id_pref=_prefid, session=[])
    _ddan0 = _dan.to_dict()
    _dtls = list(_ddan0['datetime'].values())

    # dtKx =  self.find_dt_min(_dtls[0])
    # xx = self.norm_cof['oc0'][dtKx]

    _dan['oc'] = _dan['close'] - _dan['open']
    _dan['hl'] = _dan['high'] - _dan['low']
    _dan['th'] = _dan.high - _dan[["open", "close"]].max(axis=1)
    _dan['tl'] = _dan[["open", "close"]].min(axis=1) - _dan.low
    #        _dan[_dan['hl'] == 0] = 0.01
    _dan['spr_p'] = (_dan['close'] - _dan['low']) / _dan['hl']
    _dan['spr_m'] = (_dan['close'] - _dan['high']) / _dan['hl']

    _dan['spr_p'] = round(_dan['spr_p'], 1)
    _dan['spr_m'] = round(_dan['spr_m'], 1)

    _dan = _dan.fillna(0.0)
    data_tek = datetime(2000, 1, 1).date()
    self.koef0, self.koef1 = {}, {}

    _sourse = {}
    for row in _dan.itertuples():
      if data_tek != row.datetime.date():
        data_tek = row.datetime.date()
        dtKx = self.find_dt_min(row.datetime)
        print(row)

      d = {}
      sk = str(0 if row.datetime.hour < 19 else 1)
      # spread - положительный/отрицательный
      d['spred' + sk] = row.spr_p if row.oc > 0 else row.spr_m

      # нормируем oc
      d['oc' + sk] = round(min(row.oc / self.norm_cof["oc" + sk][dtKx], 1), 1)

      # нормируем hl
      d['hl' + sk] = round(min(row.hl / self.norm_cof["hl" + sk][dtKx], 1), 1)

      # нормируем th
      d['th' + sk] = round(min(row.th / self.norm_cof["th" + sk][dtKx], 1), 1)

      # нормируем tl
      d['tl' + sk] = round(min(row.tl / self.norm_cof["tl" + sk][dtKx], 1), 1)

      # нормируем volume
      d['volume' + sk] = round(min(row.volume / (self.norm_cof["volume" + sk][dtKx] * 1), 1), 1)

      _sourse[row.datetime] = d
    print(" запускаем программу обновления записи")

    _skey = "norm.pkl"
    _path = [_name_ticker, self.timeframe, 'Normalization', str(_dt0.date()), str(_dt1.date()), _skey]
    self.norm['path'] = _path
    self.norm['dt0'] = _dt0
    self.norm['dt1'] = _dt1
    self.norm['norm'] = _sourse

    self.save_pickle(self.norm)


'''

  def _calc_coef(self, *args, **kwargs):
    k = 1
    nametime = self.timeframe            kwargs.get('nametime', "5min")
    self.id_pref = self._tpref.get_index(nametime)
    session = kwargs.get('session', [0])
    _id_session = session[0] if session.__len__() > 0 else 0

    timeframe_end = kwargs.get('timeframe_end', "1W")
    dt0, dt1 = self.db_min_max(self.id_pref)

    _dan0 = self.read_db_pandas(dt0=dt0, dt1=dt1, session=session)

    _d = re.match(r'\d*', nametime).group(0)
    _pref_kof = _d + nametime[len(_d)] + "Nk" + str(_id_session)

    pref_id_koef = self._tpref.insert(_pref_kof)

    _dan0.index = pd.to_datetime(_dan0.datetime)

    _dan0['oc'] = abs(_dan0['close'] - _dan0['open'])
    _dan0['hl'] = abs(_dan0['high'] - _dan0['low'])
    _dan0['th'] = _dan0.high - _dan0[["open", "close"]].max(axis=1)
    _dan0['tl'] = _dan0[["open", "close"]].min(axis=1) - _dan0.low
    _dan0['doc'] = _dan0['oc']
    _dan0['dhl'] = _dan0['hl']
    _dan0['dth'] = _dan0['th']
    _dan0['dtl'] = _dan0['tl']
    _dan0['dvol'] = _dan0['volume']

    _dan1 = _dan0.resample(timeframe_end).agg({
      'datetime': 'last',
      'oc': 'max', 'hl': 'max', 'th': 'max', 'tl': 'max', 'volume': 'max',
      'doc': 'std', 'dhl': 'std', 'dth': 'std', 'dtl': 'std', 'dvol': 'std'})  #

    _dtls = _dan1['datetime'].tolist()
    _dtls0 = self.finds_dt(_dtls)

    self._tdt.insert(_dtls0)
    _id_dt = self._tdt.get(_dtls0)

    _sourse = {}
    i = 0
    print("  формируем данные для записи")
    for i1, row in _dan1.iterrows():  # print(f"Index: {i}")  print(f"{row}\n")
      xx = row.to_dict()
      _sourse[i] = dict(pref_id=pref_id_koef,
                        tdt_id=_id_dt[_dtls0[i]],
                        nork=[xx['oc'], xx['hl'], xx['th'], xx['tl'], xx['volume'],
                              xx['doc'], xx['dhl'], xx['dth'], xx['dtl'], xx['dvol']])
      i += 1
    print(f"  пишем в  {self.name_tick} запись")
    #        self.insert_dan_norm_kof(_sourse)
    self.insert_dan_new(self.name_tick, _sourse)




  # def find_dt_max(self, _dtx: datetime):
  #   return np.min(self.knorm["daten"][self.knorm["daten"] > _dtx])

  # def find_dt_min(self, _dtx: datetime):
  #   return np.max(self.knorm["daten"][self.knorm["daten"] < _dtx])

    k=1
    # dt = [x.date() for x in _db_all['datetime']]
    # try:
    #   istart = dt.index(self._dt0.date())
    # except:
    #   istart = 0
    # istart = max((istart - self._nfft), 0)
    #
    # _dt1end = max([x for x in _db_all['datetime'] if x.date() == self._dt1.date()])
    # iend = _db_all['datetime'].index(_dt1end)
    #
    # _ls = _db_all.keys()
    # for item in _ls:
    #   _d = _db_all[item][istart:iend + 1]
    #   self._dan[item] = _d

    # kwargs['timeframe'] = self.timeframe
    # TDateTimeNew.__init__(self, *args, **kwargs, id = self._dan['id'], datetime=self._dan['datetime'])


  #
  # def get_week(self, snork=""):
  #   _nt = self.name_tick
  #   _dt_n = self._tdt._dbname
  #   fun = lambda id_pref: f"select DISTINCT tdt.datetime, {_nt}.nork  from {_dt_n}, {_nt} " \
  #                         f"where {_nt}.Pref_Id={id_pref} " \
  #                         f" and {_nt}.tdt_id={_dt_n}.id " \
  #                         f" and {_dt_n}.session = 100  " \
  #                         f"ORDER BY {_dt_n}.datetime"
  #
  #   if snork == "":
  #     _dan = {z[0]: z[1] for z in
  #             self.fcommand_fetchall(f"select datetime, id  from {self._tdt._dbname} where session=100;")}
  #     return _dan, list(_dan.keys())
  #
  #   return {z[0]: z[1] for z in self.fcommand_fetchall(fun(self._pref_id_kof0))}, \
  #          {z[0]: z[1] for z in self.fcommand_fetchall(fun(self._pref_id_kof1))}
 
'''
