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

import time

import pytest
import six
try:
    import pandas
except ImportError:
    pandas = None

from google.cloud import bigquery

ORIGINAL_FRIENDLY_NAME = 'Original friendly name'
ORIGINAL_DESCRIPTION = 'Original description'
LOCALLY_CHANGED_FRIENDLY_NAME = 'Locally-changed friendly name'
LOCALLY_CHANGED_DESCRIPTION = 'Locally-changed description'
UPDATED_FRIENDLY_NAME = 'Updated friendly name'
UPDATED_DESCRIPTION = 'Updated description'

SCHEMA = [
    bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
]

ROWS = [
    ('Phred Phlyntstone', 32),
    ('Bharney Rhubble', 33),
    ('Wylma Phlyntstone', 29),
    ('Bhettye Rhubble', 27),
]

QUERY = (
    'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
    'WHERE state = "TX"')


@pytest.fixture(scope='module')
def client():
    return bigquery.Client()


@pytest.fixture
def to_delete(client):
    doomed = []
    yield doomed
    for item in doomed:
        if isinstance(item, (bigquery.Dataset, bigquery.DatasetReference)):
            client.delete_dataset(item, delete_contents=True)
        elif isinstance(item, (bigquery.Table, bigquery.TableReference)):
            client.delete_table(item)
        else:
            item.delete()


def _millis():
    return int(time.time() * 1000)


class _CloseOnDelete(object):

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def delete(self):
        self._wrapped.close()


def test_list_datasets(client):
    """List datasets for a project."""
    # [START bigquery_list_datasets]
    # client = bigquery.Client()
    datasets = list(client.list_datasets())
    project = client.project

    if datasets:
        print('Datasets in project {}:'.format(project))
        for dataset in datasets:  # API request(s)
            print('\t{}'.format(dataset.dataset_id))
    else:
        print('{} project does not contain any datasets.'.format(project))
    # [END bigquery_list_datasets]


def test_create_dataset(client, to_delete):
    """Create a dataset."""
    dataset_id = 'create_dataset_{}'.format(_millis())

    # [START bigquery_create_dataset]
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    # Create a DatasetReference using a chosen dataset ID.
    # The project defaults to the Client's project if not specified.
    dataset_ref = client.dataset(dataset_id)

    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_ref)

    # Send the dataset to the API for creation.
    # Raises google.api_core.exceptions.AlreadyExists if the Dataset already
    # exists within the project.
    dataset = client.create_dataset(dataset)  # API request
    # [END bigquery_create_dataset]

    to_delete.append(dataset)


def test_get_dataset_information(client, to_delete):
    """View information about a dataset."""
    dataset_id = 'get_dataset_{}'.format(_millis())
    dataset_labels = {'color': 'green'}
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.description = ORIGINAL_DESCRIPTION
    dataset.labels = dataset_labels
    dataset = client.create_dataset(dataset)  # API request
    to_delete.append(dataset)

    # [START bigquery_get_dataset]
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    dataset = client.get_dataset(dataset_ref)  # API request

    # View dataset properties
    print('Dataset ID: '.format(dataset_id))
    print('Description: '.format(dataset.description))
    print('Labels:')
    for label, value in dataset.labels.items():
        print('\t{}: {}'.format(label, value))
    # View tables in dataset
    print('Tables:')
    tables = list(client.list_tables(dataset_ref))  # API request(s)
    if tables:
        for table in tables:
            print('\t{}'.format(table.table_id))
    else:
        print('\tThis dataset does not contain any tables.')
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
    DATASET_ID = 'get_table_dataset_{}'.format(_millis())
    dataset_ref = client.dataset(DATASET_ID)
    dataset = bigquery.Dataset(dataset_ref)
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    assert dataset_exists(client, dataset_ref)
    assert not dataset_exists(client, client.dataset('i_dont_exist'))


def test_update_dataset_description(client, to_delete):
    """Update a dataset's description."""
    dataset_id = 'update_dataset_description_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.description = 'Original description.'
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_update_dataset_description]
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # dataset = client.get_dataset(dataset_ref)  # API request

    assert dataset.description == 'Original description.'
    dataset.description = 'Updated description.'

    dataset = client.update_dataset(dataset, ['description'])  # API request

    assert dataset.description == 'Updated description.'
    # [END bigquery_update_dataset_description]


def test_update_dataset_default_table_expiration(client, to_delete):
    """Update a dataset's default table expiration."""
    dataset_id = 'update_dataset_default_expiration_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_update_dataset_expiration]
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # dataset = client.get_dataset(dataset_ref)  # API request

    assert dataset.default_table_expiration_ms is None
    one_day_ms = 24 * 60 * 60 * 1000  # in milliseconds
    dataset.default_table_expiration_ms = one_day_ms

    dataset = client.update_dataset(
        dataset, ['default_table_expiration_ms'])  # API request

    assert dataset.default_table_expiration_ms == one_day_ms
    # [END bigquery_update_dataset_expiration]


