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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.vpcaccess_v1.types import vpc_access

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseVpcAccessServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class VpcAccessServiceRestInterceptor:
    """Interceptor for VpcAccessService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the VpcAccessServiceRestTransport.

    .. code-block:: python
        class MyCustomVpcAccessServiceInterceptor(VpcAccessServiceRestInterceptor):
            def pre_create_connector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_connector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_connector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_connector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_connector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_connector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_connectors(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_connectors(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = VpcAccessServiceRestTransport(interceptor=MyCustomVpcAccessServiceInterceptor())
        client = VpcAccessServiceClient(transport=transport)


    """

    def pre_create_connector(
        self,
        request: vpc_access.CreateConnectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vpc_access.CreateConnectorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_connector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VpcAccessService server.
        """
        return request, metadata

    def post_create_connector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_connector

        Override in a subclass to manipulate the response
        after it is returned by the VpcAccessService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_connector(
        self,
        request: vpc_access.DeleteConnectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vpc_access.DeleteConnectorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_connector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VpcAccessService server.
        """
        return request, metadata

    def post_delete_connector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_connector

        Override in a subclass to manipulate the response
        after it is returned by the VpcAccessService server but before
        it is returned to user code.
        """
        return response

    def pre_get_connector(
        self,
        request: vpc_access.GetConnectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vpc_access.GetConnectorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_connector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VpcAccessService server.
        """
        return request, metadata

    def post_get_connector(
        self, response: vpc_access.Connector
    ) -> vpc_access.Connector:
        """Post-rpc interceptor for get_connector

        Override in a subclass to manipulate the response
        after it is returned by the VpcAccessService server but before
        it is returned to user code.
        """
        return response

    def pre_list_connectors(
        self,
        request: vpc_access.ListConnectorsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vpc_access.ListConnectorsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_connectors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VpcAccessService server.
        """
        return request, metadata

    def post_list_connectors(
        self, response: vpc_access.ListConnectorsResponse
    ) -> vpc_access.ListConnectorsResponse:
        """Post-rpc interceptor for list_connectors

        Override in a subclass to manipulate the response
        after it is returned by the VpcAccessService server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VpcAccessService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the VpcAccessService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VpcAccessService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the VpcAccessService server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VpcAccessService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the VpcAccessService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class VpcAccessServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: VpcAccessServiceRestInterceptor


class VpcAccessServiceRestTransport(_BaseVpcAccessServiceRestTransport):
    """REST backend synchronous transport for VpcAccessService.

    Serverless VPC Access API allows users to create and manage
    connectors for App Engine, Cloud Functions and Cloud Run to have
    internal connections to Virtual Private Cloud networks.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "vpcaccess.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[VpcAccessServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'vpcaccess.googleapis.com').
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
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or VpcAccessServiceRestInterceptor()
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

    class _CreateConnector(
        _BaseVpcAccessServiceRestTransport._BaseCreateConnector,
        VpcAccessServiceRestStub,
    ):
        def __hash__(self):
            return hash("VpcAccessServiceRestTransport.CreateConnector")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: vpc_access.CreateConnectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create connector method over HTTP.

            Args:
                request (~.vpc_access.CreateConnectorRequest):
                    The request object. Request for creating a Serverless VPC
                Access connector.
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

            http_options = (
                _BaseVpcAccessServiceRestTransport._BaseCreateConnector._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_connector(
                request, metadata
            )
            transcoded_request = _BaseVpcAccessServiceRestTransport._BaseCreateConnector._get_transcoded_request(
                http_options, request
            )

            body = _BaseVpcAccessServiceRestTransport._BaseCreateConnector._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVpcAccessServiceRestTransport._BaseCreateConnector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VpcAccessServiceRestTransport._CreateConnector._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_connector(resp)
            return resp

    class _DeleteConnector(
        _BaseVpcAccessServiceRestTransport._BaseDeleteConnector,
        VpcAccessServiceRestStub,
    ):
        def __hash__(self):
            return hash("VpcAccessServiceRestTransport.DeleteConnector")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: vpc_access.DeleteConnectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete connector method over HTTP.

            Args:
                request (~.vpc_access.DeleteConnectorRequest):
                    The request object. Request for deleting a Serverless VPC
                Access connector.
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

            http_options = (
                _BaseVpcAccessServiceRestTransport._BaseDeleteConnector._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_connector(
                request, metadata
            )
            transcoded_request = _BaseVpcAccessServiceRestTransport._BaseDeleteConnector._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVpcAccessServiceRestTransport._BaseDeleteConnector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VpcAccessServiceRestTransport._DeleteConnector._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_connector(resp)
            return resp

    class _GetConnector(
        _BaseVpcAccessServiceRestTransport._BaseGetConnector, VpcAccessServiceRestStub
    ):
        def __hash__(self):
            return hash("VpcAccessServiceRestTransport.GetConnector")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: vpc_access.GetConnectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vpc_access.Connector:
            r"""Call the get connector method over HTTP.

            Args:
                request (~.vpc_access.GetConnectorRequest):
                    The request object. Request for getting a Serverless VPC
                Access connector.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vpc_access.Connector:
                    Definition of a Serverless VPC Access
                connector.

            """

            http_options = (
                _BaseVpcAccessServiceRestTransport._BaseGetConnector._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_connector(request, metadata)
            transcoded_request = _BaseVpcAccessServiceRestTransport._BaseGetConnector._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVpcAccessServiceRestTransport._BaseGetConnector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VpcAccessServiceRestTransport._GetConnector._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = vpc_access.Connector()
            pb_resp = vpc_access.Connector.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_connector(resp)
            return resp

    class _ListConnectors(
        _BaseVpcAccessServiceRestTransport._BaseListConnectors, VpcAccessServiceRestStub
    ):
        def __hash__(self):
            return hash("VpcAccessServiceRestTransport.ListConnectors")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: vpc_access.ListConnectorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vpc_access.ListConnectorsResponse:
            r"""Call the list connectors method over HTTP.

            Args:
                request (~.vpc_access.ListConnectorsRequest):
                    The request object. Request for listing Serverless VPC
                Access connectors in a location.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vpc_access.ListConnectorsResponse:
                    Response for listing Serverless VPC
                Access connectors.

            """

            http_options = (
                _BaseVpcAccessServiceRestTransport._BaseListConnectors._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_connectors(request, metadata)
            transcoded_request = _BaseVpcAccessServiceRestTransport._BaseListConnectors._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVpcAccessServiceRestTransport._BaseListConnectors._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VpcAccessServiceRestTransport._ListConnectors._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = vpc_access.ListConnectorsResponse()
            pb_resp = vpc_access.ListConnectorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_connectors(resp)
            return resp

    @property
    def create_connector(
        self,
    ) -> Callable[[vpc_access.CreateConnectorRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateConnector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_connector(
        self,
    ) -> Callable[[vpc_access.DeleteConnectorRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteConnector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_connector(
        self,
    ) -> Callable[[vpc_access.GetConnectorRequest], vpc_access.Connector]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConnector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_connectors(
        self,
    ) -> Callable[
        [vpc_access.ListConnectorsRequest], vpc_access.ListConnectorsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConnectors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseVpcAccessServiceRestTransport._BaseListLocations, VpcAccessServiceRestStub
    ):
        def __hash__(self):
            return hash("VpcAccessServiceRestTransport.ListLocations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseVpcAccessServiceRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseVpcAccessServiceRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVpcAccessServiceRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VpcAccessServiceRestTransport._ListLocations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseVpcAccessServiceRestTransport._BaseGetOperation, VpcAccessServiceRestStub
    ):
        def __hash__(self):
            return hash("VpcAccessServiceRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseVpcAccessServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseVpcAccessServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVpcAccessServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VpcAccessServiceRestTransport._GetOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseVpcAccessServiceRestTransport._BaseListOperations, VpcAccessServiceRestStub
    ):
        def __hash__(self):
            return hash("VpcAccessServiceRestTransport.ListOperations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseVpcAccessServiceRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseVpcAccessServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVpcAccessServiceRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VpcAccessServiceRestTransport._ListOperations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("VpcAccessServiceRestTransport",)
