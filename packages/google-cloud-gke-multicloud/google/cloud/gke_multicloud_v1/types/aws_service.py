# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.gke_multicloud_v1.types import aws_resources

__protobuf__ = proto.module(
    package="google.cloud.gkemulticloud.v1",
    manifest={
        "CreateAwsClusterRequest",
        "UpdateAwsClusterRequest",
        "GetAwsClusterRequest",
        "ListAwsClustersRequest",
        "ListAwsClustersResponse",
        "DeleteAwsClusterRequest",
        "CreateAwsNodePoolRequest",
        "UpdateAwsNodePoolRequest",
        "GetAwsNodePoolRequest",
        "ListAwsNodePoolsRequest",
        "ListAwsNodePoolsResponse",
        "DeleteAwsNodePoolRequest",
        "GetAwsServerConfigRequest",
        "GenerateAwsAccessTokenRequest",
        "GenerateAwsAccessTokenResponse",
    },
)


class CreateAwsClusterRequest(proto.Message):
    r"""Request message for ``AwsClusters.CreateAwsCluster`` method.

    Attributes:
        parent (str):
            Required. The parent location where this
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
            resource will be created.

            Location names are formatted as
            ``projects/<project-id>/locations/<region>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud resource names.
        aws_cluster (google.cloud.gke_multicloud_v1.types.AwsCluster):
            Required. The specification of the
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster] to
            create.
        aws_cluster_id (str):
            Required. A client provided ID the resource. Must be unique
            within the parent resource.

            The provided ID will be part of the
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
            resource name formatted as
            ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

            Valid characters are ``/[a-z][0-9]-/``. Cannot be longer
            than 63 characters.
        validate_only (bool):
            If set, only validate the request, but do not
            actually create the cluster.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    aws_cluster: aws_resources.AwsCluster = proto.Field(
        proto.MESSAGE,
        number=2,
        message=aws_resources.AwsCluster,
    )
    aws_cluster_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateAwsClusterRequest(proto.Message):
    r"""Request message for ``AwsClusters.UpdateAwsCluster`` method.

    Attributes:
        aws_cluster (google.cloud.gke_multicloud_v1.types.AwsCluster):
            Required. The
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
            resource to update.
        validate_only (bool):
            If set, only validate the request, but do not
            actually update the cluster.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update. At least one path must
            be supplied in this field. The elements of the repeated
            paths field can only include these fields from
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]:

            -  ``description``.
            -  ``annotations``.
            -  ``control_plane.version``.
            -  ``authorization.admin_users``.
            -  ``control_plane.aws_services_authentication.role_arn``.
            -  ``control_plane.aws_services_authentication.role_session_name``.
            -  ``control_plane.config_encryption.kms_key_arn``.
            -  ``control_plane.instance_type``.
            -  ``control_plane.security_group_ids``.
            -  ``control_plane.proxy_config``.
            -  ``control_plane.proxy_config.secret_arn``.
            -  ``control_plane.proxy_config.secret_version``.
            -  ``control_plane.root_volume.size_gib``.
            -  ``control_plane.root_volume.volume_type``.
            -  ``control_plane.root_volume.iops``.
            -  ``control_plane.root_volume.kms_key_arn``.
            -  ``control_plane.ssh_config``.
            -  ``control_plane.ssh_config.ec2_key_pair``.
            -  ``control_plane.instance_placement.tenancy``.
            -  ``control_plane.iam_instance_profile``.
            -  ``logging_config.component_config.enable_components``.
            -  ``control_plane.tags``.
            -  ``monitoring_config.managed_prometheus_config.enabled``.
    """

    aws_cluster: aws_resources.AwsCluster = proto.Field(
        proto.MESSAGE,
        number=1,
        message=aws_resources.AwsCluster,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=4,
        message=field_mask_pb2.FieldMask,
    )


class GetAwsClusterRequest(proto.Message):
    r"""Request message for ``AwsClusters.GetAwsCluster`` method.

    Attributes:
        name (str):
            Required. The name of the
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
            resource to describe.

            ``AwsCluster`` names are formatted as
            ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud Platform resource names.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAwsClustersRequest(proto.Message):
    r"""Request message for ``AwsClusters.ListAwsClusters`` method.

    Attributes:
        parent (str):
            Required. The parent location which owns this collection of
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
            resources.

            Location names are formatted as
            ``projects/<project-id>/locations/<region>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud Platform resource names.
        page_size (int):
            The maximum number of items to return.

            If not specified, a default value of 50 will be used by the
            service. Regardless of the pageSize value, the response can
            include a partial list and a caller should only rely on
            response's
            [nextPageToken][google.cloud.gkemulticloud.v1.ListAwsClustersResponse.next_page_token]
            to determine if there are more instances left to be queried.
        page_token (str):
            The ``nextPageToken`` value returned from a previous
            [awsClusters.list][google.cloud.gkemulticloud.v1.AwsClusters.ListAwsClusters]
            request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListAwsClustersResponse(proto.Message):
    r"""Response message for ``AwsClusters.ListAwsClusters`` method.

    Attributes:
        aws_clusters (MutableSequence[google.cloud.gke_multicloud_v1.types.AwsCluster]):
            A list of
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
            resources in the specified Google Cloud Platform project and
            region region.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    aws_clusters: MutableSequence[aws_resources.AwsCluster] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=aws_resources.AwsCluster,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteAwsClusterRequest(proto.Message):
    r"""Request message for ``AwsClusters.DeleteAwsCluster`` method.

    Attributes:
        name (str):
            Required. The resource name the
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster] to
            delete.

            ``AwsCluster`` names are formatted as
            ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud Platform resource names.
        validate_only (bool):
            If set, only validate the request, but do not
            actually delete the resource.
        allow_missing (bool):
            If set to true, and the
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
            resource is not found, the request will succeed but no
            action will be taken on the server and a completed
            [Operation][google.longrunning.Operation] will be returned.

            Useful for idempotent deletion.
        etag (str):
            The current etag of the
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster].

            Allows clients to perform deletions through optimistic
            concurrency control.

            If the provided etag does not match the current etag of the
            cluster, the request will fail and an ABORTED error will be
            returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=4,
    )


class CreateAwsNodePoolRequest(proto.Message):
    r"""Response message for ``AwsClusters.CreateAwsNodePool`` method.

    Attributes:
        parent (str):
            Required. The
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
            resource where this node pool will be created.

            ``AwsCluster`` names are formatted as
            ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud resource names.
        aws_node_pool (google.cloud.gke_multicloud_v1.types.AwsNodePool):
            Required. The specification of the
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool] to
            create.
        aws_node_pool_id (str):
            Required. A client provided ID the resource. Must be unique
            within the parent resource.

            The provided ID will be part of the
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
            resource name formatted as
            ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>/awsNodePools/<node-pool-id>``.

            Valid characters are ``/[a-z][0-9]-/``. Cannot be longer
            than 63 characters.
        validate_only (bool):
            If set, only validate the request, but do not
            actually create the node pool.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    aws_node_pool: aws_resources.AwsNodePool = proto.Field(
        proto.MESSAGE,
        number=2,
        message=aws_resources.AwsNodePool,
    )
    aws_node_pool_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateAwsNodePoolRequest(proto.Message):
    r"""Request message for ``AwsClusters.UpdateAwsNodePool`` method.

    Attributes:
        aws_node_pool (google.cloud.gke_multicloud_v1.types.AwsNodePool):
            Required. The
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
            resource to update.
        validate_only (bool):
            If set, only validate the request, but don't
            actually update the node pool.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update. At least one path must
            be supplied in this field. The elements of the repeated
            paths field can only include these fields from
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]:

            -  ``annotations``.
            -  ``version``.
            -  ``autoscaling.min_node_count``.
            -  ``autoscaling.max_node_count``.
            -  ``config.config_encryption.kms_key_arn``.
            -  ``config.security_group_ids``.
            -  ``config.root_volume.iops``.
            -  ``config.root_volume.kms_key_arn``.
            -  ``config.root_volume.volume_type``.
            -  ``config.root_volume.size_gib``.
            -  ``config.proxy_config``.
            -  ``config.proxy_config.secret_arn``.
            -  ``config.proxy_config.secret_version``.
            -  ``config.ssh_config``.
            -  ``config.ssh_config.ec2_key_pair``.
            -  ``config.instance_placement.tenancy``.
            -  ``config.iam_instance_profile``.
            -  ``config.labels``.
            -  ``config.tags``.
            -  ``config.autoscaling_metrics_collection``.
            -  ``config.autoscaling_metrics_collection.granularity``.
            -  ``config.autoscaling_metrics_collection.metrics``.
    """

    aws_node_pool: aws_resources.AwsNodePool = proto.Field(
        proto.MESSAGE,
        number=1,
        message=aws_resources.AwsNodePool,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=3,
        message=field_mask_pb2.FieldMask,
    )


