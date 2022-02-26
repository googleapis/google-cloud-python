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
    package="google.cloud.osconfig.v1",
    manifest={
        "GetOSPolicyAssignmentReportRequest",
        "ListOSPolicyAssignmentReportsRequest",
        "ListOSPolicyAssignmentReportsResponse",
        "OSPolicyAssignmentReport",
    },
)


class GetOSPolicyAssignmentReportRequest(proto.Message):
    r"""Get a report of the OS policy assignment for a VM instance.

    Attributes:
        name (str):
            Required. API resource name for OS policy assignment report.

            Format:
            ``/projects/{project}/locations/{location}/instances/{instance}/osPolicyAssignments/{assignment}/report``

            For ``{project}``, either ``project-number`` or
            ``project-id`` can be provided. For ``{instance_id}``,
            either Compute Engine ``instance-id`` or ``instance-name``
            can be provided. For ``{assignment_id}``, the
            OSPolicyAssignment id must be provided.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListOSPolicyAssignmentReportsRequest(proto.Message):
    r"""List the OS policy assignment reports for VM instances.

    Attributes:
        parent (str):
            Required. The parent resource name.

            Format:
            ``projects/{project}/locations/{location}/instances/{instance}/osPolicyAssignments/{assignment}/reports``

            For ``{project}``, either ``project-number`` or
            ``project-id`` can be provided. For ``{instance}``, either
            ``instance-name``, ``instance-id``, or ``-`` can be
            provided. If '-' is provided, the response will include
            OSPolicyAssignmentReports for all instances in the
            project/location. For ``{assignment}``, either
            ``assignment-id`` or ``-`` can be provided. If '-' is
            provided, the response will include
            OSPolicyAssignmentReports for all OSPolicyAssignments in the
            project/location. Either {instance} or {assignment} must be
            ``-``.

            For example:
            ``projects/{project}/locations/{location}/instances/{instance}/osPolicyAssignments/-/reports``
            returns all reports for the instance
            ``projects/{project}/locations/{location}/instances/-/osPolicyAssignments/{assignment-id}/reports``
            returns all the reports for the given assignment across all
            instances.
            ``projects/{project}/locations/{location}/instances/-/osPolicyAssignments/-/reports``
            returns all the reports for all assignments across all
            instances.
        page_size (int):
            The maximum number of results to return.
        filter (str):
            If provided, this field specifies the criteria that must be
            met by the ``OSPolicyAssignmentReport`` API resource that is
            included in the response.
        page_token (str):
            A pagination token returned from a previous call to the
            ``ListOSPolicyAssignmentReports`` method that indicates
            where this listing should continue from.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    filter = proto.Field(proto.STRING, number=3,)
    page_token = proto.Field(proto.STRING, number=4,)


