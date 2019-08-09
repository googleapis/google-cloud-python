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


def load_table_from_uri_cmek(client, to_delete):

    # [START bigquery_load_table_gcs_json_cmek]
    dataset_id = "load_table_from_uri_cmek_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = "US"
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    # Set the encryption key to use for the destination.
    # TODO: Replace this key with a key you have created in KMS.
    kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
        "cloud-samples-tests", "us-central1", "test", "test"
    )
    encryption_config = bigquery.EncryptionConfiguration(kms_key_name=kms_key_name)
    job_config.destination_encryption_configuration = encryption_config
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"

    load_job = client.load_table_from_uri(
        uri,
        dataset_ref.table("us_states"),
        location="US",  # Location must match that of the destination dataset.
        job_config=job_config,
    )  # API request

    assert load_job.job_type == "load"

    load_job.result()  # Waits for table load to complete.

    assert load_job.state == "DONE"
    table = client.get_table(dataset_ref.table("us_states"))
    assert table.encryption_configuration.kms_key_name == kms_key_name

    # [END bigquery_load_table_gcs_json_cmek]