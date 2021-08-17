Working with Geographic data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BigQuery provides a `GEOGRAPHY data type
<https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#geography_type>`_
for `working with geographic data
<https://cloud.google.com/bigquery/docs/gis-data>`_, including:

- Points,
- Linestrings,
- Polygons, and
- Collections of points, linestrings, and polygons.

Geographic data uses the `WGS84
<https://earth-info.nga.mil/#tab_wgs84-data>`_ coordinate system.

To define a geography column, use the `GEOGRAPHY` data type imported
from the `sqlalchemy_bigquery` module:

.. literalinclude:: samples/snippets/geography.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_sqlalchemy_create_table_with_geography]
   :end-before: [END bigquery_sqlalchemy_create_table_with_geography]

BigQuery has a variety of `SQL geographic functions
<https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions>`_
for working with geographic data.  Among these are functions for
converting between SQL geometry objects and `standard text (WKT) and
binary (WKB) representations
<https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>`_.

Geography data is typically represented in Python as text strings in
WKT format or as `WKB` objects, which contain binary data in WKB
format.  Querying geographic data returns `WKB` objects and `WKB`
objects may be used in queries.  When
calling spatial functions that expect geographic arguments, text
arguments are automatically coerced to geography.

Inserting data
~~~~~~~~~~~~~~

When inserting geography data, you can pass WKT strings, `WKT` objects,
or `WKB` objects:

.. literalinclude:: samples/snippets/geography.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_sqlalchemy_insert_geography]
   :end-before: [END bigquery_sqlalchemy_insert_geography]

Note that in the `lake3` example, we got a `WKB` object by creating a
`WKT` object and getting its `wkb` property.  Normally, we'd get `WKB`
objects as results of previous queries.

Queries
~~~~~~~

When performing spacial queries, and geography objects are expected,
you can to pass `WKB` or `WKT` objects:

.. literalinclude:: samples/snippets/geography.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_sqlalchemy_query_geography_wkb]
   :end-before: [END bigquery_sqlalchemy_query_geography_wkb]

In this example, we passed the `geog` attribute of `lake2`, which is a WKB object.

Or you can pass strings in WKT format:

.. literalinclude:: samples/snippets/geography.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_sqlalchemy_query_geography_text]
   :end-before: [END bigquery_sqlalchemy_query_geography_text]

Installing geography support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get geography support, you need to install `sqlalchemy-bigquery`
with the `geography` extra, or separately install `GeoAlchemy2` and
`shapely`.

.. code-block:: console

    pip install 'sqlalchemy-bigquery[geography]'
