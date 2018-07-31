Read-only Transactions via Snapshots
####################################

A :class:`~google.cloud.spanner.snapshot.Snapshot` represents a read-only
transaction:  when multiple read operations are peformed via a Snapshot,
the results are consistent as of a particular point in time.


Beginning a Snapshot
--------------------

To begin using a snapshot using the default "bound" (which is "strong"),
meaning all reads are performed at a timestamp where all previously-committed
transactions are visible:

.. code:: python

    snapshot = database.snapshot()

You can also specify a weaker bound, which can either be to perform all
reads as of a given timestamp:

.. code:: python

    import datetime
    from pytz import UTC
    TIMESTAMP = datetime.datetime.utcnow().replace(tzinfo=UTC)
    snapshot = database.snapshot(read_timestamp=TIMESTAMP)

or as of a given duration in the past:

.. code:: python

    import datetime
    DURATION = datetime.timedelta(seconds=5)
    snapshot = database.snapshot(exact_staleness=DURATION)

Single Use and Multiple Use Snapshots
-------------------------------------

In the context of read only transactions, ``read`` and ``execute_sql``
methods can be used multiple times if you specify ``multi_use=True``
in the constructor of the snapshot.  However, ``multi_use=True`` is
incompatible with either ``max_staleness`` and/or ``min_read_timestamp``.

Otherwise ``multi_use`` defaults to ``False`` and the snapshot cannot be
reused.

.. code:: python

    snapshot = database.snapshot(multi_use=True)

:meth:`~.spanner_v1.snapshot.Snapshot.begin` can only be used on a
snapshot with ``multi_use=True``.  In which case it is also necessary
to call if you need to have multiple pending operations.

Read Table Data
---------------

Read data for selected rows from a table in the database.  Calls
the ``Read`` API, which returns all rows specified in ``key_set``, or else
fails if the result set is too large,

.. code:: python

    with database.snapshot() as snapshot:
        result = snapshot.read(
            table='table-name', columns=['first_name', 'last_name', 'age'],
            key_set=['phred@example.com', 'bharney@example.com'])

        for row in result.rows:
            print(row)

.. note::

   Perform all iteration within the context of the ``with database.snapshot()``
   block.


Execute a SQL Select Statement
------------------------------

Read data from a query against tables in the database.  Calls
the ``ExecuteSql`` API, which returns all rows matching the query, or else
fails if the result set is too large,

.. code:: python

    with database.snapshot() as snapshot:
        QUERY = (
            'SELECT e.first_name, e.last_name, p.telephone '
            'FROM employees as e, phones as p '
            'WHERE p.employee_id == e.employee_id')
        result = snapshot.execute_sql(QUERY)

        for row in list(result):
            print(row)

.. note::

   Perform all iteration within the context of the ``with database.snapshot()``
   block.


Next Step
---------

Next, learn about :doc:`transaction-usage`.
