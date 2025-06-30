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

from google.ads.admanager_v1.types import (
    request_platform_enum,
    targeted_video_bumper_type_enum,
    video_position_enum,
)

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Targeting",
        "GeoTargeting",
        "TechnologyTargeting",
        "BandwidthTargeting",
        "DeviceCategoryTargeting",
        "OperatingSystemTargeting",
        "InventoryTargeting",
        "AdUnitTargeting",
        "RequestPlatformTargeting",
        "CustomTargeting",
        "CustomTargetingClause",
        "CustomTargetingLiteral",
        "UserDomainTargeting",
        "VideoPositionTargeting",
        "VideoPosition",
        "DataSegmentTargeting",
    },
)


class Targeting(proto.Message):
    r"""Targeting expression.

    Attributes:
        geo_targeting (google.ads.admanager_v1.types.GeoTargeting):
            Optional. Used to target/exclude various geo
            targets.
        technology_targeting (google.ads.admanager_v1.types.TechnologyTargeting):
            Optional. Used to target various technology
            targeting dimensions.
        inventory_targeting (google.ads.admanager_v1.types.InventoryTargeting):
            Optional. Used to target/exclude various ad
            units and/or placements.
        request_platform_targeting (google.ads.admanager_v1.types.RequestPlatformTargeting):
            Optional. Used to target specific request
            platforms.
        custom_targeting (google.ads.admanager_v1.types.CustomTargeting):
            Optional. Used to target key/values, audience
            segments, and/or CMS metadata.
        user_domain_targeting (google.ads.admanager_v1.types.UserDomainTargeting):
            Optional. Used to target user domains.
        video_position_targeting (google.ads.admanager_v1.types.VideoPositionTargeting):
            Optional. Used to target video positions.
        data_segment_targeting (google.ads.admanager_v1.types.DataSegmentTargeting):
            Optional. Used to target data segments.
    """

    geo_targeting: "GeoTargeting" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="GeoTargeting",
    )
    technology_targeting: "TechnologyTargeting" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="TechnologyTargeting",
    )
    inventory_targeting: "InventoryTargeting" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="InventoryTargeting",
    )
    request_platform_targeting: "RequestPlatformTargeting" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="RequestPlatformTargeting",
    )
    custom_targeting: "CustomTargeting" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="CustomTargeting",
    )
    user_domain_targeting: "UserDomainTargeting" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="UserDomainTargeting",
    )
    video_position_targeting: "VideoPositionTargeting" = proto.Field(
        proto.MESSAGE,
        number=12,
        message="VideoPositionTargeting",
    )
    data_segment_targeting: "DataSegmentTargeting" = proto.Field(
        proto.MESSAGE,
        number=13,
        message="DataSegmentTargeting",
    )


class GeoTargeting(proto.Message):
    r"""Represents a list of targeted and excluded geos.

    Attributes:
        targeted_geos (MutableSequence[str]):
            Optional. A list of geo resource names that
            should be targeted/included.
        excluded_geos (MutableSequence[str]):
            Optional. A list of geo resource names that
            should be excluded.
    """

    targeted_geos: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    excluded_geos: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


class TechnologyTargeting(proto.Message):
    r"""Various types of technology targeting expressed by child
    messages are applied with logical AND.

    Attributes:
        bandwidth_targeting (google.ads.admanager_v1.types.BandwidthTargeting):
            Optional. Bandwidth targeting dimension.
        device_category_targeting (google.ads.admanager_v1.types.DeviceCategoryTargeting):
            Optional. Device category targeting
            dimension.
        operating_system_targeting (google.ads.admanager_v1.types.OperatingSystemTargeting):
            Optional. Operating system targeting
            dimension.
    """

    bandwidth_targeting: "BandwidthTargeting" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="BandwidthTargeting",
    )
    device_category_targeting: "DeviceCategoryTargeting" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="DeviceCategoryTargeting",
    )
    operating_system_targeting: "OperatingSystemTargeting" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="OperatingSystemTargeting",
    )


