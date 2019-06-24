# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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


class Architecture(enum.IntEnum):
    """
    Instruction set architectures supported by various package managers.

    Attributes:
      ARCHITECTURE_UNSPECIFIED (int): Unknown architecture.
      X86 (int): X86 architecture.
      X64 (int): X64 architecture.
    """

    ARCHITECTURE_UNSPECIFIED = 0
    X86 = 1
    X64 = 2


class NoteKind(enum.IntEnum):
    """
    Kind represents the kinds of notes supported.

    Attributes:
      NOTE_KIND_UNSPECIFIED (int): Unknown.
      VULNERABILITY (int): The note and occurrence represent a package vulnerability.
      BUILD (int): The note and occurrence assert build provenance.
      IMAGE (int): This represents an image basis relationship.
      PACKAGE (int): This represents a package installed via a package manager.
      DEPLOYMENT (int): The note and occurrence track deployment events.
      DISCOVERY (int): The note and occurrence track the initial discovery status of a resource.
      ATTESTATION (int): This represents a logical "role" that can attest to artifacts.
    """

    NOTE_KIND_UNSPECIFIED = 0
    VULNERABILITY = 1
    BUILD = 2
    IMAGE = 3
    PACKAGE = 4
    DEPLOYMENT = 5
    DISCOVERY = 6
    ATTESTATION = 7


class Severity(enum.IntEnum):
    """
    Note provider assigned severity/impact ranking.

    Attributes:
      SEVERITY_UNSPECIFIED (int): Unknown.
      MINIMAL (int): Minimal severity.
      LOW (int): Low severity.
      MEDIUM (int): Medium severity.
      HIGH (int): High severity.
      CRITICAL (int): Critical severity.
    """

    SEVERITY_UNSPECIFIED = 0
    MINIMAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


class AliasContext(object):
    class Kind(enum.IntEnum):
        """
        The type of an alias.

        Attributes:
          KIND_UNSPECIFIED (int): Unknown.
          FIXED (int): Git tag.
          MOVABLE (int): Git branch.
          OTHER (int): Used to specify non-standard aliases. For example, if a Git repo has a
          ref named "refs/foo/bar".
        """

        KIND_UNSPECIFIED = 0
        FIXED = 1
        MOVABLE = 2
        OTHER = 4


class CVSSv3(object):
    class AttackComplexity(enum.IntEnum):
        """
        Attributes:
          ATTACK_COMPLEXITY_UNSPECIFIED (int)
          ATTACK_COMPLEXITY_LOW (int)
          ATTACK_COMPLEXITY_HIGH (int)
        """

        ATTACK_COMPLEXITY_UNSPECIFIED = 0
        ATTACK_COMPLEXITY_LOW = 1
        ATTACK_COMPLEXITY_HIGH = 2

    class AttackVector(enum.IntEnum):
        """
        Attributes:
          ATTACK_VECTOR_UNSPECIFIED (int)
          ATTACK_VECTOR_NETWORK (int)
          ATTACK_VECTOR_ADJACENT (int)
          ATTACK_VECTOR_LOCAL (int)
          ATTACK_VECTOR_PHYSICAL (int)
        """

        ATTACK_VECTOR_UNSPECIFIED = 0
        ATTACK_VECTOR_NETWORK = 1
        ATTACK_VECTOR_ADJACENT = 2
        ATTACK_VECTOR_LOCAL = 3
        ATTACK_VECTOR_PHYSICAL = 4

    class Impact(enum.IntEnum):
        """
        Attributes:
          IMPACT_UNSPECIFIED (int)
          IMPACT_HIGH (int)
          IMPACT_LOW (int)
          IMPACT_NONE (int)
        """

        IMPACT_UNSPECIFIED = 0
        IMPACT_HIGH = 1
        IMPACT_LOW = 2
        IMPACT_NONE = 3

    class PrivilegesRequired(enum.IntEnum):
        """
        Attributes:
          PRIVILEGES_REQUIRED_UNSPECIFIED (int)
          PRIVILEGES_REQUIRED_NONE (int)
          PRIVILEGES_REQUIRED_LOW (int)
          PRIVILEGES_REQUIRED_HIGH (int)
        """

        PRIVILEGES_REQUIRED_UNSPECIFIED = 0
        PRIVILEGES_REQUIRED_NONE = 1
        PRIVILEGES_REQUIRED_LOW = 2
        PRIVILEGES_REQUIRED_HIGH = 3

    class Scope(enum.IntEnum):
        """
        Attributes:
          SCOPE_UNSPECIFIED (int)
          SCOPE_UNCHANGED (int)
          SCOPE_CHANGED (int)
        """

        SCOPE_UNSPECIFIED = 0
        SCOPE_UNCHANGED = 1
        SCOPE_CHANGED = 2

    class UserInteraction(enum.IntEnum):
        """
        Attributes:
          USER_INTERACTION_UNSPECIFIED (int)
          USER_INTERACTION_NONE (int)
          USER_INTERACTION_REQUIRED (int)
        """

        USER_INTERACTION_UNSPECIFIED = 0
        USER_INTERACTION_NONE = 1
        USER_INTERACTION_REQUIRED = 2


class DeploymentOccurrence(object):
    class Platform(enum.IntEnum):
        """
        Types of platforms.

        Attributes:
          PLATFORM_UNSPECIFIED (int): Unknown.
          GKE (int): Google Container Engine.
          FLEX (int): Google App Engine: Flexible Environment.
          CUSTOM (int): Custom user-defined platform.
        """

        PLATFORM_UNSPECIFIED = 0
        GKE = 1
        FLEX = 2
        CUSTOM = 3


class DiscoveryOccurrence(object):
    class AnalysisStatus(enum.IntEnum):
        """
        Analysis status for a resource. Currently for initial analysis only (not
        updated in continuous analysis).

        Attributes:
          ANALYSIS_STATUS_UNSPECIFIED (int): Unknown.
          PENDING (int): Resource is known but no action has been taken yet.
          SCANNING (int): Resource is being analyzed.
          FINISHED_SUCCESS (int): Analysis has finished successfully.
          FINISHED_FAILED (int): Analysis has finished unsuccessfully, the analysis itself is in a bad
          state.
          FINISHED_UNSUPPORTED (int): The resource is known not to be supported
        """

        ANALYSIS_STATUS_UNSPECIFIED = 0
        PENDING = 1
        SCANNING = 2
        FINISHED_SUCCESS = 3
        FINISHED_FAILED = 4
        FINISHED_UNSUPPORTED = 5

    class ContinuousAnalysis(enum.IntEnum):
        """
        Whether the resource is continuously analyzed.

        Attributes:
          CONTINUOUS_ANALYSIS_UNSPECIFIED (int): Unknown.
          ACTIVE (int): The resource is continuously analyzed.
          INACTIVE (int): The resource is ignored for continuous analysis.
        """

        CONTINUOUS_ANALYSIS_UNSPECIFIED = 0
        ACTIVE = 1
        INACTIVE = 2


class Version(object):
    class VersionKind(enum.IntEnum):
        """
        Whether this is an ordinary package version or a sentinel MIN/MAX version.

        Attributes:
          VERSION_KIND_UNSPECIFIED (int): Unknown.
          NORMAL (int): A standard package version.
          MINIMUM (int): A special version representing negative infinity.
          MAXIMUM (int): A special version representing positive infinity.
        """

        VERSION_KIND_UNSPECIFIED = 0
        NORMAL = 1
        MINIMUM = 2
        MAXIMUM = 3