def test_update_dataset_multiple_properties(client, to_delete):
    """Update a dataset's metadata."""
    dataset_id = 'update_dataset_multiple_properties_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_update_dataset_multiple_properties]
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')
    # dataset = client.get_dataset(dataset_ref)  # API request

    assert dataset.default_table_expiration_ms is None
    assert dataset.labels == {}
    one_day_ms = 24 * 60 * 60 * 1000  # in milliseconds
    labels = {'color': 'green'}
    dataset.labels = labels
    dataset.default_table_expiration_ms = one_day_ms

    dataset = client.update_dataset(
        dataset,
        ['labels', 'default_table_expiration_ms']
    )  # API request

    assert dataset.default_table_expiration_ms == one_day_ms
    assert dataset.labels == labels
    # [END bigquery_update_dataset_multiple_properties]


def test_update_dataset_access(client, to_delete):
    """Update a dataset's access controls."""
    dataset_id = 'update_dataset_access_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_update_dataset_access]
    # client = bigquery.Client()
    # dataset = client.get_dataset(client.dataset('my_dataset'))

    entry = bigquery.AccessEntry(
        role='READER',
        entity_type='userByEmail',
        entity_id='sample.bigquery.dev@gmail.com')
    assert entry not in dataset.access_entries
    entries = list(dataset.access_entries)
    entries.append(entry)
    dataset.access_entries = entries

    dataset = client.update_dataset(dataset, ['access_entries'])  # API request

    assert entry in dataset.access_entries
    # [END bigquery_update_dataset_access]


def test_delete_dataset(client):
    """Delete a dataset."""
    from google.cloud.exceptions import NotFound

    dataset_id = 'delete_dataset_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)

    # [START bigquery_delete_dataset]
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    client.delete_dataset(dataset_ref)  # API request

    print('Dataset {} deleted.'.format(dataset_id))
    # [END bigquery_delete_dataset]

    with pytest.raises(NotFound):
        client.get_dataset(dataset)  # API request


def test_list_tables(client, to_delete):
    """List tables within a dataset."""
    dataset_id = 'list_tables_dataset_{}'.format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = client.create_dataset(bigquery.Dataset(dataset_ref))
    to_delete.append(dataset)

    # [START bigquery_list_tables]
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    tables = list(client.list_tables(dataset_ref))  # API request(s)
    assert len(tables) == 0

    table_ref = dataset.table('my_table')
    table = bigquery.Table(table_ref)
    client.create_table(table)                  # API request
    tables = list(client.list_tables(dataset))  # API request(s)

    assert len(tables) == 1
    assert tables[0].table_id == 'my_table'
    # [END bigquery_list_tables]

    to_delete.insert(0, table)


def test_create_table(client, to_delete):
    """Create a table."""
    dataset_id = 'create_table_dataset_{}'.format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_create_table]
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    schema = [
        bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
    ]
    table_ref = dataset_ref.table('my_table')
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)  # API request

    assert table.table_id == 'my_table'
    # [END bigquery_create_table]

    to_delete.insert(0, table)


def test_create_table_then_add_schema(client, to_delete):
    """Create a table without specifying a schema"""
    dataset_id = 'create_table_without_schema_dataset_{}'.format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_create_table_without_schema]
    # client = bigquery.Client()
    # dataset_ref = client.dataset('my_dataset')

    table_ref = dataset_ref.table('my_table')
    table = bigquery.Table(table_ref)
    table = client.create_table(table)

    assert table.table_id == 'my_table'
    # [END bigquery_create_table_without_schema]

    to_delete.insert(0, table)

    # [START bigquery_add_schema_to_empty]
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    table_ref = client.dataset(dataset_id).table('my_table')
    schema = [
        bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
    ]
    table = bigquery.Table(table_ref, schema=schema)

    table = client.update_table(table, ['schema'])  # API request

    assert table.schema == schema
    # [END bigquery_add_schema_to_empty]


def test_create_table_cmek(client, to_delete):
    DATASET_ID = 'create_table_cmek_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_create_table_cmek]
    table_ref = dataset.table('my_table')
    table = bigquery.Table(table_ref)

    # Set the encryption key to use for the table.
    # TODO: Replace this key with a key you have created in Cloud KMS.
    kms_key_name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        'cloud-samples-tests', 'us-central1', 'test', 'test')
    table.encryption_configuration = bigquery.EncryptionConfiguration(
        kms_key_name=kms_key_name)

    table = client.create_table(table)  # API request

    assert table.encryption_configuration.kms_key_name == kms_key_name
    # [END bigquery_create_table_cmek]


