import requests
from config import client

pair_state = {}
start_deal_price = {}
deal_time = {}
tick_balance = {}
deal_high = {}
last_deal_time = {}
usdt_start_deal_balance = {}
half_quantity = {}
step_sizes = {}

response = requests.get('https://api.binance.com/api/v3/ticker/price')
data = response.json()

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        pair_state[symbol] = 'Not in deal'

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        start_deal_price[symbol] = 0

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        deal_time[symbol] = 0

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        deal_high[symbol] = 0

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        last_deal_time[symbol] = 0

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        tick_balance[symbol] = 0

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        half_quantity[symbol] = 'No'

usdt_start_deal_balance['balance'] = 0

url = f'https://api.binance.com/api/v1/exchangeInfo'
response = requests.get(url)

data = response.json()
step_size = 0
for symbol_info in data['symbols']:
    if symbol_info['symbol'].endswith('USDT'):
        symbol = symbol_info['symbol']
        for filter_item in symbol_info['filters']:
            if filter_item['filterType'] == 'LOT_SIZE':
                step_sizes[symbol] = filter_item['stepSize']

