# Stock & Crypto Ticker App (*ticker*)

> *A stock ticker strip that supports both stocks and cryptocurrencies.*

![Python version][python-version]
![Latest version][latest-version]
[![GitHub issues][issues-image]][issues-url]
[![GitHub forks][fork-image]][fork-url]
[![GitHub Stars][stars-image]][stars-url]
[![License][license-image]][license-url]

NOTE: This project was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with [@clamytoe's](https://github.com/clamytoe) [toepack](https://github.com/clamytoe/toepack) project template.

## Initial setup

```zsh
cd Projects
git clone https://github.com/clamytoe/ticker.git
cd ticker
```

### Anaconda setup

If you are an Anaconda user, this command will get you up to speed with the base installation.

```zsh
conda env create
conda activate ticker
```

### Regular Python setup

If you are just using normal Python, this will get you ready, but I highly recommend that you do this in a virtual environment.
There are many ways to do this, the simplest using *venv*.

```zsh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Final setup

```zsh
pip install -e .
```

## Usage

```zsh
ticker
```

If all went well, you should be seeing a ticker strip near the bottom of your screen.

![ticker_ribbon](images/ticker_ribbon.png)

## Configuring

Edit the `portfolio.json` file to add or remove stocks and cryptocurrencies.
As of this version, you must have at least one of each.

```json
{
    "stocks": [
        "AMD",
        "INTC",
        "NVDA",
        "PLTR",
        "SOFI"
    ],
    "crypto_keymap": {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "ripple": "XRP"
    }
}
```

## Contributing

Contributions are welcomed.
Tests can be run with with `pytest -v`, please ensure that all tests are passing and that you've checked your code with the following packages before submitting a pull request:

* black
* flake8
* isort
* mypy
* pytest-cov

I am not adhering to them strictly, but try to clean up what's reasonable.

## License

Distributed under the terms of the [MIT](https://opensource.org/licenses/MIT) license, "ticker" is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://github.com/clamytoe/toepack/issues) along with a detailed description.

## Changelog

* **v0.1.0** Initial commit.

[python-version]:https://img.shields.io/badge/python-3.13.3-brightgreen.svg
[latest-version]:https://img.shields.io/badge/version-0.1.0-blue.svg
[issues-image]:https://img.shields.io/github/issues/clamytoe/ticker.svg
[issues-url]:https://github.com/clamytoe/ticker/issues
[fork-image]:https://img.shields.io/github/forks/clamytoe/ticker.svg
[fork-url]:https://github.com/clamytoe/ticker/network
[stars-image]:https://img.shields.io/github/stars/clamytoe/ticker.svg
[stars-url]:https://github.com/clamytoe/ticker/stargazers
[license-image]:https://img.shields.io/github/license/clamytoe/ticker.svg
[license-url]:https://github.com/clamytoe/ticker/blob/main/LICENSE
