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
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.orchestration.airflow.service_v1.types import environments

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import EnvironmentsTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class EnvironmentsRestInterceptor:
    """Interceptor for Environments.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the EnvironmentsRestTransport.

    .. code-block:: python
        class MyCustomEnvironmentsInterceptor(EnvironmentsRestInterceptor):
            def pre_create_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_user_workloads_config_map(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_user_workloads_config_map(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_user_workloads_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_user_workloads_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_database_failover(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_database_failover(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_user_workloads_config_map(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_user_workloads_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_execute_airflow_command(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_execute_airflow_command(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_database_properties(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_database_properties(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_user_workloads_config_map(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_user_workloads_config_map(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_user_workloads_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_user_workloads_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_environments(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_environments(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_user_workloads_config_maps(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_user_workloads_config_maps(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_user_workloads_secrets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_user_workloads_secrets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_workloads(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_workloads(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_load_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_load_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_poll_airflow_command(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_poll_airflow_command(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_save_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_save_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_airflow_command(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_airflow_command(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_environment(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_environment(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_user_workloads_config_map(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_user_workloads_config_map(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_user_workloads_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_user_workloads_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = EnvironmentsRestTransport(interceptor=MyCustomEnvironmentsInterceptor())
        client = EnvironmentsClient(transport=transport)


    """

    def pre_create_environment(
        self,
        request: environments.CreateEnvironmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.CreateEnvironmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_create_environment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_environment

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_create_user_workloads_config_map(
        self,
        request: environments.CreateUserWorkloadsConfigMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        environments.CreateUserWorkloadsConfigMapRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_user_workloads_config_map

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_create_user_workloads_config_map(
        self, response: environments.UserWorkloadsConfigMap
    ) -> environments.UserWorkloadsConfigMap:
        """Post-rpc interceptor for create_user_workloads_config_map

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_create_user_workloads_secret(
        self,
        request: environments.CreateUserWorkloadsSecretRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        environments.CreateUserWorkloadsSecretRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_user_workloads_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_create_user_workloads_secret(
        self, response: environments.UserWorkloadsSecret
    ) -> environments.UserWorkloadsSecret:
        """Post-rpc interceptor for create_user_workloads_secret

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_database_failover(
        self,
        request: environments.DatabaseFailoverRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.DatabaseFailoverRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for database_failover

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_database_failover(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for database_failover

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_delete_environment(
        self,
        request: environments.DeleteEnvironmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.DeleteEnvironmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_delete_environment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_environment

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_delete_user_workloads_config_map(
        self,
        request: environments.DeleteUserWorkloadsConfigMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        environments.DeleteUserWorkloadsConfigMapRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_user_workloads_config_map

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def pre_delete_user_workloads_secret(
        self,
        request: environments.DeleteUserWorkloadsSecretRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        environments.DeleteUserWorkloadsSecretRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_user_workloads_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def pre_execute_airflow_command(
        self,
        request: environments.ExecuteAirflowCommandRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.ExecuteAirflowCommandRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for execute_airflow_command

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_execute_airflow_command(
        self, response: environments.ExecuteAirflowCommandResponse
    ) -> environments.ExecuteAirflowCommandResponse:
        """Post-rpc interceptor for execute_airflow_command

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_database_properties(
        self,
        request: environments.FetchDatabasePropertiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.FetchDatabasePropertiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_database_properties

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_fetch_database_properties(
        self, response: environments.FetchDatabasePropertiesResponse
    ) -> environments.FetchDatabasePropertiesResponse:
        """Post-rpc interceptor for fetch_database_properties

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_get_environment(
        self,
        request: environments.GetEnvironmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.GetEnvironmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_get_environment(
        self, response: environments.Environment
    ) -> environments.Environment:
        """Post-rpc interceptor for get_environment

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_get_user_workloads_config_map(
        self,
        request: environments.GetUserWorkloadsConfigMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        environments.GetUserWorkloadsConfigMapRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_user_workloads_config_map

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_get_user_workloads_config_map(
        self, response: environments.UserWorkloadsConfigMap
    ) -> environments.UserWorkloadsConfigMap:
        """Post-rpc interceptor for get_user_workloads_config_map

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_get_user_workloads_secret(
        self,
        request: environments.GetUserWorkloadsSecretRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.GetUserWorkloadsSecretRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_user_workloads_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_get_user_workloads_secret(
        self, response: environments.UserWorkloadsSecret
    ) -> environments.UserWorkloadsSecret:
        """Post-rpc interceptor for get_user_workloads_secret

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_list_environments(
        self,
        request: environments.ListEnvironmentsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.ListEnvironmentsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_environments

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_list_environments(
        self, response: environments.ListEnvironmentsResponse
    ) -> environments.ListEnvironmentsResponse:
        """Post-rpc interceptor for list_environments

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_list_user_workloads_config_maps(
        self,
        request: environments.ListUserWorkloadsConfigMapsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        environments.ListUserWorkloadsConfigMapsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_user_workloads_config_maps

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_list_user_workloads_config_maps(
        self, response: environments.ListUserWorkloadsConfigMapsResponse
    ) -> environments.ListUserWorkloadsConfigMapsResponse:
        """Post-rpc interceptor for list_user_workloads_config_maps

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_list_user_workloads_secrets(
        self,
        request: environments.ListUserWorkloadsSecretsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.ListUserWorkloadsSecretsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_user_workloads_secrets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_list_user_workloads_secrets(
        self, response: environments.ListUserWorkloadsSecretsResponse
    ) -> environments.ListUserWorkloadsSecretsResponse:
        """Post-rpc interceptor for list_user_workloads_secrets

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_list_workloads(
        self,
        request: environments.ListWorkloadsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.ListWorkloadsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_workloads

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_list_workloads(
        self, response: environments.ListWorkloadsResponse
    ) -> environments.ListWorkloadsResponse:
        """Post-rpc interceptor for list_workloads

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_load_snapshot(
        self,
        request: environments.LoadSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.LoadSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for load_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_load_snapshot(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for load_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_poll_airflow_command(
        self,
        request: environments.PollAirflowCommandRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.PollAirflowCommandRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for poll_airflow_command

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_poll_airflow_command(
        self, response: environments.PollAirflowCommandResponse
    ) -> environments.PollAirflowCommandResponse:
        """Post-rpc interceptor for poll_airflow_command

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_save_snapshot(
        self,
        request: environments.SaveSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.SaveSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for save_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_save_snapshot(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for save_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_stop_airflow_command(
        self,
        request: environments.StopAirflowCommandRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.StopAirflowCommandRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for stop_airflow_command

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_stop_airflow_command(
        self, response: environments.StopAirflowCommandResponse
    ) -> environments.StopAirflowCommandResponse:
        """Post-rpc interceptor for stop_airflow_command

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_update_environment(
        self,
        request: environments.UpdateEnvironmentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[environments.UpdateEnvironmentRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_environment

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_update_environment(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_environment

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_update_user_workloads_config_map(
        self,
        request: environments.UpdateUserWorkloadsConfigMapRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        environments.UpdateUserWorkloadsConfigMapRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_user_workloads_config_map

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_update_user_workloads_config_map(
        self, response: environments.UserWorkloadsConfigMap
    ) -> environments.UserWorkloadsConfigMap:
        """Post-rpc interceptor for update_user_workloads_config_map

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response

    def pre_update_user_workloads_secret(
        self,
        request: environments.UpdateUserWorkloadsSecretRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        environments.UpdateUserWorkloadsSecretRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_user_workloads_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_update_user_workloads_secret(
        self, response: environments.UserWorkloadsSecret
    ) -> environments.UserWorkloadsSecret:
        """Post-rpc interceptor for update_user_workloads_secret

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
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
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
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
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
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
        before they are sent to the Environments server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Environments server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class EnvironmentsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: EnvironmentsRestInterceptor


class EnvironmentsRestTransport(EnvironmentsTransport):
    """REST backend transport for Environments.

    Managed Apache Airflow Environments.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "composer.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[EnvironmentsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'composer.googleapis.com').
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
        self._interceptor = interceptor or EnvironmentsRestInterceptor()
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

    class _CreateEnvironment(EnvironmentsRestStub):
        def __hash__(self):
            return hash("CreateEnvironment")

        def __call__(
            self,
            request: environments.CreateEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create environment method over HTTP.

            Args:
                request (~.environments.CreateEnvironmentRequest):
                    The request object. Create a new environment.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/environments",
                    "body": "environment",
                },
            ]
            request, metadata = self._interceptor.pre_create_environment(
                request, metadata
            )
            pb_request = environments.CreateEnvironmentRequest.pb(request)
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
            resp = self._interceptor.post_create_environment(resp)
            return resp

    class _CreateUserWorkloadsConfigMap(EnvironmentsRestStub):
        def __hash__(self):
            return hash("CreateUserWorkloadsConfigMap")

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
            request: environments.CreateUserWorkloadsConfigMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.UserWorkloadsConfigMap:
            r"""Call the create user workloads
            config map method over HTTP.

                Args:
                    request (~.environments.CreateUserWorkloadsConfigMapRequest):
                        The request object. Create user workloads ConfigMap
                    request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.environments.UserWorkloadsConfigMap:
                        User workloads ConfigMap used by
                    Airflow tasks that run with Kubernetes
                    executor or KubernetesPodOperator.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/environments/*}/userWorkloadsConfigMaps",
                    "body": "user_workloads_config_map",
                },
            ]
            request, metadata = self._interceptor.pre_create_user_workloads_config_map(
                request, metadata
            )
            pb_request = environments.CreateUserWorkloadsConfigMapRequest.pb(request)
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
            resp = environments.UserWorkloadsConfigMap()
            pb_resp = environments.UserWorkloadsConfigMap.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_user_workloads_config_map(resp)
            return resp

    class _CreateUserWorkloadsSecret(EnvironmentsRestStub):
        def __hash__(self):
            return hash("CreateUserWorkloadsSecret")

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
            request: environments.CreateUserWorkloadsSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.UserWorkloadsSecret:
            r"""Call the create user workloads
            secret method over HTTP.

                Args:
                    request (~.environments.CreateUserWorkloadsSecretRequest):
                        The request object. Create user workloads Secret request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.environments.UserWorkloadsSecret:
                        User workloads Secret used by Airflow
                    tasks that run with Kubernetes executor
                    or KubernetesPodOperator.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/environments/*}/userWorkloadsSecrets",
                    "body": "user_workloads_secret",
                },
            ]
            request, metadata = self._interceptor.pre_create_user_workloads_secret(
                request, metadata
            )
            pb_request = environments.CreateUserWorkloadsSecretRequest.pb(request)
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
            resp = environments.UserWorkloadsSecret()
            pb_resp = environments.UserWorkloadsSecret.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_user_workloads_secret(resp)
            return resp

    class _DatabaseFailover(EnvironmentsRestStub):
        def __hash__(self):
            return hash("DatabaseFailover")

        def __call__(
            self,
            request: environments.DatabaseFailoverRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the database failover method over HTTP.

            Args:
                request (~.environments.DatabaseFailoverRequest):
                    The request object. Request to trigger database failover
                (only for highly resilient
                environments).
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
                    "uri": "/v1/{environment=projects/*/locations/*/environments/*}:databaseFailover",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_database_failover(
                request, metadata
            )
            pb_request = environments.DatabaseFailoverRequest.pb(request)
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
            resp = self._interceptor.post_database_failover(resp)
            return resp

    class _DeleteEnvironment(EnvironmentsRestStub):
        def __hash__(self):
            return hash("DeleteEnvironment")

        def __call__(
            self,
            request: environments.DeleteEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete environment method over HTTP.

            Args:
                request (~.environments.DeleteEnvironmentRequest):
                    The request object. Delete an environment.
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
                    "uri": "/v1/{name=projects/*/locations/*/environments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_environment(
                request, metadata
            )
            pb_request = environments.DeleteEnvironmentRequest.pb(request)
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
            resp = self._interceptor.post_delete_environment(resp)
            return resp

    class _DeleteUserWorkloadsConfigMap(EnvironmentsRestStub):
        def __hash__(self):
            return hash("DeleteUserWorkloadsConfigMap")

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
            request: environments.DeleteUserWorkloadsConfigMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete user workloads
            config map method over HTTP.

                Args:
                    request (~.environments.DeleteUserWorkloadsConfigMapRequest):
                        The request object. Delete user workloads ConfigMap
                    request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/environments/*/userWorkloadsConfigMaps/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_user_workloads_config_map(
                request, metadata
            )
            pb_request = environments.DeleteUserWorkloadsConfigMapRequest.pb(request)
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

    class _DeleteUserWorkloadsSecret(EnvironmentsRestStub):
        def __hash__(self):
            return hash("DeleteUserWorkloadsSecret")

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
            request: environments.DeleteUserWorkloadsSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete user workloads
            secret method over HTTP.

                Args:
                    request (~.environments.DeleteUserWorkloadsSecretRequest):
                        The request object. Delete user workloads Secret request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/environments/*/userWorkloadsSecrets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_user_workloads_secret(
                request, metadata
            )
            pb_request = environments.DeleteUserWorkloadsSecretRequest.pb(request)
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

    class _ExecuteAirflowCommand(EnvironmentsRestStub):
        def __hash__(self):
            return hash("ExecuteAirflowCommand")

        def __call__(
            self,
            request: environments.ExecuteAirflowCommandRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.ExecuteAirflowCommandResponse:
            r"""Call the execute airflow command method over HTTP.

            Args:
                request (~.environments.ExecuteAirflowCommandRequest):
                    The request object. Execute Airflow Command request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environments.ExecuteAirflowCommandResponse:
                    Response to
                ExecuteAirflowCommandRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{environment=projects/*/locations/*/environments/*}:executeAirflowCommand",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_execute_airflow_command(
                request, metadata
            )
            pb_request = environments.ExecuteAirflowCommandRequest.pb(request)
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
            resp = environments.ExecuteAirflowCommandResponse()
            pb_resp = environments.ExecuteAirflowCommandResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_execute_airflow_command(resp)
            return resp

    class _FetchDatabaseProperties(EnvironmentsRestStub):
        def __hash__(self):
            return hash("FetchDatabaseProperties")

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
            request: environments.FetchDatabasePropertiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.FetchDatabasePropertiesResponse:
            r"""Call the fetch database properties method over HTTP.

            Args:
                request (~.environments.FetchDatabasePropertiesRequest):
                    The request object. Request to fetch properties of
                environment's database.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environments.FetchDatabasePropertiesResponse:
                    Response for
                FetchDatabasePropertiesRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{environment=projects/*/locations/*/environments/*}:fetchDatabaseProperties",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_database_properties(
                request, metadata
            )
            pb_request = environments.FetchDatabasePropertiesRequest.pb(request)
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
            resp = environments.FetchDatabasePropertiesResponse()
            pb_resp = environments.FetchDatabasePropertiesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_database_properties(resp)
            return resp

    class _GetEnvironment(EnvironmentsRestStub):
        def __hash__(self):
            return hash("GetEnvironment")

        def __call__(
            self,
            request: environments.GetEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.Environment:
            r"""Call the get environment method over HTTP.

            Args:
                request (~.environments.GetEnvironmentRequest):
                    The request object. Get an environment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environments.Environment:
                    An environment for running
                orchestration tasks.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/environments/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_environment(request, metadata)
            pb_request = environments.GetEnvironmentRequest.pb(request)
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
            resp = environments.Environment()
            pb_resp = environments.Environment.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_environment(resp)
            return resp

    class _GetUserWorkloadsConfigMap(EnvironmentsRestStub):
        def __hash__(self):
            return hash("GetUserWorkloadsConfigMap")

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
            request: environments.GetUserWorkloadsConfigMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.UserWorkloadsConfigMap:
            r"""Call the get user workloads config
            map method over HTTP.

                Args:
                    request (~.environments.GetUserWorkloadsConfigMapRequest):
                        The request object. Get user workloads ConfigMap request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.environments.UserWorkloadsConfigMap:
                        User workloads ConfigMap used by
                    Airflow tasks that run with Kubernetes
                    executor or KubernetesPodOperator.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/environments/*/userWorkloadsConfigMaps/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_user_workloads_config_map(
                request, metadata
            )
            pb_request = environments.GetUserWorkloadsConfigMapRequest.pb(request)
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
            resp = environments.UserWorkloadsConfigMap()
            pb_resp = environments.UserWorkloadsConfigMap.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_user_workloads_config_map(resp)
            return resp

    class _GetUserWorkloadsSecret(EnvironmentsRestStub):
        def __hash__(self):
            return hash("GetUserWorkloadsSecret")

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
            request: environments.GetUserWorkloadsSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.UserWorkloadsSecret:
            r"""Call the get user workloads secret method over HTTP.

            Args:
                request (~.environments.GetUserWorkloadsSecretRequest):
                    The request object. Get user workloads Secret request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environments.UserWorkloadsSecret:
                    User workloads Secret used by Airflow
                tasks that run with Kubernetes executor
                or KubernetesPodOperator.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/environments/*/userWorkloadsSecrets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_user_workloads_secret(
                request, metadata
            )
            pb_request = environments.GetUserWorkloadsSecretRequest.pb(request)
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
            resp = environments.UserWorkloadsSecret()
            pb_resp = environments.UserWorkloadsSecret.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_user_workloads_secret(resp)
            return resp

    class _ListEnvironments(EnvironmentsRestStub):
        def __hash__(self):
            return hash("ListEnvironments")

        def __call__(
            self,
            request: environments.ListEnvironmentsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.ListEnvironmentsResponse:
            r"""Call the list environments method over HTTP.

            Args:
                request (~.environments.ListEnvironmentsRequest):
                    The request object. List environments in a project and
                location.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environments.ListEnvironmentsResponse:
                    The environments in a project and
                location.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/environments",
                },
            ]
            request, metadata = self._interceptor.pre_list_environments(
                request, metadata
            )
            pb_request = environments.ListEnvironmentsRequest.pb(request)
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
            resp = environments.ListEnvironmentsResponse()
            pb_resp = environments.ListEnvironmentsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_environments(resp)
            return resp

    class _ListUserWorkloadsConfigMaps(EnvironmentsRestStub):
        def __hash__(self):
            return hash("ListUserWorkloadsConfigMaps")

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
            request: environments.ListUserWorkloadsConfigMapsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.ListUserWorkloadsConfigMapsResponse:
            r"""Call the list user workloads
            config maps method over HTTP.

                Args:
                    request (~.environments.ListUserWorkloadsConfigMapsRequest):
                        The request object. List user workloads ConfigMaps
                    request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.environments.ListUserWorkloadsConfigMapsResponse:
                        The user workloads ConfigMaps for a
                    given environment.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/environments/*}/userWorkloadsConfigMaps",
                },
            ]
            request, metadata = self._interceptor.pre_list_user_workloads_config_maps(
                request, metadata
            )
            pb_request = environments.ListUserWorkloadsConfigMapsRequest.pb(request)
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
            resp = environments.ListUserWorkloadsConfigMapsResponse()
            pb_resp = environments.ListUserWorkloadsConfigMapsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_user_workloads_config_maps(resp)
            return resp

    class _ListUserWorkloadsSecrets(EnvironmentsRestStub):
        def __hash__(self):
            return hash("ListUserWorkloadsSecrets")

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
            request: environments.ListUserWorkloadsSecretsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.ListUserWorkloadsSecretsResponse:
            r"""Call the list user workloads
            secrets method over HTTP.

                Args:
                    request (~.environments.ListUserWorkloadsSecretsRequest):
                        The request object. List user workloads Secrets request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.environments.ListUserWorkloadsSecretsResponse:
                        The user workloads Secrets for a
                    given environment.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/environments/*}/userWorkloadsSecrets",
                },
            ]
            request, metadata = self._interceptor.pre_list_user_workloads_secrets(
                request, metadata
            )
            pb_request = environments.ListUserWorkloadsSecretsRequest.pb(request)
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
            resp = environments.ListUserWorkloadsSecretsResponse()
            pb_resp = environments.ListUserWorkloadsSecretsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_user_workloads_secrets(resp)
            return resp

    class _ListWorkloads(EnvironmentsRestStub):
        def __hash__(self):
            return hash("ListWorkloads")

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
            request: environments.ListWorkloadsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.ListWorkloadsResponse:
            r"""Call the list workloads method over HTTP.

            Args:
                request (~.environments.ListWorkloadsRequest):
                    The request object. Request for listing workloads in a
                Cloud Composer environment.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environments.ListWorkloadsResponse:
                    Response to ListWorkloadsRequest.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/environments/*}/workloads",
                },
            ]
            request, metadata = self._interceptor.pre_list_workloads(request, metadata)
            pb_request = environments.ListWorkloadsRequest.pb(request)
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
            resp = environments.ListWorkloadsResponse()
            pb_resp = environments.ListWorkloadsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_workloads(resp)
            return resp

    class _LoadSnapshot(EnvironmentsRestStub):
        def __hash__(self):
            return hash("LoadSnapshot")

        def __call__(
            self,
            request: environments.LoadSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the load snapshot method over HTTP.

            Args:
                request (~.environments.LoadSnapshotRequest):
                    The request object. Request to load a snapshot into a
                Cloud Composer environment.
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
                    "uri": "/v1/{environment=projects/*/locations/*/environments/*}:loadSnapshot",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_load_snapshot(request, metadata)
            pb_request = environments.LoadSnapshotRequest.pb(request)
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
            resp = self._interceptor.post_load_snapshot(resp)
            return resp

    class _PollAirflowCommand(EnvironmentsRestStub):
        def __hash__(self):
            return hash("PollAirflowCommand")

        def __call__(
            self,
            request: environments.PollAirflowCommandRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.PollAirflowCommandResponse:
            r"""Call the poll airflow command method over HTTP.

            Args:
                request (~.environments.PollAirflowCommandRequest):
                    The request object. Poll Airflow Command request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environments.PollAirflowCommandResponse:
                    Response to
                PollAirflowCommandRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{environment=projects/*/locations/*/environments/*}:pollAirflowCommand",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_poll_airflow_command(
                request, metadata
            )
            pb_request = environments.PollAirflowCommandRequest.pb(request)
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
            resp = environments.PollAirflowCommandResponse()
            pb_resp = environments.PollAirflowCommandResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_poll_airflow_command(resp)
            return resp

    class _SaveSnapshot(EnvironmentsRestStub):
        def __hash__(self):
            return hash("SaveSnapshot")

        def __call__(
            self,
            request: environments.SaveSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the save snapshot method over HTTP.

            Args:
                request (~.environments.SaveSnapshotRequest):
                    The request object. Request to create a snapshot of a
                Cloud Composer environment.
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
                    "uri": "/v1/{environment=projects/*/locations/*/environments/*}:saveSnapshot",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_save_snapshot(request, metadata)
            pb_request = environments.SaveSnapshotRequest.pb(request)
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
            resp = self._interceptor.post_save_snapshot(resp)
            return resp

    class _StopAirflowCommand(EnvironmentsRestStub):
        def __hash__(self):
            return hash("StopAirflowCommand")

        def __call__(
            self,
            request: environments.StopAirflowCommandRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.StopAirflowCommandResponse:
            r"""Call the stop airflow command method over HTTP.

            Args:
                request (~.environments.StopAirflowCommandRequest):
                    The request object. Stop Airflow Command request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.environments.StopAirflowCommandResponse:
                    Response to
                StopAirflowCommandRequest.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{environment=projects/*/locations/*/environments/*}:stopAirflowCommand",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_stop_airflow_command(
                request, metadata
            )
            pb_request = environments.StopAirflowCommandRequest.pb(request)
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
            resp = environments.StopAirflowCommandResponse()
            pb_resp = environments.StopAirflowCommandResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_stop_airflow_command(resp)
            return resp

    class _UpdateEnvironment(EnvironmentsRestStub):
        def __hash__(self):
            return hash("UpdateEnvironment")

        def __call__(
            self,
            request: environments.UpdateEnvironmentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update environment method over HTTP.

            Args:
                request (~.environments.UpdateEnvironmentRequest):
                    The request object. Update an environment.
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
                    "uri": "/v1/{name=projects/*/locations/*/environments/*}",
                    "body": "environment",
                },
            ]
            request, metadata = self._interceptor.pre_update_environment(
                request, metadata
            )
            pb_request = environments.UpdateEnvironmentRequest.pb(request)
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
            resp = self._interceptor.post_update_environment(resp)
            return resp

    class _UpdateUserWorkloadsConfigMap(EnvironmentsRestStub):
        def __hash__(self):
            return hash("UpdateUserWorkloadsConfigMap")

        def __call__(
            self,
            request: environments.UpdateUserWorkloadsConfigMapRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.UserWorkloadsConfigMap:
            r"""Call the update user workloads
            config map method over HTTP.

                Args:
                    request (~.environments.UpdateUserWorkloadsConfigMapRequest):
                        The request object. Update user workloads ConfigMap
                    request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.environments.UserWorkloadsConfigMap:
                        User workloads ConfigMap used by
                    Airflow tasks that run with Kubernetes
                    executor or KubernetesPodOperator.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1/{user_workloads_config_map.name=projects/*/locations/*/environments/*/userWorkloadsConfigMaps/*}",
                    "body": "user_workloads_config_map",
                },
            ]
            request, metadata = self._interceptor.pre_update_user_workloads_config_map(
                request, metadata
            )
            pb_request = environments.UpdateUserWorkloadsConfigMapRequest.pb(request)
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
            resp = environments.UserWorkloadsConfigMap()
            pb_resp = environments.UserWorkloadsConfigMap.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_user_workloads_config_map(resp)
            return resp

    class _UpdateUserWorkloadsSecret(EnvironmentsRestStub):
        def __hash__(self):
            return hash("UpdateUserWorkloadsSecret")

        def __call__(
            self,
            request: environments.UpdateUserWorkloadsSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> environments.UserWorkloadsSecret:
            r"""Call the update user workloads
            secret method over HTTP.

                Args:
                    request (~.environments.UpdateUserWorkloadsSecretRequest):
                        The request object. Update user workloads Secret request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.environments.UserWorkloadsSecret:
                        User workloads Secret used by Airflow
                    tasks that run with Kubernetes executor
                    or KubernetesPodOperator.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "put",
                    "uri": "/v1/{user_workloads_secret.name=projects/*/locations/*/environments/*/userWorkloadsSecrets/*}",
                    "body": "user_workloads_secret",
                },
            ]
            request, metadata = self._interceptor.pre_update_user_workloads_secret(
                request, metadata
            )
            pb_request = environments.UpdateUserWorkloadsSecretRequest.pb(request)
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
            resp = environments.UserWorkloadsSecret()
            pb_resp = environments.UserWorkloadsSecret.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_user_workloads_secret(resp)
            return resp

    @property
    def create_environment(
        self,
    ) -> Callable[[environments.CreateEnvironmentRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_user_workloads_config_map(
        self,
    ) -> Callable[
        [environments.CreateUserWorkloadsConfigMapRequest],
        environments.UserWorkloadsConfigMap,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateUserWorkloadsConfigMap(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_user_workloads_secret(
        self,
    ) -> Callable[
        [environments.CreateUserWorkloadsSecretRequest],
        environments.UserWorkloadsSecret,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateUserWorkloadsSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def database_failover(
        self,
    ) -> Callable[[environments.DatabaseFailoverRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DatabaseFailover(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_environment(
        self,
    ) -> Callable[[environments.DeleteEnvironmentRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_user_workloads_config_map(
        self,
    ) -> Callable[[environments.DeleteUserWorkloadsConfigMapRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteUserWorkloadsConfigMap(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_user_workloads_secret(
        self,
    ) -> Callable[[environments.DeleteUserWorkloadsSecretRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteUserWorkloadsSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def execute_airflow_command(
        self,
    ) -> Callable[
        [environments.ExecuteAirflowCommandRequest],
        environments.ExecuteAirflowCommandResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExecuteAirflowCommand(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_database_properties(
        self,
    ) -> Callable[
        [environments.FetchDatabasePropertiesRequest],
        environments.FetchDatabasePropertiesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchDatabaseProperties(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_environment(
        self,
    ) -> Callable[[environments.GetEnvironmentRequest], environments.Environment]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_user_workloads_config_map(
        self,
    ) -> Callable[
        [environments.GetUserWorkloadsConfigMapRequest],
        environments.UserWorkloadsConfigMap,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetUserWorkloadsConfigMap(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_user_workloads_secret(
        self,
    ) -> Callable[
        [environments.GetUserWorkloadsSecretRequest], environments.UserWorkloadsSecret
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetUserWorkloadsSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_environments(
        self,
    ) -> Callable[
        [environments.ListEnvironmentsRequest], environments.ListEnvironmentsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEnvironments(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_user_workloads_config_maps(
        self,
    ) -> Callable[
        [environments.ListUserWorkloadsConfigMapsRequest],
        environments.ListUserWorkloadsConfigMapsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListUserWorkloadsConfigMaps(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_user_workloads_secrets(
        self,
    ) -> Callable[
        [environments.ListUserWorkloadsSecretsRequest],
        environments.ListUserWorkloadsSecretsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListUserWorkloadsSecrets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_workloads(
        self,
    ) -> Callable[
        [environments.ListWorkloadsRequest], environments.ListWorkloadsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListWorkloads(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def load_snapshot(
        self,
    ) -> Callable[[environments.LoadSnapshotRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._LoadSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def poll_airflow_command(
        self,
    ) -> Callable[
        [environments.PollAirflowCommandRequest],
        environments.PollAirflowCommandResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PollAirflowCommand(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def save_snapshot(
        self,
    ) -> Callable[[environments.SaveSnapshotRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SaveSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def stop_airflow_command(
        self,
    ) -> Callable[
        [environments.StopAirflowCommandRequest],
        environments.StopAirflowCommandResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopAirflowCommand(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_environment(
        self,
    ) -> Callable[[environments.UpdateEnvironmentRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEnvironment(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_user_workloads_config_map(
        self,
    ) -> Callable[
        [environments.UpdateUserWorkloadsConfigMapRequest],
        environments.UserWorkloadsConfigMap,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateUserWorkloadsConfigMap(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_user_workloads_secret(
        self,
    ) -> Callable[
        [environments.UpdateUserWorkloadsSecretRequest],
        environments.UserWorkloadsSecret,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateUserWorkloadsSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(EnvironmentsRestStub):
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

    class _GetOperation(EnvironmentsRestStub):
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

    class _ListOperations(EnvironmentsRestStub):
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


__all__ = ("EnvironmentsRestTransport",)
