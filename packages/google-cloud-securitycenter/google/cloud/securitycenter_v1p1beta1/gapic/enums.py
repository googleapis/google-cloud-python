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


class NullValue(enum.IntEnum):
    """
    ``NullValue`` is a singleton enumeration to represent the null value for
    the ``Value`` type union.

    The JSON representation for ``NullValue`` is JSON ``null``.

    Attributes:
      NULL_VALUE (int): Null value.
    """

    NULL_VALUE = 0


class Finding(object):
    class State(enum.IntEnum):
        """
        The state of the finding.

        Attributes:
          STATE_UNSPECIFIED (int): Unspecified state.
          ACTIVE (int): The finding requires attention and has not been addressed yet.
          INACTIVE (int): The finding has been fixed, triaged as a non-issue or otherwise addressed
          and is no longer active.
        """

        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        INACTIVE = 2


class ListAssetsResponse(object):
    class ListAssetsResult(object):
        class StateChange(enum.IntEnum):
            """
            The change in state of the asset.

            When querying across two points in time this describes the change
            between the two points: ADDED, REMOVED, or ACTIVE. If there was no
            compare\_duration supplied in the request the state change will be:
            UNUSED

            Attributes:
              UNUSED (int): State change is unused, this is the canonical default for this enum.
              ADDED (int): Asset was added between the points in time.
              REMOVED (int): Asset was removed between the points in time.
              ACTIVE (int): Asset was present at both point(s) in time.
            """

            UNUSED = 0
            ADDED = 1
            REMOVED = 2
            ACTIVE = 3


class ListFindingsResponse(object):
    class ListFindingsResult(object):
        class StateChange(enum.IntEnum):
            """
            The change in state of the finding.

            When querying across two points in time this describes the change in the
            finding between the two points: CHANGED, UNCHANGED, ADDED, or REMOVED.
            Findings can not be deleted, so REMOVED implies that the finding at
            timestamp does not match the filter specified, but it did at timestamp -
            compare\_duration. If there was no compare\_duration supplied in the
            request the state change will be: UNUSED

            Attributes:
              UNUSED (int): State change is unused, this is the canonical default for this enum.
              CHANGED (int): The finding has changed state in some way between the points in time
              and existed at both points.
              UNCHANGED (int): The finding has not changed state between the points in time and
              existed at both points.
              ADDED (int): The finding was created between the points in time.
              REMOVED (int): The finding at timestamp does not match the filter specified, but it did
              at timestamp - compare\_duration.
            """

            UNUSED = 0
            CHANGED = 1
            UNCHANGED = 2
            ADDED = 3
            REMOVED = 4


class NotificationConfig(object):
    class EventType(enum.IntEnum):
        """
        The type of events.

        Attributes:
          EVENT_TYPE_UNSPECIFIED (int): Unspecified event type.
          FINDING (int): Events for findings.
        """

        EVENT_TYPE_UNSPECIFIED = 0
        FINDING = 1


class OrganizationSettings(object):
    class AssetDiscoveryConfig(object):
        class InclusionMode(enum.IntEnum):
            """
            The mode of inclusion when running Asset Discovery. Asset discovery can
            be limited by explicitly identifying projects to be included or
            excluded. If INCLUDE\_ONLY is set, then only those projects within the
            organization and their children are discovered during asset discovery.
            If EXCLUDE is set, then projects that don't match those projects are
            discovered during asset discovery. If neither are set, then all projects
            within the organization are discovered during asset discovery.

            Attributes:
              INCLUSION_MODE_UNSPECIFIED (int): Unspecified. Setting the mode with this value will disable
              inclusion/exclusion filtering for Asset Discovery.
              INCLUDE_ONLY (int): Asset Discovery will capture only the resources within the projects
              specified. All other resources will be ignored.
              EXCLUDE (int): Asset Discovery will ignore all resources under the projects specified.
              All other resources will be retrieved.
            """

            INCLUSION_MODE_UNSPECIFIED = 0
            INCLUDE_ONLY = 1
            EXCLUDE = 2


class RunAssetDiscoveryResponse(object):
    class State(enum.IntEnum):
        """
        The state of an asset discovery run.

        Attributes:
          STATE_UNSPECIFIED (int): Asset discovery run state was unspecified.
          COMPLETED (int): Asset discovery run completed successfully.
          SUPERSEDED (int): Asset discovery run was cancelled with tasks still pending, as another
          run for the same organization was started with a higher priority.
          TERMINATED (int): Asset discovery run was killed and terminated.
        """

        STATE_UNSPECIFIED = 0
        COMPLETED = 1
        SUPERSEDED = 2
        TERMINATED = 3
