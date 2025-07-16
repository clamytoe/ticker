import os

import pytest
import wx

from ticker.main_frame import MainFrame


@pytest.mark.skipif("DISPLAY" not in os.environ, reason="Requires X server")
def test_main_frame_creation():
    app = wx.App(False)
    frame = MainFrame({"BTC": {"name": "Bitcoin", "price": 120000}})
    assert frame.IsShown()
    frame.Destroy()
    app.Destroy()


def test_on_hotkey_closes(monkeypatch):
    import wx

    from ticker.main_frame import MainFrame

    app = wx.App(False)
    frame = MainFrame({})
    event = wx.KeyEvent(wx.wxEVT_CHAR_HOOK)
    event.SetKeyCode(ord("C"))
    event.SetControlDown(True)
    event.SetShiftDown(True)
    frame.on_hotkey(event)
    assert not frame.IsShown()
    frame.Destroy()
    app.Destroy()
