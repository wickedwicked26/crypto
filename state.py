import requests
from config import client

pair_state = {}
start_deal_price = {}
start_deal_time = {}
tick_balance = {}
last_deal_time = {}
usdt_start_deal_balance = {}
deal = {'deal': False}
usdt_balance = {}
step_size = {}
start_time_for_data_base = {}

response = requests.get('https://api.binance.com/api/v3/ticker/price')
data = response.json()
for item in data:
	symbol = item["symbol"]
	if symbol.endswith("USDT"):
		last_deal_time[symbol] = 0

for item in data:
	symbol = item["symbol"]
	if symbol.endswith("USDT"):
		pair_state[symbol] = False


usdt_balance['symbol'] = float(client.get_asset_balance('USDT')['free'])

