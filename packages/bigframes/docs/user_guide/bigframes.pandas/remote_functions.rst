
Using the Remote Functions
==========================

BigQuery DataFrames gives you the ability to turn your custom scalar functions
into a BigQuery remote function. It requires the GCP project to be set up
appropriately and the user having sufficient privileges to use them. One can
find more details on it via `help` command.

.. code-block:: python

    import bigframes.pandas as pd
    help(pd.remote_function)

Read a table and inspect the column of interest.

.. code-block:: python

    df = pd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    df["body_mass_g"].head(10)

Define a custom function, and specify the intent to turn it into a remote
function. It requires a BigQuery connection. If the connection is not already
created, BigQuery DataFrames will attempt to create one assuming the necessary
APIs and IAM permissions are setup in the project.

.. code-block:: python

    @pd.remote_function([float], str, bigquery_connection='bigframes-rf-conn')
    def get_bucket(num):
        if not num: return "NA"
        boundary = 4000
        return "at_or_above_4000" if num >= boundary else "below_4000"

Run the custom function on the column of interest to create a new column.

.. code-block:: python

    df = df.assign(body_mass_bucket=df['body_mass_g'].apply(get_bucket))
    df[['body_mass_g', 'body_mass_bucket']].head(10)
