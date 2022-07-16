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
        "Exfiltration",
        "ExfilResource",
    },
)


class Exfiltration(proto.Message):
    r"""Exfiltration represents a data exfiltration attempt of one or
    more sources to one or more targets.  Sources represent the
    source of data that is exfiltrated, and Targets represents the
    destination the data was copied to.

    Attributes:
        sources (Sequence[google.cloud.securitycenter_v1.types.ExfilResource]):
            If there are multiple sources, then the data
            is considered "joined" between them. For
            instance, BigQuery can join multiple tables, and
            each table would be considered a source.
        targets (Sequence[google.cloud.securitycenter_v1.types.ExfilResource]):
            If there are multiple targets, each target
            would get a complete copy of the "joined" source
            data.
    """

    sources = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ExfilResource",
    )
    targets = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="ExfilResource",
    )


class ExfilResource(proto.Message):
    r"""Resource that has been exfiltrated or exfiltrated_to.

    Attributes:
        name (str):
            Resource's URI
            (https://google.aip.dev/122#full-resource-names)
        components (Sequence[str]):
            Subcomponents of the asset that is
            exfiltrated - these could be URIs used during
            exfiltration, table names, databases, filenames,
            etc. For example, multiple tables may be
            exfiltrated from the same CloudSQL instance, or
            multiple files from the same Cloud Storage
            bucket.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    components = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
