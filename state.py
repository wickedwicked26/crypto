import requests
from config import client

pair_state = {}
start_deal_price = {}
pair_day_volume = {}
deal_time = {}
tick_balance = {}
deal_high = {}
last_deal_time = {}
balance = {}
half_quantity = {}

response = requests.get('https://api.binance.com/api/v3/ticker/price')
data = response.json()

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        pair_state[symbol] = 'Not in deal'

for item in data:
    symbol = item["symbol"]
    if symbol.endswith("USDT"):
        pair_day_volume[symbol] = 0

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


balance['balance'] = 10_000


