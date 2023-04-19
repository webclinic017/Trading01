#!/usr/bin/env python3

import math
import pandas as pd
import finplot as fplt
import requests
import time

from datetime import datetime
from ConfigDbSing import ConfigDbSing
from Ticker import Ticker

def form_data():
  _connect_db = ConfigDbSing().get_config()
  pref_comp = _connect_db["comp_pref"]
  _connect_db['timeframe'] = "4H"  # "1min" "4H"
  _connect_db['TickerName'] = "SBRF"

  if pref_comp == "E:\\":
    _connect_db['dt0'] = datetime(2007, 8, 1, 0, 0)
    _connect_db['dt1'] = datetime(2008, 12, 31, 0, 0)

  _ticker = Ticker(_connect_db)

  return _ticker.get_ohlcv(formatd=0) #  0 в формате datefrane --  по умолчанию 1 dict

  # volume

def cumcnt_indices(v):
    v[~v] = math.nan
    cumsum = v.cumsum().fillna(method='pad')
    reset = -cumsum[v.isnull()].diff().fillna(cumsum)
    r = v.where(v.notnull(), reset).cumsum().fillna(0.0)
    return r.astype(int)


def td_sequential(close):
    close4 = close.shift(4)
    # close4 = close.shift(periods=4)
    td = cumcnt_indices(close > close4)
    ts = cumcnt_indices(close < close4)
    return td, ts


def update():
    # load data
    limit = 500
    start = int(time.time()*1000) - (500-2)*60*1000
    # url = 'https://api.bitfinex.com/v2/candles/trade:1m:tBTCUSD/hist?limit=%i&sort=1&start=%i' % (limit, start)
    # table = requests.get(url).json()
    # df = pd.DataFrame(table, columns='time open close high low volume'.split())
    df = form_data()
    # df = df.set_index('datetime')
    # calculate indicator
    _close = df['close']
    tdup,tddn = td_sequential(_close)
    df['tdup'] = [('%i'%i if 0<i<10 else '') for i in tdup]
    df['tddn'] = [('%i'%i if 0<i<10 else '') for i in tddn]

    print(df.columns.values)
    print(df.head())
    # pick columns for our three data sources: candlesticks and TD sequencial labels for up/down
    candlesticks = df['datetime open close high low'.split()]
    volumes = df['datetime open close volume'.split()]
    td_up_labels = df['datetime  high tdup'.split()]
    td_dn_labels = df['datetime  low tddn'.split()]

    plot_candles.candlestick_ochl(candlesticks)
    plot_volume.volume_ocv(volumes, ax=ax.overlay())
    plot_td_up.labels(td_up_labels, color='#009900')
    plot_td_dn.labels(td_dn_labels, color='#990000', anchor=(0.5,0))


plots = []
ax = fplt.create_plot('Realtime Bitcoin/Dollar 1m TD Sequential (BitFinex REST)', init_zoom_periods=100, maximize=False)
plot_candles, plot_volume, plot_td_up, plot_td_dn = fplt.live(4)
update() # !!!!!  повторный вызов 5 раз
fplt.timer_callback(update, 5.0) # update (using synchronous rest call) every N seconds

fplt.show()
k=1