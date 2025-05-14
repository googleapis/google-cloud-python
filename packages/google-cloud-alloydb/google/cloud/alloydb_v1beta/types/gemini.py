# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.alloydb.v1beta",
    manifest={
        "GCAEntitlementType",
        "GeminiClusterConfig",
        "GeminiInstanceConfig",
        "GCAInstanceConfig",
    },
)


class GCAEntitlementType(proto.Enum):
    r"""Enum representing the type of GCA entitlement assigned to a
    resource.

    Values:
        GCA_ENTITLEMENT_TYPE_UNSPECIFIED (0):
            No GCA entitlement is assigned.
        GCA_STANDARD (1):
            The resource is entitled to the GCA Standard
            Tier.
    """
    GCA_ENTITLEMENT_TYPE_UNSPECIFIED = 0
    GCA_STANDARD = 1


class GeminiClusterConfig(proto.Message):
    r"""Cluster level configuration parameters related to the Gemini
    in Databases add-on.

    Attributes:
        entitled (bool):
            Output only. Whether the Gemini in Databases
            add-on is enabled for the cluster. It will be
            true only if the add-on has been enabled for the
            billing account corresponding to the cluster.
            Its status is toggled from the Admin Control
            Center (ACC) and cannot be toggled using
            AlloyDB's APIs.
    """

    entitled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class GeminiInstanceConfig(proto.Message):
    r"""Instance level configuration parameters related to the Gemini
    in Databases add-on.

    Attributes:
        entitled (bool):
            Output only. Whether the Gemini in Databases
            add-on is enabled for the instance. It will be
            true only if the add-on has been enabled for the
            billing account corresponding to the instance.
            Its status is toggled from the Admin Control
            Center (ACC) and cannot be toggled using
            AlloyDB's APIs.
    """

    entitled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class GCAInstanceConfig(proto.Message):
    r"""Instance level configuration parameters related to the Gemini
    Cloud Assist product.

    Attributes:
        gca_entitlement (google.cloud.alloydb_v1beta.types.GCAEntitlementType):
            Output only. Represents the GCA entitlement
            state of the instance.
    """

    gca_entitlement: "GCAEntitlementType" = proto.Field(
        proto.ENUM,
        number=1,
        enum="GCAEntitlementType",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
