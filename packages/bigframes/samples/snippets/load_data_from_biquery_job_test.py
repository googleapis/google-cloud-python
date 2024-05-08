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


def test_bigquery_dataframes_load_data_from_bigquery_job() -> None:
    # Determine project id, in this case prefer the one set in the environment
    # variable GOOGLE_CLOUD_PROJECT (if any)
    import os

    your_project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "bigframes-dev")

    # Construct a BigQuery client object.
    from google.cloud import bigquery

    client = bigquery.Client(project=your_project_id, location="us")

    query = """
        SELECT *
        FROM `bigquery-public-data.ml_datasets.penguins`
        LIMIT 20
    """
    query_job = client.query(query)
    JOB_ID = query_job.job_id

    # [START bigquery_dataframes_load_data_from_bigquery_job]
    from google.cloud import bigquery

    import bigframes.pandas as bpd

    # Project ID inserted based on the query results selected to explore
    project = your_project_id
    # Location inserted based on the query results selected to explore
    location = "us"
    client = bigquery.Client(project=project, location=location)

    # Job ID inserted based on the query results selcted to explore
    job_id = JOB_ID
    job = client.get_job(job_id)
    destination = str(job.destination)

    # Load data from a BigQuery table using BigFrames DataFrames:
    bq_df = bpd.read_gbq_table(destination)

    # [END bigquery_dataframes_load_data_from_bigquery_job]
    assert bq_df is not None
