Bigtable
========

.. toctree::
  :maxdepth: 2
  :hidden:

  client-intro
  client
  cluster
  instance
  instance-api
  table
  table-api
  column-family
  row
  row-data
  row-filters
  data-api

API requests are sent to the `Google Cloud Bigtable`_ API via RPC over HTTP/2.
In order to support this, we'll rely on `gRPC`_. We are working with the gRPC
team to rapidly make the install story more user-friendly.

Get started by learning about the
:class:`Client <google.cloud.bigtable.client.Client>` on the
:doc:`client-intro` page.

In the hierarchy of API concepts

* a :class:`Client <google.cloud.bigtable.client.Client>` owns an
  :class:`Instance <google.cloud.bigtable.instance.Instance>`
* an :class:`Instance <google.cloud.bigtable.instance.Instance>` owns a
  :class:`Table <google.cloud.bigtable.table.Table>`
* a :class:`Table <google.cloud.bigtable.table.Table>` owns a
  :class:`ColumnFamily <google.cloud.bigtable.column_family.ColumnFamily>`
* a :class:`Table <google.cloud.bigtable.table.Table>` owns a
  :class:`Row <google.cloud.bigtable.row.Row>`
  (and all the cells in the row)

.. _Google Cloud Bigtable: https://cloud.google.com/bigtable/docs/
.. _gRPC: http://www.grpc.io/
.. _grpcio: https://pypi.org/project/grpcio/
