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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.gkehub_v1.types import feature, membership

__protobuf__ = proto.module(
    package="google.cloud.gkehub.v1",
    manifest={
        "ListMembershipsRequest",
        "ListMembershipsResponse",
        "GetMembershipRequest",
        "CreateMembershipRequest",
        "DeleteMembershipRequest",
        "UpdateMembershipRequest",
        "GenerateConnectManifestRequest",
        "GenerateConnectManifestResponse",
        "ConnectAgentResource",
        "TypeMeta",
        "ListFeaturesRequest",
        "ListFeaturesResponse",
        "GetFeatureRequest",
        "CreateFeatureRequest",
        "DeleteFeatureRequest",
        "UpdateFeatureRequest",
        "OperationMetadata",
    },
)


class ListMembershipsRequest(proto.Message):
    r"""Request message for ``GkeHub.ListMemberships`` method.

    Attributes:
        parent (str):
            Required. The parent (project and location) where the
            Memberships will be listed. Specified in the format
            ``projects/*/locations/*``. ``projects/*/locations/-`` list
            memberships in all the regions.
        page_size (int):
            Optional. When requesting a 'page' of resources,
            ``page_size`` specifies number of resources to return. If
            unspecified or set to 0, all resources will be returned.
        page_token (str):
            Optional. Token returned by previous call to
            ``ListMemberships`` which specifies the position in the list
            from where to continue listing the resources.
        filter (str):
            Optional. Lists Memberships that match the filter
            expression, following the syntax outlined in
            https://google.aip.dev/160.

            Examples:

            -  Name is ``bar`` in project ``foo-proj`` and location
               ``global``:

               name =
               "projects/foo-proj/locations/global/membership/bar"

            -  Memberships that have a label called ``foo``:

               labels.foo:\*

            -  Memberships that have a label called ``foo`` whose value
               is ``bar``:

               labels.foo = bar

            -  Memberships in the CREATING state:

               state = CREATING
        order_by (str):
            Optional. One or more fields to compare and
            use to sort the output. See
            https://google.aip.dev/132#ordering.
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


class ListMembershipsResponse(proto.Message):
    r"""Response message for the ``GkeHub.ListMemberships`` method.

    Attributes:
        resources (MutableSequence[google.cloud.gkehub_v1.types.Membership]):
            The list of matching Memberships.
        next_page_token (str):
            A token to request the next page of resources from the
            ``ListMemberships`` method. The value of an empty string
            means that there are no more resources to return.
        unreachable (MutableSequence[str]):
            List of locations that could not be reached
            while fetching this list.
    """

    @property
    def raw_page(self):
        return self

    resources: MutableSequence[membership.Membership] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=membership.Membership,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetMembershipRequest(proto.Message):
    r"""Request message for ``GkeHub.GetMembership`` method.

    Attributes:
        name (str):
            Required. The Membership resource name in the format
            ``projects/*/locations/*/memberships/*``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateMembershipRequest(proto.Message):
    r"""Request message for the ``GkeHub.CreateMembership`` method.

    Attributes:
        parent (str):
            Required. The parent (project and location) where the
            Memberships will be created. Specified in the format
            ``projects/*/locations/*``.
        membership_id (str):
            Required. Client chosen ID for the membership.
            ``membership_id`` must be a valid RFC 1123 compliant DNS
            label:

            1. At most 63 characters in length
            2. It must consist of lower case alphanumeric characters or
               ``-``
            3. It must start and end with an alphanumeric character

            Which can be expressed as the regex:
            ``[a-z0-9]([-a-z0-9]*[a-z0-9])?``, with a maximum length of
            63 characters.
        resource (google.cloud.gkehub_v1.types.Membership):
            Required. The membership to create.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.

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
    membership_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    resource: membership.Membership = proto.Field(
        proto.MESSAGE,
        number=3,
        message=membership.Membership,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class DeleteMembershipRequest(proto.Message):
    r"""Request message for ``GkeHub.DeleteMembership`` method.

    Attributes:
        name (str):
            Required. The Membership resource name in the format
            ``projects/*/locations/*/memberships/*``.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.

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
        force (bool):
            Optional. If set to true, any subresource
            from this Membership will also be deleted.
            Otherwise, the request will only work if the
            Membership has no subresource.
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


class UpdateMembershipRequest(proto.Message):
    r"""Request message for ``GkeHub.UpdateMembership`` method.

    Attributes:
        name (str):
            Required. The Membership resource name in the format
            ``projects/*/locations/*/memberships/*``.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update.
        resource (google.cloud.gkehub_v1.types.Membership):
            Required. Only fields specified in update_mask are updated.
            If you specify a field in the update_mask but don't specify
            its value here that field will be deleted. If you are
            updating a map field, set the value of a key to null or
            empty string to delete the key from the map. It's not
            possible to update a key's value to the empty string. If you
            specify the update_mask to be a special path "*", fully
            replaces all user-modifiable fields to match ``resource``.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.

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
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    resource: membership.Membership = proto.Field(
        proto.MESSAGE,
        number=3,
        message=membership.Membership,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class GenerateConnectManifestRequest(proto.Message):
    r"""Request message for ``GkeHub.GenerateConnectManifest`` method. .

    Attributes:
        name (str):
            Required. The Membership resource name the Agent will
            associate with, in the format
            ``projects/*/locations/*/memberships/*``.
        namespace (str):
            Optional. Namespace for GKE Connect agent resources.
            Defaults to ``gke-connect``.

            The Connect Agent is authorized automatically when run in
            the default namespace. Otherwise, explicit authorization
            must be granted with an additional IAM binding.
        proxy (bytes):
            Optional. URI of a proxy if connectivity from the agent to
            gkeconnect.googleapis.com requires the use of a proxy.
            Format must be in the form ``http(s)://{proxy_address}``,
            depending on the HTTP/HTTPS protocol supported by the proxy.
            This will direct the connect agent's outbound traffic
            through a HTTP(S) proxy.
        version (str):
            Optional. The Connect agent version to use.
            Defaults to the most current version.
        is_upgrade (bool):
            Optional. If true, generate the resources for
            upgrade only. Some resources generated only for
            installation (e.g. secrets) will be excluded.
        registry (str):
            Optional. The registry to fetch the connect
            agent image from. Defaults to gcr.io/gkeconnect.
        image_pull_secret_content (bytes):
            Optional. The image pull secret content for
            the registry, if not public.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    namespace: str = proto.Field(
        proto.STRING,
        number=2,
    )
    proxy: bytes = proto.Field(
        proto.BYTES,
        number=3,
    )
    version: str = proto.Field(
        proto.STRING,
        number=4,
    )
    is_upgrade: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    registry: str = proto.Field(
        proto.STRING,
        number=6,
    )
    image_pull_secret_content: bytes = proto.Field(
        proto.BYTES,
        number=7,
    )


class GenerateConnectManifestResponse(proto.Message):
    r"""GenerateConnectManifestResponse contains manifest information
    for installing/upgrading a Connect agent.

    Attributes:
        manifest (MutableSequence[google.cloud.gkehub_v1.types.ConnectAgentResource]):
            The ordered list of Kubernetes resources that
            need to be applied to the cluster for GKE
            Connect agent installation/upgrade.
    """

    manifest: MutableSequence["ConnectAgentResource"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ConnectAgentResource",
    )


class ConnectAgentResource(proto.Message):
    r"""ConnectAgentResource represents a Kubernetes resource
    manifest for Connect Agent deployment.

    Attributes:
        type_ (google.cloud.gkehub_v1.types.TypeMeta):
            Kubernetes type of the resource.
        manifest (str):
            YAML manifest of the resource.
    """

    type_: "TypeMeta" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="TypeMeta",
    )
    manifest: str = proto.Field(
        proto.STRING,
        number=2,
    )


class TypeMeta(proto.Message):
    r"""TypeMeta is the type information needed for content
    unmarshalling of Kubernetes resources in the manifest.

    Attributes:
        kind (str):
            Kind of the resource (e.g. Deployment).
        api_version (str):
            APIVersion of the resource (e.g. v1).
    """

    kind: str = proto.Field(
        proto.STRING,
        number=1,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListFeaturesRequest(proto.Message):
    r"""Request message for ``GkeHub.ListFeatures`` method.

    Attributes:
        parent (str):
            Required. The parent (project and location) where the
            Features will be listed. Specified in the format
            ``projects/*/locations/*``.
        page_size (int):
            When requesting a 'page' of resources, ``page_size``
            specifies number of resources to return. If unspecified or
            set to 0, all resources will be returned.
        page_token (str):
            Token returned by previous call to ``ListFeatures`` which
            specifies the position in the list from where to continue
            listing the resources.
        filter (str):
            Lists Features that match the filter expression, following
            the syntax outlined in https://google.aip.dev/160.

            Examples:

            -  Feature with the name "servicemesh" in project
               "foo-proj":

               name =
               "projects/foo-proj/locations/global/features/servicemesh"

            -  Features that have a label called ``foo``:

               labels.foo:\*

            -  Features that have a label called ``foo`` whose value is
               ``bar``:

               labels.foo = bar
        order_by (str):
            One or more fields to compare and use to sort
            the output. See
            https://google.aip.dev/132#ordering.
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


class ListFeaturesResponse(proto.Message):
    r"""Response message for the ``GkeHub.ListFeatures`` method.

    Attributes:
        resources (MutableSequence[google.cloud.gkehub_v1.types.Feature]):
            The list of matching Features
        next_page_token (str):
            A token to request the next page of resources from the
            ``ListFeatures`` method. The value of an empty string means
            that there are no more resources to return.
    """

    @property
    def raw_page(self):
        return self

    resources: MutableSequence[feature.Feature] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=feature.Feature,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetFeatureRequest(proto.Message):
    r"""Request message for ``GkeHub.GetFeature`` method.

    Attributes:
        name (str):
            Required. The Feature resource name in the format
            ``projects/*/locations/*/features/*``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateFeatureRequest(proto.Message):
    r"""Request message for the ``GkeHub.CreateFeature`` method.

    Attributes:
        parent (str):
            Required. The parent (project and location) where the
            Feature will be created. Specified in the format
            ``projects/*/locations/*``.
        feature_id (str):
            The ID of the feature to create.
        resource (google.cloud.gkehub_v1.types.Feature):
            The Feature resource to create.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.

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
    feature_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    resource: feature.Feature = proto.Field(
        proto.MESSAGE,
        number=3,
        message=feature.Feature,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class DeleteFeatureRequest(proto.Message):
    r"""Request message for ``GkeHub.DeleteFeature`` method.

    Attributes:
        name (str):
            Required. The Feature resource name in the format
            ``projects/*/locations/*/features/*``.
        force (bool):
            If set to true, the delete will ignore any outstanding
            resources for this Feature (that is,
            ``FeatureState.has_resources`` is set to true). These
            resources will NOT be cleaned up or modified in any way.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.

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
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateFeatureRequest(proto.Message):
    r"""Request message for ``GkeHub.UpdateFeature`` method.

    Attributes:
        name (str):
            Required. The Feature resource name in the format
            ``projects/*/locations/*/features/*``.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Mask of fields to update.
        resource (google.cloud.gkehub_v1.types.Feature):
            Only fields specified in update_mask are updated. If you
            specify a field in the update_mask but don't specify its
            value here that field will be deleted. If you are updating a
            map field, set the value of a key to null or empty string to
            delete the key from the map. It's not possible to update a
            key's value to the empty string. If you specify the
            update_mask to be a special path "*", fully replaces all
            user-modifiable fields to match ``resource``.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.

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
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    resource: feature.Feature = proto.Field(
        proto.MESSAGE,
        number=3,
        message=feature.Feature,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
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
        status_detail (str):
            Output only. Human-readable status of the
            operation, if any.
        cancel_requested (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have
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
    status_detail: str = proto.Field(
        proto.STRING,
        number=5,
    )
    cancel_requested: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
