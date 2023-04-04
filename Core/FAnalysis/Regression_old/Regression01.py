import numpy as np

from LoadSavePickle import LoadSavePickle
from Ticker import Ticker
from TDateTimeNew import TDateTimeNew


class Regression01(Ticker, TDateTimeNew, LoadSavePickle):
    kX = {}

    def __init__(self, *args, **kwargs):
        if args.__len__() == 0:
            return

        Ticker.__init__(self, *args)
        LoadSavePickle.__init__(self, *args, **kwargs)
        print('  === Грузим данные ===')
        #        self._connect_db = args[0]
        self._candels = args[0].get('candels', ['close'])
        self._max_point = args[0].get('npoint', 200)
        self._npoint = self._max_point
        self.m = np.zeros(self._max_point)
        self._dt0, self._dt1 = args[0].get('dt0', self._dt_begin), args[0].get('dt1', self._dt_end)
        self._dan = self.get_dan(self.get_ohlcv(self._candels, dt0=self._dt0, dt1=self._dt1),
                                 1)  # 1 - c индексом как db

        self.timeframe = kwargs.get('timeframe', "x")
        self.id = kwargs.get('id', [])
        self.datetime = kwargs.get('datetime', [])
        kwargs['timeframe'] = self.nametime

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
        rez = {}
        for item in self._candels:
            print('------ {} ---'.format(item))
            _candels = self._dan[item]
            d = {"betta": 0, "alfa": 0, "ugol": 0, "koef_cor": 0, "sse": 0}
            _ls0 = [d for _ in range(self._npoint)]
            _count = len(_candels)
            _pro = _count // 100

            for i in range(self._npoint, _count):
                _ls0.append(self.Calc({'y': _candels[i - self._npoint:i]}))
                if (i % _pro) != 0:
                    pass
                elif (i % 5) == 0:
                    print(f" {item}   выполнено {i // _pro}%")

            _s = f"{str(self._npoint)}{item}"

            rez['ugol' + _s] = [x["ugol"] for x in _ls0]
            rez['koef_cor' + _s] = [x["koef_cor"] for x in _ls0]
            rez['sse' + _s] = [x["sse"] for x in _ls0]

        # формирую путь  ТИКЕР  (sbrf)  ls[0] //  Тime  (1min) ls[1] // Kalman  ls[2] //
        #  dt0_dt1 (ls[3]) + "_" + str(ls[4]) //  название файла ls[5]
        # _path = _path + "\\" + ls[5]+".pkl"
        __keyset = list(
            set([x.replace('ugol', '').replace('koef_cor', '').replace('sse', '') for x in list(rez.keys())]))
        __keyset.sort()
        _skey = '_'.join([x for x in __keyset]) + ".pkl"
        _path = [self.name_tick, self.nametime, 'Regression', self._dt0.date(), self._dt1.date(), _skey]
        rez['path'] = _path
        # rez['id'] = self._dan['id']
        # rez['ditetime'] = self._dan['datetime']
        self.save_pickle(rez)
        return rez


'''
от 30 марта 2022 11:30

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
        rez = {}
        for item in self._candels:
            print('------ {} ---'.format(item))
            _candels = self._dan[item]
            d = {"betta": 0, "alfa": 0, "ugol": 0, "koef_cor": 0, "sse": 0}
            _ls0 = [d for _ in range(self._npoint)]
            _count = len(_candels)
            _pro = _count // 100
            for i in range(self._npoint, _count):
                _ls0.append(self.Calc({'y': _candels[i - self._npoint:i]}))
                if (i % _pro) != 0:
                    pass
                elif (i % 5) == 0:
                    print(f" {item}   выполнено {i // _pro}%")

            _s = f"{str(self._npoint)}{item}"

            rez['ugol' + _s] = [x["ugol"] for x in _ls0]
            rez['koef_cor' + _s] = [x["koef_cor"] for x in _ls0]
            rez['sse' + _s] = [x["sse"] for x in _ls0]
          
        # формирую путь  ТИКЕР  (sbrf)  ls[0] //  Тime  (1min) ls[1] // Kalman  ls[2] //
        #  dt0_dt1 (ls[3]) + "_" + str(ls[4]) //  название файла ls[5]
        # _path = _path + "\\" + ls[5]+".pkl"
        __keyset = list(
            set([x.replace('ugol', '').replace('koef_cor', '').replace('sse', '') for x in list(rez.keys())]))
        __keyset.sort()
        _skey = '_'.join([x for x in __keyset]) + ".pkl"
        _path = [self.name_tick, self.nametime, 'Regression', self._dt0.date(), self._dt1.date(), _skey]
        rez['path'] = _path
        # rez['id'] = self._dan['id']
        # rez['ditetime'] = self._dan['datetime']
        self.save_pickle(rez)
        return rez




*****************************************************************************************************
    def CalcAll(self, *args, **kwargs):
        rez = {}
        for item in self._candels:
            print('------ {} ---'.format(item))
            _candels = self._dan[item]
            d = {"betta": 0, "alfa": 0, "ugol": 0, "koef_cor": 0, "sse": 0}
            _ls0 = [d for _ in range(self._npoint)]
            _count = len(_candels)
            _pro = _count // 100
            for i in range(self._npoint, _count):
                _ls0.append(self.Calc({'y': _candels[i - self._npoint:i]}))
                if (i % _pro) != 0:
                    pass
                elif (i % 5) == 0:
                    print(f" {item}   выполнено {i // _pro}%")

            _s = f"{str(self._npoint)}{item}"

            rez['ugol' + _s] = [x["ugol"] for x in _ls0]
            rez['koef_cor' + _s] = [x["koef_cor"] for x in _ls0]
            rez['sse' + _s] = [x["sse"] for x in _ls0]
        # формирую путь  ТИКЕР  (sbrf)  ls[0] //  Тime  (1min) ls[1] // Kalman  ls[2] //
        #  dt0_dt1 (ls[3]) + "_" + str(ls[4]) //  название файла ls[5]
        # _path = _path + "\\" + ls[5]+".pkl"
        __keyset = list(
            set([x.replace('ugol', '').replace('koef_cor', '').replace('sse', '') for x in list(rez.keys())]))
        __keyset.sort()
        _skey = '_'.join([x for x in __keyset]) + ".pkl"
        _path = [self.name_tick, self.nametime, 'Regression', self._dt0.date(), self._dt1.date(), _skey]
        rez['path'] = _path
        # rez['id'] = self._dan['id']
        # rez['ditetime'] = self._dan['datetime']
        self.save_pickle(rez)
        return rez




    #
    # def test(self, ddd):
    #     print(Regression.sss)
    #     Regression.sss = ddd

    def CalcStep(self, n, y):
        # self.m[:-1] = self.m[-1:]
        # self.m[self._max_point-1] = y

        self.m[:self._max_point - 1] = self.m[1:self._max_point]
        self.m[self._max_point - 1] = y

        fkw = lambda x0: list(map(lambda z: z * z, x0))
        _x = np.arange(n)
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

        _y = self.m[self._max_point - n:]
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

        _y1 = __y[n - 1]
        return {"betta": betta, "alfa": alfa, "ugol": _ugol, "koef_cor": __koef_cor, "sse": sse, "y": _y1}

    # def add(self, *args):
    #     if args.__len__() < 2:
    #         return
    #     self.name_candels = args[0]
    #     self.dan[(self.name_candels, self.count_std)] = args[2]
 
'''
