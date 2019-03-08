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


class Instance(object):
    class State(enum.IntEnum):
        """
        Represents the different states of a Redis instance.

        Attributes:
          STATE_UNSPECIFIED (int): Not set.
          CREATING (int): Redis instance is being created.
          READY (int): Redis instance has been created and is fully usable.
          UPDATING (int): Redis instance configuration is being updated. Certain kinds of updates
          may cause the instance to become unusable while the update is in
          progress.
          DELETING (int): Redis instance is being deleted.
          REPAIRING (int): Redis instance is being repaired and may be unusable. Details can be
          found in the ``status_message`` field.
          MAINTENANCE (int): Maintenance is being performed on this Redis instance.
        """

        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        UPDATING = 3
        DELETING = 4
        REPAIRING = 5
        MAINTENANCE = 6

    class Tier(enum.IntEnum):
        """
        Available service tiers to choose from

        Attributes:
          TIER_UNSPECIFIED (int): Not set.
          BASIC (int): BASIC tier: standalone instance
          STANDARD_HA (int): STANDARD\_HA tier: highly available primary/replica instances
        """

        TIER_UNSPECIFIED = 0
        BASIC = 1
        STANDARD_HA = 3
