

import numpy as np
from torch import tensor, fft
import threading
from sklearn import preprocessing
from ElementPostgres import ElementPostgres

class FFTOneTimeInicial(threading.Thread, ElementPostgres):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        ElementPostgres.__init__(self, *args, 'fft', 'json', **kwargs)
        self._nffts = args[0].get('nfft', [32])
        self._ind_nfft = 1
        self.read_db_ohlcv()

    def run(self):
        for item_nfft in self._nffts:
            self._nfft = item_nfft          #repeat_dan_new(self,  fun_loc, params=None, **kwargs):
            self._ind_nfft=self._nfft//2+1
            params = {}  # params["func"]=  self.outer_function
            self.repeat_dan_new(self.calc_all_xxx, params=params, dt0=self._dt0, dt1=self._dt1)
        kk=1

    def outer_function(self, _m):
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
        return {'a':_a.tolist(), 'f':_f.tolist(), 'd':_d.tolist(), 'n':_norm}
#
