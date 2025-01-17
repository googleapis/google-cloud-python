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

from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import proto  # type: ignore

from google.identity.accesscontextmanager.type import (
    device_resources_pb2,
)  # type: ignore

__protobuf__ = proto.module(
    package="google.identity.accesscontextmanager.v1",
    manifest={
        "AccessLevel",
        "BasicLevel",
        "Condition",
        "CustomLevel",
        "DevicePolicy",
        "OsConstraint",
    },
)


class AccessLevel(proto.Message):
    r"""An ``AccessLevel`` is a label that can be applied to requests to
    Google Cloud services, along with a list of requirements necessary
    for the label to be applied.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Resource name for the Access Level. The
            ``short_name`` component must begin with a letter and only
            include alphanumeric and '_'. Format:
            ``accessPolicies/{access_policy}/accessLevels/{access_level}``.
            The maximum length of the ``access_level`` component is 50
            characters.
        title (str):
            Human readable title. Must be unique within
            the Policy.
        description (str):
            Description of the ``AccessLevel`` and its use. Does not
            affect behavior.
        basic (google.cloud.accesscontextmanager_v1.types.BasicLevel):
            A ``BasicLevel`` composed of ``Conditions``.

            This field is a member of `oneof`_ ``level``.
        custom (google.cloud.accesscontextmanager_v1.types.CustomLevel):
            A ``CustomLevel`` written in the Common Expression Language.

            This field is a member of `oneof`_ ``level``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the ``AccessLevel`` was created in UTC.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the ``AccessLevel`` was updated in UTC.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    title: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    basic: "BasicLevel" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="level",
        message="BasicLevel",
    )
    custom: "CustomLevel" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="level",
        message="CustomLevel",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )


class BasicLevel(proto.Message):
    r"""``BasicLevel`` is an ``AccessLevel`` using a set of recommended
    features.

    Attributes:
        conditions (MutableSequence[google.cloud.accesscontextmanager_v1.types.Condition]):
            Required. A list of requirements for the ``AccessLevel`` to
            be granted.
        combining_function (google.cloud.accesscontextmanager_v1.types.BasicLevel.ConditionCombiningFunction):
            How the ``conditions`` list should be combined to determine
            if a request is granted this ``AccessLevel``. If AND is
            used, each ``Condition`` in ``conditions`` must be satisfied
            for the ``AccessLevel`` to be applied. If OR is used, at
            least one ``Condition`` in ``conditions`` must be satisfied
            for the ``AccessLevel`` to be applied. Default behavior is
            AND.
    """

    class ConditionCombiningFunction(proto.Enum):
        r"""Options for how the ``conditions`` list should be combined to
        determine if this ``AccessLevel`` is applied. Default is AND.

        Values:
            AND (0):
                All ``Conditions`` must be true for the ``BasicLevel`` to be
                true.
            OR (1):
                If at least one ``Condition`` is true, then the
                ``BasicLevel`` is true.
        """
        AND = 0
        OR = 1

    conditions: MutableSequence["Condition"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Condition",
    )
    combining_function: ConditionCombiningFunction = proto.Field(
        proto.ENUM,
        number=2,
        enum=ConditionCombiningFunction,
    )


class Condition(proto.Message):
    r"""A condition necessary for an ``AccessLevel`` to be granted. The
    Condition is an AND over its fields. So a Condition is true if: 1)
    the request IP is from one of the listed subnetworks AND 2) the
    originating device complies with the listed device policy AND 3) all
    listed access levels are granted AND 4) the request was sent at a
    time allowed by the DateTimeRestriction.

    Attributes:
        ip_subnetworks (MutableSequence[str]):
            CIDR block IP subnetwork specification. May
            be IPv4 or IPv6. Note that for a CIDR IP address
            block, the specified IP address portion must be
            properly truncated (i.e. all the host bits must
            be zero) or the input is considered malformed.
            For example, "192.0.2.0/24" is accepted but
            "192.0.2.1/24" is not. Similarly, for IPv6,
            "2001:db8::/32" is accepted whereas
            "2001:db8::1/32" is not. The originating IP of a
            request must be in one of the listed subnets in
            order for this Condition to be true. If empty,
            all IP addresses are allowed.
        device_policy (google.cloud.accesscontextmanager_v1.types.DevicePolicy):
            Device specific restrictions, all
            restrictions must hold for the Condition to be
            true. If not specified, all devices are allowed.
        required_access_levels (MutableSequence[str]):
            A list of other access levels defined in the same
            ``Policy``, referenced by resource name. Referencing an
            ``AccessLevel`` which does not exist is an error. All access
            levels listed must be granted for the Condition to be true.
            Example:
            "``accessPolicies/MY_POLICY/accessLevels/LEVEL_NAME"``
        negate (bool):
            Whether to negate the Condition. If true, the
            Condition becomes a NAND over its non-empty
            fields, each field must be false for the
            Condition overall to be satisfied. Defaults to
            false.
        members (MutableSequence[str]):
            The request must be made by one of the provided user or
            service accounts. Groups are not supported. Syntax:
            ``user:{emailid}`` ``serviceAccount:{emailid}`` If not
            specified, a request may come from any user.
        regions (MutableSequence[str]):
            The request must originate from one of the
            provided countries/regions. Must be valid ISO
            3166-1 alpha-2 codes.
    """

    ip_subnetworks: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    device_policy: "DevicePolicy" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DevicePolicy",
    )
    required_access_levels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    negate: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    members: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    regions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )


class CustomLevel(proto.Message):
    r"""``CustomLevel`` is an ``AccessLevel`` using the Cloud Common
    Expression Language to represent the necessary conditions for the
    level to apply to a request. See CEL spec at:
    https://github.com/google/cel-spec

    Attributes:
        expr (google.type.expr_pb2.Expr):
            Required. A Cloud CEL expression evaluating
            to a boolean.
    """

    expr: expr_pb2.Expr = proto.Field(
        proto.MESSAGE,
        number=1,
        message=expr_pb2.Expr,
    )


class DevicePolicy(proto.Message):
    r"""``DevicePolicy`` specifies device specific restrictions necessary to
    acquire a given access level. A ``DevicePolicy`` specifies
    requirements for requests from devices to be granted access levels,
    it does not do any enforcement on the device. ``DevicePolicy`` acts
    as an AND over all specified fields, and each repeated field is an
    OR over its elements. Any unset fields are ignored. For example, if
    the proto is { os_type : DESKTOP_WINDOWS, os_type : DESKTOP_LINUX,
    encryption_status: ENCRYPTED}, then the DevicePolicy will be true
    for requests originating from encrypted Linux desktops and encrypted
    Windows desktops.

    Attributes:
        require_screenlock (bool):
            Whether or not screenlock is required for the DevicePolicy
            to be true. Defaults to ``false``.
        allowed_encryption_statuses (MutableSequence[google.identity.accesscontextmanager.type.device_resources_pb2.DeviceEncryptionStatus]):
            Allowed encryptions statuses, an empty list
            allows all statuses.
        os_constraints (MutableSequence[google.cloud.accesscontextmanager_v1.types.OsConstraint]):
            Allowed OS versions, an empty list allows all
            types and all versions.
        allowed_device_management_levels (MutableSequence[google.identity.accesscontextmanager.type.device_resources_pb2.DeviceManagementLevel]):
            Allowed device management levels, an empty
            list allows all management levels.
        require_admin_approval (bool):
            Whether the device needs to be approved by
            the customer admin.
        require_corp_owned (bool):
            Whether the device needs to be corp owned.
    """

    require_screenlock: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    allowed_encryption_statuses: MutableSequence[
        device_resources_pb2.DeviceEncryptionStatus
    ] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=device_resources_pb2.DeviceEncryptionStatus,
    )
    os_constraints: MutableSequence["OsConstraint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="OsConstraint",
    )
    allowed_device_management_levels: MutableSequence[
        device_resources_pb2.DeviceManagementLevel
    ] = proto.RepeatedField(
        proto.ENUM,
        number=6,
        enum=device_resources_pb2.DeviceManagementLevel,
    )
    require_admin_approval: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    require_corp_owned: bool = proto.Field(
        proto.BOOL,
        number=8,
    )


class OsConstraint(proto.Message):
    r"""A restriction on the OS type and version of devices making
    requests.

    Attributes:
        os_type (google.identity.accesscontextmanager.type.device_resources_pb2.OsType):
            Required. The allowed OS type.
        minimum_version (str):
            The minimum allowed OS version. If not set, any version of
            this OS satisfies the constraint. Format:
            ``"major.minor.patch"``. Examples: ``"10.5.301"``,
            ``"9.2.1"``.
        require_verified_chrome_os (bool):
            Only allows requests from devices with a
            verified Chrome OS. Verifications includes
            requirements that the device is
            enterprise-managed, conformant to domain
            policies, and the caller has permission to call
            the API targeted by the request.
    """

    os_type: device_resources_pb2.OsType = proto.Field(
        proto.ENUM,
        number=1,
        enum=device_resources_pb2.OsType,
    )
    minimum_version: str = proto.Field(
        proto.STRING,
        number=2,
    )
    require_verified_chrome_os: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
