import os
from io import BytesIO

import requests
import wx
from PIL import Image


def fetch_logo(ticker, url, cache_dir="logo_cache"):
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{ticker.upper()}.png")
    if os.path.exists(cache_path):
        return cache_path
    try:
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200 and resp.content and len(resp.content) > 150:
            with open(cache_path, "wb") as f:
                f.write(resp.content)
            return cache_path
    except Exception:
        pass
    return None


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


def get_logo_bitmap(logo_source, size=(48, 48)):
    if logo_source.startswith("http"):
        return url_to_wx_bitmap(logo_source, size)
    else:
        # Assume local file path
        return local_path_to_wx_bitmap(logo_source, size)


def local_path_to_wx_bitmap(path, size=(48, 48)):
    # Load image file as wx.Image. Format will be detected automatically.
    img = wx.Image(path, wx.BITMAP_TYPE_ANY)
    # Resize if needed
    img = img.Scale(size[0], size[1], wx.IMAGE_QUALITY_HIGH)
    # Convert to wx.Bitmap for display
    bmp = wx.Bitmap(img)
    return bmp


def url_to_wx_bitmap(url, size=(48, 48)):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).resize(size)
        return wx.Bitmap.FromBuffer(*image.size, image.convert("RGB").tobytes())
    except Exception:
        return wx.Bitmap(size[0], size[1])  # Fallback empty bitmap
