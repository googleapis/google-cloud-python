# Copyright 2019. PyData Development Team
# Distributed under BSD 3-Clause License.
# See LICENSE.txt for details.

from google.cloud import bigquery
import pytest
import test_utils.prefixer


prefixer = test_utils.prefixer.Prefixer("python-bigquery-pandas", "samples/snippets")


@pytest.fixture(scope="session", autouse=True)
def cleanup_datasets(bigquery_client: bigquery.Client):
    for dataset in bigquery_client.list_datasets():
        if prefixer.should_cleanup(dataset.dataset_id):
            bigquery_client.delete_dataset(
                dataset, delete_contents=True, not_found_ok=True
            )


@pytest.fixture(scope="session")
def bigquery_client() -> bigquery.Client:
    return bigquery.Client()


@pytest.fixture(scope="session")
def project_id(bigquery_client) -> str:
    return bigquery_client.project


@pytest.fixture(scope="session")
def dataset_id(bigquery_client: bigquery.Client, project_id: str):
    dataset_id = prefixer.create_prefix()
    full_dataset_id = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(full_dataset_id)
    bigquery_client.create_dataset(dataset)
    yield dataset_id
    bigquery_client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)
