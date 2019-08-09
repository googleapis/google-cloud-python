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


def copy_table_cmek(client, to_delete):

    # [START bigquery_copy_table_cmek]
    dataset_id = "copy_table_cmek_{}".format(_millis())
    dest_dataset = bigquery.Dataset(client.dataset(dataset_id))
    dest_dataset.location = "US"
    dest_dataset = client.create_dataset(dest_dataset)
    to_delete.append(dest_dataset)

    # from google.cloud import bigquery
    # client = bigquery.Client()

    source_dataset = bigquery.DatasetReference("bigquery-public-data", "samples")
    source_table_ref = source_dataset.table("shakespeare")

    # dataset_id = 'my_dataset'
    dest_dataset_ref = client.dataset(dataset_id)
    dest_table_ref = dest_dataset_ref.table("destination_table")

    # Set the encryption key to use for the destination.
    # TODO: Replace this key with a key you have created in KMS.
    kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
        "cloud-samples-tests", "us-central1", "test", "test"
    )
    encryption_config = bigquery.EncryptionConfiguration(kms_key_name=kms_key_name)
    job_config = bigquery.CopyJobConfig()
    job_config.destination_encryption_configuration = encryption_config

    job = client.copy_table(
        source_table_ref,
        dest_table_ref,
        # Location must match that of the source and destination tables.
        location="US",
        job_config=job_config,
    )  # API request
    job.result()  # Waits for job to complete.

    assert job.state == "DONE"
    dest_table = client.get_table(dest_table_ref)
    assert dest_table.encryption_configuration.kms_key_name == kms_key_name

    # [END bigquery_copy_table_cmek]