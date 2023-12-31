from datetime import timedelta, datetime
from binance import Client
import pandas as pd
from orders import buy_order
from config import client


def day_data(timestamp, symbol, price, period_open_price):
	candle = client.get_historical_klines(symbol=symbol,
										  interval='1m',
										  start_str=f'{datetime.strptime(timestamp, "%Y-%m-%d %H:%M") - timedelta(hours=8)}',
										  end_str=f'{timestamp}')
	df = pd.DataFrame(candle,
					  columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
							   'quote_asset_volume',
							   'number_of_trades', 'taker_buy_base_asset_volume',
							   'taker_buy_quote_asset_volume',
							   'ignore'])

	if len(df) <= 1:
		return None
	df['low'] = pd.to_numeric(df['low'], errors='coerce')
	df['high'] = pd.to_numeric(df['high'], errors='coerce')

	df = df[:-1]

	df['range_of_high'] = df['high'].pct_change() * 100
	last_negative = df[df['range_of_high'] < 0].index[-1]
	df = df[:last_negative]

	min_price = df['low'].min()
	max_price = df['high'].max()

	range_of_day = round(((max_price - min_price) / min_price) * 100, 2)

	if range_of_day > 6.5:
		return None

	if max_price > price:
		return None

	buy_order(symbol, price, timestamp, period_open_price)
