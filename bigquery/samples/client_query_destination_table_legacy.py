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


def client_query_destination_table_legacy(client, to_delete):

    # [START bigquery_query_legacy_large_results]
    dataset_id = "query_destination_table_legacy_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    to_delete.append(dataset_ref)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    client.create_dataset(dataset)

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'your_dataset_id'

    job_config = bigquery.QueryJobConfig()
    # Set use_legacy_sql to True to use legacy SQL syntax.
    job_config.use_legacy_sql = True
    # Set the destination table
    table_ref = client.dataset(dataset_id).table("your_table_id")
    job_config.destination = table_ref
    job_config.allow_large_results = True
    sql = """
        SELECT corpus
        FROM [bigquery-public-data:samples.shakespeare]
        GROUP BY corpus;
    """
    # Start the query, passing in the extra configuration.
    query_job = client.query(
        sql,
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    query_job.result()  # Waits for the query to finish
    print("Query results loaded to table {}".format(table_ref.path))

    # [END bigquery_query_legacy_large_results]