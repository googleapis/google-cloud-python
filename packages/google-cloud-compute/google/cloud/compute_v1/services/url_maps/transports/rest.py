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

from .base import UrlMapsTransport, DEFAULT_CLIENT_INFO


class UrlMapsRestTransport(UrlMapsTransport):
    """REST backend transport for UrlMaps.

    The UrlMaps API.

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

    def aggregated_list(
        self,
        request: compute.AggregatedListUrlMapsRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.UrlMapsAggregatedList:
        r"""Call the aggregated list method over HTTP.

        Args:
            request (~.compute.AggregatedListUrlMapsRequest):
                The request object. A request message for
                UrlMaps.AggregatedList. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.UrlMapsAggregatedList:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/aggregated/urlMaps".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.AggregatedListUrlMapsRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.AggregatedListUrlMapsRequest.include_all_scopes in request:
            query_params["includeAllScopes"] = request.include_all_scopes
        if compute.AggregatedListUrlMapsRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.AggregatedListUrlMapsRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.AggregatedListUrlMapsRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.AggregatedListUrlMapsRequest.return_partial_success in request:
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
        return compute.UrlMapsAggregatedList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def delete(
        self,
        request: compute.DeleteUrlMapRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete method over HTTP.

        Args:
            request (~.compute.DeleteUrlMapRequest):
                The request object. A request message for UrlMaps.Delete.
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

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/urlMaps/{url_map}".format(
            host=self._host, project=request.project, url_map=request.url_map,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.DeleteUrlMapRequest.request_id in request:
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

    def get(
        self,
        request: compute.GetUrlMapRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.UrlMap:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetUrlMapRequest):
                The request object. A request message for UrlMaps.Get.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.UrlMap:
                Represents a URL Map resource.

                Google Compute Engine has two URL Map resources:

                -  `Global </compute/docs/reference/rest/{$api_version}/urlMaps>`__
                   \*
                   `Regional </compute/docs/reference/rest/{$api_version}/regionUrlMaps>`__

                A URL map resource is a component of certain types of
                GCP load balancers and Traffic Director.

                -  urlMaps are used by external HTTP(S) load balancers
                   and Traffic Director. \* regionUrlMaps are used by
                   internal HTTP(S) load balancers.

                For a list of supported URL map features by load
                balancer type, see the Load balancing features: Routing
                and traffic management table.

                For a list of supported URL map features for Traffic
                Director, see the Traffic Director features: Routing and
                traffic management table.

                This resource defines mappings from host names and URL
                paths to either a backend service or a backend bucket.

                To use the global urlMaps resource, the backend service
                must have a loadBalancingScheme of either EXTERNAL or
                INTERNAL_SELF_MANAGED. To use the regionUrlMaps
                resource, the backend service must have a
                loadBalancingScheme of INTERNAL_MANAGED. For more
                information, read URL Map Concepts.

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/urlMaps/{url_map}".format(
            host=self._host, project=request.project, url_map=request.url_map,
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
        return compute.UrlMap.from_json(response.content, ignore_unknown_fields=True)

    def insert(
        self,
        request: compute.InsertUrlMapRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the insert method over HTTP.

        Args:
            request (~.compute.InsertUrlMapRequest):
                The request object. A request message for UrlMaps.Insert.
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
        body = compute.UrlMap.to_json(
            request.url_map_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/urlMaps".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.InsertUrlMapRequest.request_id in request:
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

    def invalidate_cache(
        self,
        request: compute.InvalidateCacheUrlMapRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the invalidate cache method over HTTP.

        Args:
            request (~.compute.InvalidateCacheUrlMapRequest):
                The request object. A request message for
                UrlMaps.InvalidateCache. See the method
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
        body = compute.CacheInvalidationRule.to_json(
            request.cache_invalidation_rule_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/urlMaps/{url_map}/invalidateCache".format(
            host=self._host, project=request.project, url_map=request.url_map,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.InvalidateCacheUrlMapRequest.request_id in request:
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
        request: compute.ListUrlMapsRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.UrlMapList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListUrlMapsRequest):
                The request object. A request message for UrlMaps.List.
                See the method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.UrlMapList:
                Contains a list of UrlMap resources.
        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/urlMaps".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListUrlMapsRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListUrlMapsRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListUrlMapsRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListUrlMapsRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.ListUrlMapsRequest.return_partial_success in request:
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
        return compute.UrlMapList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def patch(
        self,
        request: compute.PatchUrlMapRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the patch method over HTTP.

        Args:
            request (~.compute.PatchUrlMapRequest):
                The request object. A request message for UrlMaps.Patch.
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
        body = compute.UrlMap.to_json(
            request.url_map_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/urlMaps/{url_map}".format(
            host=self._host, project=request.project, url_map=request.url_map,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.PatchUrlMapRequest.request_id in request:
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

    def update(
        self,
        request: compute.UpdateUrlMapRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the update method over HTTP.

        Args:
            request (~.compute.UpdateUrlMapRequest):
                The request object. A request message for UrlMaps.Update.
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
        body = compute.UrlMap.to_json(
            request.url_map_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/urlMaps/{url_map}".format(
            host=self._host, project=request.project, url_map=request.url_map,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.UpdateUrlMapRequest.request_id in request:
            query_params["requestId"] = request.request_id

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.put(
            url, headers=headers, params=query_params, data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def validate(
        self,
        request: compute.ValidateUrlMapRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.UrlMapsValidateResponse:
        r"""Call the validate method over HTTP.

        Args:
            request (~.compute.ValidateUrlMapRequest):
                The request object. A request message for
                UrlMaps.Validate. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.UrlMapsValidateResponse:

        """

        # Jsonify the request body
        body = compute.UrlMapsValidateRequest.to_json(
            request.url_maps_validate_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/urlMaps/{url_map}/validate".format(
            host=self._host, project=request.project, url_map=request.url_map,
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
        return compute.UrlMapsValidateResponse.from_json(
            response.content, ignore_unknown_fields=True
        )


__all__ = ("UrlMapsRestTransport",)
