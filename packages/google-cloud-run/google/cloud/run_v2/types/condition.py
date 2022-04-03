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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.run.v2",
    manifest={
        "Condition",
    },
)


class Condition(proto.Message):
    r"""Defines a status condition for a resource.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        type_ (str):
            type is used to communicate the status of the reconciliation
            process. See also:
            https://github.com/knative/serving/blob/main/docs/spec/errors.md#error-conditions-and-reporting
            Types common to all resources include:

            -  "Ready": True when the Resource is ready.
        state (google.cloud.run_v2.types.Condition.State):
            State of the condition.
        message (str):
            Human readable message indicating details
            about the current status.
        last_transition_time (google.protobuf.timestamp_pb2.Timestamp):
            Last time the condition transitioned from one
            status to another.
        severity (google.cloud.run_v2.types.Condition.Severity):
            How to interpret failures of this condition,
            one of Error, Warning, Info
        reason (google.cloud.run_v2.types.Condition.CommonReason):
            A common (service-level) reason for this
            condition.

            This field is a member of `oneof`_ ``reasons``.
        internal_reason (google.cloud.run_v2.types.Condition.InternalReason):
            A reason for the internal condition.

            This field is a member of `oneof`_ ``reasons``.
        domain_mapping_reason (google.cloud.run_v2.types.Condition.DomainMappingReason):
            A reason for the domain mapping condition.

            This field is a member of `oneof`_ ``reasons``.
        revision_reason (google.cloud.run_v2.types.Condition.RevisionReason):
            A reason for the revision condition.

            This field is a member of `oneof`_ ``reasons``.
        execution_reason (google.cloud.run_v2.types.Condition.ExecutionReason):
            A reason for the execution condition.

            This field is a member of `oneof`_ ``reasons``.
    """

    class State(proto.Enum):
        r"""Represents the possible Condition states."""
        STATE_UNSPECIFIED = 0
        CONDITION_PENDING = 1
        CONDITION_RECONCILING = 2
        CONDITION_FAILED = 3
        CONDITION_SUCCEEDED = 4

    class Severity(proto.Enum):
        r"""Represents the severity of the condition failures."""
        SEVERITY_UNSPECIFIED = 0
        ERROR = 1
        WARNING = 2
        INFO = 3

    class CommonReason(proto.Enum):
        r"""Reasons common to all types of conditions."""
        COMMON_REASON_UNDEFINED = 0
        UNKNOWN = 1
        ROUTE_MISSING = 2
        REVISION_FAILED = 3
        PROGRESS_DEADLINE_EXCEEDED = 4
        BUILD_STEP_FAILED = 5
        CONTAINER_MISSING = 6
        CONTAINER_PERMISSION_DENIED = 7
        CONTAINER_IMAGE_UNAUTHORIZED = 8
        CONTAINER_IMAGE_AUTHORIZATION_CHECK_FAILED = 9
        ENCRYPTION_KEY_PERMISSION_DENIED = 10
        ENCRYPTION_KEY_CHECK_FAILED = 11
        SECRETS_ACCESS_CHECK_FAILED = 12
        WAITING_FOR_OPERATION = 13
        IMMEDIATE_RETRY = 14
        POSTPONED_RETRY = 15

    class InternalReason(proto.Enum):
        r"""Reasons applicable to internal resources not exposed to
        users. These will surface in Service.conditions, and could be
        useful for further diagnosis.
        """
        INTERNAL_REASON_UNDEFINED = 0
        CONFLICTING_REVISION_NAME = 1
        REVISION_MISSING = 2
        CONFIGURATION_MISSING = 3
        ASSIGNING_TRAFFIC = 4
        UPDATING_INGRESS_TRAFFIC_ALLOWED = 5
        REVISION_ORG_POLICY_VIOLATION = 6
        ENABLING_GCFV2_URI_SUPPORT = 7

    class DomainMappingReason(proto.Enum):
        r"""Reasons specific to DomainMapping resource."""
        DOMAIN_MAPPING_REASON_UNDEFINED = 0
        ROUTE_NOT_READY = 1
        PERMISSION_DENIED = 2
        CERTIFICATE_ALREADY_EXISTS = 3
        MAPPING_ALREADY_EXISTS = 4
        CERTIFICATE_PENDING = 5
        CERTIFICATE_FAILED = 6

    class RevisionReason(proto.Enum):
        r"""Reasons specific to Revision resource."""
        REVISION_REASON_UNDEFINED = 0
        PENDING = 1
        RESERVE = 2
        RETIRED = 3
        RETIRING = 4
        RECREATING = 5
        HEALTH_CHECK_CONTAINER_ERROR = 6
        CUSTOMIZED_PATH_RESPONSE_PENDING = 7
        MIN_INSTANCES_NOT_PROVISIONED = 8
        ACTIVE_REVISION_LIMIT_REACHED = 9
        NO_DEPLOYMENT = 10
        HEALTH_CHECK_SKIPPED = 11

    class ExecutionReason(proto.Enum):
        r"""Reasons specific to Execution resource."""
        EXECUTION_REASON_UNDEFINED = 0
        JOB_STATUS_SERVICE_POLLING_ERROR = 1
        NON_ZERO_EXIT_CODE = 2

    type_ = proto.Field(
        proto.STRING,
        number=1,
    )
    state = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    message = proto.Field(
        proto.STRING,
        number=3,
    )
    last_transition_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    severity = proto.Field(
        proto.ENUM,
        number=5,
        enum=Severity,
    )
    reason = proto.Field(
        proto.ENUM,
        number=6,
        oneof="reasons",
        enum=CommonReason,
    )
    internal_reason = proto.Field(
        proto.ENUM,
        number=7,
        oneof="reasons",
        enum=InternalReason,
    )
    domain_mapping_reason = proto.Field(
        proto.ENUM,
        number=8,
        oneof="reasons",
        enum=DomainMappingReason,
    )
    revision_reason = proto.Field(
        proto.ENUM,
        number=9,
        oneof="reasons",
        enum=RevisionReason,
    )
    execution_reason = proto.Field(
        proto.ENUM,
        number=11,
        oneof="reasons",
        enum=ExecutionReason,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
