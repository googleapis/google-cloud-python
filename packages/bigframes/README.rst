BigQuery DataFrames
===================

BigQuery DataFrames provides a Pythonic DataFrame and machine learning (ML) API
powered by the BigQuery engine.

* ``bigframes.pandas`` provides a pandas-compatible API for analytics.
* ``bigframes.ml`` provides a scikit-learn-like API for ML.

Documentation
-------------

* `BigQuery DataFrames sample notebooks <https://github.com/googleapis/python-bigquery-dataframes/tree/main/notebooks>`_
* `BigQuery DataFrames API reference <https://cloud.google.com/python/docs/reference/bigframes/latest>`_
* `BigQuery documentation <https://cloud.google.com/bigquery/docs/>`_


Quickstart
----------

Prerequisites
^^^^^^^^^^^^^

* Install the ``bigframes`` package.
* Create a Google Cloud project and billing account.
* When running locally, authenticate with application default credentials. See
  the `gcloud auth application-default login
  <https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login>`_
  reference.

Code sample
^^^^^^^^^^^

Import ``bigframes.pandas`` for a pandas-like interface. The ``read_gbq``
method accepts either a fully-qualified table ID or a SQL query.

.. code-block:: python

  import bigframes.pandas as bpd

  df1 = bpd.read_gbq("project.dataset.table")
  df2 = bpd.read_gbq("SELECT a, b, c, FROM `project.dataset.table`")

* `More code samples <https://github.com/googleapis/python-bigquery-dataframes/tree/main/samples/snippets>`_


Locations
---------
BigQuery DataFrames uses a
`BigQuery session <https://cloud.google.com/bigquery/docs/sessions-intro>`_
internally to manage metadata on the service side. This session is tied to a
`location <https://cloud.google.com/bigquery/docs/locations>`_ .
BigQuery DataFrames uses the US multi-region as the default location, but you
can use ``session_options.location`` to set a different location. Every query
in a session is executed in the location where the session was created.

If you want to reset the location of the created DataFrame or Series objects,
can reset the session by executing ``bigframes.pandas.reset_session()``.
After that, you can reuse ``bigframes.pandas.options.bigquery.location`` to
specify another location.


``read_gbq()`` requires you to specify a location if the dataset you are
querying is not in the US multi-region. If you try to read a table from another
location, you get a NotFound exception.


ML locations
------------

``bigframes.ml`` supports the same locations as BigQuery ML. BigQuery ML model
prediction and other ML functions are supported in all BigQuery regions. Support
for model training varies by region. For more information, see
`BigQuery ML locations <https://cloud.google.com/bigquery/docs/locations#bqml-loc>`_.


Data types
----------

BigQuery DataFrames supports the following numpy and pandas dtypes:

* ``numpy.dtype("O")``
* ``pandas.BooleanDtype()``
* ``pandas.Float64Dtype()``
* ``pandas.Int64Dtype()``
* ``pandas.StringDtype(storage="pyarrow")``
* ``pandas.ArrowDtype(pa.date32())``
* ``pandas.ArrowDtype(pa.time64("us"))``
* ``pandas.ArrowDtype(pa.timestamp("us"))``
* ``pandas.ArrowDtype(pa.timestamp("us", tz="UTC"))``

BigQuery DataFrames doesn’t support the following BigQuery data types:

* ``ARRAY``
* ``NUMERIC``
* ``BIGNUMERIC``
* ``INTERVAL``
* ``STRUCT``
* ``JSON``

All other BigQuery data types display as the object type.


Remote functions
----------------

BigQuery DataFrames gives you the ability to turn your custom scalar functions
into `BigQuery remote functions
<https://cloud.google.com/bigquery/docs/remote-functions>`_ . Creating a remote
function in BigQuery DataFrames creates a BigQuery remote function, a `BigQuery
connection
<https://cloud.google.com/bigquery/docs/create-cloud-resource-connection>`_ ,
and a `Cloud Functions (2nd gen) function
<https://cloud.google.com/functions/docs/concepts/overview>`_ .

BigQuery connections are created in the same location as the BigQuery
DataFrames session, using the name you provide in the custom function
definition. To view and manage connections, do the following:

1. Go to `BigQuery in the Google Cloud Console <https://console.cloud.google.com/bigquery>`__.
2. Select the project in which you created the remote function.
3. In the Explorer pane, expand that project and then expand External connections.

