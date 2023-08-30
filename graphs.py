import kaleido
from binance import Client
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from config import client


def start_graph(symbol, timestamp):
    klines = client.get_historical_klines(symbol=symbol, interval='1m',
                                          start_str=f'{datetime.strptime(timestamp, "%Y-%m-%d %H:%M") - timedelta(hours=4)}',
                                          end_str=f'{timestamp}')
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                         'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                         'taker_buy_quote_asset_volume', 'ignored'])

    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    data.set_index('timestamp', inplace=True)
    data['open'] = data['open'].astype(float)
    data['high'] = data['high'].astype(float)
    data['low'] = data['low'].astype(float)
    data['close'] = data['close'].astype(float)
    data['volume'] = pd.to_numeric(data['volume'], errors='coerce')
    data.dropna(subset=['volume'], inplace=True)
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['open'],
                                         high=data['high'],
                                         low=data['low'],
                                         close=data['close'],
                                         increasing_line_color='green',
                                         decreasing_line_color='red')])
    fig.update_layout(
        xaxis_rangeslider_visible=False,  # Скрыть интерактивную строку
        plot_bgcolor='black',  # Цвет фона графика
        paper_bgcolor='black',  # Цвет фона области графика
        font_color='white',
        title=f'{symbol}'
    )

    fig.write_image(f'{symbol}_{timestamp}.png')


def finish_graph(symbol, timestamp, start_deal_timestamp):
    client = Client()
    klines = client.get_historical_klines(symbol=symbol, interval='1m',
                                          start_str=f'{start_deal_timestamp}',
                                          end_str=f'{timestamp}')
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                         'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                         'taker_buy_quote_asset_volume', 'ignored'])

    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    data.set_index('timestamp', inplace=True)
    data['open'] = data['open'].astype(float)
    data['high'] = data['high'].astype(float)
    data['low'] = data['low'].astype(float)
    data['close'] = data['close'].astype(float)
    data['volume'] = pd.to_numeric(data['volume'], errors='coerce')
    data.dropna(subset=['volume'], inplace=True)
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['open'],
                                         high=data['high'],
                                         low=data['low'],
                                         close=data['close'],
                                         increasing_line_color='green',
                                         decreasing_line_color='red')])
    fig.update_layout(
        xaxis_rangeslider_visible=False,  # Скрыть интерактивную строку
        plot_bgcolor='black',  # Цвет фона графика
        paper_bgcolor='black',  # Цвет фона области графика
        font_color='white',
        title=f'{symbol}'
    )

    fig.write_image(f'{symbol}_{timestamp}.png')