class GetAwsNodePoolRequest(proto.Message):
    r"""Request message for ``AwsClusters.GetAwsNodePool`` method.

    Attributes:
        name (str):
            Required. The name of the
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
            resource to describe.

            ``AwsNodePool`` names are formatted as
            ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>/awsNodePools/<node-pool-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud resource names.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAwsNodePoolsRequest(proto.Message):
    r"""Request message for ``AwsClusters.ListAwsNodePools`` method.

    Attributes:
        parent (str):
            Required. The parent ``AwsCluster`` which owns this
            collection of
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
            resources.

            ``AwsCluster`` names are formatted as
            ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud resource names.
        page_size (int):
            The maximum number of items to return.

            If not specified, a default value of 50 will be used by the
            service. Regardless of the pageSize value, the response can
            include a partial list and a caller should only rely on
            response's
            [nextPageToken][google.cloud.gkemulticloud.v1.ListAwsNodePoolsResponse.next_page_token]
            to determine if there are more instances left to be queried.
        page_token (str):
            The ``nextPageToken`` value returned from a previous
            [awsNodePools.list][google.cloud.gkemulticloud.v1.AwsClusters.ListAwsNodePools]
            request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListAwsNodePoolsResponse(proto.Message):
    r"""Response message for ``AwsClusters.ListAwsNodePools`` method.

    Attributes:
        aws_node_pools (MutableSequence[google.cloud.gke_multicloud_v1.types.AwsNodePool]):
            A list of
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
            resources in the specified ``AwsCluster``.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    aws_node_pools: MutableSequence[aws_resources.AwsNodePool] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=aws_resources.AwsNodePool,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteAwsNodePoolRequest(proto.Message):
    r"""Request message for ``AwsClusters.DeleteAwsNodePool`` method.

    Attributes:
        name (str):
            Required. The resource name the
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool] to
            delete.

            ``AwsNodePool`` names are formatted as
            ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>/awsNodePools/<node-pool-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud resource names.
        validate_only (bool):
            If set, only validate the request, but do not
            actually delete the node pool.
        allow_missing (bool):
            If set to true, and the
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool]
            resource is not found, the request will succeed but no
            action will be taken on the server and a completed
            [Operation][google.longrunning.Operation] will be returned.

            Useful for idempotent deletion.
        etag (str):
            The current ETag of the
            [AwsNodePool][google.cloud.gkemulticloud.v1.AwsNodePool].

            Allows clients to perform deletions through optimistic
            concurrency control.

            If the provided ETag does not match the current etag of the
            node pool, the request will fail and an ABORTED error will
            be returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=4,
    )


