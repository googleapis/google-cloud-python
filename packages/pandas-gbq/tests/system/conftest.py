# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import functools
import pathlib

from google.cloud import bigquery
import pytest
import test_utils.prefixer


prefixer = test_utils.prefixer.Prefixer("python-bigquery-pandas", "tests/system")

REPO_DIR = pathlib.Path(__file__).parent.parent.parent


# TODO: remove when fully migrated off of Circle CI
@pytest.fixture(scope="session", autouse=True)
def default_credentials():
    """Setup application default credentials for use in code samples."""
    # Written by the 'ci/config_auth.sh' script.
    path = REPO_DIR / "ci" / "service_account.json"

    if path.is_file() and "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(path)


@pytest.fixture(scope="session", autouse=True)
def cleanup_datasets(bigquery_client: bigquery.Client):
    for dataset in bigquery_client.list_datasets():
        if prefixer.should_cleanup(dataset.dataset_id):
            bigquery_client.delete_dataset(
                dataset.reference, delete_contents=True, not_found_ok=True
            )


@pytest.fixture(scope="session")
def bigquery_client() -> bigquery.Client:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GBQ_PROJECT_ID"))
    return bigquery.Client(project=project_id)


@pytest.fixture()
def credentials(bigquery_client):
    return bigquery_client._credentials


@pytest.fixture(scope="session")
def project_id(bigquery_client) -> str:
    return bigquery_client.project


@pytest.fixture(scope="session")
def project(project_id):
    return project_id


@pytest.fixture
def to_gbq(credentials, project_id):
    import pandas_gbq

    return functools.partial(
        pandas_gbq.to_gbq, project_id=project_id, credentials=credentials
    )


@pytest.fixture
def read_gbq(credentials, project_id):
    import pandas_gbq

    return functools.partial(
        pandas_gbq.read_gbq, project_id=project_id, credentials=credentials
    )


@pytest.fixture()
def random_dataset_id(bigquery_client: bigquery.Client, project_id: str):
    dataset_id = prefixer.create_prefix()
    full_dataset_id = f"{project_id}.{dataset_id}"
    yield dataset_id
    bigquery_client.delete_dataset(
        full_dataset_id, delete_contents=True, not_found_ok=True
    )


@pytest.fixture()
def gbq_connector(project, credentials):
    from pandas_gbq import gbq

    return gbq.GbqConnector(project, credentials=credentials)


@pytest.fixture()
def random_dataset(bigquery_client, random_dataset_id):
    from google.cloud import bigquery

    dataset_ref = bigquery.DatasetReference(bigquery_client.project, random_dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    bigquery_client.create_dataset(dataset)
    return dataset


@pytest.fixture()
def tokyo_dataset(bigquery_client, random_dataset_id):
    from google.cloud import bigquery

    dataset_ref = bigquery.DatasetReference(bigquery_client.project, random_dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "asia-northeast1"
    bigquery_client.create_dataset(dataset)
    return random_dataset_id


@pytest.fixture()
def tokyo_table(bigquery_client, tokyo_dataset):
    table_id = "tokyo_table"
    # Create a random table using DDL.
    # https://github.com/GoogleCloudPlatform/golang-samples/blob/2ab2c6b79a1ea3d71d8f91609b57a8fbde07ae5d/bigquery/snippets/snippet.go#L739
    bigquery_client.query(
        """CREATE TABLE {}.{}
        AS SELECT
          2000 + CAST(18 * RAND() as INT64) as year,
          IF(RAND() > 0.5,"foo","bar") as token
        FROM UNNEST(GENERATE_ARRAY(0,5,1)) as r
        """.format(
            tokyo_dataset, table_id
        ),
        location="asia-northeast1",
    ).result()
    return table_id


@pytest.fixture()
def gbq_dataset(project, credentials):
    from pandas_gbq import gbq

    return gbq._Dataset(project, credentials=credentials)


@pytest.fixture()
def gbq_table(project, credentials, random_dataset_id):
    from pandas_gbq import gbq

    return gbq._Table(project, random_dataset_id, credentials=credentials)
