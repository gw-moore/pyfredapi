# pyfredapi - Python API for the Federal Reserve Economic Data (FRED)
<!-- badges: start -->

[![PyPi Version](https://img.shields.io/pypi/v/pyfredapi.svg)](https://pypi.python.org/pypi/pyfredapi/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyfredapi)](https://pypi.python.org/pypi/pyfredapi)
[![Documentation Status](https://readthedocs.org/projects/pyfredapi/badge/?version=latest)](https://pyfredapi.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<!-- badges: end -->

`pyfredapi` is a Python API for accessing the [FRED API web service](https://fred.stlouisfed.org/docs/api/fred/) provided by the Federal Reserve Bank of St. Louis. `pyfredapi` makes it easy to retrieve economic data from [FRED](https://fred.stlouisfed.org/) and [ALFRED](https://alfred.stlouisfed.org/). Requests to the api can be customized according to the parameters made available by the web service.

`pyfredapi` aims to be a full featured api for the FRED API web service. `pyfredapi` provides convenient methods for requesting data series and can return data as a [pandas](https://pandas.pydata.org/) dataframe or as json.

## Installation
```bash
pip install pyfredapi
```

## Basic Usage

Before using `pyfredapi` and must have a API key to the FRED API web service. You can apply for [one for free](https://fred.stlouisfed.org/docs/api/api_key.html) on the FRED website.

You can either be set as the environment variable `FRED_API_KEY`, or pass it to the `api_key` parameters when initializing `pyfredapi`.

```python
from pyfredapi import FredApi

# api key set as environment variable
client = FredApi()

# api key passed to initializer
client = FredApi(api_key = "my_api_key")

# get GDP data
client.get_series("GDP")
```

## Contributing

Coming soon
