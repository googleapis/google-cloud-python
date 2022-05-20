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

.. toctree::
  :maxdepth: 2

  job_base


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
    table.CloneDefinition
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

.. toctree::
  :maxdepth: 2

  query


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

.. toctree::
    :maxdepth: 2

    format_options


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

Helper SQL type classes.

.. toctree::
    :maxdepth: 2

    bigquery/standard_sql


Legacy proto-based Types (deprecated)
=====================================

The legacy type classes based on protocol buffers.

.. deprecated:: 3.0.0
    These types are provided for backward compatibility only, and are not maintained
    anymore.

.. toctree::
    :maxdepth: 2

    bigquery/legacy_proto_types
