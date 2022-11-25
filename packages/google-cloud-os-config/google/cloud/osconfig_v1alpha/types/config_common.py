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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.osconfig.v1alpha",
    manifest={
        "OSPolicyComplianceState",
        "OSPolicyResourceConfigStep",
        "OSPolicyResourceCompliance",
    },
)


class OSPolicyComplianceState(proto.Enum):
    r"""Supported OSPolicy compliance states."""
    _pb_options = {"deprecated": True}
    OS_POLICY_COMPLIANCE_STATE_UNSPECIFIED = 0
    COMPLIANT = 1
    NON_COMPLIANT = 2
    UNKNOWN = 3
    NO_OS_POLICIES_APPLICABLE = 4


class OSPolicyResourceConfigStep(proto.Message):
    r"""Step performed by the OS Config agent for configuring an
    ``OSPolicyResource`` to its desired state.

    Attributes:
        type_ (google.cloud.osconfig_v1alpha.types.OSPolicyResourceConfigStep.Type):
            Configuration step type.
        outcome (google.cloud.osconfig_v1alpha.types.OSPolicyResourceConfigStep.Outcome):
            Outcome of the configuration step.
        error_message (str):
            An error message recorded during the
            execution of this step. Only populated when
            outcome is FAILED.
    """

    class Type(proto.Enum):
        r"""Supported configuration step types"""
        _pb_options = {"deprecated": True}
        TYPE_UNSPECIFIED = 0
        VALIDATION = 1
        DESIRED_STATE_CHECK = 2
        DESIRED_STATE_ENFORCEMENT = 3
        DESIRED_STATE_CHECK_POST_ENFORCEMENT = 4

    class Outcome(proto.Enum):
        r"""Supported outcomes for a configuration step."""
        _pb_options = {"deprecated": True}
        OUTCOME_UNSPECIFIED = 0
        SUCCEEDED = 1
        FAILED = 2

    type_: Type = proto.Field(
        proto.ENUM,
        number=1,
        enum=Type,
    )
    outcome: Outcome = proto.Field(
        proto.ENUM,
        number=2,
        enum=Outcome,
    )
    error_message: str = proto.Field(
        proto.STRING,
        number=3,
    )


class OSPolicyResourceCompliance(proto.Message):
    r"""Compliance data for an OS policy resource.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        os_policy_resource_id (str):
            The id of the OS policy resource.
        config_steps (MutableSequence[google.cloud.osconfig_v1alpha.types.OSPolicyResourceConfigStep]):
            Ordered list of configuration steps taken by
            the agent for the OS policy resource.
        state (google.cloud.osconfig_v1alpha.types.OSPolicyComplianceState):
            Compliance state of the OS policy resource.
        exec_resource_output (google.cloud.osconfig_v1alpha.types.OSPolicyResourceCompliance.ExecResourceOutput):
            ExecResource specific output.

            This field is a member of `oneof`_ ``output``.
    """

    class ExecResourceOutput(proto.Message):
        r"""ExecResource specific output.

        Attributes:
            enforcement_output (bytes):
                Output from Enforcement phase output file (if
                run). Output size is limited to 100K bytes.
        """

        enforcement_output: bytes = proto.Field(
            proto.BYTES,
            number=2,
        )

    os_policy_resource_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    config_steps: MutableSequence["OSPolicyResourceConfigStep"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="OSPolicyResourceConfigStep",
    )
    state: "OSPolicyComplianceState" = proto.Field(
        proto.ENUM,
        number=3,
        enum="OSPolicyComplianceState",
    )
    exec_resource_output: ExecResourceOutput = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="output",
        message=ExecResourceOutput,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
