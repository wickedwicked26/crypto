import asyncio
from datetime import datetime, timedelta
import pandas as pd
import websockets
import json
from error_logs import bot_error_logs
from usdt_tickers import get_tickers
from state import pair_state, last_deal_time, last_deal_open, deal, start_deal_price, tick_balance

from period import current_open, period_data, previous_close, period_price_range, period_end
from deal import state_tracker
from telegram_message import send_error, send_connection_res
from day_data import day_data

ticks = get_tickers()[:1]


async def main_data(message):
    try:
        data = json.loads(message)
        df = pd.json_normalize(data, sep='_')
        df['E'] = pd.to_datetime(df['E'], unit='ms').dt.strftime('%Y-%m-%d %H:%M')

        timestamp = df['E'][0]
        symbol = df['s'][0]
        price = float(df['k_c'][0])
        open_price = float(df['k_o'][0])

        timedelta_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")

        if pair_state[symbol]:
            state_tracker(symbol, price, timestamp)
            return None

        if last_deal_time[symbol] != 0:
            if timedelta_timestamp < last_deal_time[symbol] + timedelta(hours=3):
                return None

        if previous_close[symbol] == 0:
            previous_close[symbol] = price

        if current_open[symbol] == 0:
            current_open[symbol] = open_price

        range_of_price = ((price - previous_close[symbol]) / previous_close[symbol]) * 100

        if len(period_data[symbol]) >= 1:

            period_price_range[symbol].append(range_of_price)

            if timestamp != period_data[symbol][-1][0]:
                if open_price != period_data[symbol][-1][1]:
                    period_data[symbol].append([timestamp, open_price])

            if len(period_data[symbol]) > 3:
                period_data[symbol].pop(0)
                current_open[symbol] = period_data[symbol][0][-1]
                period_end[symbol] = True
        else:
            period_data[symbol].append([timestamp, open_price])
            period_price_range[symbol].append(range_of_price)

        impulse = round(((price - current_open[symbol]) / current_open[symbol]) * 100, 4)
        last_five_sec_range_sum = sum(period_price_range[symbol][-5:])

        if timestamp == last_deal_time[symbol]:
            return None

        if deal['deal']:
            return None

        if last_deal_open[symbol] == current_open[symbol]:
            return None

        if impulse >= 6:
            if range_of_price < 6:
                if last_five_sec_range_sum < 6:
                    last_deal_open[symbol] = current_open[symbol]
                    day_data(timestamp, symbol, price)

        if period_end[symbol]:
            period_price_range[symbol] = period_price_range[symbol][-5:]
            period_end[symbol] = False

        previous_close[symbol] = price
    except KeyError:
        pass


async def candle_stick_data(ticker):
    url = "wss://stream.binance.com:9443/ws/"  # steam address
    first_pair = "xprusdt@kline_1m"  # first pair
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
                line = line.strip()
                symbol = line.split(' ')[0]
                start_deal_price[symbol] = float(line.split(' ')[1])
                tick_balance[symbol] = float(line.split(' ')[-1])
                pair_state[symbol] = 'Deal'
            file.seek(0)
            file.truncate()

        asyncio.run(main())

    except Exception as exp:

        send_error(f'EXCEPTION IN MODULE 1: {exp}. MODULE WAS STOPPED.')

        with open('active_trades.txt', 'w') as file:
            for key, value in pair_state.items():
                if value == 'Deal':
                    file.write(key + ' ' + f'{start_deal_price[key]}' + ' ' + f'{tick_balance[key]}' + '\n')

        bot_error_logs(exp)
