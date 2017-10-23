# Copyright 2016 Google Inc.
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

from google.cloud import bigquery

ORIGINAL_FRIENDLY_NAME = 'Original friendly name'
ORIGINAL_DESCRIPTION = 'Original description'
LOCALLY_CHANGED_FRIENDLY_NAME = 'Locally-changed friendly name'
LOCALLY_CHANGED_DESCRIPTION = 'Locally-changed description'
UPDATED_FRIENDLY_NAME = 'Updated friendly name'
UPDATED_DESCRIPTION = 'Updated description'

SCHEMA = [
    bigquery.SchemaField('full_name', 'STRING', mode='required'),
    bigquery.SchemaField('age', 'INTEGER', mode='required'),
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
        if isinstance(item, bigquery.Dataset):
            client.delete_dataset(item)
        elif isinstance(item, bigquery.Table):
            client.delete_table(item)
        else:
            item.delete()


def _millis():
    return time.time() * 1000


class _CloseOnDelete(object):

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def delete(self):
        self._wrapped.close()


def test_client_list_datasets(client):
    """List datasets for a project."""

    def do_something_with(_):
        pass

    # [START client_list_datasets]
    for dataset in client.list_datasets():  # API request(s)
        do_something_with(dataset)
    # [END client_list_datasets]


def test_create_dataset(client, to_delete):
    """Create a dataset."""
    DATASET_ID = 'create_dataset_%d' % (_millis(),)

    # [START create_dataset]
    # DATASET_ID = 'dataset_ids_are_strings'
    dataset_ref = client.dataset(DATASET_ID)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.description = 'my dataset'
    dataset = client.create_dataset(dataset)  # API request
    # [END create_dataset]

    to_delete.append(dataset)


def test_get_dataset(client, to_delete):
    """Reload a dataset's metadata."""
    DATASET_ID = 'get_dataset_%d' % (_millis(),)
    dataset_ref = client.dataset(DATASET_ID)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.description = ORIGINAL_DESCRIPTION
    dataset = client.create_dataset(dataset)  # API request
    to_delete.append(dataset)

    # [START get_dataset]
    assert dataset.description == ORIGINAL_DESCRIPTION
    dataset.description = LOCALLY_CHANGED_DESCRIPTION
    assert dataset.description == LOCALLY_CHANGED_DESCRIPTION
    dataset = client.get_dataset(dataset)  # API request
    assert dataset.description == ORIGINAL_DESCRIPTION
    # [END get_dataset]


def test_update_dataset_simple(client, to_delete):
    """Update a dataset's metadata."""
    DATASET_ID = 'update_dataset_simple_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset.description = ORIGINAL_DESCRIPTION
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START update_dataset_simple]
    assert dataset.description == ORIGINAL_DESCRIPTION
    dataset.description = UPDATED_DESCRIPTION

    dataset = client.update_dataset(dataset, ['description'])  # API request

    assert dataset.description == UPDATED_DESCRIPTION
    # [END update_dataset_simple]


def test_update_dataset_multiple_properties(client, to_delete):
    """Update a dataset's metadata."""
    DATASET_ID = 'update_dataset_multiple_properties_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset.description = ORIGINAL_DESCRIPTION
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START update_dataset_multiple_properties]
    assert dataset.description == ORIGINAL_DESCRIPTION
    assert dataset.default_table_expiration_ms is None
    entry = bigquery.AccessEntry(
        role='READER', entity_type='domain', entity_id='example.com')
    assert entry not in dataset.access_entries
    ONE_DAY_MS = 24 * 60 * 60 * 1000  # in milliseconds
    dataset.description = UPDATED_DESCRIPTION
    dataset.default_table_expiration_ms = ONE_DAY_MS
    entries = list(dataset.access_entries)
    entries.append(entry)
    dataset.access_entries = entries

    dataset = client.update_dataset(
        dataset,
        ['description', 'default_table_expiration_ms', 'access_entries']
    )  # API request

    assert dataset.description == UPDATED_DESCRIPTION
    assert dataset.default_table_expiration_ms == ONE_DAY_MS
    assert entry in dataset.access_entries
    # [END update_dataset_multiple_properties]