def test_get_table(client, to_delete):
    """Reload a table's metadata."""
    DATASET_ID = 'get_table_dataset_{}'.format(_millis())
    TABLE_ID = 'get_table_table_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(TABLE_ID), schema=SCHEMA)
    table.description = ORIGINAL_DESCRIPTION
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START get_table]
    assert table.description == ORIGINAL_DESCRIPTION
    table.description = LOCALLY_CHANGED_DESCRIPTION
    table = client.get_table(table)  # API request
    assert table.description == ORIGINAL_DESCRIPTION
    # [END get_table]


def test_get_table_information(client, to_delete):
    """Show a table's properties."""
    dataset_id = 'show_table_dataset_{}'.format(_millis())
    table_id = 'show_table_table_{}'.format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table.description = ORIGINAL_DESCRIPTION
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START bigquery_get_table]
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
    DATASET_ID = 'get_table_dataset_{}'.format(_millis())
    TABLE_ID = 'get_table_table_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table_ref = dataset.table(TABLE_ID)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    table = client.create_table(table)
    to_delete.insert(0, table)

    assert table_exists(client, table_ref)
    assert not table_exists(client, dataset.table('i_dont_exist'))


def test_update_table_description(client, to_delete):
    """Update a table's description."""
    dataset_id = 'update_table_description_dataset_{}'.format(_millis())
    table_id = 'update_table_description_table_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table.description = 'Original description.'
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START bigquery_update_table_description]
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('my_table')
    # table = client.get_table(table_ref)  # API request

    assert table.description == 'Original description.'
    table.description = 'Updated description.'

    table = client.update_table(table, ['description'])  # API request

    assert table.description == 'Updated description.'
    # [END bigquery_update_table_description]


def test_update_table_expiration(client, to_delete):
    """Update a table's expiration time."""
    dataset_id = 'update_table_expiration_dataset_{}'.format(_millis())
    table_id = 'update_table_expiration_table_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START bigquery_update_table_expiration]
    import datetime
    import pytz

    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('my_table')
    # table = client.get_table(table_ref)  # API request

    assert table.expires is None

    # set table to expire 5 days from now
    expiration = datetime.datetime.now(pytz.utc) + datetime.timedelta(days=5)
    table.expires = expiration
    table = client.update_table(table, ['expires'])  # API request

    # expiration is stored in milliseconds
    margin = datetime.timedelta(microseconds=1000)
    assert expiration - margin <= table.expires <= expiration + margin
    # [END bigquery_update_table_expiration]


def test_add_empty_column(client, to_delete):
    """Adds an empty column to an existing table."""
    dataset_id = 'add_empty_column_dataset_{}'.format(_millis())
    table_id = 'add_empty_column_table_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START bigquery_add_empty_column]
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # API request

    original_schema = table.schema
    new_schema = original_schema[:]  # creates a copy of the schema
    new_schema.append(bigquery.SchemaField('phone', 'STRING'))

    table.schema = new_schema
    table = client.update_table(table, ['schema'])  # API request

    assert len(table.schema) == len(original_schema) + 1 == len(new_schema)
    # [END bigquery_add_empty_column]


def test_relax_column(client, to_delete):
    """Updates a schema field from required to nullable."""
    dataset_id = 'relax_column_dataset_{}'.format(_millis())
    table_id = 'relax_column_table_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_relax_column]
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'
    original_schema = [
        bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
    ]
    table_ref = client.dataset(dataset_id).table(table_id)
    table = bigquery.Table(table_ref, schema=original_schema)
    table = client.create_table(table)
    assert all(field.mode == 'REQUIRED' for field in table.schema)

    # SchemaField properties cannot be edited after initialization.
    # To make changes, construct new SchemaField objects.
    relaxed_schema = [
        bigquery.SchemaField('full_name', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('age', 'INTEGER', mode='NULLABLE'),
    ]
    table.schema = relaxed_schema
    table = client.update_table(table, ['schema'])

    assert all(field.mode == 'NULLABLE' for field in table.schema)
    # [END bigquery_relax_column]

    to_delete.insert(0, table)


def test_update_table_multiple_properties(client, to_delete):
    """Update a table's metadata."""
    dataset_id = 'update_table_multiple_properties_dataset_{}'.format(
        _millis())
    table_id = 'update_table_multiple_properties_table_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.description = 'Original description'
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table.friendly_name = 'Original friendly name'
    table.description = 'Original description'
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START bigquery_update_table_multiple_properties]
    assert table.friendly_name == 'Original friendly name'
    assert table.description == 'Original description'

    new_schema = list(table.schema)
    new_schema.append(bigquery.SchemaField('phone', 'STRING'))
    table.friendly_name = 'Updated friendly name'
    table.description = 'Updated description'
    table.schema = new_schema
    table = client.update_table(
        table,
        ['schema', 'friendly_name', 'description']
    )  # API request

    assert table.friendly_name == 'Updated friendly name'
    assert table.description == 'Updated description'
    assert table.schema == new_schema
    # [END bigquery_update_table_multiple_properties]


