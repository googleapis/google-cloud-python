# Copyright 2011 Google LLC
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

import pytest

from google.api_core import exceptions
from test_utils.retry import RetryErrors

from .utils import clear_datastore
from .utils import populate_datastore
from . import _helpers


retry_503 = RetryErrors(exceptions.ServiceUnavailable)


def _make_iterator(query, **kw):
    # Do retry for errors raised during initial API call
    return retry_503(query.fetch)(**kw)


def _pull_iterator(query, **kw):
    return list(_make_iterator(query, **kw))


def _do_fetch(query, **kw):
    # Do retry for errors raised during iteration
    return retry_503(_pull_iterator)(query, **kw)


@pytest.fixture(scope="session")
def query_client(datastore_client):
    return _helpers.clone_client(datastore_client, namespace=None)


@pytest.fixture(scope="session")
def ancestor_key(query_client, in_emulator):

    # In the emulator, re-populating the datastore is cheap.
    if in_emulator:
        populate_datastore.add_characters(client=query_client)

    ancestor_key = query_client.key(*populate_datastore.ANCESTOR)

    yield ancestor_key

    # In the emulator, destroy the query entities.
    if in_emulator:
        clear_datastore.remove_all_entities(client=query_client)


def _make_ancestor_query(query_client, ancestor_key):
    return query_client.query(kind="Character", ancestor=ancestor_key)


@pytest.fixture(scope="function")
def ancestor_query(query_client, ancestor_key):
    return _make_ancestor_query(query_client, ancestor_key)


def test_query_w_ancestor(ancestor_query):
    query = ancestor_query
    expected_matches = 8

    # We expect 8, but allow the query to get 1 extra.
    entities = _do_fetch(query, limit=expected_matches + 1)

    assert len(entities) == expected_matches


def test_query_w_limit_paging(ancestor_query):
    query = ancestor_query
    limit = 5

    # Fetch characters.
    iterator = query.fetch(limit=limit)
    page = next(iterator.pages)
    character_entities = list(page)
    cursor = iterator.next_page_token
    assert len(character_entities) == limit

    # Check cursor after fetch.
    assert cursor is not None

    # Fetch remaining characters.
    new_character_entities = _do_fetch(query, start_cursor=cursor)
    characters_remaining = len(populate_datastore.CHARACTERS) - limit
    assert len(new_character_entities) == characters_remaining


def test_query_w_simple_filter(ancestor_query):
    query = ancestor_query
    query.add_filter("appearances", ">=", 20)
    expected_matches = 6

    # We expect 6, but allow the query to get 1 extra.
    entities = _do_fetch(query, limit=expected_matches + 1)

    assert len(entities) == expected_matches


def test_query_w_multiple_filters(ancestor_query):
    query = ancestor_query
    query.add_filter("appearances", ">=", 26)
    query = query.add_filter("family", "=", "Stark")
    expected_matches = 4

    # We expect 4, but allow the query to get 1 extra.
    entities = _do_fetch(query, limit=expected_matches + 1)

    assert len(entities) == expected_matches


def test_query_key_filter(query_client, ancestor_query):
    # Use the client for this test instead of the global.
    query = ancestor_query
    rickard_key = query_client.key(*populate_datastore.RICKARD)
    query.key_filter(rickard_key)
    expected_matches = 1

    # We expect 1, but allow the query to get 1 extra.
    entities = _do_fetch(query, limit=expected_matches + 1)

    assert len(entities) == expected_matches


def test_query_w_order(ancestor_query):
    query = ancestor_query
    query.order = "appearances"
    expected_matches = 8

    # We expect 8, but allow the query to get 1 extra.
    entities = _do_fetch(query, limit=expected_matches + 1)

    assert len(entities) == expected_matches

    # Actually check the ordered data returned.
    assert entities[0]["name"] == populate_datastore.CHARACTERS[0]["name"]
    assert entities[7]["name"] == populate_datastore.CHARACTERS[3]["name"]


def test_query_w_projection(ancestor_query):
    filtered_query = ancestor_query
    filtered_query.projection = ["name", "family"]
    filtered_query.order = ["name", "family"]

    # NOTE: There are 9 responses because of Catelyn. She has both
    #       Stark and Tully as her families, hence occurs twice in
    #       the results.
    expected_matches = 9

    # We expect 9, but allow the query to get 1 extra.
    entities = list(filtered_query.fetch(limit=expected_matches + 1))
    assert len(entities) == expected_matches

    arya_entity = entities[0]
    catelyn_stark_entity = entities[2]
    catelyn_tully_entity = entities[3]
    sansa_entity = entities[8]

    assert dict(arya_entity) == {"name": "Arya", "family": "Stark"}

    # Check both Catelyn keys are the same.
    assert catelyn_stark_entity.key == catelyn_tully_entity.key
    assert dict(catelyn_stark_entity) == {"name": "Catelyn", "family": "Stark"}
    assert dict(catelyn_tully_entity) == {"name": "Catelyn", "family": "Tully"}

    assert dict(sansa_entity) == {"name": "Sansa", "family": "Stark"}


