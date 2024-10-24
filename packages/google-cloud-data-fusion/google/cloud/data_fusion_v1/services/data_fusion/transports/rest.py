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
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.data_fusion_v1.types import datafusion

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseDataFusionRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class DataFusionRestInterceptor:
    """Interceptor for DataFusion.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DataFusionRestTransport.

    .. code-block:: python
        class MyCustomDataFusionInterceptor(DataFusionRestInterceptor):
            def pre_create_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_available_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_available_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restart_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restart_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DataFusionRestTransport(interceptor=MyCustomDataFusionInterceptor())
        client = DataFusionClient(transport=transport)


    """

    def pre_create_instance(
        self,
        request: datafusion.CreateInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datafusion.CreateInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataFusion server.
        """
        return request, metadata

    def post_create_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_instance

        Override in a subclass to manipulate the response
        after it is returned by the DataFusion server but before
        it is returned to user code.
        """
        return response

    def pre_delete_instance(
        self,
        request: datafusion.DeleteInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datafusion.DeleteInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataFusion server.
        """
        return request, metadata

    def post_delete_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_instance

        Override in a subclass to manipulate the response
        after it is returned by the DataFusion server but before
        it is returned to user code.
        """
        return response

    def pre_get_instance(
        self,
        request: datafusion.GetInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datafusion.GetInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataFusion server.
        """
        return request, metadata

    def post_get_instance(self, response: datafusion.Instance) -> datafusion.Instance:
        """Post-rpc interceptor for get_instance

        Override in a subclass to manipulate the response
        after it is returned by the DataFusion server but before
        it is returned to user code.
        """
        return response

    def pre_list_available_versions(
        self,
        request: datafusion.ListAvailableVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datafusion.ListAvailableVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_available_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataFusion server.
        """
        return request, metadata

    def post_list_available_versions(
        self, response: datafusion.ListAvailableVersionsResponse
    ) -> datafusion.ListAvailableVersionsResponse:
        """Post-rpc interceptor for list_available_versions

        Override in a subclass to manipulate the response
        after it is returned by the DataFusion server but before
        it is returned to user code.
        """
        return response

    def pre_list_instances(
        self,
        request: datafusion.ListInstancesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datafusion.ListInstancesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataFusion server.
        """
        return request, metadata

    def post_list_instances(
        self, response: datafusion.ListInstancesResponse
    ) -> datafusion.ListInstancesResponse:
        """Post-rpc interceptor for list_instances

        Override in a subclass to manipulate the response
        after it is returned by the DataFusion server but before
        it is returned to user code.
        """
        return response

    def pre_restart_instance(
        self,
        request: datafusion.RestartInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datafusion.RestartInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for restart_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataFusion server.
        """
        return request, metadata

    def post_restart_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for restart_instance

        Override in a subclass to manipulate the response
        after it is returned by the DataFusion server but before
        it is returned to user code.
        """
        return response

    def pre_update_instance(
        self,
        request: datafusion.UpdateInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[datafusion.UpdateInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the DataFusion server.
        """
        return request, metadata

    def post_update_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_instance

        Override in a subclass to manipulate the response
        after it is returned by the DataFusion server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DataFusionRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DataFusionRestInterceptor


class DataFusionRestTransport(_BaseDataFusionRestTransport):
    """REST backend synchronous transport for DataFusion.

    Service for creating and managing Data Fusion instances.
    Data Fusion enables ETL developers to build code-free, data
    integration pipelines via a point-and-click UI.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "datafusion.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DataFusionRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'datafusion.googleapis.com').
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
        self._interceptor = interceptor or DataFusionRestInterceptor()
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

    class _CreateInstance(
        _BaseDataFusionRestTransport._BaseCreateInstance, DataFusionRestStub
    ):
        def __hash__(self):
            return hash("DataFusionRestTransport.CreateInstance")

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
            request: datafusion.CreateInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create instance method over HTTP.

            Args:
                request (~.datafusion.CreateInstanceRequest):
                    The request object. Request message for creating a Data
                Fusion instance.
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
                _BaseDataFusionRestTransport._BaseCreateInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_instance(request, metadata)
            transcoded_request = _BaseDataFusionRestTransport._BaseCreateInstance._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseDataFusionRestTransport._BaseCreateInstance._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataFusionRestTransport._BaseCreateInstance._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = DataFusionRestTransport._CreateInstance._get_response(
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
            resp = self._interceptor.post_create_instance(resp)
            return resp

    class _DeleteInstance(
        _BaseDataFusionRestTransport._BaseDeleteInstance, DataFusionRestStub
    ):
        def __hash__(self):
            return hash("DataFusionRestTransport.DeleteInstance")

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
            request: datafusion.DeleteInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete instance method over HTTP.

            Args:
                request (~.datafusion.DeleteInstanceRequest):
                    The request object. Request message for deleting a Data
                Fusion instance.
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
                _BaseDataFusionRestTransport._BaseDeleteInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_instance(request, metadata)
            transcoded_request = _BaseDataFusionRestTransport._BaseDeleteInstance._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseDataFusionRestTransport._BaseDeleteInstance._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = DataFusionRestTransport._DeleteInstance._get_response(
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
            resp = self._interceptor.post_delete_instance(resp)
            return resp

    class _GetInstance(
        _BaseDataFusionRestTransport._BaseGetInstance, DataFusionRestStub
    ):
        def __hash__(self):
            return hash("DataFusionRestTransport.GetInstance")

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
            request: datafusion.GetInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datafusion.Instance:
            r"""Call the get instance method over HTTP.

            Args:
                request (~.datafusion.GetInstanceRequest):
                    The request object. Request message for getting details
                about a Data Fusion instance.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datafusion.Instance:
                    Represents a Data Fusion instance.
            """

            http_options = (
                _BaseDataFusionRestTransport._BaseGetInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_instance(request, metadata)
            transcoded_request = (
                _BaseDataFusionRestTransport._BaseGetInstance._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataFusionRestTransport._BaseGetInstance._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = DataFusionRestTransport._GetInstance._get_response(
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
            resp = datafusion.Instance()
            pb_resp = datafusion.Instance.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_instance(resp)
            return resp

    class _ListAvailableVersions(
        _BaseDataFusionRestTransport._BaseListAvailableVersions, DataFusionRestStub
    ):
        def __hash__(self):
            return hash("DataFusionRestTransport.ListAvailableVersions")

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
            request: datafusion.ListAvailableVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datafusion.ListAvailableVersionsResponse:
            r"""Call the list available versions method over HTTP.

            Args:
                request (~.datafusion.ListAvailableVersionsRequest):
                    The request object. Request message for the list
                available versions request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datafusion.ListAvailableVersionsResponse:
                    Response message for the list
                available versions request.

            """

            http_options = (
                _BaseDataFusionRestTransport._BaseListAvailableVersions._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_available_versions(
                request, metadata
            )
            transcoded_request = _BaseDataFusionRestTransport._BaseListAvailableVersions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseDataFusionRestTransport._BaseListAvailableVersions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataFusionRestTransport._ListAvailableVersions._get_response(
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
            resp = datafusion.ListAvailableVersionsResponse()
            pb_resp = datafusion.ListAvailableVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_available_versions(resp)
            return resp

    class _ListInstances(
        _BaseDataFusionRestTransport._BaseListInstances, DataFusionRestStub
    ):
        def __hash__(self):
            return hash("DataFusionRestTransport.ListInstances")

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
            request: datafusion.ListInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> datafusion.ListInstancesResponse:
            r"""Call the list instances method over HTTP.

            Args:
                request (~.datafusion.ListInstancesRequest):
                    The request object. Request message for listing Data
                Fusion instances.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.datafusion.ListInstancesResponse:
                    Response message for the list
                instance request.

            """

            http_options = (
                _BaseDataFusionRestTransport._BaseListInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_instances(request, metadata)
            transcoded_request = (
                _BaseDataFusionRestTransport._BaseListInstances._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataFusionRestTransport._BaseListInstances._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = DataFusionRestTransport._ListInstances._get_response(
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
            resp = datafusion.ListInstancesResponse()
            pb_resp = datafusion.ListInstancesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_instances(resp)
            return resp

    class _RestartInstance(
        _BaseDataFusionRestTransport._BaseRestartInstance, DataFusionRestStub
    ):
        def __hash__(self):
            return hash("DataFusionRestTransport.RestartInstance")

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
            request: datafusion.RestartInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restart instance method over HTTP.

            Args:
                request (~.datafusion.RestartInstanceRequest):
                    The request object. Request message for restarting a Data
                Fusion instance.
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
                _BaseDataFusionRestTransport._BaseRestartInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_restart_instance(
                request, metadata
            )
            transcoded_request = _BaseDataFusionRestTransport._BaseRestartInstance._get_transcoded_request(
                http_options, request
            )

            body = _BaseDataFusionRestTransport._BaseRestartInstance._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseDataFusionRestTransport._BaseRestartInstance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = DataFusionRestTransport._RestartInstance._get_response(
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
            resp = self._interceptor.post_restart_instance(resp)
            return resp

    class _UpdateInstance(
        _BaseDataFusionRestTransport._BaseUpdateInstance, DataFusionRestStub
    ):
        def __hash__(self):
            return hash("DataFusionRestTransport.UpdateInstance")

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
            request: datafusion.UpdateInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update instance method over HTTP.

            Args:
                request (~.datafusion.UpdateInstanceRequest):
                    The request object. Request message for updating a Data
                Fusion instance. Data Fusion allows
                updating the labels, options, and stack
                driver settings. This is also used for
                CDF version upgrade.
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
                _BaseDataFusionRestTransport._BaseUpdateInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_instance(request, metadata)
            transcoded_request = _BaseDataFusionRestTransport._BaseUpdateInstance._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseDataFusionRestTransport._BaseUpdateInstance._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseDataFusionRestTransport._BaseUpdateInstance._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = DataFusionRestTransport._UpdateInstance._get_response(
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
            resp = self._interceptor.post_update_instance(resp)
            return resp

    @property
    def create_instance(
        self,
    ) -> Callable[[datafusion.CreateInstanceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_instance(
        self,
    ) -> Callable[[datafusion.DeleteInstanceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_instance(
        self,
    ) -> Callable[[datafusion.GetInstanceRequest], datafusion.Instance]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_available_versions(
        self,
    ) -> Callable[
        [datafusion.ListAvailableVersionsRequest],
        datafusion.ListAvailableVersionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAvailableVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_instances(
        self,
    ) -> Callable[[datafusion.ListInstancesRequest], datafusion.ListInstancesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def restart_instance(
        self,
    ) -> Callable[[datafusion.RestartInstanceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestartInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_instance(
        self,
    ) -> Callable[[datafusion.UpdateInstanceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DataFusionRestTransport",)
