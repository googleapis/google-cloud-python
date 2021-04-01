# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.bigtable_admin_v2.types import bigtable_table_admin
from google.cloud.bigtable_admin_v2.types import table
from google.cloud.bigtable_admin_v2.types import table as gba_table
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigtable-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class BigtableTableAdminTransport(abc.ABC):
    """Abstract transport class for BigtableTableAdmin."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/bigtable.admin",
        "https://www.googleapis.com/auth/bigtable.admin.table",
        "https://www.googleapis.com/auth/cloud-bigtable.admin",
        "https://www.googleapis.com/auth/cloud-bigtable.admin.table",
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
    )

    def __init__(
        self,
        *,
        host: str = "bigtableadmin.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=self._scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=self._scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_table: gapic_v1.method.wrap_method(
                self.create_table, default_timeout=300.0, client_info=client_info,
            ),
            self.create_table_from_snapshot: gapic_v1.method.wrap_method(
                self.create_table_from_snapshot,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_tables: gapic_v1.method.wrap_method(
                self.list_tables,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_table: gapic_v1.method.wrap_method(
                self.get_table,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_table: gapic_v1.method.wrap_method(
                self.delete_table, default_timeout=60.0, client_info=client_info,
            ),
            self.modify_column_families: gapic_v1.method.wrap_method(
                self.modify_column_families,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.drop_row_range: gapic_v1.method.wrap_method(
                self.drop_row_range, default_timeout=3600.0, client_info=client_info,
            ),
            self.generate_consistency_token: gapic_v1.method.wrap_method(
                self.generate_consistency_token,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.check_consistency: gapic_v1.method.wrap_method(
                self.check_consistency,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.snapshot_table: gapic_v1.method.wrap_method(
                self.snapshot_table, default_timeout=None, client_info=client_info,
            ),
            self.get_snapshot: gapic_v1.method.wrap_method(
                self.get_snapshot,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_snapshots: gapic_v1.method.wrap_method(
                self.list_snapshots,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_snapshot: gapic_v1.method.wrap_method(
                self.delete_snapshot, default_timeout=60.0, client_info=client_info,
            ),
            self.create_backup: gapic_v1.method.wrap_method(
                self.create_backup, default_timeout=60.0, client_info=client_info,
            ),
            self.get_backup: gapic_v1.method.wrap_method(
                self.get_backup,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_backup: gapic_v1.method.wrap_method(
                self.update_backup, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_backup: gapic_v1.method.wrap_method(
                self.delete_backup, default_timeout=60.0, client_info=client_info,
            ),
            self.list_backups: gapic_v1.method.wrap_method(
                self.list_backups,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.restore_table: gapic_v1.method.wrap_method(
                self.restore_table, default_timeout=60.0, client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=60.0, client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_table(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.CreateTableRequest],
        typing.Union[gba_table.Table, typing.Awaitable[gba_table.Table]],
    ]:
        raise NotImplementedError()

    @property
    def create_table_from_snapshot(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.CreateTableFromSnapshotRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_tables(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.ListTablesRequest],
        typing.Union[
            bigtable_table_admin.ListTablesResponse,
            typing.Awaitable[bigtable_table_admin.ListTablesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_table(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.GetTableRequest],
        typing.Union[table.Table, typing.Awaitable[table.Table]],
    ]:
        raise NotImplementedError()

    @property
    def delete_table(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.DeleteTableRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def modify_column_families(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.ModifyColumnFamiliesRequest],
        typing.Union[table.Table, typing.Awaitable[table.Table]],
    ]:
        raise NotImplementedError()

    @property
    def drop_row_range(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.DropRowRangeRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def generate_consistency_token(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.GenerateConsistencyTokenRequest],
        typing.Union[
            bigtable_table_admin.GenerateConsistencyTokenResponse,
            typing.Awaitable[bigtable_table_admin.GenerateConsistencyTokenResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def check_consistency(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.CheckConsistencyRequest],
        typing.Union[
            bigtable_table_admin.CheckConsistencyResponse,
            typing.Awaitable[bigtable_table_admin.CheckConsistencyResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def snapshot_table(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.SnapshotTableRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_snapshot(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.GetSnapshotRequest],
        typing.Union[table.Snapshot, typing.Awaitable[table.Snapshot]],
    ]:
        raise NotImplementedError()

    @property
    def list_snapshots(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.ListSnapshotsRequest],
        typing.Union[
            bigtable_table_admin.ListSnapshotsResponse,
            typing.Awaitable[bigtable_table_admin.ListSnapshotsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_snapshot(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.DeleteSnapshotRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_backup(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.CreateBackupRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_backup(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.GetBackupRequest],
        typing.Union[table.Backup, typing.Awaitable[table.Backup]],
    ]:
        raise NotImplementedError()

    @property
    def update_backup(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.UpdateBackupRequest],
        typing.Union[table.Backup, typing.Awaitable[table.Backup]],
    ]:
        raise NotImplementedError()

    @property
    def delete_backup(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.DeleteBackupRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_backups(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.ListBackupsRequest],
        typing.Union[
            bigtable_table_admin.ListBackupsResponse,
            typing.Awaitable[bigtable_table_admin.ListBackupsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def restore_table(
        self,
    ) -> typing.Callable[
        [bigtable_table_admin.RestoreTableRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.GetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.SetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> typing.Callable[
        [iam_policy.TestIamPermissionsRequest],
        typing.Union[
            iam_policy.TestIamPermissionsResponse,
            typing.Awaitable[iam_policy.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("BigtableTableAdminTransport",)
