# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import ad_unit_enums, ad_unit_size, applied_label
from google.ads.admanager_v1.types import frequency_cap as gaa_frequency_cap

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "AdUnit",
        "AdUnitParent",
        "TargetWindowEnum",
        "LabelFrequencyCap",
        "SmartSizeModeEnum",
        "GetAdUnitRequest",
        "ListAdUnitsRequest",
        "ListAdUnitsResponse",
    },
)


class AdUnit(proto.Message):
    r"""The AdUnit resource.

    Attributes:
        name (str):
            Identifier. The resource name of the AdUnit. Format:
            ``networks/{network_code}/adUnits/{ad_unit_id}``
        ad_unit_id (int):
            Output only. AdUnit ID.
        parent_ad_unit (str):
            Required. Immutable. The AdUnit's parent. Every ad unit has
            a parent except for the root ad unit, which is created by
            Google. Format:
            "networks/{network_code}/adUnits/{ad_unit_id}".
        parent_path (MutableSequence[google.ads.admanager_v1.types.AdUnitParent]):
            Output only. The path to this AdUnit in the
            ad unit hierarchy represented as a list from the
            root to this ad unit's parent. For root ad
            units, this list is empty.
        display_name (str):
            Required. The display name of the ad unit.
            Its maximum length is 255 characters.
        ad_unit_code (str):
            Immutable. A string used to uniquely identify
            the ad unit for the purposes of serving the ad.
            This attribute is optional and can be set during
            ad unit creation. If it is not provided, it will
            be assigned by Google based off of the ad unit
            ID.
        status (google.ads.admanager_v1.types.AdUnit.Status):
            Output only. The status of this ad unit.  It
            defaults to ACTIVE.
        target_window (google.ads.admanager_v1.types.TargetWindowEnum.TargetWindow):
            Non-empty default. The value to use for the
            HTML link's target attribute. This value will be
            interpreted as TOP if left blank.
        applied_teams (MutableSequence[str]):
            Optional. The resource names of Teams directly applied to
            this AdUnit. Format:
            "networks/{network_code}/teams/{team_id}".
        teams (MutableSequence[str]):
            Output only. The resource names of all Teams that this
            AdUnit is on as well as those inherited from parent AdUnits.
            Format: "networks/{network_code}/teams/{team_id}".
        description (str):
            Optional. A description of the ad unit. The
            maximum length is 65,535 characters.
        explicitly_targeted (bool):
            Optional. If this field is set to true, then
            the AdUnit will not be implicitly targeted when
            its parent is. Traffickers must explicitly
            target such an AdUnit or else no line items will
            serve to it. This feature is only available for
            Ad Manager 360 accounts.
        has_children (bool):
            Output only. This field is set to true if the
            ad unit has any children.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant this AdUnit was last
            modified.
        ad_unit_sizes (MutableSequence[google.ads.admanager_v1.types.AdUnitSize]):
            Optional. The sizes that can be served inside
            this ad unit.
        external_set_top_box_channel_id (str):
            Optional. Determines what set top box video
            on demand channel this ad unit corresponds to in
            an external set top box ad campaign system.
        refresh_delay (google.protobuf.duration_pb2.Duration):
            Optional. The duration after which an Ad Unit
            will automatically refresh. This is only valid
            for ad units in mobile apps. If not set, the ad
            unit will not refresh.
        ctv_application_id (int):
            Optional. The ID of the CTV application that
            this ad unit is within.
        applied_labels (MutableSequence[google.ads.admanager_v1.types.AppliedLabel]):
            Optional. The set of labels applied directly
            to this ad unit.
        effective_applied_labels (MutableSequence[google.ads.admanager_v1.types.AppliedLabel]):
            Output only. Contains the set of labels
            applied directly to the ad unit as well as those
            inherited from the parent ad units. If a label
            has been negated, only the negated label is
            returned. This field is readonly and is assigned
            by Google.
        applied_label_frequency_caps (MutableSequence[google.ads.admanager_v1.types.LabelFrequencyCap]):
            Optional. The set of label frequency caps
            applied directly to this ad unit. There is a
            limit of 10 label frequency caps per ad unit.
        effective_label_frequency_caps (MutableSequence[google.ads.admanager_v1.types.LabelFrequencyCap]):
            Output only. The label frequency caps applied
            directly to the ad unit as well as those
            inherited from parent ad units.
        smart_size_mode (google.ads.admanager_v1.types.SmartSizeModeEnum.SmartSizeMode):
            Optional. The smart size mode for this ad
            unit. This attribute is optional and defaults to
            SmartSizeMode.NONE for fixed sizes.
        applied_adsense_enabled (google.ads.admanager_v1.types.AppliedAdsenseEnabledEnum.AppliedAdsenseEnabled):
            Optional. The value of AdSense enabled
            directly applied to this ad unit. This attribute
            is optional and if not specified this ad unit
            will inherit the value of
            effectiveAdsenseEnabled from its ancestors.
        effective_adsense_enabled (bool):
            Output only. Specifies whether or not the
            AdUnit is enabled for serving ads from the
            AdSense content network. This attribute defaults
            to the ad unit's parent or ancestor's setting if
            one has been set. If no ancestor of the ad unit
            has set appliedAdsenseEnabled, the attribute is
            defaulted to true.
    """

    class Status(proto.Enum):
        r"""The status of an AdUnit.

        Values:
            STATUS_UNSPECIFIED (0):
                Default value. This value is unused.
            ACTIVE (1):
                The ad unit is active, available for
                targeting, and serving.
            INACTIVE (2):
                The ad unit will be visible in the UI, but
                ignored by serving.
            ARCHIVED (3):
                The ad unit will be hidden in the UI and
                ignored by serving.
        """
        STATUS_UNSPECIFIED = 0
        ACTIVE = 1
        INACTIVE = 2
        ARCHIVED = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ad_unit_id: int = proto.Field(
        proto.INT64,
        number=15,
    )
    parent_ad_unit: str = proto.Field(
        proto.STRING,
        number=10,
    )
    parent_path: MutableSequence["AdUnitParent"] = proto.RepeatedField(
        proto.MESSAGE,
        number=11,
        message="AdUnitParent",
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=9,
    )
    ad_unit_code: str = proto.Field(
        proto.STRING,
        number=2,
    )
    status: Status = proto.Field(
        proto.ENUM,
        number=13,
        enum=Status,
    )
    target_window: "TargetWindowEnum.TargetWindow" = proto.Field(
        proto.ENUM,
        number=12,
        enum="TargetWindowEnum.TargetWindow",
    )
    applied_teams: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    teams: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    explicitly_targeted: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    has_children: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    ad_unit_sizes: MutableSequence[ad_unit_size.AdUnitSize] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message=ad_unit_size.AdUnitSize,
    )
    external_set_top_box_channel_id: str = proto.Field(
        proto.STRING,
        number=17,
    )
    refresh_delay: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=19,
        message=duration_pb2.Duration,
    )
    ctv_application_id: int = proto.Field(
        proto.INT64,
        number=20,
    )
    applied_labels: MutableSequence[applied_label.AppliedLabel] = proto.RepeatedField(
        proto.MESSAGE,
        number=21,
        message=applied_label.AppliedLabel,
    )
    effective_applied_labels: MutableSequence[
        applied_label.AppliedLabel
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=22,
        message=applied_label.AppliedLabel,
    )
    applied_label_frequency_caps: MutableSequence[
        "LabelFrequencyCap"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=23,
        message="LabelFrequencyCap",
    )
    effective_label_frequency_caps: MutableSequence[
        "LabelFrequencyCap"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=24,
        message="LabelFrequencyCap",
    )
    smart_size_mode: "SmartSizeModeEnum.SmartSizeMode" = proto.Field(
        proto.ENUM,
        number=25,
        enum="SmartSizeModeEnum.SmartSizeMode",
    )
    applied_adsense_enabled: ad_unit_enums.AppliedAdsenseEnabledEnum.AppliedAdsenseEnabled = proto.Field(
        proto.ENUM,
        number=26,
        enum=ad_unit_enums.AppliedAdsenseEnabledEnum.AppliedAdsenseEnabled,
    )
    effective_adsense_enabled: bool = proto.Field(
        proto.BOOL,
        number=27,
    )


