# Copyright 2024 Google LLC All rights reserved.
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

"""Classes for representing vector queries for the Google Cloud Firestore API.
"""

from google.cloud.firestore_v1.base_vector_query import BaseVectorQuery
from typing import Iterable, Optional, TypeVar, Union
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1 import document
from google.cloud.firestore_v1.base_query import (
    BaseQuery,
    _query_response_to_snapshot,
    _collection_group_query_response_to_snapshot,
)

TVectorQuery = TypeVar("TVectorQuery", bound="VectorQuery")


class VectorQuery(BaseVectorQuery):
    """Represents a vector query to the Firestore API."""

    def __init__(
        self,
        nested_query: Union[BaseQuery, TVectorQuery],
    ) -> None:
        """Presents the vector query.
        Args:
            nested_query (BaseQuery | VectorQuery): the base query to apply as the prefilter.
        """
        super(VectorQuery, self).__init__(nested_query)

    def get(
        self,
        transaction=None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: Optional[float] = None,
    ) -> Iterable[DocumentSnapshot]:
        """Runs the vector query.

        This sends a ``RunQuery`` RPC and returns a list of document messages.

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
            list: The vector query results.
        """
        result = self.stream(transaction=transaction, retry=retry, timeout=timeout)

        return list(result)

    def _get_stream_iterator(self, transaction, retry, timeout):
        """Helper method for :meth:`stream`."""
        request, expected_prefix, kwargs = self._prep_stream(
            transaction,
            retry,
            timeout,
        )

        response_iterator = self._client._firestore_api.run_query(
            request=request,
            metadata=self._client._rpc_metadata,
            **kwargs,
        )

        return response_iterator, expected_prefix

    def stream(
        self,
        transaction=None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
    ) -> Iterable[document.DocumentSnapshot]:
        """Reads the documents in the collection that match this query.

        This sends a ``RunQuery`` RPC and then returns an iterator which
        consumes each document returned in the stream of ``RunQueryResponse``
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
            :class:`~google.cloud.firestore_v1.document.DocumentSnapshot`:
            The next document that fulfills the query.
        """
        response_iterator, expected_prefix = self._get_stream_iterator(
            transaction,
            retry,
            timeout,
        )

        while True:
            response = next(response_iterator, None)

            if response is None:  # EOI
                break

            if self._nested_query._all_descendants:
                snapshot = _collection_group_query_response_to_snapshot(
                    response, self._nested_query._parent
                )
            else:
                snapshot = _query_response_to_snapshot(
                    response, self._nested_query._parent, expected_prefix
                )
            if snapshot is not None:
                yield snapshot
