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

__protobuf__ = proto.module(
    package="google.cloud.accesscontextmanager.v1",
    manifest={
        "AccessPolicy",
    },
)


class AccessPolicy(proto.Message):
    r"""``AccessPolicy`` is a container for ``AccessLevels`` (which define
    the necessary attributes to use Google Cloud services) and
    ``ServicePerimeters`` (which define regions of services able to
    freely pass data within a perimeter). An access policy is globally
    visible within an organization, and the restrictions it specifies
    apply to all projects within an organization.

    Attributes:
        name (str):
            Output only. Resource name of the ``AccessPolicy``. Format:
            ``accessPolicies/{access_policy}``
        parent (str):
            Required. The parent of this ``AccessPolicy`` in the Cloud
            Resource Hierarchy. Currently immutable once created.
            Format: ``organizations/{organization_id}``
        title (str):
            Required. Human readable title. Does not
            affect behavior.
        scopes (MutableSequence[str]):
            The scopes of a policy define which resources an ACM policy
            can restrict, and where ACM resources can be referenced. For
            example, a policy with scopes=["folders/123"] has the
            following behavior:

            -  vpcsc perimeters can only restrict projects within
               folders/123
            -  access levels can only be referenced by resources within
               folders/123. If empty, there are no limitations on which
               resources can be restricted by an ACM policy, and there
               are no limitations on where ACM resources can be
               referenced. Only one policy can include a given scope
               (attempting to create a second policy which includes
               "folders/123" will result in an error). Currently, scopes
               cannot be modified after a policy is created. Currently,
               policies can only have a single scope. Format: list of
               ``folders/{folder_number}`` or
               ``projects/{project_number}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the ``AccessPolicy`` was created in UTC.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the ``AccessPolicy`` was updated in UTC.
        etag (str):
            Output only. An opaque identifier for the current version of
            the ``AccessPolicy``. This will always be a strongly
            validated etag, meaning that two Access Polices will be
            identical if and only if their etags are identical. Clients
            should not expect this to be in any specific format.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    parent: str = proto.Field(
        proto.STRING,
        number=2,
    )
    title: str = proto.Field(
        proto.STRING,
        number=3,
    )
    scopes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
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
        number=6,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
