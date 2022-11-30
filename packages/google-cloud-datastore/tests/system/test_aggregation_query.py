# Copyright 2022 Google LLC
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


def _make_iterator(aggregation_query, **kw):
    # Do retry for errors raised during initial API call
    return retry_503(aggregation_query.fetch)(**kw)


def _pull_iterator(aggregation_query, **kw):
    return list(_make_iterator(aggregation_query, **kw))


def _do_fetch(aggregation_query, **kw):
    # Do retry for errors raised during iteration
    return retry_503(_pull_iterator)(aggregation_query, **kw)


@pytest.fixture(scope="session")
def aggregation_query_client(datastore_client):
    return _helpers.clone_client(datastore_client, namespace=None)


@pytest.fixture(scope="session")
def ancestor_key(aggregation_query_client, in_emulator):

    # In the emulator, re-populating the datastore is cheap.
    if in_emulator:
        populate_datastore.add_characters(client=aggregation_query_client)

    ancestor_key = aggregation_query_client.key(*populate_datastore.ANCESTOR)

    yield ancestor_key

    # In the emulator, destroy the query entities.
    if in_emulator:
        clear_datastore.remove_all_entities(client=aggregation_query_client)


def _make_query(aggregation_query_client, ancestor_key):
    return aggregation_query_client.query(kind="Character", ancestor=ancestor_key)


@pytest.fixture(scope="function")
def nested_query(aggregation_query_client, ancestor_key):
    return _make_query(aggregation_query_client, ancestor_key)


def test_aggregation_query_default(aggregation_query_client, nested_query):
    query = nested_query

    aggregation_query = aggregation_query_client.aggregation_query(query)
    aggregation_query.count()
    result = _do_fetch(aggregation_query)
    assert len(result) == 1
    for r in result[0]:
        assert r.alias == "property_1"
        assert r.value == 8


def test_aggregation_query_with_alias(aggregation_query_client, nested_query):
    query = nested_query

    aggregation_query = aggregation_query_client.aggregation_query(query)
    aggregation_query.count(alias="total")
    result = _do_fetch(aggregation_query)
    assert len(result) == 1
    for r in result[0]:
        assert r.alias == "total"
        assert r.value > 0


def test_aggregation_query_with_limit(aggregation_query_client, nested_query):
    query = nested_query

    aggregation_query = aggregation_query_client.aggregation_query(query)
    aggregation_query.count(alias="total")
    result = _do_fetch(aggregation_query)  # count without limit
    assert len(result) == 1
    for r in result[0]:
        assert r.alias == "total"
        assert r.value == 8

    aggregation_query = aggregation_query_client.aggregation_query(query)
    aggregation_query.count(alias="total_up_to")
    result = _do_fetch(aggregation_query, limit=2)  # count with limit = 2
    assert len(result) == 1
    for r in result[0]:
        assert r.alias == "total_up_to"
        assert r.value == 2


def test_aggregation_query_multiple_aggregations(
    aggregation_query_client, nested_query
):
    query = nested_query

    aggregation_query = aggregation_query_client.aggregation_query(query)
    aggregation_query.count(alias="total")
    aggregation_query.count(alias="all")
    result = _do_fetch(aggregation_query)
    assert len(result) == 1
    for r in result[0]:
        assert r.alias in ["all", "total"]
        assert r.value > 0


def test_aggregation_query_add_aggregation(aggregation_query_client, nested_query):
    from google.cloud.datastore.aggregation import CountAggregation

    query = nested_query

    aggregation_query = aggregation_query_client.aggregation_query(query)
    count_aggregation = CountAggregation(alias="total")
    aggregation_query.add_aggregation(count_aggregation)
    result = _do_fetch(aggregation_query)
    assert len(result) == 1
    for r in result[0]:
        assert r.alias == "total"
        assert r.value > 0


def test_aggregation_query_add_aggregations(aggregation_query_client, nested_query):
    from google.cloud.datastore.aggregation import CountAggregation

    query = nested_query

    aggregation_query = aggregation_query_client.aggregation_query(query)
    count_aggregation_1 = CountAggregation(alias="total")
    count_aggregation_2 = CountAggregation(alias="all")
    aggregation_query.add_aggregations([count_aggregation_1, count_aggregation_2])
    result = _do_fetch(aggregation_query)
    assert len(result) == 1
    for r in result[0]:
        assert r.alias in ["total", "all"]
        assert r.value > 0


def test_aggregation_query_add_aggregations_duplicated_alias(
    aggregation_query_client, nested_query
):
    from google.cloud.datastore.aggregation import CountAggregation
    from google.api_core.exceptions import BadRequest

    query = nested_query

    aggregation_query = aggregation_query_client.aggregation_query(query)
    count_aggregation_1 = CountAggregation(alias="total")
    count_aggregation_2 = CountAggregation(alias="total")
    aggregation_query.add_aggregations([count_aggregation_1, count_aggregation_2])
    with pytest.raises(BadRequest):
        _do_fetch(aggregation_query)

    aggregation_query = aggregation_query_client.aggregation_query(query)
    aggregation_query.add_aggregation(count_aggregation_1)
    aggregation_query.add_aggregation(count_aggregation_2)
    with pytest.raises(BadRequest):
        _do_fetch(aggregation_query)

    aggregation_query = aggregation_query_client.aggregation_query(query)
    aggregation_query.count(alias="total")
    aggregation_query.count(alias="total")
    with pytest.raises(BadRequest):
        _do_fetch(aggregation_query)


def test_aggregation_query_with_nested_query_filtered(
    aggregation_query_client, nested_query
):
    query = nested_query

    query.add_filter("appearances", ">=", 20)
    expected_matches = 6

    # We expect 6, but allow the query to get 1 extra.
    entities = _do_fetch(query, limit=expected_matches + 1)

    assert len(entities) == expected_matches

    aggregation_query = aggregation_query_client.aggregation_query(query)
    aggregation_query.count(alias="total")
    result = _do_fetch(aggregation_query)
    assert len(result) == 1

    for r in result[0]:
        assert r.alias == "total"
        assert r.value == 6


def test_aggregation_query_with_nested_query_multiple_filters(
    aggregation_query_client, nested_query
):
    query = nested_query

    query.add_filter("appearances", ">=", 26)
    query = query.add_filter("family", "=", "Stark")
    expected_matches = 4

    # We expect 4, but allow the query to get 1 extra.
    entities = _do_fetch(query, limit=expected_matches + 1)

    assert len(entities) == expected_matches

    aggregation_query = aggregation_query_client.aggregation_query(query)
    aggregation_query.count(alias="total")
    result = _do_fetch(aggregation_query)
    assert len(result) == 1

    for r in result[0]:
        assert r.alias == "total"
        assert r.value == 4
