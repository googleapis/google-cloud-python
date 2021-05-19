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

from google.cloud.securitycenter_v1beta1.types import (
    security_marks as gcs_security_marks,
)
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1beta1", manifest={"Asset",},
)


class Asset(proto.Message):
    r"""Security Command Center representation of a Google Cloud
    resource.

    The Asset is a Security Command Center resource that captures
    information about a single Google Cloud resource. All
    modifications to an Asset are only within the context of
    Security Command Center and don't affect the referenced Google
    Cloud resource.

    Attributes:
        name (str):
            The relative resource name of this asset. See:
            https://cloud.google.com/apis/design/resource_names#relative_resource_name
            Example:
            "organizations/{organization_id}/assets/{asset_id}".
        security_center_properties (google.cloud.securitycenter_v1beta1.types.Asset.SecurityCenterProperties):
            Security Command Center managed properties.
            These properties are managed by Security Command
            Center and cannot be modified by the user.
        resource_properties (Sequence[google.cloud.securitycenter_v1beta1.types.Asset.ResourcePropertiesEntry]):
            Resource managed properties. These properties
            are managed and defined by the Google Cloud
            resource and cannot be modified by the user.
        security_marks (google.cloud.securitycenter_v1beta1.types.SecurityMarks):
            User specified security marks. These marks
            are entirely managed by the user and come from
            the SecurityMarks resource that belongs to the
            asset.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the asset was created in
            Security Command Center.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the asset was last updated,
            added, or deleted in Security Command Center.
    """

    class SecurityCenterProperties(proto.Message):
        r"""Security Command Center managed properties. These properties
        are managed by Security Command Center and cannot be modified by
        the user.

        Attributes:
            resource_name (str):
                Immutable. The full resource name of the Google Cloud
                resource this asset represents. This field is immutable
                after create time. See:
                https://cloud.google.com/apis/design/resource_names#full_resource_name
            resource_type (str):
                The type of the Google Cloud resource.
                Examples include: APPLICATION, PROJECT, and
                ORGANIZATION. This is a case insensitive field
                defined by Security Command Center and/or the
                producer of the resource and is immutable after
                create time.
            resource_parent (str):
                The full resource name of the immediate parent of the
                resource. See:
                https://cloud.google.com/apis/design/resource_names#full_resource_name
            resource_project (str):
                The full resource name of the project the resource belongs
                to. See:
                https://cloud.google.com/apis/design/resource_names#full_resource_name
            resource_owners (Sequence[str]):
                Owners of the Google Cloud resource.
        """

        resource_name = proto.Field(proto.STRING, number=1,)
        resource_type = proto.Field(proto.STRING, number=2,)
        resource_parent = proto.Field(proto.STRING, number=3,)
        resource_project = proto.Field(proto.STRING, number=4,)
        resource_owners = proto.RepeatedField(proto.STRING, number=5,)

    name = proto.Field(proto.STRING, number=1,)
    security_center_properties = proto.Field(
        proto.MESSAGE, number=2, message=SecurityCenterProperties,
    )
    resource_properties = proto.MapField(
        proto.STRING, proto.MESSAGE, number=7, message=struct_pb2.Value,
    )
    security_marks = proto.Field(
        proto.MESSAGE, number=8, message=gcs_security_marks.SecurityMarks,
    )
    create_time = proto.Field(proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
