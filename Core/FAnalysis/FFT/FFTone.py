import numpy as np
import copy
import json

from torch import tensor, fft

import threading

from sklearn import preprocessing
from ElementPostgres import ElementPostgres
import re

'''
Входные данные: 
- name_ticker  -> sbrf
-  
'''


class FFTone(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self._d_candels = None
        if args.__len__() == 0:
            return
        #        self._fftdb = ElementPostgres(*args, **kwargs)
        self._fftdb = ElementPostgres(*args, 'fft', 'json')

        _nametime = args[0].get('nametime', None)
        if _nametime is None:
            return

        self._candels = args[0].get('candels', ["close"])
        self._nfft = args[0].get('nfft', 32)
        self._ind_nfft = self._nfft // 2 + 1
        _d = re.match(r'\d*', _nametime).group(0)
        self._pref = _d + _nametime[len(_d)] + str(self._nfft)
        self.dan = {}
        self.__mbasa = None

    def run(self, **kwargs):
        self._dt0 = kwargs.get('dt0', self._fftdb._dt_begin)
        self._dt1 = kwargs.get('dt1', self._fftdb._dt_end)

        self._dan_fft = self._fftdb.get_field(**kwargs)
        _count_id = len(self._dan_fft['id'])
        _count_isnone = len({key: val for key, val in self._dan_fft['fft'].items() if val is None})
        _wqe = [(self._dan_fft['datetime'][key], val) for key, val in self._dan_fft['fft'].items() if val is None]
        if _count_isnone > 0:
            # пересчитать все значения поля fft
            self.calc_all_fft()
        self._dan_fft = self._fftdb.get_field(**kwargs)
        self.dan = {}
        _datetime = self._dan_fft['datetime']
        _fft = self._dan_fft['fft']

        for i in range(len(_fft)):
            self.dan[i] = {'dt': _datetime[i], 'fft': _fft[i]}

    def calc_all_fft(self):
        _m = None
        self._d_candels = self._fftdb.get_ohlcv(self._candels)

        _sourse = {}

        for _candel in self._candels:
            print(f" Обработка  -> {_candel} ")
            self.__candel = _candel
            _pref = self._pref + _candel
            _m = self.__calc_m_basa()

            _datetime = self._d_candels['datetime']
            _id_dt_end1 = [(key, val) for key, val in _datetime.items() if val >= self._dt1]
            if len(_id_dt_end1) == 0:
                self._id_dt_end = len(self._d_candels['datetime'])
            else:
                self._id_dt_end = _id_dt_end1[0][0]

            for i in range(self._id_start, self._id_dt_end + 1):
                try:
                    print(f" {_candel} - {i}  = {self._id_dt_end}   дата   {_datetime[i]} ")
                except:
                    break

                _m.pop(0)
                _m.append(self._d_candels[_candel][i])
                _fft = fft.rfft(tensor(_m))
                _a = _fft.abs()
                _f = _fft.angle()
                _d = np.degrees(_f)
                _x = np.array(_f).tolist()
                _x.append(np.pi)
                _x.append(-np.pi)
                norm = preprocessing.normalize([np.array(_x)])
                _norm = norm[0].tolist()
                _norm.pop(self._ind_nfft)
                _norm.pop(self._ind_nfft)
                #                __d = {'a':_a, 'f':_f, 'd':_d, 'n':_norm }
                __d = {'a': _a.tolist(), 'f': _f.tolist(), 'd': _d.tolist(), 'n': _norm}
                #                __d = {'a':_a.tolist()}
                try:
                    _xd = _sourse[self._d_candels['id'][i]]
                    _xd[_pref] = __d
                    _sourse[self._d_candels['id'][i]] = _xd
                except:
                    _sourse[self._d_candels['id'][i]] = {_pref: __d}

        _sourse_conv = [tuple([json.dumps(val), key]) for key, val in _sourse.items()]
        self._fftdb.fupdate_nor(_sourse_conv)

    def __calc_m_basa(self):
        _m = np.zeros(self._nfft).tolist()
        _datetime = self._d_candels['datetime']
        _dt_start = [(key, val) for key, val in _datetime.items() if val < self._dt0]
        self._id_start = len(_dt_start)
        if self._id_start == 0:
            pass
        elif self._id_start >= self._nfft:
            _m = [val for key, val in self._d_candels[self.__candel].items()
                  if key in [key[0] for key in _dt_start[-self._nfft:]]]
        else:
            _count = len(_dt_start)
            _m[-_count:] = [val for key, val in self._d_candels[self.__candel].items()
                            if key in [key[0] for key in _dt_start[-self._nfft:]]]
        self.__mbasa = copy.deepcopy(_m)
        return _m

    '''
        формат входных данных:
            dan {}  - id-[] - индекс в базе
                    - datetime-[]
                    - candles -[]
            npoint - кол-во точек БПФ        
        return
            rez {}  - id-[] - индекс в базе
                    - d{id(индех):{ Амплитуда, Фаза(радиан), Фаза(угол)} }                         
    '''

    ''' 
    
    def calc_fft(self, dan):
        _m = np.array([val for key, val in dan['ohl'].items()])
        m = np.zeros(self.npoint).tolist()
        _count = len(_m)
        for i in range(_count):
            m.pop(0)
            m.append(_m[i])
            _fft = fft.rfft(tensor(m))
            k = 1

        _mt = tensor(_m[:self.npoint])
        _fft = fft.rfft(_mt)
        print(_fft[0])
        print(_fft[1])
        print(_fft[3])

        phase0 = cmath.phase(_fft[0])
        phase1 = cmath.phase(_fft[1])
        phase2 = cmath.phase(_fft[2])
        print(f' {_fft[0]}  Phase =', phase0)
        print(f' {_fft[1]}  Phase =', phase1)
        print(f' {_fft[2]}  Phase =', phase2)

        print('Phase0 in Degrees0 =', numpy.degrees(phase0))
        print('Phase1 in Degrees0 =', numpy.degrees(phase1))
        print('Phase2 in Degrees0 =', numpy.degrees(phase2))

        print('-2 - 2j Phase =', cmath.phase(_fft[1]), 'radians. Degrees =', numpy.degrees(cmath.phase(_fft[1])))

        polar0 = cmath.polar(_fft[0])
        polar1 = cmath.polar(_fft[1])
        polar2 = cmath.polar(_fft[2])
        print(f' {_fft[0]}  polar =', polar0)
        print(f' {_fft[1]}  polar =', polar1)
        print(f' {_fft[2]}  polar =', polar2)

        _z = _fft.abs()
        _angle = _fft.angle()
        print(_fft.abs())
        print(np.degrees(_fft.angle()))
        print(_fft.angle())
        _x = np.array(_fft.angle()).tolist()
        _x.append(np.pi)
        _x.append(-np.pi)
        _x = np.array(_x)
        norm = preprocessing.normalize([_x])
        print(" ___ ", norm)
        xx = norm[0].tolist()
        i = self.npoint // 2 + 1
        xx.pop(i)
        xx.pop(i)
        print('--  ', xx)
    '''

    def __setitem__(self, name, value):
        self.__dict__[name] = value

    #        self.name =value

    def __getitem__(self, key):
        return self.__dict__[key]
#        return self.key
