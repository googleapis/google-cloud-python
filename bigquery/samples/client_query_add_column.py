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


def client_query_add_column(client, dataset_id):

    # [START bigquery_add_column_query_append]
    from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset where the table is.
    # dataset_id = "your-project.your_dataset"

    dataset = client.get_dataset(dataset_id)

    schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]

    table_id = dataset.table("sample_table")

    table = client.create_table(bigquery.Table(table_id, schema=schema))

    # Retrieves the destination table and checks the length of the schema
    table = client.get_table(table_id)
    if len(table.schema) == 2:
        print("Table {} contains {} columns.".format(table_id, len(table.schema)))

    # Configures the query to append the results to a destination table,
    # allowing field addition
    job_config = bigquery.QueryJobConfig()
    job_config.schema_update_options = [
        bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
    ]
    job_config.destination = table_id
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    query_job = client.query(
        # In this example, the existing table contains only the 'full_name' and
        # 'age' columns, while the results of this query will contain an
        # additional 'favorite_color' column.
        'SELECT "Timmy" as full_name, 85 as age, "Blue" as favorite_color;',
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    query_job.result()

    # Checks the updated length of the schema
    table = client.get_table(table)
    if len(table.schema) == 3 and table.num_rows > 0:
        print("Table {} now contains {} columns.".format(table_id, len(table.schema)))

    # [END bigquery_add_column_query_append]
