# Copyright 2025 Google LLC
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


def run_udf_and_read_gbq_function(
    project_id: str, dataset_id: str, routine_id: str
) -> None:
    your_gcp_project_id = project_id
    your_bq_dataset_id = dataset_id
    your_bq_routine_id = routine_id

    # [START bigquery_dataframes_udf]
    import bigframes.pandas as bpd

    # Set BigQuery DataFrames options
    bpd.options.bigquery.project = your_gcp_project_id
    bpd.options.bigquery.location = "US"

    # BigQuery DataFrames gives you the ability to turn your custom functions
    # into a BigQuery Python UDF. One can find more details about the usage and
    # the requirements via `help` command.
    help(bpd.udf)

    # Read a table and inspect the column of interest.
    df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    df["body_mass_g"].peek(10)

    # Define a custom function, and specify the intent to turn it into a
    # BigQuery Python UDF. Let's try a `pandas`-like use case in which we want
    # to apply a user defined function to every value in a `Series`, more
    # specifically bucketize the `body_mass_g` value of the penguins, which is a
    # real number, into a category, which is a string.
    @bpd.udf(
        dataset=your_bq_dataset_id,
        name=your_bq_routine_id,
    )
    def get_bucket(num: float) -> str:
        if not num:
            return "NA"
        boundary = 4000
        return "at_or_above_4000" if num >= boundary else "below_4000"

    # Then we can apply the udf on the `Series` of interest via
    # `apply` API and store the result in a new column in the DataFrame.
    df = df.assign(body_mass_bucket=df["body_mass_g"].apply(get_bucket))

    # This will add a new column `body_mass_bucket` in the DataFrame. You can
    # preview the original value and the bucketized value side by side.
    df[["body_mass_g", "body_mass_bucket"]].peek(10)

    # The above operation was possible by doing all the computation on the
    # cloud through an underlying BigQuery Python UDF that was created to
    # support the user's operations in the Python code.

    # The BigQuery Python UDF created to support the BigQuery DataFrames
    # udf can be located via a property `bigframes_bigquery_function`
    # set in the udf object.
    print(f"Created BQ Python UDF: {get_bucket.bigframes_bigquery_function}")

    # If you have already defined a custom function in BigQuery, either via the
    # BigQuery Google Cloud Console or with the `udf` decorator,
    # or otherwise, you may use it with BigQuery DataFrames with the
    # `read_gbq_function` method. More details are available via the `help`
    # command.
    help(bpd.read_gbq_function)

    existing_get_bucket_bq_udf = get_bucket.bigframes_bigquery_function

    # Here is an example of using `read_gbq_function` to load an existing
    # BigQuery Python UDF.
    df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    get_bucket_function = bpd.read_gbq_function(existing_get_bucket_bq_udf)

    df = df.assign(body_mass_bucket=df["body_mass_g"].apply(get_bucket_function))
    df.peek(10)

    # Let's continue trying other potential use cases of udf. Let's say we
    # consider the `species`, `island` and `sex` of the penguins sensitive
    # information and want to redact that by replacing with their hash code
    # instead. Let's define another scalar custom function and decorate it
    # as a udf. The custom function in this example has external package
    # dependency, which can be specified via `packages` parameter.
    @bpd.udf(
        dataset=your_bq_dataset_id,
        name=your_bq_routine_id,
        packages=["cryptography"],
    )
    def get_hash(input: str) -> str:
        from cryptography.fernet import Fernet

        # handle missing value
        if input is None:
            input = ""

        key = Fernet.generate_key()
        f = Fernet(key)
        return f.encrypt(input.encode()).decode()

    # We can use this udf in another `pandas`-like API `map` that
    # can be applied on a DataFrame
    df_redacted = df[["species", "island", "sex"]].map(get_hash)
    df_redacted.peek(10)

    # [END bigquery_dataframes_udf]

    # Clean up cloud artifacts
    session = bpd.get_global_session()
    session.bqclient.delete_routine(
        f"{your_bq_dataset_id}.{your_bq_routine_id}", not_found_ok=True
    )
