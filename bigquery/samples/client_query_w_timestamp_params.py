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


def client_query_w_timestamp_params(client, capsys):

    # [START bigquery_query_params_timestamps]
    """Run a query using query parameters"""

    # from google.cloud import bigquery
    # client = bigquery.Client()

    import datetime
    import pytz

    query = "SELECT TIMESTAMP_ADD(@ts_value, INTERVAL 1 HOUR);"
    query_params = [
        bigquery.ScalarQueryParameter(
            "ts_value",
            "TIMESTAMP",
            datetime.datetime(2016, 12, 7, 8, 0, tzinfo=pytz.UTC),
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
        print(row)

    assert query_job.state == "DONE"

    out, _ = capsys.readouterr()
    assert "2016, 12, 7, 9, 0" in out

    # [END bigquery_query_params_timestamps]