Table Factory
-------------

To create a :class:`Table <google.cloud.bigtable.table.Table>` object:

.. code:: python

    table = instance.table(table_id)

Even if this :class:`Table <google.cloud.bigtable.table.Table>` already
has been created with the API, you'll want this object to use as a
:class:`Row <google.cloud.bigtable.row.Row>`.

Next Step
---------

Now we go down the final step of the hierarchy from
:class:`Table <google.cloud.bigtable.table.Table>` to
:class:`Row <google.cloud.bigtable.row.Row>` as well as streaming
data directly via a :class:`Table <google.cloud.bigtable.table.Table>`.

Head next to learn about the :doc:`data-api`.