def test_update_table_cmek(client, to_delete):
    """Patch a table's metadata."""
    dataset_id = 'update_table_cmek_{}'.format(_millis())
    table_id = 'update_table_cmek_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id))
    original_kms_key_name = (
        'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
            'cloud-samples-tests', 'us-central1', 'test', 'test'))
    table.encryption_configuration = bigquery.EncryptionConfiguration(
        kms_key_name=original_kms_key_name)
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START bigquery_update_table_cmek]
    assert table.encryption_configuration.kms_key_name == original_kms_key_name

    # Set a new encryption key to use for the destination.
    # TODO: Replace this key with a key you have created in KMS.
    updated_kms_key_name = (
        'projects/cloud-samples-tests/locations/us-central1/'
        'keyRings/test/cryptoKeys/otherkey')
    table.encryption_configuration = bigquery.EncryptionConfiguration(
        kms_key_name=updated_kms_key_name)

    table = client.update_table(
        table, ['encryption_configuration'])  # API request

    assert table.encryption_configuration.kms_key_name == updated_kms_key_name
    assert original_kms_key_name != updated_kms_key_name
    # [END bigquery_update_table_cmek]


def test_browse_table_data(client, to_delete, capsys):
    """Retreive selected row data from a table."""

    # [START bigquery_browse_table]
    # client = bigquery.Client()
    dataset_ref = client.dataset('samples', project='bigquery-public-data')
    table_ref = dataset_ref.table('shakespeare')
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
    format_string = '{!s:<16} ' * len(rows.schema)
    field_names = [field.name for field in rows.schema]
    print(format_string.format(*field_names))  # prints column headers
    for row in rows:
        print(format_string.format(*row))      # prints row data
    # [END bigquery_browse_table]

    out, err = capsys.readouterr()
    out = list(filter(bool, out.split('\n')))  # list of non-blank lines
    assert len(out) == 11


def test_table_insert_rows(client, to_delete):
    """Insert / fetch table data."""
    dataset_id = 'table_insert_rows_dataset_{}'.format(_millis())
    table_id = 'table_insert_rows_table_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(table_id), schema=SCHEMA)
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START bigquery_table_insert_rows]
    rows_to_insert = [
        (u'Phred Phlyntstone', 32),
        (u'Wylma Phlyntstone', 29),
    ]

    errors = client.insert_rows(table, rows_to_insert)  # API request

    assert errors == []
    # [END bigquery_table_insert_rows]


def test_load_table_from_file(client, to_delete):
    """Upload table data from a CSV file."""
    DATASET_ID = 'table_upload_from_file_dataset_{}'.format(_millis())
    TABLE_ID = 'table_upload_from_file_table_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START load_table_from_file]
    csv_file = six.BytesIO(b"""full_name,age
Phred Phlyntstone,32
Wylma Phlyntstone,29
""")

    table_ref = dataset.table(TABLE_ID)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = 'CSV'
    job_config.skip_leading_rows = 1
    job_config.autodetect = True
    job = client.load_table_from_file(
        csv_file, table_ref, job_config=job_config)  # API request
    job.result()  # Waits for table load to complete.
    # [END load_table_from_file]

    table = client.get_table(table_ref)
    to_delete.insert(0, table)
    found_rows = []

    def do_something(row):
        found_rows.append(row)

    # [START table_list_rows]
    for row in client.list_rows(table):  # API request
        do_something(row)
    # [END table_list_rows]

    assert len(found_rows) == 2

    # [START table_list_rows_iterator_properties]
    iterator = client.list_rows(table)  # API request
    page = six.next(iterator.pages)
    rows = list(page)
    total = iterator.total_rows
    token = iterator.next_page_token
    # [END table_list_rows_iterator_properties]

    assert len(rows) == total == 2
    assert token is None
    # Order is not preserved, so compare individually
    row1 = bigquery.Row(('Wylma Phlyntstone', 29), {'full_name': 0, 'age': 1})
    assert row1 in rows
    row2 = bigquery.Row(('Phred Phlyntstone', 32), {'full_name': 0, 'age': 1})
    assert row2 in rows


