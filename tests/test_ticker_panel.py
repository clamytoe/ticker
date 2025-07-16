import wx

from ticker.ticker_panel import TickerPanel


def test_prepare_ticker_items():
    app = wx.App(False)
    frame = wx.Frame(None)
    data = {
        "BTC": {"name": "Bitcoin", "price": 120000, "symbol": "BTC"},
        "ETH": {"name": "Ethereum", "price": 3000, "symbol": "ETH"},
    }
    panel = TickerPanel(frame, data)
    items = panel.prepare_ticker_items()
    assert isinstance(items, list)
    assert all(isinstance(item, wx.Bitmap) for item in items)
    panel.Destroy()
    frame.Destroy()
    app.Destroy()
