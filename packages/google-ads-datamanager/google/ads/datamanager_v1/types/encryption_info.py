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
    package="google.ads.datamanager.v1",
    manifest={
        "EncryptionInfo",
        "GcpWrappedKeyInfo",
    },
)


class EncryptionInfo(proto.Message):
    r"""Encryption information for the data being ingested.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcp_wrapped_key_info (google.ads.datamanager_v1.types.GcpWrappedKeyInfo):
            Google Cloud Platform wrapped key
            information.

            This field is a member of `oneof`_ ``wrapped_key``.
    """

    gcp_wrapped_key_info: "GcpWrappedKeyInfo" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="wrapped_key",
        message="GcpWrappedKeyInfo",
    )


class GcpWrappedKeyInfo(proto.Message):
    r"""Information about the Google Cloud Platform wrapped
    key.

    Attributes:
        key_type (google.ads.datamanager_v1.types.GcpWrappedKeyInfo.KeyType):
            Required. The type of algorithm used to
            encrypt the data.
        wip_provider (str):
            Required. The `Workload
            Identity <//cloud.google.com/iam/docs/workload-identity-federation>`__
            pool provider required to use KEK.
        kek_uri (str):
            Required. Google Cloud Platform `Cloud Key Management
            Service resource
            ID <//cloud.google.com/kms/docs/getting-resource-ids>`__.
            Should be in the format of
            "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{key}".
        encrypted_dek (str):
            Required. The base64 encoded encrypted data
            encryption key.
    """

    class KeyType(proto.Enum):
        r"""The type of algorithm used to encrypt the data.

        Values:
            KEY_TYPE_UNSPECIFIED (0):
                Unspecified key type. Should never be used.
            XCHACHA20_POLY1305 (1):
                Algorithm XChaCha20-Poly1305
        """
        KEY_TYPE_UNSPECIFIED = 0
        XCHACHA20_POLY1305 = 1

    key_type: KeyType = proto.Field(
        proto.ENUM,
        number=1,
        enum=KeyType,
    )
    wip_provider: str = proto.Field(
        proto.STRING,
        number=2,
    )
    kek_uri: str = proto.Field(
        proto.STRING,
        number=3,
    )
    encrypted_dek: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
