
from ConfigDbSing import ConfigDbSing
from PSQLCommand import PSQLCommand
from TPref import *
from Ticker import *
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

if __name__ == '__main__':
  # X_train = np.array([[1., -1., 2.],[2., 0., 0.],[0., 1., -1.]])
  # scaler = StandardScaler().fit(X_train)

  # scalerModel = scaler.fit(dataFrame)
  # scaledData = scalerModel.transform(dataFrame)
  # scaledData.show()


  print(" ===> Start programm  db 01 <===")
  _connect_db = ConfigDbSing().get_config()
  pref_comp = _connect_db["comp_pref"]
  _connect_db['timeframe'] = "4H"   #"1min" "4H"
  _connect_db['TickerName'] = "SBRF"
  _ticker = Ticker(_connect_db)

  _close = list( _ticker.get_ohlcv(['close'])['close'].values())
  _count_close = len(_close)
  _n_count = 100
  _n_step = 25
  _n_start = _n_count // _n_step
  _n_end = _count_close//_n_step
  _mclose = np.array(_close[:_n_count])
  for i in range(_n_count, _count_close, _n_step):
    print(i)
    m = np.array(_close[i:i+_n_step])
    _mclose = np.append(_mclose, m)[-_n_count:]
    # _mclose = _mclose[-_n_count:]

    _mtclose= _mclose.transpose()
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler.fit(_mtclose.reshape(_n_count, -1)) # .reshape(1, _n_count )
    print(scaler.data_min_.min, scaler.data_max_.max)
    # normalize the dataset and print the first 5 rows
    normalized = scaler.transform(_mtclose.reshape(_n_count, -1 ))
    for i in range(5):
      print(normalized[i][0])
    # inverse transform and print the first 5 rows
    inversed = scaler.inverse_transform(normalized)
    for i in range(5):
      print(inversed[i][0])


    z_scores_np = (_mclose - _mclose.mean()) / _mclose.std()
    np_minmax = 2*((_mclose - _mclose.min()) / (_mclose.max() - _mclose.min()))-1

    scaler = StandardScaler().fit(_mtclose.reshape(_n_count, 1 ))
    X_scaled = scaler.transform(_mtclose.reshape(_n_count, 1 ))
    inversed11 = scaler.inverse_transform(X_scaled)
    X_scaled11 = X_scaled[1]
    X_scaled11=(np.array([-1.8])).transpose()
    inversed12 = scaler.inverse_transform(X_scaled11.reshape(1, 1 ))
    kkkk=1
  k=1
