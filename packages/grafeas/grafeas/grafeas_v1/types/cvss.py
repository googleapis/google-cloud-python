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
    package="grafeas.v1",
    manifest={
        "CVSSVersion",
        "CVSSv3",
        "CVSS",
    },
)


class CVSSVersion(proto.Enum):
    r"""CVSS Version.

    Values:
        CVSS_VERSION_UNSPECIFIED (0):
            No description available.
        CVSS_VERSION_2 (1):
            No description available.
        CVSS_VERSION_3 (2):
            No description available.
    """
    CVSS_VERSION_UNSPECIFIED = 0
    CVSS_VERSION_2 = 1
    CVSS_VERSION_3 = 2


class CVSSv3(proto.Message):
    r"""Common Vulnerability Scoring System version 3.
    For details, see
    https://www.first.org/cvss/specification-document

    Attributes:
        base_score (float):
            The base score is a function of the base
            metric scores.
        exploitability_score (float):

        impact_score (float):

        attack_vector (grafeas.grafeas_v1.types.CVSSv3.AttackVector):
            Base Metrics
            Represents the intrinsic characteristics of a
            vulnerability that are constant over time and
            across user environments.
        attack_complexity (grafeas.grafeas_v1.types.CVSSv3.AttackComplexity):

        privileges_required (grafeas.grafeas_v1.types.CVSSv3.PrivilegesRequired):

        user_interaction (grafeas.grafeas_v1.types.CVSSv3.UserInteraction):

        scope (grafeas.grafeas_v1.types.CVSSv3.Scope):

        confidentiality_impact (grafeas.grafeas_v1.types.CVSSv3.Impact):

        integrity_impact (grafeas.grafeas_v1.types.CVSSv3.Impact):

        availability_impact (grafeas.grafeas_v1.types.CVSSv3.Impact):

    """

    class AttackVector(proto.Enum):
        r"""

        Values:
            ATTACK_VECTOR_UNSPECIFIED (0):
                No description available.
            ATTACK_VECTOR_NETWORK (1):
                No description available.
            ATTACK_VECTOR_ADJACENT (2):
                No description available.
            ATTACK_VECTOR_LOCAL (3):
                No description available.
            ATTACK_VECTOR_PHYSICAL (4):
                No description available.
        """
        ATTACK_VECTOR_UNSPECIFIED = 0
        ATTACK_VECTOR_NETWORK = 1
        ATTACK_VECTOR_ADJACENT = 2
        ATTACK_VECTOR_LOCAL = 3
        ATTACK_VECTOR_PHYSICAL = 4

    class AttackComplexity(proto.Enum):
        r"""

        Values:
            ATTACK_COMPLEXITY_UNSPECIFIED (0):
                No description available.
            ATTACK_COMPLEXITY_LOW (1):
                No description available.
            ATTACK_COMPLEXITY_HIGH (2):
                No description available.
        """
        ATTACK_COMPLEXITY_UNSPECIFIED = 0
        ATTACK_COMPLEXITY_LOW = 1
        ATTACK_COMPLEXITY_HIGH = 2

    class PrivilegesRequired(proto.Enum):
        r"""

        Values:
            PRIVILEGES_REQUIRED_UNSPECIFIED (0):
                No description available.
            PRIVILEGES_REQUIRED_NONE (1):
                No description available.
            PRIVILEGES_REQUIRED_LOW (2):
                No description available.
            PRIVILEGES_REQUIRED_HIGH (3):
                No description available.
        """
        PRIVILEGES_REQUIRED_UNSPECIFIED = 0
        PRIVILEGES_REQUIRED_NONE = 1
        PRIVILEGES_REQUIRED_LOW = 2
        PRIVILEGES_REQUIRED_HIGH = 3

    class UserInteraction(proto.Enum):
        r"""

        Values:
            USER_INTERACTION_UNSPECIFIED (0):
                No description available.
            USER_INTERACTION_NONE (1):
                No description available.
            USER_INTERACTION_REQUIRED (2):
                No description available.
        """
        USER_INTERACTION_UNSPECIFIED = 0
        USER_INTERACTION_NONE = 1
        USER_INTERACTION_REQUIRED = 2

    class Scope(proto.Enum):
        r"""

        Values:
            SCOPE_UNSPECIFIED (0):
                No description available.
            SCOPE_UNCHANGED (1):
                No description available.
            SCOPE_CHANGED (2):
                No description available.
        """
        SCOPE_UNSPECIFIED = 0
        SCOPE_UNCHANGED = 1
        SCOPE_CHANGED = 2

    class Impact(proto.Enum):
        r"""

        Values:
            IMPACT_UNSPECIFIED (0):
                No description available.
            IMPACT_HIGH (1):
                No description available.
            IMPACT_LOW (2):
                No description available.
            IMPACT_NONE (3):
                No description available.
        """
        IMPACT_UNSPECIFIED = 0
        IMPACT_HIGH = 1
        IMPACT_LOW = 2
        IMPACT_NONE = 3

    base_score: float = proto.Field(
        proto.FLOAT,
        number=1,
    )
    exploitability_score: float = proto.Field(
        proto.FLOAT,
        number=2,
    )
    impact_score: float = proto.Field(
        proto.FLOAT,
        number=3,
    )
    attack_vector: AttackVector = proto.Field(
        proto.ENUM,
        number=5,
        enum=AttackVector,
    )
    attack_complexity: AttackComplexity = proto.Field(
        proto.ENUM,
        number=6,
        enum=AttackComplexity,
    )
    privileges_required: PrivilegesRequired = proto.Field(
        proto.ENUM,
        number=7,
        enum=PrivilegesRequired,
    )
    user_interaction: UserInteraction = proto.Field(
        proto.ENUM,
        number=8,
        enum=UserInteraction,
    )
    scope: Scope = proto.Field(
        proto.ENUM,
        number=9,
        enum=Scope,
    )
    confidentiality_impact: Impact = proto.Field(
        proto.ENUM,
        number=10,
        enum=Impact,
    )
    integrity_impact: Impact = proto.Field(
        proto.ENUM,
        number=11,
        enum=Impact,
    )
    availability_impact: Impact = proto.Field(
        proto.ENUM,
        number=12,
        enum=Impact,
    )


