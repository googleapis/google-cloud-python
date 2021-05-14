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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.appengine.v1",
    manifest={"OperationMetadataV1", "CreateVersionMetadataV1",},
)


class OperationMetadataV1(proto.Message):
    r"""Metadata for the given
    [google.longrunning.Operation][google.longrunning.Operation].

    Attributes:
        method (str):
            API method that initiated this operation. Example:
            ``google.appengine.v1.Versions.CreateVersion``.

            @OutputOnly
        insert_time (google.protobuf.timestamp_pb2.Timestamp):
            Time that this operation was created.
            @OutputOnly
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Time that this operation completed.
            @OutputOnly
        user (str):
            User who requested this operation.
            @OutputOnly
        target (str):
            Name of the resource that this operation is acting on.
            Example: ``apps/myapp/services/default``.

            @OutputOnly
        ephemeral_message (str):
            Ephemeral message that may change every time
            the operation is polled. @OutputOnly
        warning (Sequence[str]):
            Durable messages that persist on every
            operation poll. @OutputOnly
        create_version_metadata (google.cloud.appengine_admin_v1.types.CreateVersionMetadataV1):

    """

    method = proto.Field(proto.STRING, number=1,)
    insert_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    user = proto.Field(proto.STRING, number=4,)
    target = proto.Field(proto.STRING, number=5,)
    ephemeral_message = proto.Field(proto.STRING, number=6,)
    warning = proto.RepeatedField(proto.STRING, number=7,)
    create_version_metadata = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="method_metadata",
        message="CreateVersionMetadataV1",
    )


class CreateVersionMetadataV1(proto.Message):
    r"""Metadata for the given
    [google.longrunning.Operation][google.longrunning.Operation] during
    a
    [google.appengine.v1.CreateVersionRequest][google.appengine.v1.CreateVersionRequest].

    Attributes:
        cloud_build_id (str):
            The Cloud Build ID if one was created as part
            of the version create. @OutputOnly
    """

    cloud_build_id = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
