from unittest.mock import patch

from ticker.crypto import get_crypto_info


@patch("ticker.crypto.cg.get_coins_markets")
@patch("ticker.crypto.fetch_logo", return_value="http://logo.url")
def test_get_crypto_info_basic(mock_logo, mock_markets):
    mock_markets.return_value = [
        {
            "name": "Bitcoin",
            "current_price": 120000,
            "price_change_24h": 1000,
            "price_change_percentage_24h": 1.7,
            "image": "http://image.url",
            "symbol": "btc",
        }
    ]
    result = get_crypto_info(["bitcoin"])
    assert "BTC" in result
    assert result["BTC"]["name"] == "Bitcoin"
    assert result["BTC"]["price"] == 120000
    assert result["BTC"]["logo_url"] == "http://logo.url"


@patch("ticker.crypto.cg.get_coins_markets", return_value=[])
def test_get_crypto_info_empty(mock_markets):
    result = get_crypto_info([])
    assert result == {}
