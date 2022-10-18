.. pyfreadpi documentation master file, created by
   sphinx-quickstart on Sat Sep 24 14:07:36 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyfreadpi - Python client for FRED API
=======================================

:code:`pyfredapi` is a Python client for the for the `FRED API web service <https://fred.stlouisfed.org/docs/api/fred.html>`_
provided by the Federal Reserve Bank of St. Louis. :code:`pyfredapi` covers all the the FRED API end points, and
can retrieve economic data from `FRED <https://fred.stlouisfed.org/>`_ and `ALFRED <https://alfred.stlouisfed.org/>`_. Data
can be return as a `pandas <https://pandas.pydata.org/>`_ dataframe or as json. Requests to the FRED API can be customized according to
the parameters made available by the web service endpoints.

Quick Start
===========

FRED API Key
------------

Before you can use :code:`pyfredapi` you must have an API key to the FRED API web service. You can `apply for one <https://fred.stlouisfed.org/docs/api/api_key.html>`_ for free on the FRED website.

You can set your API in two ways:

* set your API key to the environment variable :code:`FRED_API_KEY`
* pass it to the :code:`api_key` parameter

Installation
-------------

:code:`pyfreadpi` can be installed via pip.

.. code-block:: bash

   pip install pyfredapi

Usage
------

Users will primarily interact with the :code:`FredApi` class. :code:`FredApi` is a convenience wrapper around separate classes that
cover each of the FRED API namespaces. For a deeper dive into each of the separate clients, see the `API documentation <https://pyfredapi.readthedocs.io/en/latest/references/api.html#>`_.

- :code:`FredCategory` - covers the FRED Categories endpoints.
- :code:`FredMaps` - covers the FRED Maps endpoints.
- :code:`FredRelease` - covers the FRED Releases endpoints.
- :code:`FredSeries`` - covers the FRED Series endpoints.
- :code:`FredSources` - covers the FRED Sources endpoints.
- :code:`FredTags` - covers the FRED Tags endpoints.

Quick start example of how to pull U.S. gross domestic product data.

.. code-block:: python

   from pyfredapi import FredSeries

   # api key set as environment variable
   client = FredSeries()

   # api key passed to initializer
   client = FredSeries(api_key = "my_api_key")

   # get GDP data
   client.get_series("GDP")

For practical examples using the different clients, checkout the tutorials in the sidebar.

.. toctree::
   :titlesonly:
   :caption: Tutorials
   :hidden:

   FRED Series <tutorials/FredSeries.ipynb>
   Series Collection <tutorials/SeriesCollection.ipynb>
   FRED Maps <tutorials/FredMaps.ipynb>

.. toctree::
   :maxdepth: 1
   :caption: References
   :hidden:

   API <references/api>
   Changelog <references/CHANGELOG.md>