class BandwidthTargeting(proto.Message):
    r"""Bandwidth Targeting.

    Reach users accessing the internet via various means of
    connection, such as cable, DSL, or dial-up. Can be useful to
    target campaigns using low-resolution creatives or text ads for
    users with low bandwidth.

    Attributes:
        targeted_bandwidth_groups (MutableSequence[str]):
            Optional. A list of resource names of the
            bandwidth groups that should be
            targeted/included.
        excluded_bandwidth_groups (MutableSequence[str]):
            Optional. A list of resource names of the
            bandwidth groups that should be excluded.
    """

    targeted_bandwidth_groups: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    excluded_bandwidth_groups: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


class DeviceCategoryTargeting(proto.Message):
    r"""Represents a list of targeted and excluded device categories.

    Attributes:
        targeted_categories (MutableSequence[str]):
            Optional. A list of device category resource
            names that should be targeted/included.
        excluded_categories (MutableSequence[str]):
            Optional. A list of device category resource
            names that should be excluded.
    """

    targeted_categories: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    excluded_categories: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


class OperatingSystemTargeting(proto.Message):
    r"""Operating System Targeting

    Attributes:
        targeted_operating_systems (MutableSequence[str]):
            Optional. A list of operating system resource
            names that should be targeted/included.
        excluded_operating_systems (MutableSequence[str]):
            Optional. A list of operating system resource
            names that should be excluded.
        targeted_operating_system_versions (MutableSequence[str]):
            Optional. A list of operating system version
            resource names that should be targeted/included.
        excluded_operating_system_versions (MutableSequence[str]):
            Optional. A list of operating system version
            resource names that should be excluded.
    """

    targeted_operating_systems: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    excluded_operating_systems: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    targeted_operating_system_versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    excluded_operating_system_versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )


class InventoryTargeting(proto.Message):
    r"""Targeted ad units and AU placements are applied with logical OR.
    Example:

    (au:1 OR au:2 OR au_placement:5) AND (NOT (au:3))

    Attributes:
        targeted_ad_units (MutableSequence[google.ads.admanager_v1.types.AdUnitTargeting]):
            Optional. A list of ad units that should be
            targeted/included.
        excluded_ad_units (MutableSequence[google.ads.admanager_v1.types.AdUnitTargeting]):
            Optional. A list of ad units that should be
            excluded.
            Excluded AUs take precedence over targeted AUs.
            In fact an AU can be excluded only if one of its
            ancestors is targeted. Subsequently child AUs of
            an excluded AU can not be targeted (except via a
            placement).
        targeted_placements (MutableSequence[str]):
            Optional. The resource names of the
            placements that should be targeted/included.
    """

    targeted_ad_units: MutableSequence["AdUnitTargeting"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AdUnitTargeting",
    )
    excluded_ad_units: MutableSequence["AdUnitTargeting"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="AdUnitTargeting",
    )
    targeted_placements: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class AdUnitTargeting(proto.Message):
    r"""Specifies an ad unit and (optionally) its descendants.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        include_descendants (bool):
            Whether this ad unit's children should be
            targeted/excluded as well.

            This field is a member of `oneof`_ ``_include_descendants``.
        ad_unit (str):
            Optional. The resource name of this ad unit.

            This field is a member of `oneof`_ ``_ad_unit``.
    """

    include_descendants: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    ad_unit: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )


class RequestPlatformTargeting(proto.Message):
    r"""Represents a list of targeted request platforms.

    Attributes:
        request_platforms (MutableSequence[google.ads.admanager_v1.types.RequestPlatformEnum.RequestPlatform]):
            Optional. The list of request platforms that
            should be targeted.
    """

    request_platforms: MutableSequence[
        request_platform_enum.RequestPlatformEnum.RequestPlatform
    ] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=request_platform_enum.RequestPlatformEnum.RequestPlatform,
    )


class CustomTargeting(proto.Message):
    r"""Represents the top level targeting expression for custom
    key/values, audience segments, and/or CMS metadata.

    Attributes:
        custom_targeting_clauses (MutableSequence[google.ads.admanager_v1.types.CustomTargetingClause]):
            Optional. These clauses are all ORed
            together.
    """

    custom_targeting_clauses: MutableSequence[
        "CustomTargetingClause"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CustomTargetingClause",
    )


