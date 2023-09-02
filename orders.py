from datetime import timedelta, datetime

from binance import Client
from state import pair_state, start_deal_price, pair_day_volume, deal_time, usdt_balance
from telegram_message import send_graph, send_message
import os
from config import client


def buy_order(symbol, price, timestamp):
    # total_amount_usd = 10_000
    # quantity = total_amount_usd / price
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
    pair_state[symbol] = 'Deal'
    start_deal_price[symbol] = price
    deal_time[symbol] = timestamp

    send_message(
        f'{symbol} : DEAL STARTED\n'
        f'PRICE : {price}\n'
        f'TIMESTAMP: {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}')


def sell_order(symbol, price, timestamp):
    # total_amount_usd = 10_000
    # quantity = total_amount_usd / price
    #
    # order = client.create_order(
    #     symbol=symbol,
    #     side=Client.SIDE_SELL,
    #     type=Client.ORDER_TYPE_MARKET,
    #     quantity=str(quantity)
    # )

    send_message(f'{symbol} : DEAL FINISHED\n'
                 f'RESULT: {((price - start_deal_price[symbol]) / start_deal_price[symbol]) * 100}%\n'
                 f'DEAL START PRICE: {start_deal_price[symbol]}\n'
                 f'DEAL END PRICE: {price}\n'
                 f'DEAL START : {datetime.strptime(deal_time[symbol], "%Y-%m-%d %H:%M") + timedelta(hours=3)}'
                 f'DEAL FINISHED: {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}')
    pair_state[symbol] = 'Not in deal'
    start_deal_price[symbol] = 0
    deal_time[symbol] = 0
