"""Shared pytest fixtures for `tests/system` and `samples/tests` tests."""

import os
import os.path
import uuid

import google.oauth2.service_account
import pytest


@pytest.fixture(scope="session")
def project_id():
    return os.environ.get("GBQ_PROJECT_ID") or os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # noqa


@pytest.fixture(scope="session")
def private_key_path():
    path = os.path.join(
        "ci", "service_account.json"
    )  # Written by the 'ci/config_auth.sh' script.
    if "GBQ_GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        path = os.environ["GBQ_GOOGLE_APPLICATION_CREDENTIALS"]
    elif "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    if not os.path.isfile(path):
        pytest.skip(
            "Cannot run integration tests when there is "
            "no file at the private key json file path"
        )
        return None

    return path


@pytest.fixture(scope="session")
def private_key_contents(private_key_path):
    if private_key_path is None:
        return None

    with open(private_key_path) as f:
        return f.read()


@pytest.fixture(scope="module")
def bigquery_client(project_id, private_key_path):
    from google.cloud import bigquery

    return bigquery.Client.from_service_account_json(
        private_key_path, project=project_id
    )


@pytest.fixture()
def random_dataset_id(bigquery_client):
    import google.api_core.exceptions
    from google.cloud import bigquery

    dataset_id = "".join(["pandas_gbq_", str(uuid.uuid4()).replace("-", "_")])
    dataset_ref = bigquery.DatasetReference(
        bigquery_client.project, dataset_id
    )
    yield dataset_id
    try:
        bigquery_client.delete_dataset(dataset_ref, delete_contents=True)
    except google.api_core.exceptions.NotFound:
        pass  # Not all tests actually create a dataset


@pytest.fixture()
def credentials(private_key_path):
    return google.oauth2.service_account.Credentials.from_service_account_file(
        private_key_path
    )
