Working with BigQuery STRUCT data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The BigQuery `STRUCT data type
<https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#struct_type>`_
provided data that are collections of named fields.

`sqlalchemy-bigquery` provided a STRUCT type that can be used to
define tables with STRUCT columns:

.. literalinclude:: samples/snippets/STRUCT.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_sqlalchemy_create_table_with_struct]
   :end-before: [END bigquery_sqlalchemy_create_table_with_struct]

`STRUCT` types can be nested, as in this example.  Struct fields can
be defined in two ways:

- Fields can be provided as keyword arguments, as in the `cylinder`
  and `horsepower` fields in this example.

- Fields can be provided as name-type tuples provided as positional
  arguments, as with the `count` and `compression` fields in this example.

STRUCT columns are automatically created when existing database tables
containing STRUCT columns are introspected.

Struct data are represented in Python as Python dictionaries:

.. literalinclude:: samples/snippets/STRUCT.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_sqlalchemy_insert_struct]
   :end-before: [END bigquery_sqlalchemy_insert_struct]

When querying struct fields, you can use attribute access syntax:

.. literalinclude:: samples/snippets/STRUCT.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_sqlalchemy_query_struct]
   :end-before: [END bigquery_sqlalchemy_query_struct]

or mapping access:

.. literalinclude:: samples/snippets/STRUCT.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_sqlalchemy_query_getitem]
   :end-before: [END bigquery_sqlalchemy_query_getitem]

and field names are case insensitive:

.. literalinclude:: samples/snippets/STRUCT.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_sqlalchemy_query_STRUCT]
   :end-before: [END bigquery_sqlalchemy_query_STRUCT]

When using attribute-access syntax, field names may conflict with
column attribute names.  For example SQLAlchemy columns have `name`
and `type` attributes, among others.  When accessing a field whose name
conflicts with a column attribute name, either use mapping access, or
spell the field name with upper-case letters.




