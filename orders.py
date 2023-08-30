from binance import Client
from state import pair_state, start_deal_price, pair_day_volume, deal_time, usdt_balance
from telegram_message import send_graph, path
from graphs import start_graph, finish_graph
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

    start_graph(symbol, timestamp)
    send_graph(symbol, timestamp, f'DEAL STARTED\nPRICE : {price}\nTIMESTAMP: {timestamp}')
    os.remove(f'{symbol}_{timestamp}.png')


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

    finish_graph(symbol, timestamp, deal_time[symbol])
    send_graph(symbol, timestamp, f'DEAL FINISHED\n'
                                  f'RESULT: {((price - start_deal_price[symbol]) / start_deal_price[symbol]) * 100}%\n'
                                  f'DEAL STARTED: {start_deal_price[symbol]}\n'
                                  f'DEAL FINISHED: {timestamp}\n')
    pair_state[symbol] = 'Not in deal'
    start_deal_price[symbol] = 0
    deal_time[symbol] = 0
    os.remove(f'{symbol}_{timestamp}.png')
