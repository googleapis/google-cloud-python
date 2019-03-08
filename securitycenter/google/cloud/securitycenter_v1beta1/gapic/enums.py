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
        class State(enum.IntEnum):
            """
            State of the asset.

            When querying across two points in time this describes the change
            between the two points: ADDED, REMOVED, or ACTIVE. If there was no
            compare\_duration supplied in the request the state should be: UNUSED

            Attributes:
              STATE_UNSPECIFIED (int): Unspecified state.
              UNUSED (int): Request did not specify use of this field in the result.
              ADDED (int): Asset was added between the points in time.
              REMOVED (int): Asset was removed between the points in time.
              ACTIVE (int): Asset was active at both point(s) in time.
            """

            STATE_UNSPECIFIED = 0
            UNUSED = 1
            ADDED = 2
            REMOVED = 3
            ACTIVE = 4


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
