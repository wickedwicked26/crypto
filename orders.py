import csv
from datetime import timedelta, datetime
from state import pair_state, start_deal_price, deal_time, tick_balance, last_deal_time, deal_high, half_quantity, \
    usdt_start_deal_balance
from telegram_message import send_message
from config import client


def buy_order(symbol, price, timestamp):
    total_amount_usd = 100
    quantity = total_amount_usd / price

    usdt_balance = float(client.get_asset_balance('USDT')['free'])
    usdt_start_deal_balance['balance'] = usdt_balance

    order = client.create_order(
        symbol=symbol,
        side=client.SIDE_BUY,
        type=client.ORDER_TYPE_MARKET,
        quantity=str(quantity)
    )

    symb_balance = float(client.get_asset_balance(f'{symbol[:-4]}')['free'])
    tick_balance[symbol] = symb_balance

    pair_state[symbol] = 'Deal'
    start_deal_price[symbol] = price
    deal_time[symbol] = timestamp
    deal_high[symbol] = price
    send_message(
        f'{symbol} : DEAL STARTED\n'
        f'PRICE : {price}\n'
        f'TIMESTAMP: {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}\n'
        f'{symbol} QUANTITY : {tick_balance[symbol]}\n'
        f'USDT BALANCE : {usdt_balance - 100}\n'
    )


def sell_order(symbol, price, timestamp):
    quantity = tick_balance[symbol]

    order = client.create_order(
        symbol=symbol,
        side=client.SIDE_SELL,
        type=client.ORDER_TYPE_MARKET,
        quantity=str(quantity)
    )
    usdt_balance = float(client.get_asset_balance('USDT')['free'])
    start_balance = usdt_start_deal_balance["balance"]
    usdt_change = round(((usdt_balance - start_balance) / start_balance) * 100, 4)
    send_message(f'{symbol} : DEAL FINISHED\n'
                 f'USDT BALANCE : {usdt_balance}\n'
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
    pair_state[symbol] = 'Not in deal'
    half_quantity[symbol] = 'No'
    start_deal_price[symbol] = 0
    deal_time[symbol] = 0
    last_deal_time[symbol] = timestamp
    tick_balance[symbol] = 0
    usdt_start_deal_balance['balance'] = 0
    deal_high[symbol] = 0


def sell_half_order(symbol, price, timestamp):
    quantity = tick_balance[symbol] / 2

    order = client.create_order(
        symbol=symbol,
        side=client.SIDE_SELL,
        type=client.ORDER_TYPE_MARKET,
        quantity=str(quantity)
    )

    symb_balance = float(client.get_asset_balance(f'{symbol[:-4]}')['free'])
    tick_balance[symbol] = symb_balance

    deal_result = round(((price - start_deal_price[symbol]) / start_deal_price[symbol]) * 100, 4)
    half_quantity[symbol] = 'Yes'
    send_message(f'{symbol} : HALF QUANTITY SOLD\n'
                 f'PRICE GROW: {deal_result}%\n'
                 f'TIMESTAMP : {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}')
