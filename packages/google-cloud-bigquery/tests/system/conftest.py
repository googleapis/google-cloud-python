# Copyright 2021 Google LLC
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

import pathlib

import pytest
import test_utils.prefixer

from google.cloud import bigquery
from google.cloud.bigquery import enums
from . import helpers


prefixer = test_utils.prefixer.Prefixer("python-bigquery", "tests/system")

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


@pytest.fixture(scope="session", autouse=True)
def cleanup_datasets(bigquery_client: bigquery.Client):
    for dataset in bigquery_client.list_datasets():
        if prefixer.should_cleanup(dataset.dataset_id):
            bigquery_client.delete_dataset(
                dataset, delete_contents=True, not_found_ok=True
            )


@pytest.fixture(scope="session")
def bigquery_client():
    return bigquery.Client()


@pytest.fixture(scope="session")
def project_id(bigquery_client: bigquery.Client):
    return bigquery_client.project


@pytest.fixture(scope="session")
def bqstorage_client(bigquery_client):
    from google.cloud import bigquery_storage

    return bigquery_storage.BigQueryReadClient(credentials=bigquery_client._credentials)


@pytest.fixture(scope="session")
def dataset_id(bigquery_client):
    dataset_id = prefixer.create_prefix()
    bigquery_client.create_dataset(dataset_id)
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)


@pytest.fixture
def table_id(dataset_id):
    return f"{dataset_id}.table_{helpers.temp_suffix()}"


@pytest.fixture(scope="session")
def scalars_table(bigquery_client: bigquery.Client, project_id: str, dataset_id: str):
    schema = bigquery_client.schema_from_json(DATA_DIR / "scalars_schema.json")
    job_config = bigquery.LoadJobConfig()
    job_config.schema = schema
    job_config.source_format = enums.SourceFormat.NEWLINE_DELIMITED_JSON
    full_table_id = f"{project_id}.{dataset_id}.scalars"
    with open(DATA_DIR / "scalars.jsonl", "rb") as data_file:
        job = bigquery_client.load_table_from_file(
            data_file, full_table_id, job_config=job_config
        )
    job.result()
    yield full_table_id
    bigquery_client.delete_table(full_table_id)


@pytest.fixture(scope="session")
def scalars_extreme_table(
    bigquery_client: bigquery.Client, project_id: str, dataset_id: str
):
    schema = bigquery_client.schema_from_json(DATA_DIR / "scalars_schema.json")
    job_config = bigquery.LoadJobConfig()
    job_config.schema = schema
    job_config.source_format = enums.SourceFormat.NEWLINE_DELIMITED_JSON
    full_table_id = f"{project_id}.{dataset_id}.scalars_extreme"
    with open(DATA_DIR / "scalars_extreme.jsonl", "rb") as data_file:
        job = bigquery_client.load_table_from_file(
            data_file, full_table_id, job_config=job_config
        )
    job.result()
    yield full_table_id
    bigquery_client.delete_table(full_table_id)
