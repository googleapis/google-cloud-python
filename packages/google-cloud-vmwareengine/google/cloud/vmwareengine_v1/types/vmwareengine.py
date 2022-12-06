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
from typing import MutableMapping, MutableSequence

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.vmwareengine.v1",
    manifest={
        "NetworkConfig",
        "NodeTypeConfig",
        "PrivateCloud",
        "ListPrivateCloudsRequest",
        "ListPrivateCloudsResponse",
        "GetPrivateCloudRequest",
        "CreatePrivateCloudRequest",
        "UpdatePrivateCloudRequest",
        "DeletePrivateCloudRequest",
        "UndeletePrivateCloudRequest",
        "Cluster",
        "ListClustersRequest",
        "ListClustersResponse",
        "GetClusterRequest",
        "CreateClusterRequest",
        "UpdateClusterRequest",
        "DeleteClusterRequest",
        "Subnet",
        "ListSubnetsRequest",
        "ListSubnetsResponse",
        "OperationMetadata",
        "NodeType",
        "ListNodeTypesRequest",
        "ListNodeTypesResponse",
        "GetNodeTypeRequest",
        "Credentials",
        "ShowNsxCredentialsRequest",
        "ShowVcenterCredentialsRequest",
        "ResetNsxCredentialsRequest",
        "ResetVcenterCredentialsRequest",
        "ListHcxActivationKeysResponse",
        "HcxActivationKey",
        "ListHcxActivationKeysRequest",
        "GetHcxActivationKeyRequest",
        "CreateHcxActivationKeyRequest",
        "Hcx",
        "Nsx",
        "Vcenter",
        "NetworkPolicy",
        "ListNetworkPoliciesRequest",
        "ListNetworkPoliciesResponse",
        "GetNetworkPolicyRequest",
        "UpdateNetworkPolicyRequest",
        "CreateNetworkPolicyRequest",
        "DeleteNetworkPolicyRequest",
        "VmwareEngineNetwork",
        "CreateVmwareEngineNetworkRequest",
        "UpdateVmwareEngineNetworkRequest",
        "DeleteVmwareEngineNetworkRequest",
        "GetVmwareEngineNetworkRequest",
        "ListVmwareEngineNetworksRequest",
        "ListVmwareEngineNetworksResponse",
    },
)


class NetworkConfig(proto.Message):
    r"""Network configuration in the consumer project
    with which the peering has to be done.

    Attributes:
        management_cidr (str):
            Required. Management CIDR used by VMware
            management appliances.
        vmware_engine_network (str):
            Optional. The relative resource name of the VMware Engine
            network attached to the private cloud. Specify the name in
            the following form:
            ``projects/{project}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
            where ``{project}`` can either be a project number or a
            project ID.
        vmware_engine_network_canonical (str):
            Output only. The canonical name of the VMware Engine network
            in the form:
            ``projects/{project_number}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
        management_ip_address_layout_version (int):
            Output only. The IP address layout version of the management
            IP address range. Possible versions include:

            -  ``managementIpAddressLayoutVersion=1``: Indicates the
               legacy IP address layout used by some existing private
               clouds. This is no longer supported for new private
               clouds as it does not support all features.
            -  ``managementIpAddressLayoutVersion=2``: Indicates the
               latest IP address layout used by all newly created
               private clouds. This version supports all current
               features.
    """

    management_cidr: str = proto.Field(
        proto.STRING,
        number=4,
    )
    vmware_engine_network: str = proto.Field(
        proto.STRING,
        number=5,
    )
    vmware_engine_network_canonical: str = proto.Field(
        proto.STRING,
        number=6,
    )
    management_ip_address_layout_version: int = proto.Field(
        proto.INT32,
        number=8,
    )


class NodeTypeConfig(proto.Message):
    r"""Information about the type and number of nodes associated
    with the cluster.

    Attributes:
        node_count (int):
            Required. The number of nodes of this type in
            the cluster
        custom_core_count (int):
            Optional. Customized number of cores available to each node
            of the type. This number must always be one of
            ``nodeType.availableCustomCoreCounts``. If zero is provided
            max value from ``nodeType.availableCustomCoreCounts`` will
            be used.
    """

    node_count: int = proto.Field(
        proto.INT32,
        number=1,
    )
    custom_core_count: int = proto.Field(
        proto.INT32,
        number=2,
    )


class PrivateCloud(proto.Message):
    r"""Represents a private cloud resource. Private clouds are zonal
    resources.

    Attributes:
        name (str):
            Output only. The resource name of this private cloud.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update time of this
            resource.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the resource was
            scheduled for deletion.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the resource will be
            irreversibly deleted.
        state (google.cloud.vmwareengine_v1.types.PrivateCloud.State):
            Output only. State of the resource. New
            values may be added to this enum when
            appropriate.
        network_config (google.cloud.vmwareengine_v1.types.NetworkConfig):
            Required. Network configuration of the
            private cloud.
        management_cluster (google.cloud.vmwareengine_v1.types.PrivateCloud.ManagementCluster):
            Input only. The management cluster for this private cloud.
            This field is required during creation of the private cloud
            to provide details for the default cluster.

            The following fields can't be changed after private cloud
            creation: ``ManagementCluster.clusterId``,
            ``ManagementCluster.nodeTypeId``.
        description (str):
            User-provided description for this private
            cloud.
        hcx (google.cloud.vmwareengine_v1.types.Hcx):
            Output only. HCX appliance.
        nsx (google.cloud.vmwareengine_v1.types.Nsx):
            Output only. NSX appliance.
        vcenter (google.cloud.vmwareengine_v1.types.Vcenter):
            Output only. Vcenter appliance.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
    """

    class State(proto.Enum):
        r"""Enum State defines possible states of private clouds."""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2
        UPDATING = 3
        FAILED = 5
        DELETED = 6
        PURGING = 7

    class ManagementCluster(proto.Message):
        r"""Management cluster configuration.

        Attributes:
            cluster_id (str):
                Required. The user-provided identifier of the new
                ``Cluster``. The identifier must meet the following
                requirements:

                -  Only contains 1-63 alphanumeric characters and hyphens
                -  Begins with an alphabetical character
                -  Ends with a non-hyphen character
                -  Not formatted as a UUID
                -  Complies with `RFC
                   1034 <https://datatracker.ietf.org/doc/html/rfc1034>`__
                   (section 3.5)
            node_type_configs (MutableMapping[str, google.cloud.vmwareengine_v1.types.NodeTypeConfig]):
                Required. The map of cluster node types in this cluster,
                where the key is canonical identifier of the node type
                (corresponds to the ``NodeType``).
        """

        cluster_id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        node_type_configs: MutableMapping[str, "NodeTypeConfig"] = proto.MapField(
            proto.STRING,
            proto.MESSAGE,
            number=7,
            message="NodeTypeConfig",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    expire_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=8,
        enum=State,
    )
    network_config: "NetworkConfig" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="NetworkConfig",
    )
    management_cluster: ManagementCluster = proto.Field(
        proto.MESSAGE,
        number=10,
        message=ManagementCluster,
    )
    description: str = proto.Field(
        proto.STRING,
        number=11,
    )
    hcx: "Hcx" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="Hcx",
    )
    nsx: "Nsx" = proto.Field(
        proto.MESSAGE,
        number=18,
        message="Nsx",
    )
    vcenter: "Vcenter" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="Vcenter",
    )
    uid: str = proto.Field(
        proto.STRING,
        number=20,
    )


class ListPrivateCloudsRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ListPrivateClouds][google.cloud.vmwareengine.v1.VmwareEngine.ListPrivateClouds]

    Attributes:
        parent (str):
            Required. The resource name of the private cloud to be
            queried for clusters. Resource names are schemeless URIs
            that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example: ``projects/my-project/locations/us-west1-a``
        page_size (int):
            The maximum number of private clouds to
            return in one page. The service may return fewer
            than this value. The maximum value is coerced to
            1000.
            The default value of this field is 500.
        page_token (str):
            A page token, received from a previous ``ListPrivateClouds``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListPrivateClouds`` must match the call that provided the
            page token.
        filter (str):
            A filter expression that matches resources returned in the
            response. The expression must specify the field name, a
            comparison operator, and the value that you want to use for
            filtering. The value must be a string, a number, or a
            boolean. The comparison operator must be ``=``, ``!=``,
            ``>``, or ``<``.

            For example, if you are filtering a list of private clouds,
            you can exclude the ones named ``example-pc`` by specifying
            ``name != "example-pc"``.

            You can also filter nested fields. For example, you could
            specify ``networkConfig.managementCidr = "192.168.0.0/24"``
            to include private clouds only if they have a matching
            address in their network configuration.

            To filter on multiple expressions, provide each separate
            expression within parentheses. For example:

            ::

               (name = "example-pc")
               (createTime > "2021-04-12T08:15:10.40Z")

            By default, each expression is an ``AND`` expression.
            However, you can include ``AND`` and ``OR`` expressions
            explicitly. For example:

            ::

               (name = "private-cloud-1") AND
               (createTime > "2021-04-12T08:15:10.40Z") OR
               (name = "private-cloud-2")
        order_by (str):
            Sorts list results by a certain order. By default, returned
            results are ordered by ``name`` in ascending order. You can
            also sort results in descending order based on the ``name``
            value using ``orderBy="name desc"``. Currently, only
            ordering by ``name`` is supported.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListPrivateCloudsResponse(proto.Message):
    r"""Response message for
    [VmwareEngine.ListPrivateClouds][google.cloud.vmwareengine.v1.VmwareEngine.ListPrivateClouds]

    Attributes:
        private_clouds (MutableSequence[google.cloud.vmwareengine_v1.types.PrivateCloud]):
            A list of private clouds.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached when
            making an aggregated query using wildcards.
    """

    @property
    def raw_page(self):
        return self

    private_clouds: MutableSequence["PrivateCloud"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="PrivateCloud",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetPrivateCloudRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.GetPrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.GetPrivateCloud]

    Attributes:
        name (str):
            Required. The resource name of the private cloud to
            retrieve. Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreatePrivateCloudRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.CreatePrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.CreatePrivateCloud]

    Attributes:
        parent (str):
            Required. The resource name of the location to create the
            new private cloud in. Resource names are schemeless URIs
            that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example: ``projects/my-project/locations/us-west1-a``
        private_cloud_id (str):
            Required. The user-provided identifier of the private cloud
            to be created. This identifier must be unique among each
            ``PrivateCloud`` within the parent and becomes the final
            token in the name URI. The identifier must meet the
            following requirements:

            -  Only contains 1-63 alphanumeric characters and hyphens
            -  Begins with an alphabetical character
            -  Ends with a non-hyphen character
            -  Not formatted as a UUID
            -  Complies with `RFC
               1034 <https://datatracker.ietf.org/doc/html/rfc1034>`__
               (section 3.5)
        private_cloud (google.cloud.vmwareengine_v1.types.PrivateCloud):
            Required. The initial description of the new
            private cloud.
        request_id (str):
            Optional. The request ID must be a valid UUID
            with the exception that zero UUID is not
            supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. True if you want the request to be
            validated and not executed; false otherwise.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    private_cloud_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    private_cloud: "PrivateCloud" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="PrivateCloud",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class UpdatePrivateCloudRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.UpdatePrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.UpdatePrivateCloud]

    Attributes:
        private_cloud (google.cloud.vmwareengine_v1.types.PrivateCloud):
            Required. Private cloud description.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the ``PrivateCloud`` resource by the update.
            The fields specified in ``updateMask`` are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields will be overwritten.
        request_id (str):
            Optional. The request ID must be a valid UUID
            with the exception that zero UUID is not
            supported
            (00000000-0000-0000-0000-000000000000).
    """

    private_cloud: "PrivateCloud" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PrivateCloud",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeletePrivateCloudRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.DeletePrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.DeletePrivateCloud]

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. The resource name of the private cloud to delete.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
        request_id (str):
            Optional. The request ID must be a valid UUID
            with the exception that zero UUID is not
            supported
            (00000000-0000-0000-0000-000000000000).
        force (bool):
            Optional. If set to true, cascade delete is
            enabled and all children of this private cloud
            resource are also deleted. When this flag is set
            to false, the private cloud will not be deleted
            if there are any children other than the
            management cluster. The management cluster is
            always deleted.
        delay_hours (int):
            Optional. Time delay of the deletion specified in hours. The
            default value is ``3``. Specifying a non-zero value for this
            field changes the value of ``PrivateCloud.state`` to
            ``DELETED`` and sets ``expire_time`` to the planned deletion
            time. Deletion can be cancelled before ``expire_time``
            elapses using
            [VmwareEngine.UndeletePrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.UndeletePrivateCloud].
            Specifying a value of ``0`` for this field instead begins
            the deletion process and ceases billing immediately. During
            the final deletion process, the value of
            ``PrivateCloud.state`` becomes ``PURGING``.

            This field is a member of `oneof`_ ``_delay_hours``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    delay_hours: int = proto.Field(
        proto.INT32,
        number=4,
        optional=True,
    )


class UndeletePrivateCloudRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.UndeletePrivateCloud][google.cloud.vmwareengine.v1.VmwareEngine.UndeletePrivateCloud]

    Attributes:
        name (str):
            Required. The resource name of the private cloud scheduled
            for deletion. Resource names are schemeless URIs that follow
            the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
        request_id (str):
            Optional. The request ID must be a valid UUID
            with the exception that zero UUID is not
            supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Cluster(proto.Message):
    r"""A cluster in a private cloud.

    Attributes:
        name (str):
            Output only. The resource name of this cluster. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud/clusters/my-cluster``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update time of this
            resource.
        state (google.cloud.vmwareengine_v1.types.Cluster.State):
            Output only. State of the resource.
        management (bool):
            Output only. True if the cluster is a
            management cluster; false otherwise. There can
            only be one management cluster in a private
            cloud and it has to be the first one.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
        node_type_configs (MutableMapping[str, google.cloud.vmwareengine_v1.types.NodeTypeConfig]):
            Required. The map of cluster node types in this cluster,
            where the key is canonical identifier of the node type
            (corresponds to the ``NodeType``).
    """

    class State(proto.Enum):
        r"""Enum State defines possible states of private cloud clusters."""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2
        UPDATING = 3
        DELETING = 4
        REPAIRING = 5

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=6,
        enum=State,
    )
    management: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=14,
    )
    node_type_configs: MutableMapping[str, "NodeTypeConfig"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=16,
        message="NodeTypeConfig",
    )


class ListClustersRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ListClusters][google.cloud.vmwareengine.v1.VmwareEngine.ListClusters]

    Attributes:
        parent (str):
            Required. The resource name of the private cloud to query
            for clusters. Resource names are schemeless URIs that follow
            the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
        page_size (int):
            The maximum number of clusters to return in
            one page. The service may return fewer than this
            value. The maximum value is coerced to 1000.
            The default value of this field is 500.
        page_token (str):
            A page token, received from a previous ``ListClusters``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListClusters`` must match the call that provided the page
            token.
        filter (str):
            To filter on multiple expressions, provide each separate
            expression within parentheses. For example:

            ::

               (name = "example-cluster")
               (nodeCount = "3")

            By default, each expression is an ``AND`` expression.
            However, you can include ``AND`` and ``OR`` expressions
            explicitly. For example:

            ::

               (name = "example-cluster-1") AND
               (createTime > "2021-04-12T08:15:10.40Z") OR
               (name = "example-cluster-2")
        order_by (str):
            Sorts list results by a certain order. By default, returned
            results are ordered by ``name`` in ascending order. You can
            also sort results in descending order based on the ``name``
            value using ``orderBy="name desc"``. Currently, only
            ordering by ``name`` is supported.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListClustersResponse(proto.Message):
    r"""Response message for
    [VmwareEngine.ListClusters][google.cloud.vmwareengine.v1.VmwareEngine.ListClusters]

    Attributes:
        clusters (MutableSequence[google.cloud.vmwareengine_v1.types.Cluster]):
            A list of private cloud clusters.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached when
            making an aggregated query using wildcards.
    """

    @property
    def raw_page(self):
        return self

    clusters: MutableSequence["Cluster"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Cluster",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetClusterRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.GetCluster][google.cloud.vmwareengine.v1.VmwareEngine.GetCluster]

    Attributes:
        name (str):
            Required. The cluster resource name to retrieve. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud/clusters/my-cluster``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateClusterRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.CreateCluster][google.cloud.vmwareengine.v1.VmwareEngine.CreateCluster]

    Attributes:
        parent (str):
            Required. The resource name of the private cloud to create a
            new cluster in. Resource names are schemeless URIs that
            follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
        cluster_id (str):
            Required. The user-provided identifier of the new
            ``Cluster``. This identifier must be unique among clusters
            within the parent and becomes the final token in the name
            URI. The identifier must meet the following requirements:

            -  Only contains 1-63 alphanumeric characters and hyphens
            -  Begins with an alphabetical character
            -  Ends with a non-hyphen character
            -  Not formatted as a UUID
            -  Complies with `RFC
               1034 <https://datatracker.ietf.org/doc/html/rfc1034>`__
               (section 3.5)
        cluster (google.cloud.vmwareengine_v1.types.Cluster):
            Required. The initial description of the new
            cluster.
        request_id (str):
            Optional. The request ID must be a valid UUID
            with the exception that zero UUID is not
            supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. True if you want the request to be
            validated and not executed; false otherwise.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster: "Cluster" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Cluster",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class UpdateClusterRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.UpdateCluster][google.cloud.vmwareengine.v1.VmwareEngine.UpdateCluster]

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the ``Cluster`` resource by the update. The
            fields specified in the ``updateMask`` are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields will be overwritten.
        cluster (google.cloud.vmwareengine_v1.types.Cluster):
            Required. The description of the cluster.
        request_id (str):
            Optional. The request ID must be a valid UUID
            with the exception that zero UUID is not
            supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. True if you want the request to be
            validated and not executed; false otherwise.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    cluster: "Cluster" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Cluster",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class DeleteClusterRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.DeleteCluster][google.cloud.vmwareengine.v1.VmwareEngine.DeleteCluster]

    Attributes:
        name (str):
            Required. The resource name of the cluster to delete.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud/clusters/my-cluster``
        request_id (str):
            Optional. The request ID must be a valid UUID
            with the exception that zero UUID is not
            supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Subnet(proto.Message):
    r"""Subnet in a private cloud. Either ``management`` subnets (such as
    vMotion) that are read-only, or ``userDefined``, which can also be
    updated.

    Attributes:
        name (str):
            Output only. The resource name of this subnet. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud/subnets/my-subnet``
        ip_cidr_range (str):
            The IP address range of the subnet in CIDR
            format '10.0.0.0/24'.
        gateway_ip (str):
            The IP address of the gateway of this subnet.
            Must fall within the IP prefix defined above.
        type_ (str):
            Output only. The type of the subnet. For
            example "management" or "userDefined".
        state (google.cloud.vmwareengine_v1.types.Subnet.State):
            Output only. The state of the resource.
    """

    class State(proto.Enum):
        r"""Defines possible states of subnets."""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2
        UPDATING = 3
        DELETING = 4

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ip_cidr_range: str = proto.Field(
        proto.STRING,
        number=7,
    )
    gateway_ip: str = proto.Field(
        proto.STRING,
        number=8,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=11,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=13,
        enum=State,
    )


class ListSubnetsRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ListSubnets][google.cloud.vmwareengine.v1.VmwareEngine.ListSubnets]

    Attributes:
        parent (str):
            Required. The resource name of the private cloud to be
            queried for subnets. Resource names are schemeless URIs that
            follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
        page_size (int):
            The maximum number of subnets to return in
            one page. The service may return fewer than this
            value. The maximum value is coerced to 1000.
            The default value of this field is 500.
        page_token (str):
            A page token, received from a previous
            ``ListSubnetsRequest`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListSubnetsRequest`` must match the call that provided the
            page token.
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


class ListSubnetsResponse(proto.Message):
    r"""Response message for
    [VmwareEngine.ListSubnets][google.cloud.vmwareengine.v1.VmwareEngine.ListSubnets]

    Attributes:
        subnets (MutableSequence[google.cloud.vmwareengine_v1.types.Subnet]):
            A list of subnets.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    subnets: MutableSequence["Subnet"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Subnet",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. True if the user has requested cancellation of
            the operation; false otherwise. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


class NodeType(proto.Message):
    r"""Describes node type.

    Attributes:
        name (str):
            Output only. The resource name of this node type. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-proj/locations/us-west1-a/nodeTypes/standard-72``
        node_type_id (str):
            Output only. The canonical identifier of the node type
            (corresponds to the ``NodeType``). For example: standard-72.
        display_name (str):
            Output only. The friendly name for this node
            type. For example: ve1-standard-72
        virtual_cpu_count (int):
            Output only. The total number of virtual CPUs
            in a single node.
        total_core_count (int):
            Output only. The total number of CPU cores in
            a single node.
        memory_gb (int):
            Output only. The amount of physical memory
            available, defined in GB.
        disk_size_gb (int):
            Output only. The amount of storage available,
            defined in GB.
        available_custom_core_counts (MutableSequence[int]):
            Output only. List of possible values of
            custom core count.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    node_type_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    virtual_cpu_count: int = proto.Field(
        proto.INT32,
        number=4,
    )
    total_core_count: int = proto.Field(
        proto.INT32,
        number=5,
    )
    memory_gb: int = proto.Field(
        proto.INT32,
        number=7,
    )
    disk_size_gb: int = proto.Field(
        proto.INT32,
        number=8,
    )
    available_custom_core_counts: MutableSequence[int] = proto.RepeatedField(
        proto.INT32,
        number=11,
    )


class ListNodeTypesRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ListNodeTypes][google.cloud.vmwareengine.v1.VmwareEngine.ListNodeTypes]

    Attributes:
        parent (str):
            Required. The resource name of the location to be queried
            for node types. Resource names are schemeless URIs that
            follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example: ``projects/my-project/locations/us-west1-a``
        page_size (int):
            The maximum number of node types to return in
            one page. The service may return fewer than this
            value. The maximum value is coerced to 1000.
            The default value of this field is 500.
        page_token (str):
            A page token, received from a previous ``ListNodeTypes``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListNodeTypes`` must match the call that provided the page
            token.
        filter (str):
            A filter expression that matches resources returned in the
            response. The expression must specify the field name, a
            comparison operator, and the value that you want to use for
            filtering. The value must be a string, a number, or a
            boolean. The comparison operator must be ``=``, ``!=``,
            ``>``, or ``<``.

            For example, if you are filtering a list of node types, you
            can exclude the ones named ``standard-72`` by specifying
            ``name != "standard-72"``.

            To filter on multiple expressions, provide each separate
            expression within parentheses. For example:

            ::

               (name = "standard-72")
               (virtual_cpu_count > 2)

            By default, each expression is an ``AND`` expression.
            However, you can include ``AND`` and ``OR`` expressions
            explicitly. For example:

            ::

               (name = "standard-96") AND
               (virtual_cpu_count > 2) OR
               (name = "standard-72")
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListNodeTypesResponse(proto.Message):
    r"""Response message for
    [VmwareEngine.ListNodeTypes][google.cloud.vmwareengine.v1.VmwareEngine.ListNodeTypes]

    Attributes:
        node_types (MutableSequence[google.cloud.vmwareengine_v1.types.NodeType]):
            A list of Node Types.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached when
            making an aggregated query using wildcards.
    """

    @property
    def raw_page(self):
        return self

    node_types: MutableSequence["NodeType"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="NodeType",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetNodeTypeRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.GetNodeType][google.cloud.vmwareengine.v1.VmwareEngine.GetNodeType]

    Attributes:
        name (str):
            Required. The resource name of the node type to retrieve.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-proj/locations/us-west1-a/nodeTypes/standard-72``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Credentials(proto.Message):
    r"""Credentials for a private cloud.

    Attributes:
        username (str):
            Initial username.
        password (str):
            Initial password.
    """

    username: str = proto.Field(
        proto.STRING,
        number=1,
    )
    password: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ShowNsxCredentialsRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ShowNsxCredentials][google.cloud.vmwareengine.v1.VmwareEngine.ShowNsxCredentials]

    Attributes:
        private_cloud (str):
            Required. The resource name of the private cloud to be
            queried for credentials. Resource names are schemeless URIs
            that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
    """

    private_cloud: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ShowVcenterCredentialsRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ShowVcenterCredentials][google.cloud.vmwareengine.v1.VmwareEngine.ShowVcenterCredentials]

    Attributes:
        private_cloud (str):
            Required. The resource name of the private cloud to be
            queried for credentials. Resource names are schemeless URIs
            that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
    """

    private_cloud: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ResetNsxCredentialsRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ResetNsxCredentials][google.cloud.vmwareengine.v1.VmwareEngine.ResetNsxCredentials]

    Attributes:
        private_cloud (str):
            Required. The resource name of the private cloud to reset
            credentials for. Resource names are schemeless URIs that
            follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server guarantees that a request
            doesn't result in creation of duplicate
            commitments for at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    private_cloud: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ResetVcenterCredentialsRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ResetVcenterCredentials][google.cloud.vmwareengine.v1.VmwareEngine.ResetVcenterCredentials]

    Attributes:
        private_cloud (str):
            Required. The resource name of the private cloud to reset
            credentials for. Resource names are schemeless URIs that
            follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1-a/privateClouds/my-cloud``
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server guarantees that a request
            doesn't result in creation of duplicate
            commitments for at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    private_cloud: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListHcxActivationKeysResponse(proto.Message):
    r"""Response message for
    [VmwareEngine.ListHcxActivationKeys][google.cloud.vmwareengine.v1.VmwareEngine.ListHcxActivationKeys]

    Attributes:
        hcx_activation_keys (MutableSequence[google.cloud.vmwareengine_v1.types.HcxActivationKey]):
            List of HCX activation keys.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached when
            making an aggregated query using wildcards.
    """

    @property
    def raw_page(self):
        return self

    hcx_activation_keys: MutableSequence["HcxActivationKey"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="HcxActivationKey",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class HcxActivationKey(proto.Message):
    r"""HCX activation key. A default key is created during private cloud
    provisioning, but this behavior is subject to change and you should
    always verify active keys. Use
    [VmwareEngine.ListHcxActivationKeys][google.cloud.vmwareengine.v1.VmwareEngine.ListHcxActivationKeys]
    to retrieve existing keys and
    [VmwareEngine.CreateHcxActivationKey][google.cloud.vmwareengine.v1.VmwareEngine.CreateHcxActivationKey]
    to create new ones.

    Attributes:
        name (str):
            Output only. The resource name of this HcxActivationKey.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1/privateClouds/my-cloud/hcxActivationKeys/my-key``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of HCX activation
            key.
        state (google.cloud.vmwareengine_v1.types.HcxActivationKey.State):
            Output only. State of HCX activation key.
        activation_key (str):
            Output only. HCX activation key.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
    """

    class State(proto.Enum):
        r"""State of HCX activation key"""
        STATE_UNSPECIFIED = 0
        AVAILABLE = 1
        CONSUMED = 2
        CREATING = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=3,
        enum=State,
    )
    activation_key: str = proto.Field(
        proto.STRING,
        number=4,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListHcxActivationKeysRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ListHcxActivationKeys][google.cloud.vmwareengine.v1.VmwareEngine.ListHcxActivationKeys]

    Attributes:
        parent (str):
            Required. The resource name of the private cloud to be
            queried for HCX activation keys. Resource names are
            schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1/privateClouds/my-cloud``
        page_size (int):
            The maximum number of HCX activation keys to
            return in one page. The service may return fewer
            than this value. The maximum value is coerced to
            1000.
            The default value of this field is 500.
        page_token (str):
            A page token, received from a previous
            ``ListHcxActivationKeys`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListHcxActivationKeys`` must match the call that provided
            the page token.
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


class GetHcxActivationKeyRequest(proto.Message):
    r"""Request message for [VmwareEngine.GetHcxActivationKeys][]

    Attributes:
        name (str):
            Required. The resource name of the HCX activation key to
            retrieve. Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-west1/privateClouds/my-cloud/hcxActivationKeys/my-key``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateHcxActivationKeyRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.CreateHcxActivationKey][google.cloud.vmwareengine.v1.VmwareEngine.CreateHcxActivationKey]

    Attributes:
        parent (str):
            Required. The resource name of the private cloud to create
            the key for. Resource names are schemeless URIs that follow
            the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1/privateClouds/my-cloud``
        hcx_activation_key (google.cloud.vmwareengine_v1.types.HcxActivationKey):
            Required. The initial description of a new
            HCX activation key. When creating a new key,
            this field must be an empty object.
        hcx_activation_key_id (str):
            Required. The user-provided identifier of the
            ``HcxActivationKey`` to be created. This identifier must be
            unique among ``HcxActivationKey`` resources within the
            parent and becomes the final token in the name URI. The
            identifier must meet the following requirements:

            -  Only contains 1-63 alphanumeric characters and hyphens
            -  Begins with an alphabetical character
            -  Ends with a non-hyphen character
            -  Not formatted as a UUID
            -  Complies with `RFC
               1034 <https://datatracker.ietf.org/doc/html/rfc1034>`__
               (section 3.5)
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server guarantees that a request doesn't result
            in creation of duplicate commitments for at
            least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    hcx_activation_key: "HcxActivationKey" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="HcxActivationKey",
    )
    hcx_activation_key_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class Hcx(proto.Message):
    r"""Details about a HCX Cloud Manager appliance.

    Attributes:
        internal_ip (str):
            Internal IP address of the appliance.
        version (str):
            Version of the appliance.
        state (google.cloud.vmwareengine_v1.types.Hcx.State):
            Output only. The state of the appliance.
        fqdn (str):
            Fully qualified domain name of the appliance.
    """

    class State(proto.Enum):
        r"""State of the appliance"""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2

    internal_ip: str = proto.Field(
        proto.STRING,
        number=2,
    )
    version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    fqdn: str = proto.Field(
        proto.STRING,
        number=6,
    )


