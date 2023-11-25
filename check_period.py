import pandas as pd
from config import client
from datetime import datetime, timedelta


def period_filter(timestamp, symbol, open_price):
    candle = client.get_historical_klines(symbol=symbol,
                                          interval='1s',
                                          start_str=f'{datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=4)}',
                                          end_str=f'{timestamp}')
    df = pd.DataFrame(candle,
                      columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                               'quote_asset_volume',
                               'number_of_trades', 'taker_buy_base_asset_volume',
                               'taker_buy_quote_asset_volume',
                               'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['open'] = pd.to_numeric(df['open'], errors='coerce')
    prices = df['close']
    df['range of close'] = prices.pct_change() * 100

    period_start_ind = df[df['open'] >= open_price].index[0]

    df = df[['timestamp', 'open', 'range of close']][period_start_ind:]
    range_of_close_values = []
    for index, row in df['range of close'][::-1].items():
        range_of_close_values.append(row)
        if sum(range_of_close_values) >= 2:
            if len(range_of_close_values) <= 5:
                return False
            return True
