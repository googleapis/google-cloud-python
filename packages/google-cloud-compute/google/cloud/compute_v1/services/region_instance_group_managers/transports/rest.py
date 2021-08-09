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

from .base import RegionInstanceGroupManagersTransport, DEFAULT_CLIENT_INFO


class RegionInstanceGroupManagersRestTransport(RegionInstanceGroupManagersTransport):
    """REST backend transport for RegionInstanceGroupManagers.

    The RegionInstanceGroupManagers API.

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

    def abandon_instances(
        self,
        request: compute.AbandonInstancesRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the abandon instances method over HTTP.

        Args:
            request (~.compute.AbandonInstancesRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.AbandonInstances.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagersAbandonInstancesRequest.to_json(
            request.region_instance_group_managers_abandon_instances_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/abandonInstances".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.AbandonInstancesRegionInstanceGroupManagerRequest.request_id
            in request
        ):
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

    def apply_updates_to_instances(
        self,
        request: compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the apply updates to
        instances method over HTTP.

        Args:
            request (~.compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.ApplyUpdatesToInstances.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagersApplyUpdatesRequest.to_json(
            request.region_instance_group_managers_apply_updates_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/applyUpdatesToInstances".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}

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

    def create_instances(
        self,
        request: compute.CreateInstancesRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the create instances method over HTTP.

        Args:
            request (~.compute.CreateInstancesRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.CreateInstances.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagersCreateInstancesRequest.to_json(
            request.region_instance_group_managers_create_instances_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/createInstances".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.CreateInstancesRegionInstanceGroupManagerRequest.request_id
            in request
        ):
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

    def delete(
        self,
        request: compute.DeleteRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete method over HTTP.

        Args:
            request (~.compute.DeleteRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.Delete. See
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

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.DeleteRegionInstanceGroupManagerRequest.request_id in request:
            query_params["requestId"] = request.request_id

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.delete(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def delete_instances(
        self,
        request: compute.DeleteInstancesRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete instances method over HTTP.

        Args:
            request (~.compute.DeleteInstancesRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.DeleteInstances.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagersDeleteInstancesRequest.to_json(
            request.region_instance_group_managers_delete_instances_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/deleteInstances".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.DeleteInstancesRegionInstanceGroupManagerRequest.request_id
            in request
        ):
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

    def delete_per_instance_configs(
        self,
        request: compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete per instance
        configs method over HTTP.

        Args:
            request (~.compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.DeletePerInstanceConfigs.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagerDeleteInstanceConfigReq.to_json(
            request.region_instance_group_manager_delete_instance_config_req_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/deletePerInstanceConfigs".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}

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

    def get(
        self,
        request: compute.GetRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.InstanceGroupManager:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.Get. See the
                method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.InstanceGroupManager:
                Represents a Managed Instance Group resource.

                An instance group is a collection of VM instances that
                you can manage as a single entity. For more information,
                read Instance groups.

                For zonal Managed Instance Group, use the
                instanceGroupManagers resource.

                For regional Managed Instance Group, use the
                regionInstanceGroupManagers resource. (== resource_for
                {$api_version}.instanceGroupManagers ==) (==
                resource_for {$api_version}.regionInstanceGroupManagers
                ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
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
        return compute.InstanceGroupManager.from_json(
            response.content, ignore_unknown_fields=True
        )

    def insert(
        self,
        request: compute.InsertRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the insert method over HTTP.

        Args:
            request (~.compute.InsertRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.Insert. See
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
        body = compute.InstanceGroupManager.to_json(
            request.instance_group_manager_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers".format(
            host=self._host, project=request.project, region=request.region,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.InsertRegionInstanceGroupManagerRequest.request_id in request:
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

    def list(
        self,
        request: compute.ListRegionInstanceGroupManagersRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.RegionInstanceGroupManagerList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListRegionInstanceGroupManagersRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.List. See
                the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.RegionInstanceGroupManagerList:
                Contains a list of managed instance
                groups.

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers".format(
            host=self._host, project=request.project, region=request.region,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListRegionInstanceGroupManagersRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListRegionInstanceGroupManagersRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListRegionInstanceGroupManagersRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListRegionInstanceGroupManagersRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if (
            compute.ListRegionInstanceGroupManagersRequest.return_partial_success
            in request
        ):
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
        return compute.RegionInstanceGroupManagerList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def list_errors(
        self,
        request: compute.ListErrorsRegionInstanceGroupManagersRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.RegionInstanceGroupManagersListErrorsResponse:
        r"""Call the list errors method over HTTP.

        Args:
            request (~.compute.ListErrorsRegionInstanceGroupManagersRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.ListErrors.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.RegionInstanceGroupManagersListErrorsResponse:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/listErrors".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListErrorsRegionInstanceGroupManagersRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListErrorsRegionInstanceGroupManagersRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListErrorsRegionInstanceGroupManagersRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListErrorsRegionInstanceGroupManagersRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if (
            compute.ListErrorsRegionInstanceGroupManagersRequest.return_partial_success
            in request
        ):
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
        return compute.RegionInstanceGroupManagersListErrorsResponse.from_json(
            response.content, ignore_unknown_fields=True
        )

    def list_managed_instances(
        self,
        request: compute.ListManagedInstancesRegionInstanceGroupManagersRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.RegionInstanceGroupManagersListInstancesResponse:
        r"""Call the list managed instances method over HTTP.

        Args:
            request (~.compute.ListManagedInstancesRegionInstanceGroupManagersRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.ListManagedInstances.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.RegionInstanceGroupManagersListInstancesResponse:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/listManagedInstances".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.ListManagedInstancesRegionInstanceGroupManagersRequest.filter
            in request
        ):
            query_params["filter"] = request.filter
        if (
            compute.ListManagedInstancesRegionInstanceGroupManagersRequest.max_results
            in request
        ):
            query_params["maxResults"] = request.max_results
        if (
            compute.ListManagedInstancesRegionInstanceGroupManagersRequest.order_by
            in request
        ):
            query_params["orderBy"] = request.order_by
        if (
            compute.ListManagedInstancesRegionInstanceGroupManagersRequest.page_token
            in request
        ):
            query_params["pageToken"] = request.page_token
        if (
            compute.ListManagedInstancesRegionInstanceGroupManagersRequest.return_partial_success
            in request
        ):
            query_params["returnPartialSuccess"] = request.return_partial_success

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.post(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.RegionInstanceGroupManagersListInstancesResponse.from_json(
            response.content, ignore_unknown_fields=True
        )

    def list_per_instance_configs(
        self,
        request: compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.RegionInstanceGroupManagersListInstanceConfigsResp:
        r"""Call the list per instance configs method over HTTP.

        Args:
            request (~.compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.ListPerInstanceConfigs.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.RegionInstanceGroupManagersListInstanceConfigsResp:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/listPerInstanceConfigs".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest.filter
            in request
        ):
            query_params["filter"] = request.filter
        if (
            compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest.max_results
            in request
        ):
            query_params["maxResults"] = request.max_results
        if (
            compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest.order_by
            in request
        ):
            query_params["orderBy"] = request.order_by
        if (
            compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest.page_token
            in request
        ):
            query_params["pageToken"] = request.page_token
        if (
            compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest.return_partial_success
            in request
        ):
            query_params["returnPartialSuccess"] = request.return_partial_success

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.post(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.RegionInstanceGroupManagersListInstanceConfigsResp.from_json(
            response.content, ignore_unknown_fields=True
        )

    def patch(
        self,
        request: compute.PatchRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the patch method over HTTP.

        Args:
            request (~.compute.PatchRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.Patch. See
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
        body = compute.InstanceGroupManager.to_json(
            request.instance_group_manager_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.PatchRegionInstanceGroupManagerRequest.request_id in request:
            query_params["requestId"] = request.request_id

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.patch(
            url, headers=headers, params=query_params, data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def patch_per_instance_configs(
        self,
        request: compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the patch per instance
        configs method over HTTP.

        Args:
            request (~.compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.PatchPerInstanceConfigs.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagerPatchInstanceConfigReq.to_json(
            request.region_instance_group_manager_patch_instance_config_req_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/patchPerInstanceConfigs".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest.request_id
            in request
        ):
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

    def recreate_instances(
        self,
        request: compute.RecreateInstancesRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the recreate instances method over HTTP.

        Args:
            request (~.compute.RecreateInstancesRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.RecreateInstances.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagersRecreateRequest.to_json(
            request.region_instance_group_managers_recreate_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/recreateInstances".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.RecreateInstancesRegionInstanceGroupManagerRequest.request_id
            in request
        ):
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

    def resize(
        self,
        request: compute.ResizeRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the resize method over HTTP.

        Args:
            request (~.compute.ResizeRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.Resize. See
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

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/resize".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ResizeRegionInstanceGroupManagerRequest.request_id in request:
            query_params["requestId"] = request.request_id
        query_params["size"] = request.size

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.post(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def set_instance_template(
        self,
        request: compute.SetInstanceTemplateRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the set instance template method over HTTP.

        Args:
            request (~.compute.SetInstanceTemplateRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.SetInstanceTemplate.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagersSetTemplateRequest.to_json(
            request.region_instance_group_managers_set_template_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/setInstanceTemplate".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.SetInstanceTemplateRegionInstanceGroupManagerRequest.request_id
            in request
        ):
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

    def set_target_pools(
        self,
        request: compute.SetTargetPoolsRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the set target pools method over HTTP.

        Args:
            request (~.compute.SetTargetPoolsRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.SetTargetPools.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagersSetTargetPoolsRequest.to_json(
            request.region_instance_group_managers_set_target_pools_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/setTargetPools".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.SetTargetPoolsRegionInstanceGroupManagerRequest.request_id
            in request
        ):
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

    def update_per_instance_configs(
        self,
        request: compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the update per instance
        configs method over HTTP.

        Args:
            request (~.compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest):
                The request object. A request message for
                RegionInstanceGroupManagers.UpdatePerInstanceConfigs.
                See the method description for details.

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
        body = compute.RegionInstanceGroupManagerUpdateInstanceConfigReq.to_json(
            request.region_instance_group_manager_update_instance_config_req_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/updatePerInstanceConfigs".format(
            host=self._host,
            project=request.project,
            region=request.region,
            instance_group_manager=request.instance_group_manager,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if (
            compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest.request_id
            in request
        ):
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


__all__ = ("RegionInstanceGroupManagersRestTransport",)
