.. BigQuery DataFrames documentation main file

Welcome to BigQuery DataFrames
==============================

**BigQuery DataFrames** (``bigframes``) provides a Pythonic interface for data analysis that scales to petabytes. It gives you the best of both worlds: the familiar API of **pandas** and **scikit-learn**, powered by the distributed computing engine of **BigQuery**.

BigQuery DataFrames consists of three main components:

* **bigframes.pandas**: A pandas-compatible API for data exploration and transformation.
* **bigframes.ml**: A scikit-learn-like interface for BigQuery ML, including integration with Gemini.
* **bigframes.bigquery**: Specialized functions for managing BigQuery resources and deploying custom logic.

Why BigQuery DataFrames?
------------------------

BigFrames allows you to process data where it lives. Instead of downloading massive datasets to your local machine, BigFrames translates your Python code into SQL and executes it across the BigQuery fleet.

* **Scalability:** Work with datasets that exceed local memory limits without complex refactoring.
* **Collaboration & Extensibility:** Bridge the gap between Python and SQL. Deploy custom Python functions to BigQuery, making your logic accessible to SQL-based teammates and data analysts.
* **Production-Ready Pipelines:** Move seamlessly from interactive notebooks to production. BigFrames simplifies data engineering by integrating with tools like **dbt** and **Airflow**, offering a simpler operational model than Spark.
* **Security & Governance:** Keep your data within the BigQuery perimeter. Benefit from enterprise-grade security, auditing, and data governance throughout your entire Python workflow.
* **Familiarity:** Use ``read_gbq``, ``merge``, ``groupby``, and ``pivot_table`` just like you do in pandas.

Quickstart
----------

Install the library via pip:

.. code-block:: bash

    pip install --upgrade bigframes

Load and aggregate a public dataset in just a few lines:

.. code-block:: python

    import bigframes.pandas as bpd

    # Load data from BigQuery
    df = bpd.read_gbq("bigquery-public-data.usa_names.usa_1910_2013")

    # Perform familiar pandas operations at scale
    top_names = (
        df.groupby("name")
        .agg({"number": "sum"})
        .sort_values("number", ascending=False)
        .head(10)
    )

    print(top_names.to_pandas())


User Guide
----------

.. toctree::
    :maxdepth: 2

    user_guide/index

API reference
-------------

.. toctree::
    :maxdepth: 3

    reference/index
    supported_pandas_apis

Changelog
---------

For a list of all BigQuery DataFrames releases:

.. toctree::
    :maxdepth: 2

    changelog