class AdUnitParent(proto.Message):
    r"""The summary of a parent AdUnit.

    Attributes:
        parent_ad_unit (str):
            Output only. The parent of the current AdUnit Format:
            ``networks/{network_code}/adUnits/{ad_unit_id}``
        display_name (str):
            Output only. The display name of the parent
            AdUnit.
        ad_unit_code (str):
            Output only. A string used to uniquely
            identify the ad unit for the purposes of serving
            the ad.
    """

    parent_ad_unit: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    ad_unit_code: str = proto.Field(
        proto.STRING,
        number=3,
    )


class TargetWindowEnum(proto.Message):
    r"""Wrapper message for
    [TargetWindow][google.ads.admanager.v1.TargetWindowEnum.TargetWindow].

    """

    class TargetWindow(proto.Enum):
        r"""Corresponds to an HTML link's target attribute.
        See http://www.w3.org/TR/html401/present/frames.html#adef-target

        Values:
            TARGET_WINDOW_UNSPECIFIED (0):
                Default value. This value is unused.
            TOP (1):
                Specifies that the link should open in the
                full body of the page.
            BLANK (2):
                Specifies that the link should open in a new
                window.
        """
        TARGET_WINDOW_UNSPECIFIED = 0
        TOP = 1
        BLANK = 2


