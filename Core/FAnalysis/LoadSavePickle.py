from ConfigDbSing import ConfigDbSing
import os
import pickle


class LoadSavePickle:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def save_pickle(self, *args, **kwargs):
        if args.__len__() <= 0:
            return

        d = args[0]
        _path = d.get('path', None)
        if _path is None:
            return

        del d['path']
        _key = list(d.keys())
        _path_file =  self.__create_path(_path)

        # self.__setattr__('id', self.id)
        # self.__setattr__('datetimw', self.datetime)

        self.__setattr__('mykey', _key)
        for item in _key:
            self.__setattr__(item, d[item])

        if os.path.exists(_path_file):
            os.remove(_path_file)


        with open(_path_file, "wb") as fp:
                    pickle.dump(self, fp)
        k=1

    def save_path(self, path):
        d = self._args[0]
        _key = list(d.keys())

        self.__setattr__('mykey', _key)
        for item in _key:
            self.__setattr__(item, d[item])

        if os.path.exists(path):
            os.remove(path)


        with open(path, "wb") as fp:
                    pickle.dump(self, fp)
        k=1


    def load_pickle(self, *args):
        if args.__len__() <= 0:
            return

        with open(args[0], "rb") as fp:
            a1 = pickle.load(fp)
            return a1
    def load_path(self, path):

        with open(path, "rb") as fp:
            a1 = pickle.load(fp)
            return a1


    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        self.__getattribute__('mykey')
        self.mykey = self.__getattribute__('mykey')
        for item in self.mykey:
            self.__getattribute__(item)
            state[item]=self.__getattribute__(item)
        state['id']=self.__getattribute__('id')
        state['datetimw']=self.__getattribute__('datetime')

        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        _mykey = list(state.keys())

        for item in _mykey:
            self.__setattr__(item, state[item])

    def __create_path(self, ls: list):
        _path = ConfigDbSing().path_dan()
        if ls.__len__() < 6:
            return None

        # проверка на каталог ТИКЕР  (sbrf)
        _path = _path + "\\" + ls[0]  # self._name_ticker
        if not (os.path.exists(_path)):
            os.mkdir(_path)

        # проверка на каталог Тime  (1min)
        _path = _path + "\\" + ls[1]  # self.timeframe
        if not (os.path.exists(_path)):
            os.mkdir(_path)

        # проверка на каталог Kalman  (1min)
        _path = _path + "\\" + ls[2]        # 'Kalman'
        if not (os.path.exists(_path)):
            os.mkdir(_path)

        # проверка на каталог dt0_dt1
        _path = _path + "\\" + str(ls[3]) + "_" + str(ls[4])    # str(self.dt0.date()) + "_" + str(self.dt1.date())
        if not (os.path.exists(_path)):
            os.mkdir(_path)

        # название файла
        _path = _path + "\\" + ls[5]
        return _path

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        self.__getattribute__('mykey')
        self.mykey = self.__getattribute__('mykey')
        for item in self.mykey:
            self.__getattribute__(item)
            state[item]=self.__getattribute__(item)
        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        _mykey = list(state.keys())

        for item in _mykey:
            self.__setattr__(item, state[item])
