import numpy as np
import copy
import os, sys
from LoadSavePickle import LoadSavePickle
from Ticker import Ticker
from TDateTimeNew import TDateTimeNew

from torch import tensor, fft
import threading
from sklearn import preprocessing


class FFTPone(threading.Thread, Ticker, TDateTimeNew, LoadSavePickle):

  def __init__(self, *args, **kwargs):
    threading.Thread.__init__(self)
    Ticker.__init__(self, *args)
    LoadSavePickle.__init__(self, *args, **kwargs)

    _z = sys.version_info
    self.__isNorm = True if (_z.major==3) and (_z.minor <10) else False

    self._d_candels = None
    if args.__len__() == 0:
      return

    if self.timeframeid is None:
      return

    self._candels = args[0].get('candels', ["close"])
    self._nfft = args[0].get('nfft', 32)
    self._ind_nfft = self._nfft // 2 + 1

    self._pref = str(self._nfft)
    self._dan = {}
    self.__mbasa = None
    self._dt0, self._dt1 = args[0].get('dt0', self.dtmin), args[0].get('dt1', self.dtmax)
    if (args.__len__() == 2) and (args[1] in 'read'):
      return

    self._dt0file, self._dt1file = copy.deepcopy(self._dt0.date()), copy.deepcopy(self._dt1.date())

    _db_all = self.get_dan(self.get_ohlcv(self._candels), 1)  # 1 - c индексом как db
    dt = [x.date() for x in _db_all['datetime']]
    try:
      istart = dt.index(self._dt0.date())
    except:
      istart = 0
    istart = max((istart - self._nfft), 0)

    _dt1end = max([x for x in _db_all['datetime'] if x.date() <= self.dt1.date()])
    iend = _db_all['datetime'].index(_dt1end)

    _ls = _db_all.keys()
    for item in _ls:
      _d = _db_all[item][istart:iend + 1]
      self._dan[item] = _d

    kwargs['timeframe'] = self.timeframeName
    TDateTimeNew.__init__(self, *args, **kwargs, id=self._dan['id'], datetime=self._dan['datetime'])
    kk=1

  def run(self):
    _m = None
    _sourse = {}

    for _candel in self._candels:
      print(f" Обработка  -> {_candel} ")
      self.__candel = _candel
      _pref = self._pref + _candel

      _m = np.zeros(self._nfft).tolist()

      self._id_start = self._dan['datetime'].index(
        min([x for x in self._dan['datetime'] if x.date() >= self.dt0.date()]))

      if self._id_start == 0:
        pass
      elif self._id_start >= self._nfft:
        _m = self._dan[self.__candel][0:self._id_start]
      else:
        _m[-self._id_start:] = self._dan[self.__candel][0:self._id_start]

      self._id_dt_end = len(self._dan['datetime']) + 1

      _dcalc = {}
      for i in range(self._id_start, self._id_dt_end + 1):
        __d =  {'a': 0, 'f': 0, 'd': 0, 'n': 0} if self.__isNorm else {'a': 0, 'f': 0, 'd': 0}
        try:
          print(f" {self.timeframe} =>  {_candel} - {i}  = {self._id_dt_end}   дата   {self._dan['datetime'][i]} ")
        except:
          break
        # _dtxxx = self.datetime[i]
        _m.pop(0)
        _m.append(self._dan[_candel][i])
        _fft = fft.rfft(tensor(_m))
        _a, _f = _fft.abs(), _fft.angle()
        _d, _x = np.degrees(_f), np.array(_f).tolist()
        if self.__isNorm:
          _x.append(np.pi)
          _x.append(-np.pi)
          norm = preprocessing.normalize([np.array(_x)])
          _norm = norm[0].tolist()
          _norm.pop(self._ind_nfft)
          _norm.pop(self._ind_nfft)
          __d['n'] = _norm

        __d['a'] = _a
        __d['f'] = _f
        __d['d'] = _d

        _dcalc[self.datetime[i]] = __d
      _sourse[_pref] = _dcalc
      __keyset = list(_sourse.keys())
      __keyset.sort()

      _skey = '_'.join([x for x in __keyset]) + ".pkl"
      _path = [self.TickerName, self.timeframeName, 'FFT', self._dt0file, self._dt1file, _skey]
      _sourse['path'] = _path
      # _sourse['id'] = self._dan['id']
      # _sourse['ditetime'] = self._dan['datetime']
      self.save_pickle(_sourse)
      _sourse = {}

    # __keyset = list(_sourse.keys())
    # __keyset.sort()
    #
    # _skey = '_'.join([x for x in __keyset]) + ".pkl"
    # _path = [self.name_tick, self.timeframe, 'FFT', self._dt0file, self._dt1file, _skey]
    # _sourse['path'] = _path
    # # _sourse['id'] = self._dan['id']
    # # _sourse['ditetime'] = self._dan['datetime']
    # self.save_pickle(_sourse)

  def loads(self, path):
    _name0 = os.path.basename(path).split('.')[0]
    z = self.load_pickle(path)
    self.__setattr__(_name0, z[_name0])


'''
***   Обратить внимание на формирование название:list =>  { Амплитуда:[.....]}
    def run(self):
        _m = None
        _sourse = {}

        for _candel in self._candels:
            print(f" Обработка  -> {_candel} ")
            self.__candel = _candel
            _pref = self._pref + _candel

            _m = np.zeros(self._nfft).tolist()

            self._id_start = self._dan['datetime'].index(
                                min([x for x in  self._dan['datetime'] if x.date() == self._dt0.date()]))
            if self._id_start == 0:
                pass
            elif self._id_start >= self._nfft:
                _m = self._dan[self.__candel][0:self._id_start]
            else:
                _m[-self._id_start:] = self._dan[self.__candel][0:self._id_start]

            self._id_dt_end = len( self._dan['datetime'])+1

            _dcalc ={}
            __d = {'a':[], 'f':[], 'd':[], 'n':[] }
            for i in range(self._id_start, self._id_dt_end + 1):
                try:
                    print(f" {self.timeframe} =>  {_candel} - {i}  = {self._id_dt_end}   дата   {self._dan['datetime'][i]} ")
                except:
                    break
                # _dtxxx = self.datetime[i]
                _m.pop(0)
                _m.append(self._dan[_candel][i])
                _fft = fft.rfft(tensor(_m))
                _a, _f = _fft.abs(), _fft.angle()
                _d, _x = np.degrees(_f), np.array(_f).tolist()
                _x.append(np.pi)
                _x.append(-np.pi)
                norm = preprocessing.normalize([np.array(_x)])
                _norm = norm[0].tolist()
                _norm.pop(self._ind_nfft)
                _norm.pop(self._ind_nfft)
                __d['a'] +=[_a]
                __d['f'] +=[_f]
                __d['d'] +=[_d]
                __d['n'] +=[_norm]
            _sourse[_pref] = __d

        __keyset = list(_sourse.keys())
        __keyset.sort()

        _skey = '_'.join([x for x in __keyset]) + ".pkl"
        _path = [self.name_tick, self.timeframe, 'FFT', self._dt0file, self._dt1file, _skey]
        _sourse['path'] = _path
        _sourse['id'] = self._dan['id']
        _sourse['ditetime'] = self._dan['datetime']
        self.save_pickle(_sourse)
 
'''
