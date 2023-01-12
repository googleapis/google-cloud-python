# Copyright 2023 Google LLC All rights reserved.
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

"""Classes for representing aggregation queries for the Google Cloud Firestore API.

A :class:`~google.cloud.firestore_v1.aggregation.AggregationQuery` can be created directly from
a :class:`~google.cloud.firestore_v1.collection.Collection` and that can be
a more common way to create an aggregation query than direct usage of the constructor.
"""


from __future__ import annotations

import abc


from abc import ABC

from typing import List, Coroutine, Union, Tuple, Generator, Any, AsyncGenerator

from google.api_core import gapic_v1
from google.api_core import retry as retries


from google.cloud.firestore_v1.types import RunAggregationQueryResponse

from google.cloud.firestore_v1.types import StructuredAggregationQuery
from google.cloud.firestore_v1 import _helpers


class AggregationResult(object):
    """
    A class representing result from Aggregation Query
    :type alias: str
    :param alias: The alias for the aggregation.
    :type value: int
    :param value: The resulting value from the aggregation.
    :type read_time:
    :param value: The resulting read_time
    """

    def __init__(self, alias: str, value: int, read_time=None):
        self.alias = alias
        self.value = value
        self.read_time = read_time

    def __repr__(self):
        return f"<Aggregation alias={self.alias}, value={self.value}, readtime={self.read_time}>"


class BaseAggregation(ABC):
    @abc.abstractmethod
    def _to_protobuf(self):
        """Convert this instance to the protobuf representation"""


class CountAggregation(BaseAggregation):
    def __init__(self, alias: str | None = None):
        self.alias = alias

    def _to_protobuf(self):
        """Convert this instance to the protobuf representation"""
        aggregation_pb = StructuredAggregationQuery.Aggregation()
        aggregation_pb.alias = self.alias
        aggregation_pb.count = StructuredAggregationQuery.Aggregation.Count()
        return aggregation_pb


def _query_response_to_result(
    response_pb: RunAggregationQueryResponse,
) -> List[AggregationResult]:
    results = [
        AggregationResult(
            alias=key,
            value=response_pb.result.aggregate_fields[key].integer_value,
            read_time=response_pb.read_time,
        )
        for key in response_pb.result.aggregate_fields.pb.keys()
    ]

    return results


class BaseAggregationQuery(ABC):
    """Represents an aggregation query to the Firestore API."""

    def __init__(
        self,
        nested_query,
    ) -> None:
        self._nested_query = nested_query
        self._collection_ref = nested_query._parent
        self._aggregations: List[BaseAggregation] = []

    @property
    def _client(self):
        return self._collection_ref._client

    def count(self, alias: str | None = None):
        """
        Adds a count over the nested query
        """
        count_aggregation = CountAggregation(alias=alias)
        self._aggregations.append(count_aggregation)
        return self

    def add_aggregation(self, aggregation: BaseAggregation) -> None:
        """
        Adds an aggregation operation to the nested query

        :type aggregation: :class:`google.cloud.firestore_v1.aggregation.BaseAggregation`
        :param aggregation: An aggregation operation, e.g. a CountAggregation
        """
        self._aggregations.append(aggregation)

    def add_aggregations(self, aggregations: List[BaseAggregation]) -> None:
        """
        Adds a list of aggregations to the nested query

        :type aggregations: list
        :param aggregations: a list of aggregation operations
        """
        self._aggregations.extend(aggregations)

    def _to_protobuf(self) -> StructuredAggregationQuery:
        pb = StructuredAggregationQuery()
        pb.structured_query = self._nested_query._to_protobuf()

        for aggregation in self._aggregations:
            aggregation_pb = aggregation._to_protobuf()
            pb.aggregations.append(aggregation_pb)
        return pb

    def _prep_stream(
        self,
        transaction=None,
        retry: Union[retries.Retry, None, gapic_v1.method._MethodDefault] = None,
        timeout: float | None = None,
    ) -> Tuple[dict, dict]:
        parent_path, expected_prefix = self._collection_ref._parent_info()
        request = {
            "parent": parent_path,
            "structured_aggregation_query": self._to_protobuf(),
            "transaction": _helpers.get_transaction_id(transaction),
        }
        kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

        return request, kwargs

    @abc.abstractmethod
    def get(
        self,
        transaction=None,
        retry: Union[
            retries.Retry, None, gapic_v1.method._MethodDefault
        ] = gapic_v1.method.DEFAULT,
        timeout: float | None = None,
    ) -> List[AggregationResult] | Coroutine[Any, Any, List[AggregationResult]]:
        """Runs the aggregation query.

        This sends a ``RunAggregationQuery`` RPC and returns a list of aggregation results in the stream of ``RunAggregationQueryResponse`` messages.

        Args:
            transaction
                (Optional[:class:`~google.cloud.firestore_v1.transaction.Transaction`]):
                An existing transaction that this query will run in.
                If a ``transaction`` is used and it already has write operations
                added, this method cannot be used (i.e. read-after-write is not
                allowed).
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.  Defaults to a system-specified policy.
            timeout (float): The timeout for this request.  Defaults to a
                system-specified value.

        Returns:
            list: The aggregation query results

        """

    @abc.abstractmethod
    def stream(
        self,
        transaction=None,
        retry: Union[
            retries.Retry, None, gapic_v1.method._MethodDefault
        ] = gapic_v1.method.DEFAULT,
        timeout: float | None = None,
    ) -> Generator[List[AggregationResult], Any, None] | AsyncGenerator[
        List[AggregationResult], None
    ]:
        """Runs the aggregation query.

        This sends a``RunAggregationQuery`` RPC and returns an iterator in the stream of ``RunAggregationQueryResponse`` messages.

        Args:
            transaction
                (Optional[:class:`~google.cloud.firestore_v1.transaction.Transaction`]):
                An existing transaction that this query will run in.
                If a ``transaction`` is used and it already has write operations
                added, this method cannot be used (i.e. read-after-write is not
                allowed).
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.  Defaults to a system-specified policy.
            timeout (float): The timeout for this request.  Defaults to a
                system-specified value.

        Returns:
            list: The aggregation query results

        """
