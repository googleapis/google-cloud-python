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


def client_query_w_struct_params(client, capsys):

    # [START bigquery_query_params_structs]
    """Run a query using struct query parameters"""
    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = "SELECT @struct_value AS s;"
    query_params = [
        bigquery.StructQueryParameter(
            "struct_value",
            bigquery.ScalarQueryParameter("x", "INT64", 1),
            bigquery.ScalarQueryParameter("y", "STRING", "foo"),
        )
    ]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    # Print the results
    for row in query_job:
        print(row.s)

    assert query_job.state == "DONE"

    out, _ = capsys.readouterr()
    assert "1" in out
    assert "foo" in out

    # [END bigquery_query_params_structs]