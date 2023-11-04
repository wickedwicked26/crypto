import pandas as pd
from state import start_deal_price, deal_high
from orders import sell_order


def state_tracker(symbol, price, timestamp):
    if price > deal_high[symbol]:
        deal_high[symbol] = price
    sell_order(symbol, price, timestamp)
    price_difference = round(((price - start_deal_price[symbol]) / start_deal_price[symbol]) * 100, 4)

    if price_difference >= 5 or price <= start_deal_price[symbol]:
        sell_order(symbol, price, timestamp)
