import tradingview_ta
from tradingview_ta import TA_Handler, Interval, Exchange

tesla = TA_Handler(
    symbol="TSLA",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY
)
print(tesla.get_analysis().summary)

print(tradingview_ta.__version__)

handler = TA_Handler(
    symbol="",
    exchange="",
    screener="",
    interval="",
    timeout=None
)

k=1