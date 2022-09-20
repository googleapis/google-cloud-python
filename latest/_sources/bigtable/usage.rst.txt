Using the API
=============

.. toctree::
  :maxdepth: 2

  client-intro
  client
  cluster
  instance
  table
  column-family
  row
  row-data
  row-filters


In the hierarchy of API concepts

* a :class:`Client <google.cloud.bigtable.client.Client>` owns an
  :class:`Instance <google.cloud.bigtable.instance.Instance>`
* an :class:`Instance <google.cloud.bigtable.instance.Instance>` owns a
  :class:`Table <google.cloud.bigtable.table.Table>`
* a :class:`Table <google.cloud.bigtable.table.Table>` owns a
  :class:`ColumnFamily <google.cloud.bigtable.column_family.ColumnFamily>`
* a :class:`Table <google.cloud.bigtable.table.Table>` owns a
  :class:`Row <google.cloud.bigtable.row.Row>`
  (and all the cells in the row)
