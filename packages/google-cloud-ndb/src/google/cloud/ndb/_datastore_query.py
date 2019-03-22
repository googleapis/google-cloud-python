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

import logging

from google.cloud.datastore_v1.proto import datastore_pb2
from google.cloud.datastore_v1.proto import entity_pb2
from google.cloud.datastore_v1.proto import query_pb2

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


@tasklets.tasklet
def fetch(query):
    """Fetch query results.

    Args:
        query (query.Query): The query.

    Returns:
        tasklets.Future: Result is List[model.Model]: The query results.
    """
    for name in ("filters", "orders", "default_options"):
        if getattr(query, name, None):
            raise NotImplementedError(
                "{} is not yet implemented for queries.".format(name)
            )

    client = context_module.get_context().client

    project_id = query.app
    if not project_id:
        project_id = client.project

    namespace = query.namespace
    if not namespace:
        namespace = client.namespace

    query_pb = _query_to_protobuf(query)
    results = yield _run_query(project_id, namespace, query_pb)
    return [
        _process_result(result_type, result, query.projection)
        for result_type, result in results
    ]


def _process_result(result_type, result, projection):
    """Process a single entity result.

    Args:
        result_type (query_pb2.EntityResult.ResultType): The type of the result
            (full entity, projection, or key only).
        result (query_pb2.EntityResult): The protocol buffer representation of
            the query result.
        projection (Union[list, tuple]): Sequence of property names to be
            projected in the query results.

    Returns:
        Union[model.Model, key.Key]: The processed result.
    """
    entity = model._entity_from_protobuf(result.entity)

    if result_type == RESULT_TYPE_FULL:
        return entity

    elif result_type == RESULT_TYPE_PROJECTION:
        entity._set_projection(projection)
        return entity

    raise NotImplementedError(
        "Processing for key only entity results is not yet "
        "implemented for queries."
    )


def _query_to_protobuf(query):
    """Convert an NDB query to a Datastore protocol buffer.

    Args:
        query (query.Query): The query.

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

    filters = []
    if query.ancestor:
        ancestor_pb = query.ancestor._key.to_protobuf()
        filter_pb = query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="__key__"),
            op=query_pb2.PropertyFilter.HAS_ANCESTOR,
        )
        filter_pb.value.key_value.CopyFrom(ancestor_pb)
        filters.append(filter_pb)

    if len(filters) == 1:
        query_args["filter"] = query_pb2.Filter(property_filter=filters[0])

    return query_pb2.Query(**query_args)


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
