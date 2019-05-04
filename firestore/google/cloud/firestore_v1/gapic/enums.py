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


class DocumentTransform(object):
    class FieldTransform(object):
        class ServerValue(enum.IntEnum):
            """
            A value that is calculated by the server.

            Attributes:
              SERVER_VALUE_UNSPECIFIED (int): Unspecified. This value must not be used.
              REQUEST_TIME (int): The time at which the server processed the request, with millisecond
              precision.
            """

            SERVER_VALUE_UNSPECIFIED = 0
            REQUEST_TIME = 1


class StructuredQuery(object):
    class Direction(enum.IntEnum):
        """
        A sort direction.

        Attributes:
          DIRECTION_UNSPECIFIED (int): Unspecified.
          ASCENDING (int): Ascending.
          DESCENDING (int): Descending.
        """

        DIRECTION_UNSPECIFIED = 0
        ASCENDING = 1
        DESCENDING = 2

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

    class FieldFilter(object):
        class Operator(enum.IntEnum):
            """
            A field filter operator.

            Attributes:
              OPERATOR_UNSPECIFIED (int): Unspecified. This value must not be used.
              LESS_THAN (int): Less than. Requires that the field come first in ``order_by``.
              LESS_THAN_OR_EQUAL (int): Less than or equal. Requires that the field come first in ``order_by``.
              GREATER_THAN (int): Greater than. Requires that the field come first in ``order_by``.
              GREATER_THAN_OR_EQUAL (int): Greater than or equal. Requires that the field come first in
              ``order_by``.
              EQUAL (int): Equal.
              ARRAY_CONTAINS (int): Contains. Requires that the field is an array.
            """

            OPERATOR_UNSPECIFIED = 0
            LESS_THAN = 1
            LESS_THAN_OR_EQUAL = 2
            GREATER_THAN = 3
            GREATER_THAN_OR_EQUAL = 4
            EQUAL = 5
            ARRAY_CONTAINS = 7

    class UnaryFilter(object):
        class Operator(enum.IntEnum):
            """
            A unary operator.

            Attributes:
              OPERATOR_UNSPECIFIED (int): Unspecified. This value must not be used.
              IS_NAN (int): Test if a field is equal to NaN.
              IS_NULL (int): Test if an exprestion evaluates to Null.
            """

            OPERATOR_UNSPECIFIED = 0
            IS_NAN = 2
            IS_NULL = 3


class TargetChange(object):
    class TargetChangeType(enum.IntEnum):
        """
        The type of change.

        Attributes:
          NO_CHANGE (int): No change has occurred. Used only to send an updated ``resume_token``.
          ADD (int): The targets have been added.
          REMOVE (int): The targets have been removed.
          CURRENT (int): The targets reflect all changes committed before the targets were added
          to the stream.

          This will be sent after or with a ``read_time`` that is greater than or
          equal to the time at which the targets were added.

          Listeners can wait for this change if read-after-write semantics are
          desired.
          RESET (int): The targets have been reset, and a new initial state for the targets
          will be returned in subsequent changes.

          After the initial state is complete, ``CURRENT`` will be returned even
          if the target was previously indicated to be ``CURRENT``.
        """

        NO_CHANGE = 0
        ADD = 1
        REMOVE = 2
        CURRENT = 3
        RESET = 4