def test_delete_dataset(client):
    """Delete a dataset."""
    DATASET_ID = 'delete_dataset_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    client.create_dataset(dataset)

    # [START delete_dataset]
    from google.cloud.exceptions import NotFound

    client.delete_dataset(dataset)  # API request

    with pytest.raises(NotFound):
        client.get_dataset(dataset)  # API request
    # [END delete_dataset]


def test_list_dataset_tables(client, to_delete):
    """List tables within a dataset."""
    DATASET_ID = 'list_dataset_tables_dataset_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START list_dataset_tables]
    tables = list(client.list_dataset_tables(dataset))  # API request(s)
    assert len(tables) == 0

    table_ref = dataset.table('my_table')
    table = bigquery.Table(table_ref)
    table.view_query = QUERY
    client.create_table(table)                          # API request
    tables = list(client.list_dataset_tables(dataset))  # API request(s)

    assert len(tables) == 1
    assert tables[0].table_id == 'my_table'
    # [END list_dataset_tables]

    to_delete.insert(0, table)


def test_create_table(client, to_delete):
    """Create a table."""
    DATASET_ID = 'create_table_dataset_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START create_table]
    SCHEMA = [
        bigquery.SchemaField('full_name', 'STRING', mode='required'),
        bigquery.SchemaField('age', 'INTEGER', mode='required'),
    ]
    table_ref = dataset.table('my_table')
    table = bigquery.Table(table_ref, schema=SCHEMA)
    table = client.create_table(table)      # API request

    assert table.table_id == 'my_table'
    # [END create_table]

    to_delete.insert(0, table)


def test_get_table(client, to_delete):
    """Reload a table's metadata."""
    DATASET_ID = 'get_table_dataset_%d' % (_millis(),)
    TABLE_ID = 'get_table_table_%d' % (_millis(),)
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


def test_update_table_simple(client, to_delete):
    """Patch a table's metadata."""
    DATASET_ID = 'update_table_simple_dataset_%d' % (_millis(),)
    TABLE_ID = 'update_table_simple_table_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset.description = ORIGINAL_DESCRIPTION
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(TABLE_ID), schema=SCHEMA)
    table.description = ORIGINAL_DESCRIPTION
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START update_table_simple]
    assert table.description == ORIGINAL_DESCRIPTION
    table.description = UPDATED_DESCRIPTION

    table = client.update_table(table, ['description'])  # API request

    assert table.description == UPDATED_DESCRIPTION
    # [END update_table_simple]


def test_update_table_multiple_properties(client, to_delete):
    """Update a table's metadata."""
    DATASET_ID = 'update_table_multiple_properties_dataset_%d' % (_millis(),)
    TABLE_ID = 'update_table_multiple_properties_table_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset.description = ORIGINAL_DESCRIPTION
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(TABLE_ID), schema=SCHEMA)
    table.friendly_name = ORIGINAL_FRIENDLY_NAME
    table.description = ORIGINAL_DESCRIPTION
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START update_table_multiple_properties]
    assert table.friendly_name == ORIGINAL_FRIENDLY_NAME
    assert table.description == ORIGINAL_DESCRIPTION

    NEW_SCHEMA = list(table.schema)
    NEW_SCHEMA.append(bigquery.SchemaField('phone', 'STRING'))
    table.friendly_name = UPDATED_FRIENDLY_NAME
    table.description = UPDATED_DESCRIPTION
    table.schema = NEW_SCHEMA
    table = client.update_table(
        table,
        ['schema', 'friendly_name', 'description']
    )  # API request

    assert table.friendly_name == UPDATED_FRIENDLY_NAME
    assert table.description == UPDATED_DESCRIPTION
    assert table.schema == NEW_SCHEMA
    # [END update_table_multiple_properties]


