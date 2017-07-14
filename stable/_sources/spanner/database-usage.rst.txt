Database Admin API
==================

After creating a :class:`~google.cloud.spanner.instance.Instance`, you can
interact with individual databases for that instance.


List Databases
--------------

To list of all existing databases for an instance, use its
:meth:`~google.cloud.spanner.instance.Instance.list_databases` method:

.. code:: python

    databases, token = instance.list_databases()


Database Factory
----------------

To create a :class:`~google.cloud.spanner.database.Database` object:

.. code:: python

    database = instance.database(database_id, ddl_statements)

- ``ddl_statements`` is a string containing DDL for the new database.

You can also use :meth:`Instance.database` to create a local wrapper for
a database that has already been created:

.. code:: python

    database = instance.database(existing_database_id)


Create a new Database
---------------------

After creating the database object, use its
:meth:`~google.cloud.spanner.database.Database.create` method to
trigger its creation on the server:

.. code:: python

    operation = database.create()

.. note::

    Creating an instance triggers a "long-running operation" and
    returns an :class:`google.cloud.spanner.database.Operation`
    object.  See :ref:`check-on-current-database-operation` for polling
    to find out if the operation is completed.


Update an existing Database
---------------------------

After creating the database object, you can apply additional DDL statements
via its :meth:`~google.cloud.spanner.database.Database.update_ddl` method:

.. code:: python

    operation = instance.update_ddl(ddl_statements, operation_id)

- ``ddl_statements`` is a string containing DDL to be applied to
  the database.

- ``operation_id`` is a string ID for the long-running operation.

.. note::

    Update an instance triggers a "long-running operation" and
    returns a :class:`google.cloud.spanner.database.Operation`
    object.  See :ref:`check-on-current-database-operation` for polling
    to find out if the operation is completed.


Drop a Database
---------------

Drop a databse using its
:meth:`~google.cloud.spanner.database.Database.drop` method:

.. code:: python

    database.drop()


.. _check-on-current-database-operation:

Check on Current Database Operation
-----------------------------------

The :meth:`~google.cloud.spanner.database.Database.create` and
:meth:`~google.cloud.spanner.database.Database.update` methods of instance
object trigger long-running operations on the server, and return instances
of the :class:`~google.cloud.spanner.database.Operation` class.

You can check if a long-running operation has finished
by using its :meth:`~google.cloud.spanner.database.Operation.finished`
method:

.. code:: python

    >>> operation = instance.create()
    >>> operation.finished()
    True

.. note::

    Once an :class:`~google.cloud.spanner.instance.Operation` object
    has returned :data:`True` from its
    :meth:`~google.cloud.spanner.instance.Operation.finished` method, the
    object should not be re-used. Subsequent calls to
    :meth:`~google.cloud.spanner.instance.Operation.finished`
    will result in an :exc`ValueError` being raised.


Next Step
---------

Next, learn about :doc:`session-crud-usage`.
