BigQuery DataFrames (BigFrames)
===============================


|GA| |pypi| |versions|

BigQuery DataFrames (also known as BigFrames) provides a Pythonic DataFrame
and machine learning (ML) API powered by the BigQuery engine. It provides modules
for many use cases, including:

* `bigframes.pandas <https://dataframes.bigquery.dev/reference/api/bigframes.pandas.html>`_
  is a pandas API for analytics. Many workloads can be
  migrated from pandas to bigframes by just changing a few imports.
* `bigframes.ml <https://dataframes.bigquery.dev/reference/index.html#ml-apis>`_
  is a scikit-learn-like API for ML.
* `bigframes.bigquery.ai <https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ai.html>`_
  are a collection of powerful AI methods, powered by Gemini.

BigQuery DataFrames is an `open-source package <https://github.com/googleapis/python-bigquery-dataframes>`_.

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/bigframes.svg
   :target: https://pypi.org/project/bigframes/
.. |versions| image:: https://img.shields.io/pypi/pyversions/bigframes.svg
   :target: https://pypi.org/project/bigframes/

Getting started with BigQuery DataFrames
----------------------------------------

The easiest way to get started is to try the
`BigFrames quickstart <https://cloud.google.com/bigquery/docs/dataframes-quickstart>`_
in a `notebook in BigQuery Studio <https://cloud.google.com/bigquery/docs/notebooks-introduction>`_.

To use BigFrames in your local development environment,

1. Run ``pip install --upgrade bigframes`` to install the latest version.

2. Setup `Application default credentials <https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment>`_
   for your local development environment enviroment.

3. Create a `GCP project with the BigQuery API enabled <https://cloud.google.com/bigquery/docs/sandbox>`_.

4. Use the ``bigframes`` package to query data.

.. code-block:: python

    import bigframes.pandas as bpd

    bpd.options.bigquery.project = your_gcp_project_id  # Optional in BQ Studio.
    bpd.options.bigquery.ordering_mode = "partial"  # Recommended for performance.
    df = bpd.read_gbq("bigquery-public-data.usa_names.usa_1910_2013")
    print(
        df.groupby("name")
        .agg({"number": "sum"})
        .sort_values("number", ascending=False)
        .head(10)
        .to_pandas()
    )

Documentation
-------------

To learn more about BigQuery DataFrames, visit these pages

* `Introduction to BigQuery DataFrames (BigFrames) <https://cloud.google.com/bigquery/docs/bigquery-dataframes-introduction>`_
* `Sample notebooks <https://github.com/googleapis/python-bigquery-dataframes/tree/main/notebooks>`_
* `API reference <https://dataframes.bigquery.dev/>`_
* `Source code (GitHub) <https://github.com/googleapis/python-bigquery-dataframes>`_

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
* `SQLGlot <https://sqlglot.com/sqlglot.html>`_

For details, see the `third_party
<https://github.com/googleapis/python-bigquery-dataframes/tree/main/third_party/bigframes_vendored>`_
directory.


Contact Us
----------

For further help and provide feedback, you can email us at `bigframes-feedback@google.com <https://mail.google.com/mail/?view=cm&fs=1&tf=1&to=bigframes-feedback@google.com>`_.