BigQuery remote functions are created in the dataset you specify, or
in a dataset with the name ``bigframes_temp_location``, where location is
the location used by the BigQuery DataFrames session. For example,
``bigframes_temp_us_central1``. To view and manage remote functions, do
the following:

1. Go to `BigQuery in the Google Cloud Console <https://console.cloud.google.com/bigquery>`__.
2. Select the project in which you created the remote function.
3. In the Explorer pane, expand that project, expand the dataset in which you
   created the remote function, and then expand Routines.

To view and manage Cloud Functions functions, use the
`Functions <https://console.cloud.google.com/functions/list?env=gen2>`_
page and use the project picker to select the project in which you
created the function. For easy identification, the names of the functions
created by BigQuery DataFrames are prefixed by ``bigframes-``.

**Requirements**

BigQuery DataFrames uses the ``gcloud`` command-line interface internally,
so you must run ``gcloud auth login`` before using remote functions.

To use BigQuery DataFrames remote functions, you must enable the following APIs:

* The BigQuery API (bigquery.googleapis.com)
* The BigQuery Connection API (bigqueryconnection.googleapis.com)
* The Cloud Functions API (cloudfunctions.googleapis.com)
* The Cloud Run API (run.googleapis.com)
* The Artifact Registry API (artifactregistry.googleapis.com)
* The Cloud Build API (cloudbuild.googleapis.com )
* The Cloud Resource Manager API (cloudresourcemanager.googleapis.com)

To use BigQuery DataFrames remote functions, you must be granted the
following IAM roles:

* BigQuery Data Editor (roles/bigquery.dataEditor)
* BigQuery Connection Admin (roles/bigquery.connectionAdmin)
* Cloud Functions Developer (roles/cloudfunctions.developer)
* Service Account User (roles/iam.serviceAccountUser)
* Storage Object Viewer (roles/storage.objectViewer)
* Project IAM Admin (roles/resourcemanager.projectIamAdmin)

**Limitations**

* Remote functions take about 90 seconds to become available when you first create them.
* Trivial changes in the notebook, such as inserting a new cell or renaming a variable,
  might cause the remote function to be re-created, even if these changes are unrelated
  to the remote function code.
* BigQuery DataFrames does not differentiate any personal data you include in the remote
  function code. The remote function code is serialized as an opaque box to deploy it as a
  Cloud Functions function.
* The Cloud Functions (2nd gen) functions, BigQuery connections, and BigQuery remote
  functions created by BigQuery DataFrames persist in Google Cloud. If you don’t want to
  keep these resources, you must delete them separately using an appropriate Cloud Functions
  or BigQuery interface.
* A project can have up to 1000 Cloud Functions (2nd gen) functions at a time. See Cloud
  Functions quotas for all the limits.


Quotas and limits
-----------------

`BigQuery quotas <https://cloud.google.com/bigquery/quotas>`_
including hardware, software, and network components.


Session termination
-------------------

Each BigQuery DataFrames DataFrame or Series object is tied to a BigQuery
DataFrames session, which is in turn based on a BigQuery session. BigQuery
sessions
`auto-terminate <https://cloud.google.com/bigquery/docs/sessions-terminating#auto-terminate_a_session>`_
; when this happens, you can’t use previously
created DataFrame or Series objects and must re-create them using a new
BigQuery DataFrames session. You can do this by running
``bigframes.pandas.reset_session()`` and then re-running the BigQuery
DataFrames expressions.


Data processing location
------------------------

BigQuery DataFrames is designed for scale, which it achieves by keeping data
and processing on the BigQuery service. However, you can bring data into the
memory of your client machine by calling ``.execute()`` on a DataFrame or Series
object. If you choose to do this, the memory limitation of your client machine
applies.


License
-------

BigQuery DataFrames is distributed with the `Apache-2.0 license
<https://github.com/googleapis/python-bigquery-dataframes/blob/main/LICENSE>`_.

It also contains code derived from the following third-party packages:

* `Ibis <https://ibis-project.org/>`_
* `pandas <https://pandas.pydata.org/>`_
* `Python <https://www.python.org/>`_
* `scikit-learn <https://scikit-learn.org/>`_
* `XGBoost <https://xgboost.readthedocs.io/en/stable/>`_

For details, see the `third_party
<https://github.com/googleapis/python-bigquery-dataframes/tree/main/third_party/bigframes_vendored>`_
directory.


Contact Us
----------

For further help and provide feedback, you can email us at `bigframes-feedback@google.com <https://mail.google.com/mail/?view=cm&fs=1&tf=1&to=bigframes-feedback@google.com>`_.
