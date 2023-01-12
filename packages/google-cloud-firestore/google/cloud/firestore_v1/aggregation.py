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

from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries


from google.cloud.firestore_v1.base_aggregation import (
    AggregationResult,
    BaseAggregationQuery,
    _query_response_to_result,
)

from typing import Generator, Union, List, Any


class AggregationQuery(BaseAggregationQuery):
    """Represents an aggregation query to the Firestore API."""

    def __init__(
        self,
        nested_query,
    ) -> None:
        super(AggregationQuery, self).__init__(nested_query)

    def get(
        self,
        transaction=None,
        retry: Union[
            retries.Retry, None, gapic_v1.method._MethodDefault
        ] = gapic_v1.method.DEFAULT,
        timeout: float | None = None,
    ) -> List[AggregationResult]:
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
        result = self.stream(transaction=transaction, retry=retry, timeout=timeout)
        return list(result)  # type: ignore

    def _get_stream_iterator(self, transaction, retry, timeout):
        """Helper method for :meth:`stream`."""
        request, kwargs = self._prep_stream(
            transaction,
            retry,
            timeout,
        )

        return self._client._firestore_api.run_aggregation_query(
            request=request,
            metadata=self._client._rpc_metadata,
            **kwargs,
        )

    def _retry_query_after_exception(self, exc, retry, transaction):
        """Helper method for :meth:`stream`."""
        if transaction is None:  # no snapshot-based retry inside transaction
            if retry is gapic_v1.method.DEFAULT:
                transport = self._client._firestore_api._transport
                gapic_callable = transport.run_aggregation_query
                retry = gapic_callable._retry
            return retry._predicate(exc)

        return False

    def stream(
        self,
        transaction=None,
        retry: Union[
            retries.Retry, None, gapic_v1.method._MethodDefault
        ] = gapic_v1.method.DEFAULT,
        timeout: float | None = None,
    ) -> Union[Generator[List[AggregationResult], Any, None]]:
        """Runs the aggregation query.

        This sends a ``RunAggregationQuery`` RPC and then returns an iterator which
        consumes each document returned in the stream of ``RunAggregationQueryResponse``
        messages.

        If a ``transaction`` is used and it already has write operations
        added, this method cannot be used (i.e. read-after-write is not
        allowed).

        Args:
            transaction
                (Optional[:class:`~google.cloud.firestore_v1.transaction.Transaction`]):
                An existing transaction that this query will run in.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.  Defaults to a system-specified policy.
            timeout (float): The timeout for this request.  Defaults to a
                system-specified value.

        Yields:
            :class:`~google.cloud.firestore_v1.base_aggregation.AggregationResult`:
            The result of aggregations of this query
        """

        response_iterator = self._get_stream_iterator(
            transaction,
            retry,
            timeout,
        )
        while True:
            try:
                response = next(response_iterator, None)
            except exceptions.GoogleAPICallError as exc:
                if self._retry_query_after_exception(exc, retry, transaction):
                    response_iterator = self._get_stream_iterator(
                        transaction,
                        retry,
                        timeout,
                    )
                    continue
                else:
                    raise

            if response is None:  # EOI
                break
            result = _query_response_to_result(response)
            yield result
