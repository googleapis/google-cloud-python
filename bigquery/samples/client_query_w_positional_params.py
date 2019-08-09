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


def client_query_w_positional_params(client, capsys):

    # [START bigquery_query_params_positional]
    """Run a query using query parameters"""

    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = """
        SELECT word, word_count
        FROM `bigquery-public-data.samples.shakespeare`
        WHERE corpus = ?
        AND word_count >= ?
        ORDER BY word_count DESC;
    """
    # Set the name to None to use positional parameters.
    # Note that you cannot mix named and positional parameters.
    query_params = [
        bigquery.ScalarQueryParameter(None, "STRING", "romeoandjuliet"),
        bigquery.ScalarQueryParameter(None, "INT64", 250),
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
        print("{}: \t{}".format(row.word, row.word_count))

    assert query_job.state == "DONE"

    out, _ = capsys.readouterr()
    assert "the" in out

    # [END bigquery_query_params_positional]