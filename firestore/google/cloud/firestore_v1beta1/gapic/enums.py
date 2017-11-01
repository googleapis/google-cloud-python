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


class IndexField(object):
    class Mode(object):
        """
        The mode determines how a field is indexed.

        Attributes:
          MODE_UNSPECIFIED (int): The mode is unspecified.
          ASCENDING (int): The field's values are indexed so as to support sequencing in
          ascending order and also query by <, >, <=, >=, and =.
          DESCENDING (int): The field's values are indexed so as to support sequencing in
          descending order and also query by <, >, <=, >=, and =.
        """
        MODE_UNSPECIFIED = 0
        ASCENDING = 2
        DESCENDING = 3


class Index(object):
    class State(object):
        """
        The state of an index. During index creation, an index will be in the
        ``CREATING`` state. If the index is created successfully, it will transition
        to the ``READY`` state. If the index is not able to be created, it will
        transition to the ``ERROR`` state.

        Attributes:
          STATE_UNSPECIFIED (int): The state is unspecified.
          CREATING (int): The index is being created.
          There is an active long-running operation for the index.
          The index is updated when writing a document.
          Some index data may exist.
          READY (int): The index is ready to be used.
          The index is updated when writing a document.
          The index is fully populated from all stored documents it applies to.
          ERROR (int): The index was being created, but something went wrong.
          There is no active long-running operation for the index,
          and the most recently finished long-running operation failed.
          The index is not updated when writing a document.
          Some index data may exist.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 3
        READY = 2
        ERROR = 5


class IndexOperationMetadata(object):
    class OperationType(object):
        """
        The type of index operation.

        Attributes:
          OPERATION_TYPE_UNSPECIFIED (int): Unspecified. Never set by server.
          CREATING_INDEX (int): The operation is creating the index. Initiated by a ``CreateIndex`` call.
        """
        OPERATION_TYPE_UNSPECIFIED = 0
        CREATING_INDEX = 1


class DocumentTransform(object):
    class FieldTransform(object):
        class ServerValue(object):
            """
            A value that is calculated by the server.

            Attributes:
              SERVER_VALUE_UNSPECIFIED (int): Unspecified. This value must not be used.
              REQUEST_TIME (int): The time at which the server processed the request.
            """
            SERVER_VALUE_UNSPECIFIED = 0
            REQUEST_TIME = 1


class StructuredQuery(object):
    class Direction(object):
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
        class Operator(object):
            """
            A composite filter operator.

            Attributes:
              OPERATOR_UNSPECIFIED (int): Unspecified. This value must not be used.
              AND (int): The results are required to satisfy each of the combined filters.
            """
            OPERATOR_UNSPECIFIED = 0
            AND = 1

    class FieldFilter(object):
        class Operator(object):
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
            """
            OPERATOR_UNSPECIFIED = 0
            LESS_THAN = 1
            LESS_THAN_OR_EQUAL = 2
            GREATER_THAN = 3
            GREATER_THAN_OR_EQUAL = 4
            EQUAL = 5

    class UnaryFilter(object):
        class Operator(object):
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
    class TargetChangeType(object):
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

          Listeners can wait for this change if read-after-write semantics
          are desired.
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
