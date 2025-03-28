BigQuery DataFrames
===================

|GA| |pypi| |versions|

BigQuery DataFrames provides a Pythonic DataFrame and machine learning (ML) API
powered by the BigQuery engine.

* ``bigframes.pandas`` provides a pandas-compatible API for analytics.
* ``bigframes.ml`` provides a scikit-learn-like API for ML.

BigQuery DataFrames is an open-source package. You can run
``pip install --upgrade bigframes`` to install the latest version.

.. raw:: html

    <div style="border: 1px solid #f5c6cb;
    background-color: #f8d7da; color: #721c24; padding: 15px; margin-bottom: 20px; border-radius: 4px; font-size: 90%;">
        <p style="margin-top: 0; font-weight: bold;">⚠️ Breaking Changes in BigQuery DataFrames v2.0</p>
        <p>Version 2.0 introduces breaking changes for improved security and performance. Key default behaviors have changed:</p>
        <ul>
            <li><strong>Large Results (&gt;10GB):</strong> The default value for <code>allow_large_results</code> has changed to False. Methods like <code>to_pandas()</code> will now fail if the query result's compressed data size exceeds 10GB, unless large results are explicitly permitted.</li>
            <li><strong>Remote Function Security:</strong>The library no longer automatically lets the Compute Engine default service account become the identity of the Cloud Run functions. If that is desired, it has to be indicated by passing cloud_function_service_account="default". And network ingress now defaults to "internal-only".</li>
            <li><strong>@remote_function Argument Passing:</strong> Arguments other than input_types, output_type, and dataset to remote_function must now be passed using keyword syntax, as positional arguments are no longer supported.</li>
            <li><strong>Endpoint Connections:</strong> Automatic fallback to locational endpoints in certain regions is removed. </li>
            <li><strong>LLM Changes (Shift to Gemini):</strong> Integrations now default to <code>gemini-2.0-flash-001</code>. Support for PaLM2 models has been removed; migrate any PaLM2 usage to Gemini.</li>
        </ul>
        <p><strong>Important:</strong> If you are not ready to adapt to these changes, please pin your dependency to a version less than 2.0 (e.g., <code>bigframes==1.42.0</code>) to avoid disruption.</p>
        <p style="margin-bottom: 0;"> To learn about these changes and how to migrate to version 2.0, see:  <a href="https://cloud.google.com/bigquery/docs/bigquery-dataframes-introduction" style="color: #842029; text-decoration: underline;">updated introduction guide</a>.</p>
    </div>

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
