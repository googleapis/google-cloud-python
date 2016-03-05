Data API
========

After creating a :class:`Table <gcloud.bigtable.table.Table>` and some
column families, you are ready to store and retrieve data.

Cells vs. Columns vs. Column Families
+++++++++++++++++++++++++++++++++++++

* As explained in the :doc:`table overview <bigtable-table-api>`, tables can
  have many column families.
* As described below, a table can also have many rows which are
  specified by row keys.
* Within a row, data is stored in a cell. A cell simply has a value (as
  bytes) and a timestamp. The number of cells in each row can be
  different, depending on what was stored in each row.
* Each cell lies in a column (**not** a column family). A column is really
  just a more **specific** modifier within a column family. A column
  can be present in every column family, in only one or anywhere in between.
* Within a column family there can be many columns. For example within
  the column family ``foo`` we could have columns ``bar`` and ``baz``.
  These would typically be represented as ``foo:bar`` and ``foo:baz``.

Modifying Data
++++++++++++++

Since data is stored in cells, which are stored in rows, the
:class:`Row <gcloud.bigtable.row.Row>` class is the only class used to
modify (write, update, delete) data in a
:class:`Table <gcloud.bigtable.table.Table>`.

Row Factory
-----------

To create a :class:`Row <gcloud.bigtable.row.Row>` object

.. code:: python

    row = table.row(row_key)

Unlike the previous string values we've used before, the row key must
be ``bytes``.

Direct vs. Conditional vs. Append
---------------------------------

There are three ways to modify data in a table, described by the
`MutateRow`_, `CheckAndMutateRow`_ and `ReadModifyWriteRow`_ API
methods.

* The **direct** way is via `MutateRow`_ which involves simply
  adding, overwriting or deleting cells.
