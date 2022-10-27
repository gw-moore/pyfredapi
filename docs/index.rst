pyfredapi
==================

:code:`pyfredapi` is a Python library that makes it is easy to retrieve data from the `FRED API web service <https://fred.stlouisfed.org/docs/api/fred>`_.
:code:`pyfredapi` covers all the the FRED API endpoints, and can retrieve data from `FRED <https://fred.stlouisfed.org/>`_ and `ALFRED <https://alfred.stlouisfed.org/>`_.
Data can be return as a `pandas <https://pandas.pydata.org/>`_ dataframe or as `json <https://www.json.org/json-en.html>`_. Requests to the FRED API can be customized according to
the parameters made available by the web service endpoints.

Installation
-------------

:code:`pyfreadpi` can be installed via pip.

.. code-block:: bash

   pip install pyfredapi

FRED API Key
------------

Before you can use :code:`pyfredapi` you must have an API key to the FRED API web service. You can `apply for one <https://fred.stlouisfed.org/docs/api/api_key.html>`_ for free on the FRED website.

You can set your API in two ways:

* set your API key to the environment variable :code:`FRED_API_KEY`
* pass it to the :code:`api_key` parameter when creating a client instance

Quick Start
-----------

Each of the FRED API endpoint namespaces is covered by a class in :code:`pyfredapi`. For a deeper dive into each of the
separate classes see the tutorials and API reference in the sidebar.

- :code:`FredCategory` - covers the FRED Categories endpoints
- :code:`FredMaps` - covers the FRED Maps endpoints
- :code:`FredRelease` - covers the FRED Releases endpoints
- :code:`FredSeries` - covers the FRED Series endpoints
- :code:`FredSources` - covers the FRED Sources endpoints
- :code:`FredTags` - covers the FRED Tags endpoints
- :code:`SeriesCollection` - makes handling multiple series easier

Quick start example:

.. code-block:: python

   from pyfredapi import FredSeries

   # api key set as environment variable
   client = FredSeries()

   # api key passed to initializer
   client = FredSeries(api_key = "my_api_key")

   # get GDP data
   client.get_series("GDP")

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
