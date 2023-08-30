import requests


def get_tickers():
    response = requests.get('https://api.binance.com/api/v3/ticker/price')
    data = response.json()
    usdt_pairs = []
    for item in data:
        symbol = item["symbol"]
        if symbol.endswith("USDT"):
            usdt_pairs.append(symbol.lower() + "@kline_3m")

    return usdt_pairs


def get_volume():
    response = requests.get('https://api.binance.com/api/v3/ticker/price')
    data = response.json()
    usdt_pairs_volume = []
    for item in data:
        symbol = item["symbol"]
        if symbol.endswith("USDT"):
            usdt_pairs_volume.append(symbol.lower() + "@ticker")

    return usdt_pairs_volume

