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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import gapic_v1

from google.protobuf import json_format
from google.api_core import operations_v1

from requests import __version__ as requests_version
import dataclasses
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings


from google.cloud.bigtable_admin_v2.types import bigtable_instance_admin
from google.cloud.bigtable_admin_v2.types import instance
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore


from .rest_base import _BaseBigtableInstanceAdminRestTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class BigtableInstanceAdminRestInterceptor:
    """Interceptor for BigtableInstanceAdmin.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BigtableInstanceAdminRestTransport.

    .. code-block:: python
        class MyCustomBigtableInstanceAdminInterceptor(BigtableInstanceAdminRestInterceptor):
            def pre_create_app_profile(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_app_profile(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_app_profile(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_app_profile(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_app_profile(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_app_profiles(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_app_profiles(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_hot_tablets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_hot_tablets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_partial_update_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_partial_update_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_partial_update_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_partial_update_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_app_profile(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_app_profile(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = BigtableInstanceAdminRestTransport(interceptor=MyCustomBigtableInstanceAdminInterceptor())
        client = BigtableInstanceAdminClient(transport=transport)


    """

    def pre_create_app_profile(
        self,
        request: bigtable_instance_admin.CreateAppProfileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_instance_admin.CreateAppProfileRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_app_profile

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_create_app_profile(
        self, response: instance.AppProfile
    ) -> instance.AppProfile:
        """Post-rpc interceptor for create_app_profile

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_create_cluster(
        self,
        request: bigtable_instance_admin.CreateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_instance_admin.CreateClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_create_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_cluster

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_create_instance(
        self,
        request: bigtable_instance_admin.CreateInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_instance_admin.CreateInstanceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_create_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_instance

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_delete_app_profile(
        self,
        request: bigtable_instance_admin.DeleteAppProfileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_instance_admin.DeleteAppProfileRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_app_profile

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def pre_delete_cluster(
        self,
        request: bigtable_instance_admin.DeleteClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_instance_admin.DeleteClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def pre_delete_instance(
        self,
        request: bigtable_instance_admin.DeleteInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_instance_admin.DeleteInstanceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def pre_get_app_profile(
        self,
        request: bigtable_instance_admin.GetAppProfileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_instance_admin.GetAppProfileRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_app_profile

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_get_app_profile(
        self, response: instance.AppProfile
    ) -> instance.AppProfile:
        """Post-rpc interceptor for get_app_profile

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_get_cluster(
        self,
        request: bigtable_instance_admin.GetClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_instance_admin.GetClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_get_cluster(self, response: instance.Cluster) -> instance.Cluster:
        """Post-rpc interceptor for get_cluster

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_get_instance(
        self,
        request: bigtable_instance_admin.GetInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_instance_admin.GetInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_get_instance(self, response: instance.Instance) -> instance.Instance:
        """Post-rpc interceptor for get_instance

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_list_app_profiles(
        self,
        request: bigtable_instance_admin.ListAppProfilesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_instance_admin.ListAppProfilesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_app_profiles

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_list_app_profiles(
        self, response: bigtable_instance_admin.ListAppProfilesResponse
    ) -> bigtable_instance_admin.ListAppProfilesResponse:
        """Post-rpc interceptor for list_app_profiles

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_list_clusters(
        self,
        request: bigtable_instance_admin.ListClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_instance_admin.ListClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_list_clusters(
        self, response: bigtable_instance_admin.ListClustersResponse
    ) -> bigtable_instance_admin.ListClustersResponse:
        """Post-rpc interceptor for list_clusters

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_list_hot_tablets(
        self,
        request: bigtable_instance_admin.ListHotTabletsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_instance_admin.ListHotTabletsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_hot_tablets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_list_hot_tablets(
        self, response: bigtable_instance_admin.ListHotTabletsResponse
    ) -> bigtable_instance_admin.ListHotTabletsResponse:
        """Post-rpc interceptor for list_hot_tablets

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_list_instances(
        self,
        request: bigtable_instance_admin.ListInstancesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_instance_admin.ListInstancesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_list_instances(
        self, response: bigtable_instance_admin.ListInstancesResponse
    ) -> bigtable_instance_admin.ListInstancesResponse:
        """Post-rpc interceptor for list_instances

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_partial_update_cluster(
        self,
        request: bigtable_instance_admin.PartialUpdateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_instance_admin.PartialUpdateClusterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for partial_update_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_partial_update_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for partial_update_cluster

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_partial_update_instance(
        self,
        request: bigtable_instance_admin.PartialUpdateInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_instance_admin.PartialUpdateInstanceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for partial_update_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_partial_update_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for partial_update_instance

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_update_app_profile(
        self,
        request: bigtable_instance_admin.UpdateAppProfileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_instance_admin.UpdateAppProfileRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_app_profile

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_update_app_profile(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_app_profile

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_update_cluster(
        self, request: instance.Cluster, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[instance.Cluster, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_update_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_cluster

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_update_instance(
        self, request: instance.Instance, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[instance.Instance, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableInstanceAdmin server.
        """
        return request, metadata

    def post_update_instance(self, response: instance.Instance) -> instance.Instance:
        """Post-rpc interceptor for update_instance

        Override in a subclass to manipulate the response
        after it is returned by the BigtableInstanceAdmin server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BigtableInstanceAdminRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BigtableInstanceAdminRestInterceptor


class BigtableInstanceAdminRestTransport(_BaseBigtableInstanceAdminRestTransport):
    """REST backend synchronous transport for BigtableInstanceAdmin.

    Service for creating, configuring, and deleting Cloud
    Bigtable Instances and Clusters. Provides access to the Instance
    and Cluster schemas only, not the tables' metadata or data
    stored in those tables.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "bigtableadmin.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[BigtableInstanceAdminRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'bigtableadmin.googleapis.com').
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
        self._interceptor = interceptor or BigtableInstanceAdminRestInterceptor()
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
                        "uri": "/v2/{name=operations/**}:cancel",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v2/{name=operations/**}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=operations/**}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=operations/projects/**}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateAppProfile(
        _BaseBigtableInstanceAdminRestTransport._BaseCreateAppProfile,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.CreateAppProfile")

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
            request: bigtable_instance_admin.CreateAppProfileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> instance.AppProfile:
            r"""Call the create app profile method over HTTP.

            Args:
                request (~.bigtable_instance_admin.CreateAppProfileRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.CreateAppProfile.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.instance.AppProfile:
                    A configuration object describing how
                Cloud Bigtable should treat traffic from
                a particular end user application.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseCreateAppProfile._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_app_profile(
                request, metadata
            )
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseCreateAppProfile._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BaseCreateAppProfile._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseCreateAppProfile._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BigtableInstanceAdminRestTransport._CreateAppProfile._get_response(
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
            resp = instance.AppProfile()
            pb_resp = instance.AppProfile.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_app_profile(resp)
            return resp

    class _CreateCluster(
        _BaseBigtableInstanceAdminRestTransport._BaseCreateCluster,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.CreateCluster")

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
            request: bigtable_instance_admin.CreateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cluster method over HTTP.

            Args:
                request (~.bigtable_instance_admin.CreateClusterRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.CreateCluster.
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
                _BaseBigtableInstanceAdminRestTransport._BaseCreateCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_cluster(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseCreateCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BaseCreateCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseCreateCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._CreateCluster._get_response(
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
            resp = self._interceptor.post_create_cluster(resp)
            return resp

    class _CreateInstance(
        _BaseBigtableInstanceAdminRestTransport._BaseCreateInstance,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.CreateInstance")

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
            request: bigtable_instance_admin.CreateInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create instance method over HTTP.

            Args:
                request (~.bigtable_instance_admin.CreateInstanceRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.CreateInstance.
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
                _BaseBigtableInstanceAdminRestTransport._BaseCreateInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_instance(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseCreateInstance._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BaseCreateInstance._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseCreateInstance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._CreateInstance._get_response(
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

    class _DeleteAppProfile(
        _BaseBigtableInstanceAdminRestTransport._BaseDeleteAppProfile,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.DeleteAppProfile")

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
            request: bigtable_instance_admin.DeleteAppProfileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete app profile method over HTTP.

            Args:
                request (~.bigtable_instance_admin.DeleteAppProfileRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.DeleteAppProfile.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseDeleteAppProfile._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_app_profile(
                request, metadata
            )
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseDeleteAppProfile._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseDeleteAppProfile._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BigtableInstanceAdminRestTransport._DeleteAppProfile._get_response(
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

    class _DeleteCluster(
        _BaseBigtableInstanceAdminRestTransport._BaseDeleteCluster,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.DeleteCluster")

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
            request: bigtable_instance_admin.DeleteClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete cluster method over HTTP.

            Args:
                request (~.bigtable_instance_admin.DeleteClusterRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.DeleteCluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseDeleteCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_cluster(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseDeleteCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseDeleteCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._DeleteCluster._get_response(
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

    class _DeleteInstance(
        _BaseBigtableInstanceAdminRestTransport._BaseDeleteInstance,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.DeleteInstance")

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
            request: bigtable_instance_admin.DeleteInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete instance method over HTTP.

            Args:
                request (~.bigtable_instance_admin.DeleteInstanceRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.DeleteInstance.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseDeleteInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_instance(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseDeleteInstance._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseDeleteInstance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._DeleteInstance._get_response(
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

    class _GetAppProfile(
        _BaseBigtableInstanceAdminRestTransport._BaseGetAppProfile,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.GetAppProfile")

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
            request: bigtable_instance_admin.GetAppProfileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> instance.AppProfile:
            r"""Call the get app profile method over HTTP.

            Args:
                request (~.bigtable_instance_admin.GetAppProfileRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.GetAppProfile.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.instance.AppProfile:
                    A configuration object describing how
                Cloud Bigtable should treat traffic from
                a particular end user application.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseGetAppProfile._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_app_profile(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseGetAppProfile._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseGetAppProfile._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._GetAppProfile._get_response(
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
            resp = instance.AppProfile()
            pb_resp = instance.AppProfile.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_app_profile(resp)
            return resp

    class _GetCluster(
        _BaseBigtableInstanceAdminRestTransport._BaseGetCluster,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.GetCluster")

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
            request: bigtable_instance_admin.GetClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> instance.Cluster:
            r"""Call the get cluster method over HTTP.

            Args:
                request (~.bigtable_instance_admin.GetClusterRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.GetCluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.instance.Cluster:
                    A resizable group of nodes in a particular cloud
                location, capable of serving all
                [Tables][google.bigtable.admin.v2.Table] in the parent
                [Instance][google.bigtable.admin.v2.Instance].

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseGetCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_cluster(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseGetCluster._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseGetCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._GetCluster._get_response(
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
            resp = instance.Cluster()
            pb_resp = instance.Cluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_cluster(resp)
            return resp

    class _GetIamPolicy(
        _BaseBigtableInstanceAdminRestTransport._BaseGetIamPolicy,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.GetIamPolicyRequest):
                    The request object. Request message for ``GetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BaseGetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _GetInstance(
        _BaseBigtableInstanceAdminRestTransport._BaseGetInstance,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.GetInstance")

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
            request: bigtable_instance_admin.GetInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> instance.Instance:
            r"""Call the get instance method over HTTP.

            Args:
                request (~.bigtable_instance_admin.GetInstanceRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.GetInstance.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.instance.Instance:
                    A collection of Bigtable
                [Tables][google.bigtable.admin.v2.Table] and the
                resources that serve them. All tables in an instance are
                served from all
                [Clusters][google.bigtable.admin.v2.Cluster] in the
                instance.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseGetInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_instance(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseGetInstance._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseGetInstance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._GetInstance._get_response(
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
            resp = instance.Instance()
            pb_resp = instance.Instance.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_instance(resp)
            return resp

    class _ListAppProfiles(
        _BaseBigtableInstanceAdminRestTransport._BaseListAppProfiles,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.ListAppProfiles")

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
            request: bigtable_instance_admin.ListAppProfilesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable_instance_admin.ListAppProfilesResponse:
            r"""Call the list app profiles method over HTTP.

            Args:
                request (~.bigtable_instance_admin.ListAppProfilesRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.ListAppProfiles.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable_instance_admin.ListAppProfilesResponse:
                    Response message for
                BigtableInstanceAdmin.ListAppProfiles.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseListAppProfiles._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_app_profiles(
                request, metadata
            )
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseListAppProfiles._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseListAppProfiles._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BigtableInstanceAdminRestTransport._ListAppProfiles._get_response(
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
            resp = bigtable_instance_admin.ListAppProfilesResponse()
            pb_resp = bigtable_instance_admin.ListAppProfilesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_app_profiles(resp)
            return resp

    class _ListClusters(
        _BaseBigtableInstanceAdminRestTransport._BaseListClusters,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.ListClusters")

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
            request: bigtable_instance_admin.ListClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable_instance_admin.ListClustersResponse:
            r"""Call the list clusters method over HTTP.

            Args:
                request (~.bigtable_instance_admin.ListClustersRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.ListClusters.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable_instance_admin.ListClustersResponse:
                    Response message for
                BigtableInstanceAdmin.ListClusters.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseListClusters._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_clusters(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseListClusters._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseListClusters._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._ListClusters._get_response(
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
            resp = bigtable_instance_admin.ListClustersResponse()
            pb_resp = bigtable_instance_admin.ListClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_clusters(resp)
            return resp

    class _ListHotTablets(
        _BaseBigtableInstanceAdminRestTransport._BaseListHotTablets,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.ListHotTablets")

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
            request: bigtable_instance_admin.ListHotTabletsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable_instance_admin.ListHotTabletsResponse:
            r"""Call the list hot tablets method over HTTP.

            Args:
                request (~.bigtable_instance_admin.ListHotTabletsRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.ListHotTablets.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable_instance_admin.ListHotTabletsResponse:
                    Response message for
                BigtableInstanceAdmin.ListHotTablets.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseListHotTablets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_hot_tablets(
                request, metadata
            )
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseListHotTablets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseListHotTablets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._ListHotTablets._get_response(
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
            resp = bigtable_instance_admin.ListHotTabletsResponse()
            pb_resp = bigtable_instance_admin.ListHotTabletsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_hot_tablets(resp)
            return resp

    class _ListInstances(
        _BaseBigtableInstanceAdminRestTransport._BaseListInstances,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.ListInstances")

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
            request: bigtable_instance_admin.ListInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable_instance_admin.ListInstancesResponse:
            r"""Call the list instances method over HTTP.

            Args:
                request (~.bigtable_instance_admin.ListInstancesRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.ListInstances.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable_instance_admin.ListInstancesResponse:
                    Response message for
                BigtableInstanceAdmin.ListInstances.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseListInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_instances(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseListInstances._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseListInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._ListInstances._get_response(
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
            resp = bigtable_instance_admin.ListInstancesResponse()
            pb_resp = bigtable_instance_admin.ListInstancesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_instances(resp)
            return resp

    class _PartialUpdateCluster(
        _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateCluster,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.PartialUpdateCluster")

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
            request: bigtable_instance_admin.PartialUpdateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the partial update cluster method over HTTP.

            Args:
                request (~.bigtable_instance_admin.PartialUpdateClusterRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.PartialUpdateCluster.
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
                _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_partial_update_cluster(
                request, metadata
            )
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BigtableInstanceAdminRestTransport._PartialUpdateCluster._get_response(
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
            resp = self._interceptor.post_partial_update_cluster(resp)
            return resp

    class _PartialUpdateInstance(
        _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateInstance,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.PartialUpdateInstance")

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
            request: bigtable_instance_admin.PartialUpdateInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the partial update instance method over HTTP.

            Args:
                request (~.bigtable_instance_admin.PartialUpdateInstanceRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.PartialUpdateInstance.
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
                _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_partial_update_instance(
                request, metadata
            )
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateInstance._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateInstance._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BasePartialUpdateInstance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BigtableInstanceAdminRestTransport._PartialUpdateInstance._get_response(
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
            resp = self._interceptor.post_partial_update_instance(resp)
            return resp

    class _SetIamPolicy(
        _BaseBigtableInstanceAdminRestTransport._BaseSetIamPolicy,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.SetIamPolicy")

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
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.SetIamPolicyRequest):
                    The request object. Request message for ``SetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.policy_pb2.Policy:
                    An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources.

                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members``, or
                principals, to a single ``role``. Principals can be user
                accounts, service accounts, Google groups, and domains
                (such as G Suite). A ``role`` is a named list of
                permissions; each ``role`` can be an IAM predefined role
                or a user-created custom role.

                For some types of Google Cloud resources, a ``binding``
                can also specify a ``condition``, which is a logical
                expression that allows access to a resource only if the
                expression evaluates to ``true``. A condition can add
                constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.

                **JSON example:**

                ::

                       {
                         "bindings": [
                           {
                             "role": "roles/resourcemanager.organizationAdmin",
                             "members": [
                               "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                             ]
                           },
                           {
                             "role": "roles/resourcemanager.organizationViewer",
                             "members": [
                               "user:eve@example.com"
                             ],
                             "condition": {
                               "title": "expirable access",
                               "description": "Does not grant access after Sep 2020",
                               "expression": "request.time <
                               timestamp('2020-10-01T00:00:00.000Z')",
                             }
                           }
                         ],
                         "etag": "BwWWja0YfJA=",
                         "version": 3
                       }

                **YAML example:**

                ::

                       bindings:
                       - members:
                         - user:mike@example.com
                         - group:admins@example.com
                         - domain:google.com
                         - serviceAccount:my-project-id@appspot.gserviceaccount.com
                         role: roles/resourcemanager.organizationAdmin
                       - members:
                         - user:eve@example.com
                         role: roles/resourcemanager.organizationViewer
                         condition:
                           title: expirable access
                           description: Does not grant access after Sep 2020
                           expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                       etag: BwWWja0YfJA=
                       version: 3

                For a description of IAM and its features, see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._SetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    class _TestIamPermissions(
        _BaseBigtableInstanceAdminRestTransport._BaseTestIamPermissions,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.TestIamPermissions")

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
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.iam_policy_pb2.TestIamPermissionsRequest):
                    The request object. Request message for ``TestIamPermissions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.iam_policy_pb2.TestIamPermissionsResponse:
                    Response message for ``TestIamPermissions`` method.
            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BigtableInstanceAdminRestTransport._TestIamPermissions._get_response(
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
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    class _UpdateAppProfile(
        _BaseBigtableInstanceAdminRestTransport._BaseUpdateAppProfile,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.UpdateAppProfile")

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
            request: bigtable_instance_admin.UpdateAppProfileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update app profile method over HTTP.

            Args:
                request (~.bigtable_instance_admin.UpdateAppProfileRequest):
                    The request object. Request message for
                BigtableInstanceAdmin.UpdateAppProfile.
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
                _BaseBigtableInstanceAdminRestTransport._BaseUpdateAppProfile._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_app_profile(
                request, metadata
            )
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseUpdateAppProfile._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BaseUpdateAppProfile._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseUpdateAppProfile._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BigtableInstanceAdminRestTransport._UpdateAppProfile._get_response(
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
            resp = self._interceptor.post_update_app_profile(resp)
            return resp

    class _UpdateCluster(
        _BaseBigtableInstanceAdminRestTransport._BaseUpdateCluster,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.UpdateCluster")

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
            request: instance.Cluster,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update cluster method over HTTP.

            Args:
                request (~.instance.Cluster):
                    The request object. A resizable group of nodes in a particular cloud
                location, capable of serving all
                [Tables][google.bigtable.admin.v2.Table] in the parent
                [Instance][google.bigtable.admin.v2.Instance].
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
                _BaseBigtableInstanceAdminRestTransport._BaseUpdateCluster._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_cluster(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseUpdateCluster._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BaseUpdateCluster._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseUpdateCluster._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._UpdateCluster._get_response(
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
            resp = self._interceptor.post_update_cluster(resp)
            return resp

    class _UpdateInstance(
        _BaseBigtableInstanceAdminRestTransport._BaseUpdateInstance,
        BigtableInstanceAdminRestStub,
    ):
        def __hash__(self):
            return hash("BigtableInstanceAdminRestTransport.UpdateInstance")

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
            request: instance.Instance,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> instance.Instance:
            r"""Call the update instance method over HTTP.

            Args:
                request (~.instance.Instance):
                    The request object. A collection of Bigtable
                [Tables][google.bigtable.admin.v2.Table] and the
                resources that serve them. All tables in an instance are
                served from all
                [Clusters][google.bigtable.admin.v2.Cluster] in the
                instance.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.instance.Instance:
                    A collection of Bigtable
                [Tables][google.bigtable.admin.v2.Table] and the
                resources that serve them. All tables in an instance are
                served from all
                [Clusters][google.bigtable.admin.v2.Cluster] in the
                instance.

            """

            http_options = (
                _BaseBigtableInstanceAdminRestTransport._BaseUpdateInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_instance(request, metadata)
            transcoded_request = _BaseBigtableInstanceAdminRestTransport._BaseUpdateInstance._get_transcoded_request(
                http_options, request
            )

            body = _BaseBigtableInstanceAdminRestTransport._BaseUpdateInstance._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBigtableInstanceAdminRestTransport._BaseUpdateInstance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BigtableInstanceAdminRestTransport._UpdateInstance._get_response(
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
            resp = instance.Instance()
            pb_resp = instance.Instance.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_instance(resp)
            return resp

    @property
    def create_app_profile(
        self,
    ) -> Callable[
        [bigtable_instance_admin.CreateAppProfileRequest], instance.AppProfile
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAppProfile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_cluster(
        self,
    ) -> Callable[
        [bigtable_instance_admin.CreateClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_instance(
        self,
    ) -> Callable[
        [bigtable_instance_admin.CreateInstanceRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_app_profile(
        self,
    ) -> Callable[[bigtable_instance_admin.DeleteAppProfileRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAppProfile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cluster(
        self,
    ) -> Callable[[bigtable_instance_admin.DeleteClusterRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_instance(
        self,
    ) -> Callable[[bigtable_instance_admin.DeleteInstanceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_app_profile(
        self,
    ) -> Callable[[bigtable_instance_admin.GetAppProfileRequest], instance.AppProfile]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAppProfile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cluster(
        self,
    ) -> Callable[[bigtable_instance_admin.GetClusterRequest], instance.Cluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_instance(
        self,
    ) -> Callable[[bigtable_instance_admin.GetInstanceRequest], instance.Instance]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_app_profiles(
        self,
    ) -> Callable[
        [bigtable_instance_admin.ListAppProfilesRequest],
        bigtable_instance_admin.ListAppProfilesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAppProfiles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_clusters(
        self,
    ) -> Callable[
        [bigtable_instance_admin.ListClustersRequest],
        bigtable_instance_admin.ListClustersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_hot_tablets(
        self,
    ) -> Callable[
        [bigtable_instance_admin.ListHotTabletsRequest],
        bigtable_instance_admin.ListHotTabletsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListHotTablets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_instances(
        self,
    ) -> Callable[
        [bigtable_instance_admin.ListInstancesRequest],
        bigtable_instance_admin.ListInstancesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def partial_update_cluster(
        self,
    ) -> Callable[
        [bigtable_instance_admin.PartialUpdateClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PartialUpdateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def partial_update_instance(
        self,
    ) -> Callable[
        [bigtable_instance_admin.PartialUpdateInstanceRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PartialUpdateInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_app_profile(
        self,
    ) -> Callable[
        [bigtable_instance_admin.UpdateAppProfileRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAppProfile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_cluster(self) -> Callable[[instance.Cluster], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_instance(self) -> Callable[[instance.Instance], instance.Instance]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("BigtableInstanceAdminRestTransport",)
