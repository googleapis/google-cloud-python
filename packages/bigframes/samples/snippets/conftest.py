# Copyright 2020 Google LLC
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

from typing import Generator, Iterator

from google.cloud import bigquery, storage
import pytest
import test_utils.prefixer

import bigframes.pandas as bpd

prefixer = test_utils.prefixer.Prefixer(
    "python-bigquery-dataframes", "samples/snippets"
)

routine_prefixer = test_utils.prefixer.Prefixer("bigframes", "")


@pytest.fixture(scope="session", autouse=True)
def cleanup_datasets(bigquery_client: bigquery.Client) -> None:
    for dataset in bigquery_client.list_datasets():
        if prefixer.should_cleanup(dataset.dataset_id):
            bigquery_client.delete_dataset(
                dataset, delete_contents=True, not_found_ok=True
            )


@pytest.fixture(scope="session")
def bigquery_client() -> bigquery.Client:
    bigquery_client = bigquery.Client()
    return bigquery_client


@pytest.fixture(scope="session")
def storage_client(project_id: str) -> storage.Client:
    return storage.Client(project=project_id)


@pytest.fixture(scope="session")
def project_id(bigquery_client: bigquery.Client) -> str:
    return bigquery_client.project


@pytest.fixture(scope="session")
def gcs_bucket(storage_client: storage.Client) -> Generator[str, None, None]:
    bucket_name = "bigframes_blob_test_with_data_wipeout"

    yield bucket_name

    bucket = storage_client.get_bucket(bucket_name)
    for blob in bucket.list_blobs():
        blob.delete()


@pytest.fixture(scope="session")
def gcs_bucket_snippets(storage_client: storage.Client) -> Generator[str, None, None]:
    bucket_name = "bigframes_blob_test_snippet_with_data_wipeout"

    yield bucket_name

    bucket = storage_client.get_bucket(bucket_name)
    for blob in bucket.list_blobs():
        blob.delete()


@pytest.fixture(autouse=True)
def reset_session() -> None:
    """An autouse fixture ensuring each sample runs in a fresh session.

    This allows us to have samples that query data in different locations.
    """
    bpd.reset_session()
    bpd.options.bigquery.location = None


@pytest.fixture(scope="session")
def dataset_id(bigquery_client: bigquery.Client, project_id: str) -> Iterator[str]:
    dataset_id = prefixer.create_prefix()
    full_dataset_id = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(full_dataset_id)
    bigquery_client.create_dataset(dataset)
    yield dataset_id
    bigquery_client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)


@pytest.fixture(scope="session")
def dataset_id_eu(bigquery_client: bigquery.Client, project_id: str) -> Iterator[str]:
    dataset_id = prefixer.create_prefix()
    full_dataset_id = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(full_dataset_id)
    dataset.location = "EU"
    bigquery_client.create_dataset(dataset)
    yield dataset_id
    bigquery_client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)


@pytest.fixture
def random_model_id(
    bigquery_client: bigquery.Client, project_id: str, dataset_id: str
) -> Iterator[str]:
    """Create a new table ID each time, so random_model_id can be used as
    target for load jobs.
    """
    random_model_id = prefixer.create_prefix()
    full_model_id = f"{project_id}.{dataset_id}.{random_model_id}"
    yield full_model_id
    bigquery_client.delete_model(full_model_id, not_found_ok=True)


@pytest.fixture
def random_model_id_eu(
    bigquery_client: bigquery.Client, project_id: str, dataset_id_eu: str
) -> Iterator[str]:
    """
    Create a new table ID each time, so random_model_id_eu can be used
    as a target for load jobs.
    """
    random_model_id_eu = prefixer.create_prefix()
    full_model_id = f"{project_id}.{dataset_id_eu}.{random_model_id_eu}"
    yield full_model_id
    bigquery_client.delete_model(full_model_id, not_found_ok=True)


@pytest.fixture
def routine_id() -> Iterator[str]:
    """Create a new BQ routine ID each time, so random_routine_id can be used as
    target for udf creation.
    """
    random_routine_id = routine_prefixer.create_prefix()
    yield random_routine_id
