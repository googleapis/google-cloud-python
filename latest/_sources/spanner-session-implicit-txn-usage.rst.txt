Implicit Transactions
#####################

The following operations on a session to not require creating an explicit
:class:`~google.cloud.spanner.snapshot.Snapshot` or
:class:`~google.cloud.spanner.transaction.Transaction`.


Read Table Data
---------------

Read data for selected rows from a table in the session's database.  Calls
the ``Read`` API, which returns all rows specified in ``key_set``, or else
fails if the result set is too large,

.. code:: python

    result = session.read(
        table='table-name', columns=['first_name', 'last_name', 'age'],
        key_set=['phred@example.com', 'bharney@example.com'])

    for row in result.rows:
        print(row)

.. note::

   If streaming a chunk fails due to a "resumable" error,
   :meth:`Session.read` retries the ``StreamingRead`` API reqeust,
   passing the ``resume_token`` from the last partial result streamed.


Execute a SQL Select Statement
------------------------------

Read data from a query against tables in the session's database.  Calls
the ``ExecuteSql`` API, which returns all rows matching the query, or else
fails if the result set is too large,

.. code:: python

    QUERY = (
        'SELECT e.first_name, e.last_name, p.telephone '
        'FROM employees as e, phones as p '
        'WHERE p.employee_id == e.employee_id')
    result = session.execute_sql(QUERY)

    for row in result.rows:
        print(row)


Next Step
---------

Next, learn about :doc:`spanner-batch-usage`.
