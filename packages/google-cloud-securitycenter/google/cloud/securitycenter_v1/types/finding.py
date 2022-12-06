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

from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.securitycenter_v1.types import (
    compliance,
    connection,
    contact_details,
    container,
)
from google.cloud.securitycenter_v1.types import external_system, file, iam_binding
from google.cloud.securitycenter_v1.types import exfiltration as gcs_exfiltration
from google.cloud.securitycenter_v1.types import kernel_rootkit as gcs_kernel_rootkit
from google.cloud.securitycenter_v1.types import mitre_attack as gcs_mitre_attack
from google.cloud.securitycenter_v1.types import security_marks as gcs_security_marks
from google.cloud.securitycenter_v1.types import vulnerability as gcs_vulnerability
from google.cloud.securitycenter_v1.types import access as gcs_access
from google.cloud.securitycenter_v1.types import database as gcs_database
from google.cloud.securitycenter_v1.types import indicator as gcs_indicator
from google.cloud.securitycenter_v1.types import kubernetes as gcs_kubernetes
from google.cloud.securitycenter_v1.types import process

__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1",
    manifest={
        "Finding",
    },
)


class Finding(proto.Message):
    r"""Security Command Center finding.
    A finding is a record of assessment data like security, risk,
    health, or privacy, that is ingested into Security Command
    Center for presentation, notification, analysis, policy testing,
    and enforcement. For example, a cross-site scripting (XSS)
    vulnerability in an App Engine application is a finding.

    Attributes:
        name (str):
            The relative resource name of this finding. See:
            https://cloud.google.com/apis/design/resource_names#relative_resource_name
            Example:
            "organizations/{organization_id}/sources/{source_id}/findings/{finding_id}".
        parent (str):
            The relative resource name of the source the finding belongs
            to. See:
            https://cloud.google.com/apis/design/resource_names#relative_resource_name
            This field is immutable after creation time. For example:
            "organizations/{organization_id}/sources/{source_id}".
        resource_name (str):
            For findings on Google Cloud resources, the full resource
            name of the Google Cloud resource this finding is for. See:
            https://cloud.google.com/apis/design/resource_names#full_resource_name
            When the finding is for a non-Google Cloud resource, the
            resourceName can be a customer or partner defined string.
            This field is immutable after creation time.
        state (google.cloud.securitycenter_v1.types.Finding.State):
            The state of the finding.
        category (str):
            The additional taxonomy group within findings from a given
            source. This field is immutable after creation time.
            Example: "XSS_FLASH_INJECTION".
        external_uri (str):
            The URI that, if available, points to a web
            page outside of Security Command Center where
            additional information about the finding can be
            found. This field is guaranteed to be either
            empty or a well formed URL.
        source_properties (MutableMapping[str, google.protobuf.struct_pb2.Value]):
            Source specific properties. These properties are managed by
            the source that writes the finding. The key names in the
            source_properties map must be between 1 and 255 characters,
            and must start with a letter and contain alphanumeric
            characters or underscores only.
        security_marks (google.cloud.securitycenter_v1.types.SecurityMarks):
            Output only. User specified security marks.
            These marks are entirely managed by the user and
            come from the SecurityMarks resource that
            belongs to the finding.
        event_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the finding was first detected. If
            an existing finding is updated, then this is the
            time the update occurred. For example, if the
            finding represents an open firewall, this
            property captures the time the detector believes
            the firewall became open. The accuracy is
            determined by the detector. If the finding is
            later resolved, then this time reflects when the
            finding was resolved. This must not be set to a
            value greater than the current timestamp.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the finding was created in
            Security Command Center.
        severity (google.cloud.securitycenter_v1.types.Finding.Severity):
            The severity of the finding. This field is
            managed by the source that writes the finding.
        canonical_name (str):
            The canonical name of the finding. It's either
            "organizations/{organization_id}/sources/{source_id}/findings/{finding_id}",
            "folders/{folder_id}/sources/{source_id}/findings/{finding_id}"
            or
            "projects/{project_number}/sources/{source_id}/findings/{finding_id}",
            depending on the closest CRM ancestor of the resource
            associated with the finding.
        mute (google.cloud.securitycenter_v1.types.Finding.Mute):
            Indicates the mute state of a finding (either
            muted, unmuted or undefined). Unlike other
            attributes of a finding, a finding provider
            shouldn't set the value of mute.
        finding_class (google.cloud.securitycenter_v1.types.Finding.FindingClass):
            The class of the finding.
        indicator (google.cloud.securitycenter_v1.types.Indicator):
            Represents what's commonly known as an Indicator of
            compromise (IoC) in computer forensics. This is an artifact
            observed on a network or in an operating system that, with
            high confidence, indicates a computer intrusion. Reference:
            https://en.wikipedia.org/wiki/Indicator_of_compromise
        vulnerability (google.cloud.securitycenter_v1.types.Vulnerability):
            Represents vulnerability-specific fields like
            CVE and CVS scores. CVE stands for Common
            Vulnerabilities and Exposures
            (https://cve.mitre.org/about/)
        mute_update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The most recent time this
            finding was muted or unmuted.
        external_systems (MutableMapping[str, google.cloud.securitycenter_v1.types.ExternalSystem]):
            Output only. Third party SIEM/SOAR fields
            within SCC, contains external system information
            and external system finding fields.
        mitre_attack (google.cloud.securitycenter_v1.types.MitreAttack):
            MITRE ATT&CK tactics and techniques related
            to this finding. See: https://attack.mitre.org
        access (google.cloud.securitycenter_v1.types.Access):
            Access details associated to the Finding,
            such as more information on the caller, which
            method was accessed, from where, etc.
        connections (MutableSequence[google.cloud.securitycenter_v1.types.Connection]):
            Contains information about the IP connection
            associated with the finding.
        mute_initiator (str):
            First known as mute_annotation. Records additional
            information about the mute operation e.g. mute config that
            muted the finding, user who muted the finding, etc. Unlike
            other attributes of a finding, a finding provider shouldn't
            set the value of mute.
        processes (MutableSequence[google.cloud.securitycenter_v1.types.Process]):
            Represents operating system processes
            associated with the Finding.
        contacts (MutableMapping[str, google.cloud.securitycenter_v1.types.ContactDetails]):
            Output only. Map containing the points of contact for the
            given finding. The key represents the type of contact, while
            the value contains a list of all the contacts that pertain.
            Please refer to:
            https://cloud.google.com/resource-manager/docs/managing-notification-contacts#notification-categories

            ::

                {
                  "security": {
                    "contacts": [
                      {
                        "email": "person1@company.com"
                      },
                      {
                        "email": "person2@company.com"
                      }
                    ]
                  }
                }
        compliances (MutableSequence[google.cloud.securitycenter_v1.types.Compliance]):
            Contains compliance information for security
            standards associated to the finding.
        parent_display_name (str):
            Output only. The human readable display name
            of the finding source such as "Event Threat
            Detection" or "Security Health Analytics".
        description (str):
            Contains more detail about the finding.
        exfiltration (google.cloud.securitycenter_v1.types.Exfiltration):
            Represents exfiltration associated with the
            Finding.
        iam_bindings (MutableSequence[google.cloud.securitycenter_v1.types.IamBinding]):
            Represents IAM bindings associated with the
            Finding.
        next_steps (str):
            Next steps associate to the finding.
        containers (MutableSequence[google.cloud.securitycenter_v1.types.Container]):
            Containers associated with the finding.
            containers provides information for both
            Kubernetes and non-Kubernetes containers.
        kubernetes (google.cloud.securitycenter_v1.types.Kubernetes):
            Kubernetes resources associated with the
            finding.
        database (google.cloud.securitycenter_v1.types.Database):
            Database associated with the finding.
        files (MutableSequence[google.cloud.securitycenter_v1.types.File]):
            File associated with the finding.
        kernel_rootkit (google.cloud.securitycenter_v1.types.KernelRootkit):
            Kernel Rootkit signature.
    """

    class State(proto.Enum):
        r"""The state of the finding."""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        INACTIVE = 2

    class Severity(proto.Enum):
        r"""The severity of the finding."""
        SEVERITY_UNSPECIFIED = 0
        CRITICAL = 1
        HIGH = 2
        MEDIUM = 3
        LOW = 4

    class Mute(proto.Enum):
        r"""Mute state a finding can be in."""
        MUTE_UNSPECIFIED = 0
        MUTED = 1
        UNMUTED = 2
        UNDEFINED = 4

    class FindingClass(proto.Enum):
        r"""Represents what kind of Finding it is."""
        FINDING_CLASS_UNSPECIFIED = 0
        THREAT = 1
        VULNERABILITY = 2
        MISCONFIGURATION = 3
        OBSERVATION = 4
        SCC_ERROR = 5

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    parent: str = proto.Field(
        proto.STRING,
        number=2,
    )
    resource_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    category: str = proto.Field(
        proto.STRING,
        number=5,
    )
    external_uri: str = proto.Field(
        proto.STRING,
        number=6,
    )
    source_properties: MutableMapping[str, struct_pb2.Value] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=7,
        message=struct_pb2.Value,
    )
    security_marks: gcs_security_marks.SecurityMarks = proto.Field(
        proto.MESSAGE,
        number=8,
        message=gcs_security_marks.SecurityMarks,
    )
    event_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    severity: Severity = proto.Field(
        proto.ENUM,
        number=12,
        enum=Severity,
    )
    canonical_name: str = proto.Field(
        proto.STRING,
        number=14,
    )
    mute: Mute = proto.Field(
        proto.ENUM,
        number=15,
        enum=Mute,
    )
    finding_class: FindingClass = proto.Field(
        proto.ENUM,
        number=17,
        enum=FindingClass,
    )
    indicator: gcs_indicator.Indicator = proto.Field(
        proto.MESSAGE,
        number=18,
        message=gcs_indicator.Indicator,
    )
    vulnerability: gcs_vulnerability.Vulnerability = proto.Field(
        proto.MESSAGE,
        number=20,
        message=gcs_vulnerability.Vulnerability,
    )
    mute_update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=21,
        message=timestamp_pb2.Timestamp,
    )
    external_systems: MutableMapping[
        str, external_system.ExternalSystem
    ] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=22,
        message=external_system.ExternalSystem,
    )
    mitre_attack: gcs_mitre_attack.MitreAttack = proto.Field(
        proto.MESSAGE,
        number=25,
        message=gcs_mitre_attack.MitreAttack,
    )
    access: gcs_access.Access = proto.Field(
        proto.MESSAGE,
        number=26,
        message=gcs_access.Access,
    )
    connections: MutableSequence[connection.Connection] = proto.RepeatedField(
        proto.MESSAGE,
        number=31,
        message=connection.Connection,
    )
    mute_initiator: str = proto.Field(
        proto.STRING,
        number=28,
    )
    processes: MutableSequence[process.Process] = proto.RepeatedField(
        proto.MESSAGE,
        number=30,
        message=process.Process,
    )
    contacts: MutableMapping[str, contact_details.ContactDetails] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=33,
        message=contact_details.ContactDetails,
    )
    compliances: MutableSequence[compliance.Compliance] = proto.RepeatedField(
        proto.MESSAGE,
        number=34,
        message=compliance.Compliance,
    )
    parent_display_name: str = proto.Field(
        proto.STRING,
        number=36,
    )
    description: str = proto.Field(
        proto.STRING,
        number=37,
    )
    exfiltration: gcs_exfiltration.Exfiltration = proto.Field(
        proto.MESSAGE,
        number=38,
        message=gcs_exfiltration.Exfiltration,
    )
    iam_bindings: MutableSequence[iam_binding.IamBinding] = proto.RepeatedField(
        proto.MESSAGE,
        number=39,
        message=iam_binding.IamBinding,
    )
    next_steps: str = proto.Field(
        proto.STRING,
        number=40,
    )
    containers: MutableSequence[container.Container] = proto.RepeatedField(
        proto.MESSAGE,
        number=42,
        message=container.Container,
    )
    kubernetes: gcs_kubernetes.Kubernetes = proto.Field(
        proto.MESSAGE,
        number=43,
        message=gcs_kubernetes.Kubernetes,
    )
    database: gcs_database.Database = proto.Field(
        proto.MESSAGE,
        number=44,
        message=gcs_database.Database,
    )
    files: MutableSequence[file.File] = proto.RepeatedField(
        proto.MESSAGE,
        number=46,
        message=file.File,
    )
    kernel_rootkit: gcs_kernel_rootkit.KernelRootkit = proto.Field(
        proto.MESSAGE,
        number=50,
        message=gcs_kernel_rootkit.KernelRootkit,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
