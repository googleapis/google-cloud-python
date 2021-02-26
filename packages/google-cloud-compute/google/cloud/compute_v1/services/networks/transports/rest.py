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
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.auth.transport.requests import AuthorizedSession


from google.cloud.compute_v1.types import compute


from .base import NetworksTransport, DEFAULT_CLIENT_INFO


class NetworksRestTransport(NetworksTransport):
    """REST backend transport for Networks.

    The Networks API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
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
        super().__init__(
            host=host, credentials=credentials, client_info=client_info,
        )
        self._session = AuthorizedSession(self._credentials)
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)

    def add_peering(
        self,
        request: compute.AddPeeringNetworkRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the add peering method over HTTP.

        Args:
            request (~.compute.AddPeeringNetworkRequest):
                The request object.
                A request message for
                Networks.AddPeering. See the method
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
        body = compute.NetworksAddPeeringRequest.to_json(
            request.networks_add_peering_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/networks/{network}/addPeering".format(
            host=self._host, project=request.project, network=request.network,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "requestId": request.request_id,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.post(url, data=body,)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def delete(
        self,
        request: compute.DeleteNetworkRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete method over HTTP.

        Args:
            request (~.compute.DeleteNetworkRequest):
                The request object.
                A request message for
                Networks.Delete. See the method
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
        url = "https://{host}/compute/v1/projects/{project}/global/networks/{network}".format(
            host=self._host, project=request.project, network=request.network,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "requestId": request.request_id,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.delete(url)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def get(
        self,
        request: compute.GetNetworkRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Network:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetNetworkRequest):
                The request object.
                A request message for Networks.Get.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Network:
                Represents a VPC Network resource.

                Networks connect resources to each other and to the
                internet. For more information, read Virtual Private
                Cloud (VPC) Network. (== resource_for
                {$api_version}.networks ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/networks/{network}".format(
            host=self._host, project=request.project, network=request.network,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.get(url)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.Network.from_json(response.content, ignore_unknown_fields=True)

    def insert(
        self,
        request: compute.InsertNetworkRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the insert method over HTTP.

        Args:
            request (~.compute.InsertNetworkRequest):
                The request object.
                A request message for
                Networks.Insert. See the method
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
        body = compute.Network.to_json(
            request.network_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/networks".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "requestId": request.request_id,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.post(url, data=body,)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def list(
        self,
        request: compute.ListNetworksRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.NetworkList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListNetworksRequest):
                The request object.
                A request message for Networks.List.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.NetworkList:
                Contains a list of networks.
        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/networks".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "filter": request.filter,
            "maxResults": request.max_results,
            "orderBy": request.order_by,
            "pageToken": request.page_token,
            "returnPartialSuccess": request.return_partial_success,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.get(url)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.NetworkList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def list_peering_routes(
        self,
        request: compute.ListPeeringRoutesNetworksRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.ExchangedPeeringRoutesList:
        r"""Call the list peering routes method over HTTP.

        Args:
            request (~.compute.ListPeeringRoutesNetworksRequest):
                The request object.
                A request message for
                Networks.ListPeeringRoutes. See the
                method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.ExchangedPeeringRoutesList:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/networks/{network}/listPeeringRoutes".format(
            host=self._host, project=request.project, network=request.network,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "direction": request.direction,
            "filter": request.filter,
            "maxResults": request.max_results,
            "orderBy": request.order_by,
            "pageToken": request.page_token,
            "peeringName": request.peering_name,
            "region": request.region,
            "returnPartialSuccess": request.return_partial_success,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.get(url)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.ExchangedPeeringRoutesList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def patch(
        self,
        request: compute.PatchNetworkRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the patch method over HTTP.

        Args:
            request (~.compute.PatchNetworkRequest):
                The request object.
                A request message for Networks.Patch.
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
        body = compute.Network.to_json(
            request.network_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/networks/{network}".format(
            host=self._host, project=request.project, network=request.network,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "requestId": request.request_id,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.patch(url, data=body,)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def remove_peering(
        self,
        request: compute.RemovePeeringNetworkRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the remove peering method over HTTP.

        Args:
            request (~.compute.RemovePeeringNetworkRequest):
                The request object.
                A request message for
                Networks.RemovePeering. See the method
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
        body = compute.NetworksRemovePeeringRequest.to_json(
            request.networks_remove_peering_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/networks/{network}/removePeering".format(
            host=self._host, project=request.project, network=request.network,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "requestId": request.request_id,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.post(url, data=body,)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def switch_to_custom_mode(
        self,
        request: compute.SwitchToCustomModeNetworkRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the switch to custom mode method over HTTP.

        Args:
            request (~.compute.SwitchToCustomModeNetworkRequest):
                The request object.
                A request message for
                Networks.SwitchToCustomMode. See the
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

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/networks/{network}/switchToCustomMode".format(
            host=self._host, project=request.project, network=request.network,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "requestId": request.request_id,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.post(url)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def update_peering(
        self,
        request: compute.UpdatePeeringNetworkRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the update peering method over HTTP.

        Args:
            request (~.compute.UpdatePeeringNetworkRequest):
                The request object.
                A request message for
                Networks.UpdatePeering. See the method
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
        body = compute.NetworksUpdatePeeringRequest.to_json(
            request.networks_update_peering_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/networks/{network}/updatePeering".format(
            host=self._host, project=request.project, network=request.network,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {
            "requestId": request.request_id,
        }
        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = [
            "{k}={v}".format(k=k, v=v) for k, v in query_params.items() if v
        ]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.patch(url, data=body,)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)


__all__ = ("NetworksRestTransport",)
