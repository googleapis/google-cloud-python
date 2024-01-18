# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.securityposture.v1',
    manifest={
        'PolicyRule',
        'CustomConstraint',
    },
)


class PolicyRule(proto.Message):
    r"""A rule used to express this policy.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        values (google.cloud.securityposture_v1.types.PolicyRule.StringValues):
            List of values to be used for this policy
            rule. This field can be set only in policies for
            list constraints.

            This field is a member of `oneof`_ ``kind``.
        allow_all (bool):
            Setting this to true means that all values
            are allowed. This field can be set only in
            policies for list constraints.

            This field is a member of `oneof`_ ``kind``.
        deny_all (bool):
            Setting this to true means that all values
            are denied. This field can be set only in
            policies for list constraints.

            This field is a member of `oneof`_ ``kind``.
        enforce (bool):
            If ``true``, then the policy is enforced. If ``false``, then
            any configuration is acceptable. This field can be set only
            in policies for boolean constraints.

            This field is a member of `oneof`_ ``kind``.
        condition (google.type.expr_pb2.Expr):
            A condition which determines whether this rule is used in
            the evaluation of the policy. When set, the ``expression``
            field in the \`Expr' must include from 1 to 10
            subexpressions, joined by the "||" or "&&" operators. Each
            subexpression must be of the form
            "resource.matchTag('<ORG_ID>/tag_key_short_name,
            'tag_value_short_name')" or
            "resource.matchTagId('tagKeys/key_id',
            'tagValues/value_id')" where key_name and value_name are the
            resource names for Label Keys and Values. These names are
            available from the Tag Manager Service. An example
            expression is: "resource.matchTag('123456789/environment,
            'prod')" or "resource.matchTagId('tagKeys/123',
            'tagValues/456')".
    """

    class StringValues(proto.Message):
        r"""A message that holds specific allowed and denied values. This
        message can define specific values and subtrees of the Resource
        Manager resource hierarchy (``Organizations``, ``Folders``,
        ``Projects``) that are allowed or denied. This is achieved by using
        the ``under:`` and optional ``is:`` prefixes. The ``under:`` prefix
        is used to denote resource subtree values. The ``is:`` prefix is
        used to denote specific values, and is required only if the value
        contains a ":". Values prefixed with "is:" are treated the same as
        values with no prefix. Ancestry subtrees must be in one of the
        following formats:

        -  ``projects/<project-id>`` (for example,
           ``projects/tokyo-rain-123``)
        -  ``folders/<folder-id>`` (for example, ``folders/1234``)
        -  ``organizations/<organization-id>`` (for example,
           ``organizations/1234``)

        The ``supports_under`` field of the associated ``Constraint``
        defines whether ancestry prefixes can be used.

        Attributes:
            allowed_values (MutableSequence[str]):
                List of values allowed at this resource.
            denied_values (MutableSequence[str]):
                List of values denied at this resource.
        """

        allowed_values: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        denied_values: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    values: StringValues = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof='kind',
        message=StringValues,
    )
    allow_all: bool = proto.Field(
        proto.BOOL,
        number=2,
        oneof='kind',
    )
    deny_all: bool = proto.Field(
        proto.BOOL,
        number=3,
        oneof='kind',
    )
    enforce: bool = proto.Field(
        proto.BOOL,
        number=4,
        oneof='kind',
    )
    condition: expr_pb2.Expr = proto.Field(
        proto.MESSAGE,
        number=5,
        message=expr_pb2.Expr,
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

            -

            ``organizations/{organization_id}/customConstraints/{custom_constraint_id}``

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
        method_types (MutableSequence[google.cloud.securityposture_v1.types.CustomConstraint.MethodType]):
            All the operations being applied for this
            constraint.
        condition (str):
            Org policy condition/expression. For example:
            ``resource.instanceName.matches("[production|test]_.*_(\d)+")``
            or, ``resource.management.auto_upgrade == true``

            The max length of the condition is 1000 characters.
        action_type (google.cloud.securityposture_v1.types.CustomConstraint.ActionType):
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
        """
        METHOD_TYPE_UNSPECIFIED = 0
        CREATE = 1
        UPDATE = 2
        DELETE = 3

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
