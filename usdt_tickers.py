import requests


def get_tickers():
    response = requests.get('https://api.binance.com/api/v3/ticker/price')
    data = response.json()
    usdt_pairs = []
    for item in data:
        symbol = item["symbol"]
        if symbol.endswith("USDT"):
            if symbol == 'BTTCUSDT':
                continue
            usdt_pairs.append(symbol.lower() + "@kline_1m")

    return usdt_pairs


def get_ticks():
    response = requests.get('https://api.binance.com/api/v3/ticker/price')
    data = response.json()
    usdt_ticks = []
    for item in data:
        symbol = item["symbol"]
        if symbol.endswith("USDT"):
            usdt_ticks.append(symbol.lower() + "@ticker")

    return usdt_ticks

