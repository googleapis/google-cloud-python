API Reference
~~~~~~~~~~~~~

.. currentmodule:: google.cloud.bigquery

The main concepts with this API are:

- :class:`~google.cloud.bigquery.client.Client` manages connections to the
  BigQuery API. Use the client methods to run jobs (such as a
  :class:`~google.cloud.bigquery.job.QueryJob` via
  :meth:`~google.cloud.bigquery.client.Client.query`) and manage resources.

- :class:`~google.cloud.bigquery.dataset.Dataset` represents a
  collection of tables.

- :class:`~google.cloud.bigquery.table.Table` represents a single "relation".

Client
======

.. autosummary::
    :toctree: reference

    client.Client

Job
===

Job Configuration
-----------------

.. autosummary::
    :toctree: reference

    job.QueryJobConfig
    job.CopyJobConfig
    job.LoadJobConfig
    job.ExtractJobConfig

Job Classes
-----------

.. autosummary::
    :toctree: reference

    job.QueryJob
    job.CopyJob
    job.LoadJob
    job.ExtractJob
    job.UnknownJob

Job Resources
-------------

.. autosummary::
    :toctree: reference

    job.Compression
    job.CreateDisposition
    job.DestinationFormat
    job.Encoding
    job.QueryPriority
    job.SourceFormat
    job.WriteDisposition


Dataset
=======

.. autosummary::
    :toctree: reference

    dataset.Dataset
    dataset.DatasetReference
    dataset.AccessEntry


Table
=====

.. autosummary::
    :toctree: reference

    table.Table
    table.TableReference
    table.Row
    table.EncryptionConfiguration
    table.TimePartitioning
    table.TimePartitioningType


Schema
======

.. autosummary::
    :toctree: reference

    schema.SchemaField


Query
=====

.. autosummary::
    :toctree: reference

    query.ArrayQueryParameter
    query.ScalarQueryParameter
    query.StructQueryParameter
    query.UDFResource


External Configuration
======================

.. autosummary::
    :toctree: reference

    external_config.ExternalConfig
    external_config.BigtableOptions
    external_config.BigtableColumnFamily
    external_config.BigtableColumn
    external_config.CSVOptions
    external_config.GoogleSheetsOptions


Magics
======================

.. autosummary::
    :toctree: reference

    magics
