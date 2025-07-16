#!/usr/bin/env python3
"""
app.py

Stock & Crypto Ticker App
"""
import threading
import time

import wx

from ticker.crypto import get_crypto_info
from ticker.stock import get_stock_info
from ticker.utils import url_to_wx_bitmap

STOCKS = [
    "ALAB",
    "ALZN",
    "AMD",
    "ELF",
    "HNST",
    "INTC",
    "MSTR",
    "MSTX",
    "NVDA",
    "NVDL",
    "PLTR",
    "SLXN",
    "SOFI",
    "SOUN",
    "SWIN",
    "VERB",
    "VST",
]
CRYPTO_KEYMAP = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "ripple": "XRP",
    "stellar": "XLM",
    "hedera": "HBAR",
    "shiba-inu": "SHIB",
}
CRYPTO = list(CRYPTO_KEYMAP)


class TickerPanel(wx.Panel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.SetBackgroundColour(wx.BLACK)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.update(data)

    def format_stock_display(self, info):
        pnl = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Logo
        bmp = (
            url_to_wx_bitmap(info["logo_url"])
            if info["logo_url"]
            else wx.Bitmap(48, 48)
        )
        logo = wx.StaticBitmap(pnl, bitmap=bmp)
        sizer.Add(logo, 0, wx.ALL, 2)
        # Text block
        textsizer = wx.BoxSizer(wx.VERTICAL)
        stock_name = wx.StaticText(pnl, label=info["name"])
        stock_name.SetForegroundColour(wx.WHITE)
        textsizer.Add(stock_name)
        # Line 2: Price, arrow, change
        up = "\u25b2"
        down = "\u25bc"
        symbol_arrow = up if info["change"] >= 0 else down
        color = wx.Colour(0, 200, 0) if info["change"] >= 0 else wx.Colour(200, 0, 0)
        line2 = wx.StaticText(
            pnl,
            label=f"${info['price']:.2f} {symbol_arrow} {info['change']:+.2f} ({info['percent']:+.2f}%)",
        )
        line2.SetForegroundColour(color)
        textsizer.Add(line2)
        sizer.Add(textsizer)
        pnl.SetSizer(sizer)
        return pnl

    def update(self, all_data):
        self.sizer.Clear(True)
        for _, info in all_data.items():
            pnl = self.format_stock_display(info)
            self.sizer.Add(pnl, 0, wx.ALL, 10)
        self.Layout()


class MainFrame(wx.Frame):
    def __init__(self, stock_data):
        super().__init__(
            None,
            title="Stock and Crypto Ticker",
            style=wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR,
        )
        self.SetSize((wx.DisplaySize()[0], 120))  # width of screen, height for ticker
        self.SetPosition((0, wx.DisplaySize()[1] - 120))
        panel = wx.Panel(self)
        self.ticker = TickerPanel(panel, stock_data)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self.ticker, 0, wx.EXPAND)
        panel.SetSizer(sizer)
        self.Show()


def gather_all_data():
    all_data = {}

    # Gather stock data
    for symbol in STOCKS:
        try:
            info = get_stock_info(symbol)
            if info:  # Only add if retrieval was successful
                all_data[symbol] = info
        except Exception as e:
            print(f"Error getting stock info for {symbol}: {e}")

    # Gather crypto data (batched for efficiency)
    try:
        crypto_data = get_crypto_info(CRYPTO)
        for cg_id, info in zip(
            CRYPTO, [crypto_data.get(CRYPTO_KEYMAP[cg_id], None) for cg_id in CRYPTO]
        ):
            if info:
                display_symbol = CRYPTO_KEYMAP[cg_id]  # BTC, ETH, etc.
                all_data[display_symbol] = info
    except Exception as e:
        print(f"Error getting crypto info: {e}")

    return all_data


def main():
    data = gather_all_data()
    app = wx.App(False)
    frame = MainFrame(data)
    app.MainLoop()


if __name__ == "__main__":
    main()
