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


class RestoreSourceType(enum.IntEnum):
    """
    Indicates the type of the restore source.

    Attributes:
      TYPE_UNSPECIFIED (int): No restore associated.
      BACKUP (int): A backup was used as the source of the restore.
    """

    TYPE_UNSPECIFIED = 0
    BACKUP = 1


class Backup(object):
    class State(enum.IntEnum):
        """
        Indicates the current state of the backup.

        Attributes:
          STATE_UNSPECIFIED (int): Not specified.
          CREATING (int): The pending backup is still being created. Operations on the backup
          may fail with ``FAILED_PRECONDITION`` in this state.
          READY (int): The backup is complete and ready for use.
        """

        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2


class Database(object):
    class State(enum.IntEnum):
        """
        Indicates the current state of the database.

        Attributes:
          STATE_UNSPECIFIED (int): Not specified.
          CREATING (int): The database is still being created. Operations on the database may
          fail with ``FAILED_PRECONDITION`` in this state.
          READY (int): The database is fully created and ready for use.
          READY_OPTIMIZING (int): The database is fully created and ready for use, but is still being
          optimized for performance and cannot handle full load.

          In this state, the database still references the backup it was restore
          from, preventing the backup from being deleted. When optimizations are
          complete, the full performance of the database will be restored, and the
          database will transition to ``READY`` state.
        """

        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        READY_OPTIMIZING = 3
