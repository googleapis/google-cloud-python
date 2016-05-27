# Copyright 2016 Google Inc. All rights reserved.
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

"""Testable usage examples for Google Cloud BigQuery API wrapper

Each example function takes a ``client`` argument (which must be an instance
of :class:`gcloud.bigquery.client.Client`) and uses it to perform a task with
the API.

To facility running the examples as system tests, each example is also passed
a ``to_delete`` list;  the function adds to the list any objects created which
need to be deleted during teardown.
"""

import time

from gcloud.bigquery.client import Client


def snippet(func):
    """Mark ``func`` as a snippet example function."""
    func._snippet = True
    return func


def _millis():
    return time.time() * 1000


@snippet
def client_list_datasets(client, to_delete):  # pylint: disable=unused-argument
    """List datasets for a project."""

    def do_something_with(sub):  # pylint: disable=unused-argument
        pass

    # [START client_list_datasets]
    datasets, token = client.list_datasets()   # API request
    while True:
        for dataset in datasets:
            do_something_with(dataset)
        if token is None:
            break
        datasets, token = client.list_datasets(page_token=token)  # API request
    # [END client_list_datasets]


@snippet
def dataset_create(client, to_delete):
    """Create a dataset."""
    DATASET_NAME = 'dataset_create_%d' % (_millis(),)

    # [START dataset_create]
    dataset = client.dataset(DATASET_NAME)
    dataset.create()              # API request
    # [END dataset_create]

    to_delete.append(dataset)


@snippet
def dataset_exists(client, to_delete):
    """Test existence of a dataset."""
    DATASET_NAME = 'dataset_exists_%d' % (_millis(),)
    dataset = client.dataset(DATASET_NAME)
    to_delete.append(dataset)

    # [START dataset_exists]
    assert not dataset.exists()   # API request
    dataset.create()              # API request
    assert dataset.exists()       # API request
    # [END dataset_exists]


@snippet
def dataset_reload(client, to_delete):
    """Reload a dataset's metadata."""
    DATASET_NAME = 'dataset_reload_%d' % (_millis(),)
    ORIGINAL_DESCRIPTION = 'Original description'
    LOCALLY_CHANGED_DESCRIPTION = 'Locally-changed description'
    dataset = client.dataset(DATASET_NAME)
    dataset.description = ORIGINAL_DESCRIPTION
    dataset.create()
    to_delete.append(dataset)

    # [START dataset_reload]
    assert dataset.description == ORIGINAL_DESCRIPTION
    dataset.description = LOCALLY_CHANGED_DESCRIPTION
    assert dataset.description == LOCALLY_CHANGED_DESCRIPTION
    dataset.reload()              # API request
    assert dataset.description == ORIGINAL_DESCRIPTION
    # [END dataset_reload]


@snippet
def dataset_patch(client, to_delete):
    """Patch a dataset's metadata."""
    DATASET_NAME = 'dataset_patch_%d' % (_millis(),)
    ORIGINAL_DESCRIPTION = 'Original description'
    PATCHED_DESCRIPTION = 'Patched description'
    dataset = client.dataset(DATASET_NAME)
    dataset.description = ORIGINAL_DESCRIPTION
    dataset.create()
    to_delete.append(dataset)

    # [START dataset_patch]
    ONE_DAY_MS = 24 * 60 * 60 * 1000
    assert dataset.description == ORIGINAL_DESCRIPTION
    dataset.patch(
        description=PATCHED_DESCRIPTION,
        default_table_expiration_ms=ONE_DAY_MS
    )      # API request
    assert dataset.description == PATCHED_DESCRIPTION
    assert dataset.default_table_expiration_ms == ONE_DAY_MS
    # [END dataset_patch]


@snippet
def dataset_update(client, to_delete):
    """Update a dataset's metadata."""
    DATASET_NAME = 'dataset_update_%d' % (_millis(),)
    ORIGINAL_DESCRIPTION = 'Original description'
    UPDATED_DESCRIPTION = 'Updated description'
    dataset = client.dataset(DATASET_NAME)
    dataset.description = ORIGINAL_DESCRIPTION
    dataset.create()
    to_delete.append(dataset)
    dataset.reload()

    # [START dataset_update]
    from gcloud.bigquery import AccessGrant
    assert dataset.description == ORIGINAL_DESCRIPTION
    assert dataset.default_table_expiration_ms == None
    grant = AccessGrant(
        role='READER', entity_type='domain', entity_id='example.com')
    assert grant not in dataset.access_grants
    ONE_DAY_MS = 24 * 60 * 60 * 1000
    dataset.description = UPDATED_DESCRIPTION
    dataset.default_table_expiration_ms = ONE_DAY_MS
    grants = list(dataset.access_grants)
    grants.append(grant)
    dataset.access_grants = grants
    dataset.update()              # API request
    assert dataset.description == UPDATED_DESCRIPTION
    assert dataset.default_table_expiration_ms == ONE_DAY_MS
    assert grant in dataset.access_grants
    # [END dataset_update]


@snippet
def dataset_delete(client, to_delete):  # pylint: disable=unused-argument
    """Delete a dataset."""
    DATASET_NAME = 'dataset_delete_%d' % (_millis(),)
    dataset = client.dataset(DATASET_NAME)
    dataset.create()

    # [START dataset_delete]
    assert dataset.exists()       # API request
    dataset.delete()
    assert not dataset.exists()   # API request
    # [END dataset_delete]


def _find_examples():
    funcs = [obj for obj in globals().values()
             if getattr(obj, '_snippet', False)]
    for func in sorted(funcs, key=lambda f: f.func_code.co_firstlineno):
        yield func


def main():
    client = Client()
    for example in _find_examples():
        to_delete = []
        print('%-25s: %s' % (
            example.func_name, example.func_doc))
        try:
            example(client, to_delete)
        except AssertionError as e:
            print('   FAIL: %s' % (e,))
        except Exception as e:  # pylint: disable=broad-except
            print('  ERROR: %r' % (e,))
        for item in to_delete:
            item.delete()

if __name__ == '__main__':
    main()
