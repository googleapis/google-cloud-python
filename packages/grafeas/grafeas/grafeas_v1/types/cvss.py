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


__protobuf__ = proto.module(package="grafeas.v1", manifest={"CVSSv3",},)


class CVSSv3(proto.Message):
    r"""Common Vulnerability Scoring System version 3.
    For details, see https://www.first.org/cvss/specification-
    document

    Attributes:
        base_score (float):
            The base score is a function of the base
            metric scores.
        exploitability_score (float):

        impact_score (float):

        attack_vector (~.cvss.CVSSv3.AttackVector):
            Base Metrics
            Represents the intrinsic characteristics of a
            vulnerability that are constant over time and
            across user environments.
        attack_complexity (~.cvss.CVSSv3.AttackComplexity):

        privileges_required (~.cvss.CVSSv3.PrivilegesRequired):

        user_interaction (~.cvss.CVSSv3.UserInteraction):

        scope (~.cvss.CVSSv3.Scope):

        confidentiality_impact (~.cvss.CVSSv3.Impact):

        integrity_impact (~.cvss.CVSSv3.Impact):

        availability_impact (~.cvss.CVSSv3.Impact):

    """

    class AttackVector(proto.Enum):
        r""""""
        ATTACK_VECTOR_UNSPECIFIED = 0
        ATTACK_VECTOR_NETWORK = 1
        ATTACK_VECTOR_ADJACENT = 2
        ATTACK_VECTOR_LOCAL = 3
        ATTACK_VECTOR_PHYSICAL = 4

    class AttackComplexity(proto.Enum):
        r""""""
        ATTACK_COMPLEXITY_UNSPECIFIED = 0
        ATTACK_COMPLEXITY_LOW = 1
        ATTACK_COMPLEXITY_HIGH = 2

    class PrivilegesRequired(proto.Enum):
        r""""""
        PRIVILEGES_REQUIRED_UNSPECIFIED = 0
        PRIVILEGES_REQUIRED_NONE = 1
        PRIVILEGES_REQUIRED_LOW = 2
        PRIVILEGES_REQUIRED_HIGH = 3

    class UserInteraction(proto.Enum):
        r""""""
        USER_INTERACTION_UNSPECIFIED = 0
        USER_INTERACTION_NONE = 1
        USER_INTERACTION_REQUIRED = 2

    class Scope(proto.Enum):
        r""""""
        SCOPE_UNSPECIFIED = 0
        SCOPE_UNCHANGED = 1
        SCOPE_CHANGED = 2

    class Impact(proto.Enum):
        r""""""
        IMPACT_UNSPECIFIED = 0
        IMPACT_HIGH = 1
        IMPACT_LOW = 2
        IMPACT_NONE = 3

    base_score = proto.Field(proto.FLOAT, number=1)

    exploitability_score = proto.Field(proto.FLOAT, number=2)

    impact_score = proto.Field(proto.FLOAT, number=3)

    attack_vector = proto.Field(proto.ENUM, number=5, enum=AttackVector,)

    attack_complexity = proto.Field(proto.ENUM, number=6, enum=AttackComplexity,)

    privileges_required = proto.Field(proto.ENUM, number=7, enum=PrivilegesRequired,)

    user_interaction = proto.Field(proto.ENUM, number=8, enum=UserInteraction,)

    scope = proto.Field(proto.ENUM, number=9, enum=Scope,)

    confidentiality_impact = proto.Field(proto.ENUM, number=10, enum=Impact,)

    integrity_impact = proto.Field(proto.ENUM, number=11, enum=Impact,)

    availability_impact = proto.Field(proto.ENUM, number=12, enum=Impact,)


__all__ = tuple(sorted(__protobuf__.manifest))