class GetAwsServerConfigRequest(proto.Message):
    r"""GetAwsServerConfigRequest gets the server config of GKE
    cluster on AWS.

    Attributes:
        name (str):
            Required. The name of the
            [AwsServerConfig][google.cloud.gkemulticloud.v1.AwsServerConfig]
            resource to describe.

            ``AwsServerConfig`` names are formatted as
            ``projects/<project-id>/locations/<region>/awsServerConfig``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud resource names.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GenerateAwsAccessTokenRequest(proto.Message):
    r"""Request message for ``AwsClusters.GenerateAwsAccessToken`` method.

    Attributes:
        aws_cluster (str):
            Required. The name of the
            [AwsCluster][google.cloud.gkemulticloud.v1.AwsCluster]
            resource to authenticate to.

            ``AwsCluster`` names are formatted as
            ``projects/<project-id>/locations/<region>/awsClusters/<cluster-id>``.

            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names>`__
            for more details on Google Cloud resource names.
    """

    aws_cluster: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GenerateAwsAccessTokenResponse(proto.Message):
    r"""Response message for ``AwsClusters.GenerateAwsAccessToken`` method.

    Attributes:
        access_token (str):
            Output only. Access token to authenticate to
            k8s api-server.
        expiration_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp at which the token
            will expire.
    """

    access_token: str = proto.Field(
        proto.STRING,
        number=1,
    )
    expiration_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
