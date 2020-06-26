from mpl_finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import requests as rq
from convert_DF import convert


url ='https://crix-api-cdn.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-%s&count=%d&to=%s'
to = ''
is_continue = True
coin="ETH"
max_count = 200

response = rq.get(url%(coin, max_count, to))  # % operation:string formating
candles = convert(response.json())

# print(candles)

fig = plt.figure(figsize=(10, 10))
ax_main = fig.add_subplot(1,1,1)

candlestick2_ohlc(ax_main, candles['open'], candles['high'], candles['low'], candles['close'], width=0.5, colorup='r', colordown='b')

plt.grid()
plt.show()