Instance Admin API
==================

After creating a :class:`Client <google.cloud.bigtable.client.Client>`, you can
interact with individual instances for a project.

List Instances
--------------

If you want a comprehensive list of all existing instances, make a
`ListInstances`_ API request with
:meth:`Client.list_instances() <google.cloud.bigtable.client.Client.list_instances>`:

.. code:: python

    instances = client.list_instances()

Instance Factory
----------------

To create an :class:`Instance <google.cloud.bigtable.instance.Instance>` object:

.. code:: python

    instance = client.instance(instance_id, location_id,
                               display_name=display_name)

- ``location_id`` is the ID of the location in which the instance's cluster
  will be hosted, e.g.  ``'us-central1-c'``.  ``location_id`` is required for
  instances which do not already exist.

- ``display_name`` is optional. When not provided, ``display_name`` defaults
  to the ``instance_id`` value.

You can also use :meth:`Client.instance` to create a local wrapper for
instances that have already been created with the API, or through the web
console:

.. code:: python

    instance = client.instance(existing_instance_id)
    instance.reload()

Create a new Instance
---------------------

After creating the instance object, make a `CreateInstance`_ API request
with :meth:`create() <google.cloud.bigtable.instance.Instance.create>`:

.. code:: python

    instance.display_name = 'My very own instance'
    instance.create()

Check on Current Operation
--------------------------

.. note::

    When modifying an instance (via a `CreateInstance`_ request), the Bigtable
    API will return a `long-running operation`_ and a corresponding
    :class:`Operation <google.cloud.bigtable.instance.Operation>` object
    will be returned by
    :meth:`create() <google.cloud.bigtable.instance.Instance.create>`.

You can check if a long-running operation (for a
:meth:`create() <google.cloud.bigtable.instance.Instance.create>` has finished
by making a `GetOperation`_ request with
:meth:`Operation.finished() <google.cloud.bigtable.instance.Operation.finished>`:

.. code:: python

    >>> operation = instance.create()
    >>> operation.finished()
    True

.. note::

    Once an :class:`Operation <google.cloud.bigtable.instance.Operation>` object
    has returned :data:`True` from
    :meth:`finished() <google.cloud.bigtable.instance.Operation.finished>`, the
    object should not be re-used. Subsequent calls to
    :meth:`finished() <google.cloud.bigtable.instance.Operation.finished>`
    will result in a :class:`ValueError <exceptions.ValueError>`.

Get metadata for an existing Instance
-------------------------------------

After creating the instance object, make a `GetInstance`_ API request
with :meth:`reload() <google.cloud.bigtable.instance.Instance.reload>`:

.. code:: python

    instance.reload()

This will load ``display_name`` for the existing ``instance`` object.

Update an existing Instance
---------------------------

After creating the instance object, make an `UpdateInstance`_ API request
with :meth:`update() <google.cloud.bigtable.instance.Instance.update>`:

.. code:: python

    client.display_name = 'New display_name'
    instance.update()

Delete an existing Instance
---------------------------

Make a `DeleteInstance`_ API request with
:meth:`delete() <google.cloud.bigtable.instance.Instance.delete>`:

.. code:: python

    instance.delete()

Next Step
---------

Now we go down the hierarchy from
:class:`Instance <google.cloud.bigtable.instance.Instance>` to a
:class:`Table <google.cloud.bigtable.table.Table>`.

Head next to learn about the :doc:`table-api`.

.. _Instance Admin API: https://cloud.google.com/bigtable/docs/creating-instance
.. _CreateInstance: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/instance/v1/bigtable_instance_service.proto#L66-L68
.. _GetInstance: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/instance/v1/bigtable_instance_service.proto#L38-L40
.. _UpdateInstance: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/instance/v1/bigtable_instance_service.proto#L93-L95
.. _DeleteInstance: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/instance/v1/bigtable_instance_service.proto#L109-L111
.. _ListInstances: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/admin/instance/v1/bigtable_instance_service.proto#L44-L46
.. _GetOperation: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/longrunning/operations.proto#L43-L45
.. _long-running operation: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/longrunning/operations.proto#L73-L102
