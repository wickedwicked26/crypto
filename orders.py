import csv
from datetime import timedelta, datetime

from binance import Client
from state import pair_state, start_deal_price, pair_day_volume, deal_time, tick_balance, last_deal_time
from telegram_message import send_graph, send_message
import os
from config import client

usdt_balance = 10_000


def buy_order(symbol, price, timestamp):
    global usdt_balance
    total_amount_usd = 10_000
    quantity = total_amount_usd / price

    tick_balance[symbol] = total_amount_usd / price
    usdt_balance -= total_amount_usd
    # account_info = client.get_account()
    #
    # for balance in account_info['balances']:
    #     if balance['asset'] == 'USDT':
    #         usdt_balance = float(balance['free'])
    #
    #         break
    # order = client.create_order(
    #     symbol=symbol,
    #     side=Client.SIDE_BUY,
    #     type=Client.ORDER_TYPE_MARKET,
    #     quantity=quantity
    # )
    # account_info = client.get_account()
    # for balance in account_info['balances']:
    #     if balance['asset'] == f'{symbol[:-4]}':
    #         tick_balance[symbol] = float(balance['free'])
    pair_state[symbol] = 'Deal'
    start_deal_price[symbol] = price
    deal_time[symbol] = timestamp

    send_message(
        f'{symbol} : DEAL STARTED\n'
        f'PRICE : {price}\n'
        f'TIMESTAMP: {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}\n'
        f'{symbol} QUANTITY : {tick_balance[symbol]}\n'
        f'USDT BALANCE : {usdt_balance}\n'
    )


def sell_order(symbol, price, timestamp):
    # total_amount_usd = 10_000
    global usdt_balance
    quantity = tick_balance[symbol]
    #
    # order = client.create_order(
    #     symbol=symbol,
    #     side=Client.SIDE_SELL,
    #     type=Client.ORDER_TYPE_MARKET,
    #     quantity=str(quantity)
    # )
    usdt_balance += quantity * price
    deal_result = ((price - start_deal_price[symbol]) / start_deal_price[symbol]) * 100
    send_message(f'{symbol} : DEAL FINISHED\n'
                 f'USDT BALANCE : {usdt_balance}\n'
                 f'USDT BALANCE CHANGE : {round(((usdt_balance - 10_000) / 10_000) * 100, 4)}\n'
                 f'RESULT: {deal_result}%\n'
                 f'DEAL START PRICE: {start_deal_price[symbol]}\n'
                 f'DEAL END PRICE: {price}\n'
                 f'DEAL START : {datetime.strptime(deal_time[symbol], "%Y-%m-%d %H:%M") + timedelta(hours=3)}\n'
                 f'DEAL FINISHED: {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}'
                 )
    with open('data_base.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((
            symbol,
            deal_time[symbol],
            start_deal_price[symbol],
            timestamp,
            price,
            deal_result
        ))
    pair_state[symbol] = 'Not in deal'
    start_deal_price[symbol] = 0
    deal_time[symbol] = 0
    last_deal_time[symbol] = timestamp
    tick_balance[symbol] = 0


def sell_half_order(symbol, price, timestamp):
    global usdt_balance
    quantity = tick_balance[symbol] / 2
    tick_balance[symbol] = tick_balance[symbol] / 2
    usdt_balance += quantity * price
    deal_result = ((price - start_deal_price[symbol]) / start_deal_price[symbol]) * 100

    # order = client.create_order(
    #     symbol=symbol,
    #     side=Client.SIDE_SELL,
    #     type=Client.ORDER_TYPE_MARKET,
    #     quantity=str(quantity)
    # )
    send_message(f'{symbol} : HALF QUANTITY SOLD\n'
                 f'USDT BALANCE : {usdt_balance}'
                 f'RESULT: {deal_result}%\n'
                 f'TIMESTAMP : {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}')
