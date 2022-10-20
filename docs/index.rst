.. pyfreadpi documentation master file, created by
   sphinx-quickstart on Sat Sep 24 14:07:36 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python client for FRED API
=======================================

:code:`pyfredapi` is a Python client for the for the `FRED API web service <https://fred.stlouisfed.org/docs/api/fred.html>`_
provided by the Federal Reserve Bank of St. Louis. :code:`pyfredapi` covers all the the FRED API end points, and
can retrieve economic data from `FRED <https://fred.stlouisfed.org/>`_ and `ALFRED <https://alfred.stlouisfed.org/>`_. Data
can be return as a `pandas <https://pandas.pydata.org/>`_ dataframe or as json. Requests to the FRED API can be customized according to
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
* pass it to the :code:`api_key` parameter

Usage
------

Each of the FRED API namespaces is covered by a class in :code:`pyfredapi`. For a deeper dive into each of the separate classes, see the `API documentation <https://pyfredapi.readthedocs.io/en/latest/references/api.html#>`_.

- :code:`FredCategory` - covers the FRED Categories endpoints.
- :code:`FredMaps` - covers the FRED Maps endpoints.
- :code:`FredRelease` - covers the FRED Releases endpoints.
- :code:`FredSeries` - covers the FRED Series endpoints.
- :code:`FredSources` - covers the FRED Sources endpoints.
- :code:`FredTags` - covers the FRED Tags endpoints.
- :code:`SeriesCollection` - make handling multiple series easier.

Quick start example of how to pull U.S. gross domestic product data.

.. code-block:: python

   from pyfredapi import FredSeries

   # api key set as environment variable
   client = FredSeries()

   # api key passed to initializer
   client = FredSeries(api_key = "my_api_key")

   # get GDP data
   client.get_series("GDP")

.. toctree::
   :titlesonly:
   :hidden:

   FRED Series <tutorials/FredSeries.ipynb>
   .. Series Collection <tutorials/SeriesCollection.ipynb>
   FRED Maps <tutorials/FredMaps.ipynb>

.. toctree::
   :maxdepth: 1
   :hidden:

   API <references/api>
   Changelog <references/CHANGELOG.md>
