# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
#  -> Используйте метакласс
import os, sys

class Singleton():
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._inst[cls]

    @property
    def inst(self):
        return self._inst

    def Config(self):
        self._inst['pathGl'] = 'E:\MLserver'
        self._instW = 'E:'
        self._inst['pathDb'] = 'Trade\DbData'
        self._inst['log'] = 'Trade\Log'

        if not os.path.isdir(self.FullPathDir()):
            self._inst['pathGl'] =  self._instW = 'E:'
            if not os.path.exists(self.FullPathDir()):
                print(" Нет db котировок \n  ==>>  Error -1")
                sys.exit(-1)


    def FullPathDir(self):
        return self._inst['pathGl']+"\\"+self._inst['pathDb']


    def FullPathDb(self):
        return self._inst['pathGl']+"\\"+self._inst['pathDb'] + "\\" + self._inst['nameDb']

    def FullPathLog(self):
        return self._inst['pathGl']+"\\"+self._inst['log'] + "\\" + self._inst["log_dir"]
