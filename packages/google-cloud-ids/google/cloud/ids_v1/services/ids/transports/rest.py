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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.ids_v1.types import ids

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import IDSTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class IDSRestInterceptor:
    """Interceptor for IDS.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the IDSRestTransport.

    .. code-block:: python
        class MyCustomIDSInterceptor(IDSRestInterceptor):
            def pre_create_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_endpoint(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_endpoint(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_endpoints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_endpoints(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = IDSRestTransport(interceptor=MyCustomIDSInterceptor())
        client = IDSClient(transport=transport)


    """

    def pre_create_endpoint(
        self, request: ids.CreateEndpointRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[ids.CreateEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IDS server.
        """
        return request, metadata

    def post_create_endpoint(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the IDS server but before
        it is returned to user code.
        """
        return response

    def pre_delete_endpoint(
        self, request: ids.DeleteEndpointRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[ids.DeleteEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IDS server.
        """
        return request, metadata

    def post_delete_endpoint(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the IDS server but before
        it is returned to user code.
        """
        return response

    def pre_get_endpoint(
        self, request: ids.GetEndpointRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[ids.GetEndpointRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_endpoint

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IDS server.
        """
        return request, metadata

    def post_get_endpoint(self, response: ids.Endpoint) -> ids.Endpoint:
        """Post-rpc interceptor for get_endpoint

        Override in a subclass to manipulate the response
        after it is returned by the IDS server but before
        it is returned to user code.
        """
        return response

    def pre_list_endpoints(
        self, request: ids.ListEndpointsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[ids.ListEndpointsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_endpoints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the IDS server.
        """
        return request, metadata

    def post_list_endpoints(
        self, response: ids.ListEndpointsResponse
    ) -> ids.ListEndpointsResponse:
        """Post-rpc interceptor for list_endpoints

        Override in a subclass to manipulate the response
        after it is returned by the IDS server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class IDSRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: IDSRestInterceptor


class IDSRestTransport(IDSTransport):
    """REST backend transport for IDS.

    The IDS Service

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "ids.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[IDSRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'ids.googleapis.com').
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
                Generally, you only need to set this if you are developing
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or IDSRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateEndpoint(IDSRestStub):
        def __hash__(self):
            return hash("CreateEndpoint")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "endpointId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: ids.CreateEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create endpoint method over HTTP.

            Args:
                request (~.ids.CreateEndpointRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/endpoints",
                    "body": "endpoint",
                },
            ]
            request, metadata = self._interceptor.pre_create_endpoint(request, metadata)
            pb_request = ids.CreateEndpointRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_endpoint(resp)
            return resp

    class _DeleteEndpoint(IDSRestStub):
        def __hash__(self):
            return hash("DeleteEndpoint")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: ids.DeleteEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete endpoint method over HTTP.

            Args:
                request (~.ids.DeleteEndpointRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/endpoints/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_endpoint(request, metadata)
            pb_request = ids.DeleteEndpointRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_endpoint(resp)
            return resp

    class _GetEndpoint(IDSRestStub):
        def __hash__(self):
            return hash("GetEndpoint")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: ids.GetEndpointRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ids.Endpoint:
            r"""Call the get endpoint method over HTTP.

            Args:
                request (~.ids.GetEndpointRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ids.Endpoint:
                    Endpoint describes a single IDS
                endpoint. It defines a forwarding rule
                to which packets can be sent for IDS
                inspection.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/endpoints/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_endpoint(request, metadata)
            pb_request = ids.GetEndpointRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = ids.Endpoint()
            pb_resp = ids.Endpoint.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_endpoint(resp)
            return resp

    class _ListEndpoints(IDSRestStub):
        def __hash__(self):
            return hash("ListEndpoints")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: ids.ListEndpointsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ids.ListEndpointsResponse:
            r"""Call the list endpoints method over HTTP.

            Args:
                request (~.ids.ListEndpointsRequest):
                    The request object.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ids.ListEndpointsResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/endpoints",
                },
            ]
            request, metadata = self._interceptor.pre_list_endpoints(request, metadata)
            pb_request = ids.ListEndpointsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = ids.ListEndpointsResponse()
            pb_resp = ids.ListEndpointsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_endpoints(resp)
            return resp

    @property
    def create_endpoint(
        self,
    ) -> Callable[[ids.CreateEndpointRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_endpoint(
        self,
    ) -> Callable[[ids.DeleteEndpointRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_endpoint(self) -> Callable[[ids.GetEndpointRequest], ids.Endpoint]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEndpoint(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_endpoints(
        self,
    ) -> Callable[[ids.ListEndpointsRequest], ids.ListEndpointsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEndpoints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("IDSRestTransport",)
