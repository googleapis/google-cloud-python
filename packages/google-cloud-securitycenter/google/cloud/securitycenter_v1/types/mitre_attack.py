# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
    package="google.cloud.securitycenter.v1",
    manifest={
        "MitreAttack",
    },
)


class MitreAttack(proto.Message):
    r"""MITRE ATT&CK tactics and techniques related to this finding.
    See: https://attack.mitre.org

    Attributes:
        primary_tactic (google.cloud.securitycenter_v1.types.MitreAttack.Tactic):
            The MITRE ATT&CK tactic most closely
            represented by this finding, if any.
        primary_techniques (Sequence[google.cloud.securitycenter_v1.types.MitreAttack.Technique]):
            The MITRE ATT&CK technique most closely represented by this
            finding, if any. primary_techniques is a repeated field
            because there are multiple levels of MITRE ATT&CK
            techniques. If the technique most closely represented by
            this finding is a sub-technique (e.g.
            ``SCANNING_IP_BLOCKS``), both the sub-technique and its
            parent technique(s) will be listed (e.g.
            ``SCANNING_IP_BLOCKS``, ``ACTIVE_SCANNING``).
        additional_tactics (Sequence[google.cloud.securitycenter_v1.types.MitreAttack.Tactic]):
            Additional MITRE ATT&CK tactics related to
            this finding, if any.
        additional_techniques (Sequence[google.cloud.securitycenter_v1.types.MitreAttack.Technique]):
            Additional MITRE ATT&CK techniques related to
            this finding, if any, along with any of their
            respective parent techniques.
        version (str):
            The MITRE ATT&CK version referenced by the
            above fields. E.g. "8".
    """

    class Tactic(proto.Enum):
        r"""MITRE ATT&CK tactics that can be referenced by SCC findings.
        See: https://attack.mitre.org/tactics/enterprise/
        """
        TACTIC_UNSPECIFIED = 0
        RECONNAISSANCE = 1
        RESOURCE_DEVELOPMENT = 2
        INITIAL_ACCESS = 5
        EXECUTION = 3
        PERSISTENCE = 6
        PRIVILEGE_ESCALATION = 8
        DEFENSE_EVASION = 7
        CREDENTIAL_ACCESS = 9
        DISCOVERY = 10
        LATERAL_MOVEMENT = 11
        COLLECTION = 12
        COMMAND_AND_CONTROL = 4
        EXFILTRATION = 13
        IMPACT = 14

    class Technique(proto.Enum):
        r"""MITRE ATT&CK techniques that can be referenced by SCC
        findings. See: https://attack.mitre.org/techniques/enterprise/
        """
        TECHNIQUE_UNSPECIFIED = 0
        ACTIVE_SCANNING = 1
        SCANNING_IP_BLOCKS = 2
        INGRESS_TOOL_TRANSFER = 3
        NATIVE_API = 4
        SHARED_MODULES = 5
        COMMAND_AND_SCRIPTING_INTERPRETER = 6
        UNIX_SHELL = 7
        RESOURCE_HIJACKING = 8
        PROXY = 9
        EXTERNAL_PROXY = 10
        MULTI_HOP_PROXY = 11
        DYNAMIC_RESOLUTION = 12
        UNSECURED_CREDENTIALS = 13
        VALID_ACCOUNTS = 14
        LOCAL_ACCOUNTS = 15
        CLOUD_ACCOUNTS = 16
        NETWORK_DENIAL_OF_SERVICE = 17
        PERMISSION_GROUPS_DISCOVERY = 18
        CLOUD_GROUPS = 19
        EXFILTRATION_OVER_WEB_SERVICE = 20
        EXFILTRATION_TO_CLOUD_STORAGE = 21
        ACCOUNT_MANIPULATION = 22
        SSH_AUTHORIZED_KEYS = 23
        CREATE_OR_MODIFY_SYSTEM_PROCESS = 24
        STEAL_WEB_SESSION_COOKIE = 25
        MODIFY_CLOUD_COMPUTE_INFRASTRUCTURE = 26
        EXPLOIT_PUBLIC_FACING_APPLICATION = 27
        MODIFY_AUTHENTICATION_PROCESS = 28
        DATA_DESTRUCTION = 29
        DOMAIN_POLICY_MODIFICATION = 30
        IMPAIR_DEFENSES = 31
        NETWORK_SERVICE_DISCOVERY = 32
        ACCESS_TOKEN_MANIPULATION = 33
        ABUSE_ELEVATION_CONTROL_MECHANISM = 34

    primary_tactic = proto.Field(
        proto.ENUM,
        number=1,
        enum=Tactic,
    )
    primary_techniques = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=Technique,
    )
    additional_tactics = proto.RepeatedField(
        proto.ENUM,
        number=3,
        enum=Tactic,
    )
    additional_techniques = proto.RepeatedField(
        proto.ENUM,
        number=4,
        enum=Technique,
    )
    version = proto.Field(
        proto.STRING,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
