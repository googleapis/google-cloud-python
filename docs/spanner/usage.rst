Spanner
=======

.. toctree::
  :maxdepth: 2
  :hidden:

  client-usage
  instance-usage
  database-usage
  batch-usage
  snapshot-usage
  transaction-usage
  advanced-session-pool-topics

  client-api
  instance-api
  database-api
  session-api
  keyset-api
  snapshot-api
  batch-api
  transaction-api
  streamed-api

API requests are sent to the `Cloud Spanner`_ API via RPC over
HTTP/2.  In order to support this, we'll rely on `gRPC`_.

Get started by learning about the :class:`~google.cloud.spanner.client.Client`
on the :doc:`client-usage` page.

In the hierarchy of API concepts

* a :class:`~google.cloud.spanner.client.Client` owns an
  :class:`~google.cloud.spanner.instance.Instance`
* an :class:`~google.cloud.spanner.instance.Instance` owns a
  :class:`~google.cloud.spanner.database.Database`

.. _Cloud Spanner: https://cloud.google.com/spanner/docs/
.. _gRPC: http://www.grpc.io/
.. _grpcio: https://pypi.org/project/grpcio/
