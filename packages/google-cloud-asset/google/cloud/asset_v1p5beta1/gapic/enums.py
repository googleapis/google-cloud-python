# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class ContentType(enum.IntEnum):
    """
    Asset content type.

    Attributes:
      CONTENT_TYPE_UNSPECIFIED (int): Unspecified content type.
      RESOURCE (int): Resource metadata.
      IAM_POLICY (int): The actual IAM policy set on a resource.
      ORG_POLICY (int): The Cloud Organization Policy set on an asset.
      ACCESS_POLICY (int): The Cloud Access context mananger Policy set on an asset.
    """

    CONTENT_TYPE_UNSPECIFIED = 0
    RESOURCE = 1
    IAM_POLICY = 2
    ORG_POLICY = 4
    ACCESS_POLICY = 5


class DeviceEncryptionStatus(enum.IntEnum):
    """
    The encryption state of the device.

    Attributes:
      ENCRYPTION_UNSPECIFIED (int): The encryption status of the device is not specified or not known.
      ENCRYPTION_UNSUPPORTED (int): The device does not support encryption.
      UNENCRYPTED (int): The device supports encryption, but is currently unencrypted.
      ENCRYPTED (int): The device is encrypted.
    """

    ENCRYPTION_UNSPECIFIED = 0
    ENCRYPTION_UNSUPPORTED = 1
    UNENCRYPTED = 2
    ENCRYPTED = 3


class DeviceManagementLevel(enum.IntEnum):
    """
    The degree to which the device is managed by the Cloud organization.

    Attributes:
      MANAGEMENT_UNSPECIFIED (int): The device's management level is not specified or not known.
      NONE (int): The device is not managed.
      BASIC (int): Basic management is enabled, which is generally limited to monitoring and
      wiping the corporate account.
      COMPLETE (int): Complete device management. This includes more thorough monitoring and the
      ability to directly manage the device (such as remote wiping). This can be
      enabled through the Android Enterprise Platform.
    """

    MANAGEMENT_UNSPECIFIED = 0
    NONE = 1
    BASIC = 2
    COMPLETE = 3


class NullValue(enum.IntEnum):
    """
    ``NullValue`` is a singleton enumeration to represent the null value
    for the ``Value`` type union.

    The JSON representation for ``NullValue`` is JSON ``null``.

    Attributes:
      NULL_VALUE (int): Null value.
    """

    NULL_VALUE = 0


class OsType(enum.IntEnum):
    """
    The operating system type of the device.
    Next id: 7

    Attributes:
      OS_UNSPECIFIED (int): The operating system of the device is not specified or not known.
      DESKTOP_MAC (int): A desktop Mac operating system.
      DESKTOP_WINDOWS (int): A desktop Windows operating system.
      DESKTOP_LINUX (int): A desktop Linux operating system.
      DESKTOP_CHROME_OS (int): A desktop ChromeOS operating system.
      ANDROID (int): An Android operating system.
      IOS (int): An iOS operating system.
    """

    OS_UNSPECIFIED = 0
    DESKTOP_MAC = 1
    DESKTOP_WINDOWS = 2
    DESKTOP_LINUX = 3
    DESKTOP_CHROME_OS = 6
    ANDROID = 4
    IOS = 5


class BasicLevel(object):
    class ConditionCombiningFunction(enum.IntEnum):
        """
        Options for how the ``conditions`` list should be combined to
        determine if this ``AccessLevel`` is applied. Default is AND.

        Attributes:
          AND (int): All ``Conditions`` must be true for the ``BasicLevel`` to be true.
          OR (int): If at least one ``Condition`` is true, then the ``BasicLevel`` is
          true.
        """

        AND = 0
        OR = 1


class Policy(object):
    class ListPolicy(object):
        class AllValues(enum.IntEnum):
            """
            This enum can be used to set ``Policies`` that apply to all possible
            configuration values rather than specific values in ``allowed_values``
            or ``denied_values``.

            Settting this to ``ALLOW`` will mean this ``Policy`` allows all values.
            Similarly, setting it to ``DENY`` will mean no values are allowed. If
            set to either ``ALLOW`` or
            ``DENY,``\ allowed_values\ ``and``\ denied_values\ ``must be unset. Setting this to``\ ALL_VALUES_UNSPECIFIED\ ``allows for setting``\ allowed_values\ ``and``\ denied_values`.

            Attributes:
              ALL_VALUES_UNSPECIFIED (int): Indicates that allowed_values or denied_values must be set.
              ALLOW (int): A policy with this set allows all values.
              DENY (int): A policy with this set denies all values.
            """

            ALL_VALUES_UNSPECIFIED = 0
            ALLOW = 1
            DENY = 2


class ServicePerimeter(object):
    class PerimeterType(enum.IntEnum):
        """
        Specifies the type of the Perimeter. There are two types: regular and
        bridge. Regular Service Perimeter contains resources, access levels, and
        restricted services. Every resource can be in at most ONE
        regular Service Perimeter.

        In addition to being in a regular service perimeter, a resource can also
        be in zero or more perimeter bridges.  A perimeter bridge only contains
        resources.  Cross project operations are permitted if all effected
        resources share some perimeter (whether bridge or regular). Perimeter
        Bridge does not contain access levels or services: those are governed
        entirely by the regular perimeter that resource is in.

        Perimeter Bridges are typically useful when building more complex toplogies
        with many independent perimeters that need to share some data with a common
        perimeter, but should not be able to share data among themselves.

        Attributes:
          PERIMETER_TYPE_REGULAR (int): Regular Perimeter.
          PERIMETER_TYPE_BRIDGE (int): Perimeter Bridge.
        """

        PERIMETER_TYPE_REGULAR = 0
        PERIMETER_TYPE_BRIDGE = 1
