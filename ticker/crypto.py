from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def get_crypto_info(ids):
    # ids: list of CoinGecko IDs (e.g., 'bitcoin')
    market = cg.get_coins_markets(vs_currency="usd", ids=ids)
    result = {}
    for coin in market:
        name = coin["name"]
        price = coin["current_price"]
        change = coin["price_change_24h"]
        percent = coin["price_change_percentage_24h"]
        logo_url = coin.get("image")
        symbol = coin["symbol"].upper()
        result[symbol] = {
            "name": name,
            "price": price,
            "change": change,
            "percent": percent,
            "logo_url": logo_url,
        }
    return result
