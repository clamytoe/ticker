from io import BytesIO

import requests
import wx
from PIL import Image


def url_to_wx_bitmap(url, size=(48, 48)):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).resize(size)
        return wx.Bitmap.FromBuffer(*image.size, image.convert("RGB").tobytes())
    except Exception:
        return wx.Bitmap(size[0], size[1])  # Fallback empty bitmap
