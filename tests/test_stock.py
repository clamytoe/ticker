from ticker.stock import get_stock_info


def test_get_stock_info_returns_dict():
    result = get_stock_info("AAPL")
    assert isinstance(result, dict)
