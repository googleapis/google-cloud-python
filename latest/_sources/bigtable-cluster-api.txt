Cluster Admin API
=================

After creating a :class:`Client <gcloud.bigtable.client.Client>`, you can
interact with individual clusters, groups of clusters or available
zones for a project.

List Clusters
-------------

If you want a comprehensive list of all existing clusters, make a
`ListClusters`_ API request with
:meth:`Client.list_clusters() <gcloud.bigtable.client.Client.list_clusters>`:

.. code:: python

    clusters = client.list_clusters()

List Zones
----------

If you aren't sure which ``zone`` to create a cluster in, find out
which zones your project has access to with a `ListZones`_ API request
with :meth:`Client.list_zones() <gcloud.bigtable.client.Client.list_zones>`:

.. code:: python

    zones = client.list_zones()

You can choose a :class:`string <str>` from among the result to pass to
the :class:`Cluster <gcloud.bigtable.cluster.Cluster>` constructor.

The available zones (as of February 2016) are

.. code:: python

    >>> zones
    [u'asia-east1-b', u'europe-west1-c', u'us-central1-c', u'us-central1-b']

Cluster Factory
---------------

To create a :class:`Cluster <gcloud.bigtable.cluster.Cluster>` object:

.. code:: python

    cluster = client.cluster(zone, cluster_id,
                             display_name=display_name,
                             serve_nodes=3)

Both ``display_name`` and ``serve_nodes`` are optional. When not provided,
``display_name`` defaults to the ``cluster_id`` value and ``serve_nodes``
defaults to the minimum allowed:
:data:`DEFAULT_SERVE_NODES <gcloud.bigtable.cluster.DEFAULT_SERVE_NODES>`.

Even if this :class:`Cluster <gcloud.bigtable.cluster.Cluster>` already
has been created with the API, you'll want this object to use as a
parent of a :class:`Table <gcloud.bigtable.table.Table>` just as the
:class:`Client <gcloud.bigtable.client.Client>` is used as the parent of
a :class:`Cluster <gcloud.bigtable.cluster.Cluster>`.

Create a new Cluster
--------------------

After creating the cluster object, make a `CreateCluster`_ API request
with :meth:`create() <gcloud.bigtable.cluster.Cluster.create>`:

.. code:: python

    cluster.display_name = 'My very own cluster'
    cluster.create()

If you would like more than the minimum number of nodes
(:data:`DEFAULT_SERVE_NODES <gcloud.bigtable.cluster.DEFAULT_SERVE_NODES>`)
in your cluster:

.. code:: python

    cluster.serve_nodes = 10
    cluster.create()

Check on Current Operation
--------------------------

.. note::

    When modifying a cluster (via a `CreateCluster`_, `UpdateCluster`_ or
    `UndeleteCluster`_ request), the Bigtable API will return a
    `long-running operation`_ and a corresponding
    :class:`Operation <gcloud.bigtable.cluster.Operation>` object
    will be returned by each of
    :meth:`create() <gcloud.bigtable.cluster.Cluster.create>`,
    :meth:`update() <gcloud.bigtable.cluster.Cluster.update>` and
    :meth:`undelete() <gcloud.bigtable.cluster.Cluster.undelete>`.

You can check if a long-running operation (for a
:meth:`create() <gcloud.bigtable.cluster.Cluster.create>`,
:meth:`update() <gcloud.bigtable.cluster.Cluster.update>` or
:meth:`undelete() <gcloud.bigtable.cluster.Cluster.undelete>`) has finished
by making a `GetOperation`_ request with
:meth:`Operation.finished() <gcloud.bigtable.cluster.Operation.finished>`:

.. code:: python

    >>> operation = cluster.create()
    >>> operation.finished()
    True

.. note::

    Once an :class:`Operation <gcloud.bigtable.cluster.Operation>` object
    has returned :data:`True` from
    :meth:`finished() <gcloud.bigtable.cluster.Operation.finished>`, the
    object should not be re-used. Subsequent calls to
    :meth:`finished() <gcloud.bigtable.cluster.Operation.finished>`
    will result in a :class:`ValueError <exceptions.ValueError>`.

Get metadata for an existing Cluster
------------------------------------

After creating the cluster object, make a `GetCluster`_ API request
with :meth:`reload() <gcloud.bigtable.cluster.Cluster.reload>`:

.. code:: python

    cluster.reload()

This will load ``serve_nodes`` and ``display_name`` for the existing
``cluster`` in addition to the ``cluster_id``, ``zone`` and ``project``
already set on the :class:`Cluster <gcloud.bigtable.cluster.Cluster>` object.

Update an existing Cluster
--------------------------

After creating the cluster object, make an `UpdateCluster`_ API request
with :meth:`update() <gcloud.bigtable.cluster.Cluster.update>`:

.. code:: python

    client.display_name = 'New display_name'
    cluster.update()

Delete an existing Cluster
--------------------------

Make a `DeleteCluster`_ API request with
:meth:`delete() <gcloud.bigtable.cluster.Cluster.delete>`:

.. code:: python

    cluster.delete()

Undelete a deleted Cluster
--------------------------

Make an `UndeleteCluster`_ API request with
:meth:`undelete() <gcloud.bigtable.cluster.Cluster.undelete>`:

.. code:: python

    cluster.undelete()

Next Step
---------

Now we go down the hierarchy from
:class:`Cluster <gcloud.bigtable.cluster.Cluster>` to a
:class:`Table <gcloud.bigtable.table.Table>`.

Head next to learn about the :doc:`bigtable-table-api`.

.. _Cluster Admin API: https://cloud.google.com/bigtable/docs/creating-cluster
.. _CreateCluster: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/cluster/v1/bigtable_cluster_service.proto#L66-L68
.. _GetCluster: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/cluster/v1/bigtable_cluster_service.proto#L38-L40
.. _UpdateCluster: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/cluster/v1/bigtable_cluster_service.proto#L93-L95
.. _DeleteCluster: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/cluster/v1/bigtable_cluster_service.proto#L109-L111
.. _ListZones: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/cluster/v1/bigtable_cluster_service.proto#L33-L35
.. _ListClusters: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/cluster/v1/bigtable_cluster_service.proto#L44-L46
.. _GetOperation: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/longrunning/operations.proto#L43-L45
.. _UndeleteCluster: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/cluster/v1/bigtable_cluster_service.proto#L126-L128
.. _long-running operation: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/longrunning/operations.proto#L73-L102
