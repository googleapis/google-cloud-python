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


class OperationState(enum.IntEnum):
    """
    Describes the state of the operation.

    Attributes:
      OPERATION_STATE_UNSPECIFIED (int): Unspecified.
      INITIALIZING (int): Request is being prepared for processing.
      PROCESSING (int): Request is actively being processed.
      CANCELLING (int): Request is in the process of being cancelled after user called
      google.longrunning.Operations.CancelOperation on the operation.
      FINALIZING (int): Request has been processed and is in its finalization stage.
      SUCCESSFUL (int): Request has completed successfully.
      FAILED (int): Request has finished being processed, but encountered an error.
      CANCELLED (int): Request has finished being cancelled after user called
      google.longrunning.Operations.CancelOperation.
    """

    OPERATION_STATE_UNSPECIFIED = 0
    INITIALIZING = 1
    PROCESSING = 2
    CANCELLING = 3
    FINALIZING = 4
    SUCCESSFUL = 5
    FAILED = 6
    CANCELLED = 7


class FieldOperationMetadata(object):
    class IndexConfigDelta(object):
        class ChangeType(enum.IntEnum):
            """
            Specifies how the index is changing.

            Attributes:
              CHANGE_TYPE_UNSPECIFIED (int): The type of change is not specified or known.
              ADD (int): The single field index is being added.
              REMOVE (int): The single field index is being removed.
            """

            CHANGE_TYPE_UNSPECIFIED = 0
            ADD = 1
            REMOVE = 2


class Index(object):
    class QueryScope(enum.IntEnum):
        """
        Query Scope defines the scope at which a query is run. This is specified
        on a StructuredQuery's ``from`` field.

        Attributes:
          QUERY_SCOPE_UNSPECIFIED (int): The query scope is unspecified. Not a valid option.
          COLLECTION (int): Indexes with a collection query scope specified allow queries
          against a collection that is the child of a specific document, specified
          at query time, and that has the collection id specified by the index.
          COLLECTION_GROUP (int): Indexes with a collection group query scope specified allow queries
          against all collections that has the collection id specified by the
          index.
        """

        QUERY_SCOPE_UNSPECIFIED = 0
        COLLECTION = 1
        COLLECTION_GROUP = 2

    class State(enum.IntEnum):
        """
        The state of an index. During index creation, an index will be in the
        ``CREATING`` state. If the index is created successfully, it will
        transition to the ``READY`` state. If the index creation encounters a
        problem, the index will transition to the ``NEEDS_REPAIR`` state.

        Attributes:
          STATE_UNSPECIFIED (int): The state is unspecified.
          CREATING (int): The index is being created.
          There is an active long-running operation for the index.
          The index is updated when writing a document.
          Some index data may exist.
          READY (int): The index is ready to be used.
          The index is updated when writing a document.
          The index is fully populated from all stored documents it applies to.
          NEEDS_REPAIR (int): The index was being created, but something went wrong.
          There is no active long-running operation for the index,
          and the most recently finished long-running operation failed.
          The index is not updated when writing a document.
          Some index data may exist.
          Use the google.longrunning.Operations API to determine why the operation
          that last attempted to create this index failed, then re-create the
          index.
        """

        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        NEEDS_REPAIR = 3

    class IndexField(object):
        class ArrayConfig(enum.IntEnum):
            """
            The supported array value configurations.

            Attributes:
              ARRAY_CONFIG_UNSPECIFIED (int): The index does not support additional array queries.
              CONTAINS (int): The index supports array containment queries.
            """

            ARRAY_CONFIG_UNSPECIFIED = 0
            CONTAINS = 1

        class Order(enum.IntEnum):
            """
            The supported orderings.

            Attributes:
              ORDER_UNSPECIFIED (int): The ordering is unspecified. Not a valid option.
              ASCENDING (int): The field is ordered by ascending field value.
              DESCENDING (int): The field is ordered by descending field value.
            """

            ORDER_UNSPECIFIED = 0
            ASCENDING = 1
            DESCENDING = 2
