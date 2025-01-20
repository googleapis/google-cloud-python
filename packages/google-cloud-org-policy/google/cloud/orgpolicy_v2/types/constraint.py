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
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.orgpolicy.v2",
    manifest={
        "Constraint",
        "CustomConstraint",
    },
)


class Constraint(proto.Message):
    r"""A constraint describes a way to restrict resource's configuration.
    For example, you could enforce a constraint that controls which
    Google Cloud services can be activated across an organization, or
    whether a Compute Engine instance can have serial port connections
    established. Constraints can be configured by the organization
    policy administrator to fit the needs of the organization by setting
    a policy that includes constraints at different locations in the
    organization's resource hierarchy. Policies are inherited down the
    resource hierarchy from higher levels, but can also be overridden.
    For details about the inheritance rules please read about
    [``policies``][google.cloud.OrgPolicy.v2.Policy].

    Constraints have a default behavior determined by the
    ``constraint_default`` field, which is the enforcement behavior that
    is used in the absence of a policy being defined or inherited for
    the resource in question.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Immutable. The resource name of the constraint. Must be in
            one of the following forms:

            -  ``projects/{project_number}/constraints/{constraint_name}``
            -  ``folders/{folder_id}/constraints/{constraint_name}``
            -  ``organizations/{organization_id}/constraints/{constraint_name}``

            For example,
            "/projects/123/constraints/compute.disableSerialPortAccess".
        display_name (str):
            The human readable name.

            Mutable.
        description (str):
            Detailed description of what this constraint
            controls as well as how and where it is
            enforced.

            Mutable.
        constraint_default (google.cloud.orgpolicy_v2.types.Constraint.ConstraintDefault):
            The evaluation behavior of this constraint in
            the absence of a policy.
        list_constraint (google.cloud.orgpolicy_v2.types.Constraint.ListConstraint):
            Defines this constraint as being a
            ListConstraint.

            This field is a member of `oneof`_ ``constraint_type``.
        boolean_constraint (google.cloud.orgpolicy_v2.types.Constraint.BooleanConstraint):
            Defines this constraint as being a
            BooleanConstraint.

            This field is a member of `oneof`_ ``constraint_type``.
        supports_dry_run (bool):
            Shows if dry run is supported for this
            constraint or not.
    """

    class ConstraintDefault(proto.Enum):
        r"""Specifies the default behavior in the absence of any policy for the
        constraint. This must not be ``CONSTRAINT_DEFAULT_UNSPECIFIED``.

        Immutable after creation.

        Values:
            CONSTRAINT_DEFAULT_UNSPECIFIED (0):
                This is only used for distinguishing unset
                values and should never be used.
            ALLOW (1):
                Indicate that all values are allowed for list
                constraints. Indicate that enforcement is off
                for boolean constraints.
            DENY (2):
                Indicate that all values are denied for list
                constraints. Indicate that enforcement is on for
                boolean constraints.
        """
        CONSTRAINT_DEFAULT_UNSPECIFIED = 0
        ALLOW = 1
        DENY = 2

    class ListConstraint(proto.Message):
        r"""A constraint that allows or disallows a list of string
        values, which are configured by an Organization Policy
        administrator with a policy.

        Attributes:
            supports_in (bool):
                Indicates whether values grouped into categories can be used
                in ``Policy.allowed_values`` and ``Policy.denied_values``.
                For example, ``"in:Python"`` would match any value in the
                'Python' group.
            supports_under (bool):
                Indicates whether subtrees of the Resource Manager resource
                hierarchy can be used in ``Policy.allowed_values`` and
                ``Policy.denied_values``. For example,
                ``"under:folders/123"`` would match any resource under the
                'folders/123' folder.
        """

        supports_in: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        supports_under: bool = proto.Field(
            proto.BOOL,
            number=2,
        )

    class BooleanConstraint(proto.Message):
        r"""A constraint that is either enforced or not.

        For example, a constraint
        ``constraints/compute.disableSerialPortAccess``. If it is enforced
        on a VM instance, serial port connections will not be opened to that
        instance.

        """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    constraint_default: ConstraintDefault = proto.Field(
        proto.ENUM,
        number=4,
        enum=ConstraintDefault,
    )
    list_constraint: ListConstraint = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="constraint_type",
        message=ListConstraint,
    )
    boolean_constraint: BooleanConstraint = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="constraint_type",
        message=BooleanConstraint,
    )
    supports_dry_run: bool = proto.Field(
        proto.BOOL,
        number=7,
    )


