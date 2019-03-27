# Copyright 2016 Google LLC
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

"""Testable usage examples for Google BigQuery API wrapper

Each example function takes a ``client`` argument (which must be an instance
of :class:`google.cloud.bigquery.client.Client`) and uses it to perform a task
with the API.

To facilitate running the examples as system tests, each example is also passed
a ``to_delete`` list;  the function adds to the list any objects created which
need to be deleted during teardown.
"""

import os
import time

import mock
import pytest
import six

try:
    import fastparquet
except (ImportError, AttributeError):
    fastparquet = None
try:
    import pandas
except (ImportError, AttributeError):
    pandas = None
try:
    import pyarrow
except (ImportError, AttributeError):
    pyarrow = None

from google.api_core import datetime_helpers
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import ServiceUnavailable
from google.api_core.exceptions import TooManyRequests
from google.cloud import bigquery
from google.cloud import storage
from test_utils.retry import RetryErrors

ORIGINAL_FRIENDLY_NAME = "Original friendly name"
ORIGINAL_DESCRIPTION = "Original description"
LOCALLY_CHANGED_FRIENDLY_NAME = "Locally-changed friendly name"
LOCALLY_CHANGED_DESCRIPTION = "Locally-changed description"
UPDATED_FRIENDLY_NAME = "Updated friendly name"
UPDATED_DESCRIPTION = "Updated description"

SCHEMA = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
]

ROWS = [
    ("Phred Phlyntstone", 32),
    ("Bharney Rhubble", 33),
    ("Wylma Phlyntstone", 29),
    ("Bhettye Rhubble", 27),
]

QUERY = (
    "SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` "
    'WHERE state = "TX"'
)


retry_429 = RetryErrors(TooManyRequests)
retry_storage_errors = RetryErrors(
    (TooManyRequests, InternalServerError, ServiceUnavailable)
)


@pytest.fixture(scope="module")
def client():
    return bigquery.Client()


@pytest.fixture
def to_delete(client):
    doomed = []
    yield doomed
    for item in doomed:
        if isinstance(item, (bigquery.Dataset, bigquery.DatasetReference)):
            retry_429(client.delete_dataset)(item, delete_contents=True)
        elif isinstance(item, storage.Bucket):
            retry_storage_errors(item.delete)()
        else:
            retry_429(item.delete)()


def _millis():
    return int(time.time() * 1000)


class _CloseOnDelete(object):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def delete(self):
        self._wrapped.close()


def test_create_client_default_credentials():
    """Create a BigQuery client with Application Default Credentials"""

    # [START bigquery_client_default_credentials]
    from google.cloud import bigquery

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    client = bigquery.Client()
    # [END bigquery_client_default_credentials]

    assert client is not None


def test_create_client_json_credentials():
    """Create a BigQuery client with Application Default Credentials"""
    with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]) as creds_file:
        creds_file_data = creds_file.read()

    open_mock = mock.mock_open(read_data=creds_file_data)

    with mock.patch("io.open", open_mock):
        # [START bigquery_client_json_credentials]
        from google.cloud import bigquery

        # Explicitly use service account credentials by specifying the private
        # key file. All clients in google-cloud-python have this helper.
        client = bigquery.Client.from_service_account_json(
            "path/to/service_account.json"
        )
        # [END bigquery_client_json_credentials]

    assert client is not None


def test_list_datasets(client):
    """List datasets for a project."""
    # [START bigquery_list_datasets]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    datasets = list(client.list_datasets())
    project = client.project

    if datasets:
        print("Datasets in project {}:".format(project))
        for dataset in datasets:  # API request(s)
            print("\t{}".format(dataset.dataset_id))
    else:
        print("{} project does not contain any datasets.".format(project))
    # [END bigquery_list_datasets]


def test_list_datasets_by_label(client, to_delete):
    dataset_id = "list_datasets_by_label_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.labels = {"color": "green"}
    dataset = client.create_dataset(dataset)  # API request
    to_delete.append(dataset)

    # [START bigquery_list_datasets_by_label]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    # The following label filter example will find datasets with an
    # arbitrary 'color' label set to 'green'
    label_filter = "labels.color:green"
    datasets = list(client.list_datasets(filter=label_filter))

    if datasets:
        print("Datasets filtered by {}:".format(label_filter))
        for dataset in datasets:  # API request(s)
            print("\t{}".format(dataset.dataset_id))
    else:
        print("No datasets found with this filter.")
    # [END bigquery_list_datasets_by_label]
    found = set([dataset.dataset_id for dataset in datasets])
    assert dataset_id in found


def test_create_dataset(client, to_delete):
    """Create a dataset."""
    dataset_id = "create_dataset_{}".format(_millis())

    # [START bigquery_create_dataset]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    # Create a DatasetReference using a chosen dataset ID.
    # The project defaults to the Client's project if not specified.
    dataset_ref = client.dataset(dataset_id)

    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_ref)
    # Specify the geographic location where the dataset should reside.
    dataset.location = "US"

    # Send the dataset to the API for creation.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    dataset = client.create_dataset(dataset)  # API request
    # [END bigquery_create_dataset]

    to_delete.append(dataset)


def test_get_dataset_information(client, to_delete):
    """View information about a dataset."""
    dataset_id = "get_dataset_{}".format(_millis())
    dataset_labels = {"color": "green"}
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.description = ORIGINAL_DESCRIPTION
    dataset.labels = dataset_labels
    dataset = client.create_dataset(dataset)  # API request
    to_delete.append(dataset)

    # [START bigquery_get_dataset]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    dataset = client.get_dataset(dataset_ref)  # API request

    # View dataset properties
    print("Dataset ID: {}".format(dataset_id))
    print("Description: {}".format(dataset.description))
    print("Labels:")
    labels = dataset.labels
    if labels:
        for label, value in labels.items():
            print("\t{}: {}".format(label, value))
    else:
        print("\tDataset has no labels defined.")

    # View tables in dataset
    print("Tables:")
    tables = list(client.list_tables(dataset_ref))  # API request(s)
    if tables:
        for table in tables:
            print("\t{}".format(table.table_id))
    else:
        print("\tThis dataset does not contain any tables.")
    # [END bigquery_get_dataset]

    assert dataset.description == ORIGINAL_DESCRIPTION
    assert dataset.labels == dataset_labels
    assert tables == []


# [START bigquery_dataset_exists]
def dataset_exists(client, dataset_reference):
    """Return if a dataset exists.

    Args:
        client (google.cloud.bigquery.client.Client):
            A client to connect to the BigQuery API.
        dataset_reference (google.cloud.bigquery.dataset.DatasetReference):
            A reference to the dataset to look for.

    Returns:
        bool: ``True`` if the dataset exists, ``False`` otherwise.
    """
    from google.cloud.exceptions import NotFound

    try:
        client.get_dataset(dataset_reference)
        return True
    except NotFound:
        return False


# [END bigquery_dataset_exists]


def test_dataset_exists(client, to_delete):
    """Determine if a dataset exists."""
    DATASET_ID = "get_table_dataset_{}".format(_millis())
    dataset_ref = client.dataset(DATASET_ID)
    dataset = bigquery.Dataset(dataset_ref)
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    assert dataset_exists(client, dataset_ref)
    assert not dataset_exists(client, client.dataset("i_dont_exist"))


@pytest.mark.skip(
    reason=(
        "update_dataset() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5588"
    )
)
def test_update_dataset_description(client, to_delete):
    """Update a dataset's description."""
    dataset_id = "update_dataset_description_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.description = "Original description."
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_update_dataset_description]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # dataset = client.get_dataset(dataset_ref)  # API request

    assert dataset.description == "Original description."
    dataset.description = "Updated description."

    dataset = client.update_dataset(dataset, ["description"])  # API request

    assert dataset.description == "Updated description."
    # [END bigquery_update_dataset_description]


@pytest.mark.skip(
    reason=(
        "update_dataset() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5588"
    )
)
def test_update_dataset_default_table_expiration(client, to_delete):
    """Update a dataset's default table expiration."""
    dataset_id = "update_dataset_default_expiration_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_update_dataset_expiration]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # dataset = client.get_dataset(dataset_ref)  # API request

    assert dataset.default_table_expiration_ms is None
    one_day_ms = 24 * 60 * 60 * 1000  # in milliseconds
    dataset.default_table_expiration_ms = one_day_ms

    dataset = client.update_dataset(
        dataset, ["default_table_expiration_ms"]
    )  # API request

    assert dataset.default_table_expiration_ms == one_day_ms
    # [END bigquery_update_dataset_expiration]


@pytest.mark.skip(
    reason=(
        "update_dataset() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5588"
    )
)
def test_manage_dataset_labels(client, to_delete):
    dataset_id = "label_dataset_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_label_dataset]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # dataset = client.get_dataset(dataset_ref)  # API request

    assert dataset.labels == {}
    labels = {"color": "green"}
    dataset.labels = labels

    dataset = client.update_dataset(dataset, ["labels"])  # API request

    assert dataset.labels == labels
    # [END bigquery_label_dataset]

    # [START bigquery_get_dataset_labels]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    dataset = client.get_dataset(dataset_ref)  # API request

    # View dataset labels
    print("Dataset ID: {}".format(dataset_id))
    print("Labels:")
    if dataset.labels:
        for label, value in dataset.labels.items():
            print("\t{}: {}".format(label, value))
    else:
        print("\tDataset has no labels defined.")
    # [END bigquery_get_dataset_labels]
    assert dataset.labels == labels

    # [START bigquery_delete_label_dataset]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # dataset = client.get_dataset(dataset_ref)  # API request

    # This example dataset starts with one label
    assert dataset.labels == {"color": "green"}
    # To delete a label from a dataset, set its value to None
    dataset.labels["color"] = None

    dataset = client.update_dataset(dataset, ["labels"])  # API request

    assert dataset.labels == {}
    # [END bigquery_delete_label_dataset]


