import requests
from config import client


pair_state = {}
start_deal_price = {}
deal_time = {}
tick_balance = {}
deal_high = {}
last_deal_time = {}
usdt_start_deal_balance = {}
last_deal_open = {}
deal = {'deal': False}
usdt_balance = {}
step_size = {}

response = requests.get('https://api.binance.com/api/v3/ticker/price')
data = response.json()

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        pair_state[symbol] = False

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
    symbol = item['symbol']
    if symbol.endswith("USDT"):
        last_deal_open[symbol] = 0

for item in data:
    symbol = item['symbol']
    if symbol.endswith("USDT"):
        usdt_start_deal_balance[symbol] = 0

for item in data:
    symbol = item['symbol']
    if symbol.endswith("USDT"):
        step_size[symbol] = 0

usdt_balance['symbol'] = float(client.get_asset_balance('USDT')['free'])