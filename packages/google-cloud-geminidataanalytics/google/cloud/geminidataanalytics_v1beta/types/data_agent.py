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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.geminidataanalytics_v1beta.types import (
    data_analytics_agent as gcg_data_analytics_agent,
)

__protobuf__ = proto.module(
    package="google.cloud.geminidataanalytics.v1beta",
    manifest={
        "DataAgent",
    },
)


class DataAgent(proto.Message):
    r"""Message describing a DataAgent object.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        data_analytics_agent (google.cloud.geminidataanalytics_v1beta.types.DataAnalyticsAgent):
            Data analytics agent.

            This field is a member of `oneof`_ ``type``.
        name (str):
            Optional. Identifier. The unique resource name of a
            DataAgent. Format:
            ``projects/{project}/locations/{location}/dataAgents/{data_agent_id}``
            ``{data_agent}`` is the resource id and should be 63
            characters or less and must match the format described in
            https://google.aip.dev/122#resource-id-segments

            Example:
            ``projects/1234567890/locations/us-central1/dataAgents/my-agent``.

            It is recommended to skip setting this field during agent
            creation as it will be inferred automatically and
            overwritten with the {parent}/dataAgents/{data_agent_id}.
        display_name (str):
            Optional. User friendly display name.

            - Must be between 1-256 characters.
        description (str):
            Optional. Description of the agent.

            - Must be between 1-1024 characters.
        labels (MutableMapping[str, str]):
            Optional. Labels to help users filter related agents. For
            example, "sales", "business", "etl", and so on. Note labels
            are used only for filtering and not for policies. See the
            `labels
            documentation <https://cloud.google.com/resource-manager/docs/labels-overview>`__
            for more details on label usage.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the data agent was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the data agent was
            last updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] The time the data agent was soft
            deleted.
        purge_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp in UTC of when this data agent is
            considered expired. This is *always* provided on output,
            regardless of what was sent on input.
    """

    data_analytics_agent: gcg_data_analytics_agent.DataAnalyticsAgent = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="type",
        message=gcg_data_analytics_agent.DataAnalyticsAgent,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=12,
        message=timestamp_pb2.Timestamp,
    )
    purge_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=13,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
