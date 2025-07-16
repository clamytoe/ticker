import json
import os


def test_load_config():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "portfolio.json"
    )
    assert os.path.exists(config_path)
    with open(config_path) as f:
        config = json.load(f)
    assert "stocks" in config
    assert "crypto_keymap" in config
    assert isinstance(config["stocks"], list)
    assert isinstance(config["crypto_keymap"], dict)
