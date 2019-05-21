# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

"""Wrappers for protocol buffer enum types."""

import enum


class NullValue(enum.IntEnum):
    """
    ``NullValue`` is a singleton enumeration to represent the null value for
    the ``Value`` type union.

    The JSON representation for ``NullValue`` is JSON ``null``.

    Attributes:
      NULL_VALUE (int): Null value.
    """

    NULL_VALUE = 0


class CommitRequest(object):
    class Mode(enum.IntEnum):
        """
        The modes available for commits.

        Attributes:
          MODE_UNSPECIFIED (int): Unspecified. This value must not be used.
          TRANSACTIONAL (int): Transactional: The mutations are either all applied, or none are
          applied. Learn about transactions
          `here <https://cloud.google.com/datastore/docs/concepts/transactions>`__.
          NON_TRANSACTIONAL (int): Non-transactional: The mutations may not apply as all or none.
        """

        MODE_UNSPECIFIED = 0
        TRANSACTIONAL = 1
        NON_TRANSACTIONAL = 2


class CompositeFilter(object):
    class Operator(enum.IntEnum):
        """
        A composite filter operator.

        Attributes:
          OPERATOR_UNSPECIFIED (int): Unspecified. This value must not be used.
          AND (int): The results are required to satisfy each of the combined filters.
        """

        OPERATOR_UNSPECIFIED = 0
        AND = 1


class EntityResult(object):
    class ResultType(enum.IntEnum):
        """
        Specifies what data the 'entity' field contains. A ``ResultType`` is
        either implied (for example, in ``LookupResponse.missing`` from
        ``datastore.proto``, it is always ``KEY_ONLY``) or specified by context
        (for example, in message ``QueryResultBatch``, field
        ``entity_result_type`` specifies a ``ResultType`` for all the values in
        field ``entity_results``).

        Attributes:
          RESULT_TYPE_UNSPECIFIED (int): Unspecified. This value is never used.
          FULL (int): The key and properties.
          PROJECTION (int): A projected subset of properties. The entity may have no key.
          KEY_ONLY (int): Only the key.
        """

        RESULT_TYPE_UNSPECIFIED = 0
        FULL = 1
        PROJECTION = 2
        KEY_ONLY = 3


class PropertyFilter(object):
    class Operator(enum.IntEnum):
        """
        A property filter operator.

        Attributes:
          OPERATOR_UNSPECIFIED (int): Unspecified. This value must not be used.
          LESS_THAN (int): Less than.
          LESS_THAN_OR_EQUAL (int): Less than or equal.
          GREATER_THAN (int): Greater than.
          GREATER_THAN_OR_EQUAL (int): Greater than or equal.
          EQUAL (int): Equal.
          HAS_ANCESTOR (int): Has ancestor.
        """

        OPERATOR_UNSPECIFIED = 0
        LESS_THAN = 1
        LESS_THAN_OR_EQUAL = 2
        GREATER_THAN = 3
        GREATER_THAN_OR_EQUAL = 4
        EQUAL = 5
        HAS_ANCESTOR = 11


class PropertyOrder(object):
    class Direction(enum.IntEnum):
        """
        The sort direction.

        Attributes:
          DIRECTION_UNSPECIFIED (int): Unspecified. This value must not be used.
          ASCENDING (int): Ascending.
          DESCENDING (int): Descending.
        """

        DIRECTION_UNSPECIFIED = 0
        ASCENDING = 1
        DESCENDING = 2


class QueryResultBatch(object):
    class MoreResultsType(enum.IntEnum):
        """
        The possible values for the ``more_results`` field.

        Attributes:
          MORE_RESULTS_TYPE_UNSPECIFIED (int): Unspecified. This value is never used.
          NOT_FINISHED (int): There may be additional batches to fetch from this query.
          MORE_RESULTS_AFTER_LIMIT (int): The query is finished, but there may be more results after the limit.
          MORE_RESULTS_AFTER_CURSOR (int): The query is finished, but there may be more results after the end
          cursor.
          NO_MORE_RESULTS (int): The query is finished, and there are no more results.
        """

        MORE_RESULTS_TYPE_UNSPECIFIED = 0
        NOT_FINISHED = 1
        MORE_RESULTS_AFTER_LIMIT = 2
        MORE_RESULTS_AFTER_CURSOR = 4
        NO_MORE_RESULTS = 3


class ReadOptions(object):
    class ReadConsistency(enum.IntEnum):
        """
        The possible values for read consistencies.

        Attributes:
          READ_CONSISTENCY_UNSPECIFIED (int): Unspecified. This value must not be used.
          STRONG (int): Strong consistency.
          EVENTUAL (int): Eventual consistency.
        """

        READ_CONSISTENCY_UNSPECIFIED = 0
        STRONG = 1
        EVENTUAL = 2
