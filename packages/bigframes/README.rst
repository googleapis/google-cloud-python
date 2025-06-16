BigQuery DataFrames (BigFrames)
===============================

|GA| |pypi| |versions|

BigQuery DataFrames (also known as BigFrames) provides a Pythonic DataFrame
and machine learning (ML) API powered by the BigQuery engine.

* `bigframes.pandas` provides a pandas API for analytics. Many workloads can be
  migrated from pandas to bigframes by just changing a few imports.
* ``bigframes.ml`` provides a scikit-learn-like API for ML.

BigQuery DataFrames is an open-source package.

**Version 2.0 introduces breaking changes for improved security and performance. See below for details.**

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

    bpd.options.bigquery.project = your_gcp_project_id
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
* `API reference <https://cloud.google.com/python/docs/reference/bigframes/latest/summary_overview>`_
* `Source code (GitHub) <https://github.com/googleapis/python-bigquery-dataframes>`_

⚠️ Warning: Breaking Changes in BigQuery DataFrames v2.0
--------------------------------------------------------

Version 2.0 introduces breaking changes for improved security and performance. Key default behaviors have changed, including

* **Large Results (>10GB):** The default value for ``allow_large_results`` has changed to ``False``.
  Methods like ``to_pandas()`` will now fail if the query result's compressed data size exceeds 10GB,
  unless large results are explicitly permitted.
* **Remote Function Security:** The library no longer automatically lets the Compute Engine default service
  account become the identity of the Cloud Run functions. If that is desired, it has to be indicated by passing
  ``cloud_function_service_account="default"``. And network ingress now defaults to ``"internal-only"``.
* **@remote_function Argument Passing:** Arguments other than ``input_types``, ``output_type``, and ``dataset``
  to ``remote_function`` must now be passed using keyword syntax, as positional arguments are no longer supported.
* **@udf Argument Passing:** Arguments ``dataset`` and ``name`` to ``udf`` are now mandatory.
* **Endpoint Connections:** Automatic fallback to locational endpoints in certain regions is removed.
* **LLM Updates (Gemini Integration):** Integrations now default to the ``gemini-2.0-flash-001`` model.
  PaLM2 support has been removed; please migrate any existing PaLM2 usage to Gemini. **Note:** The current default
  model will be removed in Version 3.0.

**Important:** If you are not ready to adapt to these changes, please pin your dependency to a version less than 2.0
(e.g., ``bigframes==1.42.0``) to avoid disruption.

To learn about these changes and how to migrate to version 2.0, see the
`updated introduction guide <https://cloud.google.com/bigquery/docs/bigquery-dataframes-introduction>`_.

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/bigframes.svg
   :target: https://pypi.org/project/bigframes/
.. |versions| image:: https://img.shields.io/pypi/pyversions/bigframes.svg
   :target: https://pypi.org/project/bigframes/

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
