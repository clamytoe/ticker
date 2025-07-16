import yfinance as yf


def get_stock_info(ticker):
    t = yf.Ticker(ticker)
    info = t.info
    price: float = info.get("regularMarketPrice", "0.0")
    prev_close: float = info.get("regularMarketPreviousClose", price)
    change = price - prev_close
    percent = (change / prev_close) * 100 if prev_close else 0
    name = info.get("longName", ticker)
    return {
        "name": name,
        "price": price,
        "change": change,
        "percent": percent,
        "logo_url": info.get("logo_url", f"{ticker.upper()}"),
    }
