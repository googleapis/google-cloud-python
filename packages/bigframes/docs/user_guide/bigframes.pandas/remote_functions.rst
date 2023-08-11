
Using the Remote Functions
==========================

BigQuery DataFrames gives you the ability to turn your custom scalar functions
into a BigQuery remote function. It requires the GCP project to be set up
appropriately and the user having sufficient privileges to use them. One can
find more details on it via `help` command.

.. code-block:: python

    import bigframes.pandas as bpd
    help(bpd.remote_function)

Read a table and inspect the column of interest.

.. code-block:: python

    df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    df["body_mass_g"].head(10)

Define a custom function, and specify the intent to turn it into a remote
function. It requires a BigQuery connection. If the connection is not already
created, BigQuery DataFrames will attempt to create one assuming the necessary
APIs and IAM permissions are setup in the project. In our examples we would be
using a pre-created connection named `bigframes-rf-conn`. Let's try a
`pandas`-like use case in which we want to apply a user defined scalar function
to every value in a `Series`, more specifically bucketize the `body_mass_g` value
of the penguins, which is a real number, into a category, which is a string.

.. code-block:: python

    @bpd.remote_function([float], str, bigquery_connection='bigframes-rf-conn')
    def get_bucket(num):
        if not num: return "NA"
        boundary = 4000
        return "at_or_above_4000" if num >= boundary else "below_4000"

Then we can apply the remote function on the `Series`` of interest via `apply`
API and store the result in a new column in the DataFrame.

.. code-block:: python

    df = df.assign(body_mass_bucket=df['body_mass_g'].apply(get_bucket))

This will add a new column `body_mass_bucket` in the DataFrame. You can preview
the original value and the bucketized value side by side.

.. code-block:: python

    df[['body_mass_g', 'body_mass_bucket']].head(10)

This operation was possible by doing all the computation on the cloud. For that,
there is a google cloud function deployed by serializing the user code.

.. warning::
    The deployed cloud function may be visible to other users with sufficient
    privilege in the project. The user should be careful about having any
    sensitive data in the code that will be deployed as a remote function.

The cloud function can be located from a property set in the remote function object.

.. code-block:: python

    get_bucket.bigframes_cloud_function

and then there is a BigQuery remote function created configured to call into the
cloud function via the BigQuery connection. That can also be located from
another property set in the remote function object.

.. code-block:: python

    get_bucket.bigframes_remote_function

The cloud assets created are persistant and the user can manage them directy
from the Google Cloud Console.

Let's continue trying other potential use cases of remote functions. Let's say
we consider the `species`, `island` and `sex` of the penguins sensitive
information and want to redact that by replacing with their hash code instead.
Let's define another scalar custom function and decorated it as a remote function:

.. code-block:: python

    @bpd.remote_function([str], str, bigquery_connection='bigframes-rf-conn')
    def get_hash(input):
        import hashlib
        # handle missing value
        if input is None:
        input = ""
        encoded_input = input.encode()
        hash = hashlib.md5(encoded_input)
        return hash.hexdigest()

We can use this remote function in another `pandas`-like API `map` that can be
applied on a DataFrame:

.. code-block:: python

    df_redacted = df[["species", "island", "sex"]].map(get_hash)
    df_redacted.head(10).

Using Existing Functions
========================

If you have already defined a custom function in BigQuery, either in the
BigQuery Studio or with the `remote_function` decorator above or otherwise, you
may use it with BigQuery DataFrames with the `read_gbq_function` method.

More details are available via the `help` command:

.. code-block:: python

    import bigframes.pandas as pd
    help(pd.read_gbq_function)

Here is an example of using `read_gbq_function` to load an existing function
named `get_bucket`:

.. code-block:: python

    import bigframes.pandas as pd

    df = pd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    get_bucket = pd.read_gbq_function("get_bucket")

    df = df.assign(body_mass_bucket=df['body_mass_g'].apply(get_bucket))
    df.head(10)

Note: As mentioned above, if a function is created using the `remote_function`
decorator, its generated name (including project and dataset) is accessible
immediately afterward in the function's `bigframes_remote_function` attribute.
The same string can be passed to `read_gbq_function` later in another context.