@pytest.mark.skip(
    reason=(
        "update_dataset() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5588"
    )
)
def test_update_dataset_access(client, to_delete):
    """Update a dataset's access controls."""
    dataset_id = "update_dataset_access_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_update_dataset_access]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset = client.get_dataset(client.dataset('my_dataset'))

    entry = bigquery.AccessEntry(
        role="READER",
        entity_type="userByEmail",
        entity_id="sample.bigquery.dev@gmail.com",
    )
    assert entry not in dataset.access_entries
    entries = list(dataset.access_entries)
    entries.append(entry)
    dataset.access_entries = entries

    dataset = client.update_dataset(dataset, ["access_entries"])  # API request

    assert entry in dataset.access_entries
    # [END bigquery_update_dataset_access]


def test_delete_dataset(client):
    """Delete a dataset."""
    from google.cloud.exceptions import NotFound

    dataset1_id = "delete_dataset_{}".format(_millis())
    dataset1 = bigquery.Dataset(client.dataset(dataset1_id))
    client.create_dataset(dataset1)

    dataset2_id = "delete_dataset_with_tables{}".format(_millis())
    dataset2 = bigquery.Dataset(client.dataset(dataset2_id))
    client.create_dataset(dataset2)

    table = bigquery.Table(dataset2.table("new_table"))
    client.create_table(table)

    # [START bigquery_delete_dataset]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    # Delete a dataset that does not contain any tables
    # dataset1_id = 'my_empty_dataset'
    dataset1_ref = client.dataset(dataset1_id)
    client.delete_dataset(dataset1_ref)  # API request

    print("Dataset {} deleted.".format(dataset1_id))

    # Use the delete_contents parameter to delete a dataset and its contents
    # dataset2_id = 'my_dataset_with_tables'
    dataset2_ref = client.dataset(dataset2_id)
    client.delete_dataset(dataset2_ref, delete_contents=True)  # API request

    print("Dataset {} deleted.".format(dataset2_id))
    # [END bigquery_delete_dataset]

    for dataset in [dataset1, dataset2]:
        with pytest.raises(NotFound):
            client.get_dataset(dataset)  # API request


def test_list_tables(client, to_delete):
    """List tables within a dataset."""
    dataset_id = "list_tables_dataset_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = client.create_dataset(bigquery.Dataset(dataset_ref))
    to_delete.append(dataset)

    # [START bigquery_list_tables]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    tables = list(client.list_tables(dataset_ref))  # API request(s)
    assert len(tables) == 0

    table_ref = dataset.table("my_table")
    table = bigquery.Table(table_ref)
    client.create_table(table)  # API request
    tables = list(client.list_tables(dataset))  # API request(s)

    assert len(tables) == 1
    assert tables[0].table_id == "my_table"
    # [END bigquery_list_tables]


def test_create_table(client, to_delete):
    """Create a table."""
    dataset_id = "create_table_dataset_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_create_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]
    table_ref = dataset_ref.table("my_table")
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)  # API request

    assert table.table_id == "my_table"
    # [END bigquery_create_table]


def test_create_table_nested_repeated_schema(client, to_delete):
    dataset_id = "create_table_nested_repeated_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_nested_repeated_schema]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    schema = [
        bigquery.SchemaField("id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("dob", "DATE", mode="NULLABLE"),
        bigquery.SchemaField(
            "addresses",
            "RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField("status", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("address", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("city", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("state", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("zip", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("numberOfYears", "STRING", mode="NULLABLE"),
            ],
        ),
    ]
    table_ref = dataset_ref.table("my_table")
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)  # API request

    print("Created table {}".format(table.full_table_id))
    # [END bigquery_nested_repeated_schema]


def test_create_table_cmek(client, to_delete):
    dataset_id = "create_table_cmek_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_create_table_cmek]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    table_ref = client.dataset(dataset_id).table("my_table")
    table = bigquery.Table(table_ref)

    # Set the encryption key to use for the table.
    # TODO: Replace this key with a key you have created in Cloud KMS.
    kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
        "cloud-samples-tests", "us-central1", "test", "test"
    )
    table.encryption_configuration = bigquery.EncryptionConfiguration(
        kms_key_name=kms_key_name
    )

    table = client.create_table(table)  # API request

    assert table.encryption_configuration.kms_key_name == kms_key_name
    # [END bigquery_create_table_cmek]


def test_create_partitioned_table(client, to_delete):
    dataset_id = "create_table_partitioned_{}".format(_millis())
    dataset_ref = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset_ref)
    to_delete.append(dataset)

    # [START bigquery_create_table_partitioned]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    table_ref = dataset_ref.table("my_partitioned_table")
    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
        bigquery.SchemaField("date", "DATE"),
    ]
    table = bigquery.Table(table_ref, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="date",  # name of column to use for partitioning
        expiration_ms=7776000000,
    )  # 90 days

    table = client.create_table(table)

    print(
        "Created table {}, partitioned on column {}".format(
            table.table_id, table.time_partitioning.field
        )
    )
    # [END bigquery_create_table_partitioned]

    assert table.time_partitioning.type_ == "DAY"
    assert table.time_partitioning.field == "date"
    assert table.time_partitioning.expiration_ms == 7776000000


