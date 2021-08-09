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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import gapic_v1  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.auth.transport.requests import AuthorizedSession

from google.cloud.compute_v1.types import compute

from .base import RegionInstanceGroupsTransport, DEFAULT_CLIENT_INFO


class RegionInstanceGroupsRestTransport(RegionInstanceGroupsTransport):
    """REST backend transport for RegionInstanceGroups.

    The RegionInstanceGroups API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._prep_wrapped_messages(client_info)

    def get(
        self,
        request: compute.GetRegionInstanceGroupRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.InstanceGroup:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetRegionInstanceGroupRequest):
                The request object. A request message for
                RegionInstanceGroups.Get. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.InstanceGroup:
                Represents an Instance Group resource.

                Instance Groups can be used to configure a target for
                load balancing.

                Instance groups can either be managed or unmanaged.

                To create managed instance groups, use the
                instanceGroupManager or regionInstanceGroupManager
                resource instead.

                Use zonal unmanaged instance groups if you need to apply
                load balancing to groups of heterogeneous instances or
                if you need to manage the instances yourself. You cannot
                create regional unmanaged instance groups.

                For more information, read Instance groups.

                (== resource_for {$api_version}.instanceGroups ==) (==
                resource_for {$api_version}.regionInstanceGroups ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroups/{instance_group}".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group=request.instance_group,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.get(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.InstanceGroup.from_json(
            response.content, ignore_unknown_fields=True
        )

    def list(
        self,
        request: compute.ListRegionInstanceGroupsRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.RegionInstanceGroupList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListRegionInstanceGroupsRequest):
                The request object. A request message for
                RegionInstanceGroups.List. See the
                method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.RegionInstanceGroupList:
                Contains a list of InstanceGroup
                resources.

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroups".format(
            host=self._host, project=request.project, region=request.region,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListRegionInstanceGroupsRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListRegionInstanceGroupsRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListRegionInstanceGroupsRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListRegionInstanceGroupsRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.ListRegionInstanceGroupsRequest.return_partial_success in request:
            query_params["returnPartialSuccess"] = request.return_partial_success

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.get(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.RegionInstanceGroupList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def list_instances(
        self,
        request: compute.ListInstancesRegionInstanceGroupsRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.RegionInstanceGroupsListInstances:
        r"""Call the list instances method over HTTP.

        Args:
            request (~.compute.ListInstancesRegionInstanceGroupsRequest):
                The request object. A request message for
                RegionInstanceGroups.ListInstances. See
                the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.RegionInstanceGroupsListInstances:

        """

        # Jsonify the request body
        body = compute.RegionInstanceGroupsListInstancesRequest.to_json(
            request.region_instance_groups_list_instances_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroups/{instance_group}/listInstances".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group=request.instance_group,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListInstancesRegionInstanceGroupsRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListInstancesRegionInstanceGroupsRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListInstancesRegionInstanceGroupsRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListInstancesRegionInstanceGroupsRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if (
            compute.ListInstancesRegionInstanceGroupsRequest.return_partial_success
            in request
        ):
            query_params["returnPartialSuccess"] = request.return_partial_success

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.post(
            url, headers=headers, params=query_params, data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.RegionInstanceGroupsListInstances.from_json(
            response.content, ignore_unknown_fields=True
        )

    def set_named_ports(
        self,
        request: compute.SetNamedPortsRegionInstanceGroupRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the set named ports method over HTTP.

        Args:
            request (~.compute.SetNamedPortsRegionInstanceGroupRequest):
                The request object. A request message for
                RegionInstanceGroups.SetNamedPorts. See
                the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource.

                Google Compute Engine has three Operation resources:

                -  `Global </compute/docs/reference/rest/{$api_version}/globalOperations>`__
                   \*
                   `Regional </compute/docs/reference/rest/{$api_version}/regionOperations>`__
                   \*
                   `Zonal </compute/docs/reference/rest/{$api_version}/zoneOperations>`__

                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses.

                Operations can be global, regional or zonal.

                -  For global operations, use the ``globalOperations``
                   resource.
                -  For regional operations, use the ``regionOperations``
                   resource.
                -  For zonal operations, use the ``zonalOperations``
                   resource.

                For more information, read Global, Regional, and Zonal
                Resources. (== resource_for
                {$api_version}.globalOperations ==) (== resource_for
                {$api_version}.regionOperations ==) (== resource_for
                {$api_version}.zoneOperations ==)

        """

        # Jsonify the request body
        body = compute.RegionInstanceGroupsSetNamedPortsRequest.to_json(
            request.region_instance_groups_set_named_ports_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroups/{instance_group}/setNamedPorts".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group=request.instance_group,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.SetNamedPortsRegionInstanceGroupRequest.request_id in request:
            query_params["requestId"] = request.request_id

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.post(
            url, headers=headers, params=query_params, data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)


__all__ = ("RegionInstanceGroupsRestTransport",)