def test_table_create_rows(client, to_delete):
    """Insert / fetch table data."""
    DATASET_ID = 'table_create_rows_dataset_%d' % (_millis(),)
    TABLE_ID = 'table_create_rows_table_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dataset = client.create_dataset(dataset)
    to_delete.append(dataset)

    table = bigquery.Table(dataset.table(TABLE_ID), schema=SCHEMA)
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START table_create_rows]
    ROWS_TO_INSERT = [
        (u'Phred Phlyntstone', 32),
        (u'Wylma Phlyntstone', 29),
    ]

    errors = client.create_rows(table, ROWS_TO_INSERT)  # API request

    assert errors == []
    # [END table_create_rows]


def test_load_table_from_file(client, to_delete):
    """Upload table data from a CSV file."""
    DATASET_ID = 'table_upload_from_file_dataset_%d' % (_millis(),)
    TABLE_ID = 'table_upload_from_file_table_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table_ref = dataset.table(TABLE_ID)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    table = client.create_table(table)
    to_delete.insert(0, table)

    # [START load_table_from_file]
    csv_file = six.BytesIO(b"""full_name,age
Phred Phlyntstone,32
Wylma Phlyntstone,29
""")

    table_ref = dataset.table(TABLE_ID)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = 'CSV'
    job_config.skip_leading_rows = 1
    job = client.load_table_from_file(
        csv_file, table_ref, job_config=job_config)  # API request
    job.result()  # Waits for table load to complete.
    # [END load_table_from_file]

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

    row_tuples = [r.values() for r in rows]
    assert len(rows) == total == 2
    assert token is None
    assert (u'Phred Phlyntstone', 32) in row_tuples
    assert (u'Wylma Phlyntstone', 29) in row_tuples


def test_load_table_from_uri(client, to_delete):
    ROWS = [
        ('Phred Phlyntstone', 32),
        ('Bharney Rhubble', 33),
        ('Wylma Phlyntstone', 29),
        ('Bhettye Rhubble', 27),
    ]
    HEADER_ROW = ('Full Name', 'Age')
    bucket_name = 'gs_bq_load_test_%d' % (_millis(),)
    blob_name = 'person_ages.csv'
    bucket, blob = _write_csv_to_storage(
        bucket_name, blob_name, HEADER_ROW, ROWS)
    to_delete.extend((blob, bucket))
    DATASET_ID = 'delete_table_dataset_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START load_table_from_uri]
    table_ref = dataset.table('person_ages')
    table = bigquery.Table(table_ref)
    table.schema = [
        bigquery.SchemaField('full_name', 'STRING', mode='required'),
        bigquery.SchemaField('age', 'INTEGER', mode='required')
    ]
    client.create_table(table)  # API request
    GS_URL = 'gs://{}/{}'.format(bucket_name, blob_name)
    job_id_prefix = "my_job"
    job_config = bigquery.LoadJobConfig()
    job_config.create_disposition = 'NEVER'
    job_config.skip_leading_rows = 1
    job_config.source_format = 'CSV'
    job_config.write_disposition = 'WRITE_EMPTY'
    load_job = client.load_table_from_uri(
        GS_URL, table_ref, job_config=job_config,
        job_id_prefix=job_id_prefix)  # API request

    assert load_job.state == 'RUNNING'
    assert load_job.job_type == 'load'

    load_job.result()  # Waits for table load to complete.

    assert load_job.state == 'DONE'
    assert load_job.job_id.startswith(job_id_prefix)
    # [END load_table_from_uri]

    to_delete.insert(0, table)


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
    DATASET_ID = 'copy_table_dataset_%d' % (_millis(),)
    # [START copy_table]
    source_dataset = bigquery.DatasetReference(
        'bigquery-public-data', 'samples')
    source_table_ref = source_dataset.table('shakespeare')

    dest_dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    dest_dataset = client.create_dataset(dest_dataset)  # API request
    dest_table_ref = dest_dataset.table('destination_table')

    job_config = bigquery.CopyJobConfig()
    job = client.copy_table(
        source_table_ref, dest_table_ref, job_config=job_config)  # API request
    job.result()  # Waits for job to complete.

    assert job.state == 'DONE'
    dest_table = client.get_table(dest_table_ref)  # API request
    assert dest_table.table_id == 'destination_table'
    # [END copy_table]

    to_delete.append(dest_dataset)
    to_delete.insert(0, dest_table)


