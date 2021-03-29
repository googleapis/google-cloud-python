# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import proto  # type: ignore


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.resourcesettings.v1",
    manifest={
        "SettingValue",
        "Setting",
        "Value",
        "ListSettingsRequest",
        "ListSettingsResponse",
        "SearchSettingValuesRequest",
        "SearchSettingValuesResponse",
        "GetSettingValueRequest",
        "LookupEffectiveSettingValueRequest",
        "CreateSettingValueRequest",
        "UpdateSettingValueRequest",
        "DeleteSettingValueRequest",
    },
)


class SettingValue(proto.Message):
    r"""The instantiation of a setting. Every setting value is
    parented by its corresponding setting.

    Attributes:
        name (str):
            The resource name of the setting value. Must be in one of
            the following forms:

            -  ``projects/{project_number}/settings/{setting_name}/value``
            -  ``folders/{folder_id}/settings/{setting_name}/value``
            -  ``organizations/{organization_id}/settings/{setting_name}/value``

            For example,
            "/projects/123/settings/gcp-enableMyFeature/value".
        value (google.cloud.resourcesettings_v1.types.Value):
            The value of the setting. The data type of
            [Value][google.cloud.resourcesettings.v1.Value] must always
            be consistent with the data type defined by the parent
            setting.
        etag (str):
            A fingerprint used for optimistic concurrency. See
            [UpdateSettingValue][google.cloud.resourcesettings.v1.ResourceSettingsService.UpdateSettingValue]
            for more details.
        read_only (bool):
            Output only. A flag indicating that this setting value
            cannot be modified. This flag is inherited from its parent
            setting and is for convenience purposes. See
            [Setting.read_only][google.cloud.resourcesettings.v1.Setting.read_only]
            for more details.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp indicating when
            the setting value was last updated.
    """

    name = proto.Field(proto.STRING, number=1)

    value = proto.Field(proto.MESSAGE, number=2, message="Value",)

    etag = proto.Field(proto.STRING, number=3)

    read_only = proto.Field(proto.BOOL, number=4)

    update_time = proto.Field(proto.MESSAGE, number=5, message=timestamp.Timestamp,)


class Setting(proto.Message):
    r"""The schema for setting values. At a given Cloud resource, a
    setting can parent at most one setting value.

    Attributes:
        name (str):
            The resource name of the setting. Must be in one of the
            following forms:

            -  ``projects/{project_number}/settings/{setting_name}``
            -  ``folders/{folder_id}/settings/{setting_name}``
            -  ``organizations/{organization_id}/settings/{setting_name}``

            For example, "/projects/123/settings/gcp-enableMyFeature".
        display_name (str):
            The human readable name for this setting.
        description (str):
            A detailed description of what this setting
            does.
        read_only (bool):
            A flag indicating that values of this setting
            cannot be modified (see documentation of the
            specific setting for updates and reasons).
        data_type (google.cloud.resourcesettings_v1.types.Setting.DataType):
            The data type for this setting.
        default_value (google.cloud.resourcesettings_v1.types.Value):
            The value received by
            [LookupEffectiveSettingValue][google.cloud.resourcesettings.v1.ResourceSettingsService.LookupEffectiveSettingValue]
            if no setting value is explicitly set.

            Note: not all settings have a default value.
    """

    class DataType(proto.Enum):
        r"""The data type for setting values of this setting. See
        [Value][google.cloud.resourcesettings.v1.Value] for more details on
        the available data types.
        """
        DATA_TYPE_UNSPECIFIED = 0
        BOOLEAN = 1
        STRING = 2
        STRING_SET = 3
        ENUM_VALUE = 4

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    description = proto.Field(proto.STRING, number=3)

    read_only = proto.Field(proto.BOOL, number=4)

    data_type = proto.Field(proto.ENUM, number=5, enum=DataType,)

    default_value = proto.Field(proto.MESSAGE, number=6, message="Value",)


