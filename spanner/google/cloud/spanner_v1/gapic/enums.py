# Copyright 2017, Google LLC All rights reserved.
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
"""Wrappers for protocol buffer enum types."""


class NullValue(object):
    """
    ``NullValue`` is a singleton enumeration to represent the null value for the
    ``Value`` type union.

     The JSON representation for ``NullValue`` is JSON ``null``.

    Attributes:
      NULL_VALUE (int): Null value.
    """
    NULL_VALUE = 0


class TypeCode(object):
    """
    ``TypeCode`` is used as part of ``Type`` to
    indicate the type of a Cloud Spanner value.

    Each legal value of a type can be encoded to or decoded from a JSON
    value, using the encodings described below. All Cloud Spanner values can
    be ``null``, regardless of type; ``null``s are always encoded as a JSON
    ``null``.

    Attributes:
      TYPE_CODE_UNSPECIFIED (int): Not specified.
      BOOL (int): Encoded as JSON ``true`` or ``false``.
      INT64 (int): Encoded as ``string``, in decimal format.
      FLOAT64 (int): Encoded as ``number``, or the strings ``\"NaN\"``, ``\"Infinity\"``, or
      ``\"-Infinity\"``.
      TIMESTAMP (int): Encoded as ``string`` in RFC 3339 timestamp format. The time zone
      must be present, and must be ``\"Z\"``.
      DATE (int): Encoded as ``string`` in RFC 3339 date format.
      STRING (int): Encoded as ``string``.
      BYTES (int): Encoded as a base64-encoded ``string``, as described in RFC 4648,
      section 4.
      ARRAY (int): Encoded as ``list``, where the list elements are represented
      according to ``array_element_type``.
      STRUCT (int): Encoded as ``list``, where list element ``i`` is represented according
      to [struct_type.fields[i]][google.spanner.v1.StructType.fields].
    """
    TYPE_CODE_UNSPECIFIED = 0
    BOOL = 1
    INT64 = 2
    FLOAT64 = 3
    TIMESTAMP = 4
    DATE = 5
    STRING = 6
    BYTES = 7
    ARRAY = 8
    STRUCT = 9


class PlanNode(object):
    class Kind(object):
        """
        The kind of ``PlanNode``. Distinguishes between the two different kinds of
        nodes that can appear in a query plan.

        Attributes:
          KIND_UNSPECIFIED (int): Not specified.
          RELATIONAL (int): Denotes a Relational operator node in the expression tree. Relational
          operators represent iterative processing of rows during query execution.
          For example, a ``TableScan`` operation that reads rows from a table.
          SCALAR (int): Denotes a Scalar node in the expression tree. Scalar nodes represent
          non-iterable entities in the query plan. For example, constants or
          arithmetic operators appearing inside predicate expressions or references
          to column names.
        """
        KIND_UNSPECIFIED = 0
        RELATIONAL = 1
        SCALAR = 2


class ExecuteSqlRequest(object):
    class QueryMode(object):
        """
        Mode in which the query must be processed.

        Attributes:
          NORMAL (int): The default mode where only the query result, without any information
          about the query plan is returned.
          PLAN (int): This mode returns only the query plan, without any result rows or
          execution statistics information.
          PROFILE (int): This mode returns both the query plan and the execution statistics along
          with the result rows.
        """
        NORMAL = 0
        PLAN = 1
        PROFILE = 2
