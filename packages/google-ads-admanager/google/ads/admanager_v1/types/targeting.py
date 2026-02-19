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
        "BrowserTargeting",
        "BrowserLanguageTargeting",
        "DeviceCategoryTargeting",
        "DeviceCapabilityTargeting",
        "DeviceManufacturerTargeting",
        "MobileCarrierTargeting",
        "OperatingSystemTargeting",
        "InventoryTargeting",
        "AdUnitTargeting",
        "RequestPlatformTargeting",
        "CustomTargeting",
        "CustomTargetingClause",
        "CustomTargetingLiteral",
        "AudienceSegmentTargeting",
        "CmsMetadataTargeting",
        "UserDomainTargeting",
        "VideoPositionTargeting",
        "VideoPosition",
        "DataSegmentTargeting",
        "ContentTargeting",
        "MobileApplicationTargeting",
        "FirstPartyMobileApplicationTargeting",
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
        content_targeting (google.ads.admanager_v1.types.ContentTargeting):
            Optional. Used to target content.
        mobile_application_targeting (google.ads.admanager_v1.types.MobileApplicationTargeting):
            Optional. Used to target mobile applications.
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
    content_targeting: "ContentTargeting" = proto.Field(
        proto.MESSAGE,
        number=15,
        message="ContentTargeting",
    )
    mobile_application_targeting: "MobileApplicationTargeting" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="MobileApplicationTargeting",
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
        browser_targeting (google.ads.admanager_v1.types.BrowserTargeting):
            Optional. Browser targeting dimension.
        browser_language_targeting (google.ads.admanager_v1.types.BrowserLanguageTargeting):
            Optional. Browser language targeting
            dimension.
        device_capability_targeting (google.ads.admanager_v1.types.DeviceCapabilityTargeting):
            Optional. Device capability targeting
            dimension.
        device_category_targeting (google.ads.admanager_v1.types.DeviceCategoryTargeting):
            Optional. Device category targeting
            dimension.
        device_manufacturer_targeting (google.ads.admanager_v1.types.DeviceManufacturerTargeting):
            Optional. Device manufacturer targeting
            dimension.
        mobile_carrier_targeting (google.ads.admanager_v1.types.MobileCarrierTargeting):
            Optional. Mobile carrier targeting dimension.
        operating_system_targeting (google.ads.admanager_v1.types.OperatingSystemTargeting):
            Optional. Operating system targeting
            dimension.
    """

    bandwidth_targeting: "BandwidthTargeting" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="BandwidthTargeting",
    )
    browser_targeting: "BrowserTargeting" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="BrowserTargeting",
    )
    browser_language_targeting: "BrowserLanguageTargeting" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="BrowserLanguageTargeting",
    )
    device_capability_targeting: "DeviceCapabilityTargeting" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="DeviceCapabilityTargeting",
    )
    device_category_targeting: "DeviceCategoryTargeting" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="DeviceCategoryTargeting",
    )
    device_manufacturer_targeting: "DeviceManufacturerTargeting" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="DeviceManufacturerTargeting",
    )
    mobile_carrier_targeting: "MobileCarrierTargeting" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="MobileCarrierTargeting",
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


class BrowserTargeting(proto.Message):
    r"""Browser Targeting.

    Allows publishers to target/exclude a browser type (e.g. Chrome,
    Firefox, Safari). For more information, see
    https://support.google.com/admanager/answer/2884033 (Targeting
    types > Browser).

    Attributes:
        targeted_browsers (MutableSequence[str]):
            Optional. A list of browser resource names
            that should be targeted/included.
        excluded_browsers (MutableSequence[str]):
            Optional. A list of browser resource names
            that should be excluded.
    """

    targeted_browsers: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    excluded_browsers: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


class BrowserLanguageTargeting(proto.Message):
    r"""Browser Language Targeting.

    For ads targeting mobile apps and their associated WebViews, the
    language used is based on the language specified by the user in
    their mobile device settings. If a browser has more than one
    language assigned to it, each language generates an impression.

    Attributes:
        targeted_browser_languages (MutableSequence[str]):
            Optional. A list of browser language resource
            names that should be targeted/included.
        excluded_browser_languages (MutableSequence[str]):
            Optional. A list of browser language resource
            names that should be excluded.
    """

    targeted_browser_languages: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    excluded_browser_languages: MutableSequence[str] = proto.RepeatedField(
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


class DeviceCapabilityTargeting(proto.Message):
    r"""Device Capability Targeting.

    Can be used to target/exclude users using mobile apps, ad
    requests resulting from apps built on the MRAID standard, or
    users on devices that are able to make phone calls versus
    devices that aren't able to make phone calls, such as tablets.

    Attributes:
        targeted_capabilities (MutableSequence[str]):
            Optional. A list of device capability
            resource names that should be targeted/included.
        excluded_capabilities (MutableSequence[str]):
            Optional. A list of device capability
            resource names that should be excluded.
    """

    targeted_capabilities: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    excluded_capabilities: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


class DeviceManufacturerTargeting(proto.Message):
    r"""Device Manufacturer Targeting.

    Can be used to target/exclude users on devices made by specific
    brands or companies, such as Apple, Google, Samsung and others.
    For more information, see
    https://support.google.com/admanager/answer/2884033 ("Targeting
    types > Device manufacturer").

    Attributes:
        targeted_device_manufacturers (MutableSequence[str]):
            Optional. A list of device manufacturer
            resource names that should be targeted/included.
        excluded_device_manufacturers (MutableSequence[str]):
            Optional. A list of device manufacturer
            resource names that should be excluded.
        targeted_mobile_devices (MutableSequence[str]):
            Optional. A list of mobile device resource
            names that should be targeted/included.
        excluded_mobile_devices (MutableSequence[str]):
            Optional. A list of mobile device resource
            names that should be excluded.
        targeted_mobile_device_submodels (MutableSequence[str]):
            Optional. A list of mobile device submodel
            resource names that should be targeted/included.
        excluded_mobile_device_submodels (MutableSequence[str]):
            Optional. A list of mobile device submodel
            resource names that should be excluded.
    """

    targeted_device_manufacturers: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    excluded_device_manufacturers: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )
    targeted_mobile_devices: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    excluded_mobile_devices: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=10,
    )
    targeted_mobile_device_submodels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=11,
    )
    excluded_mobile_device_submodels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=12,
    )


class MobileCarrierTargeting(proto.Message):
    r"""Mobile Carrier Targeting.

    Can be used to target/exclude a variety of mobile carriers, such
    as AT&T, Verizon, or T-Mobile.

    Attributes:
        targeted_mobile_carriers (MutableSequence[str]):
            Optional. A list of mobile carrier resource
            names that should be targeted/included.
        excluded_mobile_carriers (MutableSequence[str]):
            Optional. A list of mobile carrier resource
            names that should be excluded.
    """

    targeted_mobile_carriers: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    excluded_mobile_carriers: MutableSequence[str] = proto.RepeatedField(
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

    custom_targeting_clauses: MutableSequence["CustomTargetingClause"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="CustomTargetingClause",
        )
    )


class CustomTargetingClause(proto.Message):
    r"""Represents a logical AND of individual custom targeting
    expressions.

    Attributes:
        custom_targeting_literals (MutableSequence[google.ads.admanager_v1.types.CustomTargetingLiteral]):
            Optional. Leaf targeting expressions for
            custom key/values.
        audience_segment_targetings (MutableSequence[google.ads.admanager_v1.types.AudienceSegmentTargeting]):
            Optional. Leaf targeting expressions for
            audience segments.
        cms_metadata_targetings (MutableSequence[google.ads.admanager_v1.types.CmsMetadataTargeting]):
            Optional. Leaf targeting expressions for cms
            metadata.
    """

    custom_targeting_literals: MutableSequence["CustomTargetingLiteral"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="CustomTargetingLiteral",
        )
    )
    audience_segment_targetings: MutableSequence["AudienceSegmentTargeting"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="AudienceSegmentTargeting",
        )
    )
    cms_metadata_targetings: MutableSequence["CmsMetadataTargeting"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message="CmsMetadataTargeting",
        )
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


class AudienceSegmentTargeting(proto.Message):
    r"""Represents targeting for audience segments. The values are combined
    in a logical ``OR``.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        negative (bool):
            Whether this expression is negatively
            targeted, meaning it matches ad requests that
            exclude the below values.

            This field is a member of `oneof`_ ``_negative``.
        audience_segments (MutableSequence[str]):
            Optional. The targeted audience segments.

            This is either the resource name of a first-party audience
            segment or an alias to the effective third-party audience
            segment. Third-party audience segment resource names
            containing ``~direct`` or ``~global`` will be normalized by
            the server. For example,
            ``networks/1234/audienceSegments/4567~direct`` will be
            normalized to ``networks/1234/audienceSegments/4567``.
    """

    negative: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    audience_segments: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class CmsMetadataTargeting(proto.Message):
    r"""Represents targeting for CMS metadata. The values are ORed
    together.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        negative (bool):
            Whether this expression is negatively
            targeted, meaning it matches ad requests that
            exclude the below values.

            This field is a member of `oneof`_ ``_negative``.
        cms_metadata_values (MutableSequence[str]):
            Optional. The resource names of the targeted
            CMS metadata values.
    """

    negative: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    cms_metadata_values: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
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


class ContentTargeting(proto.Message):
    r"""Content Targeting

    Targeted/excluded content entities and bundles.

    Attributes:
        targeted_content (MutableSequence[str]):
            Optional. The resource names of the
            [Content][google.ads.admanager.v1.Content] that should be
            targeted/included.
        excluded_content (MutableSequence[str]):
            Optional. The resource names of the
            [Content][google.ads.admanager.v1.Content] that should be
            excluded.
        targeted_content_bundles (MutableSequence[str]):
            Optional. The resource names of the
            [ContentBundles][google.ads.admanager.v1.ContentBundle] that
            should be targeted/included.
        excluded_content_bundles (MutableSequence[str]):
            Optional. The resource names of the
            [ContentBundles][google.ads.admanager.v1.ContentBundle] that
            should be excluded.
    """

    targeted_content: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    excluded_content: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    targeted_content_bundles: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    excluded_content_bundles: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )


class MobileApplicationTargeting(proto.Message):
    r"""Mobile Application Targeting

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        first_party_targeting (google.ads.admanager_v1.types.FirstPartyMobileApplicationTargeting):
            Optional. The targeted/excluded first-party
            mobile applications.

            This field is a member of `oneof`_ ``targeting``.
    """

    first_party_targeting: "FirstPartyMobileApplicationTargeting" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="targeting",
        message="FirstPartyMobileApplicationTargeting",
    )


class FirstPartyMobileApplicationTargeting(proto.Message):
    r"""First-party mobile application targeting.

    Attributes:
        targeted_applications (MutableSequence[str]):
            Optional. The resource names of the
            first-party applications that should be
            targeted.
        excluded_applications (MutableSequence[str]):
            Optional. The resource names of the
            first-party applications that should be
            excluded.
    """

    targeted_applications: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    excluded_applications: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
