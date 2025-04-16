BigQuery DataFrames
===================

|GA| |pypi| |versions|

BigQuery DataFrames provides a Pythonic DataFrame and machine learning (ML) API
powered by the BigQuery engine.

* ``bigframes.pandas`` provides a pandas-compatible API for analytics.
* ``bigframes.ml`` provides a scikit-learn-like API for ML.

BigQuery DataFrames is an open-source package. You can run
``pip install --upgrade bigframes`` to install the latest version.

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

Documentation
-------------

* `BigQuery DataFrames source code (GitHub) <https://github.com/googleapis/python-bigquery-dataframes>`_
* `BigQuery DataFrames sample notebooks <https://github.com/googleapis/python-bigquery-dataframes/tree/main/notebooks>`_
* `BigQuery DataFrames API reference <https://cloud.google.com/python/docs/reference/bigframes/latest/summary_overview>`_
* `BigQuery DataFrames supported pandas APIs <https://cloud.google.com/python/docs/reference/bigframes/latest/supported_pandas_apis>`_


Getting started with BigQuery DataFrames
----------------------------------------
Read `Introduction to BigQuery DataFrames <https://cloud.google.com/bigquery/docs/bigquery-dataframes-introduction>`_
and try the `BigQuery DataFrames quickstart <https://cloud.google.com/bigquery/docs/dataframes-quickstart>`_
to get up and running in just a few minutes.


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
