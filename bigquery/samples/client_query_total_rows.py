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


def client_query_total_rows(client, capsys):

    # [START bigquery_query_total_rows]
    """Run a query and just check for how many rows."""
    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = (
        "SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` "
        'WHERE state = "TX" '
        "LIMIT 100"
    )
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
    )  # API request - starts the query

    results = query_job.result()  # Wait for query to complete.
    print("Got {} rows.".format(results.total_rows))

    out, _ = capsys.readouterr()
    assert "Got 100 rows." in out

    # [END bigquery_query_total_rows]