class CustomConstraint(proto.Message):
    r"""A custom constraint defined by customers which can *only* be applied
    to the given resource types and organization.

    By creating a custom constraint, customers can apply policies of
    this custom constraint. *Creating a custom constraint itself does
    NOT apply any policy enforcement*.

    Attributes:
        name (str):
            Immutable. Name of the constraint. This is unique within the
            organization. Format of the name should be

            -  ``organizations/{organization_id}/customConstraints/{custom_constraint_id}``

            Example:
            ``organizations/123/customConstraints/custom.createOnlyE2TypeVms``

            The max length is 70 characters and the minimum length is 1.
            Note that the prefix
            ``organizations/{organization_id}/customConstraints/`` is
            not counted.
        resource_types (MutableSequence[str]):
            Immutable. The resource instance type on which this policy
            applies. Format will be of the form :
            ``<canonical service name>/<type>`` Example:

            -  ``compute.googleapis.com/Instance``.
        method_types (MutableSequence[google.cloud.orgpolicy_v2.types.CustomConstraint.MethodType]):
            All the operations being applied for this
            constraint.
        condition (str):
            Org policy condition/expression. For example:
            ``resource.instanceName.matches("[production|test]_.*_(\d)+")``
            or, ``resource.management.auto_upgrade == true``

            The max length of the condition is 1000 characters.
        action_type (google.cloud.orgpolicy_v2.types.CustomConstraint.ActionType):
            Allow or deny type.
        display_name (str):
            One line display name for the UI. The max length of the
            display_name is 200 characters.
        description (str):
            Detailed information about this custom policy
            constraint. The max length of the description is
            2000 characters.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last time this custom constraint was
            updated. This represents the last time that the
            ``CreateCustomConstraint`` or ``UpdateCustomConstraint`` RPC
            was called
    """

    class MethodType(proto.Enum):
        r"""The operation for which this constraint will be applied. To apply
        this constraint only when creating new VMs, the ``method_types``
        should be ``CREATE`` only. To apply this constraint when creating or
        deleting VMs, the ``method_types`` should be ``CREATE`` and
        ``DELETE``.

        ``UPDATE`` only custom constraints are not supported. Use ``CREATE``
        or ``CREATE, UPDATE``.

        Values:
            METHOD_TYPE_UNSPECIFIED (0):
                Unspecified. Results in an error.
            CREATE (1):
                Constraint applied when creating the
                resource.
            UPDATE (2):
                Constraint applied when updating the
                resource.
            DELETE (3):
                Constraint applied when deleting the
                resource. Not supported yet.
            REMOVE_GRANT (4):
                Constraint applied when removing an IAM
                grant.
            GOVERN_TAGS (5):
                Constraint applied when enforcing forced
                tagging.
        """
        METHOD_TYPE_UNSPECIFIED = 0
        CREATE = 1
        UPDATE = 2
        DELETE = 3
        REMOVE_GRANT = 4
        GOVERN_TAGS = 5

    class ActionType(proto.Enum):
        r"""Allow or deny type.

        Values:
            ACTION_TYPE_UNSPECIFIED (0):
                Unspecified. Results in an error.
            ALLOW (1):
                Allowed action type.
            DENY (2):
                Deny action type.
        """
        ACTION_TYPE_UNSPECIFIED = 0
        ALLOW = 1
        DENY = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    resource_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    method_types: MutableSequence[MethodType] = proto.RepeatedField(
        proto.ENUM,
        number=3,
        enum=MethodType,
    )
    condition: str = proto.Field(
        proto.STRING,
        number=4,
    )
    action_type: ActionType = proto.Field(
        proto.ENUM,
        number=5,
        enum=ActionType,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    description: str = proto.Field(
        proto.STRING,
        number=7,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
