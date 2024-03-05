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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.resourcesettings.v1",
    manifest={
        "SettingView",
        "Setting",
        "SettingMetadata",
        "Value",
        "ListSettingsRequest",
        "ListSettingsResponse",
        "GetSettingRequest",
        "UpdateSettingRequest",
    },
)


class SettingView(proto.Enum):
    r"""View options for Settings.

    Values:
        SETTING_VIEW_UNSPECIFIED (0):
            The default / unset value. The API will default to the
            SETTING_VIEW_BASIC view.
        SETTING_VIEW_BASIC (1):
            Include
            [Setting.metadata][google.cloud.resourcesettings.v1.Setting.metadata],
            but nothing else. This is the default value (for both
            ListSettings and GetSetting).
        SETTING_VIEW_EFFECTIVE_VALUE (2):
            Include
            [Setting.effective_value][google.cloud.resourcesettings.v1.Setting.effective_value],
            but nothing else.
        SETTING_VIEW_LOCAL_VALUE (3):
            Include
            [Setting.local_value][google.cloud.resourcesettings.v1.Setting.local_value],
            but nothing else.
    """
    SETTING_VIEW_UNSPECIFIED = 0
    SETTING_VIEW_BASIC = 1
    SETTING_VIEW_EFFECTIVE_VALUE = 2
    SETTING_VIEW_LOCAL_VALUE = 3


