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
from google.rpc import status_pb2  # type: ignore
from grafeas.grafeas_v1.types import common


__protobuf__ = proto.module(
    package="grafeas.v1", manifest={"DiscoveryNote", "DiscoveryOccurrence",},
)


class DiscoveryNote(proto.Message):
    r"""A note that indicates a type of analysis a provider would perform.
    This note exists in a provider's project. A ``Discovery`` occurrence
    is created in a consumer's project at the start of analysis.

    Attributes:
        analysis_kind (grafeas.grafeas_v1.types.NoteKind):
            Required. Immutable. The kind of analysis
            that is handled by this discovery.
    """

    analysis_kind = proto.Field(proto.ENUM, number=1, enum=common.NoteKind,)


class DiscoveryOccurrence(proto.Message):
    r"""Provides information about the analysis status of a
    discovered resource.

    Attributes:
        continuous_analysis (grafeas.grafeas_v1.types.DiscoveryOccurrence.ContinuousAnalysis):
            Whether the resource is continuously
            analyzed.
        analysis_status (grafeas.grafeas_v1.types.DiscoveryOccurrence.AnalysisStatus):
            The status of discovery for the resource.
        analysis_status_error (google.rpc.status_pb2.Status):
            When an error is encountered this will
            contain a LocalizedMessage under details to show
            to the user. The LocalizedMessage is output only
            and populated by the API.
        cpe (str):
            The CPE of the resource being scanned.
        last_scan_time (google.protobuf.timestamp_pb2.Timestamp):
            The last time this resource was scanned.
        archive_time (google.protobuf.timestamp_pb2.Timestamp):
            The time occurrences related to this
            discovery occurrence were archived.
    """

    class ContinuousAnalysis(proto.Enum):
        r"""Whether the resource is continuously analyzed."""
        CONTINUOUS_ANALYSIS_UNSPECIFIED = 0
        ACTIVE = 1
        INACTIVE = 2

    class AnalysisStatus(proto.Enum):
        r"""Analysis status for a resource. Currently for initial
        analysis only (not updated in continuous analysis).
        """
        ANALYSIS_STATUS_UNSPECIFIED = 0
        PENDING = 1
        SCANNING = 2
        FINISHED_SUCCESS = 3
        FINISHED_FAILED = 4
        FINISHED_UNSUPPORTED = 5

    continuous_analysis = proto.Field(proto.ENUM, number=1, enum=ContinuousAnalysis,)
    analysis_status = proto.Field(proto.ENUM, number=2, enum=AnalysisStatus,)
    analysis_status_error = proto.Field(
        proto.MESSAGE, number=3, message=status_pb2.Status,
    )
    cpe = proto.Field(proto.STRING, number=4,)
    last_scan_time = proto.Field(
        proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,
    )
    archive_time = proto.Field(
        proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
