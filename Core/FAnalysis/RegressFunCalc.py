
import numpy as np
from datetime import datetime, timedelta

from LoadSavePickle import LoadSavePickle
from Ticker import Ticker
import threading
import multiprocessing as mp


class OneCalcRegrres(threading.Thread, Ticker):
  def __init__(self, *args, **kwargs):
    threading.Thread.__init__(self)
    Ticker.__init__(self, *args)
    self.q = args[1]
    self._str00 = args[2]
    self._npoint = args[3]

  def run(self):
    self.q.put({self._npoint: str(self._str00)})



class RegressFunCalc(Ticker, LoadSavePickle):
  def __init__(self, *args, **kwargs):
    print(" ===  Class RegressFunCalc  ===  ")
    if args.__len__() == 0:
      return

    Ticker.__init__(self, *args)
    LoadSavePickle.__init__(self, *args, **kwargs)
    self._args = args
    self._kwargs = kwargs
    self.q = mp.Queue()


  def CalcOne(self, *args):
    print(f" timrframe - {args[0][0]} первый период - {args[0][1]} втлрой период - {args[0][2]}  ")
    self._args[0]['timeframe'] = "4H"
    self._args[0]['npoint'] = 4
    _oneCalcRegrres_01 = OneCalcRegrres(self._args[0], self. q, "test_01", 20)
    self._args[0]['timeframe'] = "4H"
    self._args[0]['npoint'] = 8

    _oneCalcRegrres_02 = OneCalcRegrres(self._args[0], self. q, "test_02", 40)
    _oneCalcRegrres_01.start()
    _oneCalcRegrres_02.start()
    _oneCalcRegrres_01.join()
    _oneCalcRegrres_02.join()
    print("ххххххххххххххххххх")
    import time
    time.sleep(0.5)
    while not self.q.empty():
        print(self.q.get())




  def CalcAll(self, *args):
    pass


