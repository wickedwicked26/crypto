import pandas as pd
from state import start_deal_price, deal_high
from orders import sell_order, sell_half_order


def state_tracker(symbol, price, volume, timestamp):
    if round(((start_deal_price[symbol] - price) / price) * 100, 4) >= 20:
        sell_order(symbol, price, timestamp)

    if round(((start_deal_price[symbol] - price) / price) * 100, 4) >= 10:
        sell_half_order(symbol, price, timestamp)
    if price > deal_high[symbol]:
        deal_high[symbol] = price

        return None

    price_difference = round(((deal_high[symbol] - price) / price) * 100, 4)
    # print(f'price:{price} high:{deal_high[symbol]} diff: {price_difference}')

    if price_difference > 6.5:
        sell_order(symbol, price, timestamp)