class CustomTargetingClause(proto.Message):
    r"""Represents a logical AND of individual custom targeting
    expressions.

    Attributes:
        custom_targeting_literals (MutableSequence[google.ads.admanager_v1.types.CustomTargetingLiteral]):
            Optional. Leaf targeting expressions for
            custom key/values.
    """

    custom_targeting_literals: MutableSequence[
        "CustomTargetingLiteral"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CustomTargetingLiteral",
    )


class CustomTargetingLiteral(proto.Message):
    r"""Represents targeting for custom key/values. The values are
    ORed together.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        negative (bool):
            Whether this expression is negatively
            targeted, meaning it matches ad requests that
            exclude the below values.

            This field is a member of `oneof`_ ``_negative``.
        custom_targeting_key (str):
            Optional. The resource name of the targeted
            CustomKey.

            This field is a member of `oneof`_ ``_custom_targeting_key``.
        custom_targeting_values (MutableSequence[str]):
            Optional. The resource names of the targeted
            CustomValues.
    """

    negative: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    custom_targeting_key: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    custom_targeting_values: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class UserDomainTargeting(proto.Message):
    r"""User Domain Targeting

    Attributes:
        targeted_user_domains (MutableSequence[str]):
            Optional. A list of user domains that should
            be targeted/included.
        excluded_user_domains (MutableSequence[str]):
            Optional. A list of user domains that should
            be excluded.
    """

    targeted_user_domains: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    excluded_user_domains: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class VideoPositionTargeting(proto.Message):
    r"""Video Position Targeting

    Attributes:
        video_positions (MutableSequence[google.ads.admanager_v1.types.VideoPosition]):
            Optional. A list of video position targeting
            criterion (applied with a logical AND).
    """

    video_positions: MutableSequence["VideoPosition"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="VideoPosition",
    )


class VideoPosition(proto.Message):
    r"""Video Position Targeting Criterion

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        midroll_index (int):
            Optional. The index of the mid-roll to target. This field is
            ignored when targeting any video position (e.g.
            position_type) other than MIDROLL.

            This field is a member of `oneof`_ ``_midroll_index``.
        reverse_midroll_index (int):
            Optional. The index from the back of the pod of the mid-roll
            to target. This field is ignored when targeting any video
            position (e.g. position_type) other than MIDROLL or if
            targeting a specific midroll index (e.g. midroll_index !=
            0).

            This field is a member of `oneof`_ ``_reverse_midroll_index``.
        pod_position (int):
            Optional. The video position within a pod to target. This
            field must be unset in order to target a specific video
            position (e.g. position_type), bumper type (e.g.
            bumper_type), or custom ad spot (e.g. custom_spot_id).

            This field is a member of `oneof`_ ``_pod_position``.
        position_type (google.ads.admanager_v1.types.VideoPositionEnum.VideoPosition):
            Optional. The position within a video to
            target. A video ad can target a position
            (pre-roll, all mid-rolls, or post-roll) or a
            specific mid-roll index.

            This field is a member of `oneof`_ ``_position_type``.
        bumper_type (google.ads.admanager_v1.types.TargetedVideoBumperTypeEnum.TargetedVideoBumperType):
            Optional. The video bumper type to target. This field must
            be unset in order to target a specific video position (e.g.
            position_type), pod position (e.g. pod_position), or custom
            ad spot (e.g. custom_spot_id).

            This field is a member of `oneof`_ ``_bumper_type``.
    """

    midroll_index: int = proto.Field(
        proto.INT64,
        number=1,
        optional=True,
    )
    reverse_midroll_index: int = proto.Field(
        proto.INT64,
        number=2,
        optional=True,
    )
    pod_position: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    position_type: video_position_enum.VideoPositionEnum.VideoPosition = proto.Field(
        proto.ENUM,
        number=5,
        optional=True,
        enum=video_position_enum.VideoPositionEnum.VideoPosition,
    )
    bumper_type: targeted_video_bumper_type_enum.TargetedVideoBumperTypeEnum.TargetedVideoBumperType = proto.Field(
        proto.ENUM,
        number=6,
        optional=True,
        enum=targeted_video_bumper_type_enum.TargetedVideoBumperTypeEnum.TargetedVideoBumperType,
    )


class DataSegmentTargeting(proto.Message):
    r"""Data Segment Targeting

    Attributes:
        has_data_segment_targeting (bool):
            Output only. Whether any data segments are
            currently targeted.
    """

    has_data_segment_targeting: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
