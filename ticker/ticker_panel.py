import wx

from ticker.utils import get_logo_bitmap


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
        if info.get("logo_url") and info["logo_url"].startswith("logo_cache"):
            icon_bmp = get_logo_bitmap(info["logo_url"])
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
