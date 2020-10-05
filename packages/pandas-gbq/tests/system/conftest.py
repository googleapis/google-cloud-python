import google.oauth2.service_account
import pytest


@pytest.fixture(params=["env"])
def project(request, project_id):
    if request.param == "env":
        return project_id
    elif request.param == "none":
        return None


@pytest.fixture()
def credentials(private_key_path):
    return google.oauth2.service_account.Credentials.from_service_account_file(
        private_key_path
    )


@pytest.fixture()
def gbq_connector(project, credentials):
    from pandas_gbq import gbq

    return gbq.GbqConnector(project, credentials=credentials)


@pytest.fixture()
def random_dataset(bigquery_client, random_dataset_id):
    from google.cloud import bigquery

    dataset_ref = bigquery.DatasetReference(
        bigquery_client.project, random_dataset_id
    )
    dataset = bigquery.Dataset(dataset_ref)
    bigquery_client.create_dataset(dataset)
    return dataset


@pytest.fixture()
def tokyo_dataset(bigquery_client, random_dataset_id):
    from google.cloud import bigquery

    dataset_ref = bigquery.DatasetReference(
        bigquery_client.project, random_dataset_id
    )
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
