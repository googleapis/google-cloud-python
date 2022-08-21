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


__protobuf__ = proto.module(
    package="google.cloud.apigeeregistry.v1",
    manifest={
        "CreateInstanceRequest",
        "DeleteInstanceRequest",
        "GetInstanceRequest",
        "OperationMetadata",
        "Instance",
    },
)


class CreateInstanceRequest(proto.Message):
    r"""Request message for CreateInstance.

    Attributes:
        parent (str):
            Required. Parent resource of the Instance, of the form:
            ``projects/*/locations/*``
        instance_id (str):
            Required. Identifier to assign to the
            Instance. Must be unique within scope of the
            parent resource.
        instance (google.cloud.apigee_registry_v1.types.Instance):
            Required. The Instance.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    instance_id = proto.Field(
        proto.STRING,
        number=2,
    )
    instance = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Instance",
    )


class DeleteInstanceRequest(proto.Message):
    r"""Request message for DeleteInstance.

    Attributes:
        name (str):
            Required. The name of the Instance to delete. Format:
            ``projects/*/locations/*/instances/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class GetInstanceRequest(proto.Message):
    r"""Request message for GetInstance.

    Attributes:
        name (str):
            Required. The name of the Instance to retrieve. Format:
            ``projects/*/locations/*/instances/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation finished running.
        target (str):
            Server-defined resource path for the target
            of the operation.
        verb (str):
            Name of the verb executed by the operation.
        status_message (str):
            Human-readable status of the operation, if
            any.
        cancellation_requested (bool):
            Identifies whether the user has requested cancellation of
            the operation. Operations that have successfully been
            cancelled have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            API version used to start the operation.
    """

    create_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target = proto.Field(
        proto.STRING,
        number=3,
    )
    verb = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message = proto.Field(
        proto.STRING,
        number=5,
    )
    cancellation_requested = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version = proto.Field(
        proto.STRING,
        number=7,
    )


class Instance(proto.Message):
    r"""An Instance represents the instance resources of the
    Registry. Currently, only one instance is allowed for each
    project.

    Attributes:
        name (str):
            Format: ``projects/*/locations/*/instance``. Currently only
            ``locations/global`` is supported.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation timestamp.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update timestamp.
        state (google.cloud.apigee_registry_v1.types.Instance.State):
            Output only. The current state of the
            Instance.
        state_message (str):
            Output only. Extra information of Instance.State if the
            state is ``FAILED``.
        config (google.cloud.apigee_registry_v1.types.Instance.Config):
            Required. Config of the Instance.
    """

    class State(proto.Enum):
        r"""State of the Instance."""
        STATE_UNSPECIFIED = 0
        INACTIVE = 1
        CREATING = 2
        ACTIVE = 3
        UPDATING = 4
        DELETING = 5
        FAILED = 6

    class Config(proto.Message):
        r"""Available configurations to provision an Instance.

        Attributes:
            location (str):
                Output only. The GCP location where the
                Instance resides.
            cmek_key_name (str):
                Required. The Customer Managed Encryption Key (CMEK) used
                for data encryption. The CMEK name should follow the format
                of
                ``projects/([^/]+)/locations/([^/]+)/keyRings/([^/]+)/cryptoKeys/([^/]+)``,
                where the ``location`` must match InstanceConfig.location.
        """

        location = proto.Field(
            proto.STRING,
            number=1,
        )
        cmek_key_name = proto.Field(
            proto.STRING,
            number=2,
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    state_message = proto.Field(
        proto.STRING,
        number=5,
    )
    config = proto.Field(
        proto.MESSAGE,
        number=6,
        message=Config,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