class Setting(proto.Message):
    r"""The schema for settings.

    Attributes:
        name (str):
            The resource name of the setting. Must be in one of the
            following forms:

            -  ``projects/{project_number}/settings/{setting_name}``
            -  ``folders/{folder_id}/settings/{setting_name}``
            -  ``organizations/{organization_id}/settings/{setting_name}``

            For example, "/projects/123/settings/gcp-enableMyFeature".
        metadata (google.cloud.resourcesettings_v1.types.SettingMetadata):
            Output only. Metadata about a setting which
            is not editable by the end user.
        local_value (google.cloud.resourcesettings_v1.types.Value):
            The configured value of the setting at the given parent
            resource (ignoring the resource hierarchy). The data type of
            [Value][google.cloud.resourcesettings.v1.Value] must always
            be consistent with the data type defined in
            [Setting.metadata][google.cloud.resourcesettings.v1.Setting.metadata].
        effective_value (google.cloud.resourcesettings_v1.types.Value):
            Output only. The computed effective value of the setting at
            the given parent resource (based on the resource hierarchy).

            The effective value evaluates to one of the following
            options in the given order (the next option is used if the
            previous one does not exist):

            1. the local setting value on the given resource:
               [Setting.local_value][google.cloud.resourcesettings.v1.Setting.local_value]
            2. if one of the given resource's ancestors have a local
               setting value, the local value at the nearest such
               ancestor
            3. the setting's default value:
               [SettingMetadata.default_value][google.cloud.resourcesettings.v1.SettingMetadata.default_value]
            4. an empty value (defined as a ``Value`` with all fields
               unset)

            The data type of
            [Value][google.cloud.resourcesettings.v1.Value] must always
            be consistent with the data type defined in
            [Setting.metadata][google.cloud.resourcesettings.v1.Setting.metadata].
        etag (str):
            A fingerprint used for optimistic concurrency. See
            [UpdateSetting][google.cloud.resourcesettings.v1.ResourceSettingsService.UpdateSetting]
            for more details.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    metadata: "SettingMetadata" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="SettingMetadata",
    )
    local_value: "Value" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="Value",
    )
    effective_value: "Value" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="Value",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=10,
    )


class SettingMetadata(proto.Message):
    r"""Metadata about a setting which is not editable by the end
    user.

    Attributes:
        display_name (str):
            The human readable name for this setting.
        description (str):
            A detailed description of what this setting
            does.
        read_only (bool):
            A flag indicating that values of this setting
            cannot be modified (see documentation of the
            specific setting for updates and reasons).
        data_type (google.cloud.resourcesettings_v1.types.SettingMetadata.DataType):
            The data type for this setting.
        default_value (google.cloud.resourcesettings_v1.types.Value):
            The value provided by
            [Setting.effective_value][google.cloud.resourcesettings.v1.Setting.effective_value]
            if no setting value is explicitly set.

            Note: not all settings have a default value.
    """

    class DataType(proto.Enum):
        r"""The data type for setting values of this setting. See
        [Value][google.cloud.resourcesettings.v1.Value] for more details on
        the available data types.

        Values:
            DATA_TYPE_UNSPECIFIED (0):
                Unspecified data type.
            BOOLEAN (1):
                A boolean setting.
            STRING (2):
                A string setting.
            STRING_SET (3):
                A string set setting.
            ENUM_VALUE (4):
                A Enum setting
        """
        DATA_TYPE_UNSPECIFIED = 0
        BOOLEAN = 1
        STRING = 2
        STRING_SET = 3
        ENUM_VALUE = 4

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    read_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    data_type: DataType = proto.Field(
        proto.ENUM,
        number=4,
        enum=DataType,
    )
    default_value: "Value" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="Value",
    )


class Value(proto.Message):
    r"""The data in a setting value.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        boolean_value (bool):
            Defines this value as being a boolean value.

            This field is a member of `oneof`_ ``value``.
        string_value (str):
            Defines this value as being a string value.

            This field is a member of `oneof`_ ``value``.
        string_set_value (google.cloud.resourcesettings_v1.types.Value.StringSet):
            Defines this value as being a StringSet.

            This field is a member of `oneof`_ ``value``.
        enum_value (google.cloud.resourcesettings_v1.types.Value.EnumValue):
            Defines this value as being a Enum.

            This field is a member of `oneof`_ ``value``.
    """

    class StringSet(proto.Message):
        r"""A string set value that can hold a set of strings. The
        maximum length of each string is 200 characters and there can be
        a maximum of 50 strings in the string set.

        Attributes:
            values (MutableSequence[str]):
                The strings in the set
        """

        values: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    class EnumValue(proto.Message):
        r"""A enum value that can hold any enum type setting values.
        Each enum type is represented by a number, this representation
        is stored in the definitions.

        Attributes:
            value (str):
                The value of this enum
        """

        value: str = proto.Field(
            proto.STRING,
            number=1,
        )

    boolean_value: bool = proto.Field(
        proto.BOOL,
        number=1,
        oneof="value",
    )
    string_value: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="value",
    )
    string_set_value: StringSet = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="value",
        message=StringSet,
    )
    enum_value: EnumValue = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="value",
        message=EnumValue,
    )


class ListSettingsRequest(proto.Message):
    r"""The request for ListSettings.

    Attributes:
        parent (str):
            Required. The Cloud resource that parents the setting. Must
            be in one of the following forms:

            -  ``projects/{project_number}``
            -  ``projects/{project_id}``
            -  ``folders/{folder_id}``
            -  ``organizations/{organization_id}``
        page_size (int):
            Unused. The size of the page to be returned.
        page_token (str):
            Unused. A page token used to retrieve the
            next page.
        view (google.cloud.resourcesettings_v1.types.SettingView):
            The SettingView for this request.
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
    view: "SettingView" = proto.Field(
        proto.ENUM,
        number=4,
        enum="SettingView",
    )


class ListSettingsResponse(proto.Message):
    r"""The response from ListSettings.

    Attributes:
        settings (MutableSequence[google.cloud.resourcesettings_v1.types.Setting]):
            A list of settings that are available at the
            specified Cloud resource.
        next_page_token (str):
            Unused. A page token used to retrieve the
            next page.
    """

    @property
    def raw_page(self):
        return self

    settings: MutableSequence["Setting"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Setting",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetSettingRequest(proto.Message):
    r"""The request for GetSetting.

    Attributes:
        name (str):
            Required. The name of the setting to get. See
            [Setting][google.cloud.resourcesettings.v1.Setting] for
            naming requirements.
        view (google.cloud.resourcesettings_v1.types.SettingView):
            The SettingView for this request.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: "SettingView" = proto.Field(
        proto.ENUM,
        number=2,
        enum="SettingView",
    )


class UpdateSettingRequest(proto.Message):
    r"""The request for UpdateSetting.

    Attributes:
        setting (google.cloud.resourcesettings_v1.types.Setting):
            Required. The setting to update. See
            [Setting][google.cloud.resourcesettings.v1.Setting] for
            field requirements.
    """

    setting: "Setting" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Setting",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
