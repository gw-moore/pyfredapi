# pyfredapi - Python library for the Federal Reserve Economic Data (FRED) API

<div align="center">


| | |
| :--- | :--- |
| CI/CD | [![CI - Test](https://github.com/gw-moore/pyfredapi/actions/workflows/test.yml/badge.svg)](https://github.com/gw-moore/pyfredapi/actions/workflows/test.yml)|
| Docs | [![Documentation Status](https://readthedocs.org/projects/pyfredapi/badge/?version=latest)](https://pyfredapi.readthedocs.io/en/latest/?badge=latest) |
| Package | [![PyPi Version](https://img.shields.io/pypi/v/pyfredapi.svg)](https://pypi.python.org/pypi/pyfredapi/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyfredapi)](https://pypi.python.org/pypi/pyfredapi) |
| Meta | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) |

</div>

-----

`pyfredapi` is a full featured Python library that makes it is easy to retrieve data from the [Federal Reserve Economic Data](https://fred.stlouisfed.org/docs/api/fred/) (FRED) API web service. `pyfredapi` covers all the FRED api endpoints, and can retrieve data from [FRED](https://fred.stlouisfed.org/) and [ALFRED](https://alfred.stlouisfed.org). Data can be returned as a [pandas](https://pandas.pydata.org/) dataframe or json. Requests to the FRED API can be customized according to the parameters made available by the web service endpoints.

## Documentation

The [documentation](https://pyfredapi.readthedocs.io/en/latest/) is made with [MkDocs](https://www.mkdocs.org/) and hosted on [Read the Docs](https://readthedocs.org/).

## Installation

Install the latest version with pip:

```bash
pip install pyfredapi
```

Install pyfredapi with all optional dependencies.

```bash
pip install 'pyfredapi[all]'
```

You can also install a subset of all optional dependencies.

```bash
pip install 'pyfredapi[polars]'
```

## Quick Start

### FRED API Key

Before using `pyfredapi` and must have an API key to the FRED API web service. You can apply for [one for free](https://fred.stlouisfed.org/docs/api/api_key.html) on the FRED website.

You can set your API key in two ways:

* set your API key to the environment variable `FRED_API_KEY`
* pass it to the `api_key` parameter of the request function

You can set the API key as an environment variable by adding the following line to your `~/.zshrc`, `~/.bashrc` file:

```bash
export FRED_API_KEY="your_api_key"
```

### Using pyfredapi

Each of the FRED API endpoint namespaces is covered by a module in `pyfredapi`. For a deeper dive into each of the modules see the tutorials and API reference in the [documentation](https://pyfredapi.readthedocs.io/en/latest/).

- `category` - covers the FRED Categories endpoints
- `maps` - covers the FRED Maps endpoints
- `release` - covers the FRED Releases endpoints
- `series` - covers the FRED Series endpoints
- `sources` - covers the FRED Sources endpoints
- `tags` - covers the FRED Tags endpoints
- `series_collection` - makes handling multiple series easier

Quick start example:

```python
import pyfredapi as pf

# api key set as environment variable
pf.get_series(series_id="GDP")

# api key passed to the function
pf.get_series(series_id="GDP", api_key="my_api_key")
```

## Contributing

Thank you for your interest in contributing to `pyfredapi`. Check out the [contributing guide](https://pyfredapi.readthedocs.io/en/latest/references/CONTRIBUTING.html) to get started.
