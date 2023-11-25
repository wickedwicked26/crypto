import pandas as pd
from state import start_deal_price, start_deal_time
from period import period_open_price
from orders import sell_order
from datetime import datetime, timedelta


def state_tracker(symbol, price, timestamp):

    validated_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
    validated_start_deal_time = datetime.strptime(start_deal_time[symbol], "%Y-%m-%d %H:%M")

    price_difference = round(((price - start_deal_price[symbol]) / start_deal_price[symbol]) * 100, 4)

    if price <= period_open_price[symbol] or price_difference <= -5:
        sell_order(symbol, price, timestamp)
        return None

    if price_difference >= 3:
        sell_order(symbol, price, timestamp)
        return None

    if validated_timestamp > validated_start_deal_time + timedelta(minutes=30):
        if price_difference >= 1:
            sell_order(symbol, price, timestamp)
            return None

