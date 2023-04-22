pyfredapi
==================

:code:`pyfredapi` is a Python library that makes it is easy to retrieve data from the `FRED API web service <https://fred.stlouisfed.org/docs/api/fred>`_.
:code:`pyfredapi` covers all the FRED API endpoints, and can retrieve data from `FRED <https://fred.stlouisfed.org/>`_ and `ALFRED <https://alfred.stlouisfed.org/>`_.
Data can be returned as a `pandas <https://pandas.pydata.org/>`_ dataframe or as `json <https://www.json.org/json-en.html>`_. Requests to the FRED API can be customized according to
the parameters made available by the web service endpoints.

Installation
-------------

:code:`pyfreadpi` can be installed via pip.

.. code-block:: bash

   pip install pyfredapi

FRED API Key
------------

Before you can use :code:`pyfredapi` you must have an API key to the FRED API web service. You can `apply for one <https://fred.stlouisfed.org/docs/api/api_key.html>`_ for free on the FRED website.

You can set your API key in two ways:

* set your API key to the environment variable :code:`FRED_API_KEY`
* pass it to the :code:`api_key` parameter of the request function

You can set the API key as an environment variable by adding the following line to your `~/.zshrc`, `~/.bashrc` file:

.. code-block:: bash

   export FRED_API_KEY="your_api_key"

Quick Start
-----------

Each of the FRED API endpoint namespaces is covered by a module in :code:`pyfredapi`. For a deeper dive into each of the
modules see the tutorials and API reference in the sidebar.

- :code:`category` - covers the FRED Categories endpoints
- :code:`maps` - covers the FRED Maps endpoints
- :code:`release` - covers the FRED Releases endpoints
- :code:`series` - covers the FRED Series endpoints
- :code:`sources` - covers the FRED Sources endpoints
- :code:`tags` - covers the FRED Tags endpoints
- :code:`series_collection` - makes handling multiple series easier

Quick start example:

.. code-block:: python

   import pyfreadpi as pf

   # api key set as environment variable
   pf.get_series_info(series_id="GDP")

   # api key passed to initializer
   pf.get_series_info(series_id="GDP", api_key="my_api_key"")

.. toctree::
   :caption: Tutorials
   :maxdepth: 1

   FRED Series <tutorials/series.ipynb>
   Series Collection <tutorials/series_collection.ipynb>
   FRED Maps <tutorials/maps.ipynb>

.. toctree::
   :caption: Reference
   :maxdepth: 1

   API <references/api>
   Changelog <references/CHANGELOG.md>
   Contributing <references/CONTRIBUTING.rst>
