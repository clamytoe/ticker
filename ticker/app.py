#!/usr/bin/env python3
import asyncio

import wx

from ticker.data import gather_all_data_async
from ticker.main_frame import MainFrame


def main():
    data = asyncio.run(gather_all_data_async())
    app = wx.App(False)
    _ = MainFrame(data)
    app.MainLoop()


if __name__ == "__main__":
    main()
