import requests
import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
import numpy as np


def get_tickers():
    response = requests.get('https://api.binance.com/api/v3/ticker/price')
    data = response.json()
    usdt_pairs = []
    for item in data:
        symbol = item["symbol"]
        if symbol.endswith("USDT"):
            usdt_pairs.append(symbol)
    return usdt_pairs


def get_compare(symbol):
    client = Client()
    cur_time = datetime.strptime('2023-09-14 00:00:00', '%Y-%m-%d %H:%M:%S')

    old_time = (cur_time - timedelta(days=13))

    start_time = old_time.strftime('%Y-%m-%d %H:%M')
    fin_time = cur_time.strftime('%Y-%m-%d %H:%M')
    candles = client.get_historical_klines(symbol=symbol, interval='3m', start_str=start_time,
                                           end_str=fin_time)
    dataframe = pd.DataFrame(candles,
                             columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                      'quote_asset_volume',
                                      'number_of_trades', 'taker_buy_base_asset_volume',
                                      'taker_buy_quote_asset_volume',
                                      'ignore'])

    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit='ms')
    print(f'{symbol} dataframe got'
          f'')

    dataframe['open'] = pd.to_numeric(dataframe['open'], errors='coerce')
    dataframe['high'] = pd.to_numeric(dataframe['high'], errors='coerce')

    price = dataframe['high']
    dataframe['symbol'] = symbol
    roc = price.pct_change() * 100
    dataframe['roc'] = roc
    new_dataframe = dataframe.loc[dataframe['roc'] > 3]

    print(f'{len(new_dataframe)} impulses for {symbol}')

    for index, row in new_dataframe.iterrows():

        if len(new_dataframe) == 0:
            print(f'[INFO] {symbol} without impulse')
            break

        price = (row['open'] * 0.3) + row['open']

        end_time = row['timestamp']
        candle = client.get_historical_klines(symbol=symbol,
                                              interval='3m',
                                              start_str=f'{end_time - timedelta(hours=24)}',
                                              end_str=f'{end_time}')
        df = pd.DataFrame(candle,
                          columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                   'quote_asset_volume',
                                   'number_of_trades', 'taker_buy_base_asset_volume',
                                   'taker_buy_quote_asset_volume',
                                   'ignore'])

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['low'] = pd.to_numeric(df['low'], errors='coerce')
        df['high'] = pd.to_numeric(df['high'], errors='coerce')
        df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df['vol$'] = df['close'] * df['volume']

        day_volume = sum(df['vol$'])
        df['vol part'] = round((df['vol$'] / day_volume) * 100, 2)
        signal_volume_part = df['vol part'].iloc[-1]

        df = df[:-1]
        #
        # if signal_volume_part < 30:
        #     continue

        df['range_of_high'] = df['high'].pct_change() * 100
        last_negative = df[df['range_of_high'] < 0].index[-1]
        df = df[:last_negative]

        min_price = df['low'].min()
        max_price = df['high'].max()

        range_of_day = round(((max_price - min_price) / min_price) * 100, 2)

        if range_of_day > 6.5:
            continue

        if max_price > price:
            continue

        result = pd.DataFrame(columns=['symbol', 'timestamp', 'price'])

        data = pd.DataFrame({'symbol': [symbol], 'timestamp': [end_time], 'price': [price]})
        result = pd.concat([result, data], ignore_index=True)
        result.to_csv(f'/home/miguel/PycharmProjects/crypto/training/sep/{symbol}_{end_time}.csv')
        print(f'TIMESTAMP : {end_time + timedelta(hours=3)}',
              f'SYMBOL: {symbol}',
              f"IMPULSE : {row['roc']}",

              )


def main():
    ticks = get_tickers()[5:]
    count = len(ticks)
    counter = 1

    for symbol in ticks:
        print(f'[INFO] {symbol} is recording...')
        get_compare(symbol)
        print(f'[INFO] {symbol} is checked. {counter} out of {count} were processed.')
        counter += 1


if __name__ == '__main__':
    main()
