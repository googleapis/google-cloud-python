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


def load_table_from_uri_json(client, to_delete, capsys):

    # [START bigquery_load_table_gcs_json]
    dataset_id = "load_table_from_uri_json_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = "US"
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"

    load_job = client.load_table_from_uri(
        uri,
        dataset_ref.table("us_states"),
        location="US",  # Location must match that of the destination dataset.
        job_config=job_config,
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(dataset_ref.table("us_states"))
    print("Loaded {} rows.".format(destination_table.num_rows))

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out

    # [END bigquery_load_table_gcs_json]