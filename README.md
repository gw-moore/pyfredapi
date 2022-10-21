# pyfredapi - Python library for the Federal Reserve Economic Data (FRED) API
<!-- badges: start -->

[![PyPi Version](https://img.shields.io/pypi/v/pyfredapi.svg)](https://pypi.python.org/pypi/pyfredapi/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyfredapi)](https://pypi.python.org/pypi/pyfredapi)
[![Documentation Status](https://readthedocs.org/projects/pyfredapi/badge/?version=latest)](https://pyfredapi.readthedocs.io/en/latest/?badge=latest)
[![Unit Tests](https://github.com/gw-moore/pyfredapi/actions/workflows/test.yml/badge.svg)](https://github.com/gw-moore/pyfredapi/actions/workflows/test.yml)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=gw-moore_pyfredapi&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=gw-moore_pyfredapi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<!-- badges: end -->

`pyfredapi` is a Python library for the [Federal Reserve Economic Data](https://fred.stlouisfed.org/docs/api/fred/) (FRED) API web service. `pyfredapi` covers all the FRED api endpoints and can return data as a [pandas](https://pandas.pydata.org/) dataframe or json. Checkout the [docs](https://pyfredapi.readthedocs.io/en/latest/) to learn more.

## Installation

```bash
pip install pyfredapi
```

## Basic Usage

Before using `pyfredapi` and must have an API key to the FRED API web service. You can apply for [one for free](https://fred.stlouisfed.org/docs/api/api_key.html) on the FRED website.

You can either be set as the environment variable `FRED_API_KEY`, or pass it to the `api_key` parameters when initializing `pyfredapi`.

```python
import pyfredapi.series as pfs

# api key set as environment variable
gdp = pfs.get_series(series_id="GDP")

# api key passed to the function
gdp = pfs.get_series(series_id="GDP", api_key="my_api_key")
```
