from datetime import datetime, time, timedelta

from Ticker import Ticker
from Kalman import Kalman
from ConfigDbSing import ConfigDbSing
import matplotlib.pyplot as plt
import numpy as np

def my_plot(*args):
    print(" РИСУЕМ ")
    if args.__len__() < 1:
        return
    if args.__len__() == 1:
        plt.plot(args[0])
        plt.grid()
        plt.show()
        return
#
#     if args.__len__()==3:
#         # отображение результатов
#         fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 5))
# #        ax1.plot(args[0], label = "Истенные координаты")  # x
#         ax1.plot(args[0], label = "Наблюдения")           # z
#         ax1.plot(args[1], label = "Оценка" )              # xx
#         ax1.grid(True)
#         ax1.legend()
#
#         ax2.plot(args[2])                                 # P
#         ax2.grid(True)
#         plt.show()
#         return

    if args.__len__()==3:
        # отображение результатов
        fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
#        ax1.plot(args[0], label = "Истенные координаты")  # x
        ax1.plot(args[0], label = "Наблюдения")           # z
        ax1.plot(args[1], label = "Оценка" )              # xx
        ax1.plot(args[2], label = "D" )              # xx
        ax1.grid(True)
        ax1.legend()
        plt.show()


    if args.__len__()==4:
        # отображение результатов
        fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
#        ax1.plot(args[0], label = "Истенные координаты")  # x
        ax1.plot(args[0], label = "Наблюдения")           # z
        ax1.plot(args[1], label = "Оценка" )              # xx
        ax1.plot(args[2], label = "D+" )              # xx
        ax1.plot(args[3], label = "D-" )              # xx
        ax1.grid(True)
        ax1.legend()
        plt.show()


if __name__ == '__main__':
    # ls0 = [10,11,12,13 ]
    # ls1=[1,3,5,7]
    # f0 = lambda x, y: x-y
    # lsx = list(map(f0,ls0, ls1))
    
    print(' Test Kalman')
    __dt0 = datetime(2021, 9, 1)
    __dt1 = datetime(2021, 11, 1)
    _connect_db = ConfigDbSing().get_config()

    _connect_db['TickerName'] = "SBRF"
    #_connect_db['TickerName'] = "GAZP"
    _connect_db['TickerName'] = _connect_db['TickerName'].lower()
    _connect_db['timeframe'] = "1min"
    _connect_db['dt0'] = __dt0
    _connect_db['dt1'] = __dt1
    _connect_db['candels'] = ['ohl']
    _connect_db['npoint'] = 60*2

    _kalman = Kalman(_connect_db)
#    _kalman.install()
    _dan_key = _kalman.get_key_dict(keys=['kalman120ohl'] , dt0 = __dt0,  dt1 = __dt1) # , dt0 = datetime(2021, 9, 1),  dt1 = datetime(2021, 11, 1)
    _dan_d = _dan_key['kalman120ohl']['d']

    _ticker = Ticker(_connect_db)
    _candels = _ticker.get_ohlcv(['ohl'], dt0 = __dt0,  dt1 = __dt1)
    _dan = _ticker.get_dan(_candels)
    # _dt = _dan['datetime'][0]
    # _close = _dan['close'][0]
    # _ohl = _dan['ohl'][0]
    z= np.array(_dan['ohl'])

    _count = len(z)
    xx=np.zeros(_count)
    P = np.zeros(_count)
    Ndisp=60*2
    disper = np.zeros(Ndisp).tolist()
    enx =  np.zeros(Ndisp).tolist()
    xx[0]=z[0]
    P[0]=1
    r=1 #0.999
    en=0.1
#    dNoise=12
    r2=r*r
    en2=en*en
    DP=np.zeros(_count)
    DM=np.zeros(_count)
    print(' Расчет  !!!')
    for i in range(1, _count):
        disper.pop(0)
        disper.append(z[i-1])
#        dNoise = np.var(disper)
        dNoise = np.std(disper)
        enx.pop(0)
        enx.append(xx[i-1])
        f0 = lambda x, y: x-y
        lsx = list(map(f0,disper, enx))
        en=np.std(lsx)

        # en=np.var(enx)

        Pe=r2*P[i-1]+en*en
        P[i] = (Pe*dNoise)/(Pe+dNoise)
        xx[i]=r*xx[i-1]+P[i]/dNoise*(z[i]-r*xx[i-1])
        DP[i]=xx[i]+en*0.7
        DM[i]=xx[i]-en*0.7


        # Pe=r2*P[i-1]+en2
        # P[i] = (Pe*dNoise)/(Pe+dNoise)
        # xx[i]=r*xx[i-1]+P[i]/dNoise*(z[i]-r*xx[i-1])


#    my_plot(_dan['ohl'])
#    my_plot(z, xx, DP, DM)
    my_plot(z, xx, _dan_d)
    kk = 1
