Using the db-dtypes package
---------------------------

Importing the :mod:`db_dtypes` module registers the extension dtypes for use
in pandas.

Construct a date :class:`~pandas.Series` with strings in ``YYYY-MM-DD`` format
or :class:`datetime.date` objects.

.. literalinclude:: samples/snippets/pandas_date_and_time.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_pandas_date_create]
   :end-before: [END bigquery_pandas_date_create]

Working with dates
^^^^^^^^^^^^^^^^^^

Convert a date :class:`~pandas.Series` to a ``datetime64`` Series with
:meth:`~pandas.Series.astype`. The resulting values use midnight as the
time part.

.. literalinclude:: samples/snippets/pandas_date_and_time.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_pandas_date_as_datetime]
   :end-before: [END bigquery_pandas_date_as_datetime]

Just like ``datetime64`` values, date values can be subtracted. This is
equivalent to first converting to ``datetime64`` and then subtracting.

.. literalinclude:: samples/snippets/pandas_date_and_time.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_pandas_date_sub]
   :end-before: [END bigquery_pandas_date_sub]

Just like ``datetime64`` values, :class:`~pandas.tseries.offsets.DateOffset`
values can be added to them.

.. literalinclude:: samples/snippets/pandas_date_and_time.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_pandas_date_add_offset]
   :end-before: [END bigquery_pandas_date_add_offset]


Working with times
^^^^^^^^^^^^^^^^^^

Construct a time :class:`~pandas.Series` with strings in ``HH:MM:SS.fraction``
24-hour format or :class:`datetime.time` objects.

.. literalinclude:: samples/snippets/pandas_date_and_time.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_pandas_time_create]
   :end-before: [END bigquery_pandas_time_create]

Convert a time :class:`~pandas.Series` to a ``timedelta64`` Series with
:meth:`~pandas.Series.astype`.

.. literalinclude:: samples/snippets/pandas_date_and_time.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_pandas_time_as_timedelta]
   :end-before: [END bigquery_pandas_time_as_timedelta]


Combining dates and times
^^^^^^^^^^^^^^^^^^^^^^^^^

Combine a date :class:`~pandas.Series` with a time :class:`~pandas.Series` to
create a ``datetime64`` :class:`~pandas.Series`.

   .. literalinclude:: samples/snippets/pandas_date_and_time.py
      :language: python
      :dedent: 4
      :start-after: [START bigquery_pandas_combine_date_time]
      :end-before: [END bigquery_pandas_combine_date_time]