class LabelFrequencyCap(proto.Message):
    r"""Frequency cap using a label.

    Attributes:
        label (str):
            The label to used for frequency capping. Format:
            "networks/{network_code}/labels/{label_id}".
        frequency_cap (google.ads.admanager_v1.types.FrequencyCap):
            The frequency cap.
    """

    label: str = proto.Field(
        proto.STRING,
        number=1,
    )
    frequency_cap: gaa_frequency_cap.FrequencyCap = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gaa_frequency_cap.FrequencyCap,
    )


class SmartSizeModeEnum(proto.Message):
    r"""Wrapper message for
    [SmartSizeMode][google.ads.admanager.v1.SmartSizeModeEnum.SmartSizeMode].

    """

    class SmartSizeMode(proto.Enum):
        r"""The smart size mode for this ad unit. This attribute is
        optional and defaults to SmartSizeMode.NONE for fixed sizes.

        Values:
            SMART_SIZE_MODE_UNSPECIFIED (0):
                Default value. This value is unused.
            NONE (1):
                Fixed size mode (default).
            SMART_BANNER (2):
                The height is fixed for the request, the
                width is a range.
            DYNAMIC_SIZE (3):
                Height and width are ranges.
        """
        SMART_SIZE_MODE_UNSPECIFIED = 0
        NONE = 1
        SMART_BANNER = 2
        DYNAMIC_SIZE = 3


class GetAdUnitRequest(proto.Message):
    r"""Request object for GetAdUnit method.

    Attributes:
        name (str):
            Required. The resource name of the AdUnit. Format:
            ``networks/{network_code}/adUnits/{ad_unit_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAdUnitsRequest(proto.Message):
    r"""Request object for ListAdUnits method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of AdUnits.
            Format: ``networks/{network_code}``
        page_size (int):
            Optional. The maximum number of AdUnits to
            return. The service may return fewer than this
            value. If unspecified, at most 50 ad units will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListAdUnits`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListAdUnits`` must match the call that provided the page
            token.
        filter (str):
            Optional. Expression to filter the response.
            See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters
        order_by (str):
            Optional. Expression to specify sorting
            order. See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters#order
        skip (int):
            Optional. Number of individual resources to
            skip while paginating.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    skip: int = proto.Field(
        proto.INT32,
        number=6,
    )


class ListAdUnitsResponse(proto.Message):
    r"""Response object for ListAdUnitsRequest containing matching
    AdUnit resources.

    Attributes:
        ad_units (MutableSequence[google.ads.admanager_v1.types.AdUnit]):
            The AdUnit from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of AdUnits. If a filter was included in the
            request, this reflects the total number after the filtering
            is applied.

            ``total_size`` will not be calculated in the response unless
            it has been included in a response field mask. The response
            field mask can be provided to the method by using the URL
            parameter ``$fields`` or ``fields``, or by using the
            HTTP/gRPC header ``X-Goog-FieldMask``.

            For more information, see
            https://developers.google.com/ad-manager/api/beta/field-masks
    """

    @property
    def raw_page(self):
        return self

    ad_units: MutableSequence["AdUnit"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AdUnit",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
