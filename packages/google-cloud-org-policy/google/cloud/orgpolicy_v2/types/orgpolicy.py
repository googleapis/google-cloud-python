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

from google.cloud.orgpolicy_v2.types import constraint
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.orgpolicy.v2",
    manifest={
        "Policy",
        "AlternatePolicySpec",
        "PolicySpec",
        "ListConstraintsRequest",
        "ListConstraintsResponse",
        "ListPoliciesRequest",
        "ListPoliciesResponse",
        "GetPolicyRequest",
        "GetEffectivePolicyRequest",
        "CreatePolicyRequest",
        "UpdatePolicyRequest",
        "DeletePolicyRequest",
    },
)


class Policy(proto.Message):
    r"""Defines a Cloud Organization ``Policy`` which is used to specify
    ``Constraints`` for configurations of Cloud Platform resources.

    Attributes:
        name (str):
            Immutable. The resource name of the Policy. Must be one of
            the following forms, where constraint_name is the name of
            the constraint which this Policy configures:

            -  ``projects/{project_number}/policies/{constraint_name}``
            -  ``folders/{folder_id}/policies/{constraint_name}``
            -  ``organizations/{organization_id}/policies/{constraint_name}``

            For example,
            "projects/123/policies/compute.disableSerialPortAccess".

            Note: ``projects/{project_id}/policies/{constraint_name}``
            is also an acceptable name for API requests, but responses
            will return the name using the equivalent project number.
        spec (google.cloud.orgpolicy_v2.types.PolicySpec):
            Basic information about the Organization
            Policy.
        alternate (google.cloud.orgpolicy_v2.types.AlternatePolicySpec):
            An alternate policy configuration that will
            be used instead of the baseline policy
            configurations as determined by the launch.
            Currently the only way the launch can trigger
            the alternate configuration is via dry-
            run/darklaunch.
    """

    name = proto.Field(proto.STRING, number=1,)
    spec = proto.Field(proto.MESSAGE, number=2, message="PolicySpec",)
    alternate = proto.Field(proto.MESSAGE, number=3, message="AlternatePolicySpec",)


class AlternatePolicySpec(proto.Message):
    r"""Similar to PolicySpec but with an extra 'launch' field for
    launch reference. The PolicySpec here is specific for dry-
    run/darklaunch.

    Attributes:
        launch (str):
            Reference to the launch that will be used
            while audit logging and to control the launch.
            Should be set only in the alternate policy.
        spec (google.cloud.orgpolicy_v2.types.PolicySpec):
            Specify ``Constraint`` for configurations of Cloud Platform
            resources.
    """

    launch = proto.Field(proto.STRING, number=1,)
    spec = proto.Field(proto.MESSAGE, number=2, message="PolicySpec",)


