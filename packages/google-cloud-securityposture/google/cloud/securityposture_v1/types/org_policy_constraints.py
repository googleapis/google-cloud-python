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

from google.cloud.securityposture_v1.types import org_policy_config

__protobuf__ = proto.module(
    package="google.cloud.securityposture.v1",
    manifest={
        "OrgPolicyConstraint",
        "OrgPolicyConstraintCustom",
    },
)


class OrgPolicyConstraint(proto.Message):
    r"""Message for Org Policy Canned Constraint.

    Attributes:
        canned_constraint_id (str):
            Required. Org Policy Canned Constraint id.
        policy_rules (MutableSequence[google.cloud.securityposture_v1.types.PolicyRule]):
            Required. Org PolicySpec rules.
    """

    canned_constraint_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    policy_rules: MutableSequence[org_policy_config.PolicyRule] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=org_policy_config.PolicyRule,
    )


class OrgPolicyConstraintCustom(proto.Message):
    r"""Message for Org Policy Custom Constraint.

    Attributes:
        custom_constraint (google.cloud.securityposture_v1.types.CustomConstraint):
            Required. Org Policy Custom Constraint.
        policy_rules (MutableSequence[google.cloud.securityposture_v1.types.PolicyRule]):
            Required. Org Policyspec rules.
    """

    custom_constraint: org_policy_config.CustomConstraint = proto.Field(
        proto.MESSAGE,
        number=1,
        message=org_policy_config.CustomConstraint,
    )
    policy_rules: MutableSequence[org_policy_config.PolicyRule] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=org_policy_config.PolicyRule,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
