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


def load_table_from_uri_truncate(client, to_delete, capsys):

    # [START bigquery_load_table_gcs_orc_truncate]
    """Replaces table data with data from a GCS URI using various formats

    Each file format has its own tested load from URI sample. Because most of
    the code is common for autodetect, append, and truncate, this sample
    includes snippets for all supported formats but only calls a single load
    job.

    This code snippet is made up of shared code, then format-specific code,
    followed by more shared code. Note that only the last format in the
    format-specific code section will be tested in this test.
    """
    dataset_id = "load_table_from_uri_trunc_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    table_ref = dataset.table("us_states")
    body = six.BytesIO(b"Washington,WA")
    client.load_table_from_file(body, table_ref, job_config=job_config).result()
    previous_rows = client.get_table(table_ref).num_rows
    assert previous_rows > 0

    # Shared code
    # [START bigquery_load_table_gcs_avro_truncate]
    # [START bigquery_load_table_gcs_csv_truncate]
    # [START bigquery_load_table_gcs_json_truncate]
    # [START bigquery_load_table_gcs_parquet_truncate]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('existing_table')

    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    # [END bigquery_load_table_gcs_avro_truncate]
    # [END bigquery_load_table_gcs_csv_truncate]
    # [END bigquery_load_table_gcs_json_truncate]
    # [END bigquery_load_table_gcs_parquet_truncate]

    # Format-specific code
    # [START bigquery_load_table_gcs_avro_truncate]
    job_config.source_format = bigquery.SourceFormat.AVRO
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.avro"
    # [END bigquery_load_table_gcs_avro_truncate]

    # [START bigquery_load_table_gcs_csv_truncate]
    job_config.skip_leading_rows = 1
    # The source format defaults to CSV, so the line below is optional.
    job_config.source_format = bigquery.SourceFormat.CSV
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    # [END bigquery_load_table_gcs_csv_truncate]
    # unset csv-specific attribute
    del job_config._properties["load"]["skipLeadingRows"]

    # [START bigquery_load_table_gcs_json_truncate]
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"
    # [END bigquery_load_table_gcs_json_truncate]

    # [START bigquery_load_table_gcs_parquet_truncate]
    job_config.source_format = bigquery.SourceFormat.PARQUET
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.parquet"
    # [END bigquery_load_table_gcs_parquet_truncate]

    # [START bigquery_load_table_gcs_orc_truncate]
    job_config.source_format = bigquery.SourceFormat.ORC
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.orc"
    # [END bigquery_load_table_gcs_orc_truncate]

    # Shared code
    # [START bigquery_load_table_gcs_avro_truncate]
    # [START bigquery_load_table_gcs_csv_truncate]
    # [START bigquery_load_table_gcs_json_truncate]
    # [START bigquery_load_table_gcs_parquet_truncate]
    # [START bigquery_load_table_gcs_orc_truncate]
    load_job = client.load_table_from_uri(
        uri, table_ref, job_config=job_config
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(table_ref)
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_avro_truncate]
    # [END bigquery_load_table_gcs_csv_truncate]
    # [END bigquery_load_table_gcs_json_truncate]
    # [END bigquery_load_table_gcs_parquet_truncate]
    # [END bigquery_load_table_gcs_orc_truncate]

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out

    # [END bigquery_load_table_gcs_orc_truncate]