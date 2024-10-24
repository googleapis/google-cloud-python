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

from google.cloud.gke_backup_v1.types import (
    backup,
    backup_plan,
    gkebackup,
    restore,
    restore_plan,
    volume,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseBackupForGKERestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class BackupForGKERestInterceptor:
    """Interceptor for BackupForGKE.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BackupForGKERestTransport.

    .. code-block:: python
        class MyCustomBackupForGKEInterceptor(BackupForGKERestInterceptor):
            def pre_create_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_backup_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_restore(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_restore(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_restore_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_restore_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_restore(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_restore(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_restore_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_restore_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup_index_download_url(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup_index_download_url(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_restore(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_restore(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_restore_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_restore_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_volume_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_volume_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_volume_restore(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_volume_restore(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backup_plans(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backup_plans(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_restore_plans(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_restore_plans(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_restores(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_restores(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_volume_backups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_volume_backups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_volume_restores(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_volume_restores(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_backup_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_restore(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_restore(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_restore_plan(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_restore_plan(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = BackupForGKERestTransport(interceptor=MyCustomBackupForGKEInterceptor())
        client = BackupForGKEClient(transport=transport)


    """

    def pre_create_backup(
        self,
        request: gkebackup.CreateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.CreateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_create_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_create_backup_plan(
        self,
        request: gkebackup.CreateBackupPlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.CreateBackupPlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_create_backup_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_create_restore(
        self,
        request: gkebackup.CreateRestoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.CreateRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_create_restore(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_create_restore_plan(
        self,
        request: gkebackup.CreateRestorePlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.CreateRestorePlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_restore_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_create_restore_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_restore_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup(
        self,
        request: gkebackup.DeleteBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.DeleteBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_delete_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup_plan(
        self,
        request: gkebackup.DeleteBackupPlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.DeleteBackupPlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_delete_backup_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_delete_restore(
        self,
        request: gkebackup.DeleteRestoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.DeleteRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_delete_restore(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_delete_restore_plan(
        self,
        request: gkebackup.DeleteRestorePlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.DeleteRestorePlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_restore_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_delete_restore_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_restore_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup(
        self, request: gkebackup.GetBackupRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gkebackup.GetBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_backup(self, response: backup.Backup) -> backup.Backup:
        """Post-rpc interceptor for get_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup_index_download_url(
        self,
        request: gkebackup.GetBackupIndexDownloadUrlRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.GetBackupIndexDownloadUrlRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup_index_download_url

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_backup_index_download_url(
        self, response: gkebackup.GetBackupIndexDownloadUrlResponse
    ) -> gkebackup.GetBackupIndexDownloadUrlResponse:
        """Post-rpc interceptor for get_backup_index_download_url

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup_plan(
        self,
        request: gkebackup.GetBackupPlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.GetBackupPlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_backup_plan(
        self, response: backup_plan.BackupPlan
    ) -> backup_plan.BackupPlan:
        """Post-rpc interceptor for get_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_restore(
        self, request: gkebackup.GetRestoreRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gkebackup.GetRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_restore(self, response: restore.Restore) -> restore.Restore:
        """Post-rpc interceptor for get_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_restore_plan(
        self,
        request: gkebackup.GetRestorePlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.GetRestorePlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_restore_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_restore_plan(
        self, response: restore_plan.RestorePlan
    ) -> restore_plan.RestorePlan:
        """Post-rpc interceptor for get_restore_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_volume_backup(
        self,
        request: gkebackup.GetVolumeBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.GetVolumeBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_volume_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_volume_backup(
        self, response: volume.VolumeBackup
    ) -> volume.VolumeBackup:
        """Post-rpc interceptor for get_volume_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_volume_restore(
        self,
        request: gkebackup.GetVolumeRestoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.GetVolumeRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_volume_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_volume_restore(
        self, response: volume.VolumeRestore
    ) -> volume.VolumeRestore:
        """Post-rpc interceptor for get_volume_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_backup_plans(
        self,
        request: gkebackup.ListBackupPlansRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListBackupPlansRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backup_plans

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_backup_plans(
        self, response: gkebackup.ListBackupPlansResponse
    ) -> gkebackup.ListBackupPlansResponse:
        """Post-rpc interceptor for list_backup_plans

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_backups(
        self, request: gkebackup.ListBackupsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gkebackup.ListBackupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_backups(
        self, response: gkebackup.ListBackupsResponse
    ) -> gkebackup.ListBackupsResponse:
        """Post-rpc interceptor for list_backups

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_restore_plans(
        self,
        request: gkebackup.ListRestorePlansRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListRestorePlansRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_restore_plans

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_restore_plans(
        self, response: gkebackup.ListRestorePlansResponse
    ) -> gkebackup.ListRestorePlansResponse:
        """Post-rpc interceptor for list_restore_plans

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_restores(
        self,
        request: gkebackup.ListRestoresRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListRestoresRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_restores

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_restores(
        self, response: gkebackup.ListRestoresResponse
    ) -> gkebackup.ListRestoresResponse:
        """Post-rpc interceptor for list_restores

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_volume_backups(
        self,
        request: gkebackup.ListVolumeBackupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListVolumeBackupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_volume_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_volume_backups(
        self, response: gkebackup.ListVolumeBackupsResponse
    ) -> gkebackup.ListVolumeBackupsResponse:
        """Post-rpc interceptor for list_volume_backups

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_volume_restores(
        self,
        request: gkebackup.ListVolumeRestoresRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListVolumeRestoresRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_volume_restores

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_volume_restores(
        self, response: gkebackup.ListVolumeRestoresResponse
    ) -> gkebackup.ListVolumeRestoresResponse:
        """Post-rpc interceptor for list_volume_restores

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup(
        self,
        request: gkebackup.UpdateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.UpdateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_update_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup_plan(
        self,
        request: gkebackup.UpdateBackupPlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.UpdateBackupPlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_update_backup_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_update_restore(
        self,
        request: gkebackup.UpdateRestoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.UpdateRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_update_restore(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_update_restore_plan(
        self,
        request: gkebackup.UpdateRestorePlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.UpdateRestorePlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_restore_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_update_restore_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_restore_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
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
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
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
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
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
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
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
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
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
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
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
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
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
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
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
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
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
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BackupForGKERestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BackupForGKERestInterceptor


class BackupForGKERestTransport(_BaseBackupForGKERestTransport):
    """REST backend synchronous transport for BackupForGKE.

    BackupForGKE allows Kubernetes administrators to configure,
    execute, and manage backup and restore operations for their GKE
    clusters.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "gkebackup.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[BackupForGKERestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'gkebackup.googleapis.com').
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
        self._interceptor = interceptor or BackupForGKERestInterceptor()
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

    class _CreateBackup(
        _BaseBackupForGKERestTransport._BaseCreateBackup, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.CreateBackup")

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
            request: gkebackup.CreateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup method over HTTP.

            Args:
                request (~.gkebackup.CreateBackupRequest):
                    The request object. Request message for CreateBackup.
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
                _BaseBackupForGKERestTransport._BaseCreateBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_backup(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseCreateBackup._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseBackupForGKERestTransport._BaseCreateBackup._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseCreateBackup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._CreateBackup._get_response(
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
            resp = self._interceptor.post_create_backup(resp)
            return resp

    class _CreateBackupPlan(
        _BaseBackupForGKERestTransport._BaseCreateBackupPlan, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.CreateBackupPlan")

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
            request: gkebackup.CreateBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup plan method over HTTP.

            Args:
                request (~.gkebackup.CreateBackupPlanRequest):
                    The request object. Request message for CreateBackupPlan.
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
                _BaseBackupForGKERestTransport._BaseCreateBackupPlan._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_backup_plan(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseCreateBackupPlan._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupForGKERestTransport._BaseCreateBackupPlan._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseCreateBackupPlan._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._CreateBackupPlan._get_response(
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
            resp = self._interceptor.post_create_backup_plan(resp)
            return resp

    class _CreateRestore(
        _BaseBackupForGKERestTransport._BaseCreateRestore, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.CreateRestore")

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
            request: gkebackup.CreateRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create restore method over HTTP.

            Args:
                request (~.gkebackup.CreateRestoreRequest):
                    The request object. Request message for CreateRestore.
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
                _BaseBackupForGKERestTransport._BaseCreateRestore._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_restore(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseCreateRestore._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupForGKERestTransport._BaseCreateRestore._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseCreateRestore._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._CreateRestore._get_response(
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
            resp = self._interceptor.post_create_restore(resp)
            return resp

    class _CreateRestorePlan(
        _BaseBackupForGKERestTransport._BaseCreateRestorePlan, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.CreateRestorePlan")

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
            request: gkebackup.CreateRestorePlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create restore plan method over HTTP.

            Args:
                request (~.gkebackup.CreateRestorePlanRequest):
                    The request object. Request message for
                CreateRestorePlan.
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
                _BaseBackupForGKERestTransport._BaseCreateRestorePlan._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_restore_plan(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseCreateRestorePlan._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupForGKERestTransport._BaseCreateRestorePlan._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseCreateRestorePlan._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._CreateRestorePlan._get_response(
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
            resp = self._interceptor.post_create_restore_plan(resp)
            return resp

    class _DeleteBackup(
        _BaseBackupForGKERestTransport._BaseDeleteBackup, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.DeleteBackup")

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
            request: gkebackup.DeleteBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup method over HTTP.

            Args:
                request (~.gkebackup.DeleteBackupRequest):
                    The request object. Request message for DeleteBackup.
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
                _BaseBackupForGKERestTransport._BaseDeleteBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_backup(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseDeleteBackup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseDeleteBackup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._DeleteBackup._get_response(
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
            resp = self._interceptor.post_delete_backup(resp)
            return resp

    class _DeleteBackupPlan(
        _BaseBackupForGKERestTransport._BaseDeleteBackupPlan, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.DeleteBackupPlan")

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
            request: gkebackup.DeleteBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup plan method over HTTP.

            Args:
                request (~.gkebackup.DeleteBackupPlanRequest):
                    The request object. Request message for DeleteBackupPlan.
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
                _BaseBackupForGKERestTransport._BaseDeleteBackupPlan._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_backup_plan(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseDeleteBackupPlan._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseDeleteBackupPlan._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._DeleteBackupPlan._get_response(
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
            resp = self._interceptor.post_delete_backup_plan(resp)
            return resp

    class _DeleteRestore(
        _BaseBackupForGKERestTransport._BaseDeleteRestore, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.DeleteRestore")

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
            request: gkebackup.DeleteRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete restore method over HTTP.

            Args:
                request (~.gkebackup.DeleteRestoreRequest):
                    The request object. Request message for DeleteRestore.
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
                _BaseBackupForGKERestTransport._BaseDeleteRestore._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_restore(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseDeleteRestore._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseDeleteRestore._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._DeleteRestore._get_response(
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
            resp = self._interceptor.post_delete_restore(resp)
            return resp

    class _DeleteRestorePlan(
        _BaseBackupForGKERestTransport._BaseDeleteRestorePlan, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.DeleteRestorePlan")

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
            request: gkebackup.DeleteRestorePlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete restore plan method over HTTP.

            Args:
                request (~.gkebackup.DeleteRestorePlanRequest):
                    The request object. Request message for
                DeleteRestorePlan.
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
                _BaseBackupForGKERestTransport._BaseDeleteRestorePlan._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_restore_plan(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseDeleteRestorePlan._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseDeleteRestorePlan._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._DeleteRestorePlan._get_response(
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
            resp = self._interceptor.post_delete_restore_plan(resp)
            return resp

    class _GetBackup(
        _BaseBackupForGKERestTransport._BaseGetBackup, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetBackup")

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
            request: gkebackup.GetBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup.Backup:
            r"""Call the get backup method over HTTP.

            Args:
                request (~.gkebackup.GetBackupRequest):
                    The request object. Request message for GetBackup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup.Backup:
                    Represents a request to perform a
                single point-in-time capture of some
                portion of the state of a GKE cluster,
                the record of the backup operation
                itself, and an anchor for the underlying
                artifacts that comprise the Backup (the
                config backup and VolumeBackups).

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseGetBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_backup(request, metadata)
            transcoded_request = (
                _BaseBackupForGKERestTransport._BaseGetBackup._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseGetBackup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._GetBackup._get_response(
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
            resp = backup.Backup()
            pb_resp = backup.Backup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup(resp)
            return resp

    class _GetBackupIndexDownloadUrl(
        _BaseBackupForGKERestTransport._BaseGetBackupIndexDownloadUrl,
        BackupForGKERestStub,
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetBackupIndexDownloadUrl")

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
            request: gkebackup.GetBackupIndexDownloadUrlRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.GetBackupIndexDownloadUrlResponse:
            r"""Call the get backup index download
            url method over HTTP.

                Args:
                    request (~.gkebackup.GetBackupIndexDownloadUrlRequest):
                        The request object. Request message for
                    GetBackupIndexDownloadUrl.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gkebackup.GetBackupIndexDownloadUrlResponse:
                        Response message for
                    GetBackupIndexDownloadUrl.

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseGetBackupIndexDownloadUrl._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_backup_index_download_url(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseGetBackupIndexDownloadUrl._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseGetBackupIndexDownloadUrl._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                BackupForGKERestTransport._GetBackupIndexDownloadUrl._get_response(
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
            resp = gkebackup.GetBackupIndexDownloadUrlResponse()
            pb_resp = gkebackup.GetBackupIndexDownloadUrlResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup_index_download_url(resp)
            return resp

    class _GetBackupPlan(
        _BaseBackupForGKERestTransport._BaseGetBackupPlan, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetBackupPlan")

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
            request: gkebackup.GetBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup_plan.BackupPlan:
            r"""Call the get backup plan method over HTTP.

            Args:
                request (~.gkebackup.GetBackupPlanRequest):
                    The request object. Request message for GetBackupPlan.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup_plan.BackupPlan:
                    Defines the configuration and
                scheduling for a "line" of Backups.

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseGetBackupPlan._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_backup_plan(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseGetBackupPlan._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseGetBackupPlan._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._GetBackupPlan._get_response(
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
            resp = backup_plan.BackupPlan()
            pb_resp = backup_plan.BackupPlan.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup_plan(resp)
            return resp

    class _GetRestore(
        _BaseBackupForGKERestTransport._BaseGetRestore, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetRestore")

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
            request: gkebackup.GetRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> restore.Restore:
            r"""Call the get restore method over HTTP.

            Args:
                request (~.gkebackup.GetRestoreRequest):
                    The request object. Request message for GetRestore.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.restore.Restore:
                    Represents both a request to Restore
                some portion of a Backup into a target
                GKE cluster and a record of the restore
                operation itself.

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseGetRestore._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_restore(request, metadata)
            transcoded_request = (
                _BaseBackupForGKERestTransport._BaseGetRestore._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseGetRestore._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._GetRestore._get_response(
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
            resp = restore.Restore()
            pb_resp = restore.Restore.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_restore(resp)
            return resp

    class _GetRestorePlan(
        _BaseBackupForGKERestTransport._BaseGetRestorePlan, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetRestorePlan")

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
            request: gkebackup.GetRestorePlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> restore_plan.RestorePlan:
            r"""Call the get restore plan method over HTTP.

            Args:
                request (~.gkebackup.GetRestorePlanRequest):
                    The request object. Request message for GetRestorePlan.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.restore_plan.RestorePlan:
                    The configuration of a potential
                series of Restore operations to be
                performed against Backups belong to a
                particular BackupPlan.

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseGetRestorePlan._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_restore_plan(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseGetRestorePlan._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseGetRestorePlan._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._GetRestorePlan._get_response(
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
            resp = restore_plan.RestorePlan()
            pb_resp = restore_plan.RestorePlan.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_restore_plan(resp)
            return resp

    class _GetVolumeBackup(
        _BaseBackupForGKERestTransport._BaseGetVolumeBackup, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetVolumeBackup")

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
            request: gkebackup.GetVolumeBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume.VolumeBackup:
            r"""Call the get volume backup method over HTTP.

            Args:
                request (~.gkebackup.GetVolumeBackupRequest):
                    The request object. Request message for GetVolumeBackup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume.VolumeBackup:
                    Represents the backup of a specific
                persistent volume as a component of a
                Backup - both the record of the
                operation and a pointer to the
                underlying storage-specific artifacts.

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseGetVolumeBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_volume_backup(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseGetVolumeBackup._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseGetVolumeBackup._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._GetVolumeBackup._get_response(
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
            resp = volume.VolumeBackup()
            pb_resp = volume.VolumeBackup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_volume_backup(resp)
            return resp

    class _GetVolumeRestore(
        _BaseBackupForGKERestTransport._BaseGetVolumeRestore, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetVolumeRestore")

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
            request: gkebackup.GetVolumeRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume.VolumeRestore:
            r"""Call the get volume restore method over HTTP.

            Args:
                request (~.gkebackup.GetVolumeRestoreRequest):
                    The request object. Request message for GetVolumeRestore.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume.VolumeRestore:
                    Represents the operation of restoring
                a volume from a VolumeBackup.

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseGetVolumeRestore._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_volume_restore(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseGetVolumeRestore._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseGetVolumeRestore._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._GetVolumeRestore._get_response(
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
            resp = volume.VolumeRestore()
            pb_resp = volume.VolumeRestore.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_volume_restore(resp)
            return resp

    class _ListBackupPlans(
        _BaseBackupForGKERestTransport._BaseListBackupPlans, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.ListBackupPlans")

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
            request: gkebackup.ListBackupPlansRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListBackupPlansResponse:
            r"""Call the list backup plans method over HTTP.

            Args:
                request (~.gkebackup.ListBackupPlansRequest):
                    The request object. Request message for ListBackupPlans.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListBackupPlansResponse:
                    Response message for ListBackupPlans.
            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseListBackupPlans._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_backup_plans(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseListBackupPlans._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseListBackupPlans._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._ListBackupPlans._get_response(
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
            resp = gkebackup.ListBackupPlansResponse()
            pb_resp = gkebackup.ListBackupPlansResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backup_plans(resp)
            return resp

    class _ListBackups(
        _BaseBackupForGKERestTransport._BaseListBackups, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.ListBackups")

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
            request: gkebackup.ListBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListBackupsResponse:
            r"""Call the list backups method over HTTP.

            Args:
                request (~.gkebackup.ListBackupsRequest):
                    The request object. Request message for ListBackups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListBackupsResponse:
                    Response message for ListBackups.
            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseListBackups._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_backups(request, metadata)
            transcoded_request = (
                _BaseBackupForGKERestTransport._BaseListBackups._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseListBackups._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._ListBackups._get_response(
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
            resp = gkebackup.ListBackupsResponse()
            pb_resp = gkebackup.ListBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backups(resp)
            return resp

    class _ListRestorePlans(
        _BaseBackupForGKERestTransport._BaseListRestorePlans, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.ListRestorePlans")

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
            request: gkebackup.ListRestorePlansRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListRestorePlansResponse:
            r"""Call the list restore plans method over HTTP.

            Args:
                request (~.gkebackup.ListRestorePlansRequest):
                    The request object. Request message for ListRestorePlans.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListRestorePlansResponse:
                    Response message for
                ListRestorePlans.

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseListRestorePlans._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_restore_plans(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseListRestorePlans._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseListRestorePlans._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._ListRestorePlans._get_response(
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
            resp = gkebackup.ListRestorePlansResponse()
            pb_resp = gkebackup.ListRestorePlansResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_restore_plans(resp)
            return resp

    class _ListRestores(
        _BaseBackupForGKERestTransport._BaseListRestores, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.ListRestores")

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
            request: gkebackup.ListRestoresRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListRestoresResponse:
            r"""Call the list restores method over HTTP.

            Args:
                request (~.gkebackup.ListRestoresRequest):
                    The request object. Request message for ListRestores.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListRestoresResponse:
                    Response message for ListRestores.
            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseListRestores._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_restores(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseListRestores._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseListRestores._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._ListRestores._get_response(
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
            resp = gkebackup.ListRestoresResponse()
            pb_resp = gkebackup.ListRestoresResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_restores(resp)
            return resp

    class _ListVolumeBackups(
        _BaseBackupForGKERestTransport._BaseListVolumeBackups, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.ListVolumeBackups")

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
            request: gkebackup.ListVolumeBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListVolumeBackupsResponse:
            r"""Call the list volume backups method over HTTP.

            Args:
                request (~.gkebackup.ListVolumeBackupsRequest):
                    The request object. Request message for
                ListVolumeBackups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListVolumeBackupsResponse:
                    Response message for
                ListVolumeBackups.

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseListVolumeBackups._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_volume_backups(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseListVolumeBackups._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseListVolumeBackups._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._ListVolumeBackups._get_response(
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
            resp = gkebackup.ListVolumeBackupsResponse()
            pb_resp = gkebackup.ListVolumeBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_volume_backups(resp)
            return resp

    class _ListVolumeRestores(
        _BaseBackupForGKERestTransport._BaseListVolumeRestores, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.ListVolumeRestores")

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
            request: gkebackup.ListVolumeRestoresRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListVolumeRestoresResponse:
            r"""Call the list volume restores method over HTTP.

            Args:
                request (~.gkebackup.ListVolumeRestoresRequest):
                    The request object. Request message for
                ListVolumeRestores.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListVolumeRestoresResponse:
                    Response message for
                ListVolumeRestores.

            """

            http_options = (
                _BaseBackupForGKERestTransport._BaseListVolumeRestores._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_volume_restores(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseListVolumeRestores._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseListVolumeRestores._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._ListVolumeRestores._get_response(
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
            resp = gkebackup.ListVolumeRestoresResponse()
            pb_resp = gkebackup.ListVolumeRestoresResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_volume_restores(resp)
            return resp

    class _UpdateBackup(
        _BaseBackupForGKERestTransport._BaseUpdateBackup, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.UpdateBackup")

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
            request: gkebackup.UpdateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup method over HTTP.

            Args:
                request (~.gkebackup.UpdateBackupRequest):
                    The request object. Request message for UpdateBackup.
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
                _BaseBackupForGKERestTransport._BaseUpdateBackup._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_backup(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseUpdateBackup._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseBackupForGKERestTransport._BaseUpdateBackup._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseUpdateBackup._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._UpdateBackup._get_response(
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
            resp = self._interceptor.post_update_backup(resp)
            return resp

    class _UpdateBackupPlan(
        _BaseBackupForGKERestTransport._BaseUpdateBackupPlan, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.UpdateBackupPlan")

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
            request: gkebackup.UpdateBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup plan method over HTTP.

            Args:
                request (~.gkebackup.UpdateBackupPlanRequest):
                    The request object. Request message for UpdateBackupPlan.
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
                _BaseBackupForGKERestTransport._BaseUpdateBackupPlan._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_backup_plan(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseUpdateBackupPlan._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupForGKERestTransport._BaseUpdateBackupPlan._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseUpdateBackupPlan._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._UpdateBackupPlan._get_response(
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
            resp = self._interceptor.post_update_backup_plan(resp)
            return resp

    class _UpdateRestore(
        _BaseBackupForGKERestTransport._BaseUpdateRestore, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.UpdateRestore")

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
            request: gkebackup.UpdateRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update restore method over HTTP.

            Args:
                request (~.gkebackup.UpdateRestoreRequest):
                    The request object. Request message for UpdateRestore.
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
                _BaseBackupForGKERestTransport._BaseUpdateRestore._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_restore(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseUpdateRestore._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupForGKERestTransport._BaseUpdateRestore._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseUpdateRestore._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._UpdateRestore._get_response(
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
            resp = self._interceptor.post_update_restore(resp)
            return resp

    class _UpdateRestorePlan(
        _BaseBackupForGKERestTransport._BaseUpdateRestorePlan, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.UpdateRestorePlan")

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
            request: gkebackup.UpdateRestorePlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update restore plan method over HTTP.

            Args:
                request (~.gkebackup.UpdateRestorePlanRequest):
                    The request object. Request message for
                UpdateRestorePlan.
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
                _BaseBackupForGKERestTransport._BaseUpdateRestorePlan._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_restore_plan(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseUpdateRestorePlan._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupForGKERestTransport._BaseUpdateRestorePlan._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseUpdateRestorePlan._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._UpdateRestorePlan._get_response(
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
            resp = self._interceptor.post_update_restore_plan(resp)
            return resp

    @property
    def create_backup(
        self,
    ) -> Callable[[gkebackup.CreateBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_backup_plan(
        self,
    ) -> Callable[[gkebackup.CreateBackupPlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_restore(
        self,
    ) -> Callable[[gkebackup.CreateRestoreRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_restore_plan(
        self,
    ) -> Callable[[gkebackup.CreateRestorePlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRestorePlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup(
        self,
    ) -> Callable[[gkebackup.DeleteBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup_plan(
        self,
    ) -> Callable[[gkebackup.DeleteBackupPlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_restore(
        self,
    ) -> Callable[[gkebackup.DeleteRestoreRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_restore_plan(
        self,
    ) -> Callable[[gkebackup.DeleteRestorePlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRestorePlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup(self) -> Callable[[gkebackup.GetBackupRequest], backup.Backup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup_index_download_url(
        self,
    ) -> Callable[
        [gkebackup.GetBackupIndexDownloadUrlRequest],
        gkebackup.GetBackupIndexDownloadUrlResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackupIndexDownloadUrl(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup_plan(
        self,
    ) -> Callable[[gkebackup.GetBackupPlanRequest], backup_plan.BackupPlan]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_restore(self) -> Callable[[gkebackup.GetRestoreRequest], restore.Restore]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_restore_plan(
        self,
    ) -> Callable[[gkebackup.GetRestorePlanRequest], restore_plan.RestorePlan]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRestorePlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_volume_backup(
        self,
    ) -> Callable[[gkebackup.GetVolumeBackupRequest], volume.VolumeBackup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVolumeBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_volume_restore(
        self,
    ) -> Callable[[gkebackup.GetVolumeRestoreRequest], volume.VolumeRestore]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVolumeRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backup_plans(
        self,
    ) -> Callable[
        [gkebackup.ListBackupPlansRequest], gkebackup.ListBackupPlansResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackupPlans(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backups(
        self,
    ) -> Callable[[gkebackup.ListBackupsRequest], gkebackup.ListBackupsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_restore_plans(
        self,
    ) -> Callable[
        [gkebackup.ListRestorePlansRequest], gkebackup.ListRestorePlansResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRestorePlans(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_restores(
        self,
    ) -> Callable[[gkebackup.ListRestoresRequest], gkebackup.ListRestoresResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRestores(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_volume_backups(
        self,
    ) -> Callable[
        [gkebackup.ListVolumeBackupsRequest], gkebackup.ListVolumeBackupsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVolumeBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_volume_restores(
        self,
    ) -> Callable[
        [gkebackup.ListVolumeRestoresRequest], gkebackup.ListVolumeRestoresResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVolumeRestores(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup(
        self,
    ) -> Callable[[gkebackup.UpdateBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup_plan(
        self,
    ) -> Callable[[gkebackup.UpdateBackupPlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_restore(
        self,
    ) -> Callable[[gkebackup.UpdateRestoreRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_restore_plan(
        self,
    ) -> Callable[[gkebackup.UpdateRestorePlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRestorePlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseBackupForGKERestTransport._BaseGetLocation, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetLocation")

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
                _BaseBackupForGKERestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseBackupForGKERestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._GetLocation._get_response(
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
        _BaseBackupForGKERestTransport._BaseListLocations, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.ListLocations")

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
                _BaseBackupForGKERestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._ListLocations._get_response(
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
        _BaseBackupForGKERestTransport._BaseGetIamPolicy, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetIamPolicy")

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
                _BaseBackupForGKERestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseGetIamPolicy._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseGetIamPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._GetIamPolicy._get_response(
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
        _BaseBackupForGKERestTransport._BaseSetIamPolicy, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.SetIamPolicy")

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
                _BaseBackupForGKERestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseSetIamPolicy._get_transcoded_request(
                http_options, request
            )

            body = (
                _BaseBackupForGKERestTransport._BaseSetIamPolicy._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseSetIamPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._SetIamPolicy._get_response(
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
        _BaseBackupForGKERestTransport._BaseTestIamPermissions, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.TestIamPermissions")

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
                _BaseBackupForGKERestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupForGKERestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._TestIamPermissions._get_response(
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
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseBackupForGKERestTransport._BaseCancelOperation, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.CancelOperation")

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
                _BaseBackupForGKERestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseBackupForGKERestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._CancelOperation._get_response(
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
        _BaseBackupForGKERestTransport._BaseDeleteOperation, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.DeleteOperation")

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
                _BaseBackupForGKERestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseBackupForGKERestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._DeleteOperation._get_response(
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
        _BaseBackupForGKERestTransport._BaseGetOperation, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.GetOperation")

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
                _BaseBackupForGKERestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseBackupForGKERestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = BackupForGKERestTransport._GetOperation._get_response(
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
        _BaseBackupForGKERestTransport._BaseListOperations, BackupForGKERestStub
    ):
        def __hash__(self):
            return hash("BackupForGKERestTransport.ListOperations")

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
                _BaseBackupForGKERestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseBackupForGKERestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseBackupForGKERestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = BackupForGKERestTransport._ListOperations._get_response(
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


__all__ = ("BackupForGKERestTransport",)