def test_load_table_from_uri(client, to_delete):
    dataset_id = 'load_table_dataset_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_gcs_json]
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('post_abbr', 'STRING')
    ]
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    load_job = client.load_table_from_uri(
        'gs://cloud-samples-data/bigquery/us-states/us-states.json',
        dataset_ref.table('us_states'),
        job_config=job_config)  # API request

    assert load_job.job_type == 'load'

    load_job.result()  # Waits for table load to complete.

    assert load_job.state == 'DONE'
    assert client.get_table(dataset_ref.table('us_states')).num_rows > 0
    # [END bigquery_load_table_gcs_json]


def test_load_table_from_uri_cmek(client, to_delete):
    dataset_id = 'load_table_from_uri_cmek_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_gcs_json_cmek]
    # dataset_id = 'my_dataset'
    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    # Set the encryption key to use for the destination.
    # TODO: Replace this key with a key you have created in KMS.
    kms_key_name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        'cloud-samples-tests', 'us-central1', 'test', 'test')
    encryption_config = bigquery.EncryptionConfiguration(
        kms_key_name=kms_key_name)
    job_config.destination_encryption_configuration = encryption_config

    load_job = client.load_table_from_uri(
        'gs://cloud-samples-data/bigquery/us-states/us-states.json',
        dataset_ref.table('us_states'),
        job_config=job_config)  # API request

    assert load_job.job_type == 'load'

    load_job.result()  # Waits for table load to complete.

    assert load_job.state == 'DONE'
    table = client.get_table(dataset_ref.table('us_states'))
    assert table.encryption_configuration.kms_key_name == kms_key_name
    # [END bigquery_load_table_gcs_json_cmek]


def test_load_table_from_uri_autodetect(client, to_delete):
    dataset_id = 'load_table_dataset_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_gcs_json_autodetect]
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    load_job = client.load_table_from_uri(
        'gs://cloud-samples-data/bigquery/us-states/us-states.json',
        dataset_ref.table('us_states'),
        job_config=job_config)  # API request

    assert load_job.job_type == 'load'

    load_job.result()  # Waits for table load to complete.

    assert load_job.state == 'DONE'
    assert client.get_table(dataset_ref.table('us_states')).num_rows > 0
    # [END bigquery_load_table_gcs_json_autodetect]


def test_load_table_from_uri_append(client, to_delete):
    dataset_id = 'load_table_dataset_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('post_abbr', 'STRING')
    ]
    table_ref = dataset.table('us_states')
    body = six.StringIO('Washington,WA')
    client.load_table_from_file(
        body, table_ref, job_config=job_config).result()

    # [START bigquery_load_table_gcs_json_append]
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('existing_table')
    previous_rows = client.get_table(table_ref).num_rows
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    load_job = client.load_table_from_uri(
        'gs://cloud-samples-data/bigquery/us-states/us-states.json',
        table_ref,
        job_config=job_config)  # API request

    assert load_job.job_type == 'load'

    load_job.result()  # Waits for table load to complete.

    assert load_job.state == 'DONE'
    assert client.get_table(table_ref).num_rows == previous_rows + 50
    # [END bigquery_load_table_gcs_json_append]


def test_load_table_from_uri_truncate(client, to_delete):
    dataset_id = 'load_table_dataset_{}'.format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('post_abbr', 'STRING')
    ]
    table_ref = dataset.table('us_states')
    body = six.StringIO('Washington,WA')
    client.load_table_from_file(
        body, table_ref, job_config=job_config).result()

    # [START bigquery_load_table_gcs_json_truncate]
    # client = bigquery.Client()
    # table_ref = client.dataset('my_dataset').table('existing_table')
    previous_rows = client.get_table(table_ref).num_rows
    assert previous_rows > 0

    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

    load_job = client.load_table_from_uri(
        'gs://cloud-samples-data/bigquery/us-states/us-states.json',
        table_ref,
        job_config=job_config)  # API request

    assert load_job.job_type == 'load'

    load_job.result()  # Waits for table load to complete.

    assert load_job.state == 'DONE'
    assert client.get_table(table_ref).num_rows == 50
    # [END bigquery_load_table_gcs_json_truncate]


def _write_csv_to_storage(bucket_name, blob_name, header_row, data_rows):
    import csv
    from google.cloud._testing import _NamedTemporaryFile
    from google.cloud.storage import Client as StorageClient

    storage_client = StorageClient()

    # In the **very** rare case the bucket name is reserved, this
    # fails with a ConnectionError.
    bucket = storage_client.create_bucket(bucket_name)

    blob = bucket.blob(blob_name)

    with _NamedTemporaryFile() as temp:
        with open(temp.name, 'w') as csv_write:
            writer = csv.writer(csv_write)
            writer.writerow(header_row)
            writer.writerows(data_rows)

        with open(temp.name, 'rb') as csv_read:
            blob.upload_from_file(csv_read, content_type='text/csv')

    return bucket, blob


