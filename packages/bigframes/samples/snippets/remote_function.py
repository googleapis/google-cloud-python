# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run_remote_function_and_read_gbq_function(project_id: str) -> None:
    your_gcp_project_id = project_id

    # [START bigquery_dataframes_remote_function]
    import bigframes.pandas as bpd

    # Set BigQuery DataFrames options
    bpd.options.bigquery.project = your_gcp_project_id
    bpd.options.bigquery.location = "us"

    # BigQuery DataFrames gives you the ability to turn your custom scalar
    # functions into a BigQuery remote function. It requires the GCP project to
    # be set up appropriately and the user having sufficient privileges to use
    # them. One can find more details about the usage and the requirements via
    # `help` command.
    help(bpd.remote_function)

    # Read a table and inspect the column of interest.
    df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    df["body_mass_g"].head(10)

    # Define a custom function, and specify the intent to turn it into a remote
    # function. It requires a BigQuery connection. If the connection is not
    # already created, BigQuery DataFrames will attempt to create one assuming
    # the necessary APIs and IAM permissions are setup in the project. In our
    # examples we will be letting the default connection `bigframes-default-connection`
    # be used. We will also set `reuse=False` to make sure we don't
    # step over someone else creating remote function in the same project from
    # the exact same source code at the same time. Let's try a `pandas`-like use
    # case in which we want to apply a user defined scalar function to every
    # value in a `Series`, more specifically bucketize the `body_mass_g` value
    # of the penguins, which is a real number, into a category, which is a
    # string.
    @bpd.remote_function(
        reuse=False,
        cloud_function_service_account="default",
    )
    def get_bucket(num: float) -> str:
        if not num:
            return "NA"
        boundary = 4000
        return "at_or_above_4000" if num >= boundary else "below_4000"

    # Then we can apply the remote function on the `Series`` of interest via
    # `apply` API and store the result in a new column in the DataFrame.
    df = df.assign(body_mass_bucket=df["body_mass_g"].apply(get_bucket))

    # This will add a new column `body_mass_bucket` in the DataFrame. You can
    # preview the original value and the bucketized value side by side.
    df[["body_mass_g", "body_mass_bucket"]].head(10)

    # The above operation was possible by doing all the computation on the
    # cloud. For that, there is a google cloud function deployed by serializing
    # the user code, and a BigQuery remote function created to call the cloud
    # function via the latter's http endpoint on the data in the DataFrame.

    # The BigQuery remote function created to support the BigQuery DataFrames
    # remote function can be located via a property `bigframes_remote_function`
    # set in the remote function object.
    print(f"Created BQ remote function: {get_bucket.bigframes_remote_function}")

    # The cloud function can be located via another property
    # `bigframes_cloud_function` set in the remote function object.
    print(f"Created cloud function: {get_bucket.bigframes_cloud_function}")

    # Warning: The deployed cloud function may be visible to other users with
    # sufficient privilege in the project, so the user should be careful about
    # having any sensitive data in the code that will be deployed as a remote
    # function.

    # Let's continue trying other potential use cases of remote functions. Let's
    # say we consider the `species`, `island` and `sex` of the penguins
    # sensitive information and want to redact that by replacing with their hash
    # code instead. Let's define another scalar custom function and decorate it
    # as a remote function. The custom function in this example has external
    # package dependency, which can be specified via `packages` parameter.
    @bpd.remote_function(
        reuse=False,
        packages=["cryptography"],
        cloud_function_service_account="default",
    )
    def get_hash(input: str) -> str:
        from cryptography.fernet import Fernet

        # handle missing value
        if input is None:
            input = ""

        key = Fernet.generate_key()
        f = Fernet(key)
        return f.encrypt(input.encode()).decode()

    # We can use this remote function in another `pandas`-like API `map` that
    # can be applied on a DataFrame
    df_redacted = df[["species", "island", "sex"]].map(get_hash)
    df_redacted.head(10)

    # [END bigquery_dataframes_remote_function]

    existing_get_bucket_bq_udf = get_bucket.bigframes_remote_function

    # [START bigquery_dataframes_read_gbq_function]

    # If you have already defined a custom function in BigQuery, either via the
    # BigQuery Google Cloud Console or with the `remote_function` decorator,
    # or otherwise, you may use it with BigQuery DataFrames with the
    # `read_gbq_function` method. More details are available via the `help`
    # command.
    import bigframes.pandas as pd

    help(pd.read_gbq_function)

    # Here is an example of using `read_gbq_function` to load an existing
    # BigQuery function.
    df = pd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    get_bucket_function = pd.read_gbq_function(existing_get_bucket_bq_udf)

    df = df.assign(body_mass_bucket=df["body_mass_g"].apply(get_bucket_function))
    df.head(10)

    # It should be noted that if a function is created using the
    # `remote_function` decorator, its created BQ remote function is accessible
    # immediately afterward via the function's `bigframes_remote_function`
    # attribute. The same string can be passed to `read_gbq_function` later in
    # another context.

    # [END bigquery_dataframes_read_gbq_function]

    # Clean up cloud artifacts
    session = bpd.get_global_session()
    for function in (get_bucket, get_hash):
        try:
            session.bqclient.delete_routine(function.bigframes_remote_function)
        except Exception:
            # Ignore exception during clean-up
            pass

        try:
            session.cloudfunctionsclient.delete_function(
                name=function.bigframes_cloud_function
            )
        except Exception:
            # Ignore exception during clean-up
            pass
