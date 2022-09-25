.. pyfreadpi documentation master file, created by
   sphinx-quickstart on Sat Sep 24 14:07:36 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyfreadpi's documentation!
=====================================

:code:`pyfredapi` is a Python API for accessing the `FRED API web service <https://fred.stlouisfed.org/docs/api/fred/>`_
provided by the Federal Reserve Bank of St. Louis. :code:`pyfredapi` makes it easy to retrieve economic data
from `FRED <https://fred.stlouisfed.org/>`_ and `ALFRED <https://alfred.stlouisfed.org/>`_.

Requests to the API can be customized according to the parameters made available by the web service endpoints.

Quick Start
=================

Before you can use :code:`pyfredapi` you must have an API key to the FRED API web service. You can `apply for one <https://fred.stlouisfed.org/docs/api/api_key.html>`_ for free on the FRED website.

You can set your API in two ways:

* set your API key to the environment variable :code:`FRED_API_KEY`
* pass it to the :code:`api_key` parameter

Installation
------------

:code:`pyfreadpi` can be installed via pip.

.. code-block:: bash

   pip install fredapi


Example
-------

Quick start example of how to pull U.S. gross domestic product data.

.. code-block:: python

   from pyfredapi import FredApi

   # api key set as environment variable
   client = FredApi()

   # api key passed to initializer
   client = FredApi(api_key = "my_api_key")

   # get GDP data
   client.get_series_data("GDP")

.. toctree::
   :maxdepth: 1
   :caption: Tutorials
   :hidden:

.. toctree::
   :maxdepth: 3
   :caption: References
   :hidden:

   API <references/api>
   Changelog <references/CHANGELOG.md>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
