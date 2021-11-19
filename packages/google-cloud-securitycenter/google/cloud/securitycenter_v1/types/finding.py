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

from google.cloud.securitycenter_v1.types import external_system
from google.cloud.securitycenter_v1.types import indicator as gcs_indicator
from google.cloud.securitycenter_v1.types import security_marks as gcs_security_marks
from google.cloud.securitycenter_v1.types import vulnerability as gcs_vulnerability
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1", manifest={"Finding",},
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
        source_properties (Sequence[google.cloud.securitycenter_v1.types.Finding.SourcePropertiesEntry]):
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
            The time at which the event took place, or
            when an update to the finding occurred. For
            example, if the finding represents an open
            firewall it would capture the time the detector
            believes the firewall became open. The accuracy
            is determined by the detector. If the finding
            were to be resolved afterward, this time would
            reflect when the finding was resolved. Must not
            be set to a value greater than the current
            timestamp.
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
            unspecified, muted, unmuted or undefined).
        finding_class (google.cloud.securitycenter_v1.types.Finding.FindingClass):
            The class of the finding.
        indicator (google.cloud.securitycenter_v1.types.Indicator):
            Represents what's commonly known as an Indicator of
            compromise (IoC) in computer forensics. This is an artifact
            observed on a network or in an operating system that, with
            high confidence, indicates a computer intrusion. Reference:
            https://en.wikipedia.org/wiki/Indicator_of_compromise
        vulnerability (google.cloud.securitycenter_v1.types.Vulnerability):
            Represents vulnerability specific fields like
            cve, cvss scores etc. CVE stands for Common
            Vulnerabilities and Exposures
            (https://cve.mitre.org/about/)
        mute_update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The most recent time this
            finding was muted or unmuted.
        external_systems (Sequence[google.cloud.securitycenter_v1.types.Finding.ExternalSystemsEntry]):
            Output only. Third party SIEM/SOAR fields
            within SCC, contains external system information
            and external system finding fields.
        mute_initiator (str):
            First known as mute_annotation. Records additional
            information about the mute operation e.g. mute config that
            muted the finding, user who muted the finding, etc.
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

    name = proto.Field(proto.STRING, number=1,)
    parent = proto.Field(proto.STRING, number=2,)
    resource_name = proto.Field(proto.STRING, number=3,)
    state = proto.Field(proto.ENUM, number=4, enum=State,)
    category = proto.Field(proto.STRING, number=5,)
    external_uri = proto.Field(proto.STRING, number=6,)
    source_properties = proto.MapField(
        proto.STRING, proto.MESSAGE, number=7, message=struct_pb2.Value,
    )
    security_marks = proto.Field(
        proto.MESSAGE, number=8, message=gcs_security_marks.SecurityMarks,
    )
    event_time = proto.Field(proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,)
    create_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp_pb2.Timestamp,
    )
    severity = proto.Field(proto.ENUM, number=12, enum=Severity,)
    canonical_name = proto.Field(proto.STRING, number=14,)
    mute = proto.Field(proto.ENUM, number=15, enum=Mute,)
    finding_class = proto.Field(proto.ENUM, number=17, enum=FindingClass,)
    indicator = proto.Field(proto.MESSAGE, number=18, message=gcs_indicator.Indicator,)
    vulnerability = proto.Field(
        proto.MESSAGE, number=20, message=gcs_vulnerability.Vulnerability,
    )
    mute_update_time = proto.Field(
        proto.MESSAGE, number=21, message=timestamp_pb2.Timestamp,
    )
    external_systems = proto.MapField(
        proto.STRING, proto.MESSAGE, number=22, message=external_system.ExternalSystem,
    )
    mute_initiator = proto.Field(proto.STRING, number=28,)


__all__ = tuple(sorted(__protobuf__.manifest))
