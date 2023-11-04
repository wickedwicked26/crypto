import requests

current_open = {}
period_data = {}
previous_close = {}
response = requests.get('https://api.binance.com/api/v3/ticker/price')
data = response.json()

for item in data:
    symbol = item['symbol']
    if symbol.endswith('USDT'):
        current_open[symbol] = 0

for item in data:
    symbol = item['symbol']
    if symbol.endswith('USDT'):
        period_data[symbol] = []

for item in data:
    symbol = item['symbol']
    if symbol.endswith('USDT'):
        previous_close[symbol] = 0