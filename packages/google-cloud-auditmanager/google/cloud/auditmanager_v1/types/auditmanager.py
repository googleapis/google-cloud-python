# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

import google.protobuf.timestamp_pb2 as timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.auditmanager.v1",
    manifest={
        "OperationState",
        "ComplianceState",
        "EnrollResourceRequest",
        "GenerateAuditScopeReportRequest",
        "GenerateAuditReportRequest",
        "GetResourceEnrollmentStatusRequest",
        "ListResourceEnrollmentStatusesRequest",
        "ListResourceEnrollmentStatusesResponse",
        "ListAuditReportsRequest",
        "ListAuditReportsResponse",
        "GetAuditReportRequest",
        "ListControlsRequest",
        "ListControlsResponse",
        "ReportGenerationProgress",
        "Enrollment",
        "AuditScopeReport",
        "OperationMetadata",
        "ResourceEnrollmentStatus",
        "AuditReport",
        "ControlFamily",
        "Control",
        "DestinationDetails",
        "ReportSummary",
        "ControlDetails",
    },
)


class OperationState(proto.Enum):
    r"""The different execution states of the Audit Manager service.

    Values:
        OPERATION_STATE_UNSPECIFIED (0):
            Unspecified. Invalid state.
        OPERATION_STATE_NOT_STARTED (10):
            Audit report generation process has not
            started.
        OPERATION_STATE_EVALUATION_IN_PROGRESS (20):
            Audit Manager is currently evaluating the
            workloads against specific standard.
        OPERATION_STATE_EVALUATION_DONE (21):
            Audit Manager has completed Evaluation for
            the workload.
        OPERATION_STATE_EVIDENCE_REPORT_GENERATION_IN_PROGRESS (30):
            Audit Manager is creating audit report from
            the evaluated data.
        OPERATION_STATE_EVIDENCE_REPORT_GENERATION_DONE (31):
            Audit Manager has completed generation of the
            audit report.
        OPERATION_STATE_EVIDENCE_UPLOAD_IN_PROGRESS (40):
            Audit Manager is uploading the audit report
            and evidences to the customer provided
            destination.
        OPERATION_STATE_DONE (50):
            Audit report generation process is completed.
        OPERATION_STATE_FAILED (60):
            Audit report generation process has failed.
    """
    OPERATION_STATE_UNSPECIFIED = 0
    OPERATION_STATE_NOT_STARTED = 10
    OPERATION_STATE_EVALUATION_IN_PROGRESS = 20
    OPERATION_STATE_EVALUATION_DONE = 21
    OPERATION_STATE_EVIDENCE_REPORT_GENERATION_IN_PROGRESS = 30
    OPERATION_STATE_EVIDENCE_REPORT_GENERATION_DONE = 31
    OPERATION_STATE_EVIDENCE_UPLOAD_IN_PROGRESS = 40
    OPERATION_STATE_DONE = 50
    OPERATION_STATE_FAILED = 60


class ComplianceState(proto.Enum):
    r"""The compliance state after evaluation.

    Values:
        COMPLIANCE_STATE_UNSPECIFIED (0):
            Unspecified. Invalid state.
        COMPLIANT (1):
            Compliant.
        VIOLATION (2):
            Violation.
        MANUAL_REVIEW_NEEDED (3):
            MANUAL_REVIEW_NEEDED, requires manual review
        ERROR (4):
            Error while computing status.
        AUDIT_NOT_SUPPORTED (5):
            Cannot be audited
    """
    COMPLIANCE_STATE_UNSPECIFIED = 0
    COMPLIANT = 1
    VIOLATION = 2
    MANUAL_REVIEW_NEEDED = 3
    ERROR = 4
    AUDIT_NOT_SUPPORTED = 5


