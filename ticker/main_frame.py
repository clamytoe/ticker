import asyncio

import wx

from ticker.data import gather_all_data_async
from ticker.ticker_panel import TickerPanel


class MainFrame(wx.Frame):
    def __init__(self, stock_data):
        style = wx.STAY_ON_TOP | wx.BORDER_NONE
        height = 120
        super().__init__(None, title="Stock & Crypto Ticker", style=style)  # FIXED
        self.SetSize((wx.DisplaySize()[0], height))  # type: ignore
        self.SetPosition((0, wx.DisplaySize()[1] - height))  # type: ignore

        panel = wx.Panel(self)
        self.ticker = TickerPanel(panel, stock_data)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ticker, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CHAR_HOOK, self.on_hotkey)
        self.SetTransparent(200)  # 0=fully transparent, 255=opaque
        self.Show()

        self.refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_refresh_timer, self.refresh_timer)
        self.refresh_timer.Start(60000)  # 60,000 ms = 1 minute

    def on_hotkey(self, event):
        keycode = event.GetKeyCode()
        ctrl = event.CmdDown() or event.ControlDown()
        shift = event.ShiftDown()
        if ctrl and shift and (keycode == ord("C") or keycode == ord("c")):
            self.Close()
        else:
            event.Skip()

    def on_refresh_timer(self, event):
        # Run async function synchronously
        new_data = asyncio.run(gather_all_data_async())
        self.ticker.all_data = list(new_data.values())
        self.ticker.ticker_items = self.ticker.prepare_ticker_items()
        self.ticker.Refresh()

    async def refresh_data(self):
        new_data = await gather_all_data_async()
        self.ticker.all_data = list(new_data.values())
        self.ticker.ticker_items = self.ticker.prepare_ticker_items()
        self.ticker.Refresh()
