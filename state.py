import requests

pair_state = {}
start_deal_price = {}
pair_day_volume = {}
deal_time = {}
tick_balance = 0
deal_high = {}
last_deal_time = {}

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
