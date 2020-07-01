# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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


class OperationType(enum.IntEnum):
    """
    Operation types.

    Attributes:
      OPERATION_TYPE_UNSPECIFIED (int): Unspecified.
      EXPORT_ENTITIES (int): ExportEntities.
      IMPORT_ENTITIES (int): ImportEntities.
      CREATE_INDEX (int): CreateIndex.
      DELETE_INDEX (int): DeleteIndex.
    """

    OPERATION_TYPE_UNSPECIFIED = 0
    EXPORT_ENTITIES = 1
    IMPORT_ENTITIES = 2
    CREATE_INDEX = 3
    DELETE_INDEX = 4


class CommonMetadata(object):
    class State(enum.IntEnum):
        """
        The various possible states for an ongoing Operation.

        Attributes:
          STATE_UNSPECIFIED (int): Unspecified.
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

        STATE_UNSPECIFIED = 0
        INITIALIZING = 1
        PROCESSING = 2
        CANCELLING = 3
        FINALIZING = 4
        SUCCESSFUL = 5
        FAILED = 6
        CANCELLED = 7


class Index(object):
    class AncestorMode(enum.IntEnum):
        """
        For an ordered index, specifies whether each of the entity's ancestors
        will be included.

        Attributes:
          ANCESTOR_MODE_UNSPECIFIED (int): The ancestor mode is unspecified.
          NONE (int): Do not include the entity's ancestors in the index.
          ALL_ANCESTORS (int): Include all the entity's ancestors in the index.
        """

        ANCESTOR_MODE_UNSPECIFIED = 0
        NONE = 1
        ALL_ANCESTORS = 2

    class Direction(enum.IntEnum):
        """
        The direction determines how a property is indexed.

        Attributes:
          DIRECTION_UNSPECIFIED (int): The direction is unspecified.
          ASCENDING (int): The property's values are indexed so as to support sequencing in
          ascending order and also query by <, >, <=, >=, and =.
          DESCENDING (int): The property's values are indexed so as to support sequencing in
          descending order and also query by <, >, <=, >=, and =.
        """

        DIRECTION_UNSPECIFIED = 0
        ASCENDING = 1
        DESCENDING = 2

    class State(enum.IntEnum):
        """
        The possible set of states of an index.

        Attributes:
          STATE_UNSPECIFIED (int): The state is unspecified.
          CREATING (int): The index is being created, and cannot be used by queries.
          There is an active long-running operation for the index.
          The index is updated when writing an entity.
          Some index data may exist.
          READY (int): The index is ready to be used.
          The index is updated when writing an entity.
          The index is fully populated from all stored entities it applies to.
          DELETING (int): The index is being deleted, and cannot be used by queries.
          There is an active long-running operation for the index.
          The index is not updated when writing an entity.
          Some index data may exist.
          ERROR (int): The index was being created or deleted, but something went wrong.
          The index cannot by used by queries.
          There is no active long-running operation for the index,
          and the most recently finished long-running operation failed.
          The index is not updated when writing an entity.
          Some index data may exist.
        """

        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        DELETING = 3
        ERROR = 4
