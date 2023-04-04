
from ConfigDbSing import ConfigDbSing
from PSQLCommand import PSQLCommand
from TPref import *
from Ticker import *

if __name__ == '__main__':
  print(" ===> Start programm  db 01 <===")
  _connect_db = ConfigDbSing().get_config()
  pref_comp = _connect_db["comp_pref"]
  _connect_db['timeframe'] = "4H"   #"1min" "4H"
  _connect_db['TickerName'] = "SBRF"
  _ticker = Ticker(_connect_db)

  _close = _ticker.get_ohlcv(['close'])['close'].values()
  # _close = x
  k=1
