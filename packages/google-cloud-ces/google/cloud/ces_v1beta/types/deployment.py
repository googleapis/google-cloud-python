# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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

from google.cloud.ces_v1beta.types import common

__protobuf__ = proto.module(
    package="google.cloud.ces.v1beta",
    manifest={
        "ExperimentConfig",
        "Deployment",
    },
)


class ExperimentConfig(proto.Message):
    r"""Experiment for the deployment.

    Attributes:
        version_release (google.cloud.ces_v1beta.types.ExperimentConfig.VersionRelease):
            Optional. Version release for the experiment.
    """

    class State(proto.Enum):
        r"""State of the experiment.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified state.
            PENDING (1):
                Pending state. Experiment is pending and not
                valid.
            RUNNING (2):
                Running state. Experiment is running and
                valid.
            DONE (3):
                Done state. Experiment is done and no longer
                valid.
            EXPIRED (4):
                Expired state. Experiment is expired and no
                longer valid.
        """

        STATE_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3
        EXPIRED = 4

    class VersionRelease(proto.Message):
        r"""Version release for the experiment.

        Attributes:
            state (google.cloud.ces_v1beta.types.ExperimentConfig.State):
                Optional. State of the version release.
            traffic_allocations (MutableSequence[google.cloud.ces_v1beta.types.ExperimentConfig.VersionRelease.TrafficAllocation]):
                Optional. Traffic allocations for the version
                release.
        """

        class TrafficAllocation(proto.Message):
            r"""Traffic allocation for the version release.

            Attributes:
                id (str):
                    Optional. Id of the traffic allocation.
                    Free format string, up to 128 characters.
                traffic_percentage (int):
                    Optional. Traffic percentage of the traffic
                    allocation. Must be between 0 and 100.
                app_version (str):
                    Optional. App version of the traffic allocation. Format:
                    ``projects/{project}/locations/{location}/apps/{app}/versions/{version}``
            """

            id: str = proto.Field(
                proto.STRING,
                number=1,
            )
            traffic_percentage: int = proto.Field(
                proto.INT32,
                number=2,
            )
            app_version: str = proto.Field(
                proto.STRING,
                number=3,
            )

        state: "ExperimentConfig.State" = proto.Field(
            proto.ENUM,
            number=1,
            enum="ExperimentConfig.State",
        )
        traffic_allocations: MutableSequence[
            "ExperimentConfig.VersionRelease.TrafficAllocation"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="ExperimentConfig.VersionRelease.TrafficAllocation",
        )

    version_release: VersionRelease = proto.Field(
        proto.MESSAGE,
        number=1,
        message=VersionRelease,
    )


class Deployment(proto.Message):
    r"""A deployment represents an immutable, queryable version of
    the app. It is used to deploy an app version with a specific
    channel profile.

    Attributes:
        name (str):
            Identifier. The resource name of the deployment. Format:
            ``projects/{project}/locations/{location}/apps/{app}/deployments/{deployment}``
        display_name (str):
            Required. Display name of the deployment.
        app_version (str):
            Optional. The resource name of the app version to deploy.
            Format:
            ``projects/{project}/locations/{location}/apps/{app}/versions/{version}``
            Use
            ``projects/{project}/locations/{location}/apps/{app}/versions/-``
            to use the draft app.
        channel_profile (google.cloud.ces_v1beta.types.ChannelProfile):
            Required. The channel profile used in the
            deployment.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this deployment
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this deployment
            was last updated.
        etag (str):
            Output only. Etag used to ensure the object
            hasn't changed during a read-modify-write
            operation. If the etag is empty, the update will
            overwrite any concurrent changes.
        experiment_config (google.cloud.ces_v1beta.types.ExperimentConfig):
            Optional. Experiment configuration for the
            deployment.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    app_version: str = proto.Field(
        proto.STRING,
        number=2,
    )
    channel_profile: common.ChannelProfile = proto.Field(
        proto.MESSAGE,
        number=3,
        message=common.ChannelProfile,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=7,
    )
    experiment_config: "ExperimentConfig" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="ExperimentConfig",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
