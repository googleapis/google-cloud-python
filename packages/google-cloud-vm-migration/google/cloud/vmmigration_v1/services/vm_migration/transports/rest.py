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

from google.cloud.vmmigration_v1.types import vmmigration

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseVmMigrationRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class VmMigrationRestInterceptor:
    """Interceptor for VmMigration.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the VmMigrationRestTransport.

    .. code-block:: python
        class MyCustomVmMigrationInterceptor(VmMigrationRestInterceptor):
            def pre_add_group_migration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_add_group_migration(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_cancel_clone_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_cancel_clone_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_cancel_cutover_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_cancel_cutover_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_clone_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_clone_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_cutover_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cutover_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_datacenter_connector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_datacenter_connector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_migrating_vm(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_migrating_vm(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_target_project(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_target_project(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_utilization_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_utilization_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_datacenter_connector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_datacenter_connector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_migrating_vm(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_migrating_vm(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_target_project(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_target_project(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_utilization_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_utilization_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_inventory(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_inventory(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_finalize_migration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_finalize_migration(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_clone_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_clone_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cutover_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cutover_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_datacenter_connector(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_datacenter_connector(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_migrating_vm(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_migrating_vm(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_replication_cycle(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_replication_cycle(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_target_project(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_target_project(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_utilization_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_utilization_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_clone_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_clone_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_cutover_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_cutover_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_datacenter_connectors(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_datacenter_connectors(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_groups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_groups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_migrating_vms(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_migrating_vms(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_replication_cycles(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_replication_cycles(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_target_projects(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_target_projects(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_utilization_reports(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_utilization_reports(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_pause_migration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_pause_migration(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_remove_group_migration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_group_migration(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_resume_migration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resume_migration(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_migration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_migration(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_migrating_vm(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_migrating_vm(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_target_project(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_target_project(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_upgrade_appliance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_upgrade_appliance(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = VmMigrationRestTransport(interceptor=MyCustomVmMigrationInterceptor())
        client = VmMigrationClient(transport=transport)


    """

    def pre_add_group_migration(
        self,
        request: vmmigration.AddGroupMigrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.AddGroupMigrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for add_group_migration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_add_group_migration(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for add_group_migration

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_clone_job(
        self,
        request: vmmigration.CancelCloneJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CancelCloneJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_clone_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_cancel_clone_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for cancel_clone_job

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_cutover_job(
        self,
        request: vmmigration.CancelCutoverJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CancelCutoverJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_cutover_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_cancel_cutover_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for cancel_cutover_job

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_create_clone_job(
        self,
        request: vmmigration.CreateCloneJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CreateCloneJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_clone_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_create_clone_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_clone_job

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_create_cutover_job(
        self,
        request: vmmigration.CreateCutoverJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CreateCutoverJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_cutover_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_create_cutover_job(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_cutover_job

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_create_datacenter_connector(
        self,
        request: vmmigration.CreateDatacenterConnectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CreateDatacenterConnectorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_datacenter_connector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_create_datacenter_connector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_datacenter_connector

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_create_group(
        self,
        request: vmmigration.CreateGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CreateGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_create_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_group

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_create_migrating_vm(
        self,
        request: vmmigration.CreateMigratingVmRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CreateMigratingVmRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_migrating_vm

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_create_migrating_vm(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_migrating_vm

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_create_source(
        self,
        request: vmmigration.CreateSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CreateSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_create_source(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_source

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_create_target_project(
        self,
        request: vmmigration.CreateTargetProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CreateTargetProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_target_project

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_create_target_project(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_target_project

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_create_utilization_report(
        self,
        request: vmmigration.CreateUtilizationReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.CreateUtilizationReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_utilization_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_create_utilization_report(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_utilization_report

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_delete_datacenter_connector(
        self,
        request: vmmigration.DeleteDatacenterConnectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.DeleteDatacenterConnectorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_datacenter_connector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_delete_datacenter_connector(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_datacenter_connector

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_delete_group(
        self,
        request: vmmigration.DeleteGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.DeleteGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_delete_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_group

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_delete_migrating_vm(
        self,
        request: vmmigration.DeleteMigratingVmRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.DeleteMigratingVmRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_migrating_vm

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_delete_migrating_vm(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_migrating_vm

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_delete_source(
        self,
        request: vmmigration.DeleteSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.DeleteSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_delete_source(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_source

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_delete_target_project(
        self,
        request: vmmigration.DeleteTargetProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.DeleteTargetProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_target_project

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_delete_target_project(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_target_project

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_delete_utilization_report(
        self,
        request: vmmigration.DeleteUtilizationReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.DeleteUtilizationReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_utilization_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_delete_utilization_report(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_utilization_report

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_inventory(
        self,
        request: vmmigration.FetchInventoryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.FetchInventoryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_inventory

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_fetch_inventory(
        self, response: vmmigration.FetchInventoryResponse
    ) -> vmmigration.FetchInventoryResponse:
        """Post-rpc interceptor for fetch_inventory

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_finalize_migration(
        self,
        request: vmmigration.FinalizeMigrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.FinalizeMigrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for finalize_migration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_finalize_migration(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for finalize_migration

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_get_clone_job(
        self,
        request: vmmigration.GetCloneJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.GetCloneJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_clone_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_clone_job(
        self, response: vmmigration.CloneJob
    ) -> vmmigration.CloneJob:
        """Post-rpc interceptor for get_clone_job

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_get_cutover_job(
        self,
        request: vmmigration.GetCutoverJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.GetCutoverJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cutover_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_cutover_job(
        self, response: vmmigration.CutoverJob
    ) -> vmmigration.CutoverJob:
        """Post-rpc interceptor for get_cutover_job

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_get_datacenter_connector(
        self,
        request: vmmigration.GetDatacenterConnectorRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.GetDatacenterConnectorRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_datacenter_connector

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_datacenter_connector(
        self, response: vmmigration.DatacenterConnector
    ) -> vmmigration.DatacenterConnector:
        """Post-rpc interceptor for get_datacenter_connector

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_get_group(
        self, request: vmmigration.GetGroupRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[vmmigration.GetGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_group(self, response: vmmigration.Group) -> vmmigration.Group:
        """Post-rpc interceptor for get_group

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_get_migrating_vm(
        self,
        request: vmmigration.GetMigratingVmRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.GetMigratingVmRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_migrating_vm

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_migrating_vm(
        self, response: vmmigration.MigratingVm
    ) -> vmmigration.MigratingVm:
        """Post-rpc interceptor for get_migrating_vm

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_get_replication_cycle(
        self,
        request: vmmigration.GetReplicationCycleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.GetReplicationCycleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_replication_cycle

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_replication_cycle(
        self, response: vmmigration.ReplicationCycle
    ) -> vmmigration.ReplicationCycle:
        """Post-rpc interceptor for get_replication_cycle

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_get_source(
        self, request: vmmigration.GetSourceRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[vmmigration.GetSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_source(self, response: vmmigration.Source) -> vmmigration.Source:
        """Post-rpc interceptor for get_source

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_get_target_project(
        self,
        request: vmmigration.GetTargetProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.GetTargetProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_target_project

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_target_project(
        self, response: vmmigration.TargetProject
    ) -> vmmigration.TargetProject:
        """Post-rpc interceptor for get_target_project

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_get_utilization_report(
        self,
        request: vmmigration.GetUtilizationReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.GetUtilizationReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_utilization_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_utilization_report(
        self, response: vmmigration.UtilizationReport
    ) -> vmmigration.UtilizationReport:
        """Post-rpc interceptor for get_utilization_report

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_list_clone_jobs(
        self,
        request: vmmigration.ListCloneJobsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ListCloneJobsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_clone_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_clone_jobs(
        self, response: vmmigration.ListCloneJobsResponse
    ) -> vmmigration.ListCloneJobsResponse:
        """Post-rpc interceptor for list_clone_jobs

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_list_cutover_jobs(
        self,
        request: vmmigration.ListCutoverJobsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ListCutoverJobsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_cutover_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_cutover_jobs(
        self, response: vmmigration.ListCutoverJobsResponse
    ) -> vmmigration.ListCutoverJobsResponse:
        """Post-rpc interceptor for list_cutover_jobs

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_list_datacenter_connectors(
        self,
        request: vmmigration.ListDatacenterConnectorsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ListDatacenterConnectorsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_datacenter_connectors

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_datacenter_connectors(
        self, response: vmmigration.ListDatacenterConnectorsResponse
    ) -> vmmigration.ListDatacenterConnectorsResponse:
        """Post-rpc interceptor for list_datacenter_connectors

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_list_groups(
        self,
        request: vmmigration.ListGroupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ListGroupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_groups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_groups(
        self, response: vmmigration.ListGroupsResponse
    ) -> vmmigration.ListGroupsResponse:
        """Post-rpc interceptor for list_groups

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_list_migrating_vms(
        self,
        request: vmmigration.ListMigratingVmsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ListMigratingVmsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_migrating_vms

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_migrating_vms(
        self, response: vmmigration.ListMigratingVmsResponse
    ) -> vmmigration.ListMigratingVmsResponse:
        """Post-rpc interceptor for list_migrating_vms

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_list_replication_cycles(
        self,
        request: vmmigration.ListReplicationCyclesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ListReplicationCyclesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_replication_cycles

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_replication_cycles(
        self, response: vmmigration.ListReplicationCyclesResponse
    ) -> vmmigration.ListReplicationCyclesResponse:
        """Post-rpc interceptor for list_replication_cycles

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_list_sources(
        self,
        request: vmmigration.ListSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ListSourcesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_sources(
        self, response: vmmigration.ListSourcesResponse
    ) -> vmmigration.ListSourcesResponse:
        """Post-rpc interceptor for list_sources

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_list_target_projects(
        self,
        request: vmmigration.ListTargetProjectsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ListTargetProjectsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_target_projects

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_target_projects(
        self, response: vmmigration.ListTargetProjectsResponse
    ) -> vmmigration.ListTargetProjectsResponse:
        """Post-rpc interceptor for list_target_projects

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_list_utilization_reports(
        self,
        request: vmmigration.ListUtilizationReportsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ListUtilizationReportsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_utilization_reports

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_utilization_reports(
        self, response: vmmigration.ListUtilizationReportsResponse
    ) -> vmmigration.ListUtilizationReportsResponse:
        """Post-rpc interceptor for list_utilization_reports

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_pause_migration(
        self,
        request: vmmigration.PauseMigrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.PauseMigrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for pause_migration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_pause_migration(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for pause_migration

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_remove_group_migration(
        self,
        request: vmmigration.RemoveGroupMigrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.RemoveGroupMigrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for remove_group_migration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_remove_group_migration(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for remove_group_migration

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_resume_migration(
        self,
        request: vmmigration.ResumeMigrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.ResumeMigrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for resume_migration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_resume_migration(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for resume_migration

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_start_migration(
        self,
        request: vmmigration.StartMigrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.StartMigrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for start_migration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_start_migration(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for start_migration

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_update_group(
        self,
        request: vmmigration.UpdateGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.UpdateGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_update_group(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_group

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_update_migrating_vm(
        self,
        request: vmmigration.UpdateMigratingVmRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.UpdateMigratingVmRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_migrating_vm

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_update_migrating_vm(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_migrating_vm

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_update_source(
        self,
        request: vmmigration.UpdateSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.UpdateSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_update_source(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_source

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_update_target_project(
        self,
        request: vmmigration.UpdateTargetProjectRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.UpdateTargetProjectRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_target_project

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_update_target_project(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_target_project

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response

    def pre_upgrade_appliance(
        self,
        request: vmmigration.UpgradeApplianceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[vmmigration.UpgradeApplianceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for upgrade_appliance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_upgrade_appliance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for upgrade_appliance

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
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
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
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
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
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
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
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
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
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
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
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
        before they are sent to the VmMigration server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the VmMigration server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class VmMigrationRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: VmMigrationRestInterceptor


class VmMigrationRestTransport(_BaseVmMigrationRestTransport):
    """REST backend synchronous transport for VmMigration.

    VM Migration Service

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "vmmigration.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[VmMigrationRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'vmmigration.googleapis.com').
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
        self._interceptor = interceptor or VmMigrationRestInterceptor()
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

    class _AddGroupMigration(
        _BaseVmMigrationRestTransport._BaseAddGroupMigration, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.AddGroupMigration")

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
            request: vmmigration.AddGroupMigrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the add group migration method over HTTP.

            Args:
                request (~.vmmigration.AddGroupMigrationRequest):
                    The request object. Request message for
                'AddGroupMigration' request.
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
                _BaseVmMigrationRestTransport._BaseAddGroupMigration._get_http_options()
            )
            request, metadata = self._interceptor.pre_add_group_migration(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseAddGroupMigration._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseAddGroupMigration._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseAddGroupMigration._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._AddGroupMigration._get_response(
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
            resp = self._interceptor.post_add_group_migration(resp)
            return resp

    class _CancelCloneJob(
        _BaseVmMigrationRestTransport._BaseCancelCloneJob, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CancelCloneJob")

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
            request: vmmigration.CancelCloneJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the cancel clone job method over HTTP.

            Args:
                request (~.vmmigration.CancelCloneJobRequest):
                    The request object. Request message for 'CancelCloneJob'
                request.
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
                _BaseVmMigrationRestTransport._BaseCancelCloneJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_clone_job(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseCancelCloneJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseCancelCloneJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseCancelCloneJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._CancelCloneJob._get_response(
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
            resp = self._interceptor.post_cancel_clone_job(resp)
            return resp

    class _CancelCutoverJob(
        _BaseVmMigrationRestTransport._BaseCancelCutoverJob, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CancelCutoverJob")

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
            request: vmmigration.CancelCutoverJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the cancel cutover job method over HTTP.

            Args:
                request (~.vmmigration.CancelCutoverJobRequest):
                    The request object. Request message for
                'CancelCutoverJob' request.
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
                _BaseVmMigrationRestTransport._BaseCancelCutoverJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_cutover_job(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseCancelCutoverJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseCancelCutoverJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseCancelCutoverJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._CancelCutoverJob._get_response(
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
            resp = self._interceptor.post_cancel_cutover_job(resp)
            return resp

    class _CreateCloneJob(
        _BaseVmMigrationRestTransport._BaseCreateCloneJob, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CreateCloneJob")

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
            request: vmmigration.CreateCloneJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create clone job method over HTTP.

            Args:
                request (~.vmmigration.CreateCloneJobRequest):
                    The request object. Request message for 'CreateCloneJob'
                request.
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
                _BaseVmMigrationRestTransport._BaseCreateCloneJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_clone_job(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseCreateCloneJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseCreateCloneJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseCreateCloneJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._CreateCloneJob._get_response(
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
            resp = self._interceptor.post_create_clone_job(resp)
            return resp

    class _CreateCutoverJob(
        _BaseVmMigrationRestTransport._BaseCreateCutoverJob, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CreateCutoverJob")

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
            request: vmmigration.CreateCutoverJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cutover job method over HTTP.

            Args:
                request (~.vmmigration.CreateCutoverJobRequest):
                    The request object. Request message for
                'CreateCutoverJob' request.
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
                _BaseVmMigrationRestTransport._BaseCreateCutoverJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_cutover_job(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseCreateCutoverJob._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseCreateCutoverJob._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseCreateCutoverJob._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._CreateCutoverJob._get_response(
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
            resp = self._interceptor.post_create_cutover_job(resp)
            return resp

    class _CreateDatacenterConnector(
        _BaseVmMigrationRestTransport._BaseCreateDatacenterConnector,
        VmMigrationRestStub,
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CreateDatacenterConnector")

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
            request: vmmigration.CreateDatacenterConnectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create datacenter
            connector method over HTTP.

                Args:
                    request (~.vmmigration.CreateDatacenterConnectorRequest):
                        The request object. Request message for
                    'CreateDatacenterConnector' request.
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
                _BaseVmMigrationRestTransport._BaseCreateDatacenterConnector._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_datacenter_connector(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseCreateDatacenterConnector._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseCreateDatacenterConnector._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseCreateDatacenterConnector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                VmMigrationRestTransport._CreateDatacenterConnector._get_response(
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
            resp = self._interceptor.post_create_datacenter_connector(resp)
            return resp

    class _CreateGroup(
        _BaseVmMigrationRestTransport._BaseCreateGroup, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CreateGroup")

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
            request: vmmigration.CreateGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create group method over HTTP.

            Args:
                request (~.vmmigration.CreateGroupRequest):
                    The request object. Request message for 'CreateGroup'
                request.
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
                _BaseVmMigrationRestTransport._BaseCreateGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_group(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseCreateGroup._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseVmMigrationRestTransport._BaseCreateGroup._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseCreateGroup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._CreateGroup._get_response(
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
            resp = self._interceptor.post_create_group(resp)
            return resp

    class _CreateMigratingVm(
        _BaseVmMigrationRestTransport._BaseCreateMigratingVm, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CreateMigratingVm")

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
            request: vmmigration.CreateMigratingVmRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create migrating vm method over HTTP.

            Args:
                request (~.vmmigration.CreateMigratingVmRequest):
                    The request object. Request message for
                'CreateMigratingVm' request.
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
                _BaseVmMigrationRestTransport._BaseCreateMigratingVm._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_migrating_vm(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseCreateMigratingVm._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseCreateMigratingVm._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseCreateMigratingVm._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._CreateMigratingVm._get_response(
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
            resp = self._interceptor.post_create_migrating_vm(resp)
            return resp

    class _CreateSource(
        _BaseVmMigrationRestTransport._BaseCreateSource, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CreateSource")

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
            request: vmmigration.CreateSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create source method over HTTP.

            Args:
                request (~.vmmigration.CreateSourceRequest):
                    The request object. Request message for 'CreateSource'
                request.
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
                _BaseVmMigrationRestTransport._BaseCreateSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_source(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseCreateSource._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseVmMigrationRestTransport._BaseCreateSource._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseCreateSource._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._CreateSource._get_response(
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
            resp = self._interceptor.post_create_source(resp)
            return resp

    class _CreateTargetProject(
        _BaseVmMigrationRestTransport._BaseCreateTargetProject, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CreateTargetProject")

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
            request: vmmigration.CreateTargetProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create target project method over HTTP.

            Args:
                request (~.vmmigration.CreateTargetProjectRequest):
                    The request object. Request message for
                'CreateTargetProject' request.
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
                _BaseVmMigrationRestTransport._BaseCreateTargetProject._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_target_project(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseCreateTargetProject._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseCreateTargetProject._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseCreateTargetProject._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._CreateTargetProject._get_response(
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
            resp = self._interceptor.post_create_target_project(resp)
            return resp

    class _CreateUtilizationReport(
        _BaseVmMigrationRestTransport._BaseCreateUtilizationReport, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CreateUtilizationReport")

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
            request: vmmigration.CreateUtilizationReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create utilization report method over HTTP.

            Args:
                request (~.vmmigration.CreateUtilizationReportRequest):
                    The request object. Request message for
                'CreateUtilizationReport' request.
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
                _BaseVmMigrationRestTransport._BaseCreateUtilizationReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_utilization_report(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseCreateUtilizationReport._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseCreateUtilizationReport._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseCreateUtilizationReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._CreateUtilizationReport._get_response(
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
            resp = self._interceptor.post_create_utilization_report(resp)
            return resp

    class _DeleteDatacenterConnector(
        _BaseVmMigrationRestTransport._BaseDeleteDatacenterConnector,
        VmMigrationRestStub,
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.DeleteDatacenterConnector")

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
            request: vmmigration.DeleteDatacenterConnectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete datacenter
            connector method over HTTP.

                Args:
                    request (~.vmmigration.DeleteDatacenterConnectorRequest):
                        The request object. Request message for
                    'DeleteDatacenterConnector' request.
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
                _BaseVmMigrationRestTransport._BaseDeleteDatacenterConnector._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_datacenter_connector(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseDeleteDatacenterConnector._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseDeleteDatacenterConnector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                VmMigrationRestTransport._DeleteDatacenterConnector._get_response(
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
            resp = self._interceptor.post_delete_datacenter_connector(resp)
            return resp

    class _DeleteGroup(
        _BaseVmMigrationRestTransport._BaseDeleteGroup, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.DeleteGroup")

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
            request: vmmigration.DeleteGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete group method over HTTP.

            Args:
                request (~.vmmigration.DeleteGroupRequest):
                    The request object. Request message for 'DeleteGroup'
                request.
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
                _BaseVmMigrationRestTransport._BaseDeleteGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_group(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseDeleteGroup._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseDeleteGroup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._DeleteGroup._get_response(
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
            resp = self._interceptor.post_delete_group(resp)
            return resp

    class _DeleteMigratingVm(
        _BaseVmMigrationRestTransport._BaseDeleteMigratingVm, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.DeleteMigratingVm")

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
            request: vmmigration.DeleteMigratingVmRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete migrating vm method over HTTP.

            Args:
                request (~.vmmigration.DeleteMigratingVmRequest):
                    The request object. Request message for
                'DeleteMigratingVm' request.
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
                _BaseVmMigrationRestTransport._BaseDeleteMigratingVm._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_migrating_vm(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseDeleteMigratingVm._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseDeleteMigratingVm._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._DeleteMigratingVm._get_response(
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
            resp = self._interceptor.post_delete_migrating_vm(resp)
            return resp

    class _DeleteSource(
        _BaseVmMigrationRestTransport._BaseDeleteSource, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.DeleteSource")

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
            request: vmmigration.DeleteSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete source method over HTTP.

            Args:
                request (~.vmmigration.DeleteSourceRequest):
                    The request object. Request message for 'DeleteSource'
                request.
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
                _BaseVmMigrationRestTransport._BaseDeleteSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_source(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseDeleteSource._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseDeleteSource._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._DeleteSource._get_response(
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
            resp = self._interceptor.post_delete_source(resp)
            return resp

    class _DeleteTargetProject(
        _BaseVmMigrationRestTransport._BaseDeleteTargetProject, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.DeleteTargetProject")

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
            request: vmmigration.DeleteTargetProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete target project method over HTTP.

            Args:
                request (~.vmmigration.DeleteTargetProjectRequest):
                    The request object. Request message for
                'DeleteTargetProject' request.
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
                _BaseVmMigrationRestTransport._BaseDeleteTargetProject._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_target_project(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseDeleteTargetProject._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseDeleteTargetProject._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._DeleteTargetProject._get_response(
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
            resp = self._interceptor.post_delete_target_project(resp)
            return resp

    class _DeleteUtilizationReport(
        _BaseVmMigrationRestTransport._BaseDeleteUtilizationReport, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.DeleteUtilizationReport")

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
            request: vmmigration.DeleteUtilizationReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete utilization report method over HTTP.

            Args:
                request (~.vmmigration.DeleteUtilizationReportRequest):
                    The request object. Request message for
                'DeleteUtilizationReport' request.
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
                _BaseVmMigrationRestTransport._BaseDeleteUtilizationReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_utilization_report(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseDeleteUtilizationReport._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseDeleteUtilizationReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._DeleteUtilizationReport._get_response(
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
            resp = self._interceptor.post_delete_utilization_report(resp)
            return resp

    class _FetchInventory(
        _BaseVmMigrationRestTransport._BaseFetchInventory, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.FetchInventory")

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
            request: vmmigration.FetchInventoryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.FetchInventoryResponse:
            r"""Call the fetch inventory method over HTTP.

            Args:
                request (~.vmmigration.FetchInventoryRequest):
                    The request object. Request message for
                [fetchInventory][google.cloud.vmmigration.v1.VmMigration.FetchInventory].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.FetchInventoryResponse:
                    Response message for
                [fetchInventory][google.cloud.vmmigration.v1.VmMigration.FetchInventory].

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseFetchInventory._get_http_options()
            )
            request, metadata = self._interceptor.pre_fetch_inventory(request, metadata)
            transcoded_request = _BaseVmMigrationRestTransport._BaseFetchInventory._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseFetchInventory._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._FetchInventory._get_response(
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
            resp = vmmigration.FetchInventoryResponse()
            pb_resp = vmmigration.FetchInventoryResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_inventory(resp)
            return resp

    class _FinalizeMigration(
        _BaseVmMigrationRestTransport._BaseFinalizeMigration, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.FinalizeMigration")

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
            request: vmmigration.FinalizeMigrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the finalize migration method over HTTP.

            Args:
                request (~.vmmigration.FinalizeMigrationRequest):
                    The request object. Request message for
                'FinalizeMigration' request.
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
                _BaseVmMigrationRestTransport._BaseFinalizeMigration._get_http_options()
            )
            request, metadata = self._interceptor.pre_finalize_migration(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseFinalizeMigration._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseFinalizeMigration._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseFinalizeMigration._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._FinalizeMigration._get_response(
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
            resp = self._interceptor.post_finalize_migration(resp)
            return resp

    class _GetCloneJob(
        _BaseVmMigrationRestTransport._BaseGetCloneJob, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetCloneJob")

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
            request: vmmigration.GetCloneJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.CloneJob:
            r"""Call the get clone job method over HTTP.

            Args:
                request (~.vmmigration.GetCloneJobRequest):
                    The request object. Request message for 'GetCloneJob'
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.CloneJob:
                    CloneJob describes the process of creating a clone of a
                [MigratingVM][google.cloud.vmmigration.v1.MigratingVm]
                to the requested target based on the latest successful
                uploaded snapshots. While the migration cycles of a
                MigratingVm take place, it is possible to verify the
                uploaded VM can be started in the cloud, by creating a
                clone. The clone can be created without any downtime,
                and it is created using the latest snapshots which are
                already in the cloud. The cloneJob is only responsible
                for its work, not its products, which means once it is
                finished, it will never touch the instance it created.
                It will only delete it in case of the CloneJob being
                cancelled or upon failure to clone.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseGetCloneJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_clone_job(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseGetCloneJob._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseGetCloneJob._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._GetCloneJob._get_response(
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
            resp = vmmigration.CloneJob()
            pb_resp = vmmigration.CloneJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_clone_job(resp)
            return resp

    class _GetCutoverJob(
        _BaseVmMigrationRestTransport._BaseGetCutoverJob, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetCutoverJob")

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
            request: vmmigration.GetCutoverJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.CutoverJob:
            r"""Call the get cutover job method over HTTP.

            Args:
                request (~.vmmigration.GetCutoverJobRequest):
                    The request object. Request message for 'GetCutoverJob'
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.CutoverJob:
                    CutoverJob message describes a
                cutover of a migrating VM. The
                CutoverJob is the operation of shutting
                down the VM, creating a snapshot and
                clonning the VM using the replicated
                snapshot.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseGetCutoverJob._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_cutover_job(request, metadata)
            transcoded_request = _BaseVmMigrationRestTransport._BaseGetCutoverJob._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseGetCutoverJob._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._GetCutoverJob._get_response(
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
            resp = vmmigration.CutoverJob()
            pb_resp = vmmigration.CutoverJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_cutover_job(resp)
            return resp

    class _GetDatacenterConnector(
        _BaseVmMigrationRestTransport._BaseGetDatacenterConnector, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetDatacenterConnector")

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
            request: vmmigration.GetDatacenterConnectorRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.DatacenterConnector:
            r"""Call the get datacenter connector method over HTTP.

            Args:
                request (~.vmmigration.GetDatacenterConnectorRequest):
                    The request object. Request message for
                'GetDatacenterConnector' request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.DatacenterConnector:
                    DatacenterConnector message describes
                a connector between the Source and
                Google Cloud, which is installed on a
                vmware datacenter (an OVA vm installed
                by the user) to connect the Datacenter
                to Google Cloud and support vm migration
                data transfer.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseGetDatacenterConnector._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_datacenter_connector(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseGetDatacenterConnector._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseGetDatacenterConnector._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._GetDatacenterConnector._get_response(
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
            resp = vmmigration.DatacenterConnector()
            pb_resp = vmmigration.DatacenterConnector.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_datacenter_connector(resp)
            return resp

    class _GetGroup(_BaseVmMigrationRestTransport._BaseGetGroup, VmMigrationRestStub):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetGroup")

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
            request: vmmigration.GetGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.Group:
            r"""Call the get group method over HTTP.

            Args:
                request (~.vmmigration.GetGroupRequest):
                    The request object. Request message for 'GetGroup'
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.Group:
                    Describes message for 'Group'
                resource. The Group is a collections of
                several MigratingVms.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseGetGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_group(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseGetGroup._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseGetGroup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._GetGroup._get_response(
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
            resp = vmmigration.Group()
            pb_resp = vmmigration.Group.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_group(resp)
            return resp

    class _GetMigratingVm(
        _BaseVmMigrationRestTransport._BaseGetMigratingVm, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetMigratingVm")

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
            request: vmmigration.GetMigratingVmRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.MigratingVm:
            r"""Call the get migrating vm method over HTTP.

            Args:
                request (~.vmmigration.GetMigratingVmRequest):
                    The request object. Request message for 'GetMigratingVm'
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.MigratingVm:
                    MigratingVm describes the VM that
                will be migrated from a Source
                environment and its replication state.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseGetMigratingVm._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_migrating_vm(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseGetMigratingVm._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseGetMigratingVm._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._GetMigratingVm._get_response(
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
            resp = vmmigration.MigratingVm()
            pb_resp = vmmigration.MigratingVm.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_migrating_vm(resp)
            return resp

    class _GetReplicationCycle(
        _BaseVmMigrationRestTransport._BaseGetReplicationCycle, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetReplicationCycle")

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
            request: vmmigration.GetReplicationCycleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ReplicationCycle:
            r"""Call the get replication cycle method over HTTP.

            Args:
                request (~.vmmigration.GetReplicationCycleRequest):
                    The request object. Request message for
                'GetReplicationCycle' request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.ReplicationCycle:
                    ReplicationCycle contains information
                about the current replication cycle
                status.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseGetReplicationCycle._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_replication_cycle(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseGetReplicationCycle._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseGetReplicationCycle._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._GetReplicationCycle._get_response(
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
            resp = vmmigration.ReplicationCycle()
            pb_resp = vmmigration.ReplicationCycle.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_replication_cycle(resp)
            return resp

    class _GetSource(_BaseVmMigrationRestTransport._BaseGetSource, VmMigrationRestStub):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetSource")

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
            request: vmmigration.GetSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.Source:
            r"""Call the get source method over HTTP.

            Args:
                request (~.vmmigration.GetSourceRequest):
                    The request object. Request message for 'GetSource'
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.Source:
                    Source message describes a specific
                vm migration Source resource. It
                contains the source environment
                information.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseGetSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_source(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseGetSource._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseGetSource._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._GetSource._get_response(
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
            resp = vmmigration.Source()
            pb_resp = vmmigration.Source.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_source(resp)
            return resp

    class _GetTargetProject(
        _BaseVmMigrationRestTransport._BaseGetTargetProject, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetTargetProject")

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
            request: vmmigration.GetTargetProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.TargetProject:
            r"""Call the get target project method over HTTP.

            Args:
                request (~.vmmigration.GetTargetProjectRequest):
                    The request object. Request message for
                'GetTargetProject' call.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.TargetProject:
                    TargetProject message represents a
                target Compute Engine project for a
                migration or a clone.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseGetTargetProject._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_target_project(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseGetTargetProject._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseGetTargetProject._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._GetTargetProject._get_response(
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
            resp = vmmigration.TargetProject()
            pb_resp = vmmigration.TargetProject.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_target_project(resp)
            return resp

    class _GetUtilizationReport(
        _BaseVmMigrationRestTransport._BaseGetUtilizationReport, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetUtilizationReport")

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
            request: vmmigration.GetUtilizationReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.UtilizationReport:
            r"""Call the get utilization report method over HTTP.

            Args:
                request (~.vmmigration.GetUtilizationReportRequest):
                    The request object. Request message for
                'GetUtilizationReport' request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.UtilizationReport:
                    Utilization report details the
                utilization (CPU, memory, etc.) of
                selected source VMs.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseGetUtilizationReport._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_utilization_report(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseGetUtilizationReport._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseGetUtilizationReport._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._GetUtilizationReport._get_response(
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
            resp = vmmigration.UtilizationReport()
            pb_resp = vmmigration.UtilizationReport.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_utilization_report(resp)
            return resp

    class _ListCloneJobs(
        _BaseVmMigrationRestTransport._BaseListCloneJobs, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListCloneJobs")

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
            request: vmmigration.ListCloneJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ListCloneJobsResponse:
            r"""Call the list clone jobs method over HTTP.

            Args:
                request (~.vmmigration.ListCloneJobsRequest):
                    The request object. Request message for
                'ListCloneJobsRequest' request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.ListCloneJobsResponse:
                    Response message for 'ListCloneJobs'
                request.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseListCloneJobs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_clone_jobs(request, metadata)
            transcoded_request = _BaseVmMigrationRestTransport._BaseListCloneJobs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseListCloneJobs._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._ListCloneJobs._get_response(
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
            resp = vmmigration.ListCloneJobsResponse()
            pb_resp = vmmigration.ListCloneJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_clone_jobs(resp)
            return resp

    class _ListCutoverJobs(
        _BaseVmMigrationRestTransport._BaseListCutoverJobs, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListCutoverJobs")

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
            request: vmmigration.ListCutoverJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ListCutoverJobsResponse:
            r"""Call the list cutover jobs method over HTTP.

            Args:
                request (~.vmmigration.ListCutoverJobsRequest):
                    The request object. Request message for
                'ListCutoverJobsRequest' request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.ListCutoverJobsResponse:
                    Response message for
                'ListCutoverJobs' request.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseListCutoverJobs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_cutover_jobs(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseListCutoverJobs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseListCutoverJobs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._ListCutoverJobs._get_response(
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
            resp = vmmigration.ListCutoverJobsResponse()
            pb_resp = vmmigration.ListCutoverJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_cutover_jobs(resp)
            return resp

    class _ListDatacenterConnectors(
        _BaseVmMigrationRestTransport._BaseListDatacenterConnectors, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListDatacenterConnectors")

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
            request: vmmigration.ListDatacenterConnectorsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ListDatacenterConnectorsResponse:
            r"""Call the list datacenter
            connectors method over HTTP.

                Args:
                    request (~.vmmigration.ListDatacenterConnectorsRequest):
                        The request object. Request message for
                    'ListDatacenterConnectors' request.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.vmmigration.ListDatacenterConnectorsResponse:
                        Response message for
                    'ListDatacenterConnectors' request.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseListDatacenterConnectors._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_datacenter_connectors(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseListDatacenterConnectors._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseListDatacenterConnectors._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._ListDatacenterConnectors._get_response(
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
            resp = vmmigration.ListDatacenterConnectorsResponse()
            pb_resp = vmmigration.ListDatacenterConnectorsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_datacenter_connectors(resp)
            return resp

    class _ListGroups(
        _BaseVmMigrationRestTransport._BaseListGroups, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListGroups")

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
            request: vmmigration.ListGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ListGroupsResponse:
            r"""Call the list groups method over HTTP.

            Args:
                request (~.vmmigration.ListGroupsRequest):
                    The request object. Request message for 'ListGroups'
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.ListGroupsResponse:
                    Response message for 'ListGroups'
                request.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseListGroups._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_groups(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseListGroups._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseListGroups._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._ListGroups._get_response(
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
            resp = vmmigration.ListGroupsResponse()
            pb_resp = vmmigration.ListGroupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_groups(resp)
            return resp

    class _ListMigratingVms(
        _BaseVmMigrationRestTransport._BaseListMigratingVms, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListMigratingVms")

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
            request: vmmigration.ListMigratingVmsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ListMigratingVmsResponse:
            r"""Call the list migrating vms method over HTTP.

            Args:
                request (~.vmmigration.ListMigratingVmsRequest):
                    The request object. Request message for
                'LisMigratingVmsRequest' request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.ListMigratingVmsResponse:
                    Response message for
                'ListMigratingVms' request.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseListMigratingVms._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_migrating_vms(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseListMigratingVms._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseListMigratingVms._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._ListMigratingVms._get_response(
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
            resp = vmmigration.ListMigratingVmsResponse()
            pb_resp = vmmigration.ListMigratingVmsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_migrating_vms(resp)
            return resp

    class _ListReplicationCycles(
        _BaseVmMigrationRestTransport._BaseListReplicationCycles, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListReplicationCycles")

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
            request: vmmigration.ListReplicationCyclesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ListReplicationCyclesResponse:
            r"""Call the list replication cycles method over HTTP.

            Args:
                request (~.vmmigration.ListReplicationCyclesRequest):
                    The request object. Request message for
                'LisReplicationCyclesRequest' request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.ListReplicationCyclesResponse:
                    Response message for
                'ListReplicationCycles' request.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseListReplicationCycles._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_replication_cycles(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseListReplicationCycles._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseListReplicationCycles._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._ListReplicationCycles._get_response(
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
            resp = vmmigration.ListReplicationCyclesResponse()
            pb_resp = vmmigration.ListReplicationCyclesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_replication_cycles(resp)
            return resp

    class _ListSources(
        _BaseVmMigrationRestTransport._BaseListSources, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListSources")

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
            request: vmmigration.ListSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ListSourcesResponse:
            r"""Call the list sources method over HTTP.

            Args:
                request (~.vmmigration.ListSourcesRequest):
                    The request object. Request message for 'ListSources'
                request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.ListSourcesResponse:
                    Response message for 'ListSources'
                request.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseListSources._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_sources(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseListSources._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseListSources._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._ListSources._get_response(
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
            resp = vmmigration.ListSourcesResponse()
            pb_resp = vmmigration.ListSourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sources(resp)
            return resp

    class _ListTargetProjects(
        _BaseVmMigrationRestTransport._BaseListTargetProjects, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListTargetProjects")

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
            request: vmmigration.ListTargetProjectsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ListTargetProjectsResponse:
            r"""Call the list target projects method over HTTP.

            Args:
                request (~.vmmigration.ListTargetProjectsRequest):
                    The request object. Request message for
                'ListTargetProjects' call.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.ListTargetProjectsResponse:
                    Response message for
                'ListTargetProjects' call.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseListTargetProjects._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_target_projects(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseListTargetProjects._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseListTargetProjects._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._ListTargetProjects._get_response(
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
            resp = vmmigration.ListTargetProjectsResponse()
            pb_resp = vmmigration.ListTargetProjectsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_target_projects(resp)
            return resp

    class _ListUtilizationReports(
        _BaseVmMigrationRestTransport._BaseListUtilizationReports, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListUtilizationReports")

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
            request: vmmigration.ListUtilizationReportsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> vmmigration.ListUtilizationReportsResponse:
            r"""Call the list utilization reports method over HTTP.

            Args:
                request (~.vmmigration.ListUtilizationReportsRequest):
                    The request object. Request message for
                'ListUtilizationReports' request.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.vmmigration.ListUtilizationReportsResponse:
                    Response message for
                'ListUtilizationReports' request.

            """

            http_options = (
                _BaseVmMigrationRestTransport._BaseListUtilizationReports._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_utilization_reports(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseListUtilizationReports._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseListUtilizationReports._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._ListUtilizationReports._get_response(
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
            resp = vmmigration.ListUtilizationReportsResponse()
            pb_resp = vmmigration.ListUtilizationReportsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_utilization_reports(resp)
            return resp

    class _PauseMigration(
        _BaseVmMigrationRestTransport._BasePauseMigration, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.PauseMigration")

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
            request: vmmigration.PauseMigrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the pause migration method over HTTP.

            Args:
                request (~.vmmigration.PauseMigrationRequest):
                    The request object. Request message for 'PauseMigration'
                request.
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
                _BaseVmMigrationRestTransport._BasePauseMigration._get_http_options()
            )
            request, metadata = self._interceptor.pre_pause_migration(request, metadata)
            transcoded_request = _BaseVmMigrationRestTransport._BasePauseMigration._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BasePauseMigration._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BasePauseMigration._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._PauseMigration._get_response(
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
            resp = self._interceptor.post_pause_migration(resp)
            return resp

    class _RemoveGroupMigration(
        _BaseVmMigrationRestTransport._BaseRemoveGroupMigration, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.RemoveGroupMigration")

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
            request: vmmigration.RemoveGroupMigrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the remove group migration method over HTTP.

            Args:
                request (~.vmmigration.RemoveGroupMigrationRequest):
                    The request object. Request message for 'RemoveMigration'
                request.
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
                _BaseVmMigrationRestTransport._BaseRemoveGroupMigration._get_http_options()
            )
            request, metadata = self._interceptor.pre_remove_group_migration(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseRemoveGroupMigration._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseRemoveGroupMigration._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseRemoveGroupMigration._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._RemoveGroupMigration._get_response(
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
            resp = self._interceptor.post_remove_group_migration(resp)
            return resp

    class _ResumeMigration(
        _BaseVmMigrationRestTransport._BaseResumeMigration, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ResumeMigration")

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
            request: vmmigration.ResumeMigrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the resume migration method over HTTP.

            Args:
                request (~.vmmigration.ResumeMigrationRequest):
                    The request object. Request message for 'ResumeMigration'
                request.
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
                _BaseVmMigrationRestTransport._BaseResumeMigration._get_http_options()
            )
            request, metadata = self._interceptor.pre_resume_migration(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseResumeMigration._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseResumeMigration._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseResumeMigration._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._ResumeMigration._get_response(
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
            resp = self._interceptor.post_resume_migration(resp)
            return resp

    class _StartMigration(
        _BaseVmMigrationRestTransport._BaseStartMigration, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.StartMigration")

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
            request: vmmigration.StartMigrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the start migration method over HTTP.

            Args:
                request (~.vmmigration.StartMigrationRequest):
                    The request object. Request message for
                'StartMigrationRequest' request.
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
                _BaseVmMigrationRestTransport._BaseStartMigration._get_http_options()
            )
            request, metadata = self._interceptor.pre_start_migration(request, metadata)
            transcoded_request = _BaseVmMigrationRestTransport._BaseStartMigration._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseStartMigration._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseStartMigration._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._StartMigration._get_response(
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
            resp = self._interceptor.post_start_migration(resp)
            return resp

    class _UpdateGroup(
        _BaseVmMigrationRestTransport._BaseUpdateGroup, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.UpdateGroup")

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
            request: vmmigration.UpdateGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update group method over HTTP.

            Args:
                request (~.vmmigration.UpdateGroupRequest):
                    The request object. Update message for 'UpdateGroups'
                request.
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
                _BaseVmMigrationRestTransport._BaseUpdateGroup._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_group(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseUpdateGroup._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseVmMigrationRestTransport._BaseUpdateGroup._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseUpdateGroup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._UpdateGroup._get_response(
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
            resp = self._interceptor.post_update_group(resp)
            return resp

    class _UpdateMigratingVm(
        _BaseVmMigrationRestTransport._BaseUpdateMigratingVm, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.UpdateMigratingVm")

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
            request: vmmigration.UpdateMigratingVmRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update migrating vm method over HTTP.

            Args:
                request (~.vmmigration.UpdateMigratingVmRequest):
                    The request object. Request message for
                'UpdateMigratingVm' request.
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
                _BaseVmMigrationRestTransport._BaseUpdateMigratingVm._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_migrating_vm(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseUpdateMigratingVm._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseUpdateMigratingVm._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseUpdateMigratingVm._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._UpdateMigratingVm._get_response(
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
            resp = self._interceptor.post_update_migrating_vm(resp)
            return resp

    class _UpdateSource(
        _BaseVmMigrationRestTransport._BaseUpdateSource, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.UpdateSource")

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
            request: vmmigration.UpdateSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update source method over HTTP.

            Args:
                request (~.vmmigration.UpdateSourceRequest):
                    The request object. Update message for 'UpdateSources'
                request.
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
                _BaseVmMigrationRestTransport._BaseUpdateSource._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_source(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseUpdateSource._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseVmMigrationRestTransport._BaseUpdateSource._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseUpdateSource._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._UpdateSource._get_response(
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
            resp = self._interceptor.post_update_source(resp)
            return resp

    class _UpdateTargetProject(
        _BaseVmMigrationRestTransport._BaseUpdateTargetProject, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.UpdateTargetProject")

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
            request: vmmigration.UpdateTargetProjectRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update target project method over HTTP.

            Args:
                request (~.vmmigration.UpdateTargetProjectRequest):
                    The request object. Update message for
                'UpdateTargetProject' request.
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
                _BaseVmMigrationRestTransport._BaseUpdateTargetProject._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_target_project(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseUpdateTargetProject._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseUpdateTargetProject._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseUpdateTargetProject._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._UpdateTargetProject._get_response(
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
            resp = self._interceptor.post_update_target_project(resp)
            return resp

    class _UpgradeAppliance(
        _BaseVmMigrationRestTransport._BaseUpgradeAppliance, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.UpgradeAppliance")

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
            request: vmmigration.UpgradeApplianceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the upgrade appliance method over HTTP.

            Args:
                request (~.vmmigration.UpgradeApplianceRequest):
                    The request object. Request message for
                'UpgradeAppliance' request.
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
                _BaseVmMigrationRestTransport._BaseUpgradeAppliance._get_http_options()
            )
            request, metadata = self._interceptor.pre_upgrade_appliance(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseUpgradeAppliance._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseUpgradeAppliance._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseUpgradeAppliance._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._UpgradeAppliance._get_response(
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
            resp = self._interceptor.post_upgrade_appliance(resp)
            return resp

    @property
    def add_group_migration(
        self,
    ) -> Callable[[vmmigration.AddGroupMigrationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AddGroupMigration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_clone_job(
        self,
    ) -> Callable[[vmmigration.CancelCloneJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelCloneJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_cutover_job(
        self,
    ) -> Callable[[vmmigration.CancelCutoverJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelCutoverJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_clone_job(
        self,
    ) -> Callable[[vmmigration.CreateCloneJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCloneJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_cutover_job(
        self,
    ) -> Callable[[vmmigration.CreateCutoverJobRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCutoverJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_datacenter_connector(
        self,
    ) -> Callable[
        [vmmigration.CreateDatacenterConnectorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDatacenterConnector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_group(
        self,
    ) -> Callable[[vmmigration.CreateGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_migrating_vm(
        self,
    ) -> Callable[[vmmigration.CreateMigratingVmRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMigratingVm(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_source(
        self,
    ) -> Callable[[vmmigration.CreateSourceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_target_project(
        self,
    ) -> Callable[[vmmigration.CreateTargetProjectRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTargetProject(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_utilization_report(
        self,
    ) -> Callable[
        [vmmigration.CreateUtilizationReportRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateUtilizationReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_datacenter_connector(
        self,
    ) -> Callable[
        [vmmigration.DeleteDatacenterConnectorRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDatacenterConnector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_group(
        self,
    ) -> Callable[[vmmigration.DeleteGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_migrating_vm(
        self,
    ) -> Callable[[vmmigration.DeleteMigratingVmRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteMigratingVm(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_source(
        self,
    ) -> Callable[[vmmigration.DeleteSourceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_target_project(
        self,
    ) -> Callable[[vmmigration.DeleteTargetProjectRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTargetProject(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_utilization_report(
        self,
    ) -> Callable[
        [vmmigration.DeleteUtilizationReportRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteUtilizationReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_inventory(
        self,
    ) -> Callable[
        [vmmigration.FetchInventoryRequest], vmmigration.FetchInventoryResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchInventory(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def finalize_migration(
        self,
    ) -> Callable[[vmmigration.FinalizeMigrationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FinalizeMigration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_clone_job(
        self,
    ) -> Callable[[vmmigration.GetCloneJobRequest], vmmigration.CloneJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCloneJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cutover_job(
        self,
    ) -> Callable[[vmmigration.GetCutoverJobRequest], vmmigration.CutoverJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCutoverJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_datacenter_connector(
        self,
    ) -> Callable[
        [vmmigration.GetDatacenterConnectorRequest], vmmigration.DatacenterConnector
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDatacenterConnector(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_group(self) -> Callable[[vmmigration.GetGroupRequest], vmmigration.Group]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_migrating_vm(
        self,
    ) -> Callable[[vmmigration.GetMigratingVmRequest], vmmigration.MigratingVm]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMigratingVm(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_replication_cycle(
        self,
    ) -> Callable[
        [vmmigration.GetReplicationCycleRequest], vmmigration.ReplicationCycle
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetReplicationCycle(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_source(
        self,
    ) -> Callable[[vmmigration.GetSourceRequest], vmmigration.Source]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_target_project(
        self,
    ) -> Callable[[vmmigration.GetTargetProjectRequest], vmmigration.TargetProject]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTargetProject(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_utilization_report(
        self,
    ) -> Callable[
        [vmmigration.GetUtilizationReportRequest], vmmigration.UtilizationReport
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetUtilizationReport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_clone_jobs(
        self,
    ) -> Callable[
        [vmmigration.ListCloneJobsRequest], vmmigration.ListCloneJobsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCloneJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_cutover_jobs(
        self,
    ) -> Callable[
        [vmmigration.ListCutoverJobsRequest], vmmigration.ListCutoverJobsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCutoverJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_datacenter_connectors(
        self,
    ) -> Callable[
        [vmmigration.ListDatacenterConnectorsRequest],
        vmmigration.ListDatacenterConnectorsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDatacenterConnectors(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_groups(
        self,
    ) -> Callable[[vmmigration.ListGroupsRequest], vmmigration.ListGroupsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGroups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_migrating_vms(
        self,
    ) -> Callable[
        [vmmigration.ListMigratingVmsRequest], vmmigration.ListMigratingVmsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMigratingVms(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_replication_cycles(
        self,
    ) -> Callable[
        [vmmigration.ListReplicationCyclesRequest],
        vmmigration.ListReplicationCyclesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReplicationCycles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_sources(
        self,
    ) -> Callable[[vmmigration.ListSourcesRequest], vmmigration.ListSourcesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_target_projects(
        self,
    ) -> Callable[
        [vmmigration.ListTargetProjectsRequest], vmmigration.ListTargetProjectsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTargetProjects(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_utilization_reports(
        self,
    ) -> Callable[
        [vmmigration.ListUtilizationReportsRequest],
        vmmigration.ListUtilizationReportsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListUtilizationReports(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def pause_migration(
        self,
    ) -> Callable[[vmmigration.PauseMigrationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._PauseMigration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_group_migration(
        self,
    ) -> Callable[[vmmigration.RemoveGroupMigrationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveGroupMigration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resume_migration(
        self,
    ) -> Callable[[vmmigration.ResumeMigrationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResumeMigration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_migration(
        self,
    ) -> Callable[[vmmigration.StartMigrationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartMigration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_group(
        self,
    ) -> Callable[[vmmigration.UpdateGroupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_migrating_vm(
        self,
    ) -> Callable[[vmmigration.UpdateMigratingVmRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateMigratingVm(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_source(
        self,
    ) -> Callable[[vmmigration.UpdateSourceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_target_project(
        self,
    ) -> Callable[[vmmigration.UpdateTargetProjectRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTargetProject(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def upgrade_appliance(
        self,
    ) -> Callable[[vmmigration.UpgradeApplianceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpgradeAppliance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseVmMigrationRestTransport._BaseGetLocation, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetLocation")

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
                _BaseVmMigrationRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._GetLocation._get_response(
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
        _BaseVmMigrationRestTransport._BaseListLocations, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListLocations")

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
                _BaseVmMigrationRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseVmMigrationRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._ListLocations._get_response(
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
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseVmMigrationRestTransport._BaseCancelOperation, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.CancelOperation")

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
                _BaseVmMigrationRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseVmMigrationRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._CancelOperation._get_response(
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
        _BaseVmMigrationRestTransport._BaseDeleteOperation, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.DeleteOperation")

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
                _BaseVmMigrationRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseVmMigrationRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._DeleteOperation._get_response(
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
        _BaseVmMigrationRestTransport._BaseGetOperation, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.GetOperation")

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
                _BaseVmMigrationRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseVmMigrationRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseVmMigrationRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = VmMigrationRestTransport._GetOperation._get_response(
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
        _BaseVmMigrationRestTransport._BaseListOperations, VmMigrationRestStub
    ):
        def __hash__(self):
            return hash("VmMigrationRestTransport.ListOperations")

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
                _BaseVmMigrationRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseVmMigrationRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseVmMigrationRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = VmMigrationRestTransport._ListOperations._get_response(
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


__all__ = ("VmMigrationRestTransport",)
