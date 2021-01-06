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


from grafeas.grafeas_v1.types import vulnerability  # type: ignore


__protobuf__ = proto.module(
    package="google.devtools.containeranalysis.v1",
    manifest={
        "GetVulnerabilityOccurrencesSummaryRequest",
        "VulnerabilityOccurrencesSummary",
    },
)


class GetVulnerabilityOccurrencesSummaryRequest(proto.Message):
    r"""Request to get a vulnerability summary for some set of
    occurrences.

    Attributes:
        parent (str):
            The name of the project to get a vulnerability summary for
            in the form of ``projects/[PROJECT_ID]``.
        filter (str):
            The filter expression.
    """

    parent = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=2)


class VulnerabilityOccurrencesSummary(proto.Message):
    r"""A summary of how many vulnerability occurrences there are per
    resource and severity type.

    Attributes:
        counts (Sequence[google.cloud.devtools.containeranalysis_v1.types.VulnerabilityOccurrencesSummary.FixableTotalByDigest]):
            A listing by resource of the number of
            fixable and total vulnerabilities.
    """

    class FixableTotalByDigest(proto.Message):
        r"""Per resource and severity counts of fixable and total
        vulnerabilities.

        Attributes:
            resource_uri (str):
                The affected resource.
            severity (grafeas.v1.vulnerability_pb2.Severity):
                The severity for this count. SEVERITY_UNSPECIFIED indicates
                total across all severities.
            fixable_count (int):
                The number of fixable vulnerabilities
                associated with this resource.
            total_count (int):
                The total number of vulnerabilities
                associated with this resource.
        """

        resource_uri = proto.Field(proto.STRING, number=1)

        severity = proto.Field(proto.ENUM, number=2, enum=vulnerability.Severity,)

        fixable_count = proto.Field(proto.INT64, number=3)

        total_count = proto.Field(proto.INT64, number=4)

    counts = proto.RepeatedField(proto.MESSAGE, number=1, message=FixableTotalByDigest,)


__all__ = tuple(sorted(__protobuf__.manifest))
