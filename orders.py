import csv
import json
from datetime import timedelta, datetime
import requests
from binance.exceptions import BinanceAPIException

from error_logs import binance_error_logs
from period import period_data, current_open, data, period_open_price
from state import pair_state, start_deal_price, start_deal_time, tick_balance, last_deal_time, \
    usdt_start_deal_balance, deal, start_time_for_data_base
from telegram_message import send_message, send_error
from config import client
from decimal import Decimal
from binance.helpers import round_step_size
from state import usdt_balance, step_size


def buy_order(symbol, price, timestamp, period_open):
    usdt_bal = float(client.get_asset_balance('USDT')['free'])

    if usdt_bal < 50:
        return None
    total_amount_usd = 15
    # if usdt_bal >= 1_000:
    #     total_amount_usd = 1_000
    # else:
    #     total_amount_usd = usdt_bal
    usdt_start_deal_balance[symbol] = total_amount_usd
    try:
        order = client.order_market_buy(
            symbol=symbol,
            quoteOrderQty=total_amount_usd,
        )
    except BinanceAPIException as exception:
        binance_error_logs(exception)
        send_error(f'[INFO] BINANCE EXCEPTION:\n{exception}')
        return

    deal['deal'] = True
    pair_state[symbol] = True
    start_deal_price[symbol] = price
    tick_balance[symbol] = Decimal(client.get_asset_balance(f'{symbol[:-4]}')['free'])
    period_open_price[symbol] = period_open
    start_deal_time[symbol] = timestamp
    usdt_start_deal_balance[symbol] = total_amount_usd
    step_size[symbol] = get_step_size(symbol)
    start_time_for_data_base[symbol] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open('/root/project/open_deals_data.json', 'r+') as json_file:
            open_deal_data = json.load(json_file)
            open_deal_data['Module 1'].update({
                'Open deal': symbol,
                'Start deal price': start_deal_price.get(symbol, 0),
                'Balance': str(tick_balance.get(symbol, 0)),
                'Period open price': period_open_price.get(symbol, 0),
                'Start deal time': start_deal_time.get(symbol, 0),
                'Usdt quantity': usdt_start_deal_balance.get(symbol, 0),
                'Step size': str(step_size.get(symbol, 0)),
                'Start time for database': start_time_for_data_base.get(symbol, 0)
            })
            json_file.seek(0)
            json.dump(open_deal_data, json_file, indent=4)
    except Exception as e:
        send_error(f'[ERROR] OPEN DEALS DATA FILE ERROR:\n{e}')
        pass

    send_message(
        f'{symbol} : DEAL STARTED\n'
        f'PERIOD OPEN PRICE : {current_open[symbol]}'
        f'PRICE : {price}\n'
        f'TIMESTAMP: {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}\n'
        f'{symbol} QUANTITY : {tick_balance[symbol]}\n'
        f'{total_amount_usd}$ DEAL\n'
    )


def sell_order(symbol, price, timestamp):
    symbol_balance = tick_balance[symbol]

    step_size_ = step_size[symbol]

    quantity = round_step_size(symbol_balance, step_size_)
    try:
        order = client.order_market_sell(
            symbol=symbol,
            quantity=quantity
        )

    except BinanceAPIException as exception:
        binance_error_logs(exception)
        send_error(f'[INFO] BINANCE EXCEPTION:\n{exception}')
        return

    final_balance = float(order['cummulativeQuoteQty'])
    final_balance = float(58.48)
    start_balance = usdt_start_deal_balance[symbol]
    usdt_change = round(((final_balance - start_balance) / start_balance) * 100, 4)

    send_message(f'{symbol} : DEAL FINISHED\n'
                 f'USDT CHANGE : {usdt_change}%\n'
                 f'DEAL START PRICE: {start_deal_price[symbol]}\n'
                 f'DEAL END PRICE: {price}\n'
                 f'DEAL START : {datetime.strptime(start_deal_time[symbol], "%Y-%m-%d %H:%M") + timedelta(hours=3)}\n'
                 f'DEAL FINISHED: {datetime.strptime(timestamp, "%Y-%m-%d %H:%M") + timedelta(hours=3)}')

    try:
        with open('/root/project/open_deals_data.json', 'r') as json_file:
            open_deal_data = json.load(json_file)

        open_deal_data['Module 1'].update({
            'Open deal': 0,
            'Start deal price': 0,
            'Balance': 0,
            'Period open price': 0,
            'Start deal time': 0,
            'Usdt quantity': 0,
            'Step size': 0,
            'Start time for database': 0
        })
        with open('/root/project/open_deals_data.json', 'w') as json_file:
            json.dump(open_deal_data, json_file, indent=4)

    except Exception as e:
        send_error(f'[ERROR] OPEN DEALS DATA FILE ERROR:\n{e}')
        pass

    with open('/root/project/data_base.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((
            symbol,
            start_time_for_data_base[symbol],
            start_deal_price[symbol],
            timestamp,
            price,
            usdt_change
        ))

    validate_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")

    deal['deal'] = False
    pair_state[symbol] = False
    last_deal_time[symbol] = validate_timestamp
    usdt_balance['symbol'] = float(client.get_asset_balance('USDT')['free'])
    period_data[symbol] = []
    current_open[symbol] = 0

    for item in data:
        symbol = item['symbol']
        if symbol.endswith('USDT'):
            current_open[symbol] = 0

    for item in data:
        symbol = item['symbol']
        if symbol.endswith('USDT'):
            period_data[symbol] = []


def get_step_size(symbol):
    url = f'https://api.binance.com/api/v1/exchangeInfo'
    response = requests.get(url)
    data = response.json()
    size = 0
    for symbol_info in data['symbols']:
        if symbol_info['symbol'] == symbol:
            for filter_item in symbol_info['filters']:
                if filter_item['filterType'] == 'LOT_SIZE':
                    size = Decimal(filter_item['stepSize'])
                    break
    return size
