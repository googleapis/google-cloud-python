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


def load_table_relax_column(client, to_delete):

    # [START bigquery_relax_column_load_append]
    dataset_id = "load_table_relax_column_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    snippets_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(
        snippets_dir, "..", "..", "bigquery", "tests", "data", "people.csv"
    )
    table_ref = dataset_ref.table("my_table")
    old_schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("favorite_color", "STRING", mode="REQUIRED"),
    ]
    table = client.create_table(bigquery.Table(table_ref, schema=old_schema))

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # filepath = 'path/to/your_file.csv'

    # Retrieves the destination table and checks the number of required fields
    table_id = "my_table"
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    original_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
    # In this example, the existing table has 3 required fields.
    print("{} fields in the schema are required.".format(original_required_fields))

    # Configures the load job to append the data to a destination table,
    # allowing field relaxation
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.schema_update_options = [
        bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
    ]
    # In this example, the existing table contains three required fields
    # ('full_name', 'age', and 'favorite_color'), while the data to load
    # contains only the first two fields.
    job_config.schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1

    with open(filepath, "rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location="US",  # Must match the destination dataset location.
            job_config=job_config,
        )  # API request

    job.result()  # Waits for table load to complete.
    print(
        "Loaded {} rows into {}:{}.".format(
            job.output_rows, dataset_id, table_ref.table_id
        )
    )

    # Checks the updated number of required fields
    table = client.get_table(table)
    current_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
    print("{} fields in the schema are now required.".format(current_required_fields))
    assert original_required_fields - current_required_fields == 1
    assert len(table.schema) == 3
    assert table.schema[2].mode == "NULLABLE"
    assert table.num_rows > 0

    # [END bigquery_relax_column_load_append]