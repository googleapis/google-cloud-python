# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Bigtable HappyBase package.

This package is intended to emulate the HappyBase library using
Google Cloud Bigtable as the backing store.

Differences in Public API
-------------------------

Some concepts from HBase/Thrift do not map directly to the Cloud
Bigtable API. As a result, the following instance methods and functions
could not be implemented:

* :meth:`Connection.enable_table() \
      <gcloud.bigtable.happybase.connection.Connection.enable_table>` - no
  concept of enabled/disabled
* :meth:`Connection.disable_table() \
      <gcloud.bigtable.happybase.connection.Connection.disable_table>` - no
  concept of enabled/disabled
* :meth:`Connection.is_table_enabled() \
      <gcloud.bigtable.happybase.connection.Connection.is_table_enabled>`
  - no concept of enabled/disabled
* :meth:`Connection.compact_table() \
      <gcloud.bigtable.happybase.connection.Connection.compact_table>` -
  table storage is opaque to user
* :meth:`Table.regions() <gcloud.bigtable.happybase.table.Table.regions>`
  - tables in Cloud Bigtable do not expose internal storage details
* :meth:`Table.counter_set() \
      <gcloud.bigtable.happybase.table.Table.counter_set>` - method can't
  be atomic, so we disable it
* The ``__version__`` value for the HappyBase package is :data:`None`.
  However, it's worth nothing this implementation was based off HappyBase
  0.9.

In addition, many of the constants from
:mod:`connection <gcloud.bigtable.happybase.connection>`
are specific to HBase and are defined as :data:`None` in our module:

* ``COMPAT_MODES``
* ``THRIFT_TRANSPORTS``
* ``THRIFT_PROTOCOLS``
* ``DEFAULT_HOST``
* ``DEFAULT_PORT``
* ``DEFAULT_TRANSPORT``
* ``DEFAULT_COMPAT``
* ``DEFAULT_PROTOCOL``

Two of these ``DEFAULT_HOST`` and ``DEFAULT_PORT``, are even imported in
the main :mod:`happybase <gcloud.bigtable.happybase>` package.

Finally, we do not provide the ``util`` module. Though it is public in the
HappyBase library, it provides no core functionality.

API Behavior Changes
--------------------

* Since there is no concept of an enabled / disabled table, calling
  :meth:`Connection.delete_table() \
      <gcloud.bigtable.happybase.connection.Connection.delete_table>`
  with ``disable=True`` can't be supported.
  Using that argument will result in a warning.
* The :class:`Connection <gcloud.bigtable.happybase.connection.Connection>`
  constructor **disables** the use of several
  arguments and will print a warning if any of them are passed in as keyword
  arguments. The arguments are:

  * ``host``
  * ``port``
  * ``compat``
  * ``transport``
  * ``protocol``
* In order to make
  :class:`Connection <gcloud.bigtable.happybase.connection.Connection>`
  compatible with Cloud Bigtable, we add a ``cluster`` keyword argument to
  allow users to pass in their own
  :class:`Cluster <gcloud.bigtable.cluster.Cluster>` (which they can
  construct beforehand).

  For example:

  .. code:: python

      from gcloud.bigtable.client import Client
      client = Client(project=PROJECT_ID, admin=True)
      cluster = client.cluster(zone, cluster_id)
      cluster.reload()

      from gcloud.bigtable.happybase import Connection
      connection = Connection(cluster=cluster)

* Any uses of the ``wal`` (Write Ahead Log) argument will result in a
  warning as well. This includes uses in:

  * :class:`Batch <gcloud.bigtable.happybase.batch.Batch>`
  * :meth:`Batch.put() <gcloud.bigtable.happybase.batch.Batch.put>`
  * :meth:`Batch.delete() <gcloud.bigtable.happybase.batch.Batch.delete>`
  * :meth:`Table.put() <gcloud.bigtable.happybase.table.Table.put>`
  * :meth:`Table.delete() <gcloud.bigtable.happybase.table.Table.delete>`
  * :meth:`Table.batch() <gcloud.bigtable.happybase.table.Table.batch>` factory
* When calling
  :meth:`Connection.create_table() \
      <gcloud.bigtable.happybase.connection.Connection.create_table>`, the
  majority of HBase column family options cannot be used. Among

  * ``max_versions``
  * ``compression``
  * ``in_memory``
  * ``bloom_filter_type``
  * ``bloom_filter_vector_size``
  * ``bloom_filter_nb_hashes``
  * ``block_cache_enabled``
  * ``time_to_live``

  Only ``max_versions`` and ``time_to_live`` are availabe in Cloud Bigtable
  (as
  :class:`MaxVersionsGCRule <gcloud.bigtable.column_family.MaxVersionsGCRule>`
  and
  :class:`MaxAgeGCRule <gcloud.bigtable.column_family.MaxAgeGCRule>`).

  In addition to using a dictionary for specifying column family options,
  we also accept instances of :class:`.GarbageCollectionRule` or subclasses.
* :meth:`Table.scan() <gcloud.bigtable.happybase.table.Table.scan>` no longer
  accepts the following arguments (which will result in a warning):

  * ``batch_size``
  * ``scan_batching``
  * ``sorted_columns``

* Using a HBase filter string in
  :meth:`Table.scan() <gcloud.bigtable.happybase.table.Table.scan>` is
  not possible with Cloud Bigtable and will result in a
  :class:`TypeError <exceptions.TypeError>`. However, the method now accepts
  instances of :class:`.RowFilter` and subclasses.
* :meth:`Batch.delete() <gcloud.bigtable.happybase.batch.Batch.delete>` (and
  hence
  :meth:`Table.delete() <gcloud.bigtable.happybase.table.Table.delete>`)
  will fail with a :class:`ValueError <exceptions.ValueError>` when either a
  row or column family delete is attempted with a ``timestamp``. This is
  because the Cloud Bigtable API uses the ``DeleteFromFamily`` and
  ``DeleteFromRow`` mutations for these deletes, and neither of these
  mutations support a timestamp.
"""

from gcloud.bigtable.happybase.batch import Batch
from gcloud.bigtable.happybase.connection import Connection
from gcloud.bigtable.happybase.connection import DEFAULT_HOST
from gcloud.bigtable.happybase.connection import DEFAULT_PORT
from gcloud.bigtable.happybase.pool import ConnectionPool
from gcloud.bigtable.happybase.pool import NoConnectionsAvailable
from gcloud.bigtable.happybase.table import Table


# Values from HappyBase that we don't reproduce / are not relevant.
__version__ = None