def test_load_and_query_partitioned_table(client, to_delete):
    dataset_id = "load_partitioned_table_dataset_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_partitioned]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    table_id = "us_states_by_date"

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
        bigquery.SchemaField("date", "DATE"),
    ]
    job_config.skip_leading_rows = 1
    job_config.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="date",  # name of column to use for partitioning
        expiration_ms=7776000000,
    )  # 90 days
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states-by-date.csv"

    load_job = client.load_table_from_uri(
        uri, dataset_ref.table(table_id), job_config=job_config
    )  # API request

    assert load_job.job_type == "load"

    load_job.result()  # Waits for table load to complete.

    table = client.get_table(dataset_ref.table(table_id))
    print("Loaded {} rows to table {}".format(table.num_rows, table_id))
    # [END bigquery_load_table_partitioned]
    assert table.num_rows == 50

    project_id = client.project

    # [START bigquery_query_partitioned_table]
    import datetime

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # project_id = 'my-project'
    # dataset_id = 'my_dataset'
    table_id = "us_states_by_date"

    sql_template = """
        SELECT *
        FROM `{}.{}.{}`
        WHERE date BETWEEN @start_date AND @end_date
    """
    sql = sql_template.format(project_id, dataset_id, table_id)
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = [
        bigquery.ScalarQueryParameter("start_date", "DATE", datetime.date(1800, 1, 1)),
        bigquery.ScalarQueryParameter("end_date", "DATE", datetime.date(1899, 12, 31)),
    ]

    query_job = client.query(
        sql,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request

    rows = list(query_job)
    print("{} states were admitted to the US in the 1800s".format(len(rows)))
    # [END bigquery_query_partitioned_table]
    assert len(rows) == 29


def test_get_table_information(client, to_delete):
    """Show a table's properties."""
    dataset_id = "show_table_dataset_{}".format(_millis())
    table_id = "show_table_table_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table.description = ORIGINAL_DESCRIPTION
    table = client.create_table(table)

    # [START bigquery_get_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)  # API Request

    # View table properties
    print(table.schema)
    print(table.description)
    print(table.num_rows)
    # [END bigquery_get_table]

    assert table.schema == SCHEMA
    assert table.description == ORIGINAL_DESCRIPTION
    assert table.num_rows == 0


# [START bigquery_table_exists]
def table_exists(client, table_reference):
    """Return if a table exists.

    Args:
        client (google.cloud.bigquery.client.Client):
            A client to connect to the BigQuery API.
        table_reference (google.cloud.bigquery.table.TableReference):
            A reference to the table to look for.

    Returns:
        bool: ``True`` if the table exists, ``False`` otherwise.
    """
    from google.cloud.exceptions import NotFound

    try:
        client.get_table(table_reference)
        return True
    except NotFound:
        return False


# [END bigquery_table_exists]


def test_table_exists(client, to_delete):
    """Determine if a table exists."""
    DATASET_ID = "get_table_dataset_{}".format(_millis())
    TABLE_ID = "get_table_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table_ref = dataset.table(TABLE_ID)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    table = client.create_table(table)

    assert table_exists(client, table_ref)
    assert not table_exists(client, dataset.table("i_dont_exist"))


@pytest.mark.skip(
    reason=(
        "update_table() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5589"
    )
)
def test_manage_table_labels(client, to_delete):
    dataset_id = "label_table_dataset_{}".format(_millis())
    table_id = "label_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)

    # [START bigquery_label_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('my_table')
    # table = client.get_table(table_ref)  # API request

    assert table.labels == {}
    labels = {"color": "green"}
    table.labels = labels

    table = client.update_table(table, ["labels"])  # API request

    assert table.labels == labels
    # [END bigquery_label_table]

    # [START bigquery_get_table_labels]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)  # API Request

    # View table labels
    print("Table ID: {}".format(table_id))
    print("Labels:")
    if table.labels:
        for label, value in table.labels.items():
            print("\t{}: {}".format(label, value))
    else:
        print("\tTable has no labels defined.")
    # [END bigquery_get_table_labels]
    assert table.labels == labels

    # [START bigquery_delete_label_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('my_table')
    # table = client.get_table(table_ref)  # API request

    # This example table starts with one label
    assert table.labels == {"color": "green"}
    # To delete a label from a table, set its value to None
    table.labels["color"] = None

    table = client.update_table(table, ["labels"])  # API request

    assert table.labels == {}
    # [END bigquery_delete_label_table]


@pytest.mark.skip(
    reason=(
        "update_table() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5589"
    )
)
def test_update_table_description(client, to_delete):
    """Update a table's description."""
    dataset_id = "update_table_description_dataset_{}".format(_millis())
    table_id = "update_table_description_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table.description = "Original description."
    table = client.create_table(table)

    # [START bigquery_update_table_description]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('my_table')
    # table = client.get_table(table_ref)  # API request

    assert table.description == "Original description."
    table.description = "Updated description."

    table = client.update_table(table, ["description"])  # API request

    assert table.description == "Updated description."
    # [END bigquery_update_table_description]


@pytest.mark.skip(
    reason=(
        "update_table() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5589"
    )
)
def test_update_table_expiration(client, to_delete):
    """Update a table's expiration time."""
    dataset_id = "update_table_expiration_dataset_{}".format(_millis())
    table_id = "update_table_expiration_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)

    # [START bigquery_update_table_expiration]
    import datetime
    import pytz

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('my_table')
    # table = client.get_table(table_ref)  # API request

    assert table.expires is None

    # set table to expire 5 days from now
    expiration = datetime.datetime.now(pytz.utc) + datetime.timedelta(days=5)
    table.expires = expiration
    table = client.update_table(table, ["expires"])  # API request

    # expiration is stored in milliseconds
    margin = datetime.timedelta(microseconds=1000)
    assert expiration - margin <= table.expires <= expiration + margin
    # [END bigquery_update_table_expiration]


@pytest.mark.skip(
    reason=(
        "update_table() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5589"
    )
)
def test_add_empty_column(client, to_delete):
    """Adds an empty column to an existing table."""
    dataset_id = "add_empty_column_dataset_{}".format(_millis())
    table_id = "add_empty_column_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)

    # [START bigquery_add_empty_column]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # API request

    original_schema = table.schema
    new_schema = original_schema[:]  # creates a copy of the schema
    new_schema.append(bigquery.SchemaField("phone", "STRING"))

    table.schema = new_schema
    table = client.update_table(table, ["schema"])  # API request

    assert len(table.schema) == len(original_schema) + 1 == len(new_schema)
    # [END bigquery_add_empty_column]


@pytest.mark.skip(
    reason=(
        "update_table() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5589"
    )
)
def test_relax_column(client, to_delete):
    """Updates a schema field from required to nullable."""
    dataset_id = "relax_column_dataset_{}".format(_millis())
    table_id = "relax_column_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_relax_column]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    original_schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]
    table_ref = client.dataset(dataset_id).table(table_id)
    table = bigquery.Table(table_ref, schema=original_schema)
    table = client.create_table(table)
    assert all(field.mode == "REQUIRED" for field in table.schema)

    # SchemaField properties cannot be edited after initialization.
    # To make changes, construct new SchemaField objects.
    relaxed_schema = [
        bigquery.SchemaField("full_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
    ]
    table.schema = relaxed_schema
    table = client.update_table(table, ["schema"])

    assert all(field.mode == "NULLABLE" for field in table.schema)
    # [END bigquery_relax_column]


@pytest.mark.skip(
    reason=(
        "update_table() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5589"
    )
)
def test_update_table_cmek(client, to_delete):
    """Patch a table's metadata."""
    dataset_id = "update_table_cmek_{}".format(_millis())
    table_id = "update_table_cmek_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id))
    original_kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
        "cloud-samples-tests", "us-central1", "test", "test"
    )
    table.encryption_configuration = bigquery.EncryptionConfiguration(
        kms_key_name=original_kms_key_name
    )
    table = client.create_table(table)

    # [START bigquery_update_table_cmek]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    assert table.encryption_configuration.kms_key_name == original_kms_key_name

    # Set a new encryption key to use for the destination.
    # TODO: Replace this key with a key you have created in KMS.
    updated_kms_key_name = (
        "projects/cloud-samples-tests/locations/us-central1/"
        "keyRings/test/cryptoKeys/otherkey"
    )
    table.encryption_configuration = bigquery.EncryptionConfiguration(
        kms_key_name=updated_kms_key_name
    )

    table = client.update_table(table, ["encryption_configuration"])  # API request

    assert table.encryption_configuration.kms_key_name == updated_kms_key_name
    assert original_kms_key_name != updated_kms_key_name
    # [END bigquery_update_table_cmek]


def test_browse_table_data(client, to_delete, capsys):
    """Retreive selected row data from a table."""

    # [START bigquery_browse_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    dataset_ref = client.dataset("samples", project="bigquery-public-data")
    table_ref = dataset_ref.table("shakespeare")
    table = client.get_table(table_ref)  # API call

    # Load all rows from a table
    rows = client.list_rows(table)
    assert len(list(rows)) == table.num_rows

    # Load the first 10 rows
    rows = client.list_rows(table, max_results=10)
    assert len(list(rows)) == 10

    # Specify selected fields to limit the results to certain columns
    fields = table.schema[:2]  # first two columns
    rows = client.list_rows(table, selected_fields=fields, max_results=10)
    assert len(rows.schema) == 2
    assert len(list(rows)) == 10

    # Use the start index to load an arbitrary portion of the table
    rows = client.list_rows(table, start_index=10, max_results=10)

    # Print row data in tabular format
    format_string = "{!s:<16} " * len(rows.schema)
    field_names = [field.name for field in rows.schema]
    print(format_string.format(*field_names))  # prints column headers
    for row in rows:
        print(format_string.format(*row))  # prints row data
    # [END bigquery_browse_table]

    out, err = capsys.readouterr()
    out = list(filter(bool, out.split("\n")))  # list of non-blank lines
    assert len(out) == 11


@pytest.mark.skip(
    reason=(
        "update_table() is flaky "
        "https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5589"
    )
)
def test_manage_views(client, to_delete):
    project = client.project
    source_dataset_id = "source_dataset_{}".format(_millis())
    source_dataset_ref = client.dataset(source_dataset_id)
    source_dataset = bigquery.Dataset(source_dataset_ref)
    source_dataset = client.create_dataset(source_dataset)
    to_delete.append(source_dataset)

    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    job_config.skip_leading_rows = 1
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    source_table_id = "us_states"
    load_job = client.load_table_from_uri(
        uri, source_dataset.table(source_table_id), job_config=job_config
    )
    load_job.result()

    shared_dataset_id = "shared_dataset_{}".format(_millis())
    shared_dataset_ref = client.dataset(shared_dataset_id)
    shared_dataset = bigquery.Dataset(shared_dataset_ref)
    shared_dataset = client.create_dataset(shared_dataset)
    to_delete.append(shared_dataset)

    # [START bigquery_create_view]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # project = 'my-project'
    # source_dataset_id = 'my_source_dataset'
    # source_table_id = 'us_states'
    # shared_dataset_ref = client.dataset('my_shared_dataset')

    # This example shows how to create a shared view of a source table of
    # US States. The source table contains all 50 states, while the view will
    # contain only states with names starting with 'W'.
    view_ref = shared_dataset_ref.table("my_shared_view")
    view = bigquery.Table(view_ref)
    sql_template = 'SELECT name, post_abbr FROM `{}.{}.{}` WHERE name LIKE "W%"'
    view.view_query = sql_template.format(project, source_dataset_id, source_table_id)
    view = client.create_table(view)  # API request

    print("Successfully created view at {}".format(view.full_table_id))
    # [END bigquery_create_view]

    # [START bigquery_update_view_query]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # project = 'my-project'
    # source_dataset_id = 'my_source_dataset'
    # source_table_id = 'us_states'
    # shared_dataset_ref = client.dataset('my_shared_dataset')

    # This example shows how to update a shared view of a source table of
    # US States. The view's query will be updated to contain only states with
    # names starting with 'M'.
    view_ref = shared_dataset_ref.table("my_shared_view")
    view = bigquery.Table(view_ref)
    sql_template = 'SELECT name, post_abbr FROM `{}.{}.{}` WHERE name LIKE "M%"'
    view.view_query = sql_template.format(project, source_dataset_id, source_table_id)
    view = client.update_table(view, ["view_query"])  # API request
    # [END bigquery_update_view_query]

    # [START bigquery_get_view]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # shared_dataset_id = 'my_shared_dataset'

    view_ref = client.dataset(shared_dataset_id).table("my_shared_view")
    view = client.get_table(view_ref)  # API Request

    # Display view properties
    print("View at {}".format(view.full_table_id))
    print("View Query:\n{}".format(view.view_query))
    # [END bigquery_get_view]
    assert view.view_query is not None

    analyst_group_email = "example-analyst-group@google.com"
    # [START bigquery_grant_view_access]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    # Assign access controls to the dataset containing the view
    # shared_dataset_id = 'my_shared_dataset'
    # analyst_group_email = 'data_analysts@example.com'
    shared_dataset = client.get_dataset(
        client.dataset(shared_dataset_id)
    )  # API request
    access_entries = shared_dataset.access_entries
    access_entries.append(
        bigquery.AccessEntry("READER", "groupByEmail", analyst_group_email)
    )
    shared_dataset.access_entries = access_entries
    shared_dataset = client.update_dataset(
        shared_dataset, ["access_entries"]
    )  # API request

    # Authorize the view to access the source dataset
    # project = 'my-project'
    # source_dataset_id = 'my_source_dataset'
    source_dataset = client.get_dataset(
        client.dataset(source_dataset_id)
    )  # API request
    view_reference = {
        "projectId": project,
        "datasetId": shared_dataset_id,
        "tableId": "my_shared_view",
    }
    access_entries = source_dataset.access_entries
    access_entries.append(bigquery.AccessEntry(None, "view", view_reference))
    source_dataset.access_entries = access_entries
    source_dataset = client.update_dataset(
        source_dataset, ["access_entries"]
    )  # API request
    # [END bigquery_grant_view_access]


def test_table_insert_rows(client, to_delete):
    """Insert / fetch table data."""
    dataset_id = "table_insert_rows_dataset_{}".format(_millis())
    table_id = "table_insert_rows_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    dataset.location = "US"
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)

    # [START bigquery_table_insert_rows]
    # TODO(developer): Uncomment the lines below and replace with your values.
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'  # replace with your dataset ID
    # For this sample, the table must already exist and have a defined schema
    # table_id = 'my_table'  # replace with your table ID
    # table_ref = client.dataset(dataset_id).table(table_id)
    # table = client.get_table(table_ref)  # API request

    rows_to_insert = [(u"Phred Phlyntstone", 32), (u"Wylma Phlyntstone", 29)]

    errors = client.insert_rows(table, rows_to_insert)  # API request

    assert errors == []
    # [END bigquery_table_insert_rows]


