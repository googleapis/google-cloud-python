Using the API
=============

API requests are sent to the `Cloud Spanner`_ API via RPC over
HTTP/2.  In order to support this, we'll rely on `gRPC`_.

Get started by learning about the :class:`~google.cloud.spanner.client.Client`
on the :doc:`spanner-client-usage` page.

In the hierarchy of API concepts

* a :class:`~google.cloud.spanner.client.Client` owns an
  :class:`~google.cloud.spanner.instance.Instance`
* an :class:`~google.cloud.spanner.instance.Instance` owns a
  :class:`~google.cloud.spanner.database.Database`

.. _Cloud Spanner: https://cloud.google.com/spanner/docs/
.. _gRPC: http://www.grpc.io/
.. _grpcio: https://pypi.python.org/pypi/grpcio

