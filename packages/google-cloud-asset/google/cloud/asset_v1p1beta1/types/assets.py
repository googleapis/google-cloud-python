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


__protobuf__ = proto.module(
    package="google.cloud.asset.v1p1beta1",
    manifest={"StandardResourceMetadata", "IamPolicySearchResult", "Permissions",},
)


class StandardResourceMetadata(proto.Message):
    r"""The standard metadata of a cloud resource.
    Attributes:
        name (str):
            The full resource name. For example:
            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
            for more information.
        asset_type (str):
            The type of this resource.
            For example: "compute.googleapis.com/Disk".
        project (str):
            The project that this resource belongs to, in the form of
            ``projects/{project_number}``.
        display_name (str):
            The display name of this resource.
        description (str):
            One or more paragraphs of text description of
            this resource. Maximum length could be up to 1M
            bytes.
        additional_attributes (Sequence[str]):
            Additional searchable attributes of this
            resource. Informational only. The exact set of
            attributes is subject to change. For example:
            project id, DNS name etc.
        location (str):
            Location can be "global", regional like "us-
            ast1", or zonal like "us-west1-b".
        labels (Sequence[google.cloud.asset_v1p1beta1.types.StandardResourceMetadata.LabelsEntry]):
            Labels associated with this resource. See `Labelling and
            grouping GCP
            resources <https://cloud.google.com/blog/products/gcp/labelling-and-grouping-your-google-cloud-platform-resources>`__
            for more information.
        network_tags (Sequence[str]):
            Network tags associated with this resource. Like labels,
            network tags are a type of annotations used to group GCP
            resources. See `Labelling GCP
            resources <lhttps://cloud.google.com/blog/products/gcp/labelling-and-grouping-your-google-cloud-platform-resources>`__
            for more information.
    """

    name = proto.Field(proto.STRING, number=1,)
    asset_type = proto.Field(proto.STRING, number=2,)
    project = proto.Field(proto.STRING, number=3,)
    display_name = proto.Field(proto.STRING, number=4,)
    description = proto.Field(proto.STRING, number=5,)
    additional_attributes = proto.RepeatedField(proto.STRING, number=10,)
    location = proto.Field(proto.STRING, number=11,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=12,)
    network_tags = proto.RepeatedField(proto.STRING, number=13,)


class IamPolicySearchResult(proto.Message):
    r"""The result for a IAM Policy search.
    Attributes:
        resource (str):
            The `full resource
            name <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
            of the resource associated with this IAM policy.
        project (str):
            The project that the associated GCP resource belongs to, in
            the form of ``projects/{project_number}``. If an IAM policy
            is set on a resource (like VM instance, Cloud Storage
            bucket), the project field will indicate the project that
            contains the resource. If an IAM policy is set on a folder
            or orgnization, the project field will be empty.
        policy (google.iam.v1.policy_pb2.Policy):
            The IAM policy directly set on the given
            resource. Note that the original IAM policy can
            contain multiple bindings. This only contains
            the bindings that match the given query. For
            queries that don't contain a constrain on
            policies (e.g. an empty query), this contains
            all the bindings.
        explanation (google.cloud.asset_v1p1beta1.types.IamPolicySearchResult.Explanation):
            Explanation about the IAM policy search
            result. It contains additional information to
            explain why the search result matches the query.
    """

    class Explanation(proto.Message):
        r"""Explanation about the IAM policy search result.
        Attributes:
            matched_permissions (Sequence[google.cloud.asset_v1p1beta1.types.IamPolicySearchResult.Explanation.MatchedPermissionsEntry]):
                The map from roles to their included permission matching the
                permission query (e.g. containing
                ``policy.role.permissions:``). A sample role string:
                "roles/compute.instanceAdmin". The roles can also be found
                in the returned ``policy`` bindings. Note that the map is
                populated only if requesting with a permission query.
        """

        matched_permissions = proto.MapField(
            proto.STRING, proto.MESSAGE, number=1, message="Permissions",
        )

    resource = proto.Field(proto.STRING, number=1,)
    project = proto.Field(proto.STRING, number=3,)
    policy = proto.Field(proto.MESSAGE, number=4, message=policy_pb2.Policy,)
    explanation = proto.Field(proto.MESSAGE, number=5, message=Explanation,)


class Permissions(proto.Message):
    r"""IAM permissions
    Attributes:
        permissions (Sequence[str]):
            A list of permissions. A sample permission
            string: "compute.disk.get".
    """

    permissions = proto.RepeatedField(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