class EnrollResourceRequest(proto.Message):
    r"""Request message to subscribe the Audit Manager service for
    given resource.

    Attributes:
        scope (str):
            Required. The resource to be enrolled to the audit manager.
            Scope format should be resource_type/resource_identifier Eg:
            projects/{project}/locations/{location},
            folders/{folder}/locations/{location}
            organizations/{organization}/locations/{location}
        destinations (MutableSequence[google.cloud.auditmanager_v1.types.EnrollResourceRequest.EligibleDestination]):
            Required. List of destination among which
            customer can choose to upload their reports
            during the audit process. While enrolling at a
            organization/folder level, customer can choose
            Cloud storage bucket in any project. If the
            audit is triggered at project level using the
            service agent at organization/folder level, all
            the destination options associated with
            respective organization/folder level service
            agent will be available to auditing projects.
    """

    class EligibleDestination(proto.Message):
        r"""The destination details where the audit report must be
        uploaded.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            eligible_gcs_bucket (str):
                The Cloud Storage bucket location where the audit report and
                evidences can be uploaded during the ``GenerateAuditReport``
                API call.

                This field is a member of `oneof`_ ``eligible_destinations``.
        """

        eligible_gcs_bucket: str = proto.Field(
            proto.STRING,
            number=3,
            oneof="eligible_destinations",
        )

    scope: str = proto.Field(
        proto.STRING,
        number=1,
    )
    destinations: MutableSequence[EligibleDestination] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=EligibleDestination,
    )


class GenerateAuditScopeReportRequest(proto.Message):
    r"""Message for requesting audit scope report.

    Attributes:
        scope (str):
            Required. Scope for which the AuditScopeReport is required.
            Must be of format resource_type/resource_identifier Eg:
            projects/{project}/locations/{location},
            folders/{folder}/locations/{location}
        compliance_standard (str):
            Required. Compliance Standard against which the Scope Report
            must be generated. Eg: FEDRAMP_MODERATE
        report_format (google.cloud.auditmanager_v1.types.GenerateAuditScopeReportRequest.AuditScopeReportFormat):
            Required. The format in which the Scope
            report bytes should be returned.
        compliance_framework (str):
            Required. Compliance framework against which
            the Scope Report must be generated.
    """

    class AuditScopeReportFormat(proto.Enum):
        r"""The options for the audit scope report format.

        Values:
            AUDIT_SCOPE_REPORT_FORMAT_UNSPECIFIED (0):
                Unspecified. Invalid format.
            AUDIT_SCOPE_REPORT_FORMAT_ODF (1):
                Audit Scope Report creation format is Open
                Document.
        """
        AUDIT_SCOPE_REPORT_FORMAT_UNSPECIFIED = 0
        AUDIT_SCOPE_REPORT_FORMAT_ODF = 1

    scope: str = proto.Field(
        proto.STRING,
        number=2,
    )
    compliance_standard: str = proto.Field(
        proto.STRING,
        number=3,
    )
    report_format: AuditScopeReportFormat = proto.Field(
        proto.ENUM,
        number=4,
        enum=AuditScopeReportFormat,
    )
    compliance_framework: str = proto.Field(
        proto.STRING,
        number=5,
    )


class GenerateAuditReportRequest(proto.Message):
    r"""Message for requesting the Audit Report.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_uri (str):
            Destination Cloud storage bucket where report
            and evidence must be uploaded. The Cloud storage
            bucket provided here must be selected among the
            buckets entered during the enrollment process.

            This field is a member of `oneof`_ ``destination``.
        scope (str):
            Required. Scope for which the AuditScopeReport is required.
            Must be of format resource_type/resource_identifier Eg:
            projects/{project}/locations/{location},
            folders/{folder}/locations/{location}
        compliance_standard (str):
            Required. Compliance Standard against which the Scope Report
            must be generated. Eg: FEDRAMP_MODERATE
        report_format (google.cloud.auditmanager_v1.types.GenerateAuditReportRequest.AuditReportFormat):
            Required. The format in which the audit
            report should be created.
        compliance_framework (str):
            Required. Compliance framework against which
            the Report must be generated.
    """

    class AuditReportFormat(proto.Enum):
        r"""The options for the audit report format.

        Values:
            AUDIT_REPORT_FORMAT_UNSPECIFIED (0):
                Unspecified. Invalid state.
            AUDIT_REPORT_FORMAT_ODF (1):
                Audit Report creation format is Open
                Document.
        """
        AUDIT_REPORT_FORMAT_UNSPECIFIED = 0
        AUDIT_REPORT_FORMAT_ODF = 1

    gcs_uri: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="destination",
    )
    scope: str = proto.Field(
        proto.STRING,
        number=1,
    )
    compliance_standard: str = proto.Field(
        proto.STRING,
        number=3,
    )
    report_format: AuditReportFormat = proto.Field(
        proto.ENUM,
        number=4,
        enum=AuditReportFormat,
    )
    compliance_framework: str = proto.Field(
        proto.STRING,
        number=5,
    )


