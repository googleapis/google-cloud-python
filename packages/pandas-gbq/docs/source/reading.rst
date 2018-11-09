.. _reader:

Reading Tables
==============

Suppose you want to load all data from an existing BigQuery table
``test_dataset.test_table`` into a DataFrame using the
:func:`~pandas_gbq.read_gbq` function.

.. code-block:: python

   # Insert your BigQuery Project ID Here
   # Can be found in the Google web console
   projectid = "xxxxxxxx"

   data_frame = read_gbq('SELECT * FROM test_dataset.test_table', projectid)


You can define which column from BigQuery to use as an index in the
destination DataFrame as well as a preferred column order as follows:

.. code-block:: python

   data_frame = read_gbq('SELECT * FROM test_dataset.test_table',
                          index_col='index_column_name',
                          col_order=['col1', 'col2', 'col3'], projectid)


You can specify the query config as parameter to use additional options of
your job. For more information about query configuration parameters see `here
<https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query>`__.

.. code-block:: python

   configuration = {
      'query': {
        "useQueryCache": False
      }
   }
   data_frame = read_gbq('SELECT * FROM test_dataset.test_table',
                          configuration=configuration, projectid)


.. note::

   You can find your project id in the `Google developers console
   <https://console.developers.google.com>`__.


.. note::

    The ``dialect`` argument can be used to indicate whether to use BigQuery's ``'legacy'`` SQL
    or BigQuery's ``'standard'`` SQL (beta). The default value is ``'legacy'``, though this will change
    in a subsequent release to ``'standard'``. For more information
    on BigQuery's standard SQL, see `BigQuery SQL Reference
    <https://cloud.google.com/bigquery/sql-reference/>`__
