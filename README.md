# pyfredapi - Python API for the Federal Reserve Economic Data (FRED)
<!-- badges: start -->

[![PyPi Version](https://img.shields.io/pypi/v/pyfredapi.svg)](https://pypi.python.org/pypi/pyfredapi/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyfredapi)](https://pypi.python.org/pypi/pyfredapi)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

<!-- badges: end -->

`pyfredapi` is a Python API for accessing the [FRED API web service](https://fred.stlouisfed.org/docs/api/fred/) provided by the Federal Reserve Bank of St. Louis. `pyfredapi` makes it easy to retrieve economic data from [FRED](https://fred.stlouisfed.org/) and [ALFRED](https://alfred.stlouisfed.org/). Requests to the api can be customized according to the parameters made available by the web service.

`pyfredapi` aims to be a full featured api for the FRED API web service. `pyfredapi` provides convenient methods for requesting data series, and can return data as a [pandas](https://pandas.pydata.org/) dataframe of as json.

## Installation
```bash
pip install fredapi
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

# get data for the S&P500
client.get_series_data("SP500")
```

## Documentation

Coming soon

## Contributing

Coming soon
