# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Translate NDB queries to Datastore calls."""

import functools
import heapq
import itertools
import logging

from google.cloud.datastore_v1.proto import datastore_pb2
from google.cloud.datastore_v1.proto import entity_pb2
from google.cloud.datastore_v1.proto import query_pb2
from google.cloud.datastore import helpers

from google.cloud.ndb import context as context_module
from google.cloud.ndb import _datastore_api
from google.cloud.ndb import model
from google.cloud.ndb import tasklets

log = logging.getLogger(__name__)

MoreResultsType = query_pb2.QueryResultBatch.MoreResultsType
MORE_RESULTS_TYPE_NOT_FINISHED = MoreResultsType.Value("NOT_FINISHED")

ResultType = query_pb2.EntityResult.ResultType
RESULT_TYPE_FULL = ResultType.Value("FULL")
RESULT_TYPE_PROJECTION = ResultType.Value("PROJECTION")

DOWN = query_pb2.PropertyOrder.DESCENDING
UP = query_pb2.PropertyOrder.ASCENDING

FILTER_OPERATORS = {
    "=": query_pb2.PropertyFilter.EQUAL,
    "<": query_pb2.PropertyFilter.LESS_THAN,
    "<=": query_pb2.PropertyFilter.LESS_THAN_OR_EQUAL,
    ">": query_pb2.PropertyFilter.GREATER_THAN,
    ">=": query_pb2.PropertyFilter.GREATER_THAN_OR_EQUAL,
}


def make_filter(name, op, value):
    """Make a property filter protocol buffer.

    Args:
        name (str): The name of the property to filter by.
        op (str): The operator to apply in the filter. Must be one of "=", "<",
            "<=", ">", or ">=".
        value (Any): The value for comparison.

    Returns:
        query_pb2.PropertyFilter: The filter protocol buffer.
    """
    filter_pb = query_pb2.PropertyFilter(
        property=query_pb2.PropertyReference(name=name),
        op=FILTER_OPERATORS[op],
    )
    helpers._set_protobuf_value(filter_pb.value, value)
    return filter_pb


def make_composite_and_filter(filter_pbs):
    """Make a composite filter protocol buffer using AND.

    Args:
        List[Union[query_pb2.PropertyFilter, query_pb2.CompositeFilter]]: The
            list of filters to be combined.

    Returns:
        query_pb2.CompositeFilter: The new composite filter.
    """
    return query_pb2.CompositeFilter(
        op=query_pb2.CompositeFilter.AND,
        filters=[_filter_pb(filter_pb) for filter_pb in filter_pbs],
    )


@tasklets.tasklet
def fetch(query):
    """Fetch query results.

    Args:
        query (query.Query): The query.

    Returns:
        tasklets.Future: Result is List[model.Model]: The query results.
    """
    client = context_module.get_context().client

    project_id = query.project
    if not project_id:
        project_id = client.project

    namespace = query.namespace
    if not namespace:
        namespace = client.namespace

    filter_pbs = (None,)
    if query.filters:
        filter_pbs = query.filters._to_filter()
        if not isinstance(filter_pbs, (tuple, list)):
            filter_pbs = (filter_pbs,)

    queries = [
        _run_query(project_id, namespace, _query_to_protobuf(query, filter_pb))
        for filter_pb in filter_pbs
    ]
    result_sets = yield queries
    result_sets = [
        [
            _Result(result_type, result_pb, query.order_by)
            for result_type, result_pb in result_set
        ]
        for result_set in result_sets
    ]

    if len(result_sets) > 1:
        sortable = bool(query.order_by)
        results = _merge_results(result_sets, sortable)
    else:
        results = result_sets[0]

    return [result.entity(query.projection) for result in results]


@functools.total_ordering
class _Result:
    """A single, sortable query result.

    Args:
        result_type (query_pb2.EntityResult.ResultType): The type of result.
        result_pb (query_pb2.EntityResult): Protocol buffer result.
        order_by (Optional[Sequence[query.PropertyOrder]]): Ordering for the
            query. Used to merge sorted result sets while maintaining sort
            order.
    """

    def __init__(self, result_type, result_pb, order_by=None):
        self.result_type = result_type
        self.result_pb = result_pb
        self.order_by = order_by

    def __lt__(self, other):
        """For total ordering. """
        return self._compare(other) == -1

    def __eq__(self, other):
        """For total ordering. """
        if isinstance(other, _Result) and self.result_pb == other.result_pb:
            return True

        return self._compare(other) == 0

    def _compare(self, other):
        """Compare this result to another result for sorting.

        Args:
            other (_Result): The other result to compare to.

        Returns:
            int: :data:`-1` if this result should come before `other`,
                :data:`0` if this result is equivalent to `other` for sorting
                purposes, or :data:`1` if this result should come after
                `other`.

        Raises:
            NotImplemented: If `order_by` was not passed to constructor or is
                :data:`None` or is empty.
            NotImplemented: If `other` is not a `_Result`.
        """
        if not self.order_by:
            raise NotImplementedError("Can't sort result set without order_by")

        if not isinstance(other, _Result):
            return NotImplemented

        for order in self.order_by:
            this_value_pb = self.result_pb.entity.properties[order.name]
            this_value = helpers._get_value_from_value_pb(this_value_pb)
            other_value_pb = other.result_pb.entity.properties[order.name]
            other_value = helpers._get_value_from_value_pb(other_value_pb)

            direction = -1 if order.reverse else 1

            if this_value < other_value:
                return -direction

            elif this_value > other_value:
                return direction

        return 0

    def entity(self, projection=None):
        """Get an entity for an entity result.

        Args:
            projection (Optional[Sequence[str]]): Sequence of property names to
                be projected in the query results.

        Returns:
            Union[model.Model, key.Key]: The processed result.
        """
        entity = model._entity_from_protobuf(self.result_pb.entity)

        if self.result_type == RESULT_TYPE_FULL:
            return entity

        elif self.result_type == RESULT_TYPE_PROJECTION:
            entity._set_projection(projection)
            return entity

        raise NotImplementedError(
            "Got unexpected key only entity result for query."
        )


