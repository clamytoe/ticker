import pytest

from ticker.data import gather_all_data_async


@pytest.mark.asyncio
async def test_async_get_stock_info(monkeypatch):
    from ticker.data import async_get_stock_info

    def fake_get_stock_info(ticker):
        return {"symbol": ticker, "price": 100}

    monkeypatch.setattr("ticker.data.get_stock_info", fake_get_stock_info)
    result = await async_get_stock_info("AAPL")
    assert result["symbol"] == "AAPL"
    assert result["price"] == 100


@pytest.mark.asyncio
async def test_async_get_crypto_info(monkeypatch):
    from ticker.data import async_get_crypto_info

    def fake_get_crypto_info(ids):
        return {"BTC": {"symbol": "BTC", "price": 50000}}

    monkeypatch.setattr("ticker.data.get_crypto_info", fake_get_crypto_info)
    result = await async_get_crypto_info(["bitcoin"])
    assert "BTC" in result
    assert result["BTC"]["price"] == 50000


@pytest.mark.asyncio
async def test_gather_all_data_async(monkeypatch):
    monkeypatch.setattr("ticker.data.STOCKS", ["AAPL"])
    monkeypatch.setattr("ticker.data.CRYPTO", ["bitcoin"])
    monkeypatch.setattr("ticker.data.CRYPTO_KEYMAP", {"bitcoin": "BTC"})

    async def fake_async_get_stock_info(ticker):
        return {"symbol": ticker, "price": 100}

    async def fake_async_get_crypto_info(ids):
        return {"BTC": {"symbol": "BTC", "price": 50000}}

    monkeypatch.setattr("ticker.data.async_get_stock_info", fake_async_get_stock_info)
    monkeypatch.setattr("ticker.data.async_get_crypto_info", fake_async_get_crypto_info)

    result = await gather_all_data_async()
    assert "AAPL" in result
    assert "BTC" in result
    assert result["AAPL"]["price"] == 100
    assert result["BTC"]["price"] == 50000
