import asyncio
import pandas as pd
import websockets
import json
from error_logs import bot_error_logs
from usdt_tickers import get_tickers
from state import pair_state, last_deal_time, last_deal_open, deal
from deal import state_tracker
from telegram_message import send_error, send_connection_res
from day_data import day_data

ticks = get_tickers()[2:302]


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

        if open_price == last_deal_open[symbol]:
            return None

        if timestamp == last_deal_time[symbol]:
            return None

        if deal['deal'] == 'Yes':
            return None

        impulse = round(((price - open_price) / open_price) * 100, 4)

        if impulse > 9:
            last_deal_open[symbol] = open_price
            day_data(timestamp, symbol, price)

    except KeyError:
        pass


async def candle_stick_data(ticker):
    url = "wss://stream.binance.com:9443/ws/"  # steam address
    first_pair = "xprusdt@kline_3m"  # first pair
    async for sock in websockets.connect(url + first_pair):
        for key, value in pair_state.items():
            if value == 'Deal':
                send_error(f'OPEN DEAL WAS FOUND IN MODULE 1 : {key}')
        send_connection_res(f'MODULE 1 WAS STARTED')

        try:
            pairs = {'method': 'SUBSCRIBE', 'params': ticker, 'id': 1}  # other pairs
            json_subm = json.dumps(pairs)
            await sock.send(json_subm)

            while True:
                resp = await sock.recv()

                await main_data(resp)

        except websockets.ConnectionClosed as e:
            bot_error_logs(f'{e}')


async def main():
    await candle_stick_data(ticks)


if __name__ == '__main__':
    try:
        with open('active_trades.txt', 'r+') as file:
            for line in file:
                symbol = line.strip()
                pair_state[symbol] = 'Deal'
            file.seek(0)
            file.truncate()

        asyncio.run(main())

    except Exception as exp:

        send_error(f'EXCEPTION IN MODULE 1: {exp}. MODULE WAS STOPPED.')

        with open('active_trades.txt', 'w') as file:
            for key, value in pair_state.items():
                if value == 'Deal':
                    file.write(key + '\n')
        bot_error_logs(exp)