def test_copy_table(client, to_delete):
    dataset_id = 'copy_table_dataset_{}'.format(_millis())
    dest_dataset = bigquery.Dataset(client.dataset(dataset_id))
    dest_dataset = client.create_dataset(dest_dataset)
    to_delete.append(dest_dataset)

    # [START bigquery_copy_table]
    # client = bigquery.Client()
    source_dataset = client.dataset('samples', project='bigquery-public-data')
    source_table_ref = source_dataset.table('shakespeare')

    # dataset_id = 'my_dataset'
    dest_table_ref = client.dataset(dataset_id).table('destination_table')

    job = client.copy_table(source_table_ref, dest_table_ref)  # API request
    job.result()  # Waits for job to complete.

    assert job.state == 'DONE'
    dest_table = client.get_table(dest_table_ref)  # API request
    assert dest_table.num_rows > 0
    # [END bigquery_copy_table]

    to_delete.insert(0, dest_table)


def test_copy_table_multiple_source(client, to_delete):
    dest_dataset_id = 'dest_dataset_{}'.format(_millis())
    dest_dataset = bigquery.Dataset(client.dataset(dest_dataset_id))
    dest_dataset = client.create_dataset(dest_dataset)
    to_delete.append(dest_dataset)

    source_dataset_id = 'source_dataset_{}'.format(_millis())
    source_dataset = bigquery.Dataset(client.dataset(source_dataset_id))
    source_dataset = client.create_dataset(source_dataset)
    to_delete.append(source_dataset)

    schema = [
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('post_abbr', 'STRING')
    ]

    table_data = {'table1': 'Washington,WA', 'table2': 'California,CA'}
    for table_id, data in table_data.items():
        table_ref = source_dataset.table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        to_delete.insert(0, table)
        job_config = bigquery.LoadJobConfig()
        job_config.schema = schema
        body = six.StringIO(data)
        client.load_table_from_file(
            body, table_ref, job_config=job_config).result()  # API request

    # [START bigquery_copy_table_multiple_source]
    # client = bigquery.Client()
    # source_dataset_id = 'my_source_dataset'
    # dest_dataset_id = 'my_destination_dataset'
    table1_ref = client.dataset(source_dataset_id).table('table1')
    table2_ref = client.dataset(source_dataset_id).table('table2')
    dest_table_ref = client.dataset(dest_dataset_id).table('destination_table')

    job = client.copy_table(
        [table1_ref, table2_ref], dest_table_ref)  # API request
    job.result()  # Waits for job to complete.

    assert job.state == 'DONE'
    dest_table = client.get_table(dest_table_ref)  # API request
    assert dest_table.num_rows > 0
    # [END bigquery_copy_table_multiple_source]

    assert dest_table.num_rows == 2
    to_delete.insert(0, dest_table)


def test_copy_table_cmek(client, to_delete):
    dataset_id = 'copy_table_cmek_{}'.format(_millis())
    dest_dataset = bigquery.Dataset(client.dataset(dataset_id))
    dest_dataset = client.create_dataset(dest_dataset)
    to_delete.append(dest_dataset)

    # [START bigquery_copy_table_cmek]
    source_dataset = bigquery.DatasetReference(
        'bigquery-public-data', 'samples')
    source_table_ref = source_dataset.table('shakespeare')

    # dataset_id = 'my_dataset'
    dest_dataset_ref = client.dataset(dataset_id)
    dest_table_ref = dest_dataset_ref.table('destination_table')

    # Set the encryption key to use for the destination.
    # TODO: Replace this key with a key you have created in KMS.
    kms_key_name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        'cloud-samples-tests', 'us-central1', 'test', 'test')
    encryption_config = bigquery.EncryptionConfiguration(
        kms_key_name=kms_key_name)
    job_config = bigquery.CopyJobConfig()
    job_config.destination_encryption_configuration = encryption_config

    job = client.copy_table(
        source_table_ref, dest_table_ref, job_config=job_config)  # API request
    job.result()  # Waits for job to complete.

    assert job.state == 'DONE'
    dest_table = client.get_table(dest_table_ref)
    assert dest_table.encryption_configuration.kms_key_name == kms_key_name
    # [END bigquery_copy_table_cmek]

    to_delete.insert(0, dest_table)


