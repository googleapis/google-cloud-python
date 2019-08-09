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


def load_table_from_uri_autodetect(client, to_delete, capsys):

    # [START bigquery_load_table_gcs_json_autodetect]
    """Load table from a GCS URI using various formats and auto-detected schema

    Each file format has its own tested load from URI sample. Because most of
    the code is common for autodetect, append, and truncate, this sample
    includes snippets for all supported formats but only calls a single load
    job.

    This code snippet is made up of shared code, then format-specific code,
    followed by more shared code. Note that only the last format in the
    format-specific code section will be tested in this test.
    """
    dataset_id = "load_table_from_uri_auto_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # Shared code
    # [START bigquery_load_table_gcs_csv_autodetect]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    # [END bigquery_load_table_gcs_csv_autodetect]

    # Format-specific code
    # [START bigquery_load_table_gcs_csv_autodetect]
    job_config.skip_leading_rows = 1
    # The source format defaults to CSV, so the line below is optional.
    job_config.source_format = bigquery.SourceFormat.CSV
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    # [END bigquery_load_table_gcs_csv_autodetect]
    # unset csv-specific attribute
    del job_config._properties["load"]["skipLeadingRows"]

    # [START bigquery_load_table_gcs_json_autodetect]
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"
    # [END bigquery_load_table_gcs_json_autodetect]

    # Shared code
    # [START bigquery_load_table_gcs_csv_autodetect]
    # [START bigquery_load_table_gcs_json_autodetect]
    load_job = client.load_table_from_uri(
        uri, dataset_ref.table("us_states"), job_config=job_config
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(dataset_ref.table("us_states"))
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_csv_autodetect]
    # [END bigquery_load_table_gcs_json_autodetect]

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out

    # [END bigquery_load_table_gcs_json_autodetect]