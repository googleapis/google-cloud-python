# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def query_external_gcs_temporary_table(client):

    # [START bigquery_query_external_gcs_temp]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    # Configure the external data source and query job
    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = [
        "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    ]
    external_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    external_config.options.skip_leading_rows = 1  # optionally skip header row
    table_id = "us_states"
    job_config = bigquery.QueryJobConfig()
    job_config.table_definitions = {table_id: external_config}

    # Example query to find states starting with 'W'
    sql = 'SELECT * FROM `{}` WHERE name LIKE "W%"'.format(table_id)

    query_job = client.query(sql, job_config=job_config)  # API request

    w_states = list(query_job)  # Waits for query to finish
    print("There are {} states with names starting with W.".format(len(w_states)))
    assert len(w_states) == 4

    # [END bigquery_query_external_gcs_temp]