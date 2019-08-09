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


def client_query_dry_run(client):

    # [START bigquery_query_dry_run]
    """Run a dry run query"""

    # from google.cloud import bigquery
    # client = bigquery.Client()

    job_config = bigquery.QueryJobConfig()
    job_config.dry_run = True
    job_config.use_query_cache = False
    query_job = client.query(
        (
            "SELECT name, COUNT(*) as name_count "
            "FROM `bigquery-public-data.usa_names.usa_1910_2013` "
            "WHERE state = 'WA' "
            "GROUP BY name"
        ),
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request

    # A dry run query completes immediately.
    assert query_job.state == "DONE"
    assert query_job.dry_run

    print("This query will process {} bytes.".format(query_job.total_bytes_processed))

    assert query_job.total_bytes_processed > 0

    # [END bigquery_query_dry_run]