'''


class RegressFun(Ticker, TDateTimeNew, LoadSavePickle):
    kX = {}

    def __init__(self, *args, **kwargs):
        if args.__len__() == 0:
            return
#'TickerName' 'timeframeName'

        Ticker.__init__(self, *args)
        LoadSavePickle.__init__(self, *args, **kwargs)
        print('  === Грузим данные ===')
        #        self._connect_db = args[0]
        self._candels = args[0].get('candels', ['close'])
        self._max_point = args[0].get('npoint', 200)
        self._npoint = self._max_point
        self.m = np.zeros(self._max_point)
        self._dt0, self._dt1 = args[0].get('dt0', self.__getattribute__('dtmin'))\
                            , args[0].get('dt1', self.__getattribute__('dtmax'))

        _dt0file = str(self._dt0.date())
        _dt1file = str(self._dt1.date())

        # self._dt0_begin_test = self._dt0 - timedelta(days=1)
        self._dt0_begin_test = self._dt0 - timedelta(days=30)
        self._dt0_begin_test = max(self.__getattribute__('dtmin'), self._dt0_begin_test)

        self._dan = {}
        _dan = self.get_dan(
            self.get_ohlcv(self._candels, dt0 = self._dt0_begin_test, dt1 = self._dt1),1)  # 1 - c индексом как db

        _index = np.max(np.min(np.where(np.array(_dan['datetime']) >= self._dt0))-self._npoint-1, 0)

        for key, val in _dan.items():
            self._dan[key]=val[_index:]

        self.timeframe = kwargs.get('timeframe', "x")
        self.id = kwargs.get('id', [])
        self.datetime = kwargs.get('datetime', [])
        kwargs['timeframe'] = self.timeframeName


        TDateTimeNew.__init__(self, *args, **kwargs, id=self._dan['id'], datetime=self._dan['datetime'])

    def Calc(self, dan):
        fkw = lambda x0: list(map(lambda z: z * z, x0))
        _y = dan.get('y', None)
        if _y is None:
            return
        _x = dan.get("x", np.arange(len(_y)))
        _xcount = len(_x)

        if not str(_xcount) in self.kX:
            xsum, x2sum = sum(_x), sum(fkw(_x))
            x_sr = xsum / _xcount
            x_0 = list(map(lambda _z: _z - x_sr, _x))
            x_01 = sum(list(map(lambda _z: _z * _z, x_0)))
            x_001 = 1 / x_01
            xsum2 = xsum * xsum
            _z0 = x2sum / xsum2
            _z01 = 1 / (1 - (_z0 * _xcount))
            _z002 = 1 / xsum
            self.kX = {str(_xcount):
                           {"xsum": xsum, 'x2sum': x2sum, "x_0": x_0, "x_001": x_001, "xsum2": xsum2,
                            "_z0": _z0, "_z01": _z01, "_z002": _z002}}

        ysum = sum(_y)
        y2sum = sum(fkw(_y))
        xy = list(map(lambda _x0, _y0: _x0 * _y0, _x, _y))
        xysum = sum(xy)
        y_sr = ysum / _xcount
        y_0 = list(map(lambda _z: _z - y_sr, _y))
        _su = sum(list(map(lambda _x0, _y0: _x0 * _y0, self.kX[str(_xcount)]["x_0"], y_0)))
        __b = _su * self.kX[str(_xcount)]["x_001"]
        _z1 = xysum * self.kX[str(_xcount)]["_z002"]
        betta = (_z1 - self.kX[str(_xcount)]["_z0"] * ysum) * self.kX[str(_xcount)]["_z01"]  # смещение по X
        alfa = (ysum - betta * _xcount) * self.kX[str(_xcount)]["_z002"]  # угол наклона
        _ugol = np.arctan(alfa) * 180 / np.pi  # угол наклона в градусах

        __y = list(map(lambda _q: alfa * _q + betta, _x))

        __z = np.array(list(map(lambda _y0, _y1: _y0 - _y1, _y, __y)))
        # Для оценки качества модели используется критерий суммы квадратов регрессионных остатков, SSE — Sum of Squared Errors.
        sse = np.dot(__z.transpose(), __z)

        # Найдем выборочный коэффициент корреляции: чем ближе к 1 тем лучше
        __koef_cor = (_xcount * xysum - self.kX[str(_xcount)]["xsum"] * ysum) / \
                     (np.sqrt(_xcount * self.kX[str(_xcount)]["x2sum"] - self.kX[str(_xcount)]["xsum2"]) * np.sqrt(
                         _xcount * y2sum - ysum * ysum))

        return {"betta": betta, "alfa": alfa, "ugol": _ugol, "koef_cor": __koef_cor, "sse": sse}

    def CalcAll(self, *args, **kwargs):
        for item in self._candels:
            _sourse = {}
            rez = {}

            print('------ {} ---'.format(item))
            _candels = self._dan[item]
            d = {"betta": 0, "alfa": 0, "ugol": 0, "koef_cor": 0, "sse": 0}
            _ls0 = [d for _ in range(self._npoint)]
            _count = len(_candels)
            _pro = _count // 100

            for i in range(self._npoint, _count):
                if self._dan['datetime'][i] < self._dt0:
                    continue

                _zz = self.Calc({'y': _candels[i - self._npoint:i]})
                _ls0.append(_zz)
                _sourse[self._dan['datetime'][i]] =_zz
                if (i % _pro) != 0:
                    pass
                elif (i % 5) == 0:
                    print(f" {item}   выполнено {i // _pro}%")

            _s = f"{str(self._npoint)}{item}"
            _skey = _s + ".pkl"
            _path = [self.TickerName, self.timeframeName, 'Regression', self._dt0.date(), self._dt1.date(), _skey]
            rez['path'] = _path
            rez[_s] = _sourse
            self.save_pickle(rez)

'''