def test_load_table_from_file(client, to_delete):
    """Upload table data from a CSV file."""
    dataset_id = "load_table_from_file_dataset_{}".format(_millis())
    table_id = "load_table_from_file_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = "US"
    client.create_dataset(dataset)
    to_delete.append(dataset)
    snippets_dir = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        snippets_dir, "..", "..", "bigquery", "tests", "data", "people.csv"
    )

    # [START bigquery_load_from_file]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # filename = '/path/to/file.csv'
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True

    with open(filename, "rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location="US",  # Must match the destination dataset location.
            job_config=job_config,
        )  # API request

    job.result()  # Waits for table load to complete.

    print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))
    # [END bigquery_load_from_file]

    table = client.get_table(table_ref)
    rows = list(client.list_rows(table))  # API request

    assert len(rows) == 2
    # Order is not preserved, so compare individually
    row1 = bigquery.Row(("Wylma Phlyntstone", 29), {"full_name": 0, "age": 1})
    assert row1 in rows
    row2 = bigquery.Row(("Phred Phlyntstone", 32), {"full_name": 0, "age": 1})
    assert row2 in rows


def test_load_table_from_uri_avro(client, to_delete, capsys):
    dataset_id = "load_table_from_uri_avro_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_gcs_avro]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.AVRO
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.avro"

    load_job = client.load_table_from_uri(
        uri, dataset_ref.table("us_states"), job_config=job_config
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(dataset_ref.table("us_states"))
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_avro]

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out


def test_load_table_from_uri_csv(client, to_delete, capsys):
    dataset_id = "load_table_from_uri_csv_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_gcs_csv]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    job_config.skip_leading_rows = 1
    # The source format defaults to CSV, so the line below is optional.
    job_config.source_format = bigquery.SourceFormat.CSV
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"

    load_job = client.load_table_from_uri(
        uri, dataset_ref.table("us_states"), job_config=job_config
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(dataset_ref.table("us_states"))
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_csv]

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out


def test_load_table_from_uri_json(client, to_delete, capsys):
    dataset_id = "load_table_from_uri_json_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = "US"
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_gcs_json]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"

    load_job = client.load_table_from_uri(
        uri,
        dataset_ref.table("us_states"),
        location="US",  # Location must match that of the destination dataset.
        job_config=job_config,
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(dataset_ref.table("us_states"))
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_json]

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out


def test_load_table_from_uri_cmek(client, to_delete):
    dataset_id = "load_table_from_uri_cmek_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = "US"
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_gcs_json_cmek]
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


def test_load_table_from_uri_parquet(client, to_delete, capsys):
    dataset_id = "load_table_from_uri_parquet_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_gcs_parquet]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.PARQUET
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.parquet"

    load_job = client.load_table_from_uri(
        uri, dataset_ref.table("us_states"), job_config=job_config
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(dataset_ref.table("us_states"))
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_parquet]

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out


def test_load_table_from_uri_orc(client, to_delete, capsys):
    dataset_id = "load_table_from_uri_orc_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_gcs_orc]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.ORC
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.orc"

    load_job = client.load_table_from_uri(
        uri, dataset_ref.table("us_states"), job_config=job_config
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(dataset_ref.table("us_states"))
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_orc]

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out


def test_load_table_from_uri_autodetect(client, to_delete, capsys):
    """Load table from a GCS URI using various formats and auto-detected schema

    Each file format has its own tested load from URI sample. Because most of
    the code is common for autodetect, append, and truncate, this sample
    includes snippets for all supported formats but only calls a single load
    job.

    This code snippet is made up of shared code, then format-specific code,
    followed by more shared code. Note that only the last format in the
    format-specific code section will be tested in this test.
    """
    dataset_id = "load_table_from_uri_auto_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # Shared code
    # [START bigquery_load_table_gcs_csv_autodetect]
    # [START bigquery_load_table_gcs_json_autodetect]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    # [END bigquery_load_table_gcs_csv_autodetect]
    # [END bigquery_load_table_gcs_json_autodetect]

    # Format-specific code
    # [START bigquery_load_table_gcs_csv_autodetect]
    job_config.skip_leading_rows = 1
    # The source format defaults to CSV, so the line below is optional.
    job_config.source_format = bigquery.SourceFormat.CSV
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    # [END bigquery_load_table_gcs_csv_autodetect]
    # unset csv-specific attribute
    del job_config._properties["load"]["skipLeadingRows"]

    # [START bigquery_load_table_gcs_json_autodetect]
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"
    # [END bigquery_load_table_gcs_json_autodetect]

    # Shared code
    # [START bigquery_load_table_gcs_csv_autodetect]
    # [START bigquery_load_table_gcs_json_autodetect]
    load_job = client.load_table_from_uri(
        uri, dataset_ref.table("us_states"), job_config=job_config
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(dataset_ref.table("us_states"))
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_csv_autodetect]
    # [END bigquery_load_table_gcs_json_autodetect]

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out


