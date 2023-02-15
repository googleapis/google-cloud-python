# Copyright 2023 Google LLC
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
#

import os
import uuid

import pytest
from samples.snippets import entities_to_bigquery_sample

from google.cloud import bigquery

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
gcs_bucket_name = "documentai_toolbox_samples"
gcs_input_uri = "output/123456789/0"
dataset_name = f"document_ai_toolbox_test_{uuid.uuid4().hex}"
table_name = f"test_table_{uuid.uuid4().hex}"


def test_entities_to_bigquery_sample(capsys: pytest.CaptureFixture) -> None:
    client = bigquery.Client(project=project_id)
    dataset = bigquery.Dataset(f"{project_id}.{dataset_name}")
    dataset.location = "US"
    dataset = client.create_dataset(dataset, timeout=30, exists_ok=True)

    entities_to_bigquery_sample.entities_to_bigquery_sample(
        gcs_bucket_name=gcs_bucket_name,
        gcs_prefix=gcs_input_uri,
        dataset_name=dataset_name,
        table_name=table_name,
        project_id=project_id,
    )
    out, _ = capsys.readouterr()

    assert "Document entities loaded into BigQuery" in out
    assert "Job ID:" in out
    assert (
        f"Table: /projects/{project_id}/datasets/{dataset_name}/tables/{table_name}"
        in out
    )

    client.delete_dataset(dataset)
