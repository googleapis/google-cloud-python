# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from google.cloud.apphub_v1.types import attributes as gca_attributes

__protobuf__ = proto.module(
    package="google.cloud.apphub.v1",
    manifest={
        "Application",
        "Scope",
    },
)


class Application(proto.Message):
    r"""Application defines the governance boundary for App Hub
    Entities that perform a logical end-to-end business function.
    App Hub supports application level IAM permission to align with
    governance requirements.

    Attributes:
        name (str):
            Identifier. The resource name of an
            Application. Format:
            "projects/{host-project-id}/locations/{location}/applications/{application-id}".
        display_name (str):
            Optional. User-defined name for the
            Application. Can have a maximum length of 63
            characters.
        description (str):
            Optional. User-defined description of an
            Application. Can have a maximum length of 2048
            characters.
        attributes (google.cloud.apphub_v1.types.Attributes):
            Optional. Consumer provided attributes.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Create time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Update time.
        scope (google.cloud.apphub_v1.types.Scope):
            Required. Immutable. Defines what data can be
            included into this Application. Limits which
            Services and Workloads can be registered.
        uid (str):
            Output only. A universally unique identifier (in UUID4
            format) for the ``Application``.
        state (google.cloud.apphub_v1.types.Application.State):
            Output only. Application state.
    """

    class State(proto.Enum):
        r"""Application state.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified state.
            CREATING (1):
                The Application is being created.
            ACTIVE (2):
                The Application is ready to register Services
                and Workloads.
            DELETING (3):
                The Application is being deleted.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        DELETING = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    attributes: gca_attributes.Attributes = proto.Field(
        proto.MESSAGE,
        number=4,
        message=gca_attributes.Attributes,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    scope: "Scope" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="Scope",
    )
    uid: str = proto.Field(
        proto.STRING,
        number=10,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=11,
        enum=State,
    )


class Scope(proto.Message):
    r"""Scope of an application.

    Attributes:
        type_ (google.cloud.apphub_v1.types.Scope.Type):
            Required. Scope Type.
    """

    class Type(proto.Enum):
        r"""Scope Type.

        Values:
            TYPE_UNSPECIFIED (0):
                Unspecified type.
            REGIONAL (1):
                Regional type.
        """
        TYPE_UNSPECIFIED = 0
        REGIONAL = 1

    type_: Type = proto.Field(
        proto.ENUM,
        number=1,
        enum=Type,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