class PolicySpec(proto.Message):
    r"""Defines a Cloud Organization ``PolicySpec`` which is used to specify
    ``Constraints`` for configurations of Cloud Platform resources.

    Attributes:
        etag (str):
            An opaque tag indicating the current version of the
            ``Policy``, used for concurrency control.

            This field is ignored if used in a ``CreatePolicy`` request.

            When the ``Policy`` is returned from either a ``GetPolicy``
            or a ``ListPolicies`` request, this ``etag`` indicates the
            version of the current ``Policy`` to use when executing a
            read-modify-write loop.

            When the ``Policy`` is returned from a
            ``GetEffectivePolicy`` request, the ``etag`` will be unset.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time stamp this was previously updated.
            This represents the last time a call to ``CreatePolicy`` or
            ``UpdatePolicy`` was made for that ``Policy``.
        rules (Sequence[google.cloud.orgpolicy_v2.types.PolicySpec.PolicyRule]):
            Up to 10 PolicyRules are allowed.

            In Policies for boolean constraints, the following
            requirements apply:

            -  There must be one and only one PolicyRule where condition
               is unset.
            -  BooleanPolicyRules with conditions must set ``enforced``
               to the opposite of the PolicyRule without a condition.
            -  During policy evaluation, PolicyRules with conditions
               that are true for a target resource take precedence.
        inherit_from_parent (bool):
            Determines the inheritance behavior for this ``Policy``.

            If ``inherit_from_parent`` is true, PolicyRules set higher
            up in the hierarchy (up to the closest root) are inherited
            and present in the effective policy. If it is false, then no
            rules are inherited, and this Policy becomes the new root
            for evaluation. This field can be set only for Policies
            which configure list constraints.
        reset (bool):
            Ignores policies set above this resource and restores the
            ``constraint_default`` enforcement behavior of the specific
            ``Constraint`` at this resource. This field can be set in
            policies for either list or boolean constraints. If set,
            ``rules`` must be empty and ``inherit_from_parent`` must be
            set to false.
    """

    class PolicyRule(proto.Message):
        r"""A rule used to express this policy.
        Attributes:
            values (google.cloud.orgpolicy_v2.types.PolicySpec.PolicyRule.StringValues):
                List of values to be used for this
                PolicyRule. This field can be set only in
                Policies for list constraints.
            allow_all (bool):
                Setting this to true means that all values
                are allowed. This field can be set only in
                Policies for list constraints.
            deny_all (bool):
                Setting this to true means that all values
                are denied. This field can be set only in
                Policies for list constraints.
            enforce (bool):
                If ``true``, then the ``Policy`` is enforced. If ``false``,
                then any configuration is acceptable. This field can be set
                only in Policies for boolean constraints.
            condition (google.type.expr_pb2.Expr):
                A condition which determines whether this rule is used in
                the evaluation of the policy. When set, the ``expression``
                field in the \`Expr' must include from 1 to 10
                subexpressions, joined by the "||" or "&&" operators. Each
                subexpression must be of the form
                "resource.matchLabels(key_name, value_name)", where key_name
                and value_name are the resource names for Label Keys and
                Values. These names are available from the Label Manager
                Service. An example expression is:
                "resource.matchLabels('labelKeys/123, 'labelValues/456')".
        """

        class StringValues(proto.Message):
            r"""A message that holds specific allowed and denied values. This
            message can define specific values and subtrees of Cloud Resource
            Manager resource hierarchy (``Organizations``, ``Folders``,
            ``Projects``) that are allowed or denied. This is achieved by using
            the ``under:`` and optional ``is:`` prefixes. The ``under:`` prefix
            is used to denote resource subtree values. The ``is:`` prefix is
            used to denote specific values, and is required only if the value
            contains a ":". Values prefixed with "is:" are treated the same as
            values with no prefix. Ancestry subtrees must be in one of the
            following formats: - "projects/", e.g. "projects/tokyo-rain-123" -
            "folders/", e.g. "folders/1234" - "organizations/", e.g.
            "organizations/1234" The ``supports_under`` field of the associated
            ``Constraint`` defines whether ancestry prefixes can be used.

            Attributes:
                allowed_values (Sequence[str]):
                    List of values allowed at this resource.
                denied_values (Sequence[str]):
                    List of values denied at this resource.
            """

            allowed_values = proto.RepeatedField(proto.STRING, number=1,)
            denied_values = proto.RepeatedField(proto.STRING, number=2,)

        values = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="kind",
            message="PolicySpec.PolicyRule.StringValues",
        )
        allow_all = proto.Field(proto.BOOL, number=2, oneof="kind",)
        deny_all = proto.Field(proto.BOOL, number=3, oneof="kind",)
        enforce = proto.Field(proto.BOOL, number=4, oneof="kind",)
        condition = proto.Field(proto.MESSAGE, number=5, message=expr_pb2.Expr,)

    etag = proto.Field(proto.STRING, number=1,)
    update_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    rules = proto.RepeatedField(proto.MESSAGE, number=3, message=PolicyRule,)
    inherit_from_parent = proto.Field(proto.BOOL, number=4,)
    reset = proto.Field(proto.BOOL, number=5,)


