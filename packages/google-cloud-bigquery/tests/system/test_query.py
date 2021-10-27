# Copyright 2021 Google LLC
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

from google.cloud import bigquery


def test_dry_run(bigquery_client: bigquery.Client, scalars_table: str):
    query_config = bigquery.QueryJobConfig()
    query_config.dry_run = True

    query_string = f"SELECT * FROM {scalars_table}"
    query_job = bigquery_client.query(query_string, job_config=query_config,)

    # Note: `query_job.result()` is not necessary on a dry run query. All
    # necessary information is returned in the initial response.
    assert query_job.dry_run is True
    assert query_job.total_bytes_processed > 0
    assert len(query_job.schema) > 0


def test_session(bigquery_client: bigquery.Client):
    initial_config = bigquery.QueryJobConfig()
    initial_config.create_session = True
    initial_query = """
    CREATE TEMPORARY TABLE numbers(id INT64)
    AS
    SELECT * FROM UNNEST([1, 2, 3, 4, 5]) AS id;
    """
    initial_job = bigquery_client.query(initial_query, job_config=initial_config)
    initial_job.result()
    session_id = initial_job.session_info.session_id
    assert session_id is not None

    second_config = bigquery.QueryJobConfig()
    second_config.connection_properties = [
        bigquery.ConnectionProperty("session_id", session_id),
    ]
    second_job = bigquery_client.query(
        "SELECT COUNT(*) FROM numbers;", job_config=second_config
    )
    rows = list(second_job.result())

    assert len(rows) == 1
    assert rows[0][0] == 5