def test_load_table_from_uri_truncate(client, to_delete, capsys):
    """Replaces table data with data from a GCS URI using various formats

    Each file format has its own tested load from URI sample. Because most of
    the code is common for autodetect, append, and truncate, this sample
    includes snippets for all supported formats but only calls a single load
    job.

    This code snippet is made up of shared code, then format-specific code,
    followed by more shared code. Note that only the last format in the
    format-specific code section will be tested in this test.
    """
    dataset_id = "load_table_from_uri_trunc_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    table_ref = dataset.table("us_states")
    body = six.BytesIO(b"Washington,WA")
    client.load_table_from_file(body, table_ref, job_config=job_config).result()
    previous_rows = client.get_table(table_ref).num_rows
    assert previous_rows > 0

    # Shared code
    # [START bigquery_load_table_gcs_avro_truncate]
    # [START bigquery_load_table_gcs_csv_truncate]
    # [START bigquery_load_table_gcs_json_truncate]
    # [START bigquery_load_table_gcs_parquet_truncate]
    # [START bigquery_load_table_gcs_orc_truncate]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('existing_table')

    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    # [END bigquery_load_table_gcs_avro_truncate]
    # [END bigquery_load_table_gcs_csv_truncate]
    # [END bigquery_load_table_gcs_json_truncate]
    # [END bigquery_load_table_gcs_parquet_truncate]
    # [END bigquery_load_table_gcs_orc_truncate]

    # Format-specific code
    # [START bigquery_load_table_gcs_avro_truncate]
    job_config.source_format = bigquery.SourceFormat.AVRO
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.avro"
    # [END bigquery_load_table_gcs_avro_truncate]

    # [START bigquery_load_table_gcs_csv_truncate]
    job_config.skip_leading_rows = 1
    # The source format defaults to CSV, so the line below is optional.
    job_config.source_format = bigquery.SourceFormat.CSV
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    # [END bigquery_load_table_gcs_csv_truncate]
    # unset csv-specific attribute
    del job_config._properties["load"]["skipLeadingRows"]

    # [START bigquery_load_table_gcs_json_truncate]
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"
    # [END bigquery_load_table_gcs_json_truncate]

    # [START bigquery_load_table_gcs_parquet_truncate]
    job_config.source_format = bigquery.SourceFormat.PARQUET
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.parquet"
    # [END bigquery_load_table_gcs_parquet_truncate]

    # [START bigquery_load_table_gcs_orc_truncate]
    job_config.source_format = bigquery.SourceFormat.ORC
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.orc"
    # [END bigquery_load_table_gcs_orc_truncate]

    # Shared code
    # [START bigquery_load_table_gcs_avro_truncate]
    # [START bigquery_load_table_gcs_csv_truncate]
    # [START bigquery_load_table_gcs_json_truncate]
    # [START bigquery_load_table_gcs_parquet_truncate]
    # [START bigquery_load_table_gcs_orc_truncate]
    load_job = client.load_table_from_uri(
        uri, table_ref, job_config=job_config
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(table_ref)
    print("Loaded {} rows.".format(destination_table.num_rows))
    # [END bigquery_load_table_gcs_avro_truncate]
    # [END bigquery_load_table_gcs_csv_truncate]
    # [END bigquery_load_table_gcs_json_truncate]
    # [END bigquery_load_table_gcs_parquet_truncate]
    # [END bigquery_load_table_gcs_orc_truncate]

    out, _ = capsys.readouterr()
    assert "Loaded 50 rows." in out


def test_load_table_add_column(client, to_delete):
    dataset_id = "load_table_add_column_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    snippets_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(
        snippets_dir, "..", "..", "bigquery", "tests", "data", "people.csv"
    )
    table_ref = dataset_ref.table("my_table")
    old_schema = [bigquery.SchemaField("full_name", "STRING", mode="REQUIRED")]
    table = client.create_table(bigquery.Table(table_ref, schema=old_schema))

    # [START bigquery_add_column_load_append]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # filepath = 'path/to/your_file.csv'

    # Retrieves the destination table and checks the length of the schema
    table_id = "my_table"
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    print("Table {} contains {} columns.".format(table_id, len(table.schema)))

    # Configures the load job to append the data to the destination table,
    # allowing field addition
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.schema_update_options = [
        bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
    ]
    # In this example, the existing table contains only the 'full_name' column.
    # 'REQUIRED' fields cannot be added to an existing schema, so the
    # additional column must be 'NULLABLE'.
    job_config.schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
    ]
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1

    with open(filepath, "rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location="US",  # Must match the destination dataset location.
            job_config=job_config,
        )  # API request

    job.result()  # Waits for table load to complete.
    print(
        "Loaded {} rows into {}:{}.".format(
            job.output_rows, dataset_id, table_ref.table_id
        )
    )

    # Checks the updated length of the schema
    table = client.get_table(table)
    print("Table {} now contains {} columns.".format(table_id, len(table.schema)))
    # [END bigquery_add_column_load_append]
    assert len(table.schema) == 2
    assert table.num_rows > 0


def test_load_table_relax_column(client, to_delete):
    dataset_id = "load_table_relax_column_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    snippets_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(
        snippets_dir, "..", "..", "bigquery", "tests", "data", "people.csv"
    )
    table_ref = dataset_ref.table("my_table")
    old_schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("favorite_color", "STRING", mode="REQUIRED"),
    ]
    table = client.create_table(bigquery.Table(table_ref, schema=old_schema))

    # [START bigquery_relax_column_load_append]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # filepath = 'path/to/your_file.csv'

    # Retrieves the destination table and checks the number of required fields
    table_id = "my_table"
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    original_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
    # In this example, the existing table has 3 required fields.
    print("{} fields in the schema are required.".format(original_required_fields))

    # Configures the load job to append the data to a destination table,
    # allowing field relaxation
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.schema_update_options = [
        bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
    ]
    # In this example, the existing table contains three required fields
    # ('full_name', 'age', and 'favorite_color'), while the data to load
    # contains only the first two fields.
    job_config.schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1

    with open(filepath, "rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location="US",  # Must match the destination dataset location.
            job_config=job_config,
        )  # API request

    job.result()  # Waits for table load to complete.
    print(
        "Loaded {} rows into {}:{}.".format(
            job.output_rows, dataset_id, table_ref.table_id
        )
    )

    # Checks the updated number of required fields
    table = client.get_table(table)
    current_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
    print("{} fields in the schema are now required.".format(current_required_fields))
    # [END bigquery_relax_column_load_append]
    assert original_required_fields - current_required_fields == 1
    assert len(table.schema) == 3
    assert table.schema[2].mode == "NULLABLE"
    assert table.num_rows > 0


def test_copy_table(client, to_delete):
    dataset_id = "copy_table_dataset_{}".format(_millis())
    dest_dataset = bigquery.Dataset(client.dataset(dataset_id))
    dest_dataset.location = "US"
    dest_dataset = client.create_dataset(dest_dataset)
    to_delete.append(dest_dataset)

    # [START bigquery_copy_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    source_dataset = client.dataset("samples", project="bigquery-public-data")
    source_table_ref = source_dataset.table("shakespeare")

    # dataset_id = 'my_dataset'
    dest_table_ref = client.dataset(dataset_id).table("destination_table")

    job = client.copy_table(
        source_table_ref,
        dest_table_ref,
        # Location must match that of the source and destination tables.
        location="US",
    )  # API request

    job.result()  # Waits for job to complete.

    assert job.state == "DONE"
    dest_table = client.get_table(dest_table_ref)  # API request
    assert dest_table.num_rows > 0
    # [END bigquery_copy_table]


def test_copy_table_multiple_source(client, to_delete):
    dest_dataset_id = "dest_dataset_{}".format(_millis())
    dest_dataset = bigquery.Dataset(client.dataset(dest_dataset_id))
    dest_dataset.location = "US"
    dest_dataset = client.create_dataset(dest_dataset)
    to_delete.append(dest_dataset)

    source_dataset_id = "source_dataset_{}".format(_millis())
    source_dataset = bigquery.Dataset(client.dataset(source_dataset_id))
    source_dataset.location = "US"
    source_dataset = client.create_dataset(source_dataset)
    to_delete.append(source_dataset)

    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]

    table_data = {"table1": b"Washington,WA", "table2": b"California,CA"}
    for table_id, data in table_data.items():
        table_ref = source_dataset.table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.schema = schema
        body = six.BytesIO(data)
        client.load_table_from_file(
            body,
            table_ref,
            # Location must match that of the destination dataset.
            location="US",
            job_config=job_config,
        ).result()

    # [START bigquery_copy_table_multiple_source]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # source_dataset_id = 'my_source_dataset'
    # dest_dataset_id = 'my_destination_dataset'

    table1_ref = client.dataset(source_dataset_id).table("table1")
    table2_ref = client.dataset(source_dataset_id).table("table2")
    dest_table_ref = client.dataset(dest_dataset_id).table("destination_table")

    job = client.copy_table(
        [table1_ref, table2_ref],
        dest_table_ref,
        # Location must match that of the source and destination tables.
        location="US",
    )  # API request
    job.result()  # Waits for job to complete.

    assert job.state == "DONE"
    dest_table = client.get_table(dest_table_ref)  # API request
    assert dest_table.num_rows > 0
    # [END bigquery_copy_table_multiple_source]

    assert dest_table.num_rows == 2


def test_copy_table_cmek(client, to_delete):
    dataset_id = "copy_table_cmek_{}".format(_millis())
    dest_dataset = bigquery.Dataset(client.dataset(dataset_id))
    dest_dataset.location = "US"
    dest_dataset = client.create_dataset(dest_dataset)
    to_delete.append(dest_dataset)

    # [START bigquery_copy_table_cmek]
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


def test_extract_table(client, to_delete):
    bucket_name = "extract_shakespeare_{}".format(_millis())
    storage_client = storage.Client()
    bucket = retry_storage_errors(storage_client.create_bucket)(bucket_name)
    to_delete.append(bucket)

    # [START bigquery_extract_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # bucket_name = 'my-bucket'
    project = "bigquery-public-data"
    dataset_id = "samples"
    table_id = "shakespeare"

    destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.csv")
    dataset_ref = client.dataset(dataset_id, project=project)
    table_ref = dataset_ref.table(table_id)

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        # Location must match that of the source table.
        location="US",
    )  # API request
    extract_job.result()  # Waits for job to complete.

    print(
        "Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri)
    )
    # [END bigquery_extract_table]

    blob = retry_storage_errors(bucket.get_blob)("shakespeare.csv")
    assert blob.exists
    assert blob.size > 0
    to_delete.insert(0, blob)


def test_extract_table_json(client, to_delete):
    bucket_name = "extract_shakespeare_json_{}".format(_millis())
    storage_client = storage.Client()
    bucket = retry_storage_errors(storage_client.create_bucket)(bucket_name)
    to_delete.append(bucket)

    # [START bigquery_extract_table_json]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # bucket_name = 'my-bucket'

    destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.json")
    dataset_ref = client.dataset("samples", project="bigquery-public-data")
    table_ref = dataset_ref.table("shakespeare")
    job_config = bigquery.job.ExtractJobConfig()
    job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        job_config=job_config,
        # Location must match that of the source table.
        location="US",
    )  # API request
    extract_job.result()  # Waits for job to complete.
    # [END bigquery_extract_table_json]

    blob = retry_storage_errors(bucket.get_blob)("shakespeare.json")
    assert blob.exists
    assert blob.size > 0
    to_delete.insert(0, blob)


