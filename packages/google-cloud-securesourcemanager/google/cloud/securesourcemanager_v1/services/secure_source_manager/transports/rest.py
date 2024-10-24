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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.securesourcemanager_v1.types import secure_source_manager

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseSecureSourceManagerRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class SecureSourceManagerRestInterceptor:
    """Interceptor for SecureSourceManager.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SecureSourceManagerRestTransport.

    .. code-block:: python
        class MyCustomSecureSourceManagerInterceptor(SecureSourceManagerRestInterceptor):
            def pre_create_branch_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_branch_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_branch_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_branch_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_branch_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_branch_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy_repo(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy_repo(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_repository(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_repository(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_branch_rules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_branch_rules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_repositories(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_repositories(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy_repo(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy_repo(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions_repo(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions_repo(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_branch_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_branch_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SecureSourceManagerRestTransport(interceptor=MyCustomSecureSourceManagerInterceptor())
        client = SecureSourceManagerClient(transport=transport)


    """

    def pre_create_branch_rule(
        self,
        request: secure_source_manager.CreateBranchRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        secure_source_manager.CreateBranchRuleRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_branch_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_create_branch_rule(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_branch_rule

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_instance(
        self,
        request: secure_source_manager.CreateInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[secure_source_manager.CreateInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_create_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_instance

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_create_repository(
        self,
        request: secure_source_manager.CreateRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        secure_source_manager.CreateRepositoryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_create_repository(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_repository

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_branch_rule(
        self,
        request: secure_source_manager.DeleteBranchRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        secure_source_manager.DeleteBranchRuleRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_branch_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_delete_branch_rule(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_branch_rule

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_instance(
        self,
        request: secure_source_manager.DeleteInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[secure_source_manager.DeleteInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_delete_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_instance

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_delete_repository(
        self,
        request: secure_source_manager.DeleteRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        secure_source_manager.DeleteRepositoryRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_delete_repository(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_repository

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_branch_rule(
        self,
        request: secure_source_manager.GetBranchRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[secure_source_manager.GetBranchRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_branch_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_get_branch_rule(
        self, response: secure_source_manager.BranchRule
    ) -> secure_source_manager.BranchRule:
        """Post-rpc interceptor for get_branch_rule

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy_repo(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy_repo

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_get_iam_policy_repo(
        self, response: policy_pb2.Policy
    ) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy_repo

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_instance(
        self,
        request: secure_source_manager.GetInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[secure_source_manager.GetInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_get_instance(
        self, response: secure_source_manager.Instance
    ) -> secure_source_manager.Instance:
        """Post-rpc interceptor for get_instance

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_repository(
        self,
        request: secure_source_manager.GetRepositoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[secure_source_manager.GetRepositoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_repository

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_get_repository(
        self, response: secure_source_manager.Repository
    ) -> secure_source_manager.Repository:
        """Post-rpc interceptor for get_repository

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_branch_rules(
        self,
        request: secure_source_manager.ListBranchRulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[secure_source_manager.ListBranchRulesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_branch_rules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_list_branch_rules(
        self, response: secure_source_manager.ListBranchRulesResponse
    ) -> secure_source_manager.ListBranchRulesResponse:
        """Post-rpc interceptor for list_branch_rules

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_instances(
        self,
        request: secure_source_manager.ListInstancesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[secure_source_manager.ListInstancesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_list_instances(
        self, response: secure_source_manager.ListInstancesResponse
    ) -> secure_source_manager.ListInstancesResponse:
        """Post-rpc interceptor for list_instances

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_list_repositories(
        self,
        request: secure_source_manager.ListRepositoriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        secure_source_manager.ListRepositoriesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_repositories

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_list_repositories(
        self, response: secure_source_manager.ListRepositoriesResponse
    ) -> secure_source_manager.ListRepositoriesResponse:
        """Post-rpc interceptor for list_repositories

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy_repo(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy_repo

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_set_iam_policy_repo(
        self, response: policy_pb2.Policy
    ) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy_repo

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions_repo(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions_repo

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_test_iam_permissions_repo(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions_repo

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_update_branch_rule(
        self,
        request: secure_source_manager.UpdateBranchRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        secure_source_manager.UpdateBranchRuleRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_branch_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_update_branch_rule(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_branch_rule

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
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
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
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
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
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
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
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
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
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
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
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
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
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
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
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
        before they are sent to the SecureSourceManager server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the SecureSourceManager server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SecureSourceManagerRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SecureSourceManagerRestInterceptor


class SecureSourceManagerRestTransport(_BaseSecureSourceManagerRestTransport):
    """REST backend synchronous transport for SecureSourceManager.

    Secure Source Manager API

    Access Secure Source Manager instances, resources, and repositories.

    This API is split across two servers: the Control Plane and the Data
    Plane.

    Data Plane endpoints are hosted directly by your Secure Source
    Manager instance, so you must connect to your instance's API
    hostname to access them. The API hostname looks like the following:

    ::

       https://[instance-id]-[project-number]-api.[location].sourcemanager.dev

    For example,

    ::

       https://my-instance-702770452863-api.us-central1.sourcemanager.dev

    Data Plane endpoints are denoted with **Host: Data Plane**.

    All other endpoints are found in the normal Cloud API location,
    namely, ``securcesourcemanager.googleapis.com``.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "securesourcemanager.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SecureSourceManagerRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'securesourcemanager.googleapis.com').
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
        self._interceptor = interceptor or SecureSourceManagerRestInterceptor()
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

    class _CreateBranchRule(
        _BaseSecureSourceManagerRestTransport._BaseCreateBranchRule,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.CreateBranchRule")

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
            request: secure_source_manager.CreateBranchRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create branch rule method over HTTP.

            Args:
                request (~.secure_source_manager.CreateBranchRuleRequest):
                    The request object. CreateBranchRuleRequest is the
                request to create a branch rule.
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
                _BaseSecureSourceManagerRestTransport._BaseCreateBranchRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_branch_rule(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseCreateBranchRule._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecureSourceManagerRestTransport._BaseCreateBranchRule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseCreateBranchRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._CreateBranchRule._get_response(
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
            resp = self._interceptor.post_create_branch_rule(resp)
            return resp

    class _CreateInstance(
        _BaseSecureSourceManagerRestTransport._BaseCreateInstance,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.CreateInstance")

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
            request: secure_source_manager.CreateInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create instance method over HTTP.

            Args:
                request (~.secure_source_manager.CreateInstanceRequest):
                    The request object. CreateInstanceRequest is the request
                for creating an instance.
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
                _BaseSecureSourceManagerRestTransport._BaseCreateInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_instance(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseCreateInstance._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecureSourceManagerRestTransport._BaseCreateInstance._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseCreateInstance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._CreateInstance._get_response(
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

    class _CreateRepository(
        _BaseSecureSourceManagerRestTransport._BaseCreateRepository,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.CreateRepository")

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
            request: secure_source_manager.CreateRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create repository method over HTTP.

            Args:
                request (~.secure_source_manager.CreateRepositoryRequest):
                    The request object. CreateRepositoryRequest is the
                request for creating a repository.
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
                _BaseSecureSourceManagerRestTransport._BaseCreateRepository._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_repository(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseCreateRepository._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecureSourceManagerRestTransport._BaseCreateRepository._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseCreateRepository._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._CreateRepository._get_response(
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
            resp = self._interceptor.post_create_repository(resp)
            return resp

    class _DeleteBranchRule(
        _BaseSecureSourceManagerRestTransport._BaseDeleteBranchRule,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.DeleteBranchRule")

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
            request: secure_source_manager.DeleteBranchRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete branch rule method over HTTP.

            Args:
                request (~.secure_source_manager.DeleteBranchRuleRequest):
                    The request object. DeleteBranchRuleRequest is the
                request to delete a branch rule.
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
                _BaseSecureSourceManagerRestTransport._BaseDeleteBranchRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_branch_rule(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseDeleteBranchRule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseDeleteBranchRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._DeleteBranchRule._get_response(
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
            resp = self._interceptor.post_delete_branch_rule(resp)
            return resp

    class _DeleteInstance(
        _BaseSecureSourceManagerRestTransport._BaseDeleteInstance,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.DeleteInstance")

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
            request: secure_source_manager.DeleteInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete instance method over HTTP.

            Args:
                request (~.secure_source_manager.DeleteInstanceRequest):
                    The request object. DeleteInstanceRequest is the request
                for deleting an instance.
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
                _BaseSecureSourceManagerRestTransport._BaseDeleteInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_instance(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseDeleteInstance._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseDeleteInstance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._DeleteInstance._get_response(
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

    class _DeleteRepository(
        _BaseSecureSourceManagerRestTransport._BaseDeleteRepository,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.DeleteRepository")

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
            request: secure_source_manager.DeleteRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete repository method over HTTP.

            Args:
                request (~.secure_source_manager.DeleteRepositoryRequest):
                    The request object. DeleteRepositoryRequest is the
                request to delete a repository.
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
                _BaseSecureSourceManagerRestTransport._BaseDeleteRepository._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_repository(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseDeleteRepository._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseDeleteRepository._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._DeleteRepository._get_response(
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
            resp = self._interceptor.post_delete_repository(resp)
            return resp

    class _GetBranchRule(
        _BaseSecureSourceManagerRestTransport._BaseGetBranchRule,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.GetBranchRule")

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
            request: secure_source_manager.GetBranchRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> secure_source_manager.BranchRule:
            r"""Call the get branch rule method over HTTP.

            Args:
                request (~.secure_source_manager.GetBranchRuleRequest):
                    The request object. GetBranchRuleRequest is the request
                for getting a branch rule.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.secure_source_manager.BranchRule:
                    Metadata of a BranchRule. BranchRule
                is the protection rule to enforce
                pre-defined rules on desginated branches
                within a repository.

            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseGetBranchRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_branch_rule(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseGetBranchRule._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseGetBranchRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._GetBranchRule._get_response(
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
            resp = secure_source_manager.BranchRule()
            pb_resp = secure_source_manager.BranchRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_branch_rule(resp)
            return resp

    class _GetIamPolicyRepo(
        _BaseSecureSourceManagerRestTransport._BaseGetIamPolicyRepo,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.GetIamPolicyRepo")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy repo method over HTTP.

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
                _BaseSecureSourceManagerRestTransport._BaseGetIamPolicyRepo._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy_repo(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseGetIamPolicyRepo._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseGetIamPolicyRepo._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._GetIamPolicyRepo._get_response(
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy_repo(resp)
            return resp

    class _GetInstance(
        _BaseSecureSourceManagerRestTransport._BaseGetInstance,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.GetInstance")

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
            request: secure_source_manager.GetInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> secure_source_manager.Instance:
            r"""Call the get instance method over HTTP.

            Args:
                request (~.secure_source_manager.GetInstanceRequest):
                    The request object. GetInstanceRequest is the request for
                getting an instance.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.secure_source_manager.Instance:
                    A resource that represents a Secure
                Source Manager instance.

            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseGetInstance._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_instance(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseGetInstance._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseGetInstance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._GetInstance._get_response(
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
            resp = secure_source_manager.Instance()
            pb_resp = secure_source_manager.Instance.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_instance(resp)
            return resp

    class _GetRepository(
        _BaseSecureSourceManagerRestTransport._BaseGetRepository,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.GetRepository")

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
            request: secure_source_manager.GetRepositoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> secure_source_manager.Repository:
            r"""Call the get repository method over HTTP.

            Args:
                request (~.secure_source_manager.GetRepositoryRequest):
                    The request object. GetRepositoryRequest is the request
                for getting a repository.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.secure_source_manager.Repository:
                    Metadata of a Secure Source Manager
                repository.

            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseGetRepository._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_repository(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseGetRepository._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseGetRepository._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._GetRepository._get_response(
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
            resp = secure_source_manager.Repository()
            pb_resp = secure_source_manager.Repository.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_repository(resp)
            return resp

    class _ListBranchRules(
        _BaseSecureSourceManagerRestTransport._BaseListBranchRules,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.ListBranchRules")

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
            request: secure_source_manager.ListBranchRulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> secure_source_manager.ListBranchRulesResponse:
            r"""Call the list branch rules method over HTTP.

            Args:
                request (~.secure_source_manager.ListBranchRulesRequest):
                    The request object. ListBranchRulesRequest is the request
                to list branch rules.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.secure_source_manager.ListBranchRulesResponse:
                    ListBranchRulesResponse is the
                response to listing branchRules.

            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseListBranchRules._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_branch_rules(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseListBranchRules._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseListBranchRules._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._ListBranchRules._get_response(
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
            resp = secure_source_manager.ListBranchRulesResponse()
            pb_resp = secure_source_manager.ListBranchRulesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_branch_rules(resp)
            return resp

    class _ListInstances(
        _BaseSecureSourceManagerRestTransport._BaseListInstances,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.ListInstances")

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
            request: secure_source_manager.ListInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> secure_source_manager.ListInstancesResponse:
            r"""Call the list instances method over HTTP.

            Args:
                request (~.secure_source_manager.ListInstancesRequest):
                    The request object. ListInstancesRequest is the request
                to list instances.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.secure_source_manager.ListInstancesResponse:

            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseListInstances._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_instances(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseListInstances._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseListInstances._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._ListInstances._get_response(
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
            resp = secure_source_manager.ListInstancesResponse()
            pb_resp = secure_source_manager.ListInstancesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_instances(resp)
            return resp

    class _ListRepositories(
        _BaseSecureSourceManagerRestTransport._BaseListRepositories,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.ListRepositories")

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
            request: secure_source_manager.ListRepositoriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> secure_source_manager.ListRepositoriesResponse:
            r"""Call the list repositories method over HTTP.

            Args:
                request (~.secure_source_manager.ListRepositoriesRequest):
                    The request object. ListRepositoriesRequest is request to
                list repositories.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.secure_source_manager.ListRepositoriesResponse:

            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseListRepositories._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_repositories(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseListRepositories._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseListRepositories._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._ListRepositories._get_response(
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
            resp = secure_source_manager.ListRepositoriesResponse()
            pb_resp = secure_source_manager.ListRepositoriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_repositories(resp)
            return resp

    class _SetIamPolicyRepo(
        _BaseSecureSourceManagerRestTransport._BaseSetIamPolicyRepo,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.SetIamPolicyRepo")

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
            r"""Call the set iam policy repo method over HTTP.

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
                _BaseSecureSourceManagerRestTransport._BaseSetIamPolicyRepo._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy_repo(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseSetIamPolicyRepo._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecureSourceManagerRestTransport._BaseSetIamPolicyRepo._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseSetIamPolicyRepo._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._SetIamPolicyRepo._get_response(
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
            resp = self._interceptor.post_set_iam_policy_repo(resp)
            return resp

    class _TestIamPermissionsRepo(
        _BaseSecureSourceManagerRestTransport._BaseTestIamPermissionsRepo,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.TestIamPermissionsRepo")

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
            r"""Call the test iam permissions repo method over HTTP.

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
                _BaseSecureSourceManagerRestTransport._BaseTestIamPermissionsRepo._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions_repo(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseTestIamPermissionsRepo._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecureSourceManagerRestTransport._BaseTestIamPermissionsRepo._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseTestIamPermissionsRepo._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecureSourceManagerRestTransport._TestIamPermissionsRepo._get_response(
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
            resp = self._interceptor.post_test_iam_permissions_repo(resp)
            return resp

    class _UpdateBranchRule(
        _BaseSecureSourceManagerRestTransport._BaseUpdateBranchRule,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.UpdateBranchRule")

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
            request: secure_source_manager.UpdateBranchRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update branch rule method over HTTP.

            Args:
                request (~.secure_source_manager.UpdateBranchRuleRequest):
                    The request object. UpdateBranchRuleRequest is the
                request to update a branchRule.
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
                _BaseSecureSourceManagerRestTransport._BaseUpdateBranchRule._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_branch_rule(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseUpdateBranchRule._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecureSourceManagerRestTransport._BaseUpdateBranchRule._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseUpdateBranchRule._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._UpdateBranchRule._get_response(
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
            resp = self._interceptor.post_update_branch_rule(resp)
            return resp

    @property
    def create_branch_rule(
        self,
    ) -> Callable[
        [secure_source_manager.CreateBranchRuleRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBranchRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_instance(
        self,
    ) -> Callable[
        [secure_source_manager.CreateInstanceRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_repository(
        self,
    ) -> Callable[
        [secure_source_manager.CreateRepositoryRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_branch_rule(
        self,
    ) -> Callable[
        [secure_source_manager.DeleteBranchRuleRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBranchRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_instance(
        self,
    ) -> Callable[
        [secure_source_manager.DeleteInstanceRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_repository(
        self,
    ) -> Callable[
        [secure_source_manager.DeleteRepositoryRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_branch_rule(
        self,
    ) -> Callable[
        [secure_source_manager.GetBranchRuleRequest], secure_source_manager.BranchRule
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBranchRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy_repo(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicyRepo(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_instance(
        self,
    ) -> Callable[
        [secure_source_manager.GetInstanceRequest], secure_source_manager.Instance
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_repository(
        self,
    ) -> Callable[
        [secure_source_manager.GetRepositoryRequest], secure_source_manager.Repository
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRepository(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_branch_rules(
        self,
    ) -> Callable[
        [secure_source_manager.ListBranchRulesRequest],
        secure_source_manager.ListBranchRulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBranchRules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_instances(
        self,
    ) -> Callable[
        [secure_source_manager.ListInstancesRequest],
        secure_source_manager.ListInstancesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_repositories(
        self,
    ) -> Callable[
        [secure_source_manager.ListRepositoriesRequest],
        secure_source_manager.ListRepositoriesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRepositories(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy_repo(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicyRepo(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions_repo(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissionsRepo(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_branch_rule(
        self,
    ) -> Callable[
        [secure_source_manager.UpdateBranchRuleRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBranchRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseSecureSourceManagerRestTransport._BaseGetLocation,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.GetLocation")

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
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._GetLocation._get_response(
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
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseSecureSourceManagerRestTransport._BaseListLocations,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.ListLocations")

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
                _BaseSecureSourceManagerRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._ListLocations._get_response(
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
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(
        _BaseSecureSourceManagerRestTransport._BaseGetIamPolicy,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseGetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(
        _BaseSecureSourceManagerRestTransport._BaseSetIamPolicy,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.SetIamPolicy")

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
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecureSourceManagerRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseSetIamPolicy._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._SetIamPolicy._get_response(
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

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(
        _BaseSecureSourceManagerRestTransport._BaseTestIamPermissions,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.TestIamPermissions")

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
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options = (
                _BaseSecureSourceManagerRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecureSourceManagerRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                SecureSourceManagerRestTransport._TestIamPermissions._get_response(
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

            content = response.content.decode("utf-8")
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseSecureSourceManagerRestTransport._BaseCancelOperation,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.CancelOperation")

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
                _BaseSecureSourceManagerRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseSecureSourceManagerRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._CancelOperation._get_response(
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
        _BaseSecureSourceManagerRestTransport._BaseDeleteOperation,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.DeleteOperation")

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
                _BaseSecureSourceManagerRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._DeleteOperation._get_response(
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
        _BaseSecureSourceManagerRestTransport._BaseGetOperation,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.GetOperation")

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
                _BaseSecureSourceManagerRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._GetOperation._get_response(
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
        _BaseSecureSourceManagerRestTransport._BaseListOperations,
        SecureSourceManagerRestStub,
    ):
        def __hash__(self):
            return hash("SecureSourceManagerRestTransport.ListOperations")

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
                _BaseSecureSourceManagerRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseSecureSourceManagerRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseSecureSourceManagerRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = SecureSourceManagerRestTransport._ListOperations._get_response(
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


__all__ = ("SecureSourceManagerRestTransport",)
