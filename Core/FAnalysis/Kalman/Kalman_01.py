from TDateTimeNew import TDateTimeNew
from LoadSavePickle import LoadSavePickle
import threading
import numpy as np
from ConfigDbSing import ConfigDbSing
import pickle
import os
from Ticker import Ticker


class Kalman_01(threading.Thread, Ticker, TDateTimeNew, LoadSavePickle):
    def __init__(self, *args, **kwargs):
        Ticker.__init__(self, *args)
        LoadSavePickle.__init__(self, *args, **kwargs)
        self.dan = dict()
        self.kdan = dict()
        self.name_candels = ""
        self.count_std = args[0].get('npoint', 12)
        self._kwargs = kwargs
        self._name_ticker = args[0].get('name', 'x')
        self._load_candels = ""
        self._candels = args[0].get('candels', None)
        self._dt0, self._dt1 = args[0].get('dt0', self.dtmin), args[0].get('dt1', self.dtmax)
        self._dan = self.get_dan(self.get_ohlcv(self._candels, dt0=self._dt0, dt1=self._dt1),
                                 1)  # 1 - c индексом как db
        # self.id = self._dan['id']
        # self.datetime = self._dan['datetime']
        kwargs['timeframe'] = self.timeframeName
        TDateTimeNew.__init__(self, *args, **kwargs)

    def calc(self, *args):
        if args.__len__() == 2:
            self.name_candels = args[0]
            self.count_std = args[1]
            self.dan[(self.name_candels, self.count_std)] = self._dan[self.name_candels]
        elif args.__len__() == 0:
            for item in self._candels:
                self.name_candels = item
                self.dan[(self.name_candels, self.count_std)] = self._dan[item]
                self.run()

    def save(self):
        __keyset = list(set([x.replace('dp', '').replace('dm', '').replace('d', '') for x in list(self.kdan.keys())]))
        __keyset.sort()
        _skey = '_'.join([x for x in __keyset]) + ".pkl"
        _path = [self.name_tick, self.nametime, 'Kalman', self._dt0.date(), self._dt1.date(), _skey]
        self.kdan['path'] = _path
        # self.kdan['id'] = self._dan['id']
        # self.kdan['ditetime'] = self._dan['datetime']

        self.save_pickle(self.kdan)

    def loads(self, path):  # не доделал
        _name0 = os.path.basename(path).split('.')[0]
        z = self.load_pickle(path)
        self.__setattr__(_name0, z[_name0])
        k=1

    def load(self, *args, **kwargs):  # не доделал
        if args.__len__() < 1:
            return None
        if args.__len__() == 2:
            with open(args[1], "rb") as fp:
                a1 = pickle.load(fp)
            return a1

        self._load_candels = args[0]

        self.timeframe = kwargs.get('timeframe', self.timeframe)  # _connect_db['nametime'] = "1min"
        self.dt0 = kwargs.get('dt0', self.dt0)
        self.dt1 = kwargs.get('dt1', self.dt1)

        self.count_std = kwargs.get('count_std', self.count_std)

        _path = ConfigDbSing().path_dan()
        # проверка на каталог ТИКЕР  (sbrf)
        _path = _path + "\\" + self._name_ticker

        # проверка на каталог Тime  (1min)
        _path = _path + "\\" + self.timeframe

        # проверка на каталог dt0_dt1
        _path = _path + "\\" + str(self.dt0.date()) + "_" + str(self.dt1.date())

        with open("file.pkl", "rb") as fp:
            a1 = pickle.load(fp)

    def run(self, *args, **kwargs):
        _dsourse = self.dan[(self.name_candels, self.count_std)]
        _count = len(_dsourse)
        xx = np.zeros(_count)
        P = np.zeros(_count)
        Ndisp = self.count_std
        disper = np.zeros(Ndisp).tolist()
        enx = np.zeros(Ndisp).tolist()
        xx[0] = _dsourse[0]
        P[0] = 1
        r = 1  # 0.999 -  корреляция между моделю и данными  ----  переделать
        en = 0.1
        r2 = r * r
        #        en2 = en * en
        DP = np.zeros(_count)
        DM = np.zeros(_count)
        print(' Расчет  !!!')
        _pro = _count // 100
        _sourse = {}
        for i in range(1, _count):
            _d = {}
            if (i % _pro) != 0:
                pass
            elif (i % 5) == 0:
                print(f" {self.name_candels}   выполнено {i // _pro}%")

            disper.pop(0)
            disper.append(_dsourse[i - 1])
            #        dNoise = np.var(disper)
            dNoise = np.std(disper)
            dNoise =  dNoise if dNoise > 0.1 else 0.1
            enx.pop(0)
            enx.append(xx[i - 1])
            f0 = lambda x, y: x - y
            lsx = list(map(f0, disper, enx))
            en = np.std(lsx)

            Pe = r2 * P[i - 1] + en * en
            P[i] = (Pe * dNoise) / (Pe + dNoise)

            # if (i % _pro) != 0:
            #     pass
            # elif (i % 5) == 0:
            #     print(f" {self.name_candels}   выполнено {i // _pro}%")
            __z00 = xx[i - 1]
            __z01 =  r * xx[i - 1]
            __z02 =  (_dsourse[i] - r * xx[i - 1])
            xx[i] = __z01 + P[i] / dNoise * __z02
            # if i >= 6825:
            #     _xdtxx = self._dan['datetime'][i]
            #     __z03 = xx[i]
            #     jjj=1
            #
            # if (i>= 6800) and (i <= 7100): ## and (i % 10 == 0)  and (i % 10 == 0)
            #     print(f" i=>  {i} __z01={__z01}  P[i]={P[i]}  dNoise={dNoise}   __z02={__z02} ")
            #     jjj=1

            DP[i] = xx[i] + en * 0.7
            DM[i] = xx[i] - en * 0.7
            _d['d'] = xx[i]
            _d['dp'] = DP[i]
            _d['dm'] = DM[i]
#            xxx = self._dan['datetime'][i]
            _sourse[self._dan['datetime'][i]] = _d
        print(' Расчет окончен !!!')

        _s = f"{str(self.count_std)}{self.name_candels}"

        # self.kdan['d' + _s] = xx
        # self.kdan['dp' + _s] = DP
        # self.kdan['dm' + _s] = DM

        k = 1
        # __keyset = list(set([x.replace('dp', '').replace('dm', '').replace('d', '') for x in list(self.kdan.keys())]))
        # __keyset.sort()
        _skey = _s + ".pkl"
        _path = [self.TickerName, self.timeframe, 'Kalman', self._dt0.date(), self._dt1.date(), _skey]
        self.kdan['path'] = _path
        self.kdan[_s] = _sourse
        # self.kdan['id'] = self._dan['id']
        # self.kdan['ditetime'] = self._dan['datetime']

        self.save_pickle(self.kdan)
        self.kdan = {}
        k=1
