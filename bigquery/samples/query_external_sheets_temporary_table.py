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


def query_external_sheets_temporary_table(client):

    # [START bigquery_auth_drive_scope]
    # [START bigquery_query_external_sheets_temp]
    import google.auth

    # from google.cloud import bigquery

    # Create credentials with Drive & BigQuery API scopes
    # Both APIs must be enabled for your project before running this code
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery",
        ]
    )
    client = bigquery.Client(credentials=credentials, project=project)

    # Configure the external data source and query job
    external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")
    # Use a shareable link or grant viewing access to the email address you
    # used to authenticate with BigQuery (this example Sheet is public)
    sheet_url = (
        "https://docs.google.com/spreadsheets"
        "/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing"
    )
    external_config.source_uris = [sheet_url]
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
    # [END bigquery_query_external_sheets_temp]
    assert len(w_states) == 4

    # [END bigquery_auth_drive_scope]