class Nsx(proto.Message):
    r"""Details about a NSX Manager appliance.

    Attributes:
        internal_ip (str):
            Internal IP address of the appliance.
        version (str):
            Version of the appliance.
        state (google.cloud.vmwareengine_v1.types.Nsx.State):
            Output only. The state of the appliance.
        fqdn (str):
            Fully qualified domain name of the appliance.
    """

    class State(proto.Enum):
        r"""State of the appliance"""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2

    internal_ip: str = proto.Field(
        proto.STRING,
        number=2,
    )
    version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    fqdn: str = proto.Field(
        proto.STRING,
        number=6,
    )


class Vcenter(proto.Message):
    r"""Details about a vCenter Server management appliance.

    Attributes:
        internal_ip (str):
            Internal IP address of the appliance.
        version (str):
            Version of the appliance.
        state (google.cloud.vmwareengine_v1.types.Vcenter.State):
            Output only. The state of the appliance.
        fqdn (str):
            Fully qualified domain name of the appliance.
    """

    class State(proto.Enum):
        r"""State of the appliance"""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CREATING = 2

    internal_ip: str = proto.Field(
        proto.STRING,
        number=2,
    )
    version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    fqdn: str = proto.Field(
        proto.STRING,
        number=6,
    )


class NetworkPolicy(proto.Message):
    r"""Represents a network policy resource. Network policies are
    regional resources. You can use a network policy to enable or
    disable internet access and external IP access. Network policies
    are associated with a VMware Engine network, which might span
    across regions. For a given region, a network policy applies to
    all private clouds in the VMware Engine network associated with
    the policy.

    Attributes:
        name (str):
            Output only. The resource name of this network policy.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1/networkPolicies/my-network-policy``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update time of this
            resource.
        internet_access (google.cloud.vmwareengine_v1.types.NetworkPolicy.NetworkService):
            Network service that allows VMware workloads
            to access the internet.
        external_ip (google.cloud.vmwareengine_v1.types.NetworkPolicy.NetworkService):
            Network service that allows External IP addresses to be
            assigned to VMware workloads. This service can only be
            enabled when ``internet_access`` is also enabled.
        edge_services_cidr (str):
            Required. IP address range in CIDR notation
            used to create internet access and external IP
            access. An RFC 1918 CIDR block, with a "/26"
            prefix, is required. The range cannot overlap
            with any prefixes either in the consumer VPC
            network or in use by the private clouds attached
            to that VPC network.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
        vmware_engine_network (str):
            Optional. The relative resource name of the VMware Engine
            network. Specify the name in the following form:
            ``projects/{project}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
            where ``{project}`` can either be a project number or a
            project ID.
        description (str):
            Optional. User-provided description for this
            network policy.
        vmware_engine_network_canonical (str):
            Output only. The canonical name of the VMware Engine network
            in the form:
            ``projects/{project_number}/locations/{location}/vmwareEngineNetworks/{vmware_engine_network_id}``
    """

    class NetworkService(proto.Message):
        r"""Represents a network service that is managed by a ``NetworkPolicy``
        resource. A network service provides a way to control an aspect of
        external access to VMware workloads. For example, whether the VMware
        workloads in the private clouds governed by a network policy can
        access or be accessed from the internet.

        Attributes:
            enabled (bool):
                True if the service is enabled; false
                otherwise.
            state (google.cloud.vmwareengine_v1.types.NetworkPolicy.NetworkService.State):
                Output only. State of the service. New values
                may be added to this enum when appropriate.
        """

        class State(proto.Enum):
            r"""Enum State defines possible states of a network policy
            controlled service.
            """
            STATE_UNSPECIFIED = 0
            UNPROVISIONED = 1
            RECONCILING = 2
            ACTIVE = 3

        enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        state: "NetworkPolicy.NetworkService.State" = proto.Field(
            proto.ENUM,
            number=2,
            enum="NetworkPolicy.NetworkService.State",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    internet_access: NetworkService = proto.Field(
        proto.MESSAGE,
        number=6,
        message=NetworkService,
    )
    external_ip: NetworkService = proto.Field(
        proto.MESSAGE,
        number=7,
        message=NetworkService,
    )
    edge_services_cidr: str = proto.Field(
        proto.STRING,
        number=9,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=10,
    )
    vmware_engine_network: str = proto.Field(
        proto.STRING,
        number=12,
    )
    description: str = proto.Field(
        proto.STRING,
        number=13,
    )
    vmware_engine_network_canonical: str = proto.Field(
        proto.STRING,
        number=14,
    )


class ListNetworkPoliciesRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ListNetworkPolicies][google.cloud.vmwareengine.v1.VmwareEngine.ListNetworkPolicies]

    Attributes:
        parent (str):
            Required. The resource name of the location (region) to
            query for network policies. Resource names are schemeless
            URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example: ``projects/my-project/locations/us-central1``
        page_size (int):
            The maximum number of network policies to
            return in one page. The service may return fewer
            than this value. The maximum value is coerced to
            1000.
            The default value of this field is 500.
        page_token (str):
            A page token, received from a previous
            ``ListNetworkPolicies`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListNetworkPolicies`` must match the call that provided
            the page token.
        filter (str):
            A filter expression that matches resources returned in the
            response. The expression must specify the field name, a
            comparison operator, and the value that you want to use for
            filtering. The value must be a string, a number, or a
            boolean. The comparison operator must be ``=``, ``!=``,
            ``>``, or ``<``.

            For example, if you are filtering a list of network
            policies, you can exclude the ones named ``example-policy``
            by specifying ``name != "example-policy"``.

            To filter on multiple expressions, provide each separate
            expression within parentheses. For example:

            ::

               (name = "example-policy")
               (createTime > "2021-04-12T08:15:10.40Z")

            By default, each expression is an ``AND`` expression.
            However, you can include ``AND`` and ``OR`` expressions
            explicitly. For example:

            ::

               (name = "example-policy-1") AND
               (createTime > "2021-04-12T08:15:10.40Z") OR
               (name = "example-policy-2")
        order_by (str):
            Sorts list results by a certain order. By default, returned
            results are ordered by ``name`` in ascending order. You can
            also sort results in descending order based on the ``name``
            value using ``orderBy="name desc"``. Currently, only
            ordering by ``name`` is supported.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListNetworkPoliciesResponse(proto.Message):
    r"""Response message for
    [VmwareEngine.ListNetworkPolicies][google.cloud.vmwareengine.v1.VmwareEngine.ListNetworkPolicies]

    Attributes:
        network_policies (MutableSequence[google.cloud.vmwareengine_v1.types.NetworkPolicy]):
            A list of network policies.
        next_page_token (str):
            A token, which can be send as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached when
            making an aggregated query using wildcards.
    """

    @property
    def raw_page(self):
        return self

    network_policies: MutableSequence["NetworkPolicy"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="NetworkPolicy",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetNetworkPolicyRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.GetNetworkPolicy][google.cloud.vmwareengine.v1.VmwareEngine.GetNetworkPolicy]

    Attributes:
        name (str):
            Required. The resource name of the network policy to
            retrieve. Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1/networkPolicies/my-network-policy``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateNetworkPolicyRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.UpdateNetworkPolicy][google.cloud.vmwareengine.v1.VmwareEngine.UpdateNetworkPolicy]

    Attributes:
        network_policy (google.cloud.vmwareengine_v1.types.NetworkPolicy):
            Required. Network policy description.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the ``NetworkPolicy`` resource by the update.
            The fields specified in the ``update_mask`` are relative to
            the resource, not the full request. A field will be
            overwritten if it is in the mask. If the user does not
            provide a mask then all fields will be overwritten.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server guarantees that a request
            doesn't result in creation of duplicate
            commitments for at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    network_policy: "NetworkPolicy" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="NetworkPolicy",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class CreateNetworkPolicyRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.CreateNetworkPolicy][google.cloud.vmwareengine.v1.VmwareEngine.CreateNetworkPolicy]

    Attributes:
        parent (str):
            Required. The resource name of the location (region) to
            create the new network policy in. Resource names are
            schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example: ``projects/my-project/locations/us-central1``
        network_policy_id (str):
            Required. The user-provided identifier of the network policy
            to be created. This identifier must be unique within parent
            ``projects/{my-project}/locations/{us-central1}/networkPolicies``
            and becomes the final token in the name URI. The identifier
            must meet the following requirements:

            -  Only contains 1-63 alphanumeric characters and hyphens
            -  Begins with an alphabetical character
            -  Ends with a non-hyphen character
            -  Not formatted as a UUID
            -  Complies with `RFC
               1034 <https://datatracker.ietf.org/doc/html/rfc1034>`__
               (section 3.5)
        network_policy (google.cloud.vmwareengine_v1.types.NetworkPolicy):
            Required. The network policy configuration to
            use in the request.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server guarantees that a request
            doesn't result in creation of duplicate
            commitments for at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    network_policy_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    network_policy: "NetworkPolicy" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="NetworkPolicy",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class DeleteNetworkPolicyRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.DeleteNetworkPolicy][google.cloud.vmwareengine.v1.VmwareEngine.DeleteNetworkPolicy]

    Attributes:
        name (str):
            Required. The resource name of the network policy to delete.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/us-central1/networkPolicies/my-network-policy``
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server guarantees that a request
            doesn't result in creation of duplicate
            commitments for at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class VmwareEngineNetwork(proto.Message):
    r"""VMware Engine network resource that provides connectivity for
    VMware Engine private clouds.

    Attributes:
        name (str):
            Output only. The resource name of the VMware Engine network.
            Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/global/vmwareEngineNetworks/my-network``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time of this resource.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update time of this
            resource.
        description (str):
            User-provided description for this VMware
            Engine network.
        vpc_networks (MutableSequence[google.cloud.vmwareengine_v1.types.VmwareEngineNetwork.VpcNetwork]):
            Output only. VMware Engine service VPC
            networks that provide connectivity from a
            private cloud to customer projects, the
            internet, and other Google Cloud services.
        state (google.cloud.vmwareengine_v1.types.VmwareEngineNetwork.State):
            Output only. State of the VMware Engine
            network.
        type_ (google.cloud.vmwareengine_v1.types.VmwareEngineNetwork.Type):
            Required. VMware Engine network type.
        uid (str):
            Output only. System-generated unique
            identifier for the resource.
        etag (str):
            Checksum that may be sent on update and
            delete requests to ensure that the user-provided
            value is up to date before the server processes
            a request. The server computes checksums based
            on the value of other fields in the request.
    """

    class State(proto.Enum):
        r"""Enum State defines possible states of VMware Engine network."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        UPDATING = 3
        DELETING = 4

    class Type(proto.Enum):
        r"""Enum Type defines possible types of VMware Engine network."""
        TYPE_UNSPECIFIED = 0
        LEGACY = 1

    class VpcNetwork(proto.Message):
        r"""Represents a VMware Engine VPC network that is managed by a
        VMware Engine network resource.

        Attributes:
            type_ (google.cloud.vmwareengine_v1.types.VmwareEngineNetwork.VpcNetwork.Type):
                Output only. Type of VPC network (INTRANET, INTERNET, or
                GOOGLE_CLOUD)
            network (str):
                Output only. The relative resource name of the service VPC
                network this VMware Engine network is attached to. For
                example: ``projects/123123/global/networks/my-network``
        """

        class Type(proto.Enum):
            r"""Enum Type defines possible types of a VMware Engine network
            controlled service.
            """
            TYPE_UNSPECIFIED = 0
            INTRANET = 1
            INTERNET = 2
            GOOGLE_CLOUD = 3

        type_: "VmwareEngineNetwork.VpcNetwork.Type" = proto.Field(
            proto.ENUM,
            number=1,
            enum="VmwareEngineNetwork.VpcNetwork.Type",
        )
        network: str = proto.Field(
            proto.STRING,
            number=2,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    vpc_networks: MutableSequence[VpcNetwork] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message=VpcNetwork,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=8,
        enum=Type,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=9,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=10,
    )


class CreateVmwareEngineNetworkRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.CreateVmwareEngineNetwork][google.cloud.vmwareengine.v1.VmwareEngine.CreateVmwareEngineNetwork]

    Attributes:
        parent (str):
            Required. The resource name of the location to create the
            new VMware Engine network in. A VMware Engine network of
            type ``LEGACY`` is a regional resource, and a VMware Engine
            network of type ``STANDARD`` is a global resource. Resource
            names are schemeless URIs that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example: ``projects/my-project/locations/global``
        vmware_engine_network_id (str):
            Required. The user-provided identifier of the new VMware
            Engine network. This identifier must be unique among VMware
            Engine network resources within the parent and becomes the
            final token in the name URI. The identifier must meet the
            following requirements:

            -  For networks of type LEGACY, adheres to the format:
               ``{region-id}-default``. Replace ``{region-id}`` with the
               region where you want to create the VMware Engine
               network. For example, "us-west1-default".
            -  Only contains 1-63 alphanumeric characters and hyphens
            -  Begins with an alphabetical character
            -  Ends with a non-hyphen character
            -  Not formatted as a UUID
            -  Complies with `RFC
               1034 <https://datatracker.ietf.org/doc/html/rfc1034>`__
               (section 3.5)
        vmware_engine_network (google.cloud.vmwareengine_v1.types.VmwareEngineNetwork):
            Required. The initial description of the new
            VMware Engine network.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server guarantees that a request
            doesn't result in creation of duplicate
            commitments for at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    vmware_engine_network_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    vmware_engine_network: "VmwareEngineNetwork" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="VmwareEngineNetwork",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateVmwareEngineNetworkRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.UpdateVmwareEngineNetwork][google.cloud.vmwareengine.v1.VmwareEngine.UpdateVmwareEngineNetwork]

    Attributes:
        vmware_engine_network (google.cloud.vmwareengine_v1.types.VmwareEngineNetwork):
            Required. VMware Engine network description.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the VMware Engine network resource by the
            update. The fields specified in the ``update_mask`` are
            relative to the resource, not the full request. A field will
            be overwritten if it is in the mask. If the user does not
            provide a mask then all fields will be overwritten. Only the
            following fields can be updated: ``description``.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server guarantees that a request
            doesn't result in creation of duplicate
            commitments for at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    vmware_engine_network: "VmwareEngineNetwork" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="VmwareEngineNetwork",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteVmwareEngineNetworkRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.DeleteVmwareEngineNetwork][google.cloud.vmwareengine.v1.VmwareEngine.DeleteVmwareEngineNetwork]

    Attributes:
        name (str):
            Required. The resource name of the VMware Engine network to
            be deleted. Resource names are schemeless URIs that follow
            the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/global/vmwareEngineNetworks/my-network``
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server guarantees that a request
            doesn't result in creation of duplicate
            commitments for at least 60 minutes.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        etag (str):
            Optional. Checksum used to ensure that the user-provided
            value is up to date before the server processes the request.
            The server compares provided checksum with the current
            checksum of the resource. If the user-provided value is out
            of date, this request returns an ``ABORTED`` error.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GetVmwareEngineNetworkRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.GetVmwareEngineNetwork][google.cloud.vmwareengine.v1.VmwareEngine.GetVmwareEngineNetwork]

    Attributes:
        name (str):
            Required. The resource name of the VMware Engine network to
            retrieve. Resource names are schemeless URIs that follow the
            conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example:
            ``projects/my-project/locations/global/vmwareEngineNetworks/my-network``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListVmwareEngineNetworksRequest(proto.Message):
    r"""Request message for
    [VmwareEngine.ListVmwareEngineNetworks][google.cloud.vmwareengine.v1.VmwareEngine.ListVmwareEngineNetworks]

    Attributes:
        parent (str):
            Required. The resource name of the location to query for
            VMware Engine networks. Resource names are schemeless URIs
            that follow the conventions in
            https://cloud.google.com/apis/design/resource_names. For
            example: ``projects/my-project/locations/global``
        page_size (int):
            The maximum number of results to return in
            one page. The maximum value is coerced to 1000.
            The default value of this field is 500.
        page_token (str):
            A page token, received from a previous
            ``ListVmwareEngineNetworks`` call. Provide this to retrieve
            the subsequent page.

            When paginating, all other parameters provided to
            ``ListVmwareEngineNetworks`` must match the call that
            provided the page token.
        filter (str):
            A filter expression that matches resources returned in the
            response. The expression must specify the field name, a
            comparison operator, and the value that you want to use for
            filtering. The value must be a string, a number, or a
            boolean. The comparison operator must be ``=``, ``!=``,
            ``>``, or ``<``.

            For example, if you are filtering a list of network
            peerings, you can exclude the ones named ``example-network``
            by specifying ``name != "example-network"``.

            To filter on multiple expressions, provide each separate
            expression within parentheses. For example:

            ::

               (name = "example-network")
               (createTime > "2021-04-12T08:15:10.40Z")

            By default, each expression is an ``AND`` expression.
            However, you can include ``AND`` and ``OR`` expressions
            explicitly. For example:

            ::

               (name = "example-network-1") AND
               (createTime > "2021-04-12T08:15:10.40Z") OR
               (name = "example-network-2")
        order_by (str):
            Sorts list results by a certain order. By default, returned
            results are ordered by ``name`` in ascending order. You can
            also sort results in descending order based on the ``name``
            value using ``orderBy="name desc"``. Currently, only
            ordering by ``name`` is supported.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListVmwareEngineNetworksResponse(proto.Message):
    r"""Response message for
    [VmwareEngine.ListVmwareEngineNetworks][google.cloud.vmwareengine.v1.VmwareEngine.ListVmwareEngineNetworks]

    Attributes:
        vmware_engine_networks (MutableSequence[google.cloud.vmwareengine_v1.types.VmwareEngineNetwork]):
            A list of VMware Engine networks.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Unreachable resources.
    """

    @property
    def raw_page(self):
        return self

    vmware_engine_networks: MutableSequence[
        "VmwareEngineNetwork"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="VmwareEngineNetwork",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
