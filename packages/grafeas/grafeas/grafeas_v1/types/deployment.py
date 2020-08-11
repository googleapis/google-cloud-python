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


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="grafeas.v1", manifest={"DeploymentNote", "DeploymentOccurrence",},
)


class DeploymentNote(proto.Message):
    r"""An artifact that can be deployed in some runtime.

    Attributes:
        resource_uri (Sequence[str]):
            Required. Resource URI for the artifact being
            deployed.
    """

    resource_uri = proto.RepeatedField(proto.STRING, number=1)


class DeploymentOccurrence(proto.Message):
    r"""The period during which some deployable was active in a
    runtime.

    Attributes:
        user_email (str):
            Identity of the user that triggered this
            deployment.
        deploy_time (~.timestamp.Timestamp):
            Required. Beginning of the lifetime of this
            deployment.
        undeploy_time (~.timestamp.Timestamp):
            End of the lifetime of this deployment.
        config (str):
            Configuration used to create this deployment.
        address (str):
            Address of the runtime element hosting this
            deployment.
        resource_uri (Sequence[str]):
            Output only. Resource URI for the artifact
            being deployed taken from the deployable field
            with the same name.
        platform (~.deployment.DeploymentOccurrence.Platform):
            Platform hosting this deployment.
    """

    class Platform(proto.Enum):
        r"""Types of platforms."""
        PLATFORM_UNSPECIFIED = 0
        GKE = 1
        FLEX = 2
        CUSTOM = 3

    user_email = proto.Field(proto.STRING, number=1)

    deploy_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    undeploy_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    config = proto.Field(proto.STRING, number=4)

    address = proto.Field(proto.STRING, number=5)

    resource_uri = proto.RepeatedField(proto.STRING, number=6)

    platform = proto.Field(proto.ENUM, number=7, enum=Platform,)


__all__ = tuple(sorted(__protobuf__.manifest))
