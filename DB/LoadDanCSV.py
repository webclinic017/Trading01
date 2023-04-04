import copy
import json
import sys
import socket

import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta

from DbModuls.TPref import TPref
from DbModuls.TDateTime import TDateTime
from LoadCSV import LoadCSV
from Ticker import Ticker
from ConfigDbSing import ConfigDbSing
from PSQLCommand import PSQLCommand


def NoFeatures(it):
  # match it:
  #     case -1:
  #         print("Очистил базу")
  #     case -2:
  #         print("Error")

  sys.exit(it)


def delete_tables(_connect_db):
  send = "SELECT table_name FROM information_schema.tables " \
         "WHERE table_schema NOT IN ('information_schema','pg_catalog');"
  _command = PSQLCommand(_connect_db)
  _ls = _command.fcommand_fetchall(send)

  if _ls == None:
    sys.exit(0)

  ls = [x[0] for x in _ls]
  _command.del_tables(ls)
  raise NoFeatures(-1)


if __name__ == '__main__':
  _connect_db = ConfigDbSing().get_config()
  pref_comp = _connect_db["comp_pref"]
  print(pref_comp)

  to_json = json.dumps(_connect_db)

  '''
    path = pref_comp + "Trade\Log\SBER/SBER_210101_211205.csv"  # _2
    path_dir = pref_comp + "Trade\Log\SBER"
    _name_ticker = "SBRF"
    '''
  # path_dir = pref_comp + "Trade\Log\SBER"
  path_dir = pref_comp + "Trade\Log\GAZP"

  _connect_db['timeframe'] = "1min"
  #_connect_db['TickerName'] = "SBRF"
  _connect_db['TickerName'] = "GAZP"
  _connect_db['TickerName'] = _connect_db['TickerName'].lower()

  # ====----   удаление таблиц  ---=======
  # delete_tables(_connect_db)

  _ticker = Ticker(_connect_db)

  ''' 
    /////  для одного файла данных  ////
    _loadCSV = LoadCSV()
    _dancsv = _loadCSV.ReadOneFile(path)
    _ticker.write_db_ohlsv(_dancsv)
    '''

  # _loadCSV = LoadCSV(_ticker)
  # _dancsv = _loadCSV.ReadAllFiles(path_dir)

  print("======  CONVERT  1min  5min ===================!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  _ticker.ConvertTimeToTime('1min', '5min')
  print("======  CONVERT  5min  15min ===================!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  _ticker.ConvertTimeToTime('5min', '15min')
  print("======  CONVERT  15min  1H ===================!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  _ticker.ConvertTimeToTime('15min', '1H')
  print("======  CONVERT  1H  4H ===================!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  _ticker.ConvertTimeToTime('1H', '4H')

  kk = 1
  print("----  ВСЕ  -----")
''' 


    
    # _tdt.insert(ls)
    # ddd = _tdt.get(ls)

    # _tpref = TPref(_connect_DbTrade)
    # _tdt = TDateTime(_connect_DbTrade)

    # x = _tpref.insert(_connect_DbTrade['nametime'])

'''
#    _name_ticker = "GAZP"
#    path = "E:\Trade\Log\GAZP/GAZP_211201_220206.csv"
# ---    _create_tables = PSQLTables(_connect_dbUpdate)
# ---    _create_tables.create_table(_name_ticker)

# _connect_dbUpdate['name'] = _name_ticker.lower()
# _connect_dbUpdate['nametime'] = "1min"
#
# _updateDb = UpdateDb(_connect_dbUpdate, Stocks)
#    _updateDb = UpdateDb(_connect_dbUpdate, Stocks(_connect_dbUpdate))
