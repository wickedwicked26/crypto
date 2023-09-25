import asyncio
import pandas as pd
import websockets
import json
from usdt_tickers import get_tickers, get_volume
from state import pair_state, last_deal_time, last_deal_open
from deal import state_tracker
from telegram_message import send_error, send_connection_res
from day_data import day_data

ticks1 = get_tickers()[302:]


async def main_data(message):
    try:
        data = json.loads(message)

        df = pd.json_normalize(data, sep='_')
        df['E'] = pd.to_datetime(df['E'], unit='ms').dt.strftime('%Y-%m-%d %H:%M')

        timestamp = df['E'][0]
        symbol = df['s'][0]
        open_price = float(df['k_o'][0])
        price = float(df['k_c'][0])
        volume = float(df['k_v'][0]) * float(df['k_c'][0])
        if pair_state[symbol] == 'Deal':
            state_tracker(symbol, price, volume, timestamp)
            return None

        if timestamp == last_deal_time[symbol]:
            return None

        if open_price == last_deal_open[symbol]:
            return None

        impulse = round(((price - open_price) / open_price) * 100, 4)

        if impulse > 9:
            last_deal_open[symbol] = open_price
            day_data(timestamp, symbol, price)

    except KeyError:
        pass


async def candle_stick_data(tickers):
    url = "wss://stream.binance.com:9443/ws/"  # steam address
    # if ticks[0].split('@')[-1] == 'kline_3m':
    first_pair = "xprusdt@kline_3m"  # first pair
    # first_pair = "xprusdt@ticker"  # first pair
    async for sock in websockets.connect(url + first_pair):
        send_connection_res(f'МОДУЛЬ 2 ЗАПУЩЕН')

        try:
            pairs = {'method': 'SUBSCRIBE', 'params': tickers, 'id': 1}  # other pairs
            json_subm = json.dumps(pairs)
            await sock.send(json_subm)

            while True:
                resp = await sock.recv()

                await main_data(resp)

        except websockets.ConnectionClosed as e:
            print(e)


async def main():
    # await asyncio.gather(candle_stick_data(ticks), candle_stick_data(ticks1))
    await candle_stick_data(ticks1)


if __name__ == '__main__':
    try:

        asyncio.run(main())
    except Exception as exp:
        send_error(f'ВОЗНИКЛА ОШИБКА В МОДУЛЕ 2: {exp}. МОДУЛЬ ОСТАНОВЛЕН.')
