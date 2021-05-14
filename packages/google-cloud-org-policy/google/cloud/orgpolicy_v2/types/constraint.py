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


__protobuf__ = proto.module(
    package="google.cloud.orgpolicy.v2", manifest={"Constraint",},
)


class Constraint(proto.Message):
    r"""A ``constraint`` describes a way to restrict resource's
    configuration. For example, you could enforce a constraint that
    controls which cloud services can be activated across an
    organization, or whether a Compute Engine instance can have serial
    port connections established. ``Constraints`` can be configured by
    the organization's policy adminstrator to fit the needs of the
    organzation by setting a ``policy`` that includes ``constraints`` at
    different locations in the organization's resource hierarchy.
    Policies are inherited down the resource hierarchy from higher
    levels, but can also be overridden. For details about the
    inheritance rules please read about
    [``policies``][google.cloud.OrgPolicy.v2.Policy].

    ``Constraints`` have a default behavior determined by the
    ``constraint_default`` field, which is the enforcement behavior that
    is used in the absence of a ``policy`` being defined or inherited
    for the resource in question.

    Attributes:
        name (str):
            Immutable. The resource name of the Constraint. Must be in
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
            Detailed description of what this ``Constraint`` controls as
            well as how and where it is enforced.

            Mutable.
        constraint_default (google.cloud.orgpolicy_v2.types.Constraint.ConstraintDefault):
            The evaluation behavior of this constraint in
            the absence of 'Policy'.
        list_constraint (google.cloud.orgpolicy_v2.types.Constraint.ListConstraint):
            Defines this constraint as being a
            ListConstraint.
        boolean_constraint (google.cloud.orgpolicy_v2.types.Constraint.BooleanConstraint):
            Defines this constraint as being a
            BooleanConstraint.
    """

    class ConstraintDefault(proto.Enum):
        r"""Specifies the default behavior in the absence of any ``Policy`` for
        the ``Constraint``. This must not be
        ``CONSTRAINT_DEFAULT_UNSPECIFIED``.

        Immutable after creation.
        """
        CONSTRAINT_DEFAULT_UNSPECIFIED = 0
        ALLOW = 1
        DENY = 2

    class ListConstraint(proto.Message):
        r"""A ``Constraint`` that allows or disallows a list of string values,
        which are configured by an Organization's policy administrator with
        a ``Policy``.

        Attributes:
            supports_in (bool):
                Indicates whether values grouped into categories can be used
                in ``Policy.allowed_values`` and ``Policy.denied_values``.
                For example, ``"in:Python"`` would match any value in the
                'Python' group.
            supports_under (bool):
                Indicates whether subtrees of Cloud Resource Manager
                resource hierarchy can be used in ``Policy.allowed_values``
                and ``Policy.denied_values``. For example,
                ``"under:folders/123"`` would match any resource under the
                'folders/123' folder.
        """

        supports_in = proto.Field(proto.BOOL, number=1,)
        supports_under = proto.Field(proto.BOOL, number=2,)

    class BooleanConstraint(proto.Message):
        r"""A ``Constraint`` that is either enforced or not.

        For example a constraint
        ``constraints/compute.disableSerialPortAccess``. If it is enforced
        on a VM instance, serial port connections will not be opened to that
        instance.
            """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    constraint_default = proto.Field(proto.ENUM, number=4, enum=ConstraintDefault,)
    list_constraint = proto.Field(
        proto.MESSAGE, number=5, oneof="constraint_type", message=ListConstraint,
    )
    boolean_constraint = proto.Field(
        proto.MESSAGE, number=6, oneof="constraint_type", message=BooleanConstraint,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
