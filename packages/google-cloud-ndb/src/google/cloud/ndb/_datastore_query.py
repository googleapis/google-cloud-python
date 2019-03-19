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

from google.cloud.datastore_v1.proto import datastore_pb2
from google.cloud.datastore_v1.proto import query_pb2

from google.cloud.ndb import context as context_module
from google.cloud.ndb import _datastore_api
from google.cloud.ndb import model
from google.cloud.ndb import tasklets

MoreResultsType = query_pb2.QueryResultBatch.MoreResultsType
MORE_RESULTS_TYPE_NOT_FINISHED = MoreResultsType.Value("NOT_FINISHED")
ResultType = query_pb2.EntityResult.ResultType
RESULT_TYPE_FULL = ResultType.Value("FULL")


@tasklets.tasklet
def fetch(query):
    """Fetch query results.

    Args:
        query (query.Query): The query.

    Returns:
        tasklets.Future: Result is List[model.Model]: The query results.
    """
    for name in (
        "ancestor",
        "filters",
        "orders",
        "app",
        "namespace",
        "default_options",
        "projection",
        "group_by",
    ):
        if getattr(query, name, None):
            raise NotImplementedError(
                "{} is not yet implemented for queries.".format(name)
            )

    query_pb = _query_to_protobuf(query)
    results = yield _run_query(query_pb)
    return [
        _process_result(result_type, result) for result_type, result in results
    ]


def _process_result(result_type, result):
    """Process a single entity result.

    Args:
        result_type (query_pb2.EntityResult.ResultType): The type of the result
            (full entity, projection, or key only).
        result (query_pb2.EntityResult): The protocol buffer representation of
            the query result.

    Returns:
        Union[model.Model, key.Key]: The processed result.
    """
    if result_type == RESULT_TYPE_FULL:
        return model._entity_from_protobuf(result.entity)

    raise NotImplementedError(
        "Processing for projection and key only entity results is not yet "
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

    return query_pb2.Query(**query_args)


@tasklets.tasklet
def _run_query(query_pb):
    """Run a query in Datastore.

    Will potentially repeat the query to get all results.

    Args:
        query_pb (query_pb2.Query): The query protocol buffer representation.

    Returns:
        tasklets.Future: List[Tuple[query_pb2.EntityResult.ResultType,
            query_pb2.EntityResult]]: The raw query results.
    """
    client = context_module.get_context().client
    results = []

    while True:
        # See what results we get from the backend
        request = datastore_pb2.RunQueryRequest(
            project_id=client.project, query=query_pb
        )
        response = yield _datastore_api.make_call("RunQuery", request)
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
