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
    :toctree: generated

    client.Client

Job
===

Job Configuration
-----------------

.. autosummary::
    :toctree: generated

    job.QueryJobConfig
    job.CopyJobConfig
    job.LoadJobConfig
    job.ExtractJobConfig

Job Classes
-----------

.. autosummary::
    :toctree: generated

    job.QueryJob
    job.CopyJob
    job.LoadJob
    job.ExtractJob
    job.UnknownJob

Job-Related Types
-----------------

.. autosummary::
    :toctree: generated

    job.Compression
    job.CreateDisposition
    job.DestinationFormat
    job.DmlStats
    job.Encoding
    job.OperationType
    job.QueryPlanEntry
    job.QueryPlanEntryStep
    job.QueryPriority
    job.ReservationUsage
    job.SourceFormat
    job.WriteDisposition
    job.SchemaUpdateOption
    job.TransactionInfo


Dataset
=======

.. autosummary::
    :toctree: generated

    dataset.Dataset
    dataset.DatasetListItem
    dataset.DatasetReference
    dataset.AccessEntry


Table
=====

.. autosummary::
    :toctree: generated

    table.PartitionRange
    table.RangePartitioning
    table.Row
    table.RowIterator
    table.SnapshotDefinition
    table.Table
    table.TableListItem
    table.TableReference
    table.TimePartitioning
    table.TimePartitioningType

Model
=====

.. autosummary::
    :toctree: generated

    model.Model
    model.ModelReference

Routine
=======

.. autosummary::
    :toctree: generated

    routine.DeterminismLevel
    routine.Routine
    routine.RoutineArgument
    routine.RoutineReference
    routine.RoutineType

Schema
======

.. autosummary::
    :toctree: generated

    schema.SchemaField
    schema.PolicyTagList


Query
=====

.. autosummary::
    :toctree: generated

    query.ArrayQueryParameter
    query.ScalarQueryParameter
    query.ScalarQueryParameterType
    query.StructQueryParameter
    query.UDFResource


Retries
=======

.. autosummary::
    :toctree: generated

    retry.DEFAULT_RETRY


External Configuration
======================

.. autosummary::
    :toctree: generated

    external_config.ExternalSourceFormat
    external_config.ExternalConfig
    external_config.BigtableOptions
    external_config.BigtableColumnFamily
    external_config.BigtableColumn
    external_config.CSVOptions
    external_config.GoogleSheetsOptions


Magics
======

.. toctree::
    :maxdepth: 2

    magics


Enums
=====

.. toctree::
    :maxdepth: 2

    enums


Encryption Configuration
========================

.. autosummary::
    :toctree: generated

    encryption_configuration.EncryptionConfiguration


Additional Types
================

Protocol buffer classes for working with the Models API.

.. toctree::
    :maxdepth: 2

    bigquery_v2/types
