from ConfigDbSing import ConfigDbSing


from NormVSA import NormVSA

if __name__ == '__main__':
    _connect_db = ConfigDbSing().get_config()
    print(_connect_db)

    _name_ticker = "SBRF"

    _connect_db['name'] = _name_ticker.lower()
    _connect_db['nametime'] = "5min"

    #    _ticker = Ticker(_connect_DbTrade)

    _normVSA = NormVSA(_connect_db)

    print("-------------   расчет коэф-т 5 мин")
    _normVSA.Calc_koef(nametime="5min")
    print("-------------   расчет коэф-т 15 мин")
    _normVSA.Calc_koef(nametime="15min")
    print("-------------   расчет коэф-т 1 час")
    _normVSA.Calc_koef(nametime="1H")

    print("-------------   пересчет нормировка 5 мин  **************************************")
    _normVSA.Calc_ohlcv(nametime="5min")
    print("-------------   пересчет нормировка 15 мин **************************************")
    _normVSA.Calc_ohlcv(nametime="15min")
    print("-------------   пересчет нормировка 1 час  **************************************")
    _normVSA.Calc_ohlcv(nametime="1H")



    #     _normVSA.Calc_koef(dict(nametime="5min", session=1))
    #     _normVSA.Calc_Normalization(dict(nametime="1H", session=1))

    k = 1
'''
import copy
from datetime import datetime, time
from TPref import TPref
from TDateTime import TDateTime
from Ticker import Ticker
import pandas as pd
from datetime import datetime, time, timedelta
import numpy as np
 
'''
