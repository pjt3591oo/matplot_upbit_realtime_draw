from pandas import DataFrame

def convert(candles):
  after = {
    "code": [],
    "open": [],
    "high": [],
    "low": [],
    "close": [],
    "volume": [],
    "date": [],
    'timestamp_tick': [],
    'candleDateTimeKst': []
  }

  for candle in candles:
    print(candle['candleDateTime'])
    after['code'].append(candle['code'])
    after['open'].append(candle['openingPrice'])
    after['high'].append(candle['highPrice'])
    after['low'].append(candle['lowPrice'])
    after['close'].append(candle['tradePrice'])
    after['volume'].append(candle['candleAccTradeVolume'])
    after['date'].append(candle['candleDateTime'].split('+')[0])
    after['timestamp_tick'].append(int(candle['timestamp']%60))
    after['candleDateTimeKst'].append(candle['candleDateTimeKst'])
  
  return DataFrame(after)
  