class GetResourceEnrollmentStatusRequest(proto.Message):
    r"""Message for getting the enrollment status of a resource.

    Attributes:
        name (str):
            Required. Format
            folders/{folder}/locations/{location}/resourceEnrollmentStatuses/{resource_enrollment_status},
            projects/{project}/locations/{location}/resourceEnrollmentStatuses/{resource_enrollment_status},
            organizations/{organization}/locations/{location}/resourceEnrollmentStatuses/{resource_enrollment_status}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListResourceEnrollmentStatusesRequest(proto.Message):
    r"""Message for listing all the descendent resources under parent
    with enrollment.

    Attributes:
        parent (str):
            Required. The parent scope for which the list
            of resources with enrollments are required.
        page_size (int):
            Optional. The maximum number of resources to
            return.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            List request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListResourceEnrollmentStatusesResponse(proto.Message):
    r"""Response message with all the descendent resources with
    enrollment.

    Attributes:
        resource_enrollment_statuses (MutableSequence[google.cloud.auditmanager_v1.types.ResourceEnrollmentStatus]):
            The resources with their enrollment status.
        next_page_token (str):
            Output only. The token to retrieve the next
            page of results.
    """

    @property
    def raw_page(self):
        return self

    resource_enrollment_statuses: MutableSequence[
        "ResourceEnrollmentStatus"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ResourceEnrollmentStatus",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListAuditReportsRequest(proto.Message):
    r"""Message for requesting to list the audit reports.

    Attributes:
        parent (str):
            Required. The parent scope for which to list
            the reports.
        page_size (int):
            Optional. The maximum number of resources to
            return.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            List request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListAuditReportsResponse(proto.Message):
    r"""Response message with all the audit reports.

    Attributes:
        audit_reports (MutableSequence[google.cloud.auditmanager_v1.types.AuditReport]):
            Output only. The audit reports.
        next_page_token (str):
            Output only. The token to retrieve the next
            page of results.
    """

    @property
    def raw_page(self):
        return self

    audit_reports: MutableSequence["AuditReport"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AuditReport",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetAuditReportRequest(proto.Message):
    r"""Message for requesting the overall audit report for an audit
    report name.

    Attributes:
        name (str):
            Required. Format
            projects/{project}/locations/{location}/auditReports/{audit_report},
            folders/{folder}/locations/{location}/auditReports/{audit_report}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListControlsRequest(proto.Message):
    r"""Message for requesting all the controls for a compliance
    standard.

    Attributes:
        parent (str):
            Required. Format
            projects/{project}/locations/{location}/standards/{standard},
            folders/{folder}/locations/{location}/standards/{standard}
        page_size (int):
            Optional. The maximum number of resources to
            return.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            List request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListControlsResponse(proto.Message):
    r"""Response message with all the controls for a compliance
    standard.

    Attributes:
        controls (MutableSequence[google.cloud.auditmanager_v1.types.Control]):
            Output only. The controls for the compliance
            standard.
        next_page_token (str):
            Output only. The token to retrieve the next
            page of results.
    """

    @property
    def raw_page(self):
        return self

    controls: MutableSequence["Control"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Control",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ReportGenerationProgress(proto.Message):
    r"""The ``ReportGenerationProgress`` is part of
    [google.longrunning.Operation][google.longrunning.Operation]
    returned to the client for every ``GetOperation`` request.

    Attributes:
        state (google.cloud.auditmanager_v1.types.OperationState):
            Output only. The current state of execution
            for report generation.
        failure_reason (str):
            Output only. States the reason of failure during the audit
            report generation process. This field is set only if the
            state attribute is OPERATION_STATE_FAILED.
        evaluation_percent_complete (float):
            Shows the progress of the CESS service
            evaluation process. The progress is defined in
            terms of percentage complete and is being
            fetched from the CESS service.
        report_generation_percent_complete (float):
            Shows the report generation progress of the CESS Result
            Processor Service. The // progress is defined in terms of
            percentage complete and is being fetched from the CESS
            service. If report_generation_in_progress is non zero then
            evaluation_percent_complete will be 100%.
        report_uploading_percent_complete (float):
            Shows the report uploading progress of the CESS Result
            Processor Service. The progress is defined in terms of
            percentage complete and is being fetched from the CESS
            service. If report_uploading_in_progress is non zero then
            evaluation_percent_complete and
            report_generation_percent_complete will be 100%.
        destination_gcs_bucket (str):
            Output only. The Cloud Storage bucket where
            the audit report will be uploaded once the
            evaluation process is completed.
        audit_report (str):
            Output only. The name of the audit report.
    """

    state: "OperationState" = proto.Field(
        proto.ENUM,
        number=1,
        enum="OperationState",
    )
    failure_reason: str = proto.Field(
        proto.STRING,
        number=2,
    )
    evaluation_percent_complete: float = proto.Field(
        proto.DOUBLE,
        number=20,
    )
    report_generation_percent_complete: float = proto.Field(
        proto.DOUBLE,
        number=30,
    )
    report_uploading_percent_complete: float = proto.Field(
        proto.DOUBLE,
        number=40,
    )
    destination_gcs_bucket: str = proto.Field(
        proto.STRING,
        number=50,
    )
    audit_report: str = proto.Field(
        proto.STRING,
        number=51,
    )


class Enrollment(proto.Message):
    r"""The enrollment resource.

    Attributes:
        name (str):
            Identifier. The name of this Enrollment, in
            the format of scope given in request.
        destination_details (MutableSequence[google.cloud.auditmanager_v1.types.DestinationDetails]):
            Output only. The locations where the
            generated reports can be uploaded.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    destination_details: MutableSequence["DestinationDetails"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="DestinationDetails",
    )


class AuditScopeReport(proto.Message):
    r"""The audit scope report.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        scope_report_contents (bytes):
            The audit scope report content in byte
            format.

            This field is a member of `oneof`_ ``audit_report``.
        name (str):
            Identifier. The name of this Audit Report, in
            the format of scope given in request.
    """

    scope_report_contents: bytes = proto.Field(
        proto.BYTES,
        number=1,
        oneof="audit_report",
    )
    name: str = proto.Field(
        proto.STRING,
        number=2,
    )


class OperationMetadata(proto.Message):
    r"""The metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


class ResourceEnrollmentStatus(proto.Message):
    r"""A resource with its enrollment status.

    Attributes:
        name (str):
            Identifier. The name of this resource.
        enrollment (google.cloud.auditmanager_v1.types.Enrollment):
            Output only. Enrollment which contains
            enrolled destination details for a resource
        enrolled (bool):
            Output only. Is resource enrolled.
        display_name (str):
            Output only. Display name of the
            project/folder/organization.
        enrollment_state (google.cloud.auditmanager_v1.types.ResourceEnrollmentStatus.ResourceEnrollmentState):
            Output only. Enrollment state of the
            resource.
    """

    class ResourceEnrollmentState(proto.Enum):
        r"""The different enrollment states of a resource.

        Values:
            RESOURCE_ENROLLMENT_STATE_UNSPECIFIED (0):
                Unspecified. Invalid state.
            NOT_ENROLLED (1):
                Not enrolled.
            INHERITED (2):
                Resource is not enrolled but the parent is
                enrolled.
            ENROLLED (3):
                Enrolled.
        """
        RESOURCE_ENROLLMENT_STATE_UNSPECIFIED = 0
        NOT_ENROLLED = 1
        INHERITED = 2
        ENROLLED = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    enrollment: "Enrollment" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Enrollment",
    )
    enrolled: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=4,
    )
    enrollment_state: ResourceEnrollmentState = proto.Field(
        proto.ENUM,
        number=5,
        enum=ResourceEnrollmentState,
    )


class AuditReport(proto.Message):
    r"""An audit report.

    Attributes:
        name (str):
            Identifier. The name of this Audit Report, in
            the format of scope given in request.
        report_summary (google.cloud.auditmanager_v1.types.ReportSummary):
            Output only. Report summary with compliance,
            violation counts etc.
        operation_id (str):
            Output only. ClientOperationId
        destination_details (google.cloud.auditmanager_v1.types.DestinationDetails):
            Output only. The location where the generated
            report will be uploaded.
        compliance_standard (str):
            Output only. Compliance Standard.
        scope (str):
            Output only. The parent scope on which the
            report was generated.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of the audit
            report.
        control_details (MutableSequence[google.cloud.auditmanager_v1.types.ControlDetails]):
            Output only. The overall status of controls
        report_generation_state (google.cloud.auditmanager_v1.types.AuditReport.ReportGenerationState):
            Output only. The state of Audit Report
            Generation.
        compliance_framework (str):
            Output only. Compliance Framework of Audit
            Report
        scope_id (str):
            Output only. The ID/ Number for the scope on
            which the audit report was generated.
    """

    class ReportGenerationState(proto.Enum):
        r"""The different states of the Audit Manager report generation.

        Values:
            REPORT_GENERATION_STATE_UNSPECIFIED (0):
                Unspecified. Invalid state.
            IN_PROGRESS (1):
                Audit report generation process is in progress, ie.
                operation state is neither OPERATION_STATE_DONE nor
                OPERATION_STATE_FAILED.
            COMPLETED (2):
                Audit report generation process is completed. Operation
                state is OPERATION_STATE_DONE.
            FAILED (3):
                Audit report generation process has failed. Operation state
                is OPERATION_STATE_FAILED.
            SUMMARY_UNKNOWN (4):
                Audit report generation process has
                completed. But report summary is unknown. This
                is valid for older reports.
        """
        REPORT_GENERATION_STATE_UNSPECIFIED = 0
        IN_PROGRESS = 1
        COMPLETED = 2
        FAILED = 3
        SUMMARY_UNKNOWN = 4

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    report_summary: "ReportSummary" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ReportSummary",
    )
    operation_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    destination_details: "DestinationDetails" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="DestinationDetails",
    )
    compliance_standard: str = proto.Field(
        proto.STRING,
        number=5,
    )
    scope: str = proto.Field(
        proto.STRING,
        number=6,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    control_details: MutableSequence["ControlDetails"] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="ControlDetails",
    )
    report_generation_state: ReportGenerationState = proto.Field(
        proto.ENUM,
        number=9,
        enum=ReportGenerationState,
    )
    compliance_framework: str = proto.Field(
        proto.STRING,
        number=10,
    )
    scope_id: str = proto.Field(
        proto.STRING,
        number=11,
    )


class ControlFamily(proto.Message):
    r"""The regulatory family of the control.

    Attributes:
        family_id (str):
            The ID of the regulatory control family.
        display_name (str):
            The display name of the regulatory control
            family.
    """

    family_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Control(proto.Message):
    r"""A control.

    Attributes:
        id (str):
            Output only. The control identifier used to
            fetch the findings. This is same as the control
            report name.
        display_name (str):
            Output only. Display name of the control.
        family (google.cloud.auditmanager_v1.types.Control.Family):
            Output only. Group where the control belongs.
            E.g. Access Control.
        control_family (google.cloud.auditmanager_v1.types.ControlFamily):
            Output only. Regulatory Family of the control
            E.g. Access Control
        description (str):
            Output only. Regulatory control ask of the
            control
        responsibility_type (str):
            Output only. The type of responsibility for
            implementing this control. It can be google,
            customer or shared.
        google_responsibility_description (str):
            Output only. Description of the google
            responsibility for implementing this control.
        google_responsibility_implementation (str):
            Output only. Implementation of the google
            responsibility for implementing this control.
        customer_responsibility_description (str):
            Output only. Description of the customer
            responsibility for implementing this control.
        customer_responsibility_implementation (str):
            Output only. Implementation of the customer
            responsibility for implementing this control.
    """

    class Family(proto.Enum):
        r"""The family of the control. For example, Access Control.

        Values:
            FAMILY_UNSPECIFIED (0):
                Unspecified. Invalid state.
            AC (1):
                Access Control
            AT (2):
                Awareness and Training
            AU (3):
                Audit and Accountability
            CA (4):
                Certification, Accreditation and Security
                Assessments
            CM (5):
                Configuration Management
            CP (6):
                Contingency Planning
            IA (7):
                Identification and Authentication
            IR (8):
                Incident Response
            MA (9):
                Maintenance
            MP (10):
                Media Protection
            PE (11):
                Physical and Environmental Protection
            PL (12):
                Security Planning
            PS (13):
                Personnel Security
            RA (14):
                Risk Assessment
            SA (15):
                System Services and Acquisition
            SC (16):
                System and Communications Protection
            SI (17):
                System and Information Integrity
            SR (18):
                Supply Chain Risk Management
        """
        FAMILY_UNSPECIFIED = 0
        AC = 1
        AT = 2
        AU = 3
        CA = 4
        CM = 5
        CP = 6
        IA = 7
        IR = 8
        MA = 9
        MP = 10
        PE = 11
        PL = 12
        PS = 13
        RA = 14
        SA = 15
        SC = 16
        SI = 17
        SR = 18

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    family: Family = proto.Field(
        proto.ENUM,
        number=3,
        enum=Family,
    )
    control_family: "ControlFamily" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="ControlFamily",
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    responsibility_type: str = proto.Field(
        proto.STRING,
        number=5,
    )
    google_responsibility_description: str = proto.Field(
        proto.STRING,
        number=6,
    )
    google_responsibility_implementation: str = proto.Field(
        proto.STRING,
        number=7,
    )
    customer_responsibility_description: str = proto.Field(
        proto.STRING,
        number=8,
    )
    customer_responsibility_implementation: str = proto.Field(
        proto.STRING,
        number=9,
    )


class DestinationDetails(proto.Message):
    r"""The locations where the generated reports are saved.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_bucket_uri (str):
            The Cloud Storage bucket where the audit
            report is/will be uploaded.

            This field is a member of `oneof`_ ``destination``.
    """

    gcs_bucket_uri: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="destination",
    )


class ReportSummary(proto.Message):
    r"""The additional information for an audit operation.

    Attributes:
        total_count (int):
            Total number of checks.
        compliant_count (int):
            Number of compliant checks.
        violation_count (int):
            Number of checks with violations.
        manual_review_needed_count (int):
            Number of checks with "manual review needed"
            status.
        error_count (int):
            Number of checks that could not be performed
            due to errors.
    """

    total_count: int = proto.Field(
        proto.INT32,
        number=1,
    )
    compliant_count: int = proto.Field(
        proto.INT32,
        number=2,
    )
    violation_count: int = proto.Field(
        proto.INT32,
        number=3,
    )
    manual_review_needed_count: int = proto.Field(
        proto.INT32,
        number=4,
    )
    error_count: int = proto.Field(
        proto.INT32,
        number=5,
    )


class ControlDetails(proto.Message):
    r"""The evaluation details for a control.

    Attributes:
        control (google.cloud.auditmanager_v1.types.Control):
            The control for which the findings are being
            reported.
        compliance_state (google.cloud.auditmanager_v1.types.ComplianceState):
            Output only. Overall status of the findings
            for the control.
        control_report_summary (google.cloud.auditmanager_v1.types.ReportSummary):
            Report summary with compliance, violation
            counts etc.
    """

    control: "Control" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Control",
    )
    compliance_state: "ComplianceState" = proto.Field(
        proto.ENUM,
        number=2,
        enum="ComplianceState",
    )
    control_report_summary: "ReportSummary" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ReportSummary",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
