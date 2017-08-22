Batching Modifications
######################

A :class:`~google.cloud.spanner.batch.Batch` represents a set of data
modification operations to be performed on tables in a dataset.  Use of a
``Batch`` does not require creating an explicit
:class:`~google.cloud.spanner.snapshot.Snapshot` or
:class:`~google.cloud.spanner.transaction.Transaction`.  Until
:meth:`~google.cloud.spanner.batch.Batch.commit` is called on a ``Batch``,
no changes are propagated to the back-end.


Starting a Batch
----------------

.. code:: python

    batch = session.batch()


Inserting records using a Batch
-------------------------------

:meth:`Batch.insert` adds one or more new records to a table.  Fails if
any of the records already exists.

.. code:: python

    batch.insert(
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


Update records using a Batch
-------------------------------

:meth:`Batch.update` updates one or more existing records in a table.  Fails
if any of the records does not already exist.

.. code:: python

    batch.update(
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


Insert or update records using a Batch
--------------------------------------

:meth:`Batch.insert_or_update` inserts *or* updates one or more records in a
table.  Existing rows have values for the supplied columns overwritten;  other
column values are preserved.

.. code:: python

    batch.insert_or_update(
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


Replace records using a Batch
-----------------------------

:meth:`Batch.replace` inserts *or* updates one or more records in a
table.  Existing rows have values for the supplied columns overwritten;  other
column values are set to null.

.. code:: python

    batch.replace(
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


Delete records using a Batch
----------------------------

:meth:`Batch.delete` removes one or more records from a table.  Non-existent
rows do not cause errors.

.. code:: python

    from google.cloud.spanner.keyset import KeySet

    to_delete = KeySet(keys=[
        ('bharney@example.com',)
        ('nonesuch@example.com',)
    ])

    batch.delete('citizens', to_delete)


Commit changes for a Batch
--------------------------

After describing the modifications to be made to table data via the
:meth:`Batch.insert`, :meth:`Batch.update`, :meth:`Batch.insert_or_update`,
:meth:`Batch.replace`, and :meth:`Batch.delete` methods above, send them to
the back-end by calling :meth:`Batch.commit`, which makes the ``Commit``
API call.

.. code:: python

    batch.commit()


Use a Batch as a Context Manager
--------------------------------

Rather than calling :meth:`Batch.commit` manually, you can use the
:class:`Batch` instance as a context manager, and have it called automatically
if the ``with`` block exits without raising an exception.

.. code:: python

    from google.cloud.spanner.keyset import KeySet

    to_delete = KeySet(keys=[
        ('bharney@example.com',)
        ('nonesuch@example.com',)
    ])

    with session.batch() as batch:

        batch.insert(
            'citizens', columns=['email', 'first_name', 'last_name', 'age'],
            values=[
                ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
                ['bharney@example.com', 'Bharney', 'Rhubble', 31],
            ])

        batch.update(
            'citizens', columns=['email', 'age'],
            values=[
                ['phred@exammple.com', 33],
                ['bharney@example.com', 32],
            ])

        ...

        batch.delete('citizens', to_delete)


Next Step
---------

Next, learn about :doc:`snapshot-usage`.
