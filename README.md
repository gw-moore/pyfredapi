# pyfredapi - Python client for the Federal Reserve Economic Data (FRED) API
<!-- badges: start -->

[![PyPi Version](https://img.shields.io/pypi/v/pyfredapi.svg)](https://pypi.python.org/pypi/pyfredapi/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyfredapi)](https://pypi.python.org/pypi/pyfredapi)
[![Documentation Status](https://readthedocs.org/projects/pyfredapi/badge/?version=latest)](https://pyfredapi.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<!-- badges: end -->

`pyfredapi` is a Python client for the [FRED API web service](https://fred.stlouisfed.org/docs/api/fred/). `pyfredapi` covers all the FRED api endpoints and can return data as a [pandas](https://pandas.pydata.org/) dataframe or json. Checkout the [docs](https://pyfredapi.readthedocs.io/en/latest/) to learn more.

## Installation

```bash
pip install pyfredapi
```

## Basic Usage

Before using `pyfredapi` and must have an API key to the FRED API web service. You can apply for [one for free](https://fred.stlouisfed.org/docs/api/api_key.html) on the FRED website.

You can either be set as the environment variable `FRED_API_KEY`, or pass it to the `api_key` parameters when initializing `pyfredapi`.

```python
from pyfredapi import FredSeries

# api key set as environment variable
client = FredSeries()

# api key passed to initializer
client = FredSeries(api_key = "my_api_key")

# get GDP data
client.get_series("GDP")
```