def test_extract_table(client, to_delete):
    from google.cloud import storage

    bucket_name = 'extract_shakespeare_{}'.format(_millis())
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)  # API request
    to_delete.append(bucket)

    # [START bigquery_extract_table]
    # client = bigquery.Client()
    # bucket_name = 'my-bucket'
    destination_uri = 'gs://{}/{}'.format(bucket_name, 'shakespeare.csv')
    dataset_ref = client.dataset('samples', project='bigquery-public-data')
    table_ref = dataset_ref.table('shakespeare')

    extract_job = client.extract_table(
        table_ref, destination_uri)  # API request
    extract_job.result()  # Waits for job to complete.
    # [END bigquery_extract_table]

    blob = bucket.get_blob('shakespeare.csv')
    assert blob.exists
    assert blob.size > 0
    to_delete.insert(0, blob)


def test_extract_table_json(client, to_delete):
    from google.cloud import storage

    bucket_name = 'extract_shakespeare_json_{}'.format(_millis())
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)  # API request
    to_delete.append(bucket)

    # [START bigquery_extract_table_json]
    # client = bigquery.Client()
    # bucket_name = 'my-bucket'
    destination_uri = 'gs://{}/{}'.format(bucket_name, 'shakespeare.json')
    dataset_ref = client.dataset('samples', project='bigquery-public-data')
    table_ref = dataset_ref.table('shakespeare')
    job_config = bigquery.job.ExtractJobConfig()
    job_config.destination_format = (
        bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON)

    extract_job = client.extract_table(
        table_ref, destination_uri, job_config=job_config)  # API request
    extract_job.result()  # Waits for job to complete.
    # [END bigquery_extract_table_json]

    blob = bucket.get_blob('shakespeare.json')
    assert blob.exists
    assert blob.size > 0
    to_delete.insert(0, blob)


def test_extract_table_compressed(client, to_delete):
    from google.cloud import storage

    bucket_name = 'extract_shakespeare_compress_{}'.format(_millis())
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)  # API request
    to_delete.append(bucket)

    # [START bigquery_extract_table_compressed]
    # client = bigquery.Client()
    # bucket_name = 'my-bucket'
    destination_uri = 'gs://{}/{}'.format(bucket_name, 'shakespeare.csv.gz')
    dataset_ref = client.dataset('samples', project='bigquery-public-data')
    table_ref = dataset_ref.table('shakespeare')
    job_config = bigquery.job.ExtractJobConfig()
    job_config.compression = bigquery.Compression.GZIP

    extract_job = client.extract_table(
        table_ref, destination_uri, job_config=job_config)  # API request
    extract_job.result()  # Waits for job to complete.
    # [END bigquery_extract_table_compressed]

    blob = bucket.get_blob('shakespeare.csv.gz')
    assert blob.exists
    assert blob.size > 0
    to_delete.insert(0, blob)


def test_delete_table(client, to_delete):
    """Delete a table."""
    from google.cloud.exceptions import NotFound

    dataset_id = 'delete_table_dataset_{}'.format(_millis())
    table_id = 'delete_table_table_{}'.format(_millis())
    dataset_ref = client.dataset(dataset_id)
    dataset = client.create_dataset(bigquery.Dataset(dataset_ref))
    to_delete.append(dataset)

    table_ref = dataset.table(table_id)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    client.create_table(table)
    # [START bigquery_delete_table]
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    table_ref = client.dataset(dataset_id).table(table_id)
    client.delete_table(table_ref)  # API request

    print('Table {}:{} deleted.'.format(dataset_id, table_id))
    # [END bigquery_delete_table]

    with pytest.raises(NotFound):
        client.get_table(table)  # API request


def test_client_simple_query(client):
    """Run a simple query."""

    # [START client_simple_query]
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    query_job = client.query(QUERY)

    for row in query_job:  # API request
        # Row values can be accessed by field name or index
        assert row[0] == row.name == row['name']
    # [END client_simple_query]


def test_client_query(client):
    """Run a query"""

    # [START client_query]
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    TIMEOUT = 30  # in seconds
    query_job = client.query(QUERY)  # API request - starts the query

    # Waits for the query to finish
    iterator = query_job.result(timeout=TIMEOUT)
    rows = list(iterator)

    assert query_job.state == 'DONE'
    assert len(rows) == 100
    row = rows[0]
    assert row[0] == row.name == row['name']
    # [END client_query]


