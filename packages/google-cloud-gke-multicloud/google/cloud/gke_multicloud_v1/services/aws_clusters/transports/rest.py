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

from google.cloud.gke_multicloud_v1.types import aws_resources, aws_service

from .base import AwsClustersTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AwsClustersRestInterceptor:
    """Interceptor for AwsClusters.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AwsClustersRestTransport.

    .. code-block:: python
        class MyCustomAwsClustersInterceptor(AwsClustersRestInterceptor):
            def pre_create_aws_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_aws_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_aws_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_aws_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_aws_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_aws_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_aws_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_aws_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_aws_access_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_aws_access_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_aws_cluster_agent_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_aws_cluster_agent_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_aws_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_aws_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_aws_json_web_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_aws_json_web_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_aws_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_aws_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_aws_open_id_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_aws_open_id_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_aws_server_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_aws_server_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_aws_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_aws_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_aws_node_pools(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_aws_node_pools(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rollback_aws_node_pool_update(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rollback_aws_node_pool_update(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_aws_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_aws_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_aws_node_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_aws_node_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AwsClustersRestTransport(interceptor=MyCustomAwsClustersInterceptor())
        client = AwsClustersClient(transport=transport)


    """

    def pre_create_aws_cluster(
        self,
        request: aws_service.CreateAwsClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.CreateAwsClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_aws_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_create_aws_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_aws_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_create_aws_node_pool(
        self,
        request: aws_service.CreateAwsNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.CreateAwsNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_aws_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_create_aws_node_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_aws_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_delete_aws_cluster(
        self,
        request: aws_service.DeleteAwsClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.DeleteAwsClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_aws_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_delete_aws_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_aws_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_delete_aws_node_pool(
        self,
        request: aws_service.DeleteAwsNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.DeleteAwsNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_aws_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_delete_aws_node_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_aws_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_generate_aws_access_token(
        self,
        request: aws_service.GenerateAwsAccessTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.GenerateAwsAccessTokenRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for generate_aws_access_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_generate_aws_access_token(
        self, response: aws_service.GenerateAwsAccessTokenResponse
    ) -> aws_service.GenerateAwsAccessTokenResponse:
        """Post-rpc interceptor for generate_aws_access_token

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_generate_aws_cluster_agent_token(
        self,
        request: aws_service.GenerateAwsClusterAgentTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        aws_service.GenerateAwsClusterAgentTokenRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for generate_aws_cluster_agent_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_generate_aws_cluster_agent_token(
        self, response: aws_service.GenerateAwsClusterAgentTokenResponse
    ) -> aws_service.GenerateAwsClusterAgentTokenResponse:
        """Post-rpc interceptor for generate_aws_cluster_agent_token

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_aws_cluster(
        self,
        request: aws_service.GetAwsClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.GetAwsClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_aws_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_get_aws_cluster(
        self, response: aws_resources.AwsCluster
    ) -> aws_resources.AwsCluster:
        """Post-rpc interceptor for get_aws_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_aws_json_web_keys(
        self,
        request: aws_service.GetAwsJsonWebKeysRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.GetAwsJsonWebKeysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_aws_json_web_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_get_aws_json_web_keys(
        self, response: aws_resources.AwsJsonWebKeys
    ) -> aws_resources.AwsJsonWebKeys:
        """Post-rpc interceptor for get_aws_json_web_keys

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_aws_node_pool(
        self,
        request: aws_service.GetAwsNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.GetAwsNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_aws_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_get_aws_node_pool(
        self, response: aws_resources.AwsNodePool
    ) -> aws_resources.AwsNodePool:
        """Post-rpc interceptor for get_aws_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_aws_open_id_config(
        self,
        request: aws_service.GetAwsOpenIdConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.GetAwsOpenIdConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_aws_open_id_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_get_aws_open_id_config(
        self, response: aws_resources.AwsOpenIdConfig
    ) -> aws_resources.AwsOpenIdConfig:
        """Post-rpc interceptor for get_aws_open_id_config

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_get_aws_server_config(
        self,
        request: aws_service.GetAwsServerConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.GetAwsServerConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_aws_server_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_get_aws_server_config(
        self, response: aws_resources.AwsServerConfig
    ) -> aws_resources.AwsServerConfig:
        """Post-rpc interceptor for get_aws_server_config

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_list_aws_clusters(
        self,
        request: aws_service.ListAwsClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.ListAwsClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_aws_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_list_aws_clusters(
        self, response: aws_service.ListAwsClustersResponse
    ) -> aws_service.ListAwsClustersResponse:
        """Post-rpc interceptor for list_aws_clusters

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_list_aws_node_pools(
        self,
        request: aws_service.ListAwsNodePoolsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.ListAwsNodePoolsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_aws_node_pools

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_list_aws_node_pools(
        self, response: aws_service.ListAwsNodePoolsResponse
    ) -> aws_service.ListAwsNodePoolsResponse:
        """Post-rpc interceptor for list_aws_node_pools

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_rollback_aws_node_pool_update(
        self,
        request: aws_service.RollbackAwsNodePoolUpdateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.RollbackAwsNodePoolUpdateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rollback_aws_node_pool_update

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_rollback_aws_node_pool_update(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for rollback_aws_node_pool_update

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_update_aws_cluster(
        self,
        request: aws_service.UpdateAwsClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.UpdateAwsClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_aws_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_update_aws_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_aws_cluster

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response

    def pre_update_aws_node_pool(
        self,
        request: aws_service.UpdateAwsNodePoolRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[aws_service.UpdateAwsNodePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_aws_node_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_update_aws_node_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_aws_node_pool

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
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
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
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
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
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
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
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
        before they are sent to the AwsClusters server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the AwsClusters server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AwsClustersRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AwsClustersRestInterceptor


class AwsClustersRestTransport(AwsClustersTransport):
    """REST backend transport for AwsClusters.

    The AwsClusters API provides a single centrally managed
    service to create and manage Anthos clusters that run on AWS
    infrastructure.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    NOTE: This REST transport functionality is currently in a beta
    state (preview). We welcome your feedback via an issue in this
    library's source repository. Thank you!
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
        interceptor: Optional[AwsClustersRestInterceptor] = None,
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
        self._interceptor = interceptor or AwsClustersRestInterceptor()
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

    class _CreateAwsCluster(AwsClustersRestStub):
        def __hash__(self):
            return hash("CreateAwsCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "awsClusterId": "",
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
            request: aws_service.CreateAwsClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create aws cluster method over HTTP.

            Args:
                request (~.aws_service.CreateAwsClusterRequest):
                    The request object. Request message for ``AwsClusters.CreateAwsCluster``
                method.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/awsClusters",
                    "body": "aws_cluster",
                },
            ]
            request, metadata = self._interceptor.pre_create_aws_cluster(
                request, metadata
            )
            pb_request = aws_service.CreateAwsClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_create_aws_cluster(resp)
            return resp

    class _CreateAwsNodePool(AwsClustersRestStub):
        def __hash__(self):
            return hash("CreateAwsNodePool")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "awsNodePoolId": "",
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
            request: aws_service.CreateAwsNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create aws node pool method over HTTP.

            Args:
                request (~.aws_service.CreateAwsNodePoolRequest):
                    The request object. Response message for ``AwsClusters.CreateAwsNodePool``
                method.
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
                    "uri": "/v1/{parent=projects/*/locations/*/awsClusters/*}/awsNodePools",
                    "body": "aws_node_pool",
                },
            ]
            request, metadata = self._interceptor.pre_create_aws_node_pool(
                request, metadata
            )
            pb_request = aws_service.CreateAwsNodePoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_create_aws_node_pool(resp)
            return resp

    class _DeleteAwsCluster(AwsClustersRestStub):
        def __hash__(self):
            return hash("DeleteAwsCluster")

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
            request: aws_service.DeleteAwsClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete aws cluster method over HTTP.

            Args:
                request (~.aws_service.DeleteAwsClusterRequest):
                    The request object. Request message for ``AwsClusters.DeleteAwsCluster``
                method.
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
                    "uri": "/v1/{name=projects/*/locations/*/awsClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_aws_cluster(
                request, metadata
            )
            pb_request = aws_service.DeleteAwsClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_delete_aws_cluster(resp)
            return resp

    class _DeleteAwsNodePool(AwsClustersRestStub):
        def __hash__(self):
            return hash("DeleteAwsNodePool")

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
            request: aws_service.DeleteAwsNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete aws node pool method over HTTP.

            Args:
                request (~.aws_service.DeleteAwsNodePoolRequest):
                    The request object. Request message for ``AwsClusters.DeleteAwsNodePool``
                method.
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
                    "uri": "/v1/{name=projects/*/locations/*/awsClusters/*/awsNodePools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_aws_node_pool(
                request, metadata
            )
            pb_request = aws_service.DeleteAwsNodePoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_delete_aws_node_pool(resp)
            return resp

    class _GenerateAwsAccessToken(AwsClustersRestStub):
        def __hash__(self):
            return hash("GenerateAwsAccessToken")

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
            request: aws_service.GenerateAwsAccessTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> aws_service.GenerateAwsAccessTokenResponse:
            r"""Call the generate aws access token method over HTTP.

            Args:
                request (~.aws_service.GenerateAwsAccessTokenRequest):
                    The request object. Request message for
                ``AwsClusters.GenerateAwsAccessToken`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.aws_service.GenerateAwsAccessTokenResponse:
                    Response message for
                ``AwsClusters.GenerateAwsAccessToken`` method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{aws_cluster=projects/*/locations/*/awsClusters/*}:generateAwsAccessToken",
                },
            ]
            request, metadata = self._interceptor.pre_generate_aws_access_token(
                request, metadata
            )
            pb_request = aws_service.GenerateAwsAccessTokenRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = aws_service.GenerateAwsAccessTokenResponse()
            pb_resp = aws_service.GenerateAwsAccessTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_aws_access_token(resp)
            return resp

    class _GenerateAwsClusterAgentToken(AwsClustersRestStub):
        def __hash__(self):
            return hash("GenerateAwsClusterAgentToken")

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
            request: aws_service.GenerateAwsClusterAgentTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> aws_service.GenerateAwsClusterAgentTokenResponse:
            r"""Call the generate aws cluster
            agent token method over HTTP.

                Args:
                    request (~.aws_service.GenerateAwsClusterAgentTokenRequest):
                        The request object.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.aws_service.GenerateAwsClusterAgentTokenResponse:

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{aws_cluster=projects/*/locations/*/awsClusters/*}:generateAwsClusterAgentToken",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_generate_aws_cluster_agent_token(
                request, metadata
            )
            pb_request = aws_service.GenerateAwsClusterAgentTokenRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = aws_service.GenerateAwsClusterAgentTokenResponse()
            pb_resp = aws_service.GenerateAwsClusterAgentTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_aws_cluster_agent_token(resp)
            return resp

    class _GetAwsCluster(AwsClustersRestStub):
        def __hash__(self):
            return hash("GetAwsCluster")

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
            request: aws_service.GetAwsClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> aws_resources.AwsCluster:
            r"""Call the get aws cluster method over HTTP.

            Args:
                request (~.aws_service.GetAwsClusterRequest):
                    The request object. Request message for ``AwsClusters.GetAwsCluster``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.aws_resources.AwsCluster:
                    An Anthos cluster running on AWS.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/awsClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_aws_cluster(request, metadata)
            pb_request = aws_service.GetAwsClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = aws_resources.AwsCluster()
            pb_resp = aws_resources.AwsCluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_aws_cluster(resp)
            return resp

    class _GetAwsJsonWebKeys(AwsClustersRestStub):
        def __hash__(self):
            return hash("GetAwsJsonWebKeys")

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
            request: aws_service.GetAwsJsonWebKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> aws_resources.AwsJsonWebKeys:
            r"""Call the get aws json web keys method over HTTP.

            Args:
                request (~.aws_service.GetAwsJsonWebKeysRequest):
                    The request object. GetAwsJsonWebKeysRequest gets the public component of
                the keys used by the cluster to sign token requests.
                This will be the jwks_uri for the discover document
                returned by getOpenIDConfig. See the OpenID Connect
                Discovery 1.0 specification for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.aws_resources.AwsJsonWebKeys:
                    AwsJsonWebKeys is a valid JSON Web
                Key Set as specififed in RFC 7517.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{aws_cluster=projects/*/locations/*/awsClusters/*}/jwks",
                },
            ]
            request, metadata = self._interceptor.pre_get_aws_json_web_keys(
                request, metadata
            )
            pb_request = aws_service.GetAwsJsonWebKeysRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = aws_resources.AwsJsonWebKeys()
            pb_resp = aws_resources.AwsJsonWebKeys.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_aws_json_web_keys(resp)
            return resp

    class _GetAwsNodePool(AwsClustersRestStub):
        def __hash__(self):
            return hash("GetAwsNodePool")

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
            request: aws_service.GetAwsNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> aws_resources.AwsNodePool:
            r"""Call the get aws node pool method over HTTP.

            Args:
                request (~.aws_service.GetAwsNodePoolRequest):
                    The request object. Request message for ``AwsClusters.GetAwsNodePool``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.aws_resources.AwsNodePool:
                    An Anthos node pool running on AWS.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/awsClusters/*/awsNodePools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_aws_node_pool(
                request, metadata
            )
            pb_request = aws_service.GetAwsNodePoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = aws_resources.AwsNodePool()
            pb_resp = aws_resources.AwsNodePool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_aws_node_pool(resp)
            return resp

    class _GetAwsOpenIdConfig(AwsClustersRestStub):
        def __hash__(self):
            return hash("GetAwsOpenIdConfig")

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
            request: aws_service.GetAwsOpenIdConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> aws_resources.AwsOpenIdConfig:
            r"""Call the get aws open id config method over HTTP.

            Args:
                request (~.aws_service.GetAwsOpenIdConfigRequest):
                    The request object. GetAwsOpenIdConfigRequest gets the
                OIDC discovery document for the cluster.
                See the OpenID Connect Discovery 1.0
                specification for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.aws_resources.AwsOpenIdConfig:
                    AwsOpenIdConfig is an OIDC discovery
                document for the cluster. See the OpenID
                Connect Discovery 1.0 specification for
                details.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{aws_cluster=projects/*/locations/*/awsClusters/*}/.well-known/openid-configuration",
                },
            ]
            request, metadata = self._interceptor.pre_get_aws_open_id_config(
                request, metadata
            )
            pb_request = aws_service.GetAwsOpenIdConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = aws_resources.AwsOpenIdConfig()
            pb_resp = aws_resources.AwsOpenIdConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_aws_open_id_config(resp)
            return resp

    class _GetAwsServerConfig(AwsClustersRestStub):
        def __hash__(self):
            return hash("GetAwsServerConfig")

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
            request: aws_service.GetAwsServerConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> aws_resources.AwsServerConfig:
            r"""Call the get aws server config method over HTTP.

            Args:
                request (~.aws_service.GetAwsServerConfigRequest):
                    The request object. GetAwsServerConfigRequest gets the
                server config of GKE cluster on AWS.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.aws_resources.AwsServerConfig:
                    AwsServerConfig is the configuration
                of GKE cluster on AWS.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/awsServerConfig}",
                },
            ]
            request, metadata = self._interceptor.pre_get_aws_server_config(
                request, metadata
            )
            pb_request = aws_service.GetAwsServerConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = aws_resources.AwsServerConfig()
            pb_resp = aws_resources.AwsServerConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_aws_server_config(resp)
            return resp

    class _ListAwsClusters(AwsClustersRestStub):
        def __hash__(self):
            return hash("ListAwsClusters")

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
            request: aws_service.ListAwsClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> aws_service.ListAwsClustersResponse:
            r"""Call the list aws clusters method over HTTP.

            Args:
                request (~.aws_service.ListAwsClustersRequest):
                    The request object. Request message for ``AwsClusters.ListAwsClusters``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.aws_service.ListAwsClustersResponse:
                    Response message for ``AwsClusters.ListAwsClusters``
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/awsClusters",
                },
            ]
            request, metadata = self._interceptor.pre_list_aws_clusters(
                request, metadata
            )
            pb_request = aws_service.ListAwsClustersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = aws_service.ListAwsClustersResponse()
            pb_resp = aws_service.ListAwsClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_aws_clusters(resp)
            return resp

    class _ListAwsNodePools(AwsClustersRestStub):
        def __hash__(self):
            return hash("ListAwsNodePools")

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
            request: aws_service.ListAwsNodePoolsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> aws_service.ListAwsNodePoolsResponse:
            r"""Call the list aws node pools method over HTTP.

            Args:
                request (~.aws_service.ListAwsNodePoolsRequest):
                    The request object. Request message for ``AwsClusters.ListAwsNodePools``
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.aws_service.ListAwsNodePoolsResponse:
                    Response message for ``AwsClusters.ListAwsNodePools``
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/awsClusters/*}/awsNodePools",
                },
            ]
            request, metadata = self._interceptor.pre_list_aws_node_pools(
                request, metadata
            )
            pb_request = aws_service.ListAwsNodePoolsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = aws_service.ListAwsNodePoolsResponse()
            pb_resp = aws_service.ListAwsNodePoolsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_aws_node_pools(resp)
            return resp

    class _RollbackAwsNodePoolUpdate(AwsClustersRestStub):
        def __hash__(self):
            return hash("RollbackAwsNodePoolUpdate")

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
            request: aws_service.RollbackAwsNodePoolUpdateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the rollback aws node pool
            update method over HTTP.

                Args:
                    request (~.aws_service.RollbackAwsNodePoolUpdateRequest):
                        The request object. Request message for
                    ``AwsClusters.RollbackAwsNodePoolUpdate`` method.
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
                    "uri": "/v1/{name=projects/*/locations/*/awsClusters/*/awsNodePools/*}:rollback",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rollback_aws_node_pool_update(
                request, metadata
            )
            pb_request = aws_service.RollbackAwsNodePoolUpdateRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_rollback_aws_node_pool_update(resp)
            return resp

    class _UpdateAwsCluster(AwsClustersRestStub):
        def __hash__(self):
            return hash("UpdateAwsCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: aws_service.UpdateAwsClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update aws cluster method over HTTP.

            Args:
                request (~.aws_service.UpdateAwsClusterRequest):
                    The request object. Request message for ``AwsClusters.UpdateAwsCluster``
                method.
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
                    "method": "patch",
                    "uri": "/v1/{aws_cluster.name=projects/*/locations/*/awsClusters/*}",
                    "body": "aws_cluster",
                },
            ]
            request, metadata = self._interceptor.pre_update_aws_cluster(
                request, metadata
            )
            pb_request = aws_service.UpdateAwsClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_update_aws_cluster(resp)
            return resp

    class _UpdateAwsNodePool(AwsClustersRestStub):
        def __hash__(self):
            return hash("UpdateAwsNodePool")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
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
            request: aws_service.UpdateAwsNodePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update aws node pool method over HTTP.

            Args:
                request (~.aws_service.UpdateAwsNodePoolRequest):
                    The request object. Request message for ``AwsClusters.UpdateAwsNodePool``
                method.
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
                    "method": "patch",
                    "uri": "/v1/{aws_node_pool.name=projects/*/locations/*/awsClusters/*/awsNodePools/*}",
                    "body": "aws_node_pool",
                },
            ]
            request, metadata = self._interceptor.pre_update_aws_node_pool(
                request, metadata
            )
            pb_request = aws_service.UpdateAwsNodePoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

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
            resp = self._interceptor.post_update_aws_node_pool(resp)
            return resp

    @property
    def create_aws_cluster(
        self,
    ) -> Callable[[aws_service.CreateAwsClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAwsCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_aws_node_pool(
        self,
    ) -> Callable[[aws_service.CreateAwsNodePoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAwsNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_aws_cluster(
        self,
    ) -> Callable[[aws_service.DeleteAwsClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAwsCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_aws_node_pool(
        self,
    ) -> Callable[[aws_service.DeleteAwsNodePoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAwsNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_aws_access_token(
        self,
    ) -> Callable[
        [aws_service.GenerateAwsAccessTokenRequest],
        aws_service.GenerateAwsAccessTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateAwsAccessToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_aws_cluster_agent_token(
        self,
    ) -> Callable[
        [aws_service.GenerateAwsClusterAgentTokenRequest],
        aws_service.GenerateAwsClusterAgentTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateAwsClusterAgentToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_aws_cluster(
        self,
    ) -> Callable[[aws_service.GetAwsClusterRequest], aws_resources.AwsCluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAwsCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_aws_json_web_keys(
        self,
    ) -> Callable[[aws_service.GetAwsJsonWebKeysRequest], aws_resources.AwsJsonWebKeys]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAwsJsonWebKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_aws_node_pool(
        self,
    ) -> Callable[[aws_service.GetAwsNodePoolRequest], aws_resources.AwsNodePool]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAwsNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_aws_open_id_config(
        self,
    ) -> Callable[
        [aws_service.GetAwsOpenIdConfigRequest], aws_resources.AwsOpenIdConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAwsOpenIdConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_aws_server_config(
        self,
    ) -> Callable[
        [aws_service.GetAwsServerConfigRequest], aws_resources.AwsServerConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAwsServerConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_aws_clusters(
        self,
    ) -> Callable[
        [aws_service.ListAwsClustersRequest], aws_service.ListAwsClustersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAwsClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_aws_node_pools(
        self,
    ) -> Callable[
        [aws_service.ListAwsNodePoolsRequest], aws_service.ListAwsNodePoolsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAwsNodePools(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rollback_aws_node_pool_update(
        self,
    ) -> Callable[
        [aws_service.RollbackAwsNodePoolUpdateRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RollbackAwsNodePoolUpdate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_aws_cluster(
        self,
    ) -> Callable[[aws_service.UpdateAwsClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAwsCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_aws_node_pool(
        self,
    ) -> Callable[[aws_service.UpdateAwsNodePoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAwsNodePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(AwsClustersRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(AwsClustersRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(AwsClustersRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(AwsClustersRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AwsClustersRestTransport",)
