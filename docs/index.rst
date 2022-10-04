.. pyfreadpi documentation master file, created by
   sphinx-quickstart on Sat Sep 24 14:07:36 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyfreadpi's: python client for FRED
=====================================

:code:`pyfredapi` is a Python client for the for the `FRED API web service <https://fred.stlouisfed.org/docs/api/fred.html>`_
provided by the Federal Reserve Bank of St. Louis. :code:`pyfredapi` has methods to retrieve economic data
from `FRED <https://fred.stlouisfed.org/>`_ and `ALFRED <https://alfred.stlouisfed.org/>`_.

`pyfredapi` aims to be a full featured api for the FRED API web service. `pyfredapi` covers all the FRED api endpoints and can 
return data as a `pandas <https://pandas.pydata.org/>`_ dataframe or as json. Requests to the API can be customized according to 
the parameters made available by the web service endpoints.

FRED API Key
-------------

Before you can use :code:`pyfredapi` you must have an API key to the FRED API web service. You can `apply for one <https://fred.stlouisfed.org/docs/api/api_key.html>`_ for free on the FRED website.

You can set your API in two ways:

* set your API key to the environment variable :code:`FRED_API_KEY`
* pass it to the :code:`api_key` parameter

Installation
-------------

:code:`pyfreadpi` can be installed via pip.

.. code-block:: bash

   pip install pyfredapi


Example
--------

Quick start example of how to pull U.S. gross domestic product data.

.. code-block:: python

   from pyfredapi import FredApi

   # api key set as environment variable
   client = FredApi()

   # api key passed to initializer
   client = FredApi(api_key = "my_api_key")

   # get GDP data
   client.get_series("GDP")

.. toctree::
   :caption: Overview
   :titlesonly:
   :hidden:

   Overview <tutorials/overview.md>

.. toctree::
   :titlesonly:
   :caption: Tutorials
   :hidden:

   FRED Series <tutorials/FredSeries.ipynb>
   FRED Maps <tutorials/FredMaps.ipynb>
   FRED Category <tutorials/FredCategory.ipynb>
   FRED Release <tutorials/FredRelease.ipynb>
   FRED Sources <tutorials/FredSources.ipynb>
   FRED Tags <tutorials/FredTags.ipynb>

.. toctree::
   :maxdepth: 1
   :caption: References
   :hidden:

   API <references/api>
   Changelog <references/CHANGELOG.md>