class Value(proto.Message):
    r"""The data in a setting value.

    Attributes:
        boolean_value (bool):
            Defines this value as being a boolean value.
        string_value (str):
            Defines this value as being a string value.
        string_set_value (google.cloud.resourcesettings_v1.types.Value.StringSet):
            Defines this value as being a StringSet.
        enum_value (google.cloud.resourcesettings_v1.types.Value.EnumValue):
            Defines this value as being a Enum.
    """

    class StringSet(proto.Message):
        r"""A string set value that can hold a set of strings. The
        maximum length of each string is 60 characters and there can be
        a maximum of 50 strings in the string set.

        Attributes:
            values (Sequence[str]):
                The strings in the set
        """

        values = proto.RepeatedField(proto.STRING, number=1)

    class EnumValue(proto.Message):
        r"""A enum value that can hold any enum type setting values.
        Each enum type is represented by a number, this representation
        is stored in the definitions.

        Attributes:
            value (str):

        """

        value = proto.Field(proto.STRING, number=1)

    boolean_value = proto.Field(proto.BOOL, number=1, oneof="value")

    string_value = proto.Field(proto.STRING, number=2, oneof="value")

    string_set_value = proto.Field(
        proto.MESSAGE, number=3, oneof="value", message=StringSet,
    )

    enum_value = proto.Field(proto.MESSAGE, number=4, oneof="value", message=EnumValue,)


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
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListSettingsResponse(proto.Message):
    r"""The response from ListSettings.

    Attributes:
        settings (Sequence[google.cloud.resourcesettings_v1.types.Setting]):
            A list of settings that are available at the
            specified Cloud resource.
        next_page_token (str):
            Unused. A page token used to retrieve the
            next page.
    """

    @property
    def raw_page(self):
        return self

    settings = proto.RepeatedField(proto.MESSAGE, number=1, message="Setting",)

    next_page_token = proto.Field(proto.STRING, number=2)


class SearchSettingValuesRequest(proto.Message):
    r"""The request for SearchSettingValues.

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
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class SearchSettingValuesResponse(proto.Message):
    r"""The response from SearchSettingValues.

    Attributes:
        setting_values (Sequence[google.cloud.resourcesettings_v1.types.SettingValue]):
            All setting values that exist on the
            specified Cloud resource.
        next_page_token (str):
            Unused. A page token used to retrieve the
            next page.
    """

    @property
    def raw_page(self):
        return self

    setting_values = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SettingValue",
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class GetSettingValueRequest(proto.Message):
    r"""The request for GetSettingValue.

    Attributes:
        name (str):
            Required. The name of the setting value to get. See
            [SettingValue][google.cloud.resourcesettings.v1.SettingValue]
            for naming requirements.
    """

    name = proto.Field(proto.STRING, number=1)


class LookupEffectiveSettingValueRequest(proto.Message):
    r"""The request for LookupEffectiveSettingValue.

    Attributes:
        name (str):
            Required. The setting value for which an effective value
            will be evaluated. See
            [SettingValue][google.cloud.resourcesettings.v1.SettingValue]
            for naming requirements.
    """

    name = proto.Field(proto.STRING, number=1)


class CreateSettingValueRequest(proto.Message):
    r"""The request for CreateSettingValue.

    Attributes:
        parent (str):
            Required. The name of the setting for which a value should
            be created. See
            [Setting][google.cloud.resourcesettings.v1.Setting] for
            naming requirements.
        setting_value (google.cloud.resourcesettings_v1.types.SettingValue):
            Required. The setting value to create. See
            [SettingValue][google.cloud.resourcesettings.v1.SettingValue]
            for field requirements.
    """

    parent = proto.Field(proto.STRING, number=1)

    setting_value = proto.Field(proto.MESSAGE, number=2, message="SettingValue",)


class UpdateSettingValueRequest(proto.Message):
    r"""The request for UpdateSettingValue.

    Attributes:
        setting_value (google.cloud.resourcesettings_v1.types.SettingValue):
            Required. The setting value to update. See
            [SettingValue][google.cloud.resourcesettings.v1.SettingValue]
            for field requirements.
    """

    setting_value = proto.Field(proto.MESSAGE, number=1, message="SettingValue",)


class DeleteSettingValueRequest(proto.Message):
    r"""The request for DeleteSettingValue.

    Attributes:
        name (str):
            Required. The name of the setting value to delete. See
            [SettingValue][google.cloud.resourcesettings.v1.SettingValue]
            for naming requirements.
    """

    name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
