from ConfigDbSing import ConfigDbSing
from TPlot import TPlot
from TPlot import PltShow
from Ticker import *
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model
from LoadSavePickle import LoadSavePickle

if __name__ == '__main__':
  print(" ===> Формируем данные для LSTM <===")
  _tPlot = TPlot()

  _connect_db = ConfigDbSing().get_config()
  _path_kaufman = ConfigDbSing().path_files("Trading01\\NotGit\\Data\\fkaufman.pkl")

  # _path_kaufman = "E:\\MLserver\\Trading01\\NotGit\\Data\\fkaufman.pkl"
  # _path_kaufman = "E:\\Trading01\\NotGit\\Data\\fkaufman.pkl"

  _lPickle = LoadSavePickle()
  _loadFKaufman = _lPickle.load_path(_path_kaufman)
  _fk = np.array(_loadFKaufman.fk)
  _kp = np.array(_loadFKaufman.kp)
  _km = np.array(_loadFKaufman.kp)
  _close = np.array(_loadFKaufman.close)

  _dcfk = _close - _fk

  # _tPlot.PlotDict({'d':_dcfk})

  # _path_forLSTMdcfk = "E:\\MLserver\\Trading01\\NotGit\\Data\\forLSTMdcfk.pkl"
  _path_forLSTMdcfk = ConfigDbSing().path_files("Trading01\\NotGit\\Data\\forLSTMdcfk.pkl")
  _sPickle = LoadSavePickle({"close": _close, "dcfk":_dcfk})
  _sPickle.save_path(_path_forLSTMdcfk)

  k=1
