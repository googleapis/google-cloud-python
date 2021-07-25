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

import pytest

from google.cloud import bigquery
import test_utils.prefixer

from . import helpers

prefixer = test_utils.prefixer.Prefixer("python-bigquery", "tests/system")


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
