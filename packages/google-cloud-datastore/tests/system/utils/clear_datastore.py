# Copyright 2014 Google Inc.
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

"""Script to populate datastore with system test data."""

from __future__ import print_function

import os

import six

from google.cloud import datastore


FETCH_MAX = 20
ALL_KINDS = (
    'Character',
    'Company',
    'Kind',
    'Person',
    'Post',
)
TRANSACTION_MAX_GROUPS = 5


def print_func(message):
    if os.getenv('GOOGLE_CLOUD_NO_PRINT') != 'true':
        print(message)


def fetch_keys(kind, client, fetch_max=FETCH_MAX, query=None, cursor=None):
    if query is None:
        query = client.query(kind=kind)
        query.keys_only()

    iterator = query.fetch(limit=fetch_max, start_cursor=cursor)
    page = six.next(iterator.pages)
    return query, list(page), iterator.next_page_token


def get_ancestors(entities):
    # NOTE: A key will always have at least one path element.
    key_roots = [entity.key.flat_path[:2] for entity in entities]
    # Return the unique roots.
    return list(set(key_roots))


def remove_kind(kind, client):
    results = []

    query, curr_results, cursor = fetch_keys(kind, client)
    results.extend(curr_results)
    while curr_results:
        query, curr_results, cursor = fetch_keys(
            kind, client, query=query, cursor=cursor)
        results.extend(curr_results)

    if not results:
        return

    delete_outside_transaction = False
    with client.transaction():
        # Now that we have all results, we seek to delete.
        print_func('Deleting keys:')
        print_func(results)

        ancestors = get_ancestors(results)
        if len(ancestors) > TRANSACTION_MAX_GROUPS:
            delete_outside_transaction = True
        else:
            client.delete_multi([result.key for result in results])

    if delete_outside_transaction:
        client.delete_multi([result.key for result in results])


def remove_all_entities(client=None):
    if client is None:
        # Get a client that uses the test dataset.
        client = datastore.Client()
    for kind in ALL_KINDS:
        remove_kind(kind, client)


if __name__ == '__main__':
    print_func('This command will remove all entities for '
               'the following kinds:')
    print_func('\n'.join('- ' + val for val in ALL_KINDS))
    response = six.moves.input('Is this OK [y/n]? ')
    if response.lower() == 'y':
        remove_all_entities()
    else:
        print_func('Doing nothing.')
