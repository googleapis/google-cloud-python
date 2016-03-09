Bigtable Row
============

It is possible to use a :class:`RowFilter <gcloud.bigtable.row.RowFilter>`
when adding mutations to a
:class:`ConditionalRow <gcloud.bigtable.row.ConditionalRow>` and when
reading row data with :meth:`read_row() <gcloud.bigtable.table.Table.read_row>`
:meth:`read_rows() <gcloud.bigtable.table.Table.read_rows>`.

As laid out in the `RowFilter definition`_, the following basic filters
are provided:

* :class:`SinkFilter <.row.SinkFilter>`
* :class:`PassAllFilter <.row.PassAllFilter>`
* :class:`BlockAllFilter <.row.BlockAllFilter>`
* :class:`RowKeyRegexFilter <.row.RowKeyRegexFilter>`
* :class:`RowSampleFilter <.row.RowSampleFilter>`
* :class:`FamilyNameRegexFilter <.row.FamilyNameRegexFilter>`
* :class:`ColumnQualifierRegexFilter <.row.ColumnQualifierRegexFilter>`
* :class:`TimestampRangeFilter <.row.TimestampRangeFilter>`
* :class:`ColumnRangeFilter <.row.ColumnRangeFilter>`
* :class:`ValueRegexFilter <.row.ValueRegexFilter>`
* :class:`ValueRangeFilter <.row.ValueRangeFilter>`
* :class:`CellsRowOffsetFilter <.row.CellsRowOffsetFilter>`
* :class:`CellsRowLimitFilter <.row.CellsRowLimitFilter>`
* :class:`CellsColumnLimitFilter <.row.CellsColumnLimitFilter>`
* :class:`StripValueTransformerFilter <.row.StripValueTransformerFilter>`
* :class:`ApplyLabelFilter <.row.ApplyLabelFilter>`

In addition, these filters can be combined into composite filters with

* :class:`RowFilterChain <.row.RowFilterChain>`
* :class:`RowFilterUnion <.row.RowFilterUnion>`
* :class:`ConditionalRowFilter <.row.ConditionalRowFilter>`

These rules can be nested arbitrarily, with a basic filter at the lowest
level. For example:

.. code:: python

    # Filter in a specified column (matching any column family).
    col1_filter = ColumnQualifierRegexFilter(b'columnbia')

    # Create a filter to label results.
    label1 = u'label-red'
    label1_filter = ApplyLabelFilter(label1)

    # Combine the filters to label all the cells in columnbia.
    chain1 = RowFilterChain(filters=[col1_filter, label1_filter])

    # Create a similar filter to label cells blue.
    col2_filter = ColumnQualifierRegexFilter(b'columnseeya')
    label2 = u'label-blue'
    label2_filter = ApplyLabelFilter(label2)
    chain2 = RowFilterChain(filters=[col2_filter, label2_filter])

    # Bring our two labeled columns together.
    row_filter = RowFilterUnion(filters=[chain1, chain2])

----

.. automodule:: gcloud.bigtable.row
  :members:
  :undoc-members:
  :show-inheritance:

.. _RowFilter definition: https://github.com/GoogleCloudPlatform/cloud-bigtable-client/blob/1ff247c2e3b7cd0a2dd49071b2d95beaf6563092/bigtable-protos/src/main/proto/google/bigtable/v1/bigtable_data.proto#L195
