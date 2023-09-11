import pandas as pd
from state import start_deal_price, deal_high, half_quantity
from orders import sell_order, sell_half_order


def state_tracker(symbol, price, volume, timestamp):
    if price > deal_high[symbol]:
        deal_high[symbol] = price
    if round(((price - start_deal_price[symbol]) / start_deal_price[symbol]) * 100, 4) >= 20:
        sell_order(symbol, price, timestamp)
        return None
    if round(((price - start_deal_price[symbol]) / start_deal_price[symbol]) * 100, 4) >= 10:
        if half_quantity[symbol] == 'Yes':
            return None
        sell_half_order(symbol, price, timestamp)
        return None

    price_difference = round(((deal_high[symbol] - price) / price) * 100, 4)

    if price_difference > 6.5:
        sell_order(symbol, price, timestamp)
