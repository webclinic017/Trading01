# https://pypi.org/project/finplot/

k=1
import finplot as fplt
k=1
import yfinance


gg=1
df = yfinance.download('AAPL')
fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
fplt.show()
j=1