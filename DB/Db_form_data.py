from datetime import datetime

from ConfigDbSing import ConfigDbSing
from Ticker import Ticker


def Db_form_data(*args, **kwargs):
  _connect_db = ConfigDbSing().get_config()
  pref_comp = _connect_db["comp_pref"]

  _tickerName = kwargs.get("TickerName", "SBRF")
  _timeframe = kwargs.get("timeframe", "4H")
  _formatd = kwargs.get("formatd", 0)

  _connect_db['timeframe'] = _timeframe  # "1min" "4H"
  _connect_db['TickerName'] = _tickerName

  if pref_comp == "E:\\":
    _dt0 = kwargs.get('dt0', datetime(2007, 8, 1, 0, 0))
    _dt1 = kwargs.get('dt1', datetime.now())
    _dtx = max(_dt0, datetime(2007, 8, 1, 0, 0))
    _connect_db['dt0'] = _dtx
    _connect_db['dt1'] = datetime(2008, 12, 31, 0, 0)

  _ticker = Ticker(_connect_db)

  return _ticker.get_ohlcv(formatd=_formatd)  # 0 в формате datefrane --  по умолчанию 1 dict
