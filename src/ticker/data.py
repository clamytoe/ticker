import asyncio
import json
import os

from ticker.crypto import get_crypto_info
from ticker.stock import get_stock_info

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "portfolio.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)
STOCKS = config["stocks"]
CRYPTO_KEYMAP = config["crypto_keymap"]
CRYPTO = list(CRYPTO_KEYMAP)


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