def test_extract_table(client, to_delete):
    DATASET_ID = 'export_data_dataset_%d' % (_millis(),)
    dataset = bigquery.Dataset(client.dataset(DATASET_ID))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    table_ref = dataset.table('person_ages')
    table = client.create_table(bigquery.Table(table_ref, schema=SCHEMA))
    to_delete.insert(0, table)
    client.create_rows(table, ROWS)

    bucket_name = 'extract_person_ages_job_%d' % (_millis(),)
    # [START extract_table]
    from google.cloud.storage import Client as StorageClient

    storage_client = StorageClient()
    bucket = storage_client.create_bucket(bucket_name)  # API request
    destination_blob_name = 'person_ages_out.csv'
    destination = bucket.blob(destination_blob_name)

    destination_uri = 'gs://{}/{}'.format(bucket_name, destination_blob_name)
    extract_job = client.extract_table(
        table_ref, destination_uri)  # API request
    extract_job.result(timeout=100)  # Waits for job to complete.

    got = destination.download_as_string().decode('utf-8')  # API request
    assert 'Bharney Rhubble' in got
    # [END extract_table]
    to_delete.append(bucket)
    to_delete.insert(0, destination)


def test_delete_table(client, to_delete):
    """Delete a table."""
    DATASET_ID = 'delete_table_dataset_%d' % (_millis(),)
    TABLE_ID = 'delete_table_table_%d' % (_millis(),)
    dataset_ref = client.dataset(DATASET_ID)
    dataset = client.create_dataset(bigquery.Dataset(dataset_ref))
    to_delete.append(dataset)

    table_ref = dataset.table(TABLE_ID)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    client.create_table(table)
    # [START delete_table]
    from google.cloud.exceptions import NotFound

    client.delete_table(table)  # API request

    with pytest.raises(NotFound):
        client.get_table(table)  # API request
    # [END delete_table]


def test_client_query(client):
    """Run a query"""

    # [START client_query]
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    TIMEOUT = 30  # in seconds
    query_job = client.query(QUERY)  # API request - starts the query
    assert query_job.state == 'RUNNING'

    # Waits for the query to finish
    iterator = query_job.result(timeout=TIMEOUT)
    rows = list(iterator)

    assert query_job.state == 'DONE'
    assert len(rows) == 100
    row = rows[0]
    assert row[0] == row.name == row['name']
    # [END client_query]


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
    assert query_job.state == 'RUNNING'

    # Waits for the query to finish
    iterator = query_job.result(timeout=TIMEOUT)
    rows = list(iterator)

    assert query_job.state == 'DONE'
    assert len(rows) == 100
    row = rows[0]
    assert row[0] == row.name == row['name']
    assert row.state == 'TX'
    # [END client_query_w_param]


def test_client_query_rows(client):
    """Run a simple query."""

    # [START client_query_rows]
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    TIMEOUT = 30  # in seconds
    rows = list(client.query_rows(QUERY, timeout=TIMEOUT))  # API request

    assert len(rows) == 100
    row = rows[0]
    assert row[0] == row.name == row['name']
    # [END client_query_rows]


def test_client_list_jobs(client):
    """List jobs for a project."""

    def do_something_with(_):
        pass

    # [START client_list_jobs]
    job_iterator = client.list_jobs()  # API request(s)
    for job in job_iterator:
        do_something_with(job)
    # [END client_list_jobs]


if __name__ == '__main__':
    pytest.main()
