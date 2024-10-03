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

from google.ads.admanager_v1.types import (
    ad_unit_enums,
    applied_label,
    environment_type_enum,
)
from google.ads.admanager_v1.types import frequency_cap as gaa_frequency_cap
from google.ads.admanager_v1.types import size as gaa_size

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "AdUnit",
        "AdUnitSize",
        "AdUnitParent",
        "LabelFrequencyCap",
    },
)


class AdUnit(proto.Message):
    r"""The AdUnit resource.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

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
            be assigned by Google based on the ad unit ID.
        status (google.ads.admanager_v1.types.AdUnitStatusEnum.AdUnitStatus):
            Output only. The status of this ad unit.  It
            defaults to ACTIVE.
        applied_target_window (google.ads.admanager_v1.types.TargetWindowEnum.TargetWindow):
            Optional. The target window directly applied
            to this AdUnit. If this field is not set, this
            AdUnit uses the target window specified in
            effectiveTargetWindow.
        effective_target_window (google.ads.admanager_v1.types.TargetWindowEnum.TargetWindow):
            Output only. Non-empty default. The target
            window of this AdUnit. This value is inherited
            from ancestor AdUnits and defaults to TOP if no
            AdUnit in the hierarchy specifies it.
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
            Output only. The time this AdUnit was last
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
        applied_adsense_enabled (bool):
            Optional. The value of AdSense enabled
            directly applied to this ad unit. This attribute
            is optional and if not specified this ad unit
            will inherit the value of
            effectiveAdsenseEnabled from its ancestors.

            This field is a member of `oneof`_ ``_applied_adsense_enabled``.
        effective_adsense_enabled (bool):
            Output only. Specifies whether or not the
            AdUnit is enabled for serving ads from the
            AdSense content network. This attribute defaults
            to the ad unit's parent or ancestor's setting if
            one has been set. If no ancestor of the ad unit
            has set appliedAdsenseEnabled, the attribute is
            defaulted to true.
    """

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
    status: ad_unit_enums.AdUnitStatusEnum.AdUnitStatus = proto.Field(
        proto.ENUM,
        number=13,
        enum=ad_unit_enums.AdUnitStatusEnum.AdUnitStatus,
    )
    applied_target_window: ad_unit_enums.TargetWindowEnum.TargetWindow = proto.Field(
        proto.ENUM,
        number=44,
        enum=ad_unit_enums.TargetWindowEnum.TargetWindow,
    )
    effective_target_window: ad_unit_enums.TargetWindowEnum.TargetWindow = proto.Field(
        proto.ENUM,
        number=45,
        enum=ad_unit_enums.TargetWindowEnum.TargetWindow,
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
    ad_unit_sizes: MutableSequence["AdUnitSize"] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message="AdUnitSize",
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
    smart_size_mode: ad_unit_enums.SmartSizeModeEnum.SmartSizeMode = proto.Field(
        proto.ENUM,
        number=25,
        enum=ad_unit_enums.SmartSizeModeEnum.SmartSizeMode,
    )
    applied_adsense_enabled: bool = proto.Field(
        proto.BOOL,
        number=26,
        optional=True,
    )
    effective_adsense_enabled: bool = proto.Field(
        proto.BOOL,
        number=27,
    )


class AdUnitSize(proto.Message):
    r"""Represents the size, environment, and companions of an ad in
    an ad unit.

    Attributes:
        size (google.ads.admanager_v1.types.Size):
            Required. The Size of the AdUnit.
        environment_type (google.ads.admanager_v1.types.EnvironmentTypeEnum.EnvironmentType):
            Required. The EnvironmentType of the AdUnit
        companions (MutableSequence[google.ads.admanager_v1.types.Size]):
            The companions for this ad unit size. Companions are only
            valid if the environment is
            [VIDEO_PLAYER][google.ads.admanager.v1.EnvironmentTypeEnum.EnvironmentType].
    """

    size: gaa_size.Size = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gaa_size.Size,
    )
    environment_type: environment_type_enum.EnvironmentTypeEnum.EnvironmentType = (
        proto.Field(
            proto.ENUM,
            number=2,
            enum=environment_type_enum.EnvironmentTypeEnum.EnvironmentType,
        )
    )
    companions: MutableSequence[gaa_size.Size] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=gaa_size.Size,
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


class LabelFrequencyCap(proto.Message):
    r"""Frequency cap using a label.

    Attributes:
        label (str):
            Required. The label to used for frequency capping. Format:
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


__all__ = tuple(sorted(__protobuf__.manifest))
