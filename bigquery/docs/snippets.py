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

import pytest

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
        "cloud-samples-tests", "us", "test", "test"
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
        "cloud-samples-tests", "us", "test", "test"
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
        "projects/cloud-samples-tests/locations/us/keyRings/test/cryptoKeys/otherkey"
    )
    table.encryption_configuration = bigquery.EncryptionConfiguration(
        kms_key_name=updated_kms_key_name
    )

    table = client.update_table(table, ["encryption_configuration"])  # API request

    assert table.encryption_configuration.kms_key_name == updated_kms_key_name
    assert original_kms_key_name != updated_kms_key_name
    # [END bigquery_update_table_cmek]


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

    results = query_job.result()  # Wait for query to complete.
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


if __name__ == "__main__":
    pytest.main()
