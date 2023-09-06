import pandas as pd
from state import start_deal_price, deal_high
from orders import sell_order, sell_half_order


def state_tracker(symbol, price, volume, timestamp):

    if price > deal_high[symbol]:
        deal_high[symbol] = price
    if round(((start_deal_price[symbol] - price) / price) * 100, 4) >= 20:
        sell_order(symbol, price, timestamp)
        return None
    if round(((start_deal_price[symbol] - price) / price) * 100, 4) >= 10:
        sell_half_order(symbol, price, timestamp)

    price_difference = round(((deal_high[symbol] - price) / price) * 100, 4)

    if price_difference > 6.5:
        sell_order(symbol, price, timestamp)
