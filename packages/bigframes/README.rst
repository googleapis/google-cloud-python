BigQuery DataFrames
===================

BigQuery DataFrames provides a Pythonic DataFrame and machine learning (ML) API
powered by the BigQuery engine.

* ``bigframes.pandas`` provides a pandas-compatible API for analytics.
* ``bigframes.ml`` provides a scikit-learn-like API for ML.

BigQuery DataFrames is an open-source package. You can run
``pip install --upgrade bigframes`` to install the latest version.

Documentation
-------------

* `BigQuery DataFrames source code (GitHub) <https://github.com/googleapis/python-bigquery-dataframes>`_
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

  bpd.options.bigquery.project = your_gcp_project_id
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
BigQuery DataFrames
auto-populates ``bf.options.bigquery.location`` if the user starts with
``read_gbq/read_gbq_table/read_gbq_query()`` and specifies a table, either
directly or in a SQL statement.

If you want to reset the location of the created DataFrame or Series objects,
you can close the session by executing ``bigframes.pandas.close_session()``.
After that, you can reuse ``bigframes.pandas.options.bigquery.location`` to
specify another location.


``read_gbq()`` requires you to specify a location if the dataset you are
querying is not in the US multi-region. If you try to read a table from another
location, you get a NotFound exception.

Project
-------
If ``bf.options.bigquery.project`` is not set, the ``$GOOGLE_CLOUD_PROJECT``
environment variable is used, which is set in the notebook runtime serving the
BigQuery Studio/Vertex Notebooks.

ML Capabilities
---------------

The ML capabilities in BigQuery DataFrames let you preprocess data, and
then train models on that data. You can also chain these actions together to
create data pipelines.

Preprocess data
^^^^^^^^^^^^^^^^^^^^^^^^

Create transformers to prepare data for use in estimators (models) by
using the
`bigframes.ml.preprocessing module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.preprocessing>`_
and the `bigframes.ml.compose module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.compose>`_.
BigQuery DataFrames offers the following transformations:

* Use the `KBinsDiscretizer class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.compose.ColumnTransformer>`_
  in the ``bigframes.ml.preprocessing`` module to bin continuous data into intervals.
* Use the `LabelEncoder class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.preprocessing.LabelEncoder>`_
  in the ``bigframes.ml.preprocessing`` module to normalize the target labels as integer values.
* Use the `MaxAbsScaler class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.preprocessing.MaxAbsScaler>`_
  in the ``bigframes.ml.preprocessing`` module to scale each feature to the range ``[-1, 1]`` by its maximum absolute value.
* Use the `MinMaxScaler class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.preprocessing.MinMaxScaler>`_
  in the ``bigframes.ml.preprocessing`` module to standardize features by scaling each feature to the range ``[0, 1]``.
* Use the `StandardScaler class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.preprocessing.StandardScaler>`_
  in the ``bigframes.ml.preprocessing`` module to standardize features by removing the mean and scaling to unit variance.
* Use the `OneHotEncoder class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.preprocessing.OneHotEncoder>`_
  in the ``bigframes.ml.preprocessing`` module to transform categorical values into numeric format.
* Use the `ColumnTransformer class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.compose.ColumnTransformer>`_
  in the ``bigframes.ml.compose`` module to apply transformers to DataFrames columns.


Train models
^^^^^^^^^^^^

Create estimators to train models in BigQuery DataFrames.

**Clustering models**

Create estimators for clustering models by using the
`bigframes.ml.cluster module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.cluster>`_.

* Use the `KMeans class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.cluster.KMeans>`_
  to create K-means clustering models. Use these models for
  data segmentation. For example, identifying customer segments. K-means is an
  unsupervised learning technique, so model training doesn't require labels or split
  data for training or evaluation.

**Decomposition models**

Create estimators for decomposition models by using the `bigframes.ml.decomposition module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.decomposition>`_.

* Use the `PCA class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.decomposition.PCA>`_
  to create principal component analysis (PCA) models. Use these
  models for computing  principal components and using them to perform a change of
  basis on the data. This provides dimensionality reduction by projecting each data
  point onto only the first few principal components to obtain lower-dimensional
  data while preserving as much of the data's variation as possible.


**Ensemble models**

Create estimators for ensemble models by using the `bigframes.ml.ensemble module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.ensemble>`_.