def _merge_results(result_sets, sortable):
    """Merge the results of distinct queries.

    Some queries that in NDB are logically a single query have to be broken
    up into two or more Datastore queries, because Datastore doesn't have a
    composite filter with a boolean OR. The `results` are the result sets from
    two or more queries which logically form a composite query joined by OR.
    The individual result sets are combined into a single result set,
    consolidating any results which may be common to two or more result sets.

    Args:
        result_sets (Sequence[_Result]): List of individual result sets as
            returned by :func:`_run_query`. These are merged into the final
            result.
        sort (bool): Whether the results are sortable. Will depend on whether
            the query that produced them had `order_by`.

    Returns:
        Sequence[_Result]: The merged result set.
    """
    seen_keys = set()
    if sortable:
        results = heapq.merge(*result_sets)
    else:
        results = itertools.chain(*result_sets)

    for result in results:
        hash_key = result.result_pb.entity.key.SerializeToString()
        if hash_key in seen_keys:
            continue

        seen_keys.add(hash_key)
        yield result


def _query_to_protobuf(query, filter_pb=None):
    """Convert an NDB query to a Datastore protocol buffer.

    Args:
        query (query.Query): The query.
        filter_pb (Optional[query_pb2.Filter]): The filter to apply for this
        query.

    Returns:
        query_pb2.Query: The protocol buffer representation of the query.
    """
    query_args = {}
    if query.kind:
        query_args["kind"] = [query_pb2.KindExpression(name=query.kind)]

    if query.projection:
        query_args["projection"] = [
            query_pb2.Projection(
                property=query_pb2.PropertyReference(name=name)
            )
            for name in query.projection
        ]

    if query.distinct_on:
        query_args["distinct_on"] = [
            query_pb2.PropertyReference(name=name)
            for name in query.distinct_on
        ]

    if query.order_by:
        query_args["order"] = [
            query_pb2.PropertyOrder(
                property=query_pb2.PropertyReference(name=order.name),
                direction=DOWN if order.reverse else UP,
            )
            for order in query.order_by
        ]

    if query.ancestor:
        ancestor_pb = query.ancestor._key.to_protobuf()
        ancestor_filter_pb = query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="__key__"),
            op=query_pb2.PropertyFilter.HAS_ANCESTOR,
        )
        ancestor_filter_pb.value.key_value.CopyFrom(ancestor_pb)

        if filter_pb is None:
            filter_pb = ancestor_filter_pb

        elif isinstance(filter_pb, query_pb2.CompositeFilter):
            filter_pb.filters.add(property_filter=ancestor_filter_pb)

        else:
            filter_pb = query_pb2.CompositeFilter(
                op=query_pb2.CompositeFilter.AND,
                filters=[
                    _filter_pb(filter_pb),
                    _filter_pb(ancestor_filter_pb),
                ],
            )

    if filter_pb is not None:
        query_args["filter"] = _filter_pb(filter_pb)

    return query_pb2.Query(**query_args)


def _filter_pb(filter_pb):
    """Convenience function to compose a filter protocol buffer.

    The Datastore protocol uses a Filter message which has one of either a
    PropertyFilter or CompositeFilter as a sole attribute.

    Args:
        filter_pb (Union[query_pb2.CompositeFilter, query_pb2.PropertyFilter]):
            The actual filter.

    Returns:
        query_pb2.Filter: The filter at the higher level of abstraction
            required to use it in a query.
    """
    if isinstance(filter_pb, query_pb2.CompositeFilter):
        return query_pb2.Filter(composite_filter=filter_pb)

    return query_pb2.Filter(property_filter=filter_pb)


@tasklets.tasklet
def _run_query(project_id, namespace, query_pb):
    """Run a query in Datastore.

    Will potentially repeat the query to get all results.

    Args:
        project_id (str): The project/app id of the Datastore instance.
        namespace (str): The namespace to which to restrict results.
        query_pb (query_pb2.Query): The query protocol buffer representation.

    Returns:
        tasklets.Future: List[Tuple[query_pb2.EntityResult.ResultType,
            query_pb2.EntityResult]]: The raw query results.
    """
    results = []
    partition_id = entity_pb2.PartitionId(
        project_id=project_id, namespace_id=namespace
    )

    while True:
        # See what results we get from the backend
        request = datastore_pb2.RunQueryRequest(
            project_id=project_id, partition_id=partition_id, query=query_pb
        )
        response = yield _datastore_api.make_call("RunQuery", request)
        log.debug(response)

        batch = response.batch
        results.extend(
            (
                (batch.entity_result_type, result)
                for result in batch.entity_results
            )
        )

        # Did we get all of them?
        if batch.more_results != MORE_RESULTS_TYPE_NOT_FINISHED:
            break

        # Still some results left to fetch. Update cursors and try again.
        query_pb.start_cursor = batch.end_cursor

    return results
