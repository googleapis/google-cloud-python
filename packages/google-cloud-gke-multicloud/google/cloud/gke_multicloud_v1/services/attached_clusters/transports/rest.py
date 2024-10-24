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

from google.cloud.gke_multicloud_v1.types import attached_resources, attached_service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseAttachedClustersRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class AttachedClustersRestInterceptor:
    """Interceptor for AttachedClusters.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AttachedClustersRestTransport.

    .. code-block:: python
        class MyCustomAttachedClustersInterceptor(AttachedClustersRestInterceptor):
            def pre_create_attached_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_attached_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_attached_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_attached_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_attached_cluster_agent_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_attached_cluster_agent_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_attached_cluster_install_manifest(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_attached_cluster_install_manifest(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_attached_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_attached_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_attached_server_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_attached_server_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_attached_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_attached_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_attached_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_attached_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_attached_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_attached_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AttachedClustersRestTransport(interceptor=MyCustomAttachedClustersInterceptor())
        client = AttachedClustersClient(transport=transport)


    """

    def pre_create_attached_cluster(
        self,
        request: attached_service.CreateAttachedClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        attached_service.CreateAttachedClusterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_attached_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_create_attached_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_attached_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_delete_attached_cluster(
        self,
        request: attached_service.DeleteAttachedClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        attached_service.DeleteAttachedClusterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_attached_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_delete_attached_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_attached_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_generate_attached_cluster_agent_token(
        self,
        request: attached_service.GenerateAttachedClusterAgentTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        attached_service.GenerateAttachedClusterAgentTokenRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for generate_attached_cluster_agent_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_generate_attached_cluster_agent_token(
        self, response: attached_service.GenerateAttachedClusterAgentTokenResponse
    ) -> attached_service.GenerateAttachedClusterAgentTokenResponse:
        """Post-rpc interceptor for generate_attached_cluster_agent_token

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_generate_attached_cluster_install_manifest(
        self,
        request: attached_service.GenerateAttachedClusterInstallManifestRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        attached_service.GenerateAttachedClusterInstallManifestRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for generate_attached_cluster_install_manifest

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_generate_attached_cluster_install_manifest(
        self, response: attached_service.GenerateAttachedClusterInstallManifestResponse
    ) -> attached_service.GenerateAttachedClusterInstallManifestResponse:
        """Post-rpc interceptor for generate_attached_cluster_install_manifest

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_attached_cluster(
        self,
        request: attached_service.GetAttachedClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[attached_service.GetAttachedClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_attached_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_get_attached_cluster(
        self, response: attached_resources.AttachedCluster
    ) -> attached_resources.AttachedCluster:
        """Post-rpc interceptor for get_attached_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_attached_server_config(
        self,
        request: attached_service.GetAttachedServerConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        attached_service.GetAttachedServerConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_attached_server_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_get_attached_server_config(
        self, response: attached_resources.AttachedServerConfig
    ) -> attached_resources.AttachedServerConfig:
        """Post-rpc interceptor for get_attached_server_config

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_import_attached_cluster(
        self,
        request: attached_service.ImportAttachedClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        attached_service.ImportAttachedClusterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for import_attached_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_import_attached_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for import_attached_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_list_attached_clusters(
        self,
        request: attached_service.ListAttachedClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[attached_service.ListAttachedClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_attached_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_list_attached_clusters(
        self, response: attached_service.ListAttachedClustersResponse
    ) -> attached_service.ListAttachedClustersResponse:
        """Post-rpc interceptor for list_attached_clusters

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_update_attached_cluster(
        self,
        request: attached_service.UpdateAttachedClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        attached_service.UpdateAttachedClusterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_attached_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_update_attached_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_attached_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
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
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
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
        before they are sent to the AttachedClusters server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the AttachedClusters server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AttachedClustersRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AttachedClustersRestInterceptor


class AttachedClustersRestTransport(_BaseAttachedClustersRestTransport):
    """REST backend synchronous transport for AttachedClusters.

    The AttachedClusters API provides a single centrally managed
    service to register and manage Anthos attached clusters that run
    on customer's owned infrastructure.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "gkemulticloud.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AttachedClustersRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to (default: 'gkemulticloud.googleapis.com').
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
        self._interceptor = interceptor or AttachedClustersRestInterceptor()
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

    class _CreateAttachedCluster(
        _BaseAttachedClustersRestTransport._BaseCreateAttachedCluster,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.CreateAttachedCluster")

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
            request: attached_service.CreateAttachedClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create attached cluster method over HTTP.

            Args:
                request (~.attached_service.CreateAttachedClusterRequest):
                    The request object. Request message for
                ``AttachedClusters.CreateAttachedCluster`` method.
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
                _BaseAttachedClustersRestTransport._BaseCreateAttachedCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_attached_cluster(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseCreateAttachedCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseAttachedClustersRestTransport._BaseCreateAttachedCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseCreateAttachedCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AttachedClustersRestTransport._CreateAttachedCluster._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_attached_cluster(resp)
            return resp

    class _DeleteAttachedCluster(
        _BaseAttachedClustersRestTransport._BaseDeleteAttachedCluster,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.DeleteAttachedCluster")

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
            request: attached_service.DeleteAttachedClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete attached cluster method over HTTP.

            Args:
                request (~.attached_service.DeleteAttachedClusterRequest):
                    The request object. Request message for
                ``AttachedClusters.DeleteAttachedCluster`` method.
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
                _BaseAttachedClustersRestTransport._BaseDeleteAttachedCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_attached_cluster(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseDeleteAttachedCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseDeleteAttachedCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AttachedClustersRestTransport._DeleteAttachedCluster._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_attached_cluster(resp)
            return resp

    class _GenerateAttachedClusterAgentToken(
        _BaseAttachedClustersRestTransport._BaseGenerateAttachedClusterAgentToken,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash(
                "AttachedClustersRestTransport.GenerateAttachedClusterAgentToken"
            )

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
            request: attached_service.GenerateAttachedClusterAgentTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> attached_service.GenerateAttachedClusterAgentTokenResponse:
            r"""Call the generate attached cluster
            agent token method over HTTP.

                Args:
                    request (~.attached_service.GenerateAttachedClusterAgentTokenRequest):
                        The request object.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.attached_service.GenerateAttachedClusterAgentTokenResponse:

            """

            http_options = (
                _BaseAttachedClustersRestTransport._BaseGenerateAttachedClusterAgentToken._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_generate_attached_cluster_agent_token(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseGenerateAttachedClusterAgentToken._get_transcoded_request(
                http_options, request
            )

            body = _BaseAttachedClustersRestTransport._BaseGenerateAttachedClusterAgentToken._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseGenerateAttachedClusterAgentToken._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AttachedClustersRestTransport._GenerateAttachedClusterAgentToken._get_response(
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
            resp = attached_service.GenerateAttachedClusterAgentTokenResponse()
            pb_resp = attached_service.GenerateAttachedClusterAgentTokenResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_attached_cluster_agent_token(resp)
            return resp

    class _GenerateAttachedClusterInstallManifest(
        _BaseAttachedClustersRestTransport._BaseGenerateAttachedClusterInstallManifest,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash(
                "AttachedClustersRestTransport.GenerateAttachedClusterInstallManifest"
            )

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
            request: attached_service.GenerateAttachedClusterInstallManifestRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> attached_service.GenerateAttachedClusterInstallManifestResponse:
            r"""Call the generate attached cluster
            install manifest method over HTTP.

                Args:
                    request (~.attached_service.GenerateAttachedClusterInstallManifestRequest):
                        The request object. Request message for
                    ``AttachedClusters.GenerateAttachedClusterInstallManifest``
                    method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.attached_service.GenerateAttachedClusterInstallManifestResponse:
                        Response message for
                    ``AttachedClusters.GenerateAttachedClusterInstallManifest``
                    method.

            """

            http_options = (
                _BaseAttachedClustersRestTransport._BaseGenerateAttachedClusterInstallManifest._get_http_options()
            )
            (
                request,
                metadata,
            ) = self._interceptor.pre_generate_attached_cluster_install_manifest(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseGenerateAttachedClusterInstallManifest._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseGenerateAttachedClusterInstallManifest._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AttachedClustersRestTransport._GenerateAttachedClusterInstallManifest._get_response(
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
            resp = attached_service.GenerateAttachedClusterInstallManifestResponse()
            pb_resp = (
                attached_service.GenerateAttachedClusterInstallManifestResponse.pb(resp)
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_attached_cluster_install_manifest(
                resp
            )
            return resp

    class _GetAttachedCluster(
        _BaseAttachedClustersRestTransport._BaseGetAttachedCluster,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.GetAttachedCluster")

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
            request: attached_service.GetAttachedClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> attached_resources.AttachedCluster:
            r"""Call the get attached cluster method over HTTP.

            Args:
                request (~.attached_service.GetAttachedClusterRequest):
                    The request object. Request message for
                ``AttachedClusters.GetAttachedCluster`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.attached_resources.AttachedCluster:
                    An Anthos cluster running on customer
                own infrastructure.

            """

            http_options = (
                _BaseAttachedClustersRestTransport._BaseGetAttachedCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_attached_cluster(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseGetAttachedCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseGetAttachedCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AttachedClustersRestTransport._GetAttachedCluster._get_response(
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
            resp = attached_resources.AttachedCluster()
            pb_resp = attached_resources.AttachedCluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_attached_cluster(resp)
            return resp

    class _GetAttachedServerConfig(
        _BaseAttachedClustersRestTransport._BaseGetAttachedServerConfig,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.GetAttachedServerConfig")

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
            request: attached_service.GetAttachedServerConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> attached_resources.AttachedServerConfig:
            r"""Call the get attached server
            config method over HTTP.

                Args:
                    request (~.attached_service.GetAttachedServerConfigRequest):
                        The request object. GetAttachedServerConfigRequest gets
                    the server config for attached clusters.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.attached_resources.AttachedServerConfig:
                        AttachedServerConfig provides
                    information about supported Kubernetes
                    versions

            """

            http_options = (
                _BaseAttachedClustersRestTransport._BaseGetAttachedServerConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_attached_server_config(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseGetAttachedServerConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseGetAttachedServerConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AttachedClustersRestTransport._GetAttachedServerConfig._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = attached_resources.AttachedServerConfig()
            pb_resp = attached_resources.AttachedServerConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_attached_server_config(resp)
            return resp

    class _ImportAttachedCluster(
        _BaseAttachedClustersRestTransport._BaseImportAttachedCluster,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.ImportAttachedCluster")

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
            request: attached_service.ImportAttachedClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the import attached cluster method over HTTP.

            Args:
                request (~.attached_service.ImportAttachedClusterRequest):
                    The request object. Request message for
                ``AttachedClusters.ImportAttachedCluster`` method.
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
                _BaseAttachedClustersRestTransport._BaseImportAttachedCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_import_attached_cluster(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseImportAttachedCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseAttachedClustersRestTransport._BaseImportAttachedCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseImportAttachedCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AttachedClustersRestTransport._ImportAttachedCluster._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_attached_cluster(resp)
            return resp

    class _ListAttachedClusters(
        _BaseAttachedClustersRestTransport._BaseListAttachedClusters,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.ListAttachedClusters")

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
            request: attached_service.ListAttachedClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> attached_service.ListAttachedClustersResponse:
            r"""Call the list attached clusters method over HTTP.

            Args:
                request (~.attached_service.ListAttachedClustersRequest):
                    The request object. Request message for
                ``AttachedClusters.ListAttachedClusters`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.attached_service.ListAttachedClustersResponse:
                    Response message for
                ``AttachedClusters.ListAttachedClusters`` method.

            """

            http_options = (
                _BaseAttachedClustersRestTransport._BaseListAttachedClusters._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_attached_clusters(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseListAttachedClusters._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseListAttachedClusters._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AttachedClustersRestTransport._ListAttachedClusters._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = attached_service.ListAttachedClustersResponse()
            pb_resp = attached_service.ListAttachedClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_attached_clusters(resp)
            return resp

    class _UpdateAttachedCluster(
        _BaseAttachedClustersRestTransport._BaseUpdateAttachedCluster,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.UpdateAttachedCluster")

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
            request: attached_service.UpdateAttachedClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update attached cluster method over HTTP.

            Args:
                request (~.attached_service.UpdateAttachedClusterRequest):
                    The request object. Request message for
                ``AttachedClusters.UpdateAttachedCluster`` method.
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
                _BaseAttachedClustersRestTransport._BaseUpdateAttachedCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_attached_cluster(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseUpdateAttachedCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseAttachedClustersRestTransport._BaseUpdateAttachedCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseUpdateAttachedCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                AttachedClustersRestTransport._UpdateAttachedCluster._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_attached_cluster(resp)
            return resp

    @property
    def create_attached_cluster(
        self,
    ) -> Callable[
        [attached_service.CreateAttachedClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAttachedCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_attached_cluster(
        self,
    ) -> Callable[
        [attached_service.DeleteAttachedClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAttachedCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_attached_cluster_agent_token(
        self,
    ) -> Callable[
        [attached_service.GenerateAttachedClusterAgentTokenRequest],
        attached_service.GenerateAttachedClusterAgentTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateAttachedClusterAgentToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_attached_cluster_install_manifest(
        self,
    ) -> Callable[
        [attached_service.GenerateAttachedClusterInstallManifestRequest],
        attached_service.GenerateAttachedClusterInstallManifestResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateAttachedClusterInstallManifest(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_attached_cluster(
        self,
    ) -> Callable[
        [attached_service.GetAttachedClusterRequest], attached_resources.AttachedCluster
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAttachedCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_attached_server_config(
        self,
    ) -> Callable[
        [attached_service.GetAttachedServerConfigRequest],
        attached_resources.AttachedServerConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAttachedServerConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_attached_cluster(
        self,
    ) -> Callable[
        [attached_service.ImportAttachedClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportAttachedCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_attached_clusters(
        self,
    ) -> Callable[
        [attached_service.ListAttachedClustersRequest],
        attached_service.ListAttachedClustersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAttachedClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_attached_cluster(
        self,
    ) -> Callable[
        [attached_service.UpdateAttachedClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAttachedCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseAttachedClustersRestTransport._BaseCancelOperation,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.CancelOperation")

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
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseAttachedClustersRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseAttachedClustersRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AttachedClustersRestTransport._CancelOperation._get_response(
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

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseAttachedClustersRestTransport._BaseDeleteOperation,
        AttachedClustersRestStub,
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.DeleteOperation")

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
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseAttachedClustersRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseAttachedClustersRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AttachedClustersRestTransport._DeleteOperation._get_response(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseAttachedClustersRestTransport._BaseGetOperation, AttachedClustersRestStub
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.GetOperation")

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
                _BaseAttachedClustersRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseAttachedClustersRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AttachedClustersRestTransport._GetOperation._get_response(
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
        _BaseAttachedClustersRestTransport._BaseListOperations, AttachedClustersRestStub
    ):
        def __hash__(self):
            return hash("AttachedClustersRestTransport.ListOperations")

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
                _BaseAttachedClustersRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseAttachedClustersRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseAttachedClustersRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = AttachedClustersRestTransport._ListOperations._get_response(
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


__all__ = ("AttachedClustersRestTransport",)
