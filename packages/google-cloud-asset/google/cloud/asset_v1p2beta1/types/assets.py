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

from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.asset.v1p2beta1",
    manifest={"TemporalAsset", "TimeWindow", "Asset", "Resource",},
)


class TemporalAsset(proto.Message):
    r"""Temporal asset. In addition to the asset, the temporal asset
    includes the status of the asset and valid from and to time of
    it.

    Attributes:
        window (google.cloud.asset_v1p2beta1.types.TimeWindow):
            The time window when the asset data and state
            was observed.
        deleted (bool):
            If the asset is deleted or not.
        asset (google.cloud.asset_v1p2beta1.types.Asset):
            Asset.
    """

    window = proto.Field(proto.MESSAGE, number=1, message="TimeWindow",)
    deleted = proto.Field(proto.BOOL, number=2,)
    asset = proto.Field(proto.MESSAGE, number=3, message="Asset",)


class TimeWindow(proto.Message):
    r"""A time window of (start_time, end_time].
    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Start time of the time window (exclusive).
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            End time of the time window (inclusive).
            Current timestamp if not specified.
    """

    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)


class Asset(proto.Message):
    r"""Cloud asset. This includes all Google Cloud Platform
    resources, Cloud IAM policies, and other non-GCP assets.

    Attributes:
        name (str):
            The full name of the asset. For example:
            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
            for more information.
        asset_type (str):
            Type of the asset. Example:
            "compute.googleapis.com/Disk".
        resource (google.cloud.asset_v1p2beta1.types.Resource):
            Representation of the resource.
        iam_policy (google.iam.v1.policy_pb2.Policy):
            Representation of the actual Cloud IAM policy
            set on a cloud resource. For each resource,
            there must be at most one Cloud IAM policy set
            on it.
        ancestors (Sequence[str]):
            Asset's ancestry path in Cloud Resource Manager (CRM)
            hierarchy, represented as a list of relative resource names.
            Ancestry path starts with the closest CRM ancestor and ends
            at root. If the asset is a CRM project/folder/organization,
            this starts from the asset itself.

            Example: ["projects/123456789", "folders/5432",
            "organizations/1234"]
    """

    name = proto.Field(proto.STRING, number=1,)
    asset_type = proto.Field(proto.STRING, number=2,)
    resource = proto.Field(proto.MESSAGE, number=3, message="Resource",)
    iam_policy = proto.Field(proto.MESSAGE, number=4, message=policy_pb2.Policy,)
    ancestors = proto.RepeatedField(proto.STRING, number=6,)


class Resource(proto.Message):
    r"""Representation of a cloud resource.
    Attributes:
        version (str):
            The API version. Example: "v1".
        discovery_document_uri (str):
            The URL of the discovery document containing the resource's
            JSON schema. For example:
            ``"https://www.googleapis.com/discovery/v1/apis/compute/v1/rest"``.
            It will be left unspecified for resources without a
            discovery-based API, such as Cloud Bigtable.
        discovery_name (str):
            The JSON schema name listed in the discovery
            document. Example: "Project". It will be left
            unspecified for resources (such as Cloud
            Bigtable) without a discovery-based API.
        resource_url (str):
            The REST URL for accessing the resource. An HTTP GET
            operation using this URL returns the resource itself.
            Example:
            ``https://cloudresourcemanager.googleapis.com/v1/projects/my-project-123``.
            It will be left unspecified for resources without a REST
            API.
        parent (str):
            The full name of the immediate parent of this resource. See
            `Resource
            Names <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
            for more information.

            For GCP assets, it is the parent resource defined in the
            `Cloud IAM policy
            hierarchy <https://cloud.google.com/iam/docs/overview#policy_hierarchy>`__.
            For example:
            ``"//cloudresourcemanager.googleapis.com/projects/my_project_123"``.

            For third-party assets, it is up to the users to define.
        data (google.protobuf.struct_pb2.Struct):
            The content of the resource, in which some
            sensitive fields are scrubbed away and may not
            be present.
    """

    version = proto.Field(proto.STRING, number=1,)
    discovery_document_uri = proto.Field(proto.STRING, number=2,)
    discovery_name = proto.Field(proto.STRING, number=3,)
    resource_url = proto.Field(proto.STRING, number=4,)
    parent = proto.Field(proto.STRING, number=5,)
    data = proto.Field(proto.MESSAGE, number=6, message=struct_pb2.Struct,)


__all__ = tuple(sorted(__protobuf__.manifest))