* Use the `RandomForestClassifier class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.ensemble.RandomForestClassifier>`_
  to create random forest classifier models. Use these models for constructing multiple
  learning method decision trees for classification.
* Use the `RandomForestRegressor class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.ensemble.RandomForestRegressor>`_
  to create random forest regression models. Use
  these models for constructing multiple learning method decision trees for regression.
* Use the `XGBClassifier class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.ensemble.XGBClassifier>`_
  to create gradient boosted tree classifier models. Use these models for additively
  constructing multiple learning method decision trees for classification.
* Use the `XGBRegressor class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.ensemble.XGBRegressor>`_
  to create gradient boosted tree regression models. Use these models for additively
  constructing multiple learning method decision trees for regression.


**Forecasting models**

Create estimators for forecasting models by using the `bigframes.ml.forecasting module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.forecasting>`_.

* Use the `ARIMAPlus class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.forecasting.ARIMAPlus>`_
  to create time series forecasting models.

**Imported models**

Create estimators for imported models by using the `bigframes.ml.imported module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.imported>`_.

* Use the `ONNXModel class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.imported.ONNXModel>`_
  to import Open Neural Network Exchange (ONNX) models.
* Use the `TensorFlowModel class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.imported.TensorFlowModel>`_
  to import TensorFlow models.

**Linear models**

Create estimators for linear models by using the `bigframes.ml.linear_model module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.linear_model>`_.

* Use the `LinearRegression class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.linear_model.LinearRegression>`_
  to create linear regression models. Use these models for forecasting. For example,
  forecasting the sales of an item on a given day.
* Use the `LogisticRegression class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.linear_model.LogisticRegression>`_
  to create logistic regression models. Use these models for the classification of two
  or more possible values such as whether an input is ``low-value``, ``medium-value``,
  or ``high-value``.

**Large language models**

Create estimators for LLMs by using the `bigframes.ml.llm module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm>`_.

* Use the `PaLM2TextGenerator class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.PaLM2TextGenerator>`_ to create PaLM2 text generator models. Use these models
  for text generation tasks.
* Use the `PaLM2TextEmbeddingGenerator class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.PaLM2TextEmbeddingGenerator>`_ to create PaLM2 text embedding generator models.
  Use these models for text embedding generation tasks.


Create pipelines
^^^^^^^^^^^^^^^^

Create ML pipelines by using
`bigframes.ml.pipeline module <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.pipeline>`_.
Pipelines let you assemble several ML steps to be cross-validated together while setting
different parameters. This simplifies your code, and allows you to deploy data preprocessing
steps and an estimator together.

* Use the `Pipeline class <https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.pipeline.Pipeline>`_
  to create a pipeline of transforms with a final estimator.


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
function in BigQuery DataFrames (See `code samples
<https://cloud.google.com/bigquery/docs/remote-functions#bigquery-dataframes>`_)
creates a BigQuery remote function, a `BigQuery
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
in a special type of `hidden dataset <https://cloud.google.com/bigquery/docs/datasets#hidden_datasets>`__
referred to as an anonymous dataset. To view and manage remote functions created
in a user provided dataset, do the following:

1. Go to `BigQuery in the Google Cloud Console <https://console.cloud.google.com/bigquery>`__.
2. Select the project in which you created the remote function.
3. In the Explorer pane, expand that project, expand the dataset in which you
   created the remote function, and then expand Routines.

To view and manage Cloud Functions functions, use the
`Functions <https://console.cloud.google.com/functions/list?env=gen2>`_
page and use the project picker to select the project in which you
created the function. For easy identification, the names of the functions
created by BigQuery DataFrames are prefixed by ``bigframes``.

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
* Service Account User (roles/iam.serviceAccountUser) on the
  `service account <https://cloud.google.com/functions/docs/reference/iam/roles#additional-configuration> `
  ``PROJECT_NUMBER-compute@developer.gserviceaccount.com``
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
------------------

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
``bigframes.pandas.close_session()`` and then re-running the BigQuery
DataFrames expressions.


Data processing location
------------------------

BigQuery DataFrames is designed for scale, which it achieves by keeping data
and processing on the BigQuery service. However, you can bring data into the
memory of your client machine by calling ``.to_pandas()`` on a DataFrame or Series
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
