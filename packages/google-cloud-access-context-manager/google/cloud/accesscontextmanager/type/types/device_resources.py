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
    package="google.cloud.accesscontextmanager.type",
    manifest={
        "DeviceEncryptionStatus",
        "OsType",
        "DeviceManagementLevel",
    },
)


class DeviceEncryptionStatus(proto.Enum):
    r"""The encryption state of the device.

    Values:
        ENCRYPTION_UNSPECIFIED (0):
            The encryption status of the device is not
            specified or not known.
        ENCRYPTION_UNSUPPORTED (1):
            The device does not support encryption.
        UNENCRYPTED (2):
            The device supports encryption, but is
            currently unencrypted.
        ENCRYPTED (3):
            The device is encrypted.
    """
    ENCRYPTION_UNSPECIFIED = 0
    ENCRYPTION_UNSUPPORTED = 1
    UNENCRYPTED = 2
    ENCRYPTED = 3


class OsType(proto.Enum):
    r"""The operating system type of the device.
    Next id: 7

    Values:
        OS_UNSPECIFIED (0):
            The operating system of the device is not
            specified or not known.
        DESKTOP_MAC (1):
            A desktop Mac operating system.
        DESKTOP_WINDOWS (2):
            A desktop Windows operating system.
        DESKTOP_LINUX (3):
            A desktop Linux operating system.
        DESKTOP_CHROME_OS (6):
            A desktop ChromeOS operating system.
        ANDROID (4):
            An Android operating system.
        IOS (5):
            An iOS operating system.
    """
    OS_UNSPECIFIED = 0
    DESKTOP_MAC = 1
    DESKTOP_WINDOWS = 2
    DESKTOP_LINUX = 3
    DESKTOP_CHROME_OS = 6
    ANDROID = 4
    IOS = 5


class DeviceManagementLevel(proto.Enum):
    r"""The degree to which the device is managed by the Cloud
    organization.

    Values:
        MANAGEMENT_UNSPECIFIED (0):
            The device's management level is not
            specified or not known.
        NONE (1):
            The device is not managed.
        BASIC (2):
            Basic management is enabled, which is
            generally limited to monitoring and wiping the
            corporate account.
        COMPLETE (3):
            Complete device management. This includes
            more thorough monitoring and the ability to
            directly manage the device (such as remote
            wiping). This can be enabled through the Android
            Enterprise Platform.
    """
    MANAGEMENT_UNSPECIFIED = 0
    NONE = 1
    BASIC = 2
    COMPLETE = 3


__all__ = tuple(sorted(__protobuf__.manifest))
