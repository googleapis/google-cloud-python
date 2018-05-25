.. pandas-gbq documentation master file, created by
   sphinx-quickstart on Wed Feb  8 10:52:12 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pandas-gbq's documentation!
======================================

The :mod:`pandas_gbq` module provides a wrapper for Google's BigQuery
analytics web service to simplify retrieving results from BigQuery tables
using SQL-like queries. Result sets are parsed into a pandas
DataFrame with a shape and data types derived from the source table.
Additionally, DataFrames can be inserted into new BigQuery tables or appended
to existing tables.

.. warning::

   To use this module, you will need a valid BigQuery account. Refer to the
   `BigQuery Documentation <https://cloud.google.com/bigquery/what-is-bigquery>`__
   for details on the service itself.

Contents:

.. toctree::
   :maxdepth: 2

   install.rst
   intro.rst
   howto/authentication.rst
   reading.rst
   writing.rst
   tables.rst
   api.rst
   contributing.rst
   changelog.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
