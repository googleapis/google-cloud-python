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

import abc
from abc import ABC
from enum import Enum
from typing import Iterable, Optional, Tuple, Union

from google.api_core import gapic_v1
from google.api_core import retry as retries

from google.cloud.firestore_v1 import _helpers, document
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.types import query
from google.cloud.firestore_v1.vector import Vector


class DistanceMeasure(Enum):
    EUCLIDEAN = 1
    COSINE = 2
    DOT_PRODUCT = 3


class BaseVectorQuery(ABC):
    """Represents a vector query to the Firestore API."""

    def __init__(self, nested_query) -> None:
        self._nested_query = nested_query
        self._collection_ref = nested_query._parent
        self._vector_field: Optional[str] = None
        self._query_vector: Optional[Vector] = None
        self._limit: Optional[int] = None
        self._distance_measure: Optional[DistanceMeasure] = None

    @property
    def _client(self):
        return self._collection_ref._client

    def _to_protobuf(self) -> query.StructuredQuery:
        pb = query.StructuredQuery()

        distance_measure_proto = None
        if self._distance_measure == DistanceMeasure.EUCLIDEAN:
            distance_measure_proto = (
                query.StructuredQuery.FindNearest.DistanceMeasure.EUCLIDEAN
            )
        elif self._distance_measure == DistanceMeasure.COSINE:
            distance_measure_proto = (
                query.StructuredQuery.FindNearest.DistanceMeasure.COSINE
            )
        elif self._distance_measure == DistanceMeasure.DOT_PRODUCT:
            distance_measure_proto = (
                query.StructuredQuery.FindNearest.DistanceMeasure.DOT_PRODUCT
            )
        else:
            raise ValueError("Invalid distance_measure")

        pb = self._nested_query._to_protobuf()
        pb.find_nearest = query.StructuredQuery.FindNearest(
            vector_field=query.StructuredQuery.FieldReference(
                field_path=self._vector_field
            ),
            query_vector=_helpers.encode_value(self._query_vector),
            distance_measure=distance_measure_proto,
            limit=self._limit,
        )
        return pb

    def _prep_stream(
        self,
        transaction=None,
        retry: Union[retries.Retry, None, gapic_v1.method._MethodDefault] = None,
        timeout: Optional[float] = None,
    ) -> Tuple[dict, str, dict]:
        parent_path, expected_prefix = self._collection_ref._parent_info()
        request = {
            "parent": parent_path,
            "structured_query": self._to_protobuf(),
            "transaction": _helpers.get_transaction_id(transaction),
        }
        kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

        return request, expected_prefix, kwargs

    @abc.abstractmethod
    def get(
        self,
        transaction=None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: Optional[float] = None,
    ) -> Iterable[DocumentSnapshot]:
        """Runs the vector query."""

    def find_nearest(
        self,
        vector_field: str,
        query_vector: Vector,
        limit: int,
        distance_measure: DistanceMeasure,
    ):
        """Finds the closest vector embeddings to the given query vector."""
        self._vector_field = vector_field
        self._query_vector = query_vector
        self._limit = limit
        self._distance_measure = distance_measure
        return self

    def stream(
        self,
        transaction=None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
    ) -> Iterable[document.DocumentSnapshot]:
        """Reads the documents in the collection that match this query."""
