#!/usr/bin/env python3
"""
app.py

Stock & Crypto Ticker App
"""
import asyncio

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
    def __init__(self, parent, all_data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.SetBackgroundColour(wx.BLACK)
        self.all_data = list(all_data.values())
        self.scroll_x = 0
        self.ticker_height = 80
        self.ticker_spacing = 40
        self.ticker_items = self.prepare_ticker_items()
        self.scroll_speed = 2  # pixels per timer tick

        # Start timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(20)  # 50 fps

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, lambda e: self.Refresh())

    def prepare_ticker_items(self):
        """
        Prepare the info needed to render each ticker entry as a GDI+ bitmap.
        Pre-rendering is optional, but speeds up paint.
        """
        rendered_items = []
        for info in self.all_data:
            bmp = self.render_ticker_item(info)
            rendered_items.append(bmp)
        return rendered_items

    def render_ticker_item(self, info):
        """
        Render a single ticker entry to a wx.Bitmap and return it.
        """
        width = 300  # Arbitrary width, adjust as needed
        height = self.ticker_height
        bmp = wx.Bitmap(width, height)
        dc = wx.MemoryDC(bmp)
        dc.SetBackground(wx.Brush(wx.BLACK))
        dc.Clear()

        # Logo or ticker symbol
        if info.get("logo_url") and info["logo_url"].startswith("http"):
            icon_bmp = url_to_wx_bitmap(info["logo_url"], size=(48, 48))
            dc.DrawBitmap(icon_bmp, 5, (height - 48) // 2, True)
        else:
            # Draw symbol
            dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))
            dc.SetPen(wx.TRANSPARENT_PEN)
            rect = wx.Rect(5, (height - 48) // 2, 48, 48)
            dc.DrawRectangle(rect)
            dc.SetTextForeground(wx.WHITE)
            font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)  # type: ignore
            dc.SetFont(font)
            ticker = info.get("symbol", "")
            tw, th = dc.GetTextExtent(ticker)
            dc.DrawText(
                ticker,
                rect.x + (rect.width - tw) // 2,
                rect.y + (rect.height - th) // 2,
            )

        # Stock/Crypto name (top)
        dc.SetTextForeground(wx.WHITE)
        dc.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))  # type: ignore
        name = info.get("name", "")
        dc.DrawText(name, 60, 16)

        # Price and change (bottom)
        price = info.get("price", 0)
        up = "\u25b2"
        down = "\u25bc"
        arrow = up if info.get("change", 0) >= 0 else down
        chg = info.get("change", 0)
        perc = info.get("percent", 0)
        color = wx.Colour(0, 210, 0) if chg >= 0 else wx.Colour(230, 0, 0)
        dc.SetTextForeground(wx.WHITE)
        dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))  # type: ignore
        xoff = 60
        s1 = f"${price:,.2f} "
        tw, th = dc.GetTextExtent(s1)
        dc.DrawText(s1, xoff, 40)
        xoff += tw
        dc.SetTextForeground(color)
        dc.DrawText(arrow, xoff, 40)
        xoff += dc.GetTextExtent(arrow)[0] + 3
        dc.DrawText(f"{chg:+.2f}", xoff, 40)
        xoff += dc.GetTextExtent(f"{chg:+.2f}")[0] + 5
        dc.DrawText(f"({perc:+.2f}%)", xoff, 40)
        del dc
        return bmp

    def on_timer(self, evt):
        total_width = sum(
            bmp.GetWidth() + self.ticker_spacing for bmp in self.ticker_items
        )
        self.scroll_x = (self.scroll_x + self.scroll_speed) % total_width
        self.Refresh(False)

    def on_paint(self, evt):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        w, h = self.GetSize()
        y = (h - self.ticker_height) // 2

        # Scroll right-to-left
        x = -self.scroll_x
        i = 0
        while x < w:
            bmp = self.ticker_items[i % len(self.ticker_items)]
            gc.DrawBitmap(bmp, x, y, bmp.GetWidth(), bmp.GetHeight())
            x += bmp.GetWidth() + self.ticker_spacing
            i += 1


class MainFrame(wx.Frame):
    def __init__(self, stock_data):
        style = (
            wx.STAY_ON_TOP
            | wx.BORDER_NONE  # No border, no title bar, no frame decorations
        )
        height = 120
        wx.Frame.__init__(self, None, title="Stock & Crypto Ticker", style=style)
        self.SetSize((wx.DisplaySize()[0], height))  # type: ignore
        self.SetPosition((0, wx.DisplaySize()[1] - height))  # type: ignore

        panel = wx.Panel(self)
        self.ticker = TickerPanel(panel, stock_data)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ticker, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        # To handle hotkey or other close events
        self.Bind(wx.EVT_CHAR_HOOK, self.on_hotkey)
        self.Show()

    def on_hotkey(self, event):
        keycode = event.GetKeyCode()
        ctrl = event.CmdDown() or event.ControlDown()
        shift = event.ShiftDown()
        if ctrl and shift and (keycode == ord("C") or keycode == ord("c")):
            self.Close()
        else:
            event.Skip()


async def async_get_stock_info(ticker, loop=None):
    # Run sync code in a thread executor for compatibility
    return await asyncio.get_running_loop().run_in_executor(
        None, get_stock_info, ticker
    )


async def async_get_crypto_info(ids):
    # If get_crypto_info is sync, call it via executor as above
    return await asyncio.get_running_loop().run_in_executor(None, get_crypto_info, ids)


# Gather stocks concurrently
async def gather_all_data_async():
    stock_tasks = [async_get_stock_info(ticker) for ticker in STOCKS]
    stock_results = await asyncio.gather(*stock_tasks)

    # Get cryptos
    crypto_results = await async_get_crypto_info(CRYPTO)

    # Assemble all_data as before
    all_data = {info["symbol"]: info for info in stock_results if info}
    for cg_id in CRYPTO:
        display_symbol = CRYPTO_KEYMAP[cg_id]
        info = crypto_results.get(display_symbol)
        if info:
            all_data[display_symbol] = info
    return all_data


def main():
    data = asyncio.run(gather_all_data_async())
    app = wx.App(False)
    _ = MainFrame(data)
    app.MainLoop()


if __name__ == "__main__":
    main()
