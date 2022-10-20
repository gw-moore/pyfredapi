import pkg_resources as _pkg_resources

from .api import (
    FredCategory,
    FredMaps,
    FredRelease,
    FredSeries,
    ReturnFormat,
    SeriesCollection,
)

__version__ = _pkg_resources.get_distribution("pyfredapi").version

__doc__ = """
pyfredapi - Python client for the Federal Reserve Economic Data (FRED) API
===========================================================================
**pyfredapi** is a Python client for the [FRED API web service](https://fred.stlouisfed.org/docs/api/fred/).
`pyfredapi` covers all the FRED api endpoints and can return data as a [pandas](https://pandas.pydata.org/)
dataframe or json. Checkout the [docs](https://pyfredapi.readthedocs.io/en/latest/) to learn more.

Main Features
-------------
Here are just a few of the things that pyfredapi does:
  - Request economic series data from FRED api. The response can be formatted as a pandas dataframe.
  - Request economics series' metadata.
  - Keyword search for a economic series.
"""
