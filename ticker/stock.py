import yfinance as yf


def get_stock_info(ticker):
    t = yf.Ticker(ticker)
    info = t.info
    price = info.get("regularMarketPrice")
    prev_close = info.get("regularMarketPreviousClose", price)
    change = price - prev_close
    percent = (change / prev_close) * 100 if prev_close else 0
    name = info.get("longName", ticker)
    logo_url = info.get("logo_url")
    symbol = ticker.upper()
    if not logo_url:
        logo_url = None  # or symbol, but now app uses symbol as fallback if no logo_url
    return {
        "symbol": symbol,
        "name": name,
        "price": price,
        "change": change,
        "percent": percent,
        "logo_url": logo_url,
    }
