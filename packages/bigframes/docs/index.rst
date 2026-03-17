.. BigQuery DataFrames documentation main file

Scalable Python Data Analysis with BigQuery DataFrames (BigFrames)
==================================================================

.. meta::
   :description: BigQuery DataFrames (BigFrames) provides a scalable, pandas-compatible Python API for data analysis and machine learning on petabyte-scale datasets using the BigQuery engine.

**BigQuery DataFrames** (``bigframes``) is an open-source Python library that brings the power of **distributed computing** to your data science workflow. By providing a familiar **pandas** and **scikit-learn** compatible API, BigFrames allows you to analyze and model massive datasets where they live—directly in **BigQuery**.

Why Choose BigQuery DataFrames?
-------------------------------

BigFrames eliminates the "data movement bottleneck." Instead of downloading large datasets to a local environment, BigFrames translates your Python code into optimized SQL, executing complex transformations across the BigQuery fleet.

*   **Petabyte-Scale Scalability:** Effortlessly process datasets that far exceed local memory limits.
*   **Familiar Python Ecosystem:** Use the same ``read_gbq``, ``groupby``, ``merge``, and ``pivot_table`` functions you already know from pandas.
*   **Integrated Machine Learning:** Access BigQuery ML's powerful algorithms via a scikit-learn-like interface (``bigframes.ml``), including seamless **Gemini AI** integration.
*   **Enterprise-Grade Security:** Maintain data governance and security by keeping your data within the BigQuery perimeter.
*   **Hybrid Flexibility:** Easily move between distributed BigQuery processing and local pandas analysis with ``to_pandas()``.

Core Components of BigFrames
----------------------------

BigQuery DataFrames is organized into specialized modules designed for the modern data stack:

1.  :mod:`bigframes.pandas`: A high-performance, pandas-compatible API for scalable data exploration, cleaning, and transformation.
2.  :mod:`bigframes.bigquery`: Specialized utilities for direct BigQuery resource management, including integrations with Gemini and other AI models in the :mod:`bigframes.bigquery.ai` submodule.


Quickstart: Scalable Data Analysis in Seconds
---------------------------------------------

Install BigQuery DataFrames via pip:

.. code-block:: bash

    pip install --upgrade bigframes

The following example demonstrates how to perform a distributed aggregation on a public dataset with millions of rows using just a few lines of Python:

.. code-block:: python

    import bigframes.pandas as bpd

    # Initialize BigFrames and load a public dataset
    df = bpd.read_gbq("bigquery-public-data.usa_names.usa_1910_2013")

    # Perform familiar pandas operations that execute in the cloud
    top_names = (
        df.groupby("name")
        .agg({"number": "sum"})
        .sort_values("number", ascending=False)
        .head(10)
    )

    # Bring the final, aggregated results back to local memory if needed
    print(top_names.to_pandas())


Explore the Documentation
-------------------------

.. toctree::
    :maxdepth: 2
    :caption: User Documentation

    user_guide/index

.. toctree::
    :maxdepth: 2
    :caption: API Reference

    reference/index
    supported_pandas_apis

.. toctree::
    :maxdepth: 1
    :caption: Community & Updates

    changelog
