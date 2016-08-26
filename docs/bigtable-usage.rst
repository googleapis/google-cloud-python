Using the API
=============

API requests are sent to the `Google Cloud Bigtable`_ API via RPC over HTTP/2.
In order to support this, we'll rely on `gRPC`_. We are working with the gRPC
team to rapidly make the install story more user-friendly.

Get started by learning about the
:class:`Client <gcloud.bigtable.client.Client>` on the
:doc:`bigtable-client-intro` page.

In the hierarchy of API concepts

* a :class:`Client <gcloud.bigtable.client.Client>` owns a
  :class:`Cluster <gcloud.bigtable.instance.Instance`
* a :class:`Cluster <gcloud.bigtable.instance.Instance` owns a
  :class:`Table <gcloud.bigtable.table.Table>`
* a :class:`Table <gcloud.bigtable.table.Table>` owns a
  :class:`ColumnFamily <gcloud.bigtable.column_family.ColumnFamily>`
* a :class:`Table <gcloud.bigtable.table.Table>` owns a
  :class:`Row <gcloud.bigtable.row.Row>`
  (and all the cells in the row)

.. _Google Cloud Bigtable: https://cloud.google.com/bigtable/docs/
.. _gRPC: http://www.grpc.io/
.. _grpcio: https://pypi.python.org/pypi/grpcio
