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

__protobuf__ = proto.module(
    package="google.cloud.networkmanagement.v1",
    manifest={
        "VpcFlowLogsConfig",
    },
)


class VpcFlowLogsConfig(proto.Message):
    r"""A configuration to generate VPC Flow Logs.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Identifier. Unique name of the configuration using the form:
            ``projects/{project_id}/locations/global/vpcFlowLogsConfigs/{vpc_flow_logs_config_id}``
        description (str):
            Optional. The user-supplied description of
            the VPC Flow Logs configuration. Maximum of 512
            characters.

            This field is a member of `oneof`_ ``_description``.
        state (google.cloud.network_management_v1.types.VpcFlowLogsConfig.State):
            Optional. The state of the VPC Flow Log
            configuration. Default value is ENABLED. When
            creating a new configuration, it must be
            enabled.

            This field is a member of `oneof`_ ``_state``.
        aggregation_interval (google.cloud.network_management_v1.types.VpcFlowLogsConfig.AggregationInterval):
            Optional. The aggregation interval for the logs. Default
            value is INTERVAL_5_SEC.

            This field is a member of `oneof`_ ``_aggregation_interval``.
        flow_sampling (float):
            Optional. The value of the field must be in (0, 1]. The
            sampling rate of VPC Flow Logs where 1.0 means all collected
            logs are reported. Setting the sampling rate to 0.0 is not
            allowed. If you want to disable VPC Flow Logs, use the state
            field instead. Default value is 1.0.

            This field is a member of `oneof`_ ``_flow_sampling``.
        metadata (google.cloud.network_management_v1.types.VpcFlowLogsConfig.Metadata):
            Optional. Configures whether all, none or a subset of
            metadata fields should be added to the reported VPC flow
            logs. Default value is INCLUDE_ALL_METADATA.

            This field is a member of `oneof`_ ``_metadata``.
        metadata_fields (MutableSequence[str]):
            Optional. Custom metadata fields to include in the reported
            VPC flow logs. Can only be specified if "metadata" was set
            to CUSTOM_METADATA.
        filter_expr (str):
            Optional. Export filter used to define which
            VPC Flow Logs should be logged.

            This field is a member of `oneof`_ ``_filter_expr``.
        target_resource_state (google.cloud.network_management_v1.types.VpcFlowLogsConfig.TargetResourceState):
            Output only. A diagnostic bit - describes the
            state of the configured target resource for
            diagnostic purposes.

            This field is a member of `oneof`_ ``_target_resource_state``.
        interconnect_attachment (str):
            Traffic will be logged from the Interconnect Attachment.
            Format:
            projects/{project_id}/regions/{region}/interconnectAttachments/{name}

            This field is a member of `oneof`_ ``target_resource``.
        vpn_tunnel (str):
            Traffic will be logged from the VPN Tunnel. Format:
            projects/{project_id}/regions/{region}/vpnTunnels/{name}

            This field is a member of `oneof`_ ``target_resource``.
        labels (MutableMapping[str, str]):
            Optional. Resource labels to represent
            user-provided metadata.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the config was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the config was updated.
    """

    class State(proto.Enum):
        r"""Determines whether this configuration will be generating
        logs. Setting state=DISABLED will pause the log generation for
        this config.

        Values:
            STATE_UNSPECIFIED (0):
                If not specified, will default to ENABLED.
            ENABLED (1):
                When ENABLED, this configuration will
                generate logs.
            DISABLED (2):
                When DISABLED, this configuration will not
                generate logs.
        """
        STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2

    class AggregationInterval(proto.Enum):
        r"""Toggles the aggregation interval for collecting flow logs by
        5-tuple.

        Values:
            AGGREGATION_INTERVAL_UNSPECIFIED (0):
                If not specified, will default to INTERVAL_5_SEC.
            INTERVAL_5_SEC (1):
                Aggregate logs in 5s intervals.
            INTERVAL_30_SEC (2):
                Aggregate logs in 30s intervals.
            INTERVAL_1_MIN (3):
                Aggregate logs in 1m intervals.
            INTERVAL_5_MIN (4):
                Aggregate logs in 5m intervals.
            INTERVAL_10_MIN (5):
                Aggregate logs in 10m intervals.
            INTERVAL_15_MIN (6):
                Aggregate logs in 15m intervals.
        """
        AGGREGATION_INTERVAL_UNSPECIFIED = 0
        INTERVAL_5_SEC = 1
        INTERVAL_30_SEC = 2
        INTERVAL_1_MIN = 3
        INTERVAL_5_MIN = 4
        INTERVAL_10_MIN = 5
        INTERVAL_15_MIN = 6

    class Metadata(proto.Enum):
        r"""Configures which log fields would be included.

        Values:
            METADATA_UNSPECIFIED (0):
                If not specified, will default to INCLUDE_ALL_METADATA.
            INCLUDE_ALL_METADATA (1):
                Include all metadata fields.
            EXCLUDE_ALL_METADATA (2):
                Exclude all metadata fields.
            CUSTOM_METADATA (3):
                Include only custom fields (specified in metadata_fields).
        """
        METADATA_UNSPECIFIED = 0
        INCLUDE_ALL_METADATA = 1
        EXCLUDE_ALL_METADATA = 2
        CUSTOM_METADATA = 3

    class TargetResourceState(proto.Enum):
        r"""Optional states of the target resource that are used as part
        of the diagnostic bit.

        Values:
            TARGET_RESOURCE_STATE_UNSPECIFIED (0):
                Unspecified target resource state.
            TARGET_RESOURCE_EXISTS (1):
                Indicates that the target resource exists.
            TARGET_RESOURCE_DOES_NOT_EXIST (2):
                Indicates that the target resource does not
                exist.
        """
        TARGET_RESOURCE_STATE_UNSPECIFIED = 0
        TARGET_RESOURCE_EXISTS = 1
        TARGET_RESOURCE_DOES_NOT_EXIST = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=3,
        optional=True,
        enum=State,
    )
    aggregation_interval: AggregationInterval = proto.Field(
        proto.ENUM,
        number=4,
        optional=True,
        enum=AggregationInterval,
    )
    flow_sampling: float = proto.Field(
        proto.FLOAT,
        number=5,
        optional=True,
    )
    metadata: Metadata = proto.Field(
        proto.ENUM,
        number=6,
        optional=True,
        enum=Metadata,
    )
    metadata_fields: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    filter_expr: str = proto.Field(
        proto.STRING,
        number=8,
        optional=True,
    )
    target_resource_state: TargetResourceState = proto.Field(
        proto.ENUM,
        number=12,
        optional=True,
        enum=TargetResourceState,
    )
    interconnect_attachment: str = proto.Field(
        proto.STRING,
        number=102,
        oneof="target_resource",
    )
    vpn_tunnel: str = proto.Field(
        proto.STRING,
        number=103,
        oneof="target_resource",
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=11,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
