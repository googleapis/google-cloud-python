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
    package="google.cloud.oslogin.common",
    manifest={
        "OperatingSystemType",
        "PosixAccount",
        "SshPublicKey",
    },
)


class OperatingSystemType(proto.Enum):
    r"""The operating system options for account entries.

    Values:
        OPERATING_SYSTEM_TYPE_UNSPECIFIED (0):
            The operating system type associated with the
            user account information is unspecified.
        LINUX (1):
            Linux user account information.
        WINDOWS (2):
            Windows user account information.
    """
    OPERATING_SYSTEM_TYPE_UNSPECIFIED = 0
    LINUX = 1
    WINDOWS = 2


class PosixAccount(proto.Message):
    r"""The POSIX account information associated with a Google
    account.

    Attributes:
        primary (bool):
            Only one POSIX account can be marked as
            primary.
        username (str):
            The username of the POSIX account.
        uid (int):
            The user ID.
        gid (int):
            The default group ID.
        home_directory (str):
            The path to the home directory for this
            account.
        shell (str):
            The path to the logic shell for this account.
        gecos (str):
            The GECOS (user information) entry for this
            account.
        system_id (str):
            System identifier for which account the
            username or uid applies to. By default, the
            empty value is used.
        account_id (str):
            Output only. A POSIX account identifier.
        operating_system_type (google.cloud.oslogin.common.types.OperatingSystemType):
            The operating system type where this account
            applies.
        name (str):
            Output only. The canonical resource name.
    """

    primary: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    username: str = proto.Field(
        proto.STRING,
        number=2,
    )
    uid: int = proto.Field(
        proto.INT64,
        number=3,
    )
    gid: int = proto.Field(
        proto.INT64,
        number=4,
    )
    home_directory: str = proto.Field(
        proto.STRING,
        number=5,
    )
    shell: str = proto.Field(
        proto.STRING,
        number=6,
    )
    gecos: str = proto.Field(
        proto.STRING,
        number=7,
    )
    system_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    account_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    operating_system_type: "OperatingSystemType" = proto.Field(
        proto.ENUM,
        number=10,
        enum="OperatingSystemType",
    )
    name: str = proto.Field(
        proto.STRING,
        number=11,
    )


class SshPublicKey(proto.Message):
    r"""The SSH public key information associated with a Google
    account.

    Attributes:
        key (str):
            Public key text in SSH format, defined by
            `RFC4253 <https://www.ietf.org/rfc/rfc4253.txt>`__ section
            6.6.
        expiration_time_usec (int):
            An expiration time in microseconds since
            epoch.
        fingerprint (str):
            Output only. The SHA-256 fingerprint of the
            SSH public key.
        name (str):
            Output only. The canonical resource name.
    """

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    expiration_time_usec: int = proto.Field(
        proto.INT64,
        number=2,
    )
    fingerprint: str = proto.Field(
        proto.STRING,
        number=3,
    )
    name: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
