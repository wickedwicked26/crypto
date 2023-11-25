import asyncio
import traceback
from datetime import datetime, timedelta
from decimal import Decimal
import pandas as pd
import websockets
import json
from error_logs import bot_error_logs, connection_error_logs
from deal import state_tracker
from usdt_tickers import get_tickers
from state import last_deal_time, deal, start_deal_price, tick_balance, start_deal_time, pair_state, \
	usdt_start_deal_balance, step_size, start_time_for_data_base
from check_period import period_filter
from period import current_open, period_data, period_open_price
from telegram_message import send_error, send_connection_res
from day_data import day_data

ticks = get_tickers()[232:]


async def main_data(message):
	try:
		data = json.loads(message)

		if 'result' in data:
			return

		df = pd.json_normalize(data, sep='_')

		df['E'] = pd.to_datetime(df['E'], unit='ms')
		timestamp_with_seconds = df['E'][0].strftime('%Y-%m-%d %H:%M:%S')
		timestamp = df['E'][0].strftime('%Y-%m-%d %H:%M')
		timedelta_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")

		symbol = df['s'][0]

		open_price = float(df['k_o'][0])
		price = float(df['k_c'][0])

		if pair_state[symbol]:
			state_tracker(symbol, price, timestamp)
			return None

		if deal['deal']:
			if not pair_state[symbol]:
				return None

		if last_deal_time[symbol] != 0:
			if timedelta_timestamp < last_deal_time[symbol] + timedelta(hours=3):
				return None

		if current_open[symbol] == 0:
			current_open[symbol] = open_price

		if len(period_data[symbol]) >= 1:
			if timestamp != period_data[symbol][-1][0]:
				if open_price != period_data[symbol][-1][1]:
					period_data[symbol].append([timestamp, open_price])

			if len(period_data[symbol]) > 3:
				period_data[symbol].pop(0)
				current_open[symbol] = period_data[symbol][0][-1]
		else:
			period_data[symbol].append([timestamp, open_price])

		impulse = round(((price - current_open[symbol]) / current_open[symbol]) * 100, 4)

		if impulse >= 2:
			if period_filter(timestamp_with_seconds, symbol, current_open[symbol]):
				period_open = current_open[symbol]
				day_data(timestamp, symbol, price, period_open)

	except Exception as exception:
		bot_error_logs(f'{exception}')
		send_error(exception)


async def candle_stick_data(ticker):
	url = "wss://stream.binance.com:9443/ws/"  # steam address
	first_pair = "xprusdt@kline_1m"  # first pair
	async for sock in websockets.connect(url + first_pair):
		for key, value in pair_state.items():
			if value:
				send_error(f'OPEN DEAL WAS FOUND IN MODULE 2 : {key}')
				break
		send_connection_res(f'MODULE 2 WAS STARTED')

		try:
			pairs = {'method': 'SUBSCRIBE', 'params': ticker, 'id': 1}  # other pairs
			json_subm = json.dumps(pairs)
			await sock.send(json_subm)

			while True:
				resp = await sock.recv()

				await main_data(resp)

		except websockets.ConnectionClosed as e:
			connection_error_logs(f'{e}')


async def main():
	await candle_stick_data(ticks)


if __name__ == '__main__':
	try:
		with open('open_deals_data.json', 'r') as json_file:
			open_deal_data = json.load(json_file)
			module_data = open_deal_data['Module 2']
			if module_data['Open deal'] != 0:

				for key, value in module_data.items():
					symbol = module_data['Open deal']
					deal['deal'] = True
					pair_state[symbol] = True
					start_deal_price[symbol] = module_data['Start deal price']
					tick_balance[symbol] = Decimal(module_data['Balance'])
					period_open_price[symbol] = module_data['Period open price']
					start_deal_time[symbol] = module_data['Start deal time']
					usdt_start_deal_balance[symbol] = module_data['Usdt quantity']
					step_size[symbol] = Decimal(module_data['Step size'])
					start_time_for_data_base[symbol] = module_data['Start time for database']
		asyncio.run(main())

	except Exception as exp:

		traceback_str = traceback.format_exc()
		send_error(f'EXCEPTION IN MODULE 2:\n'
				   f'{traceback_str}.\n'
				   f'MODULE WAS STOPPED.')

		bot_error_logs(exp)
