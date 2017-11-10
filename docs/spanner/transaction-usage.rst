Read-write Transactions
#######################

A :class:`~google.cloud.spanner.transaction.Transaction` represents a
transaction:  when the transaction commits, it will send any accumulated
mutations to the server.

To understand more about how transactions work, visit :ref:`spanner-txn`.
To learn more about how to use them in the Python client, continue reading.


Begin a Transaction
-------------------

To begin using a transaction:

.. code:: python

    transaction = session.transaction()


Read Table Data
---------------

Read data for selected rows from a table in the session's database.  Calls
the ``Read`` API, which returns all rows specified in ``key_set``, or else
fails if the result set is too large,

.. code:: python

    result = transaction.read(
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
    result = transaction.execute_sql(QUERY)

    for row in result.rows:
        print(row)


Insert records using a Transaction
----------------------------------

:meth:`Transaction.insert` adds one or more new records to a table.  Fails if
any of the records already exists.

.. code:: python

    transaction.insert(
        'citizens', columns=['email', 'first_name', 'last_name', 'age'],
        values=[
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ])

.. note::

    Ensure that data being sent for ``STRING`` columns uses a text string
    (``str`` in Python 3; ``unicode`` in Python 2).

    Additionally, if you are writing data intended for a ``BYTES`` column, you
    must base64 encode it.


Update records using a Transaction
----------------------------------

:meth:`Transaction.update` updates one or more existing records in a table.  Fails
if any of the records does not already exist.

.. code:: python

    transaction.update(
        'citizens', columns=['email', 'age'],
        values=[
            ['phred@exammple.com', 33],
            ['bharney@example.com', 32],
        ])

.. note::

    Ensure that data being sent for ``STRING`` columns uses a text string
    (``str`` in Python 3; ``unicode`` in Python 2).

    Additionally, if you are writing data intended for a ``BYTES`` column, you
    must base64 encode it.


Insert or update records using a Transaction
--------------------------------------------

:meth:`Transaction.insert_or_update` inserts *or* updates one or more records
in a table.  Existing rows have values for the supplied columns overwritten;
other column values are preserved.

.. code:: python

    transaction.insert_or_update(
        'citizens', columns=['email', 'first_name', 'last_name', 'age'],
        values=[
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 31],
            ['wylma@example.com', 'Wylma', 'Phlyntstone', 29],
        ])

.. note::

    Ensure that data being sent for ``STRING`` columns uses a text string
    (``str`` in Python 3; ``unicode`` in Python 2).

    Additionally, if you are writing data intended for a ``BYTES`` column, you
    must base64 encode it.


Replace records using a Transaction
-----------------------------------

:meth:`Transaction.replace` inserts *or* updates one or more records in a
table.  Existing rows have values for the supplied columns overwritten;  other
column values are set to null.

.. code:: python

    transaction.replace(
        'citizens', columns=['email', 'first_name', 'last_name', 'age'],
        values=[
            ['bharney@example.com', 'Bharney', 'Rhubble', 30],
            ['bhettye@example.com', 'Bhettye', 'Rhubble', 30],
        ])

.. note::

    Ensure that data being sent for ``STRING`` columns uses a text string
    (``str`` in Python 3; ``unicode`` in Python 2).

    Additionally, if you are writing data intended for a ``BYTES`` column, you
    must base64 encode it.


Delete records using a Transaction
----------------------------------

:meth:`Transaction.delete` removes one or more records from a table.
Non-existent rows do not cause errors.

.. code:: python

    transaction.delete(
        'citizens', keyset=['bharney@example.com', 'nonesuch@example.com'])


Commit changes for a Transaction
--------------------------------

After describing the modifications to be made to table data via the
:meth:`Transaction.insert`, :meth:`Transaction.update`,
:meth:`Transaction.insert_or_update`, :meth:`Transaction.replace`, and
:meth:`Transaction.delete` methods above, send them to
the back-end by calling :meth:`Transaction.commit`, which makes the ``Commit``
API call.

.. code:: python

    transaction.commit()


Roll back changes for a Transaction
-----------------------------------

After describing the modifications to be made to table data via the
:meth:`Transaction.insert`, :meth:`Transaction.update`,
:meth:`Transaction.insert_or_update`, :meth:`Transaction.replace`, and
:meth:`Transaction.delete` methods above, cancel the transaction on the
the back-end by calling :meth:`Transaction.rollback`, which makes the
``Rollback`` API call.

.. code:: python

    transaction.rollback()


Use a Transaction as a Context Manager
--------------------------------------

Rather than calling :meth:`Transaction.commit` or :meth:`Transaction.rollback`
manually, you can use the :class:`Transaction` instance as a context manager:
in that case, the transaction's :meth:`~Transaction.commit` method will
called automatically if the ``with`` block exits without raising an exception.

If an exception is raised inside the ``with`` block, the transaction's
:meth:`~Transaction.rollback` method will be called instead.

.. code:: python

    with session.transaction() as transaction

        transaction.insert(
            'citizens', columns=['email', 'first_name', 'last_name', 'age'],
            values=[
                ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
                ['bharney@example.com', 'Bharney', 'Rhubble', 31],
            ])

        transaction.update(
            'citizens', columns=['email', 'age'],
            values=[
                ['phred@exammple.com', 33],
                ['bharney@example.com', 32],
            ])

        ...

        transaction.delete('citizens',
            keyset['bharney@example.com', 'nonesuch@example.com'])