class ListOSPolicyAssignmentReportsResponse(proto.Message):
    r"""A response message for listing OS Policy assignment reports
    including the page of results and page token.

    Attributes:
        os_policy_assignment_reports (Sequence[google.cloud.osconfig_v1.types.OSPolicyAssignmentReport]):
            List of OS policy assignment reports.
        next_page_token (str):
            The pagination token to retrieve the next
            page of OS policy assignment report objects.
    """

    @property
    def raw_page(self):
        return self

    os_policy_assignment_reports = proto.RepeatedField(
        proto.MESSAGE, number=1, message="OSPolicyAssignmentReport",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class OSPolicyAssignmentReport(proto.Message):
    r"""A report of the OS policy assignment status for a given
    instance.

    Attributes:
        name (str):
            The ``OSPolicyAssignmentReport`` API resource name.

            Format:
            ``projects/{project_number}/locations/{location}/instances/{instance_id}/osPolicyAssignments/{os_policy_assignment_id}/report``
        instance (str):
            The Compute Engine VM instance name.
        os_policy_assignment (str):
            Reference to the ``OSPolicyAssignment`` API resource that
            the ``OSPolicy`` belongs to.

            Format:
            ``projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id@revision_id}``
        os_policy_compliances (Sequence[google.cloud.osconfig_v1.types.OSPolicyAssignmentReport.OSPolicyCompliance]):
            Compliance data for each ``OSPolicy`` that is applied to the
            VM.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp for when the report was last
            generated.
        last_run_id (str):
            Unique identifier of the last attempted run
            to apply the OS policies associated with this
            assignment on the VM.
            This ID is logged by the OS Config agent while
            applying the OS policies associated with this
            assignment on the VM. NOTE: If the service is
            unable to successfully connect to the agent for
            this run, then this id will not be available in
            the agent logs.
    """

    class OSPolicyCompliance(proto.Message):
        r"""Compliance data for an OS policy

        Attributes:
            os_policy_id (str):
                The OS policy id
            compliance_state (google.cloud.osconfig_v1.types.OSPolicyAssignmentReport.OSPolicyCompliance.ComplianceState):
                The compliance state of the OS policy.
            compliance_state_reason (str):
                The reason for the OS policy to be in an unknown compliance
                state. This field is always populated when
                ``compliance_state`` is ``UNKNOWN``.

                If populated, the field can contain one of the following
                values:

                -  ``vm-not-running``: The VM was not running.
                -  ``os-policies-not-supported-by-agent``: The version of
                   the OS Config agent running on the VM does not support
                   running OS policies.
                -  ``no-agent-detected``: The OS Config agent is not
                   detected for the VM.
                -  ``resource-execution-errors``: The OS Config agent
                   encountered errors while executing one or more resources
                   in the policy. See ``os_policy_resource_compliances`` for
                   details.
                -  ``task-timeout``: The task sent to the agent to apply the
                   policy timed out.
                -  ``unexpected-agent-state``: The OS Config agent did not
                   report the final status of the task that attempted to
                   apply the policy. Instead, the agent unexpectedly started
                   working on a different task. This mostly happens when the
                   agent or VM unexpectedly restarts while applying OS
                   policies.
                -  ``internal-service-errors``: Internal service errors were
                   encountered while attempting to apply the policy.
            os_policy_resource_compliances (Sequence[google.cloud.osconfig_v1.types.OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance]):
                Compliance data for each resource within the
                policy that is applied to the VM.
        """

        class ComplianceState(proto.Enum):
            r"""Possible compliance states for an os policy."""
            UNKNOWN = 0
            COMPLIANT = 1
            NON_COMPLIANT = 2

        class OSPolicyResourceCompliance(proto.Message):
            r"""Compliance data for an OS policy resource.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                os_policy_resource_id (str):
                    The ID of the OS policy resource.
                config_steps (Sequence[google.cloud.osconfig_v1.types.OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance.OSPolicyResourceConfigStep]):
                    Ordered list of configuration completed by
                    the agent for the OS policy resource.
                compliance_state (google.cloud.osconfig_v1.types.OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance.ComplianceState):
                    The compliance state of the resource.
                compliance_state_reason (str):
                    A reason for the resource to be in the given compliance
                    state. This field is always populated when
                    ``compliance_state`` is ``UNKNOWN``.

                    The following values are supported when
                    ``compliance_state == UNKNOWN``

                    -  ``execution-errors``: Errors were encountered by the
                       agent while executing the resource and the compliance
                       state couldn't be determined.
                    -  ``execution-skipped-by-agent``: Resource execution was
                       skipped by the agent because errors were encountered
                       while executing prior resources in the OS policy.
                    -  ``os-policy-execution-attempt-failed``: The execution of
                       the OS policy containing this resource failed and the
                       compliance state couldn't be determined.
                exec_resource_output (google.cloud.osconfig_v1.types.OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance.ExecResourceOutput):
                    ExecResource specific output.

                    This field is a member of `oneof`_ ``output``.
            """

            class ComplianceState(proto.Enum):
                r"""Possible compliance states for a resource."""
                UNKNOWN = 0
                COMPLIANT = 1
                NON_COMPLIANT = 2

            class OSPolicyResourceConfigStep(proto.Message):
                r"""Step performed by the OS Config agent for configuring an
                ``OSPolicy`` resource to its desired state.

                Attributes:
                    type_ (google.cloud.osconfig_v1.types.OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance.OSPolicyResourceConfigStep.Type):
                        Configuration step type.
                    error_message (str):
                        An error message recorded during the
                        execution of this step. Only populated if errors
                        were encountered during this step execution.
                """

                class Type(proto.Enum):
                    r"""Supported configuration step types"""
                    TYPE_UNSPECIFIED = 0
                    VALIDATION = 1
                    DESIRED_STATE_CHECK = 2
                    DESIRED_STATE_ENFORCEMENT = 3
                    DESIRED_STATE_CHECK_POST_ENFORCEMENT = 4

                type_ = proto.Field(
                    proto.ENUM,
                    number=1,
                    enum="OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance.OSPolicyResourceConfigStep.Type",
                )
                error_message = proto.Field(proto.STRING, number=2,)

            class ExecResourceOutput(proto.Message):
                r"""ExecResource specific output.

                Attributes:
                    enforcement_output (bytes):
                        Output from enforcement phase output file (if
                        run). Output size is limited to 100K bytes.
                """

                enforcement_output = proto.Field(proto.BYTES, number=2,)

            os_policy_resource_id = proto.Field(proto.STRING, number=1,)
            config_steps = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance.OSPolicyResourceConfigStep",
            )
            compliance_state = proto.Field(
                proto.ENUM,
                number=3,
                enum="OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance.ComplianceState",
            )
            compliance_state_reason = proto.Field(proto.STRING, number=4,)
            exec_resource_output = proto.Field(
                proto.MESSAGE,
                number=5,
                oneof="output",
                message="OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance.ExecResourceOutput",
            )

        os_policy_id = proto.Field(proto.STRING, number=1,)
        compliance_state = proto.Field(
            proto.ENUM,
            number=2,
            enum="OSPolicyAssignmentReport.OSPolicyCompliance.ComplianceState",
        )
        compliance_state_reason = proto.Field(proto.STRING, number=3,)
        os_policy_resource_compliances = proto.RepeatedField(
            proto.MESSAGE,
            number=4,
            message="OSPolicyAssignmentReport.OSPolicyCompliance.OSPolicyResourceCompliance",
        )

    name = proto.Field(proto.STRING, number=1,)
    instance = proto.Field(proto.STRING, number=2,)
    os_policy_assignment = proto.Field(proto.STRING, number=3,)
    os_policy_compliances = proto.RepeatedField(
        proto.MESSAGE, number=4, message=OSPolicyCompliance,
    )
    update_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    last_run_id = proto.Field(proto.STRING, number=6,)


__all__ = tuple(sorted(__protobuf__.manifest))
