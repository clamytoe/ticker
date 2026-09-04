import yfinance as yf

from ticker.utils import fetch_logo, has_clearbit_logo


def get_stock_info(ticker):
    t = yf.Ticker(ticker)
    info = t.info
    price = info.get("regularMarketPrice", "0.00")
    prev_close = info.get("regularMarketPreviousClose", price)
    change = price - prev_close
    percent = (change / prev_close) * 100 if prev_close else 0
    name = info.get("longName", ticker)
    logo_url = f"https://logo.clearbit.com/{ticker.replace(' ', '').lower()}.com"
    if has_clearbit_logo(logo_url):
        logo_url = fetch_logo(ticker, logo_url)
    else:
        logo_url = (
            ticker.upper()
        )  # Clearbit logo not available, fallback to Ticker symbol
    symbol = ticker.upper()
    return {
        "symbol": symbol,
        "name": name,
        "price": price,
        "change": change,
        "percent": percent,
        "logo_url": logo_url,
    }
