
from ConfigDbSing import ConfigDbSing
from PSQLCommand import PSQLCommand
from TPlot import TPlot
from TPlot import PltShow
from Ticker import *
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model

'''
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


'''
def filterKalmana(d):
  z = np.array(d)
  _count = len(z)
  xx = np.zeros(_count)
  P = np.zeros(_count)
  Ndisp = 5
  disper = np.zeros(Ndisp).tolist()
  enx = np.zeros(Ndisp).tolist()
  xx[0] = z[0]
  P[0] = 1
  r = 1  # 0.999
  en = 0.1
  #    dNoise=12
  r2 = r * r
  en2 = en * en
  DP = np.zeros(_count)
  DM = np.zeros(_count)
  print(' Расчет  !!!')
  for i in range(1, _count):
    disper.pop(0)
    disper.append(z[i - 1])
    #        dNoise = np.var(disper)
    dNoise = np.std(disper)
    enx.pop(0)
    enx.append(xx[i - 1])
    f0 = lambda x, y: x - y
    lsx = list(map(f0, disper, enx))
    en = np.std(lsx)

    Pe = r2 * P[i - 1] + en * en
    P[i] = (Pe * dNoise) / (Pe + dNoise)
    xx[i] = r * xx[i - 1] + P[i] / dNoise * (z[i] - r * xx[i - 1])
    DP[i] = xx[i] + en * 0.7
    DM[i] = xx[i] - en * 0.7
  kkk=1
  return list(xx)
    # Pe=r2*P[i-1]+en2
    # P[i] = (Pe*dNoise)/(Pe+dNoise)
    # xx[i]=r*xx[i-1]+P[i]/dNoise*(z[i]-r*xx[i-1])
    #
    #  my_plot(_dan['ohl'])
    #  my_plot(z, xx, DP, DM)
  # my_plot(z, xx, _dan_d)
  # kk = 1


if __name__ == '__main__':
  print(" ===> Start programm  db 01 <===")
  _tPlot = TPlot()
  _connect_db = ConfigDbSing().get_config()
  pref_comp = _connect_db["comp_pref"]
  _connect_db['timeframe'] = "4H"   #"1min" "4H"
  _connect_db['TickerName'] = "SBRF"
  _ticker = Ticker(_connect_db)

  _close = list( _ticker.get_ohlcv(['close'])['close'].values())
  _count_close = len(_close)
  _n_count = 200
  _n_step = 25
  _n_start = _n_count // _n_step
  _n_end = _count_close//_n_step
  _mclose = np.array(_close[:_n_count])

  for i in range(_n_count, _count_close, _n_step):
    print(i)
    m = np.array(_close[i:i+_n_step])
    _mclose = np.append(_mclose, m)[-_n_count:]
    _mtclose = _mclose.transpose()
    _xclose=np.arange(_n_count).transpose()
    mas_price = list(_mclose)

    # _lLineregres = linear_model.LinearRegression()
    # _line_reg = _lLineregres.fit(_xclose.reshape(_n_count, -1), _mtclose.reshape(_n_count, -1))
    # _regress = _line_reg.predict(_xclose.reshape(_n_count, -1))


    masg={'d':mas_price}
    # masg['r']=list(_regress)
    masg['r']=filterKalmana(mas_price)
    masg['t']=[k0 for k0 in range(len(mas_price))]
    _tPlot.PlotDict(masg)


    scaler_min_max = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler_min_max.fit(_mtclose.reshape(_n_count, -1))
    normalized = scaler_min_max.transform(_mtclose.reshape(_n_count, -1 ))
    # for i in range(5):
    #   print(normalized[i][0])
    # # inverse transform and print the first 5 rows
    inversed = scaler_min_max.inverse_transform(normalized)
    # for i in range(5):
    #   print(inversed[i][0])

    # z_scores_np = (_mclose - _mclose.mean()) / _mclose.std()
    # np_minmax = 2*((_mclose - _mclose.min()) / (_mclose.max() - _mclose.min()))-1

    scaler_std = StandardScaler().fit(_mtclose.reshape(_n_count, 1 ))
    X_scaled = scaler_std.transform(_mtclose.reshape(_n_count, 1 ))
    inversed11 = scaler_std.inverse_transform(X_scaled)
    X_scaled11=(np.array([-1.8])).transpose()
    inversed12 = scaler_std.inverse_transform(X_scaled11.reshape(1, 1 ))



    kkk=1
  k=1
