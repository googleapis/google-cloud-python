# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1",
    manifest={
        "ExternalSystem",
    },
)


class ExternalSystem(proto.Message):
    r"""Representation of third party SIEM/SOAR fields within SCC.

    Attributes:
        name (str):
            Full resource name of the external system,
            for example:

            "organizations/1234/sources/5678/findings/123456/externalSystems/jira",
            "folders/1234/sources/5678/findings/123456/externalSystems/jira",
            "projects/1234/sources/5678/findings/123456/externalSystems/jira".
        assignees (MutableSequence[str]):
            References primary/secondary etc assignees in
            the external system.
        external_uid (str):
            Identifier that's used to track the given
            finding in the external system.
        status (str):
            Most recent status of the corresponding
            finding's ticket/tracker in the external system.
        external_system_update_time (google.protobuf.timestamp_pb2.Timestamp):
            The most recent time when the corresponding
            finding's ticket/tracker was updated in the
            external system.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    assignees: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    external_uid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    status: str = proto.Field(
        proto.STRING,
        number=4,
    )
    external_system_update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