def test_query_w_paginate_simple_uuid_keys(query_client):

    # See issue #4264
    page_query = query_client.query(kind="uuid_key")
    iterator = page_query.fetch()
    seen = set()
    page_count = 0

    for page in iterator.pages:
        page_count += 1
        for entity in page:
            uuid_str = entity.key.name
            assert uuid_str not in seen
            seen.add(uuid_str)

    assert page_count > 1


def test_query_paginate_simple_timestamp_keys(query_client):

    # See issue #4264
    page_query = query_client.query(kind="timestamp_key")
    iterator = page_query.fetch()
    seen = set()
    page_count = 0

    for page in iterator.pages:
        page_count += 1
        for entity in page:
            timestamp = entity.key.id
            assert timestamp not in seen
            seen.add(timestamp)

    assert page_count > 1


def test_query_w_offset_w_timestamp_keys(query_client):
    # See issue #4675
    max_all = 10000
    offset = 1
    max_offset = max_all - offset
    query = query_client.query(kind="timestamp_key")

    all_w_limit = _do_fetch(query, limit=max_all)
    assert len(all_w_limit) == max_all

    offset_w_limit = _do_fetch(query, offset=offset, limit=max_offset)
    assert offset_w_limit == all_w_limit[offset:]


def test_query_paginate_with_offset(ancestor_query):
    page_query = ancestor_query
    page_query.order = "appearances"
    offset = 2
    limit = 3

    iterator = page_query.fetch(limit=limit, offset=offset)

    # Fetch characters.
    page = next(iterator.pages)
    entities = list(page)
    assert len(entities) == limit
    assert entities[0]["name"] == "Robb"
    assert entities[1]["name"] == "Bran"
    assert entities[2]["name"] == "Catelyn"

    cursor = iterator.next_page_token

    # Fetch next set of characters.
    new_iterator = page_query.fetch(limit=limit, offset=0, start_cursor=cursor)

    entities = list(new_iterator)
    assert len(entities) == limit
    assert entities[0]["name"] == "Sansa"
    assert entities[1]["name"] == "Jon Snow"
    assert entities[2]["name"] == "Arya"


def test_query_paginate_with_start_cursor(query_client, ancestor_key):
    # Don't use fixture, because we need to create a clean copy later.
    page_query = _make_ancestor_query(query_client, ancestor_key)
    page_query.order = "appearances"
    limit = 3
    offset = 2

    iterator = page_query.fetch(limit=limit, offset=offset)

    # Fetch characters.
    page = next(iterator.pages)
    entities = list(page)
    assert len(entities) == limit

    cursor = iterator.next_page_token

    # Use cursor to create a fresh query.
    fresh_query = _make_ancestor_query(query_client, ancestor_key)
    fresh_query.order = "appearances"

    new_entities = list(fresh_query.fetch(start_cursor=cursor, limit=limit))

    characters_remaining = len(populate_datastore.CHARACTERS) - limit - offset
    assert len(new_entities) == characters_remaining
    assert new_entities[0]["name"] == "Sansa"
    assert new_entities[2]["name"] == "Arya"


def test_query_distinct_on(ancestor_query):
    query = ancestor_query
    query.distinct_on = ["alive"]
    expected_matches = 2

    # We expect 2, but allow the query to get 1 extra.
    entities = _do_fetch(query, limit=expected_matches + 1)

    assert len(entities) == expected_matches
    assert entities[0]["name"] == "Catelyn"
    assert entities[1]["name"] == "Arya"


@pytest.fixture(scope="session")
def large_query_client(datastore_client):
    large_query_client = _helpers.clone_client(
        datastore_client, namespace=populate_datastore.LARGE_CHARACTER_NAMESPACE,
    )
    # Populate the datastore if necessary.
    populate_datastore.add_large_character_entities(client=large_query_client)

    return large_query_client


@pytest.fixture(scope="function")
def large_query(large_query_client):
    # Use the client for this test instead of the global.
    return large_query_client.query(
        kind=populate_datastore.LARGE_CHARACTER_KIND,
        namespace=populate_datastore.LARGE_CHARACTER_NAMESPACE,
    )


@pytest.mark.parametrize(
    "limit,offset,expected",
    [
        # with no offset there are the correct # of results
        (None, None, populate_datastore.LARGE_CHARACTER_TOTAL_OBJECTS,),
        # with no limit there are results (offset provided)
        (None, 900, populate_datastore.LARGE_CHARACTER_TOTAL_OBJECTS - 900,),
        # Offset beyond items larger: verify 200 items found
        (200, 1100, 200,),
        # offset within range, expect 50 despite larger limit")
        (100, populate_datastore.LARGE_CHARACTER_TOTAL_OBJECTS - 50, 50),
        # Offset beyond items larger Verify no items found")
        (200, populate_datastore.LARGE_CHARACTER_TOTAL_OBJECTS + 1000, 0),
    ],
)
def test_large_query(large_query, limit, offset, expected):
    page_query = large_query
    page_query.add_filter("family", "=", "Stark")
    page_query.add_filter("alive", "=", False)

    iterator = page_query.fetch(limit=limit, offset=offset)

    entities = [e for e in iterator]
    assert len(entities) == expected
