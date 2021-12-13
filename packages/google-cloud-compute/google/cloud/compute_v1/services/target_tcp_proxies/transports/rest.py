from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import path_template
from google.api_core import gapic_v1
from requests import __version__ as requests_version
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

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

from google.cloud.compute_v1.types import compute

from .base import (
    TargetTcpProxiesTransport,
    DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO,
)


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class TargetTcpProxiesRestTransport(TargetTcpProxiesTransport):
    """REST backend transport for TargetTcpProxies.

    The TargetTcpProxies API.

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
        url_scheme: str = "https",
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
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
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

    def _delete(
        self,
        request: compute.DeleteTargetTcpProxyRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete method over HTTP.

        Args:
            request (~.compute.DeleteTargetTcpProxyRequest):
                The request object. A request message for
                TargetTcpProxies.Delete. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

        """

        http_options = [
            {
                "method": "delete",
                "uri": "/compute/v1/projects/{project}/global/targetTcpProxies/{target_tcp_proxy}",
            },
        ]

        required_fields = [
            # (snake_case_name, camel_case_name)
            ("project", "project"),
            ("target_tcp_proxy", "targetTcpProxy"),
        ]

        request_kwargs = compute.DeleteTargetTcpProxyRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.DeleteTargetTcpProxyRequest.to_json(
                compute.DeleteTargetTcpProxyRequest(transcoded_request["query_params"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        # Ensure required fields have values in query_params.
        # If a required field has a default value, it can get lost
        # by the to_json call above.
        orig_query_params = transcoded_request["query_params"]
        for snake_case_name, camel_case_name in required_fields:
            if snake_case_name in orig_query_params:
                if camel_case_name not in query_params:
                    query_params[camel_case_name] = orig_query_params[snake_case_name]

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def _get(
        self,
        request: compute.GetTargetTcpProxyRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.TargetTcpProxy:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetTargetTcpProxyRequest):
                The request object. A request message for
                TargetTcpProxies.Get. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.TargetTcpProxy:
                Represents a Target TCP Proxy
                resource. A target TCP proxy is a
                component of a TCP Proxy load balancer.
                Global forwarding rules reference target
                TCP proxy, and the target proxy then
                references an external backend service.
                For more information, read TCP Proxy
                Load Balancing overview.

        """

        http_options = [
            {
                "method": "get",
                "uri": "/compute/v1/projects/{project}/global/targetTcpProxies/{target_tcp_proxy}",
            },
        ]

        required_fields = [
            # (snake_case_name, camel_case_name)
            ("project", "project"),
            ("target_tcp_proxy", "targetTcpProxy"),
        ]

        request_kwargs = compute.GetTargetTcpProxyRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.GetTargetTcpProxyRequest.to_json(
                compute.GetTargetTcpProxyRequest(transcoded_request["query_params"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        # Ensure required fields have values in query_params.
        # If a required field has a default value, it can get lost
        # by the to_json call above.
        orig_query_params = transcoded_request["query_params"]
        for snake_case_name, camel_case_name in required_fields:
            if snake_case_name in orig_query_params:
                if camel_case_name not in query_params:
                    query_params[camel_case_name] = orig_query_params[snake_case_name]

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.TargetTcpProxy.from_json(
            response.content, ignore_unknown_fields=True
        )

    def _insert(
        self,
        request: compute.InsertTargetTcpProxyRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the insert method over HTTP.

        Args:
            request (~.compute.InsertTargetTcpProxyRequest):
                The request object. A request message for
                TargetTcpProxies.Insert. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

        """

        http_options = [
            {
                "method": "post",
                "uri": "/compute/v1/projects/{project}/global/targetTcpProxies",
                "body": "target_tcp_proxy_resource",
            },
        ]

        required_fields = [
            # (snake_case_name, camel_case_name)
            ("project", "project"),
        ]

        request_kwargs = compute.InsertTargetTcpProxyRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        # Jsonify the request body
        body = compute.TargetTcpProxy.to_json(
            compute.TargetTcpProxy(transcoded_request["body"]),
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.InsertTargetTcpProxyRequest.to_json(
                compute.InsertTargetTcpProxyRequest(transcoded_request["query_params"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        # Ensure required fields have values in query_params.
        # If a required field has a default value, it can get lost
        # by the to_json call above.
        orig_query_params = transcoded_request["query_params"]
        for snake_case_name, camel_case_name in required_fields:
            if snake_case_name in orig_query_params:
                if camel_case_name not in query_params:
                    query_params[camel_case_name] = orig_query_params[snake_case_name]

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
            data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def _list(
        self,
        request: compute.ListTargetTcpProxiesRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.TargetTcpProxyList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListTargetTcpProxiesRequest):
                The request object. A request message for
                TargetTcpProxies.List. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.TargetTcpProxyList:
                Contains a list of TargetTcpProxy
                resources.

        """

        http_options = [
            {
                "method": "get",
                "uri": "/compute/v1/projects/{project}/global/targetTcpProxies",
            },
        ]

        required_fields = [
            # (snake_case_name, camel_case_name)
            ("project", "project"),
        ]

        request_kwargs = compute.ListTargetTcpProxiesRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.ListTargetTcpProxiesRequest.to_json(
                compute.ListTargetTcpProxiesRequest(transcoded_request["query_params"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        # Ensure required fields have values in query_params.
        # If a required field has a default value, it can get lost
        # by the to_json call above.
        orig_query_params = transcoded_request["query_params"]
        for snake_case_name, camel_case_name in required_fields:
            if snake_case_name in orig_query_params:
                if camel_case_name not in query_params:
                    query_params[camel_case_name] = orig_query_params[snake_case_name]

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.TargetTcpProxyList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def _set_backend_service(
        self,
        request: compute.SetBackendServiceTargetTcpProxyRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the set backend service method over HTTP.

        Args:
            request (~.compute.SetBackendServiceTargetTcpProxyRequest):
                The request object. A request message for
                TargetTcpProxies.SetBackendService. See
                the method description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

        """

        http_options = [
            {
                "method": "post",
                "uri": "/compute/v1/projects/{project}/global/targetTcpProxies/{target_tcp_proxy}/setBackendService",
                "body": "target_tcp_proxies_set_backend_service_request_resource",
            },
        ]

        required_fields = [
            # (snake_case_name, camel_case_name)
            ("project", "project"),
            ("target_tcp_proxy", "targetTcpProxy"),
        ]

        request_kwargs = compute.SetBackendServiceTargetTcpProxyRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        # Jsonify the request body
        body = compute.TargetTcpProxiesSetBackendServiceRequest.to_json(
            compute.TargetTcpProxiesSetBackendServiceRequest(
                transcoded_request["body"]
            ),
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.SetBackendServiceTargetTcpProxyRequest.to_json(
                compute.SetBackendServiceTargetTcpProxyRequest(
                    transcoded_request["query_params"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        # Ensure required fields have values in query_params.
        # If a required field has a default value, it can get lost
        # by the to_json call above.
        orig_query_params = transcoded_request["query_params"]
        for snake_case_name, camel_case_name in required_fields:
            if snake_case_name in orig_query_params:
                if camel_case_name not in query_params:
                    query_params[camel_case_name] = orig_query_params[snake_case_name]

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
            data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def _set_proxy_header(
        self,
        request: compute.SetProxyHeaderTargetTcpProxyRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the set proxy header method over HTTP.

        Args:
            request (~.compute.SetProxyHeaderTargetTcpProxyRequest):
                The request object. A request message for
                TargetTcpProxies.SetProxyHeader. See the
                method description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

        """

        http_options = [
            {
                "method": "post",
                "uri": "/compute/v1/projects/{project}/global/targetTcpProxies/{target_tcp_proxy}/setProxyHeader",
                "body": "target_tcp_proxies_set_proxy_header_request_resource",
            },
        ]

        required_fields = [
            # (snake_case_name, camel_case_name)
            ("project", "project"),
            ("target_tcp_proxy", "targetTcpProxy"),
        ]

        request_kwargs = compute.SetProxyHeaderTargetTcpProxyRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        # Jsonify the request body
        body = compute.TargetTcpProxiesSetProxyHeaderRequest.to_json(
            compute.TargetTcpProxiesSetProxyHeaderRequest(transcoded_request["body"]),
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.SetProxyHeaderTargetTcpProxyRequest.to_json(
                compute.SetProxyHeaderTargetTcpProxyRequest(
                    transcoded_request["query_params"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        # Ensure required fields have values in query_params.
        # If a required field has a default value, it can get lost
        # by the to_json call above.
        orig_query_params = transcoded_request["query_params"]
        for snake_case_name, camel_case_name in required_fields:
            if snake_case_name in orig_query_params:
                if camel_case_name not in query_params:
                    query_params[camel_case_name] = orig_query_params[snake_case_name]

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
            data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteTargetTcpProxyRequest], compute.Operation]:
        return self._delete

    @property
    def get(
        self,
    ) -> Callable[[compute.GetTargetTcpProxyRequest], compute.TargetTcpProxy]:
        return self._get

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertTargetTcpProxyRequest], compute.Operation]:
        return self._insert

    @property
    def list(
        self,
    ) -> Callable[[compute.ListTargetTcpProxiesRequest], compute.TargetTcpProxyList]:
        return self._list

    @property
    def set_backend_service(
        self,
    ) -> Callable[[compute.SetBackendServiceTargetTcpProxyRequest], compute.Operation]:
        return self._set_backend_service

    @property
    def set_proxy_header(
        self,
    ) -> Callable[[compute.SetProxyHeaderTargetTcpProxyRequest], compute.Operation]:
        return self._set_proxy_header

    def close(self):
        self._session.close()


__all__ = ("TargetTcpProxiesRestTransport",)
