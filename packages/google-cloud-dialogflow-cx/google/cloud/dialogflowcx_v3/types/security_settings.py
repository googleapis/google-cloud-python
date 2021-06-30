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

from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3",
    manifest={
        "GetSecuritySettingsRequest",
        "UpdateSecuritySettingsRequest",
        "ListSecuritySettingsRequest",
        "ListSecuritySettingsResponse",
        "CreateSecuritySettingsRequest",
        "DeleteSecuritySettingsRequest",
        "SecuritySettings",
    },
)


class GetSecuritySettingsRequest(proto.Message):
    r"""The request message for
    [SecuritySettingsService.GetSecuritySettings][google.cloud.dialogflow.cx.v3.SecuritySettingsService.GetSecuritySettings].

    Attributes:
        name (str):
            Required. Resource name of the settings. Format:
            ``projects/<Project ID>/locations/<Location ID>/securitySettings/<security settings ID>``.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateSecuritySettingsRequest(proto.Message):
    r"""The request message for
    [SecuritySettingsService.UpdateSecuritySettings][google.cloud.dialogflow.cx.v3.SecuritySettingsService.UpdateSecuritySettings].

    Attributes:
        security_settings (google.cloud.dialogflowcx_v3.types.SecuritySettings):
            Required. [SecuritySettings] object that contains values for
            each of the fields to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The mask to control which fields
            get updated. If the mask is not present, all
            fields will be updated.
    """

    security_settings = proto.Field(
        proto.MESSAGE, number=1, message="SecuritySettings",
    )
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class ListSecuritySettingsRequest(proto.Message):
    r"""The request message for [SecuritySettings.ListSecuritySettings][].
    Attributes:
        parent (str):
            Required. The location to list all security settings for.
            Format: ``projects/<Project ID>/locations/<Location ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 20 and at most 100.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListSecuritySettingsResponse(proto.Message):
    r"""The response message for [SecuritySettings.ListSecuritySettings][].
    Attributes:
        security_settings (Sequence[google.cloud.dialogflowcx_v3.types.SecuritySettings]):
            The list of security settings.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    security_settings = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SecuritySettings",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class CreateSecuritySettingsRequest(proto.Message):
    r"""The request message for [SecuritySettings.CreateSecuritySettings][].
    Attributes:
        parent (str):
            Required. The location to create an
            [SecuritySettings][google.cloud.dialogflow.cx.v3.SecuritySettings]
            for. Format:
            ``projects/<Project ID>/locations/<Location ID>``.
        security_settings (google.cloud.dialogflowcx_v3.types.SecuritySettings):
            Required. The security settings to create.
    """

    parent = proto.Field(proto.STRING, number=1,)
    security_settings = proto.Field(
        proto.MESSAGE, number=2, message="SecuritySettings",
    )


class DeleteSecuritySettingsRequest(proto.Message):
    r"""The request message for [SecuritySettings.DeleteSecuritySettings][].
    Attributes:
        name (str):
            Required. The name of the
            [SecuritySettings][google.cloud.dialogflow.cx.v3.SecuritySettings]
            to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/securitySettings/<Security Settings ID>``.
    """

    name = proto.Field(proto.STRING, number=1,)


class SecuritySettings(proto.Message):
    r"""Represents the settings related to security issues, such as
    data redaction and data retention. It may take hours for updates
    on the settings to propagate to all the related components and
    take effect.

    Attributes:
        name (str):
            Required. Resource name of the settings. Format:
            ``projects/<Project ID>/locations/<Location ID>/securitySettings/<Security Settings ID>``.
        display_name (str):
            Required. The human-readable name of the
            security settings, unique within the location.
        redaction_strategy (google.cloud.dialogflowcx_v3.types.SecuritySettings.RedactionStrategy):
            Strategy that defines how we do redaction.
        redaction_scope (google.cloud.dialogflowcx_v3.types.SecuritySettings.RedactionScope):
            Defines the data for which Dialogflow applies
            redaction. Dialogflow does not redact data that
            it does not have access to – for example, Cloud
            logging.
        inspect_template (str):
            DLP inspect template name. Use this template to define
            inspect base settings.

            If empty, we use the default DLP inspect config.

            The template name will have one of the following formats:
            ``projects/<Project ID>/inspectTemplates/<Template ID>`` OR
            ``projects/<Project ID>/locations/<Location ID>/inspectTemplates/<Template ID>``
            OR
            ``organizations/<Organization ID>/inspectTemplates/<Template ID>``
        retention_window_days (int):
            Retains data in interaction logging for the
            specified number of days. This does not apply to
            Cloud logging, which is owned by the user - not
            Dialogflow.
            User must Set a value lower than Dialogflow's
            default 30d TTL. Setting a value higher than
            that has no effect.
            A missing value or setting to 0 also means we
            use Dialogflow's default TTL.
            Note: Interaction logging is a limited access
            feature. Talk to your Google representative to
            check availability for you.
        purge_data_types (Sequence[google.cloud.dialogflowcx_v3.types.SecuritySettings.PurgeDataType]):
            List of types of data to remove when
            retention settings triggers purge.
    """

    class RedactionStrategy(proto.Enum):
        r"""Defines how we redact data."""
        REDACTION_STRATEGY_UNSPECIFIED = 0
        REDACT_WITH_SERVICE = 1

    class RedactionScope(proto.Enum):
        r"""Defines what types of data to redact."""
        REDACTION_SCOPE_UNSPECIFIED = 0
        REDACT_DISK_STORAGE = 2

    class PurgeDataType(proto.Enum):
        r"""Type of data we purge after retention settings triggers
        purge.
        """
        PURGE_DATA_TYPE_UNSPECIFIED = 0
        DIALOGFLOW_HISTORY = 1

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    redaction_strategy = proto.Field(proto.ENUM, number=3, enum=RedactionStrategy,)
    redaction_scope = proto.Field(proto.ENUM, number=4, enum=RedactionScope,)
    inspect_template = proto.Field(proto.STRING, number=9,)
    retention_window_days = proto.Field(proto.INT32, number=6, oneof="data_retention",)
    purge_data_types = proto.RepeatedField(proto.ENUM, number=8, enum=PurgeDataType,)


__all__ = tuple(sorted(__protobuf__.manifest))