class CVSS(proto.Message):
    r"""Common Vulnerability Scoring System.
    For details, see
    https://www.first.org/cvss/specification-document This is a
    message we will try to use for storing various versions of CVSS
    rather than making a separate proto for storing a specific
    version.

    Attributes:
        base_score (float):
            The base score is a function of the base
            metric scores.
        exploitability_score (float):

        impact_score (float):

        attack_vector (grafeas.grafeas_v1.types.CVSS.AttackVector):
            Base Metrics
            Represents the intrinsic characteristics of a
            vulnerability that are constant over time and
            across user environments.
        attack_complexity (grafeas.grafeas_v1.types.CVSS.AttackComplexity):

        authentication (grafeas.grafeas_v1.types.CVSS.Authentication):

        privileges_required (grafeas.grafeas_v1.types.CVSS.PrivilegesRequired):

        user_interaction (grafeas.grafeas_v1.types.CVSS.UserInteraction):

        scope (grafeas.grafeas_v1.types.CVSS.Scope):

        confidentiality_impact (grafeas.grafeas_v1.types.CVSS.Impact):

        integrity_impact (grafeas.grafeas_v1.types.CVSS.Impact):

        availability_impact (grafeas.grafeas_v1.types.CVSS.Impact):

    """

    class AttackVector(proto.Enum):
        r"""

        Values:
            ATTACK_VECTOR_UNSPECIFIED (0):
                No description available.
            ATTACK_VECTOR_NETWORK (1):
                No description available.
            ATTACK_VECTOR_ADJACENT (2):
                No description available.
            ATTACK_VECTOR_LOCAL (3):
                No description available.
            ATTACK_VECTOR_PHYSICAL (4):
                No description available.
        """
        ATTACK_VECTOR_UNSPECIFIED = 0
        ATTACK_VECTOR_NETWORK = 1
        ATTACK_VECTOR_ADJACENT = 2
        ATTACK_VECTOR_LOCAL = 3
        ATTACK_VECTOR_PHYSICAL = 4

    class AttackComplexity(proto.Enum):
        r"""

        Values:
            ATTACK_COMPLEXITY_UNSPECIFIED (0):
                No description available.
            ATTACK_COMPLEXITY_LOW (1):
                No description available.
            ATTACK_COMPLEXITY_HIGH (2):
                No description available.
            ATTACK_COMPLEXITY_MEDIUM (3):
                No description available.
        """
        ATTACK_COMPLEXITY_UNSPECIFIED = 0
        ATTACK_COMPLEXITY_LOW = 1
        ATTACK_COMPLEXITY_HIGH = 2
        ATTACK_COMPLEXITY_MEDIUM = 3

    class Authentication(proto.Enum):
        r"""

        Values:
            AUTHENTICATION_UNSPECIFIED (0):
                No description available.
            AUTHENTICATION_MULTIPLE (1):
                No description available.
            AUTHENTICATION_SINGLE (2):
                No description available.
            AUTHENTICATION_NONE (3):
                No description available.
        """
        AUTHENTICATION_UNSPECIFIED = 0
        AUTHENTICATION_MULTIPLE = 1
        AUTHENTICATION_SINGLE = 2
        AUTHENTICATION_NONE = 3

    class PrivilegesRequired(proto.Enum):
        r"""

        Values:
            PRIVILEGES_REQUIRED_UNSPECIFIED (0):
                No description available.
            PRIVILEGES_REQUIRED_NONE (1):
                No description available.
            PRIVILEGES_REQUIRED_LOW (2):
                No description available.
            PRIVILEGES_REQUIRED_HIGH (3):
                No description available.
        """
        PRIVILEGES_REQUIRED_UNSPECIFIED = 0
        PRIVILEGES_REQUIRED_NONE = 1
        PRIVILEGES_REQUIRED_LOW = 2
        PRIVILEGES_REQUIRED_HIGH = 3

    class UserInteraction(proto.Enum):
        r"""

        Values:
            USER_INTERACTION_UNSPECIFIED (0):
                No description available.
            USER_INTERACTION_NONE (1):
                No description available.
            USER_INTERACTION_REQUIRED (2):
                No description available.
        """
        USER_INTERACTION_UNSPECIFIED = 0
        USER_INTERACTION_NONE = 1
        USER_INTERACTION_REQUIRED = 2

    class Scope(proto.Enum):
        r"""

        Values:
            SCOPE_UNSPECIFIED (0):
                No description available.
            SCOPE_UNCHANGED (1):
                No description available.
            SCOPE_CHANGED (2):
                No description available.
        """
        SCOPE_UNSPECIFIED = 0
        SCOPE_UNCHANGED = 1
        SCOPE_CHANGED = 2

    class Impact(proto.Enum):
        r"""

        Values:
            IMPACT_UNSPECIFIED (0):
                No description available.
            IMPACT_HIGH (1):
                No description available.
            IMPACT_LOW (2):
                No description available.
            IMPACT_NONE (3):
                No description available.
            IMPACT_PARTIAL (4):
                No description available.
            IMPACT_COMPLETE (5):
                No description available.
        """
        IMPACT_UNSPECIFIED = 0
        IMPACT_HIGH = 1
        IMPACT_LOW = 2
        IMPACT_NONE = 3
        IMPACT_PARTIAL = 4
        IMPACT_COMPLETE = 5

    base_score: float = proto.Field(
        proto.FLOAT,
        number=1,
    )
    exploitability_score: float = proto.Field(
        proto.FLOAT,
        number=2,
    )
    impact_score: float = proto.Field(
        proto.FLOAT,
        number=3,
    )
    attack_vector: AttackVector = proto.Field(
        proto.ENUM,
        number=4,
        enum=AttackVector,
    )
    attack_complexity: AttackComplexity = proto.Field(
        proto.ENUM,
        number=5,
        enum=AttackComplexity,
    )
    authentication: Authentication = proto.Field(
        proto.ENUM,
        number=6,
        enum=Authentication,
    )
    privileges_required: PrivilegesRequired = proto.Field(
        proto.ENUM,
        number=7,
        enum=PrivilegesRequired,
    )
    user_interaction: UserInteraction = proto.Field(
        proto.ENUM,
        number=8,
        enum=UserInteraction,
    )
    scope: Scope = proto.Field(
        proto.ENUM,
        number=9,
        enum=Scope,
    )
    confidentiality_impact: Impact = proto.Field(
        proto.ENUM,
        number=10,
        enum=Impact,
    )
    integrity_impact: Impact = proto.Field(
        proto.ENUM,
        number=11,
        enum=Impact,
    )
    availability_impact: Impact = proto.Field(
        proto.ENUM,
        number=12,
        enum=Impact,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