def test_client_query_destination_table(client, to_delete):
    """Run a query"""
    dataset_id = 'query_destination_table_{}'.format(_millis())
    dataset_ref = client.dataset(dataset_id)
    to_delete.append(dataset_ref)
    client.create_dataset(bigquery.Dataset(dataset_ref))
    to_delete.insert(0, dataset_ref.table('your_table_id'))

    # [START bigquery_query_destination_table]
    # client = bigquery.Client()
    job_config = bigquery.QueryJobConfig()

    # Set the destination table. Here, dataset_id is a string, such as:
    # dataset_id = 'your_dataset_id'
    table_ref = client.dataset(dataset_id).table('your_table_id')
    job_config.destination = table_ref

    # The write_disposition specifies the behavior when writing query results
    # to a table that already exists. With WRITE_TRUNCATE, any existing rows
    # in the table are overwritten by the query results.
    job_config.write_disposition = 'WRITE_TRUNCATE'

    # Start the query, passing in the extra configuration.
    query_job = client.query(
        'SELECT 17 AS my_col;', job_config=job_config)

    rows = list(query_job)  # Waits for the query to finish
    assert len(rows) == 1
    row = rows[0]
    assert row[0] == row.my_col == 17

    # In addition to using the results from the query, you can read the rows
    # from the destination table directly.
    iterator = client.list_rows(
        table_ref, selected_fields=[bigquery.SchemaField('my_col', 'INT64')])

    rows = list(iterator)
    assert len(rows) == 1
    row = rows[0]
    assert row[0] == row.my_col == 17
    # [END bigquery_query_destination_table]


def test_client_query_destination_table_cmek(client, to_delete):
    """Run a query"""
    dataset_id = 'query_destination_table_{}'.format(_millis())
    dataset_ref = client.dataset(dataset_id)
    to_delete.append(dataset_ref)
    client.create_dataset(bigquery.Dataset(dataset_ref))
    to_delete.insert(0, dataset_ref.table('your_table_id'))

    # [START bigquery_query_destination_table_cmek]
    job_config = bigquery.QueryJobConfig()

    # Set the destination table. Here, dataset_id is a string, such as:
    # dataset_id = 'your_dataset_id'
    table_ref = client.dataset(dataset_id).table('your_table_id')
    job_config.destination = table_ref

    # Set the encryption key to use for the destination.
    # TODO: Replace this key with a key you have created in KMS.
    kms_key_name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        'cloud-samples-tests', 'us-central1', 'test', 'test')
    encryption_config = bigquery.EncryptionConfiguration(
        kms_key_name=kms_key_name)
    job_config.destination_encryption_configuration = encryption_config

    # Start the query, passing in the extra configuration.
    query_job = client.query(
        'SELECT 17 AS my_col;', job_config=job_config)
    query_job.result()

    # The destination table is written using the encryption configuration.
    table = client.get_table(table_ref)
    assert table.encryption_configuration.kms_key_name == kms_key_name
    # [END bigquery_query_destination_table_cmek]


def test_client_query_w_param(client):
    """Run a query using a query parameter"""

    # [START client_query_w_param]
    QUERY_W_PARAM = (
        'SELECT name, state '
        'FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = @state '
        'LIMIT 100')
    TIMEOUT = 30  # in seconds
    param = bigquery.ScalarQueryParameter('state', 'STRING', 'TX')
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = [param]
    query_job = client.query(
        QUERY_W_PARAM, job_config=job_config)  # API request - starts the query

    # Waits for the query to finish
    iterator = query_job.result(timeout=TIMEOUT)
    rows = list(iterator)

    assert query_job.state == 'DONE'
    assert len(rows) == 100
    row = rows[0]
    assert row[0] == row.name == row['name']
    assert row.state == 'TX'
    # [END client_query_w_param]


def test_client_list_jobs(client):
    """List jobs for a project."""

    def do_something_with(_):
        pass

    # [START client_list_jobs]
    job_iterator = client.list_jobs()  # API request(s)
    for job in job_iterator:
        do_something_with(job)
    # [END client_list_jobs]


@pytest.mark.skipif(pandas is None, reason='Requires `pandas`')
def test_query_results_as_dataframe(client):
    # [START bigquery_query_results_dataframe]
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
    assert len(df) == 10       # verify the number of rows


@pytest.mark.skipif(pandas is None, reason='Requires `pandas`')
def test_list_rows_as_dataframe(client):
    # [START bigquery_list_rows_dataframe]
    # client = bigquery.Client()
    dataset_ref = client.dataset('samples', project='bigquery-public-data')
    table_ref = dataset_ref.table('shakespeare')
    table = client.get_table(table_ref)

    df = client.list_rows(table).to_dataframe()
    # [END bigquery_list_rows_dataframe]
    assert isinstance(df, pandas.DataFrame)
    assert len(list(df)) == 2  # verify the number of columns
    assert len(df) == 10       # verify the number of rows


if __name__ == '__main__':
    pytest.main()
