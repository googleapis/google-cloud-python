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
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from google.api_core import operations_v1
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.cloud.bigtable_admin_v2.types import bigtable_table_admin
from google.cloud.bigtable_admin_v2.types import table
from google.cloud.bigtable_admin_v2.types import table as gba_table
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore

from .base import (
    BigtableTableAdminTransport,
    DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO,
)


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class BigtableTableAdminRestInterceptor:
    """Interceptor for BigtableTableAdmin.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BigtableTableAdminRestTransport.

    .. code-block:: python
        class MyCustomBigtableTableAdminInterceptor(BigtableTableAdminRestInterceptor):
            def pre_check_consistency(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_check_consistency(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_copy_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_copy_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_table_from_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_table_from_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_drop_row_range(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_generate_consistency_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_consistency_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_backups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_snapshots(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_snapshots(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_tables(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_tables(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_modify_column_families(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_modify_column_families(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restore_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restore_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_snapshot_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_snapshot_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_table(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_backup(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_table(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_table(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = BigtableTableAdminRestTransport(interceptor=MyCustomBigtableTableAdminInterceptor())
        client = BigtableTableAdminClient(transport=transport)


    """

    def pre_check_consistency(
        self,
        request: bigtable_table_admin.CheckConsistencyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.CheckConsistencyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for check_consistency

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_check_consistency(
        self, response: bigtable_table_admin.CheckConsistencyResponse
    ) -> bigtable_table_admin.CheckConsistencyResponse:
        """Post-rpc interceptor for check_consistency

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_copy_backup(
        self,
        request: bigtable_table_admin.CopyBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.CopyBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for copy_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_copy_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for copy_backup

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_create_backup(
        self,
        request: bigtable_table_admin.CreateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.CreateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_create_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_create_table(
        self,
        request: bigtable_table_admin.CreateTableRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.CreateTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_create_table(self, response: gba_table.Table) -> gba_table.Table:
        """Post-rpc interceptor for create_table

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_create_table_from_snapshot(
        self,
        request: bigtable_table_admin.CreateTableFromSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_table_admin.CreateTableFromSnapshotRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_table_from_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_create_table_from_snapshot(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_table_from_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup(
        self,
        request: bigtable_table_admin.DeleteBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.DeleteBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def pre_delete_snapshot(
        self,
        request: bigtable_table_admin.DeleteSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.DeleteSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def pre_delete_table(
        self,
        request: bigtable_table_admin.DeleteTableRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.DeleteTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def pre_drop_row_range(
        self,
        request: bigtable_table_admin.DropRowRangeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.DropRowRangeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for drop_row_range

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def pre_generate_consistency_token(
        self,
        request: bigtable_table_admin.GenerateConsistencyTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_table_admin.GenerateConsistencyTokenRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for generate_consistency_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_generate_consistency_token(
        self, response: bigtable_table_admin.GenerateConsistencyTokenResponse
    ) -> bigtable_table_admin.GenerateConsistencyTokenResponse:
        """Post-rpc interceptor for generate_consistency_token

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup(
        self,
        request: bigtable_table_admin.GetBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.GetBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_get_backup(self, response: table.Backup) -> table.Backup:
        """Post-rpc interceptor for get_backup

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
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
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_get_snapshot(
        self,
        request: bigtable_table_admin.GetSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.GetSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_get_snapshot(self, response: table.Snapshot) -> table.Snapshot:
        """Post-rpc interceptor for get_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_get_table(
        self,
        request: bigtable_table_admin.GetTableRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.GetTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_get_table(self, response: table.Table) -> table.Table:
        """Post-rpc interceptor for get_table

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_list_backups(
        self,
        request: bigtable_table_admin.ListBackupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.ListBackupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_list_backups(
        self, response: bigtable_table_admin.ListBackupsResponse
    ) -> bigtable_table_admin.ListBackupsResponse:
        """Post-rpc interceptor for list_backups

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_list_snapshots(
        self,
        request: bigtable_table_admin.ListSnapshotsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.ListSnapshotsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_snapshots

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_list_snapshots(
        self, response: bigtable_table_admin.ListSnapshotsResponse
    ) -> bigtable_table_admin.ListSnapshotsResponse:
        """Post-rpc interceptor for list_snapshots

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_list_tables(
        self,
        request: bigtable_table_admin.ListTablesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.ListTablesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_tables

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_list_tables(
        self, response: bigtable_table_admin.ListTablesResponse
    ) -> bigtable_table_admin.ListTablesResponse:
        """Post-rpc interceptor for list_tables

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_modify_column_families(
        self,
        request: bigtable_table_admin.ModifyColumnFamiliesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        bigtable_table_admin.ModifyColumnFamiliesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for modify_column_families

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_modify_column_families(self, response: table.Table) -> table.Table:
        """Post-rpc interceptor for modify_column_families

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_restore_table(
        self,
        request: bigtable_table_admin.RestoreTableRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.RestoreTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for restore_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_restore_table(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for restore_table

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
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
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_snapshot_table(
        self,
        request: bigtable_table_admin.SnapshotTableRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.SnapshotTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for snapshot_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_snapshot_table(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for snapshot_table

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
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
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_undelete_table(
        self,
        request: bigtable_table_admin.UndeleteTableRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.UndeleteTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undelete_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_undelete_table(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undelete_table

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup(
        self,
        request: bigtable_table_admin.UpdateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.UpdateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_update_backup(self, response: table.Backup) -> table.Backup:
        """Post-rpc interceptor for update_backup

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response

    def pre_update_table(
        self,
        request: bigtable_table_admin.UpdateTableRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[bigtable_table_admin.UpdateTableRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_table

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BigtableTableAdmin server.
        """
        return request, metadata

    def post_update_table(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_table

        Override in a subclass to manipulate the response
        after it is returned by the BigtableTableAdmin server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BigtableTableAdminRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BigtableTableAdminRestInterceptor


class BigtableTableAdminRestTransport(BigtableTableAdminTransport):
    """REST backend transport for BigtableTableAdmin.

    Service for creating, configuring, and deleting Cloud
    Bigtable tables.

    Provides access to the table schemas only, not the data stored
    within the tables.

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
        interceptor: Optional[BigtableTableAdminRestInterceptor] = None,
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
        self._interceptor = interceptor or BigtableTableAdminRestInterceptor()
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

    class _CheckConsistency(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("CheckConsistency")

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
            request: bigtable_table_admin.CheckConsistencyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable_table_admin.CheckConsistencyResponse:
            r"""Call the check consistency method over HTTP.

            Args:
                request (~.bigtable_table_admin.CheckConsistencyRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency][google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable_table_admin.CheckConsistencyResponse:
                    Response message for
                [google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency][google.bigtable.admin.v2.BigtableTableAdmin.CheckConsistency]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/instances/*/tables/*}:checkConsistency",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_check_consistency(
                request, metadata
            )
            pb_request = bigtable_table_admin.CheckConsistencyRequest.pb(request)
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
            resp = bigtable_table_admin.CheckConsistencyResponse()
            pb_resp = bigtable_table_admin.CheckConsistencyResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_check_consistency(resp)
            return resp

    class _CopyBackup(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("CopyBackup")

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
            request: bigtable_table_admin.CopyBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the copy backup method over HTTP.

            Args:
                request (~.bigtable_table_admin.CopyBackupRequest):
                    The request object. The request for
                [CopyBackup][google.bigtable.admin.v2.BigtableTableAdmin.CopyBackup].
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
                    "uri": "/v2/{parent=projects/*/instances/*/clusters/*}/backups:copy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_copy_backup(request, metadata)
            pb_request = bigtable_table_admin.CopyBackupRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_copy_backup(resp)
            return resp

    class _CreateBackup(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("CreateBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "backupId": "",
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
            request: bigtable_table_admin.CreateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup method over HTTP.

            Args:
                request (~.bigtable_table_admin.CreateBackupRequest):
                    The request object. The request for
                [CreateBackup][google.bigtable.admin.v2.BigtableTableAdmin.CreateBackup].
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
                    "uri": "/v2/{parent=projects/*/instances/*/clusters/*}/backups",
                    "body": "backup",
                },
            ]
            request, metadata = self._interceptor.pre_create_backup(request, metadata)
            pb_request = bigtable_table_admin.CreateBackupRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_backup(resp)
            return resp

    class _CreateTable(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("CreateTable")

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
            request: bigtable_table_admin.CreateTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gba_table.Table:
            r"""Call the create table method over HTTP.

            Args:
                request (~.bigtable_table_admin.CreateTableRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.CreateTable][google.bigtable.admin.v2.BigtableTableAdmin.CreateTable]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gba_table.Table:
                    A collection of user data indexed by
                row, column, and timestamp. Each table
                is served using the resources of its
                parent cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/instances/*}/tables",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_create_table(request, metadata)
            pb_request = bigtable_table_admin.CreateTableRequest.pb(request)
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
            resp = gba_table.Table()
            pb_resp = gba_table.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_table(resp)
            return resp

    class _CreateTableFromSnapshot(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("CreateTableFromSnapshot")

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
            request: bigtable_table_admin.CreateTableFromSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create table from
            snapshot method over HTTP.

                Args:
                    request (~.bigtable_table_admin.CreateTableFromSnapshotRequest):
                        The request object. Request message for
                    [google.bigtable.admin.v2.BigtableTableAdmin.CreateTableFromSnapshot][google.bigtable.admin.v2.BigtableTableAdmin.CreateTableFromSnapshot]

                    Note: This is a private alpha release of Cloud Bigtable
                    snapshots. This feature is not currently available to
                    most Cloud Bigtable customers. This feature might be
                    changed in backward-incompatible ways and is not
                    recommended for production use. It is not subject to any
                    SLA or deprecation policy.
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
                    "uri": "/v2/{parent=projects/*/instances/*}/tables:createFromSnapshot",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_create_table_from_snapshot(
                request, metadata
            )
            pb_request = bigtable_table_admin.CreateTableFromSnapshotRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_table_from_snapshot(resp)
            return resp

    class _DeleteBackup(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("DeleteBackup")

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
            request: bigtable_table_admin.DeleteBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete backup method over HTTP.

            Args:
                request (~.bigtable_table_admin.DeleteBackupRequest):
                    The request object. The request for
                [DeleteBackup][google.bigtable.admin.v2.BigtableTableAdmin.DeleteBackup].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/instances/*/clusters/*/backups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_backup(request, metadata)
            pb_request = bigtable_table_admin.DeleteBackupRequest.pb(request)
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

    class _DeleteSnapshot(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("DeleteSnapshot")

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
            request: bigtable_table_admin.DeleteSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete snapshot method over HTTP.

            Args:
                request (~.bigtable_table_admin.DeleteSnapshotRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.DeleteSnapshot][google.bigtable.admin.v2.BigtableTableAdmin.DeleteSnapshot]

                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/instances/*/clusters/*/snapshots/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_snapshot(request, metadata)
            pb_request = bigtable_table_admin.DeleteSnapshotRequest.pb(request)
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

    class _DeleteTable(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("DeleteTable")

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
            request: bigtable_table_admin.DeleteTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete table method over HTTP.

            Args:
                request (~.bigtable_table_admin.DeleteTableRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.DeleteTable][google.bigtable.admin.v2.BigtableTableAdmin.DeleteTable]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/instances/*/tables/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_table(request, metadata)
            pb_request = bigtable_table_admin.DeleteTableRequest.pb(request)
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

    class _DropRowRange(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("DropRowRange")

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
            request: bigtable_table_admin.DropRowRangeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the drop row range method over HTTP.

            Args:
                request (~.bigtable_table_admin.DropRowRangeRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.DropRowRange][google.bigtable.admin.v2.BigtableTableAdmin.DropRowRange]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/instances/*/tables/*}:dropRowRange",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_drop_row_range(request, metadata)
            pb_request = bigtable_table_admin.DropRowRangeRequest.pb(request)
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

    class _GenerateConsistencyToken(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("GenerateConsistencyToken")

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
            request: bigtable_table_admin.GenerateConsistencyTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable_table_admin.GenerateConsistencyTokenResponse:
            r"""Call the generate consistency
            token method over HTTP.

                Args:
                    request (~.bigtable_table_admin.GenerateConsistencyTokenRequest):
                        The request object. Request message for
                    [google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken][google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken]
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.bigtable_table_admin.GenerateConsistencyTokenResponse:
                        Response message for
                    [google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken][google.bigtable.admin.v2.BigtableTableAdmin.GenerateConsistencyToken]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/instances/*/tables/*}:generateConsistencyToken",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_generate_consistency_token(
                request, metadata
            )
            pb_request = bigtable_table_admin.GenerateConsistencyTokenRequest.pb(
                request
            )
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
            resp = bigtable_table_admin.GenerateConsistencyTokenResponse()
            pb_resp = bigtable_table_admin.GenerateConsistencyTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_consistency_token(resp)
            return resp

    class _GetBackup(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("GetBackup")

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
            request: bigtable_table_admin.GetBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> table.Backup:
            r"""Call the get backup method over HTTP.

            Args:
                request (~.bigtable_table_admin.GetBackupRequest):
                    The request object. The request for
                [GetBackup][google.bigtable.admin.v2.BigtableTableAdmin.GetBackup].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.table.Backup:
                    A backup of a Cloud Bigtable table.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/instances/*/clusters/*/backups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_backup(request, metadata)
            pb_request = bigtable_table_admin.GetBackupRequest.pb(request)
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
            resp = table.Backup()
            pb_resp = table.Backup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup(resp)
            return resp

    class _GetIamPolicy(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("GetIamPolicy")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{resource=projects/*/instances/*/tables/*}:getIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{resource=projects/*/instances/*/clusters/*/backups/*}:getIamPolicy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            pb_request = request
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _GetSnapshot(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("GetSnapshot")

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
            request: bigtable_table_admin.GetSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> table.Snapshot:
            r"""Call the get snapshot method over HTTP.

            Args:
                request (~.bigtable_table_admin.GetSnapshotRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.GetSnapshot][google.bigtable.admin.v2.BigtableTableAdmin.GetSnapshot]

                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.table.Snapshot:
                    A snapshot of a table at a particular
                time. A snapshot can be used as a
                checkpoint for data restoration or a
                data source for a new table.

                Note: This is a private alpha release of
                Cloud Bigtable snapshots. This feature
                is not currently available to most Cloud
                Bigtable customers. This feature might
                be changed in backward-incompatible ways
                and is not recommended for production
                use. It is not subject to any SLA or
                deprecation policy.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/instances/*/clusters/*/snapshots/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_snapshot(request, metadata)
            pb_request = bigtable_table_admin.GetSnapshotRequest.pb(request)
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
            resp = table.Snapshot()
            pb_resp = table.Snapshot.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_snapshot(resp)
            return resp

    class _GetTable(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("GetTable")

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
            request: bigtable_table_admin.GetTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> table.Table:
            r"""Call the get table method over HTTP.

            Args:
                request (~.bigtable_table_admin.GetTableRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.GetTable][google.bigtable.admin.v2.BigtableTableAdmin.GetTable]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.table.Table:
                    A collection of user data indexed by
                row, column, and timestamp. Each table
                is served using the resources of its
                parent cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/instances/*/tables/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_table(request, metadata)
            pb_request = bigtable_table_admin.GetTableRequest.pb(request)
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
            resp = table.Table()
            pb_resp = table.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_table(resp)
            return resp

    class _ListBackups(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("ListBackups")

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
            request: bigtable_table_admin.ListBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable_table_admin.ListBackupsResponse:
            r"""Call the list backups method over HTTP.

            Args:
                request (~.bigtable_table_admin.ListBackupsRequest):
                    The request object. The request for
                [ListBackups][google.bigtable.admin.v2.BigtableTableAdmin.ListBackups].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable_table_admin.ListBackupsResponse:
                    The response for
                [ListBackups][google.bigtable.admin.v2.BigtableTableAdmin.ListBackups].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/instances/*/clusters/*}/backups",
                },
            ]
            request, metadata = self._interceptor.pre_list_backups(request, metadata)
            pb_request = bigtable_table_admin.ListBackupsRequest.pb(request)
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
            resp = bigtable_table_admin.ListBackupsResponse()
            pb_resp = bigtable_table_admin.ListBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backups(resp)
            return resp

    class _ListSnapshots(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("ListSnapshots")

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
            request: bigtable_table_admin.ListSnapshotsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable_table_admin.ListSnapshotsResponse:
            r"""Call the list snapshots method over HTTP.

            Args:
                request (~.bigtable_table_admin.ListSnapshotsRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots][google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots]

                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable_table_admin.ListSnapshotsResponse:
                    Response message for
                [google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots][google.bigtable.admin.v2.BigtableTableAdmin.ListSnapshots]

                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/instances/*/clusters/*}/snapshots",
                },
            ]
            request, metadata = self._interceptor.pre_list_snapshots(request, metadata)
            pb_request = bigtable_table_admin.ListSnapshotsRequest.pb(request)
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
            resp = bigtable_table_admin.ListSnapshotsResponse()
            pb_resp = bigtable_table_admin.ListSnapshotsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_snapshots(resp)
            return resp

    class _ListTables(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("ListTables")

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
            request: bigtable_table_admin.ListTablesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigtable_table_admin.ListTablesResponse:
            r"""Call the list tables method over HTTP.

            Args:
                request (~.bigtable_table_admin.ListTablesRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.ListTables][google.bigtable.admin.v2.BigtableTableAdmin.ListTables]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigtable_table_admin.ListTablesResponse:
                    Response message for
                [google.bigtable.admin.v2.BigtableTableAdmin.ListTables][google.bigtable.admin.v2.BigtableTableAdmin.ListTables]

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/instances/*}/tables",
                },
            ]
            request, metadata = self._interceptor.pre_list_tables(request, metadata)
            pb_request = bigtable_table_admin.ListTablesRequest.pb(request)
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
            resp = bigtable_table_admin.ListTablesResponse()
            pb_resp = bigtable_table_admin.ListTablesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_tables(resp)
            return resp

    class _ModifyColumnFamilies(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("ModifyColumnFamilies")

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
            request: bigtable_table_admin.ModifyColumnFamiliesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> table.Table:
            r"""Call the modify column families method over HTTP.

            Args:
                request (~.bigtable_table_admin.ModifyColumnFamiliesRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.ModifyColumnFamilies][google.bigtable.admin.v2.BigtableTableAdmin.ModifyColumnFamilies]
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.table.Table:
                    A collection of user data indexed by
                row, column, and timestamp. Each table
                is served using the resources of its
                parent cluster.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/instances/*/tables/*}:modifyColumnFamilies",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_modify_column_families(
                request, metadata
            )
            pb_request = bigtable_table_admin.ModifyColumnFamiliesRequest.pb(request)
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
            resp = table.Table()
            pb_resp = table.Table.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_modify_column_families(resp)
            return resp

    class _RestoreTable(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("RestoreTable")

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
            request: bigtable_table_admin.RestoreTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restore table method over HTTP.

            Args:
                request (~.bigtable_table_admin.RestoreTableRequest):
                    The request object. The request for
                [RestoreTable][google.bigtable.admin.v2.BigtableTableAdmin.RestoreTable].
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
                    "uri": "/v2/{parent=projects/*/instances/*}/tables:restore",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_restore_table(request, metadata)
            pb_request = bigtable_table_admin.RestoreTableRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_restore_table(resp)
            return resp

    class _SetIamPolicy(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("SetIamPolicy")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{resource=projects/*/instances/*/tables/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{resource=projects/*/instances/*/clusters/*/backups/*}:setIamPolicy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            pb_request = request
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    class _SnapshotTable(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("SnapshotTable")

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
            request: bigtable_table_admin.SnapshotTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the snapshot table method over HTTP.

            Args:
                request (~.bigtable_table_admin.SnapshotTableRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.SnapshotTable][google.bigtable.admin.v2.BigtableTableAdmin.SnapshotTable]

                Note: This is a private alpha release of Cloud Bigtable
                snapshots. This feature is not currently available to
                most Cloud Bigtable customers. This feature might be
                changed in backward-incompatible ways and is not
                recommended for production use. It is not subject to any
                SLA or deprecation policy.
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
                    "uri": "/v2/{name=projects/*/instances/*/tables/*}:snapshot",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_snapshot_table(request, metadata)
            pb_request = bigtable_table_admin.SnapshotTableRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_snapshot_table(resp)
            return resp

    class _TestIamPermissions(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("TestIamPermissions")

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{resource=projects/*/instances/*/tables/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{resource=projects/*/instances/*/clusters/*/backups/*}:testIamPermissions",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            pb_request = request
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
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    class _UndeleteTable(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("UndeleteTable")

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
            request: bigtable_table_admin.UndeleteTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undelete table method over HTTP.

            Args:
                request (~.bigtable_table_admin.UndeleteTableRequest):
                    The request object. Request message for
                [google.bigtable.admin.v2.BigtableTableAdmin.UndeleteTable][google.bigtable.admin.v2.BigtableTableAdmin.UndeleteTable]
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
                    "uri": "/v2/{name=projects/*/instances/*/tables/*}:undelete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_undelete_table(request, metadata)
            pb_request = bigtable_table_admin.UndeleteTableRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_undelete_table(resp)
            return resp

    class _UpdateBackup(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("UpdateBackup")

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
            request: bigtable_table_admin.UpdateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> table.Backup:
            r"""Call the update backup method over HTTP.

            Args:
                request (~.bigtable_table_admin.UpdateBackupRequest):
                    The request object. The request for
                [UpdateBackup][google.bigtable.admin.v2.BigtableTableAdmin.UpdateBackup].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.table.Backup:
                    A backup of a Cloud Bigtable table.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{backup.name=projects/*/instances/*/clusters/*/backups/*}",
                    "body": "backup",
                },
            ]
            request, metadata = self._interceptor.pre_update_backup(request, metadata)
            pb_request = bigtable_table_admin.UpdateBackupRequest.pb(request)
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
            resp = table.Backup()
            pb_resp = table.Backup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_backup(resp)
            return resp

    class _UpdateTable(BigtableTableAdminRestStub):
        def __hash__(self):
            return hash("UpdateTable")

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
            request: bigtable_table_admin.UpdateTableRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update table method over HTTP.

            Args:
                request (~.bigtable_table_admin.UpdateTableRequest):
                    The request object. The request for
                [UpdateTable][google.bigtable.admin.v2.BigtableTableAdmin.UpdateTable].
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
                    "uri": "/v2/{table.name=projects/*/instances/*/tables/*}",
                    "body": "table",
                },
            ]
            request, metadata = self._interceptor.pre_update_table(request, metadata)
            pb_request = bigtable_table_admin.UpdateTableRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_table(resp)
            return resp

    @property
    def check_consistency(
        self,
    ) -> Callable[
        [bigtable_table_admin.CheckConsistencyRequest],
        bigtable_table_admin.CheckConsistencyResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CheckConsistency(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def copy_backup(
        self,
    ) -> Callable[[bigtable_table_admin.CopyBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CopyBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_backup(
        self,
    ) -> Callable[[bigtable_table_admin.CreateBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_table(
        self,
    ) -> Callable[[bigtable_table_admin.CreateTableRequest], gba_table.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_table_from_snapshot(
        self,
    ) -> Callable[
        [bigtable_table_admin.CreateTableFromSnapshotRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTableFromSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup(
        self,
    ) -> Callable[[bigtable_table_admin.DeleteBackupRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_snapshot(
        self,
    ) -> Callable[[bigtable_table_admin.DeleteSnapshotRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_table(
        self,
    ) -> Callable[[bigtable_table_admin.DeleteTableRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def drop_row_range(
        self,
    ) -> Callable[[bigtable_table_admin.DropRowRangeRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DropRowRange(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_consistency_token(
        self,
    ) -> Callable[
        [bigtable_table_admin.GenerateConsistencyTokenRequest],
        bigtable_table_admin.GenerateConsistencyTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateConsistencyToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup(
        self,
    ) -> Callable[[bigtable_table_admin.GetBackupRequest], table.Backup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_snapshot(
        self,
    ) -> Callable[[bigtable_table_admin.GetSnapshotRequest], table.Snapshot]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_table(
        self,
    ) -> Callable[[bigtable_table_admin.GetTableRequest], table.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backups(
        self,
    ) -> Callable[
        [bigtable_table_admin.ListBackupsRequest],
        bigtable_table_admin.ListBackupsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_snapshots(
        self,
    ) -> Callable[
        [bigtable_table_admin.ListSnapshotsRequest],
        bigtable_table_admin.ListSnapshotsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSnapshots(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_tables(
        self,
    ) -> Callable[
        [bigtable_table_admin.ListTablesRequest],
        bigtable_table_admin.ListTablesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTables(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def modify_column_families(
        self,
    ) -> Callable[[bigtable_table_admin.ModifyColumnFamiliesRequest], table.Table]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ModifyColumnFamilies(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def restore_table(
        self,
    ) -> Callable[[bigtable_table_admin.RestoreTableRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestoreTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def snapshot_table(
        self,
    ) -> Callable[
        [bigtable_table_admin.SnapshotTableRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SnapshotTable(self._session, self._host, self._interceptor)  # type: ignore

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
    def undelete_table(
        self,
    ) -> Callable[
        [bigtable_table_admin.UndeleteTableRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeleteTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup(
        self,
    ) -> Callable[[bigtable_table_admin.UpdateBackupRequest], table.Backup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_table(
        self,
    ) -> Callable[[bigtable_table_admin.UpdateTableRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTable(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("BigtableTableAdminRestTransport",)
