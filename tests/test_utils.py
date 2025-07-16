import os

from ticker.utils import fetch_logo


def test_fetch_logo_bad_url(tmp_path):
    # Use a guaranteed bad URL
    url = "http://invalid.url/image.png"
    ticker = "BTC"
    cache_dir = tmp_path / "logo_cache"
    result = fetch_logo(ticker, url, cache_dir=str(cache_dir))
    # Should return None for a bad URL
    assert result is None


def test_fetch_logo_cache(tmp_path):
    # Simulate an existing cache file
    ticker = "BTC"
    cache_dir = tmp_path / "logo_cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = cache_dir / f"{ticker}.png"
    cache_path.write_bytes(b"fake image data")
    result = fetch_logo(
        ticker, "http://doesnotmatter.com/image.png", cache_dir=str(cache_dir)
    )
    # Should return the cache path
    assert result == str(cache_path)