def test_extract_table_compressed(client, to_delete):
    bucket_name = "extract_shakespeare_compress_{}".format(_millis())
    storage_client = storage.Client()
    bucket = retry_storage_errors(storage_client.create_bucket)(bucket_name)
    to_delete.append(bucket)

    # [START bigquery_extract_table_compressed]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # bucket_name = 'my-bucket'

    destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.csv.gz")
    dataset_ref = client.dataset("samples", project="bigquery-public-data")
    table_ref = dataset_ref.table("shakespeare")
    job_config = bigquery.job.ExtractJobConfig()
    job_config.compression = bigquery.Compression.GZIP

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        # Location must match that of the source table.
        location="US",
        job_config=job_config,
    )  # API request
    extract_job.result()  # Waits for job to complete.
    # [END bigquery_extract_table_compressed]

    blob = retry_storage_errors(bucket.get_blob)("shakespeare.csv.gz")
    assert blob.exists
    assert blob.size > 0
    to_delete.insert(0, blob)


def test_delete_table(client, to_delete):
    """Delete a table."""
    from google.cloud.exceptions import NotFound

    dataset_id = "delete_table_dataset_{}".format(_millis())
    table_id = "delete_table_table_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table_ref = dataset.table(table_id)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    client.create_table(table)
    # [START bigquery_delete_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    table_ref = client.dataset(dataset_id).table(table_id)
    client.delete_table(table_ref)  # API request

    print("Table {}:{} deleted.".format(dataset_id, table_id))
    # [END bigquery_delete_table]

    with pytest.raises(NotFound):
        client.get_table(table)  # API request


def test_undelete_table(client, to_delete):
    dataset_id = "undelete_table_dataset_{}".format(_millis())
    table_id = "undelete_table_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    client.create_table(table)

    # [START bigquery_undelete_table]
    # TODO(developer): Uncomment the lines below and replace with your values.
    # import time
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'  # Replace with your dataset ID.
    # table_id = 'my_table'      # Replace with your table ID.

    table_ref = client.dataset(dataset_id).table(table_id)

    # TODO(developer): Choose an appropriate snapshot point as epoch
    # milliseconds. For this example, we choose the current time as we're about
    # to delete the table immediately afterwards.
    snapshot_epoch = int(time.time() * 1000)
    # [END bigquery_undelete_table]

    # Due to very short lifecycle of the table, ensure we're not picking a time
    # prior to the table creation due to time drift between backend and client.
    table = client.get_table(table_ref)
    created_epoch = datetime_helpers.to_microseconds(table.created)
    if created_epoch > snapshot_epoch:
        snapshot_epoch = created_epoch

    # [START bigquery_undelete_table]

    # "Accidentally" delete the table.
    client.delete_table(table_ref)  # API request

    # Construct the restore-from table ID using a snapshot decorator.
    snapshot_table_id = "{}@{}".format(table_id, snapshot_epoch)
    source_table_ref = client.dataset(dataset_id).table(snapshot_table_id)

    # Choose a new table ID for the recovered table data.
    recovered_table_id = "{}_recovered".format(table_id)
    dest_table_ref = client.dataset(dataset_id).table(recovered_table_id)

    # Construct and run a copy job.
    job = client.copy_table(
        source_table_ref,
        dest_table_ref,
        # Location must match that of the source and destination tables.
        location="US",
    )  # API request

    job.result()  # Waits for job to complete.

    print(
        "Copied data from deleted table {} to {}".format(table_id, recovered_table_id)
    )
    # [END bigquery_undelete_table]


def test_client_query(client):
    """Run a simple query."""

    # [START bigquery_query]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = (
        "SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` "
        'WHERE state = "TX" '
        "LIMIT 100"
    )
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
    )  # API request - starts the query

    for row in query_job:  # API request - fetches results
        # Row values can be accessed by field name or index
        assert row[0] == row.name == row["name"]
        print(row)
    # [END bigquery_query]


def test_client_query_legacy_sql(client):
    """Run a query with Legacy SQL explicitly set"""
    # [START bigquery_query_legacy]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = (
        "SELECT name FROM [bigquery-public-data:usa_names.usa_1910_2013] "
        'WHERE state = "TX" '
        "LIMIT 100"
    )

    # Set use_legacy_sql to True to use legacy SQL syntax.
    job_config = bigquery.QueryJobConfig()
    job_config.use_legacy_sql = True

    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    # Print the results.
    for row in query_job:  # API request - fetches results
        print(row)
    # [END bigquery_query_legacy]


def test_client_query_total_rows(client, capsys):
    """Run a query and just check for how many rows."""
    # [START bigquery_query_total_rows]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = (
        "SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` "
        'WHERE state = "TX" '
        "LIMIT 100"
    )
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
    )  # API request - starts the query

    results = query_job.result()  # Waits for query to complete.
    next(iter(results))  # Fetch the first page of results, which contains total_rows.
    print("Got {} rows.".format(results.total_rows))
    # [END bigquery_query_total_rows]

    out, _ = capsys.readouterr()
    assert "Got 100 rows." in out


def test_manage_job(client):
    sql = """
        SELECT corpus
        FROM `bigquery-public-data.samples.shakespeare`
        GROUP BY corpus;
    """
    location = "us"
    job = client.query(sql, location=location)
    job_id = job.job_id

    # [START bigquery_cancel_job]
    # TODO(developer): Uncomment the lines below and replace with your values.
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # job_id = 'bq-job-123x456-123y123z123c'  # replace with your job ID
    # location = 'us'                         # replace with your location

    job = client.cancel_job(job_id, location=location)
    # [END bigquery_cancel_job]

    # [START bigquery_get_job]
    # TODO(developer): Uncomment the lines below and replace with your values.
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # job_id = 'bq-job-123x456-123y123z123c'  # replace with your job ID
    # location = 'us'                         # replace with your location

    job = client.get_job(job_id, location=location)  # API request

    # Print selected job properties
    print("Details for job {} running in {}:".format(job_id, location))
    print(
        "\tType: {}\n\tState: {}\n\tCreated: {}".format(
            job.job_type, job.state, job.created
        )
    )
    # [END bigquery_get_job]


