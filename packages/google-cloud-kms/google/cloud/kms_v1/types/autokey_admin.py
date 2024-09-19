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
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.kms.v1",
    manifest={
        "UpdateAutokeyConfigRequest",
        "GetAutokeyConfigRequest",
        "AutokeyConfig",
        "ShowEffectiveAutokeyConfigRequest",
        "ShowEffectiveAutokeyConfigResponse",
    },
)


class UpdateAutokeyConfigRequest(proto.Message):
    r"""Request message for
    [UpdateAutokeyConfig][google.cloud.kms.v1.AutokeyAdmin.UpdateAutokeyConfig].

    Attributes:
        autokey_config (google.cloud.kms_v1.types.AutokeyConfig):
            Required. [AutokeyConfig][google.cloud.kms.v1.AutokeyConfig]
            with values to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Masks which fields of the
            [AutokeyConfig][google.cloud.kms.v1.AutokeyConfig] to
            update, e.g. ``keyProject``.
    """

    autokey_config: "AutokeyConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="AutokeyConfig",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetAutokeyConfigRequest(proto.Message):
    r"""Request message for
    [GetAutokeyConfig][google.cloud.kms.v1.AutokeyAdmin.GetAutokeyConfig].

    Attributes:
        name (str):
            Required. Name of the
            [AutokeyConfig][google.cloud.kms.v1.AutokeyConfig] resource,
            e.g. ``folders/{FOLDER_NUMBER}/autokeyConfig``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AutokeyConfig(proto.Message):
    r"""Cloud KMS Autokey configuration for a folder.

    Attributes:
        name (str):
            Identifier. Name of the
            [AutokeyConfig][google.cloud.kms.v1.AutokeyConfig] resource,
            e.g. ``folders/{FOLDER_NUMBER}/autokeyConfig``.
        key_project (str):
            Optional. Name of the key project, e.g.
            ``projects/{PROJECT_ID}`` or ``projects/{PROJECT_NUMBER}``,
            where Cloud KMS Autokey will provision a new
            [CryptoKey][google.cloud.kms.v1.CryptoKey] when a
            [KeyHandle][google.cloud.kms.v1.KeyHandle] is created. On
            [UpdateAutokeyConfig][google.cloud.kms.v1.AutokeyAdmin.UpdateAutokeyConfig],
            the caller will require ``cloudkms.cryptoKeys.setIamPolicy``
            permission on this key project. Once configured, for Cloud
            KMS Autokey to function properly, this key project must have
            the Cloud KMS API activated and the Cloud KMS Service Agent
            for this key project must be granted the ``cloudkms.admin``
            role (or pertinent permissions). A request with an empty key
            project field will clear the configuration.
        state (google.cloud.kms_v1.types.AutokeyConfig.State):
            Output only. The state for the AutokeyConfig.
    """

    class State(proto.Enum):
        r"""The states AutokeyConfig can be in.

        Values:
            STATE_UNSPECIFIED (0):
                The state of the AutokeyConfig is
                unspecified.
            ACTIVE (1):
                The AutokeyConfig is currently active.
            KEY_PROJECT_DELETED (2):
                A previously configured key project has been
                deleted and the current AutokeyConfig is
                unusable.
            UNINITIALIZED (3):
                The AutokeyConfig is not yet initialized or
                has been reset to its default uninitialized
                state.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        KEY_PROJECT_DELETED = 2
        UNINITIALIZED = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    key_project: str = proto.Field(
        proto.STRING,
        number=2,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )


class ShowEffectiveAutokeyConfigRequest(proto.Message):
    r"""Request message for
    [ShowEffectiveAutokeyConfig][google.cloud.kms.v1.AutokeyAdmin.ShowEffectiveAutokeyConfig].

    Attributes:
        parent (str):
            Required. Name of the resource project to the
            show effective Cloud KMS Autokey configuration
            for. This may be helpful for interrogating the
            effect of nested folder configurations on a
            given resource project.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ShowEffectiveAutokeyConfigResponse(proto.Message):
    r"""Response message for
    [ShowEffectiveAutokeyConfig][google.cloud.kms.v1.AutokeyAdmin.ShowEffectiveAutokeyConfig].

    Attributes:
        key_project (str):
            Name of the key project configured in the
            resource project's folder ancestry.
    """

    key_project: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