class ListConstraintsRequest(proto.Message):
    r"""The request sent to the [ListConstraints]
    [google.cloud.orgpolicy.v2.OrgPolicy.ListConstraints] method.

    Attributes:
        parent (str):
            Required. The Cloud resource that parents the constraint.
            Must be in one of the following forms:

            -  ``projects/{project_number}``
            -  ``projects/{project_id}``
            -  ``folders/{folder_id}``
            -  ``organizations/{organization_id}``
        page_size (int):
            Size of the pages to be returned. This is
            currently unsupported and will be ignored. The
            server may at any point start using this field
            to limit page size.
        page_token (str):
            Page token used to retrieve the next page.
            This is currently unsupported and will be
            ignored. The server may at any point start using
            this field.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListConstraintsResponse(proto.Message):
    r"""The response returned from the [ListConstraints]
    [google.cloud.orgpolicy.v2.OrgPolicy.ListConstraints] method.

    Attributes:
        constraints (Sequence[google.cloud.orgpolicy_v2.types.Constraint]):
            The collection of constraints that are
            available on the targeted resource.
        next_page_token (str):
            Page token used to retrieve the next page.
            This is currently not used.
    """

    @property
    def raw_page(self):
        return self

    constraints = proto.RepeatedField(
        proto.MESSAGE, number=1, message=constraint.Constraint,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class ListPoliciesRequest(proto.Message):
    r"""The request sent to the [ListPolicies]
    [google.cloud.orgpolicy.v2.OrgPolicy.ListPolicies] method.

    Attributes:
        parent (str):
            Required. The target Cloud resource that parents the set of
            constraints and policies that will be returned from this
            call. Must be in one of the following forms:

            -  ``projects/{project_number}``
            -  ``projects/{project_id}``
            -  ``folders/{folder_id}``
            -  ``organizations/{organization_id}``
        page_size (int):
            Size of the pages to be returned. This is
            currently unsupported and will be ignored. The
            server may at any point start using this field
            to limit page size.
        page_token (str):
            Page token used to retrieve the next page.
            This is currently unsupported and will be
            ignored. The server may at any point start using
            this field.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListPoliciesResponse(proto.Message):
    r"""The response returned from the [ListPolicies]
    [google.cloud.orgpolicy.v2.OrgPolicy.ListPolicies] method. It will
    be empty if no ``Policies`` are set on the resource.

    Attributes:
        policies (Sequence[google.cloud.orgpolicy_v2.types.Policy]):
            All ``Policies`` that exist on the resource. It will be
            empty if no ``Policies`` are set.
        next_page_token (str):
            Page token used to retrieve the next page.
            This is currently not used, but the server may
            at any point start supplying a valid token.
    """

    @property
    def raw_page(self):
        return self

    policies = proto.RepeatedField(proto.MESSAGE, number=1, message="Policy",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetPolicyRequest(proto.Message):
    r"""The request sent to the [GetPolicy]
    [google.cloud.orgpolicy.v2.OrgPolicy.GetPolicy] method.

    Attributes:
        name (str):
            Required. Resource name of the policy. See ``Policy`` for
            naming requirements.
    """

    name = proto.Field(proto.STRING, number=1,)


class GetEffectivePolicyRequest(proto.Message):
    r"""The request sent to the [GetEffectivePolicy]
    [google.cloud.orgpolicy.v2.OrgPolicy.GetEffectivePolicy] method.

    Attributes:
        name (str):
            Required. The effective policy to compute. See ``Policy``
            for naming rules.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreatePolicyRequest(proto.Message):
    r"""The request sent to the [CreatePolicyRequest]
    [google.cloud.orgpolicy.v2.OrgPolicy.CreatePolicy] method.

    Attributes:
        parent (str):
            Required. The Cloud resource that will parent the new
            Policy. Must be in one of the following forms:

            -  ``projects/{project_number}``
            -  ``projects/{project_id}``
            -  ``folders/{folder_id}``
            -  ``organizations/{organization_id}``
        policy (google.cloud.orgpolicy_v2.types.Policy):
            Required. ``Policy`` to create.
    """

    parent = proto.Field(proto.STRING, number=1,)
    policy = proto.Field(proto.MESSAGE, number=3, message="Policy",)


class UpdatePolicyRequest(proto.Message):
    r"""The request sent to the [UpdatePolicyRequest]
    [google.cloud.orgpolicy.v2.OrgPolicy.UpdatePolicy] method.

    Attributes:
        policy (google.cloud.orgpolicy_v2.types.Policy):
            Required. ``Policy`` to update.
    """

    policy = proto.Field(proto.MESSAGE, number=1, message="Policy",)


class DeletePolicyRequest(proto.Message):
    r"""The request sent to the [DeletePolicy]
    [google.cloud.orgpolicy.v2.OrgPolicy.DeletePolicy] method.

    Attributes:
        name (str):
            Required. Name of the policy to delete. See ``Policy`` for
            naming rules.
    """

    name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
