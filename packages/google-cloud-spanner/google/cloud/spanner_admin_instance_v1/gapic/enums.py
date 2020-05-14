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


class Instance(object):
    class State(enum.IntEnum):
        """
        Indicates the current state of the instance.

        Attributes:
          STATE_UNSPECIFIED (int): Not specified.
          CREATING (int): The instance is still being created. Resources may not be
          available yet, and operations such as database creation may not
          work.
          READY (int): The instance is fully created and ready to do work such as
          creating databases.
        """

        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2


class ReplicaInfo(object):
    class ReplicaType(enum.IntEnum):
        """
        Indicates the type of replica. See the `replica types
        documentation <https://cloud.google.com/spanner/docs/replication#replica_types>`__
        for more details.

        Attributes:
          TYPE_UNSPECIFIED (int): Not specified.
          READ_WRITE (int): Read-write replicas support both reads and writes. These replicas:

          -  Maintain a full copy of your data.
          -  Serve reads.
          -  Can vote whether to commit a write.
          -  Participate in leadership election.
          -  Are eligible to become a leader.
          READ_ONLY (int): Read-only replicas only support reads (not writes). Read-only
          replicas:

          -  Maintain a full copy of your data.
          -  Serve reads.
          -  Do not participate in voting to commit writes.
          -  Are not eligible to become a leader.
          WITNESS (int): Witness replicas don't support reads but do participate in voting to
          commit writes. Witness replicas:

          -  Do not maintain a full copy of data.
          -  Do not serve reads.
          -  Vote whether to commit writes.
          -  Participate in leader election but are not eligible to become leader.
        """

        TYPE_UNSPECIFIED = 0
        READ_WRITE = 1
        READ_ONLY = 2
        WITNESS = 3
