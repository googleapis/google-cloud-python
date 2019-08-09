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


def client_query_relax_column(client, to_delete):

    # [START bigquery_relax_column_query_append]
    dataset_id = "query_relax_column_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table_ref = dataset_ref.table("my_table")
    schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]
    table = client.create_table(bigquery.Table(table_ref, schema=schema))

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    # Retrieves the destination table and checks the number of required fields
    table_id = "my_table"
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    original_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
    # In this example, the existing table has 2 required fields
    print("{} fields in the schema are required.".format(original_required_fields))

    # Configures the query to append the results to a destination table,
    # allowing field relaxation
    job_config = bigquery.QueryJobConfig()
    job_config.schema_update_options = [
        bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
    ]
    job_config.destination = table_ref
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    query_job = client.query(
        # In this example, the existing table contains 'full_name' and 'age' as
        # required columns, but the query results will omit the second column.
        'SELECT "Beyonce" as full_name;',
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    query_job.result()  # Waits for the query to finish
    print("Query job {} complete.".format(query_job.job_id))

    # Checks the updated number of required fields
    table = client.get_table(table)
    current_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
    print("{} fields in the schema are now required.".format(current_required_fields))
    assert original_required_fields - current_required_fields > 0
    assert len(table.schema) == 2
    assert table.schema[1].mode == "NULLABLE"
    assert table.num_rows > 0

    # [END bigquery_relax_column_query_append]