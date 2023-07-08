# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.workstations_v1beta.types import workstations

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import WorkstationsTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class WorkstationsRestInterceptor:
    """Interceptor for Workstations.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the WorkstationsRestTransport.

    .. code-block:: python
        class MyCustomWorkstationsInterceptor(WorkstationsRestInterceptor):
            def pre_create_workstation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_workstation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_workstation_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_workstation_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_workstation_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_workstation_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_workstation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_workstation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_workstation_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_workstation_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_workstation_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_workstation_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_access_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_access_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workstation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workstation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workstation_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workstation_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_workstation_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_workstation_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_usable_workstation_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_usable_workstation_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_usable_workstations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_usable_workstations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workstation_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workstation_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workstation_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workstation_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workstations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workstations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_workstation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_workstation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_workstation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_workstation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_workstation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_workstation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_workstation_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_workstation_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_workstation_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_workstation_config(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = WorkstationsRestTransport(interceptor=MyCustomWorkstationsInterceptor())
        client = WorkstationsClient(transport=transport)


    """

    def pre_create_workstation(
        self,
        request: workstations.CreateWorkstationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.CreateWorkstationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_workstation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_create_workstation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_workstation

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_create_workstation_cluster(
        self,
        request: workstations.CreateWorkstationClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.CreateWorkstationClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_workstation_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_create_workstation_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_workstation_cluster

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_create_workstation_config(
        self,
        request: workstations.CreateWorkstationConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.CreateWorkstationConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_workstation_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_create_workstation_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_workstation_config

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_delete_workstation(
        self,
        request: workstations.DeleteWorkstationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.DeleteWorkstationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_workstation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_delete_workstation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_workstation

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_delete_workstation_cluster(
        self,
        request: workstations.DeleteWorkstationClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.DeleteWorkstationClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_workstation_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_delete_workstation_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_workstation_cluster

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_delete_workstation_config(
        self,
        request: workstations.DeleteWorkstationConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.DeleteWorkstationConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_workstation_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_delete_workstation_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_workstation_config

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_generate_access_token(
        self,
        request: workstations.GenerateAccessTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.GenerateAccessTokenRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for generate_access_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_generate_access_token(
        self, response: workstations.GenerateAccessTokenResponse
    ) -> workstations.GenerateAccessTokenResponse:
        """Post-rpc interceptor for generate_access_token

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_get_workstation(
        self,
        request: workstations.GetWorkstationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.GetWorkstationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_workstation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_get_workstation(
        self, response: workstations.Workstation
    ) -> workstations.Workstation:
        """Post-rpc interceptor for get_workstation

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_get_workstation_cluster(
        self,
        request: workstations.GetWorkstationClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.GetWorkstationClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_workstation_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_get_workstation_cluster(
        self, response: workstations.WorkstationCluster
    ) -> workstations.WorkstationCluster:
        """Post-rpc interceptor for get_workstation_cluster

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_get_workstation_config(
        self,
        request: workstations.GetWorkstationConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.GetWorkstationConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_workstation_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_get_workstation_config(
        self, response: workstations.WorkstationConfig
    ) -> workstations.WorkstationConfig:
        """Post-rpc interceptor for get_workstation_config

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_list_usable_workstation_configs(
        self,
        request: workstations.ListUsableWorkstationConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        workstations.ListUsableWorkstationConfigsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_usable_workstation_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_list_usable_workstation_configs(
        self, response: workstations.ListUsableWorkstationConfigsResponse
    ) -> workstations.ListUsableWorkstationConfigsResponse:
        """Post-rpc interceptor for list_usable_workstation_configs

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_list_usable_workstations(
        self,
        request: workstations.ListUsableWorkstationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.ListUsableWorkstationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_usable_workstations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_list_usable_workstations(
        self, response: workstations.ListUsableWorkstationsResponse
    ) -> workstations.ListUsableWorkstationsResponse:
        """Post-rpc interceptor for list_usable_workstations

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_list_workstation_clusters(
        self,
        request: workstations.ListWorkstationClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.ListWorkstationClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_workstation_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_list_workstation_clusters(
        self, response: workstations.ListWorkstationClustersResponse
    ) -> workstations.ListWorkstationClustersResponse:
        """Post-rpc interceptor for list_workstation_clusters

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_list_workstation_configs(
        self,
        request: workstations.ListWorkstationConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.ListWorkstationConfigsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_workstation_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_list_workstation_configs(
        self, response: workstations.ListWorkstationConfigsResponse
    ) -> workstations.ListWorkstationConfigsResponse:
        """Post-rpc interceptor for list_workstation_configs

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_list_workstations(
        self,
        request: workstations.ListWorkstationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.ListWorkstationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_workstations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_list_workstations(
        self, response: workstations.ListWorkstationsResponse
    ) -> workstations.ListWorkstationsResponse:
        """Post-rpc interceptor for list_workstations

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_start_workstation(
        self,
        request: workstations.StartWorkstationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.StartWorkstationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for start_workstation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_start_workstation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for start_workstation

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_stop_workstation(
        self,
        request: workstations.StopWorkstationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.StopWorkstationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for stop_workstation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_stop_workstation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for stop_workstation

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_update_workstation(
        self,
        request: workstations.UpdateWorkstationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.UpdateWorkstationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_workstation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_update_workstation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_workstation

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_update_workstation_cluster(
        self,
        request: workstations.UpdateWorkstationClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.UpdateWorkstationClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_workstation_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_update_workstation_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_workstation_cluster

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response

    def pre_update_workstation_config(
        self,
        request: workstations.UpdateWorkstationConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[workstations.UpdateWorkstationConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_workstation_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_update_workstation_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_workstation_config

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
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
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
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
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
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
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
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
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
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
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
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
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
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
        before they are sent to the Workstations server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Workstations server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class WorkstationsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: WorkstationsRestInterceptor


class WorkstationsRestTransport(WorkstationsTransport):
    """REST backend transport for Workstations.

    Service for interacting with Cloud Workstations.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "workstations.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[WorkstationsRestInterceptor] = None,
        api_audience: Optional[str] = None,
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
        self._interceptor = interceptor or WorkstationsRestInterceptor()
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
                        "uri": "/v1beta/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1beta/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1beta/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1beta",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateWorkstation(WorkstationsRestStub):
        def __hash__(self):
            return hash("CreateWorkstation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "workstationId": "",
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
            request: workstations.CreateWorkstationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create workstation method over HTTP.

            Args:
                request (~.workstations.CreateWorkstationRequest):
                    The request object. Message for creating a
                CreateWorkstation.
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
                    "uri": "/v1beta/{parent=projects/*/locations/*/workstationClusters/*/workstationConfigs/*}/workstations",
                    "body": "workstation",
                },
            ]
            request, metadata = self._interceptor.pre_create_workstation(
                request, metadata
            )
            pb_request = workstations.CreateWorkstationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_create_workstation(resp)
            return resp

    class _CreateWorkstationCluster(WorkstationsRestStub):
        def __hash__(self):
            return hash("CreateWorkstationCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "workstationClusterId": "",
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
            request: workstations.CreateWorkstationClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create workstation
            cluster method over HTTP.

                Args:
                    request (~.workstations.CreateWorkstationClusterRequest):
                        The request object. Message for creating a
                    CreateWorkstationCluster.
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
                    "uri": "/v1beta/{parent=projects/*/locations/*}/workstationClusters",
                    "body": "workstation_cluster",
                },
            ]
            request, metadata = self._interceptor.pre_create_workstation_cluster(
                request, metadata
            )
            pb_request = workstations.CreateWorkstationClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_create_workstation_cluster(resp)
            return resp

    class _CreateWorkstationConfig(WorkstationsRestStub):
        def __hash__(self):
            return hash("CreateWorkstationConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "workstationConfigId": "",
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
            request: workstations.CreateWorkstationConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create workstation config method over HTTP.

            Args:
                request (~.workstations.CreateWorkstationConfigRequest):
                    The request object. Message for creating a
                CreateWorkstationConfig.
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
                    "uri": "/v1beta/{parent=projects/*/locations/*/workstationClusters/*}/workstationConfigs",
                    "body": "workstation_config",
                },
            ]
            request, metadata = self._interceptor.pre_create_workstation_config(
                request, metadata
            )
            pb_request = workstations.CreateWorkstationConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_create_workstation_config(resp)
            return resp

    class _DeleteWorkstation(WorkstationsRestStub):
        def __hash__(self):
            return hash("DeleteWorkstation")

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
            request: workstations.DeleteWorkstationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete workstation method over HTTP.

            Args:
                request (~.workstations.DeleteWorkstationRequest):
                    The request object. Request message for
                DeleteWorkstation.
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
                    "uri": "/v1beta/{name=projects/*/locations/*/workstationClusters/*/workstationConfigs/*/workstations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_workstation(
                request, metadata
            )
            pb_request = workstations.DeleteWorkstationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_delete_workstation(resp)
            return resp

    class _DeleteWorkstationCluster(WorkstationsRestStub):
        def __hash__(self):
            return hash("DeleteWorkstationCluster")

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
            request: workstations.DeleteWorkstationClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete workstation
            cluster method over HTTP.

                Args:
                    request (~.workstations.DeleteWorkstationClusterRequest):
                        The request object. Message for deleting a workstation
                    cluster.
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
                    "uri": "/v1beta/{name=projects/*/locations/*/workstationClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_workstation_cluster(
                request, metadata
            )
            pb_request = workstations.DeleteWorkstationClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_delete_workstation_cluster(resp)
            return resp

    class _DeleteWorkstationConfig(WorkstationsRestStub):
        def __hash__(self):
            return hash("DeleteWorkstationConfig")

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
            request: workstations.DeleteWorkstationConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete workstation config method over HTTP.

            Args:
                request (~.workstations.DeleteWorkstationConfigRequest):
                    The request object. Message for deleting a workstation
                configuration.
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
                    "uri": "/v1beta/{name=projects/*/locations/*/workstationClusters/*/workstationConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_workstation_config(
                request, metadata
            )
            pb_request = workstations.DeleteWorkstationConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_delete_workstation_config(resp)
            return resp

    class _GenerateAccessToken(WorkstationsRestStub):
        def __hash__(self):
            return hash("GenerateAccessToken")

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
            request: workstations.GenerateAccessTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workstations.GenerateAccessTokenResponse:
            r"""Call the generate access token method over HTTP.

            Args:
                request (~.workstations.GenerateAccessTokenRequest):
                    The request object. Request message for
                GenerateAccessToken.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workstations.GenerateAccessTokenResponse:
                    Response message for
                GenerateAccessToken.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{workstation=projects/*/locations/*/workstationClusters/*/workstationConfigs/*/workstations/*}:generateAccessToken",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_generate_access_token(
                request, metadata
            )
            pb_request = workstations.GenerateAccessTokenRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = workstations.GenerateAccessTokenResponse()
            pb_resp = workstations.GenerateAccessTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_access_token(resp)
            return resp

    class _GetWorkstation(WorkstationsRestStub):
        def __hash__(self):
            return hash("GetWorkstation")

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
            request: workstations.GetWorkstationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workstations.Workstation:
            r"""Call the get workstation method over HTTP.

            Args:
                request (~.workstations.GetWorkstationRequest):
                    The request object. Request message for GetWorkstation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workstations.Workstation:
                    A single instance of a developer
                workstation with its own persistent
                storage.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/workstationClusters/*/workstationConfigs/*/workstations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_workstation(request, metadata)
            pb_request = workstations.GetWorkstationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = workstations.Workstation()
            pb_resp = workstations.Workstation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_workstation(resp)
            return resp

    class _GetWorkstationCluster(WorkstationsRestStub):
        def __hash__(self):
            return hash("GetWorkstationCluster")

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
            request: workstations.GetWorkstationClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workstations.WorkstationCluster:
            r"""Call the get workstation cluster method over HTTP.

            Args:
                request (~.workstations.GetWorkstationClusterRequest):
                    The request object. Request message for
                GetWorkstationCluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workstations.WorkstationCluster:
                    A grouping of workstation
                configurations and the associated
                workstations  in that region.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/workstationClusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_workstation_cluster(
                request, metadata
            )
            pb_request = workstations.GetWorkstationClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = workstations.WorkstationCluster()
            pb_resp = workstations.WorkstationCluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_workstation_cluster(resp)
            return resp

    class _GetWorkstationConfig(WorkstationsRestStub):
        def __hash__(self):
            return hash("GetWorkstationConfig")

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
            request: workstations.GetWorkstationConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workstations.WorkstationConfig:
            r"""Call the get workstation config method over HTTP.

            Args:
                request (~.workstations.GetWorkstationConfigRequest):
                    The request object. Request message for
                GetWorkstationConfig.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workstations.WorkstationConfig:
                    A set of configuration options
                describing how a workstation will be
                run. Workstation configurations are
                intended to be shared across multiple
                workstations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=projects/*/locations/*/workstationClusters/*/workstationConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_workstation_config(
                request, metadata
            )
            pb_request = workstations.GetWorkstationConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = workstations.WorkstationConfig()
            pb_resp = workstations.WorkstationConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_workstation_config(resp)
            return resp

    class _ListUsableWorkstationConfigs(WorkstationsRestStub):
        def __hash__(self):
            return hash("ListUsableWorkstationConfigs")

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
            request: workstations.ListUsableWorkstationConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workstations.ListUsableWorkstationConfigsResponse:
            r"""Call the list usable workstation
            configs method over HTTP.

                Args:
                    request (~.workstations.ListUsableWorkstationConfigsRequest):
                        The request object. Request message for
                    ListUsableWorkstationConfigs.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.workstations.ListUsableWorkstationConfigsResponse:
                        Response message for
                    ListUsableWorkstationConfigs.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=projects/*/locations/*/workstationClusters/*}/workstationConfigs:listUsable",
                },
            ]
            request, metadata = self._interceptor.pre_list_usable_workstation_configs(
                request, metadata
            )
            pb_request = workstations.ListUsableWorkstationConfigsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = workstations.ListUsableWorkstationConfigsResponse()
            pb_resp = workstations.ListUsableWorkstationConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_usable_workstation_configs(resp)
            return resp

    class _ListUsableWorkstations(WorkstationsRestStub):
        def __hash__(self):
            return hash("ListUsableWorkstations")

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
            request: workstations.ListUsableWorkstationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workstations.ListUsableWorkstationsResponse:
            r"""Call the list usable workstations method over HTTP.

            Args:
                request (~.workstations.ListUsableWorkstationsRequest):
                    The request object. Request message for
                ListUsableWorkstations.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workstations.ListUsableWorkstationsResponse:
                    Response message for
                ListUsableWorkstations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=projects/*/locations/*/workstationClusters/*/workstationConfigs/*}/workstations:listUsable",
                },
            ]
            request, metadata = self._interceptor.pre_list_usable_workstations(
                request, metadata
            )
            pb_request = workstations.ListUsableWorkstationsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = workstations.ListUsableWorkstationsResponse()
            pb_resp = workstations.ListUsableWorkstationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_usable_workstations(resp)
            return resp

    class _ListWorkstationClusters(WorkstationsRestStub):
        def __hash__(self):
            return hash("ListWorkstationClusters")

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
            request: workstations.ListWorkstationClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workstations.ListWorkstationClustersResponse:
            r"""Call the list workstation clusters method over HTTP.

            Args:
                request (~.workstations.ListWorkstationClustersRequest):
                    The request object. Request message for
                ListWorkstationClusters.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workstations.ListWorkstationClustersResponse:
                    Response message for
                ListWorkstationClusters.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=projects/*/locations/*}/workstationClusters",
                },
            ]
            request, metadata = self._interceptor.pre_list_workstation_clusters(
                request, metadata
            )
            pb_request = workstations.ListWorkstationClustersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = workstations.ListWorkstationClustersResponse()
            pb_resp = workstations.ListWorkstationClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_workstation_clusters(resp)
            return resp

    class _ListWorkstationConfigs(WorkstationsRestStub):
        def __hash__(self):
            return hash("ListWorkstationConfigs")

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
            request: workstations.ListWorkstationConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workstations.ListWorkstationConfigsResponse:
            r"""Call the list workstation configs method over HTTP.

            Args:
                request (~.workstations.ListWorkstationConfigsRequest):
                    The request object. Request message for
                ListWorkstationConfigs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workstations.ListWorkstationConfigsResponse:
                    Response message for
                ListWorkstationConfigs.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=projects/*/locations/*/workstationClusters/*}/workstationConfigs",
                },
            ]
            request, metadata = self._interceptor.pre_list_workstation_configs(
                request, metadata
            )
            pb_request = workstations.ListWorkstationConfigsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = workstations.ListWorkstationConfigsResponse()
            pb_resp = workstations.ListWorkstationConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_workstation_configs(resp)
            return resp

    class _ListWorkstations(WorkstationsRestStub):
        def __hash__(self):
            return hash("ListWorkstations")

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
            request: workstations.ListWorkstationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> workstations.ListWorkstationsResponse:
            r"""Call the list workstations method over HTTP.

            Args:
                request (~.workstations.ListWorkstationsRequest):
                    The request object. Request message for ListWorkstations.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.workstations.ListWorkstationsResponse:
                    Response message for
                ListWorkstations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=projects/*/locations/*/workstationClusters/*/workstationConfigs/*}/workstations",
                },
            ]
            request, metadata = self._interceptor.pre_list_workstations(
                request, metadata
            )
            pb_request = workstations.ListWorkstationsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = workstations.ListWorkstationsResponse()
            pb_resp = workstations.ListWorkstationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_workstations(resp)
            return resp

    class _StartWorkstation(WorkstationsRestStub):
        def __hash__(self):
            return hash("StartWorkstation")

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
            request: workstations.StartWorkstationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the start workstation method over HTTP.

            Args:
                request (~.workstations.StartWorkstationRequest):
                    The request object. Request message for StartWorkstation.
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
                    "uri": "/v1beta/{name=projects/*/locations/*/workstationClusters/*/workstationConfigs/*/workstations/*}:start",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_start_workstation(
                request, metadata
            )
            pb_request = workstations.StartWorkstationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_start_workstation(resp)
            return resp

    class _StopWorkstation(WorkstationsRestStub):
        def __hash__(self):
            return hash("StopWorkstation")

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
            request: workstations.StopWorkstationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the stop workstation method over HTTP.

            Args:
                request (~.workstations.StopWorkstationRequest):
                    The request object. Request message for StopWorkstation.
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
                    "uri": "/v1beta/{name=projects/*/locations/*/workstationClusters/*/workstationConfigs/*/workstations/*}:stop",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_stop_workstation(
                request, metadata
            )
            pb_request = workstations.StopWorkstationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_stop_workstation(resp)
            return resp

    class _UpdateWorkstation(WorkstationsRestStub):
        def __hash__(self):
            return hash("UpdateWorkstation")

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
            request: workstations.UpdateWorkstationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update workstation method over HTTP.

            Args:
                request (~.workstations.UpdateWorkstationRequest):
                    The request object. Request message for
                UpdateWorkstation.
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
                    "uri": "/v1beta/{workstation.name=projects/*/locations/*/workstationClusters/*/workstationConfigs/*/workstations/*}",
                    "body": "workstation",
                },
            ]
            request, metadata = self._interceptor.pre_update_workstation(
                request, metadata
            )
            pb_request = workstations.UpdateWorkstationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_update_workstation(resp)
            return resp

    class _UpdateWorkstationCluster(WorkstationsRestStub):
        def __hash__(self):
            return hash("UpdateWorkstationCluster")

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
            request: workstations.UpdateWorkstationClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update workstation
            cluster method over HTTP.

                Args:
                    request (~.workstations.UpdateWorkstationClusterRequest):
                        The request object. Request message for
                    UpdateWorkstationCluster.
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
                    "uri": "/v1beta/{workstation_cluster.name=projects/*/locations/*/workstationClusters/*}",
                    "body": "workstation_cluster",
                },
            ]
            request, metadata = self._interceptor.pre_update_workstation_cluster(
                request, metadata
            )
            pb_request = workstations.UpdateWorkstationClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_update_workstation_cluster(resp)
            return resp

    class _UpdateWorkstationConfig(WorkstationsRestStub):
        def __hash__(self):
            return hash("UpdateWorkstationConfig")

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
            request: workstations.UpdateWorkstationConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update workstation config method over HTTP.

            Args:
                request (~.workstations.UpdateWorkstationConfigRequest):
                    The request object. Request message for
                UpdateWorkstationConfig.
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
                    "uri": "/v1beta/{workstation_config.name=projects/*/locations/*/workstationClusters/*/workstationConfigs/*}",
                    "body": "workstation_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_workstation_config(
                request, metadata
            )
            pb_request = workstations.UpdateWorkstationConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_update_workstation_config(resp)
            return resp

    @property
    def create_workstation(
        self,
    ) -> Callable[[workstations.CreateWorkstationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWorkstation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.CreateWorkstationClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWorkstationCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_workstation_config(
        self,
    ) -> Callable[
        [workstations.CreateWorkstationConfigRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateWorkstationConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_workstation(
        self,
    ) -> Callable[[workstations.DeleteWorkstationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWorkstation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.DeleteWorkstationClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWorkstationCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_workstation_config(
        self,
    ) -> Callable[
        [workstations.DeleteWorkstationConfigRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteWorkstationConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_access_token(
        self,
    ) -> Callable[
        [workstations.GenerateAccessTokenRequest],
        workstations.GenerateAccessTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateAccessToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workstation(
        self,
    ) -> Callable[[workstations.GetWorkstationRequest], workstations.Workstation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkstation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.GetWorkstationClusterRequest], workstations.WorkstationCluster
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkstationCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_workstation_config(
        self,
    ) -> Callable[
        [workstations.GetWorkstationConfigRequest], workstations.WorkstationConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetWorkstationConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_usable_workstation_configs(
        self,
    ) -> Callable[
        [workstations.ListUsableWorkstationConfigsRequest],
        workstations.ListUsableWorkstationConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListUsableWorkstationConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_usable_workstations(
        self,
    ) -> Callable[
        [workstations.ListUsableWorkstationsRequest],
        workstations.ListUsableWorkstationsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListUsableWorkstations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workstation_clusters(
        self,
    ) -> Callable[
        [workstations.ListWorkstationClustersRequest],
        workstations.ListWorkstationClustersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkstationClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workstation_configs(
        self,
    ) -> Callable[
        [workstations.ListWorkstationConfigsRequest],
        workstations.ListWorkstationConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkstationConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workstations(
        self,
    ) -> Callable[
        [workstations.ListWorkstationsRequest], workstations.ListWorkstationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkstations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_workstation(
        self,
    ) -> Callable[[workstations.StartWorkstationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartWorkstation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def stop_workstation(
        self,
    ) -> Callable[[workstations.StopWorkstationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopWorkstation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_workstation(
        self,
    ) -> Callable[[workstations.UpdateWorkstationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateWorkstation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.UpdateWorkstationClusterRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateWorkstationCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_workstation_config(
        self,
    ) -> Callable[
        [workstations.UpdateWorkstationConfigRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateWorkstationConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(WorkstationsRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{resource=projects/*/locations/*/workstationClusters/*/workstationConfigs/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1beta/{resource=projects/*/locations/*/workstationClusters/*/workstationConfigs/*/workstations/*}:getIamPolicy",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(WorkstationsRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{resource=projects/*/locations/*/workstationClusters/*/workstationConfigs/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta/{resource=projects/*/locations/*/workstationClusters/*/workstationConfigs/*/workstations/*}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(WorkstationsRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{resource=projects/*/locations/*/workstationClusters/*/workstationConfigs/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta/{resource=projects/*/locations/*/workstationClusters/*/workstationConfigs/*/workstations/*}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
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

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(WorkstationsRestStub):
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
                    "uri": "/v1beta/{name=projects/*/locations/*/operations/*}:cancel",
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

    class _DeleteOperation(WorkstationsRestStub):
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
                    "uri": "/v1beta/{name=projects/*/locations/*/operations/*}",
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

    class _GetOperation(WorkstationsRestStub):
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
                    "uri": "/v1beta/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(WorkstationsRestStub):
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
                    "uri": "/v1beta/{name=projects/*/locations/*}/operations",
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


__all__ = ("WorkstationsRestTransport",)
