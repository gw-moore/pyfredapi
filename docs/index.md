# pyfredapi

`pyfredapi` is a Python library that makes it is easy to retrieve data from the [FRED API web service](https://fred.stlouisfed.org/docs/api/fred).

`pyfredapi` covers all the FRED API endpoints, and can retrieve data from [FRED](https://fred.stlouisfed.org/) and [ALFRED](https://alfred.stlouisfed.org/).
Data can be returned as a [pandas](https://pandas.pydata.org/) dataframe or as [json](https://www.json.org/json-en.html). Requests to the FRED API can be customized according to
the parameters made available by the web service endpoints.

## Installation

`pyfredapi` can be installed via pip.

```bash
pip install pyfredapi

# install with plotting dependencies
pip install 'pyfredapi[plot]'
```

## FRED API Key

Before you can use `pyfredapi` you must have an API key to the FRED API web service. You can [apply for one](https://fred.stlouisfed.org/docs/api/api_key.html) for free on the FRED website.

You can set your API key in two ways:

* set your API key to the environment variable :code:`FRED_API_KEY`
* pass it to the :code:`api_key` parameter of the request function

You can set the API key as an environment variable by adding the following line to your `~/.zshrc`, `~/.bashrc` file:

```bash
export FRED_API_KEY="your_api_key"
```

## Quick Start

Each of the FRED API endpoint namespaces is covered by a module in `pyfredapi`. For a deeper dive into each of the
modules see the tutorials and API documentation in the sidebar.

- `category` - covers the FRED Categories endpoints
- `maps` - covers the FRED Maps endpoints
- `release` - covers the FRED Releases endpoints
- `series` - covers the FRED Series endpoints
- `sources` - covers the FRED Sources endpoints
- `tags` - covers the FRED Tags endpoints
- `series_collection` - makes handling multiple series easier

Quick start example:

```python
import pyfreadpi as pf

# api key set as environment variable
pf.get_series_info(series_id="GDP")

# api key passed to function
pf.get_series_info(series_id="GDP", api_key="my_api_key")
```
