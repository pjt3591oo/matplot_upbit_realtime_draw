import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_finance import candlestick_ohlc

from datetime import timedelta
import requests as rq
import pandas as pd
import numpy as np
import datetime, random

from convert_DF import convert
import matplotlib.animation as animation


url ='https://crix-api-cdn.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-%s&count=%d&to=%s'
to = ''
is_continue = True
coin="ONG"
max_count = 10

response = rq.get(url%(coin, max_count, to))  # % operation:string formating
candles = convert(response.json())

df = candles

fig = plt.figure(figsize=(8, 5)) # width, height
fig.set_facecolor('w')
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
axes = []
axes.append(plt.subplot(gs[0]))
axes.append(plt.subplot(gs[1], sharex=axes[0]))
axes[0].get_xaxis().set_visible(False)

x = np.arange(len(df.index))
ohlc = df[['open', 'high', 'low', 'close']].astype(int).values
dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))

# 봉차트
candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b')

# 거래량 차트
axes[1].bar(x, df.volume, color='k', width=0.6, align='center')

# x축
_xticks = []
_xlabels = []

for _x, d in zip(x, df.date.values):
    _xticks.append(_x)
    _xlabels.append(datetime.datetime.strptime(str(d), '%Y-%m-%dT%H:%M:%S').strftime('%H:%M:%S'))

axes[1].set_xticks(_xticks)
axes[1].set_xticklabels(_xlabels, rotation=45, minor=False)

print(df)

def update(n):
  global df
  global _xticks
  global _xlabels

  response = rq.get(url%(coin, 1, to))
  new_df = convert(response.json())

  is_add = not (new_df['candleDateTimeKst'].iloc[-1] == df['candleDateTimeKst'].iloc[-1])

  if not is_add:
    return

  df = pd.concat([df, new_df], axis=0)
  _x = datetime.datetime.strptime(str(new_df['date'].iloc[0]), '%Y-%m-%dT%H:%M:%S').strftime('%H:%M:%S')
  _xlabels.append(_x)
  _xticks.append(len(_xticks))

  x = np.arange(len(df.index))

  ohlc = df[['open', 'high', 'low', 'close']].astype(int).values
  dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))
  
  candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b')
  axes[1].bar(x, df.volume, color='k', width=0.6, align='center') 

  axes[1].set_xticks(_xticks)
  axes[1].set_xticklabels(_xlabels, rotation=45, minor=False)

  return fig

ani = animation.FuncAnimation(fig, update, interval=1)

plt.tight_layout()
axes[0].grid()
axes[1].grid()
plt.show()