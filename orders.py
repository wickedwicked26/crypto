import csv
from datetime import timedelta, datetime
import requests

from period import period_data, current_open
from state import pair_state, start_deal_price, deal_time, tick_balance, last_deal_time, deal_high, \
    usdt_start_deal_balance, deal
from telegram_message import send_message
from config import client
from decimal import Decimal
from binance.helpers import round_step_size
from state import usdt_balance


def buy_order(symbol, price, timestamp):
    usdt_bal = usdt_balance['symbol']
    if usdt_bal < 10:
        return None
    total_amount_usd = 10
    # if usdt_bal >= 1_000:
    #     total_amount_usd = 1_000
    # else:
    #     total_amount_usd = usdt_bal
    usdt_start_deal_balance[symbol] = total_amount_usd

    order = client.order_market_buy(
        symbol=symbol,
        quoteOrderQty=total_amount_usd,
    )

    symb_balance = Decimal(client.get_asset_balance(f'{symbol[:-4]}')['free'])
    tick_balance[symbol] = symb_balance
    usdt_start_deal_balance[symbol] = total_amount_usd

    deal['deal'] = True
    pair_state[symbol] = True
    start_deal_price[symbol] = price
    deal_time[symbol] = timestamp
    deal_high[symbol] = price
    send_message(
        f'{symbol} : DEAL STARTED\n'
        f'PRICE : {price}\n'
        f'TIMESTAMP: {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}\n'
        f'{symbol} QUANTITY : {tick_balance[symbol]}\n'
        f'{total_amount_usd}$ DEAL\n'
    )
    usdt_balance['symbol'] = float(client.get_asset_balance('USDT')['free'])


def sell_order(symbol, price, timestamp):
    symb_balance = tick_balance[symbol]
    step_size = 0
    url = f'https://api.binance.com/api/v1/exchangeInfo'
    response = requests.get(url)
    data = response.json()
    step_size = 0
    for symbol_info in data['symbols']:
        if symbol_info['symbol'] == symbol:
            for filter_item in symbol_info['filters']:
                if filter_item['filterType'] == 'LOT_SIZE':
                    step_size = Decimal(filter_item['stepSize'])

    quantity = round_step_size(symb_balance, step_size)

    order = client.order_market_sell(
        symbol=symbol,
        quantity=quantity
    )

    final_balance = float(order['cummulativeQuoteQty'])
    start_balance = usdt_start_deal_balance[symbol]
    usdt_change = round(((final_balance - start_balance) / start_balance) * 100, 4)
    send_message(f'{symbol} : DEAL FINISHED\n'
                 f'USDT CHANGE : {usdt_change}%\n'
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
            usdt_change
        ))

    deal['deal'] = False
    pair_state[symbol] = False
    start_deal_price[symbol] = 0
    deal_time[symbol] = 0
    last_deal_time[symbol] = timestamp
    tick_balance[symbol] = 0
    usdt_start_deal_balance[symbol] = 0
    deal_high[symbol] = 0
    usdt_balance['symbol'] = float(client.get_asset_balance('USDT')['free'])
    period_data[symbol] = []
    current_open[symbol] = 0

start = datetime.now()
symbol = 'BTCUSDT'
url = f'https://api.binance.com/api/v1/exchangeInfo'
response = requests.get(url)
data = response.json()
step_size = 0
for symbol_info in data['symbols']:
    if symbol_info['symbol'] == symbol:
        for filter_item in symbol_info['filters']:
            if filter_item['filterType'] == 'LOT_SIZE':
                step_size = Decimal(filter_item['stepSize'])

