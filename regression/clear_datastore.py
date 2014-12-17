# Copyright 2014 Google Inc. All rights reserved.
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

"""Script to populate datastore with regression test data."""


# This assumes the command is being run via tox hence the
# repository root is the current directory.
from regression import regression_utils
from six.moves import input


FETCH_MAX = 20
ALL_KINDS = [
    'Character',
    'Company',
    'Kind',
    'Person',
    'Post',
]
TRANSACTION_MAX_GROUPS = 5


def fetch_keys(dataset, kind, fetch_max=FETCH_MAX, query=None, cursor=None):
    if query is None:
        query = dataset.query(kind=kind).limit(
            fetch_max).projection(['__key__'])
    # Make new query with start cursor. Will be ignored if None.
    query = query.with_cursor(cursor)

    entities, cursor, _ = query.fetch_page()
    return query, entities, cursor


def get_ancestors(entities):
    # NOTE: A key will always have at least one path element.
    key_roots = [entity.key().path()[0] for entity in entities]
    # Turn into hashable type so we can use set to get unique roots.
    # Also sorted the items() to ensure uniqueness.
    key_roots = [tuple(sorted(root.items())) for root in key_roots]
    # Cast back to dictionary.
    return [dict(root) for root in set(key_roots)]


def delete_entities(dataset, entities):
    dataset_id = dataset.id()
    connection = dataset.connection()

    key_pbs = [entity.key().to_protobuf() for entity in entities]
    connection.delete_entities(dataset_id, key_pbs)


def remove_kind(dataset, kind):
    delete_outside_transaction = False
    with dataset.transaction():
        results = []

        query, curr_results, cursor = fetch_keys(dataset, kind)
        results.extend(curr_results)
        while curr_results:
            query, curr_results, cursor = fetch_keys(
                dataset, kind, query=query, cursor=cursor)
            results.extend(curr_results)

        if not results:
            return

        # Now that we have all results, we seek to delete.
        print('Deleting keys:')
        print(results)

        ancestors = get_ancestors(results)
        if len(ancestors) > TRANSACTION_MAX_GROUPS:
            delete_outside_transaction = True
        else:
            delete_entities(dataset, results)

    if delete_outside_transaction:
        delete_entities(dataset, results)


def remove_all_entities():
    print('This command will remove all entities for the following kinds:')
    print('\n'.join(['- ' + val for val in ALL_KINDS]))
    response = input('Is this OK [y/n]? ')
    if response.lower() != 'y':
        print('Doing nothing.')
        return

    dataset = regression_utils.get_dataset()
    for kind in ALL_KINDS:
        remove_kind(dataset, kind)


if __name__ == '__main__':
    remove_all_entities()
