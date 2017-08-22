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

    snapshot = session.snapshot()

You can also specify a weaker bound, which can either be to perform all
reads as of a given timestamp:

.. code:: python

    import datetime
    from pytz import UTC
    TIMESTAMP = datetime.utcnow().replace(tzinfo=UTC)
    snapshot = session.snapshot(read_timestamp=TIMESTAMP)

or as of a given duration in the past:

.. code:: python

    import datetime
    DURATION = datetime.timedelta(seconds=5)
    snapshot = session.snapshot(exact_staleness=DURATION)


Read Table Data
---------------

Read data for selected rows from a table in the session's database.  Calls
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

   The result set returned by
   :meth:`~google.cloud.spanner.snapshot.Snapshot.execute_sql` *must not* be
   iterated after the snapshot's session has been returned to the database's
   session pool.  Therefore, unless your application creates sessions
   manually, perform all iteration within the context of  the
   ``with database.snapshot()`` block.

.. note::

   If streaming a chunk raises an exception, the application can
   retry the ``read``, passing the ``resume_token`` from ``StreamingResultSet``
   which raised the error.  E.g.:

   .. code:: python

      result = snapshot.read(table, columns, keys)
      while True:
          try:
              for row in result.rows:
                  print row
          except Exception:
               result = snapshot.read(
                  table, columns, keys, resume_token=result.resume_token)
               continue
          else:
              break



Execute a SQL Select Statement
------------------------------

Read data from a query against tables in the session's database.  Calls
the ``ExecuteSql`` API, which returns all rows matching the query, or else
fails if the result set is too large,

.. code:: python

    with database.snapshot() as snapshot:
        QUERY = (
            'SELECT e.first_name, e.last_name, p.telephone '
            'FROM employees as e, phones as p '
            'WHERE p.employee_id == e.employee_id')
        result = snapshot.execute_sql(QUERY)

        for row in result.rows:
            print(row)

.. note::

   The result set returned by
   :meth:`~google.cloud.spanner.snapshot.Snapshot.execute_sql` *must not* be
   iterated after the snapshot's session has been returned to the database's
   session pool.  Therefore, unless your application creates sessions
   manually, perform all iteration within the context of  the
   ``with database.snapshot()`` block.

.. note::

   If streaming a chunk raises an exception, the application can
   retry the query, passing the ``resume_token`` from ``StreamingResultSet``
   which raised the error.  E.g.:

   .. code:: python

      result = snapshot.execute_sql(QUERY)
      while True:
          try:
              for row in result.rows:
                  print row
          except Exception:
               result = snapshot.execute_sql(
                  QUERY, resume_token=result.resume_token)
               continue
          else:
              break


Next Step
---------

Next, learn about :doc:`transaction-usage`.