def test_client_query_destination_table(client, to_delete):
    """Run a query"""
    dataset_id = "query_destination_table_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    to_delete.append(dataset_ref)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    client.create_dataset(dataset)

    # [START bigquery_query_destination_table]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'your_dataset_id'

    job_config = bigquery.QueryJobConfig()
    # Set the destination table
    table_ref = client.dataset(dataset_id).table("your_table_id")
    job_config.destination = table_ref
    sql = """
        SELECT corpus
        FROM `bigquery-public-data.samples.shakespeare`
        GROUP BY corpus;
    """

    # Start the query, passing in the extra configuration.
    query_job = client.query(
        sql,
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    query_job.result()  # Waits for the query to finish
    print("Query results loaded to table {}".format(table_ref.path))
    # [END bigquery_query_destination_table]


def test_client_query_destination_table_legacy(client, to_delete):
    dataset_id = "query_destination_table_legacy_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    to_delete.append(dataset_ref)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    client.create_dataset(dataset)

    # [START bigquery_query_legacy_large_results]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'your_dataset_id'

    job_config = bigquery.QueryJobConfig()
    # Set use_legacy_sql to True to use legacy SQL syntax.
    job_config.use_legacy_sql = True
    # Set the destination table
    table_ref = client.dataset(dataset_id).table("your_table_id")
    job_config.destination = table_ref
    job_config.allow_large_results = True
    sql = """
        SELECT corpus
        FROM [bigquery-public-data:samples.shakespeare]
        GROUP BY corpus;
    """
    # Start the query, passing in the extra configuration.
    query_job = client.query(
        sql,
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    query_job.result()  # Waits for the query to finish
    print("Query results loaded to table {}".format(table_ref.path))
    # [END bigquery_query_legacy_large_results]


def test_client_query_destination_table_cmek(client, to_delete):
    """Run a query"""
    dataset_id = "query_destination_table_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    to_delete.append(dataset_ref)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    client.create_dataset(dataset)

    # [START bigquery_query_destination_table_cmek]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    job_config = bigquery.QueryJobConfig()

    # Set the destination table. Here, dataset_id is a string, such as:
    # dataset_id = 'your_dataset_id'
    table_ref = client.dataset(dataset_id).table("your_table_id")
    job_config.destination = table_ref

    # Set the encryption key to use for the destination.
    # TODO: Replace this key with a key you have created in KMS.
    kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
        "cloud-samples-tests", "us-central1", "test", "test"
    )
    encryption_config = bigquery.EncryptionConfiguration(kms_key_name=kms_key_name)
    job_config.destination_encryption_configuration = encryption_config

    # Start the query, passing in the extra configuration.
    query_job = client.query(
        "SELECT 17 AS my_col;",
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location="US",
        job_config=job_config,
    )  # API request - starts the query
    query_job.result()

    # The destination table is written using the encryption configuration.
    table = client.get_table(table_ref)
    assert table.encryption_configuration.kms_key_name == kms_key_name
    # [END bigquery_query_destination_table_cmek]


def test_client_query_batch(client, to_delete):
    # [START bigquery_query_batch]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    job_config = bigquery.QueryJobConfig()
    # Run at batch priority, which won't count toward concurrent rate limit.
    job_config.priority = bigquery.QueryPriority.BATCH
    sql = """
        SELECT corpus
        FROM `bigquery-public-data.samples.shakespeare`
        GROUP BY corpus;
    """
    # Location must match that of the dataset(s) referenced in the query.
    location = "US"

    # API request - starts the query
    query_job = client.query(sql, location=location, job_config=job_config)

    # Check on the progress by getting the job's updated state. Once the state
    # is `DONE`, the results are ready.
    query_job = client.get_job(
        query_job.job_id, location=location
    )  # API request - fetches job
    print("Job {} is currently in state {}".format(query_job.job_id, query_job.state))
    # [END bigquery_query_batch]


def test_client_query_relax_column(client, to_delete):
    dataset_id = "query_relax_column_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table_ref = dataset_ref.table("my_table")
    schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]
    table = client.create_table(bigquery.Table(table_ref, schema=schema))

    # [START bigquery_relax_column_query_append]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    # Retrieves the destination table and checks the number of required fields
    table_id = "my_table"
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    original_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
    # In this example, the existing table has 2 required fields
    print("{} fields in the schema are required.".format(original_required_fields))

    # Configures the query to append the results to a destination table,
    # allowing field relaxation
    job_config = bigquery.QueryJobConfig()
    job_config.schema_update_options = [
        bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
    ]
    job_config.destination = table_ref
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    query_job = client.query(
        # In this example, the existing table contains 'full_name' and 'age' as
        # required columns, but the query results will omit the second column.
        'SELECT "Beyonce" as full_name;',
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    query_job.result()  # Waits for the query to finish
    print("Query job {} complete.".format(query_job.job_id))

    # Checks the updated number of required fields
    table = client.get_table(table)
    current_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
    print("{} fields in the schema are now required.".format(current_required_fields))
    # [END bigquery_relax_column_query_append]
    assert original_required_fields - current_required_fields > 0
    assert len(table.schema) == 2
    assert table.schema[1].mode == "NULLABLE"
    assert table.num_rows > 0


def test_client_query_add_column(client, to_delete):
    dataset_id = "query_add_column_{}".format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table_ref = dataset_ref.table("my_table")
    schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]
    table = client.create_table(bigquery.Table(table_ref, schema=schema))

    # [START bigquery_add_column_query_append]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    # Retrieves the destination table and checks the length of the schema
    table_id = "my_table"
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    print("Table {} contains {} columns.".format(table_id, len(table.schema)))

    # Configures the query to append the results to a destination table,
    # allowing field addition
    job_config = bigquery.QueryJobConfig()
    job_config.schema_update_options = [
        bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
    ]
    job_config.destination = table_ref
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    query_job = client.query(
        # In this example, the existing table contains only the 'full_name' and
        # 'age' columns, while the results of this query will contain an
        # additional 'favorite_color' column.
        'SELECT "Timmy" as full_name, 85 as age, "Blue" as favorite_color;',
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    query_job.result()  # Waits for the query to finish
    print("Query job {} complete.".format(query_job.job_id))

    # Checks the updated length of the schema
    table = client.get_table(table)
    print("Table {} now contains {} columns.".format(table_id, len(table.schema)))
    # [END bigquery_add_column_query_append]
    assert len(table.schema) == 3
    assert table.num_rows > 0


def test_client_query_w_named_params(client, capsys):
    """Run a query using named query parameters"""

    # [START bigquery_query_params_named]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = """
        SELECT word, word_count
        FROM `bigquery-public-data.samples.shakespeare`
        WHERE corpus = @corpus
        AND word_count >= @min_word_count
        ORDER BY word_count DESC;
    """
    query_params = [
        bigquery.ScalarQueryParameter("corpus", "STRING", "romeoandjuliet"),
        bigquery.ScalarQueryParameter("min_word_count", "INT64", 250),
    ]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    # Print the results
    for row in query_job:
        print("{}: \t{}".format(row.word, row.word_count))

    assert query_job.state == "DONE"
    # [END bigquery_query_params_named]

    out, _ = capsys.readouterr()
    assert "the" in out


def test_client_query_w_positional_params(client, capsys):
    """Run a query using query parameters"""

    # [START bigquery_query_params_positional]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = """
        SELECT word, word_count
        FROM `bigquery-public-data.samples.shakespeare`
        WHERE corpus = ?
        AND word_count >= ?
        ORDER BY word_count DESC;
    """
    # Set the name to None to use positional parameters.
    # Note that you cannot mix named and positional parameters.
    query_params = [
        bigquery.ScalarQueryParameter(None, "STRING", "romeoandjuliet"),
        bigquery.ScalarQueryParameter(None, "INT64", 250),
    ]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    # Print the results
    for row in query_job:
        print("{}: \t{}".format(row.word, row.word_count))

    assert query_job.state == "DONE"
    # [END bigquery_query_params_positional]

    out, _ = capsys.readouterr()
    assert "the" in out


def test_client_query_w_timestamp_params(client, capsys):
    """Run a query using query parameters"""

    # [START bigquery_query_params_timestamps]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    import datetime
    import pytz

    query = "SELECT TIMESTAMP_ADD(@ts_value, INTERVAL 1 HOUR);"
    query_params = [
        bigquery.ScalarQueryParameter(
            "ts_value",
            "TIMESTAMP",
            datetime.datetime(2016, 12, 7, 8, 0, tzinfo=pytz.UTC),
        )
    ]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    # Print the results
    for row in query_job:
        print(row)

    assert query_job.state == "DONE"
    # [END bigquery_query_params_timestamps]

    out, _ = capsys.readouterr()
    assert "2016, 12, 7, 9, 0" in out


def test_client_query_w_array_params(client, capsys):
    """Run a query using array query parameters"""
    # [START bigquery_query_params_arrays]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = """
        SELECT name, sum(number) as count
        FROM `bigquery-public-data.usa_names.usa_1910_2013`
        WHERE gender = @gender
        AND state IN UNNEST(@states)
        GROUP BY name
        ORDER BY count DESC
        LIMIT 10;
    """
    query_params = [
        bigquery.ScalarQueryParameter("gender", "STRING", "M"),
        bigquery.ArrayQueryParameter("states", "STRING", ["WA", "WI", "WV", "WY"]),
    ]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    # Print the results
    for row in query_job:
        print("{}: \t{}".format(row.name, row.count))

    assert query_job.state == "DONE"
    # [END bigquery_query_params_arrays]

    out, _ = capsys.readouterr()
    assert "James" in out


def test_client_query_w_struct_params(client, capsys):
    """Run a query using struct query parameters"""
    # [START bigquery_query_params_structs]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    query = "SELECT @struct_value AS s;"
    query_params = [
        bigquery.StructQueryParameter(
            "struct_value",
            bigquery.ScalarQueryParameter("x", "INT64", 1),
            bigquery.ScalarQueryParameter("y", "STRING", "foo"),
        )
    ]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    # Print the results
    for row in query_job:
        print(row.s)

    assert query_job.state == "DONE"
    # [END bigquery_query_params_structs]

    out, _ = capsys.readouterr()
    assert "1" in out
    assert "foo" in out


def test_client_query_dry_run(client):
    """Run a dry run query"""

    # [START bigquery_query_dry_run]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    job_config = bigquery.QueryJobConfig()
    job_config.dry_run = True
    job_config.use_query_cache = False
    query_job = client.query(
        (
            "SELECT name, COUNT(*) as name_count "
            "FROM `bigquery-public-data.usa_names.usa_1910_2013` "
            "WHERE state = 'WA' "
            "GROUP BY name"
        ),
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request

    # A dry run query completes immediately.
    assert query_job.state == "DONE"
    assert query_job.dry_run

    print("This query will process {} bytes.".format(query_job.total_bytes_processed))
    # [END bigquery_query_dry_run]

    assert query_job.total_bytes_processed > 0


def test_query_no_cache(client):
    # [START bigquery_query_no_cache]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    job_config = bigquery.QueryJobConfig()
    job_config.use_query_cache = False
    sql = """
        SELECT corpus
        FROM `bigquery-public-data.samples.shakespeare`
        GROUP BY corpus;
    """
    query_job = client.query(
        sql,
        # Location must match that of the dataset(s) referenced in the query.
        location="US",
        job_config=job_config,
    )  # API request

    # Print the results.
    for row in query_job:  # API request - fetches results
        print(row)
    # [END bigquery_query_no_cache]


def test_query_external_gcs_temporary_table(client):
    # [START bigquery_query_external_gcs_temp]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    # Configure the external data source and query job
    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = [
        "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    ]
    external_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    external_config.options.skip_leading_rows = 1  # optionally skip header row
    table_id = "us_states"
    job_config = bigquery.QueryJobConfig()
    job_config.table_definitions = {table_id: external_config}

    # Example query to find states starting with 'W'
    sql = 'SELECT * FROM `{}` WHERE name LIKE "W%"'.format(table_id)

    query_job = client.query(sql, job_config=job_config)  # API request

    w_states = list(query_job)  # Waits for query to finish
    print("There are {} states with names starting with W.".format(len(w_states)))
    # [END bigquery_query_external_gcs_temp]
    assert len(w_states) == 4


def test_query_external_gcs_permanent_table(client, to_delete):
    dataset_id = "query_external_gcs_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_query_external_gcs_perm]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    # Configure the external data source
    dataset_ref = client.dataset(dataset_id)
    table_id = "us_states"
    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    table = bigquery.Table(dataset_ref.table(table_id), schema=schema)
    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = [
        "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    ]
    external_config.options.skip_leading_rows = 1  # optionally skip header row
    table.external_data_configuration = external_config

    # Create a permanent table linked to the GCS file
    table = client.create_table(table)  # API request

    # Example query to find states starting with 'W'
    sql = 'SELECT * FROM `{}.{}` WHERE name LIKE "W%"'.format(dataset_id, table_id)

    query_job = client.query(sql)  # API request

    w_states = list(query_job)  # Waits for query to finish
    print("There are {} states with names starting with W.".format(len(w_states)))
    # [END bigquery_query_external_gcs_perm]
    assert len(w_states) == 4


def test_query_external_sheets_temporary_table(client):
    # [START bigquery_query_external_sheets_temp]
    # [START bigquery_auth_drive_scope]
    import google.auth

    # from google.cloud import bigquery

    # Create credentials with Drive & BigQuery API scopes
    # Both APIs must be enabled for your project before running this code
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery",
        ]
    )
    client = bigquery.Client(credentials=credentials, project=project)
    # [END bigquery_auth_drive_scope]

    # Configure the external data source and query job
    external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")
    # Use a shareable link or grant viewing access to the email address you
    # used to authenticate with BigQuery (this example Sheet is public)
    sheet_url = (
        "https://docs.google.com/spreadsheets"
        "/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing"
    )
    external_config.source_uris = [sheet_url]
    external_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    external_config.options.skip_leading_rows = 1  # optionally skip header row
    table_id = "us_states"
    job_config = bigquery.QueryJobConfig()
    job_config.table_definitions = {table_id: external_config}

    # Example query to find states starting with 'W'
    sql = 'SELECT * FROM `{}` WHERE name LIKE "W%"'.format(table_id)

    query_job = client.query(sql, job_config=job_config)  # API request

    w_states = list(query_job)  # Waits for query to finish
    print("There are {} states with names starting with W.".format(len(w_states)))
    # [END bigquery_query_external_sheets_temp]
    assert len(w_states) == 4


def test_query_external_sheets_permanent_table(client, to_delete):
    dataset_id = "query_external_sheets_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_query_external_sheets_perm]
    import google.auth

    # from google.cloud import bigquery
    # dataset_id = 'my_dataset'

    # Create credentials with Drive & BigQuery API scopes
    # Both APIs must be enabled for your project before running this code
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery",
        ]
    )
    client = bigquery.Client(credentials=credentials, project=project)

    # Configure the external data source
    dataset_ref = client.dataset(dataset_id)
    table_id = "us_states"
    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    table = bigquery.Table(dataset_ref.table(table_id), schema=schema)
    external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")
    # Use a shareable link or grant viewing access to the email address you
    # used to authenticate with BigQuery (this example Sheet is public)
    sheet_url = (
        "https://docs.google.com/spreadsheets"
        "/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing"
    )
    external_config.source_uris = [sheet_url]
    external_config.options.skip_leading_rows = 1  # optionally skip header row
    table.external_data_configuration = external_config

    # Create a permanent table linked to the Sheets file
    table = client.create_table(table)  # API request

    # Example query to find states starting with 'W'
    sql = 'SELECT * FROM `{}.{}` WHERE name LIKE "W%"'.format(dataset_id, table_id)

    query_job = client.query(sql)  # API request

    w_states = list(query_job)  # Waits for query to finish
    print("There are {} states with names starting with W.".format(len(w_states)))
    # [END bigquery_query_external_sheets_perm]
    assert len(w_states) == 4


def test_ddl_create_view(client, to_delete, capsys):
    """Create a view via a DDL query."""
    project = client.project
    dataset_id = "ddl_view_{}".format(_millis())
    table_id = "new_view"
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_ddl_create_view]
    # from google.cloud import bigquery
    # project = 'my-project'
    # dataset_id = 'my_dataset'
    # table_id = 'new_view'
    # client = bigquery.Client(project=project)

    sql = """
    CREATE VIEW `{}.{}.{}`
    OPTIONS(
        expiration_timestamp=TIMESTAMP_ADD(
            CURRENT_TIMESTAMP(), INTERVAL 48 HOUR),
        friendly_name="new_view",
        description="a view that expires in 2 days",
        labels=[("org_unit", "development")]
    )
    AS SELECT name, state, year, number
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE state LIKE 'W%'
    """.format(
        project, dataset_id, table_id
    )

    job = client.query(sql)  # API request.
    job.result()  # Waits for the query to finish.

    print(
        'Created new view "{}.{}.{}".'.format(
            job.destination.project,
            job.destination.dataset_id,
            job.destination.table_id,
        )
    )
    # [END bigquery_ddl_create_view]

    out, _ = capsys.readouterr()
    assert 'Created new view "{}.{}.{}".'.format(project, dataset_id, table_id) in out

    # Test that listing query result rows succeeds so that generic query
    # processing tools work with DDL statements.
    rows = list(job)
    assert len(rows) == 0

    if pandas is not None:
        df = job.to_dataframe()
        assert len(df) == 0


def test_client_list_jobs(client):
    """List jobs for a project."""

    # [START bigquery_list_jobs]
    # TODO(developer): Uncomment the lines below and replace with your values.
    # from google.cloud import bigquery
    # project = 'my_project'  # replace with your project ID
    # client = bigquery.Client(project=project)
    import datetime

    # List the 10 most recent jobs in reverse chronological order.
    # Omit the max_results parameter to list jobs from the past 6 months.
    print("Last 10 jobs:")
    for job in client.list_jobs(max_results=10):  # API request(s)
        print(job.job_id)

    # The following are examples of additional optional parameters:

    # Use min_creation_time and/or max_creation_time to specify a time window.
    print("Jobs from the last ten minutes:")
    ten_mins_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    for job in client.list_jobs(min_creation_time=ten_mins_ago):
        print(job.job_id)

    # Use all_users to include jobs run by all users in the project.
    print("Last 10 jobs run by all users:")
    for job in client.list_jobs(max_results=10, all_users=True):
        print("{} run by user: {}".format(job.job_id, job.user_email))

    # Use state_filter to filter by job state.
    print("Jobs currently running:")
    for job in client.list_jobs(state_filter="RUNNING"):
        print(job.job_id)
    # [END bigquery_list_jobs]


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_query_results_as_dataframe(client):
    # [START bigquery_query_results_dataframe]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    sql = """
        SELECT name, SUM(number) as count
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        GROUP BY name
        ORDER BY count DESC
        LIMIT 10
    """

    df = client.query(sql).to_dataframe()
    # [END bigquery_query_results_dataframe]
    assert isinstance(df, pandas.DataFrame)
    assert len(list(df)) == 2  # verify the number of columns
    assert len(df) == 10  # verify the number of rows


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_list_rows_as_dataframe(client):
    # [START bigquery_list_rows_dataframe]
    # from google.cloud import bigquery
    # client = bigquery.Client()

    dataset_ref = client.dataset("samples", project="bigquery-public-data")
    table_ref = dataset_ref.table("shakespeare")
    table = client.get_table(table_ref)

    df = client.list_rows(table).to_dataframe()
    # [END bigquery_list_rows_dataframe]
    assert isinstance(df, pandas.DataFrame)
    assert len(list(df)) == len(table.schema)  # verify the number of columns
    assert len(df) == table.num_rows  # verify the number of rows


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.parametrize("parquet_engine", ["pyarrow", "fastparquet"])
def test_load_table_from_dataframe(client, to_delete, parquet_engine):
    if parquet_engine == "pyarrow" and pyarrow is None:
        pytest.skip("Requires `pyarrow`")
    if parquet_engine == "fastparquet" and fastparquet is None:
        pytest.skip("Requires `fastparquet`")

    pandas.set_option("io.parquet.engine", parquet_engine)

    dataset_id = "load_table_from_dataframe_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_dataframe]
    # from google.cloud import bigquery
    # import pandas
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table("monty_python")
    records = [
        {"title": "The Meaning of Life", "release_year": 1983},
        {"title": "Monty Python and the Holy Grail", "release_year": 1975},
        {"title": "Life of Brian", "release_year": 1979},
        {"title": "And Now for Something Completely Different", "release_year": 1971},
    ]
    # Optionally set explicit indices.
    # If indices are not specified, a column will be created for the default
    # indices created by pandas.
    index = ["Q24980", "Q25043", "Q24953", "Q16403"]
    dataframe = pandas.DataFrame(records, index=pandas.Index(index, name="wikidata_id"))

    job = client.load_table_from_dataframe(dataframe, table_ref, location="US")

    job.result()  # Waits for table load to complete.

    assert job.state == "DONE"
    table = client.get_table(table_ref)
    assert table.num_rows == 4
    # [END bigquery_load_table_dataframe]
    column_names = [field.name for field in table.schema]
    assert sorted(column_names) == ["release_year", "title", "wikidata_id"]


if __name__ == "__main__":
    pytest.main()
