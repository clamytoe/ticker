import asyncio

import wx

from ticker.data import gather_all_data_async
from ticker.ticker_panel import TickerPanel


class MainFrame(wx.Frame):
    def __init__(self, stock_data):
        style = wx.STAY_ON_TOP | wx.BORDER_NONE
        height = 120
        super().__init__(None, title="Stock & Crypto Ticker", style=style)  # FIXED
        geometry = self.get_leftmost_display_geometry()
        self.SetSize(wx.Size(geometry.width, height))
        self.SetPosition(wx.Point(geometry.x, geometry.y))

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
        self.SetWindowStyleFlag(wx.STAY_ON_TOP | wx.BORDER_NONE)
        self.Raise()

    @staticmethod
    def get_leftmost_display_geometry() -> wx.Rect:
        count = wx.Display.GetCount()
        leftmost = wx.Display(0).GetGeometry()
        min_y = float("inf")
        for i in range(1, count):
            geo = wx.Display(i).GetGeometry()
            total_width = leftmost.width
            if geo.x < leftmost.x:
                leftmost = geo
            if geo.x > leftmost.x:
                total_width = leftmost.width
        min_y = min(min_y, leftmost.y)
        return wx.Rect(0, int(min_y), total_width, 120)

    @staticmethod
    def get_display_geometry(index: int = 0) -> wx.Rect:
        count = wx.Display.GetCount()
        total_width = 0
        min_y = float("inf")
        for i in range(count):
            geo = wx.Display(i).GetGeometry()
            total_width += geo.width
            min_y = min(min_y, geo.y)
        return wx.Rect(0, int(min_y), total_width, 120)  # height is ticker height

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
