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

from .base import ProjectsTransport, DEFAULT_CLIENT_INFO


class ProjectsRestTransport(ProjectsTransport):
    """REST backend transport for Projects.

    The Projects API.

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

    def disable_xpn_host(
        self,
        request: compute.DisableXpnHostProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the disable xpn host method over HTTP.

        Args:
            request (~.compute.DisableXpnHostProjectRequest):
                The request object. A request message for
                Projects.DisableXpnHost. See the method
                description for details.

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
        url = "https://{host}/compute/v1/projects/{project}/disableXpnHost".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.DisableXpnHostProjectRequest.request_id in request:
            query_params["requestId"] = request.request_id

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

    def disable_xpn_resource(
        self,
        request: compute.DisableXpnResourceProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the disable xpn resource method over HTTP.

        Args:
            request (~.compute.DisableXpnResourceProjectRequest):
                The request object. A request message for
                Projects.DisableXpnResource. See the
                method description for details.

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
        body = compute.ProjectsDisableXpnResourceRequest.to_json(
            request.projects_disable_xpn_resource_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/disableXpnResource".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.DisableXpnResourceProjectRequest.request_id in request:
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

    def enable_xpn_host(
        self,
        request: compute.EnableXpnHostProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the enable xpn host method over HTTP.

        Args:
            request (~.compute.EnableXpnHostProjectRequest):
                The request object. A request message for
                Projects.EnableXpnHost. See the method
                description for details.

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
        url = "https://{host}/compute/v1/projects/{project}/enableXpnHost".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.EnableXpnHostProjectRequest.request_id in request:
            query_params["requestId"] = request.request_id

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

    def enable_xpn_resource(
        self,
        request: compute.EnableXpnResourceProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the enable xpn resource method over HTTP.

        Args:
            request (~.compute.EnableXpnResourceProjectRequest):
                The request object. A request message for
                Projects.EnableXpnResource. See the
                method description for details.

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
        body = compute.ProjectsEnableXpnResourceRequest.to_json(
            request.projects_enable_xpn_resource_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/enableXpnResource".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.EnableXpnResourceProjectRequest.request_id in request:
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

    def get(
        self,
        request: compute.GetProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Project:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetProjectRequest):
                The request object. A request message for Projects.Get.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Project:
                Represents a Project resource.

                A project is used to organize resources in a Google
                Cloud Platform environment. For more information, read
                about the Resource Hierarchy. (== resource_for
                {$api_version}.projects ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}".format(
            host=self._host, project=request.project,
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
        return compute.Project.from_json(response.content, ignore_unknown_fields=True)

    def get_xpn_host(
        self,
        request: compute.GetXpnHostProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Project:
        r"""Call the get xpn host method over HTTP.

        Args:
            request (~.compute.GetXpnHostProjectRequest):
                The request object. A request message for
                Projects.GetXpnHost. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Project:
                Represents a Project resource.

                A project is used to organize resources in a Google
                Cloud Platform environment. For more information, read
                about the Resource Hierarchy. (== resource_for
                {$api_version}.projects ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/getXpnHost".format(
            host=self._host, project=request.project,
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
        return compute.Project.from_json(response.content, ignore_unknown_fields=True)

    def get_xpn_resources(
        self,
        request: compute.GetXpnResourcesProjectsRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.ProjectsGetXpnResources:
        r"""Call the get xpn resources method over HTTP.

        Args:
            request (~.compute.GetXpnResourcesProjectsRequest):
                The request object. A request message for
                Projects.GetXpnResources. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.ProjectsGetXpnResources:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/getXpnResources".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.GetXpnResourcesProjectsRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.GetXpnResourcesProjectsRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.GetXpnResourcesProjectsRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.GetXpnResourcesProjectsRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.GetXpnResourcesProjectsRequest.return_partial_success in request:
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
        return compute.ProjectsGetXpnResources.from_json(
            response.content, ignore_unknown_fields=True
        )

    def list_xpn_hosts(
        self,
        request: compute.ListXpnHostsProjectsRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.XpnHostList:
        r"""Call the list xpn hosts method over HTTP.

        Args:
            request (~.compute.ListXpnHostsProjectsRequest):
                The request object. A request message for
                Projects.ListXpnHosts. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.XpnHostList:

        """

        # Jsonify the request body
        body = compute.ProjectsListXpnHostsRequest.to_json(
            request.projects_list_xpn_hosts_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/listXpnHosts".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListXpnHostsProjectsRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListXpnHostsProjectsRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListXpnHostsProjectsRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListXpnHostsProjectsRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.ListXpnHostsProjectsRequest.return_partial_success in request:
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
        return compute.XpnHostList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def move_disk(
        self,
        request: compute.MoveDiskProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the move disk method over HTTP.

        Args:
            request (~.compute.MoveDiskProjectRequest):
                The request object. A request message for
                Projects.MoveDisk. See the method
                description for details.

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
        body = compute.DiskMoveRequest.to_json(
            request.disk_move_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/moveDisk".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.MoveDiskProjectRequest.request_id in request:
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

    def move_instance(
        self,
        request: compute.MoveInstanceProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the move instance method over HTTP.

        Args:
            request (~.compute.MoveInstanceProjectRequest):
                The request object. A request message for
                Projects.MoveInstance. See the method
                description for details.

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
        body = compute.InstanceMoveRequest.to_json(
            request.instance_move_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/moveInstance".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.MoveInstanceProjectRequest.request_id in request:
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

    def set_common_instance_metadata(
        self,
        request: compute.SetCommonInstanceMetadataProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the set common instance
        metadata method over HTTP.

        Args:
            request (~.compute.SetCommonInstanceMetadataProjectRequest):
                The request object. A request message for
                Projects.SetCommonInstanceMetadata. See
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
        body = compute.Metadata.to_json(
            request.metadata_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/setCommonInstanceMetadata".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.SetCommonInstanceMetadataProjectRequest.request_id in request:
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

    def set_default_network_tier(
        self,
        request: compute.SetDefaultNetworkTierProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the set default network tier method over HTTP.

        Args:
            request (~.compute.SetDefaultNetworkTierProjectRequest):
                The request object. A request message for
                Projects.SetDefaultNetworkTier. See the
                method description for details.

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
        body = compute.ProjectsSetDefaultNetworkTierRequest.to_json(
            request.projects_set_default_network_tier_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/setDefaultNetworkTier".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.SetDefaultNetworkTierProjectRequest.request_id in request:
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

    def set_usage_export_bucket(
        self,
        request: compute.SetUsageExportBucketProjectRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the set usage export bucket method over HTTP.

        Args:
            request (~.compute.SetUsageExportBucketProjectRequest):
                The request object. A request message for
                Projects.SetUsageExportBucket. See the
                method description for details.

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
        body = compute.UsageExportLocation.to_json(
            request.usage_export_location_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/setUsageExportBucket".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.SetUsageExportBucketProjectRequest.request_id in request:
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


__all__ = ("ProjectsRestTransport",)
