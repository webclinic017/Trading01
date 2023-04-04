from datetime import datetime, time, timedelta
import json

from ConfigDbSing import ConfigDbSing
from FFTPostgres import FFTPostgres
from ElementPostgres import ElementPostgres
#from MyFFT import MyFFT

#    Factory import MyFFT


if __name__ == '__main__':
    print("----- test FFT ---- ")

    _connect_db = ConfigDbSing().get_config()

    _name_ticker = "SBRF"

    _connect_db['name'] = _name_ticker.lower()
    _connect_db['nametime'] = "5min"
    _connect_db['dt0'] = datetime(2021,1,1)
    _connect_db['dt1'] = datetime(2021,12,4)
    dan={}
    # _myFFTthread = MyFFT(dan, npoint=64, countaf=16)
    # _myFFTthread.start()
    # _myFFTthread.join()

    print("  ----  Выход из потока  ")
    _elemetn = ElementPostgres(_connect_db, 'fft')


    npoint = 64

    _fft = FFTPostgres(_connect_db)
    '''
    _dBasa = _fft.get_fft()
    _id = _dBasa['id']
    _count = len(_id)
    _dt = _dBasa['datetime']
    _fft_db = _dBasa['fft']
    for key, val in _id.items():
        if (key % 50) == 0:
            print(f" {key}  -  {val}  -  {_dt[key]}   -   {_fft_db[key]}  ")
            k=1
    '''

#    calc_fft(npoint, _fft.get_ohlcv(npoint, ['ohl'], nametime = "5min", dt0 = datetime(2021,1,4), dt1 = datetime(2021,11,30)))

#    _d = _fft.get_ohlcv(npoint, ['ohl'], nametime = "5min", dt0 = datetime(2021,1,4), dt1 = datetime(2021,11,30))

    k=1


"""

    # 
    # ls = ['ohl', 'datetime', 'id', 'open', 'high', 'low', 'close', 'volume']
    # 
    # jj = 'ohl' in ls
    # for it in ls:
    #     match it:
    #            case "open":
    #                print("00000000000000")
    #                continue
    #            case "high":
    #                print("1111111111111")
    #                continue
    #            case "low":
    #                print("22222222222222222")
    #                continue
    #            case "close":
    #                print("33333333333333333")
    #                continue
    #            case _:
    #                pass
    # k=1


    xval = {'p0':1232, 'p1':234}
    _fft.__setitem__("5m", xval)
    print(_fft.__getitem__('5m'))
 
    dffts = {}
    count_fft = 10
    lsfft0 = [(100, 0), (90, 1), (80, 2), (70, 3), (60, 4), (50, 5), (40, 6), (30, 7), (20, 8), (10, 9)]
    lsfft1 = [(100, 10), (190, 11), (180, 12), (170, 13), (160, 14), (150, 15), (140, 16), (130, 17), (120, 18), (110, 19)]
    lsfft2 = [(200, 20), (290, 21), (280, 22), (270, 23), (260, 24), (250, 25), (240, 26), (230, 27), (220, 28), (210, 29)]
    dffts[64] = {i:val for i, val in enumerate(lsfft0)}
    dffts[99] = {i:val for i, val in enumerate(lsfft1)}
    dffts[128] = {i:val for i, val in enumerate(lsfft2)}

    _dt_tek = datetime.now()
    _dt0 = _dt_tek - timedelta(days=0)
    _dt1 = _dt_tek - timedelta(days=1)
    _dt2 = _dt_tek - timedelta(days=2)
    _dt3 = _dt_tek - timedelta(days=3)
    dDT={}
    dDT[0]=(_dt0, dffts)
    dDT[1]=(_dt1, dffts)
    dDT[2]=(_dt2, dffts)
    dDT[3]=(_dt3, dffts)
    k=1
    pprint(dDT)
    # dfft=dict.fromkeys(range(0, count_fft))
    # for i, val in enumerate(lsfft):
    #     dfft[i]=val


    json_object = json.dumps(dffts) # , indent = 5
    print(json_object)

    ddd=json.loads(json_object)
    pprint(ddd)




"""
