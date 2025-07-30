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


def test_sessions_and_io(project_id: str, dataset_id: str) -> None:
    YOUR_PROJECT_ID = project_id
    YOUR_DATASET_ID = dataset_id
    YOUR_LOCATION = "us"

    # [START bigquery_dataframes_create_and_use_session_instance]
    import bigframes
    import bigframes.pandas as bpd

    # Create session object
    context = bigframes.BigQueryOptions(
        project=YOUR_PROJECT_ID,
        location=YOUR_LOCATION,
    )
    session = bigframes.Session(context)

    # Load a BigQuery table into a dataframe
    df1 = session.read_gbq("bigquery-public-data.ml_datasets.penguins")

    # Create a dataframe with local data:
    df2 = bpd.DataFrame({"my_col": [1, 2, 3]}, session=session)
    # [END bigquery_dataframes_create_and_use_session_instance]
    assert df1 is not None
    assert df2 is not None

    # [START bigquery_dataframes_combine_data_from_multiple_sessions_raise_error]
    import bigframes
    import bigframes.pandas as bpd

    context = bigframes.BigQueryOptions(location=YOUR_LOCATION, project=YOUR_PROJECT_ID)

    session1 = bigframes.Session(context)
    session2 = bigframes.Session(context)

    series1 = bpd.Series([1, 2, 3, 4, 5], session=session1)
    series2 = bpd.Series([1, 2, 3, 4, 5], session=session2)

    try:
        series1 + series2
    except ValueError as e:
        print(e)  # Error message: Cannot use combine sources from multiple sessions
    # [END bigquery_dataframes_combine_data_from_multiple_sessions_raise_error]

    # [START bigquery_dataframes_set_options_for_global_session]
    import bigframes.pandas as bpd

    # Set project ID for the global session
    bpd.options.bigquery.project = YOUR_PROJECT_ID
    # Update the global default session location
    bpd.options.bigquery.location = YOUR_LOCATION
    # [END bigquery_dataframes_set_options_for_global_session]

    # [START bigquery_dataframes_global_session_is_the_default_session]
    # The following two statements are essentially the same
    df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    df = bpd.get_global_session().read_gbq("bigquery-public-data.ml_datasets.penguins")
    # [END bigquery_dataframes_global_session_is_the_default_session]
    assert df is not None

    # [START bigquery_dataframes_create_dataframe_from_py_and_np]
    import numpy as np

    import bigframes.pandas as bpd

    s = bpd.Series([1, 2, 3])

    # Create a dataframe with Python dict
    df = bpd.DataFrame(
        {
            "col_1": [1, 2, 3],
            "col_2": [4, 5, 6],
        }
    )

    # Create a series with Numpy
    s = bpd.Series(np.arange(10))
    # [END bigquery_dataframes_create_dataframe_from_py_and_np]
    assert s is not None

    # [START bigquery_dataframes_create_dataframe_from_pandas]
    import numpy as np
    import pandas as pd

    import bigframes.pandas as bpd

    pd_df = pd.DataFrame(np.random.randn(4, 2))

    # Convert Pandas dataframe to BigQuery DataFrame with read_pandas()
    df_1 = bpd.read_pandas(pd_df)
    # Convert Pandas dataframe to BigQuery DataFrame with the dataframe constructor
    df_2 = bpd.DataFrame(pd_df)
    # [END bigquery_dataframes_create_dataframe_from_pandas]
    assert df_1 is not None
    assert df_2 is not None

    # [START bigquery_dataframes_convert_bq_dataframe_to_pandas]
    import bigframes.pandas as bpd

    bf_df = bpd.DataFrame({"my_col": [1, 2, 3]})
    # Returns a Pandas Dataframe
    bf_df.to_pandas()

    bf_s = bpd.Series([1, 2, 3])
    # Returns a Pandas Series
    bf_s.to_pandas()
    # [END bigquery_dataframes_convert_bq_dataframe_to_pandas]
    assert bf_s.to_pandas() is not None

    # [START bigquery_dataframes_to_pandas_dry_run]
    import bigframes.pandas as bpd

    df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

    # Returns a Pandas series with dry run stats
    df.to_pandas(dry_run=True)
    # [END bigquery_dataframes_to_pandas_dry_run]
    assert df.to_pandas(dry_run=True) is not None

    # [START bigquery_dataframes_read_data_from_csv]
    import bigframes.pandas as bpd

    # Read a CSV file from GCS
    df = bpd.read_csv("gs://cloud-samples-data/bigquery/us-states/us-states.csv")
    # [END bigquery_dataframes_read_data_from_csv]
    assert df is not None

    # [START bigquery_dataframes_read_data_from_bigquery_table]
    import bigframes.pandas as bpd

    df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    # [END bigquery_dataframes_read_data_from_bigquery_table]
    assert df is not None

    # [START bigquery_dataframes_read_from_sql_query]
    import bigframes.pandas as bpd

    sql = """
    SELECT species, island, body_mass_g
    FROM bigquery-public-data.ml_datasets.penguins
    WHERE sex = 'MALE'
    """

    df = bpd.read_gbq(sql)
    # [END bigquery_dataframes_read_from_sql_query]
    assert df is not None

    YOUR_TABLE_NAME = "snippets-session-and-io-test"

    # [START bigquery_dataframes_dataframe_to_bigquery_table]
    import bigframes.pandas as bpd

    df = bpd.DataFrame({"my_col": [1, 2, 3]})

    df.to_gbq(f"{YOUR_PROJECT_ID}.{YOUR_DATASET_ID}.{YOUR_TABLE_NAME}")
    # [END bigquery_dataframes_dataframe_to_bigquery_table]
