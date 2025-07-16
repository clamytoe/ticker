from io import BytesIO

import requests
import wx
from PIL import Image


def has_clearbit_logo(url):
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code != 200:
            return False  # Not found or error

        # Check if payload is very small (common for blank PNGs)
        if len(resp.content) < 150:
            return False

        # Optionally: check if all pixels are transparent with PIL
        img = Image.open(BytesIO(resp.content)).convert("RGBA")
        if all(pixel[3] == 0 for pixel in img.getdata()):
            return False  # Fully transparent image

        return True
    except Exception:
        return False


def url_to_wx_bitmap(url, size=(48, 48)):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).resize(size)
        return wx.Bitmap.FromBuffer(*image.size, image.convert("RGB").tobytes())
    except Exception:
        return wx.Bitmap(size[0], size[1])  # Fallback empty bitmap