* The **conditional** way is via `CheckAndMutateRow`_. This method
  first checks if some filter is matched in a a given row, then
  applies one of two sets of mutations, depending on if a match
  occurred or not. (These mutation sets are called the "true
  mutations" and "false mutations".)
* The **append** way is via `ReadModifyWriteRow`_. This simply
  appends (as bytes) or increments (as an integer) data in a presumed
  existing cell in a row.

Building Up Mutations
---------------------

In all three cases, a set of mutations (or two sets) are built up
on a :class:`Row <gcloud.bigtable.row.Row>` before they are sent of
in a batch via :meth:`commit() <gcloud.bigtable.row.Row.commit>`:

.. code:: python

    row.commit()

To send **append** mutations in batch, use
:meth:`commit_modifications() <gcloud.bigtable.row.Row.commit_modifications>`:

.. code:: python

    row.commit_modifications()

We have a small set of methods on the :class:`Row <gcloud.bigtable.row.Row>`
to build these mutations up.

Direct Mutations
----------------

Direct mutations can be added via one of four methods

* :meth:`set_cell() <gcloud.bigtable.row.Row.set_cell>` allows a
  single value to be written to a column

  .. code:: python

      row.set_cell(column_family_id, column, value,
                   timestamp=timestamp)

  If the ``timestamp`` is omitted, the current time on the Google Cloud
  Bigtable server will be used when the cell is stored.

  The value can either by bytes or an integer (which will be converted to
  bytes as an unsigned 64-bit integer).

* :meth:`delete_cell() <gcloud.bigtable.row.Row.delete_cell>` deletes
  all cells (i.e. for all timestamps) in a given column

  .. code:: python

      row.delete_cell(column_family_id, column)

  Remember, this only happens in the ``row`` we are using.

  If we only want to delete cells from a limited range of time, a
  :class:`TimestampRange <gcloud.bigtable.row.TimestampRange>` can
  be used

  .. code:: python

      row.delete_cell(column_family_id, column,
                      time_range=time_range)

* :meth:`delete_cells() <gcloud.bigtable.row.Row.delete_cells>` does
  the same thing as :meth:`delete_cell() <gcloud.bigtable.row.Row.delete_cell>`
  but accepts a list of columns in a column family rather than a single one.

  .. code:: python

      row.delete_cells(column_family_id, [column1, column2],
                       time_range=time_range)

  In addition, if we want to delete cells from every column in a column family,
  the special :attr:`ALL_COLUMNS <gcloud.bigtable.row.Row.ALL_COLUMNS>` value
  can be used

  .. code:: python

      row.delete_cells(column_family_id, Row.ALL_COLUMNS,
                       time_range=time_range)

* :meth:`delete() <gcloud.bigtable.row.Row.delete>` will delete the entire row

  .. code:: python

      row.delete()

Conditional Mutations
---------------------

Making **conditional** modifications is essentially identical
to **direct** modifications, but we need to specify a filter to match
against in the row:

.. code:: python

    row = table.row(row_key, filter_=filter_val)

See the :class:`Row <gcloud.bigtable.row.Row>` class for more information
about acceptable values for ``filter_``.

The only other difference from **direct** modifications are that each mutation
added must specify a ``state``: will the mutation be applied if the filter
matches or if it fails to match.

For example:

.. code:: python

    row.set_cell(column_family_id, column, value,
                 timestamp=timestamp, state=True)

will add to the set of true mutations.

.. note::

    If ``state`` is passed when no ``filter_`` is set on a
    :class:`Row <gcloud.bigtable.row.Row>`, adding the mutation will fail.
    Similarly, if no ``state`` is passed when a ``filter_`` has been set,
    adding the mutation will fail.

Append Mutations
----------------

Append mutations can be added via one of two methods

* :meth:`append_cell_value() <gcloud.bigtable.row.Row.append_cell_value>`
  appends a bytes value to an existing cell:

  .. code:: python

      row.append_cell_value(column_family_id, column, bytes_value)

* :meth:`increment_cell_value() <gcloud.bigtable.row.Row.increment_cell_value>`
  increments an integer value in an existing cell:

  .. code:: python

      row.increment_cell_value(column_family_id, column, int_value)

  Since only bytes are stored in a cell, the cell value is decoded as
  an unsigned 64-bit integer before being incremented. (This happens on
  the Google Cloud Bigtable server, not in the library.)

Notice that no timestamp was specified. This is because **append** mutations
operate on the latest value of the specified column.

If there are no cells in the specified column, then the empty string (bytes
case) or zero (integer case) are the assumed values.

Starting Fresh
--------------

If accumulated mutations need to be dropped, use
:meth:`clear_mutations() <gcloud.bigtable.row.Row.clear_mutations>`

.. code:: python

    row.clear_mutations()

To clear **append** mutations, use
:meth:`clear_modification_rules() <gcloud.bigtable.row.Row.clear_modification_rules>`

.. code:: python

    row.clear_modification_rules()

Reading Data
++++++++++++

Read Single Row from a Table
----------------------------

To make a `ReadRows`_ API request for a single row key, use
:meth:`Table.read_row() <gcloud.bigtable.table.Table.read_row>`:

.. code:: python

    >>> row_data = table.read_row(row_key)
    >>> row_data.cells
    {
        u'fam1': {
            b'col1': [
                <gcloud.bigtable.row_data.Cell at 0x7f80d150ef10>,
                <gcloud.bigtable.row_data.Cell at 0x7f80d150ef10>,
            ],
            b'col2': [
                <gcloud.bigtable.row_data.Cell at 0x7f80d150ef10>,
            ],
        },
        u'fam2': {
            b'col3': [
                <gcloud.bigtable.row_data.Cell at 0x7f80d150ef10>,
                <gcloud.bigtable.row_data.Cell at 0x7f80d150ef10>,
                <gcloud.bigtable.row_data.Cell at 0x7f80d150ef10>,
            ],
        },
    }
    >>> cell = row_data.cells[u'fam1'][b'col1'][0]
    >>> cell
    <gcloud.bigtable.row_data.Cell at 0x7f80d150ef10>
    >>> cell.value
    b'val1'
    >>> cell.timestamp
    datetime.datetime(2016, 2, 27, 3, 41, 18, 122823, tzinfo=<UTC>)

Rather than returning a :class:`Row <gcloud.bigtable.row.Row>`, this method
returns a :class:`PartialRowData <gcloud.bigtable.row_data.PartialRowData>`
instance. This class is used for reading and parsing data rather than for
modifying data (as :class:`Row <gcloud.bigtable.row.Row>` is).

A filter can also be applied to the

.. code:: python

    row_data = table.read_row(row_key, filter_=filter_val)

The allowable ``filter_`` values are the same as those used for a
:class:`Row <gcloud.bigtable.row.Row>` with **conditional** mutations. For
more information, see the
:meth:`Table.read_row() <gcloud.bigtable.table.Table.read_row>` documentation.

Stream Many Rows from a Table
-----------------------------

To make a `ReadRows`_ API request for a stream of rows, use
:meth:`Table.read_rows() <gcloud.bigtable.table.Table.read_rows>`:

.. code:: python

    row_data = table.read_rows()

Using gRPC over HTTP/2, a continual stream of responses will be delivered.
In particular

* :meth:`consume_next() <gcloud.bigtable.row_data.PartialRowsData.consume_next>`
  pulls the next result from the stream, parses it and stores it on the
  :class:`PartialRowsData <gcloud.bigtable.row_data.PartialRowsData>` instance
* :meth:`consume_all() <gcloud.bigtable.row_data.PartialRowsData.consume_all>`
  pulls results from the stream until there are no more
* :meth:`cancel() <gcloud.bigtable.row_data.PartialRowsData.cancel>` closes
  the stream

See the :class:`PartialRowsData <gcloud.bigtable.row_data.PartialRowsData>`
documentation for more information.

As with
:meth:`Table.read_row() <gcloud.bigtable.table.Table.read_row>`, an optional
``filter_`` can be applied. In addition a ``start_key`` and / or ``end_key``
can be supplied for the stream, a ``limit`` can be set and a boolean
``allow_row_interleaving`` can be specified to allow faster streamed results
at the potential cost of non-sequential reads.

See the :meth:`Table.read_rows() <gcloud.bigtable.table.Table.read_rows>`
documentation for more information on the optional arguments.

Sample Keys in a Table
----------------------

Make a `SampleRowKeys`_ API request with
:meth:`Table.sample_row_keys() <gcloud.bigtable.table.Table.sample_row_keys>`:

.. code:: python

    keys_iterator = table.sample_row_keys()

The returned row keys will delimit contiguous sections of the table of
approximately equal size, which can be used to break up the data for
distributed tasks like mapreduces.

As with
:meth:`Table.read_rows() <gcloud.bigtable.table.Table.read_rows>`, the
returned ``keys_iterator`` is connected to a cancellable HTTP/2 stream.

The next key in the result can be accessed via

.. code:: python

    next_key = keys_iterator.next()

or all keys can be iterated over via

.. code:: python

    for curr_key in keys_iterator:
        do_something(curr_key)

Just as with reading, the stream can be canceled:

.. code:: python

    keys_iterator.cancel()

.. _ReadRows: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/v1/bigtable_service.proto#L36-L38
.. _SampleRowKeys: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/v1/bigtable_service.proto#L44-L46
.. _MutateRow: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/v1/bigtable_service.proto#L50-L52
.. _CheckAndMutateRow: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/v1/bigtable_service.proto#L62-L64
.. _ReadModifyWriteRow: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/2aae624081f652427052fb652d3ae43d8ac5bf5a/bigtable-protos/src/main/proto/google/bigtable/v1/bigtable_service.proto#L70-L72
