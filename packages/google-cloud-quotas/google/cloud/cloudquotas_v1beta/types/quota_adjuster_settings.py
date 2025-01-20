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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.api.cloudquotas.v1beta",
    manifest={
        "GetQuotaAdjusterSettingsRequest",
        "UpdateQuotaAdjusterSettingsRequest",
        "QuotaAdjusterSettings",
    },
)


class GetQuotaAdjusterSettingsRequest(proto.Message):
    r"""Request for getting QuotaAdjusterSettings

    Attributes:
        name (str):
            Required. Name of the config. Required to be
            “settings”, as only a single setting per
            container will be supported initially.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateQuotaAdjusterSettingsRequest(proto.Message):
    r"""Request for updating QuotaAdjusterSettings

    Attributes:
        quota_adjuster_settings (google.cloud.cloudquotas_v1beta.types.QuotaAdjusterSettings):
            Required. The QuotaAdjusterSettings to
            update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The list of fields to update.
        validate_only (bool):
            Optional. If set to true, validate the
            request, but do not actually update. Note that a
            request being valid does not mean that the
            request is guaranteed to be fulfilled.
    """

    quota_adjuster_settings: "QuotaAdjusterSettings" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="QuotaAdjusterSettings",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class QuotaAdjusterSettings(proto.Message):
    r"""The QuotaAdjusterSettings resource defines the settings for
    the Quota Adjuster.

    Attributes:
        name (str):
            Identifier. Name of the config would be of
            the format:
            projects/12345/locations/global/quotaAdjusterSettings
        enablement (google.cloud.cloudquotas_v1beta.types.QuotaAdjusterSettings.Enablement):
            Required. The configured value of the
            enablement at the given resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the
            QuotaAdjusterSettings was last updated.
        etag (str):
            Optional. The current etag of the
            QuotaAdjusterSettings. If an etag is provided on
            update and does not match the current server's
            etag of the QuotaAdjusterSettings, the request
            will be blocked and an ABORTED error will be
            returned. See https://google.aip.dev/134#etags
            for more details on etags.
    """

    class Enablement(proto.Enum):
        r"""The enablement status of the quota adjuster.

        Values:
            ENABLEMENT_UNSPECIFIED (0):
                The quota adjuster is in an unknown state.
            ENABLED (2):
                The quota adjuster is enabled.
            DISABLED (3):
                The quota adjuster is disabled.
        """
        ENABLEMENT_UNSPECIFIED = 0
        ENABLED = 2
        DISABLED = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    enablement: Enablement = proto.Field(
        proto.ENUM,
        number=2,
        enum=Enablement,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=6,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
