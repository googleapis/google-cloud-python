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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import packaging.version
import pkg_resources

import google.auth  # type: ignore
import google.api_core  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.area120.tables_v1alpha1.types import tables
from google.protobuf import empty_pb2  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-area120-tables",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()

try:
    # google.auth.__version__ was added in 1.26.0
    _GOOGLE_AUTH_VERSION = google.auth.__version__
except AttributeError:
    try:  # try pkg_resources if it is available
        _GOOGLE_AUTH_VERSION = pkg_resources.get_distribution("google-auth").version
    except pkg_resources.DistributionNotFound:  # pragma: NO COVER
        _GOOGLE_AUTH_VERSION = None


class TablesServiceTransport(abc.ABC):
    """Abstract transport class for TablesService."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/tables",
    )

    DEFAULT_HOST: str = "area120tables.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        **kwargs,
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
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        scopes_kwargs = self._get_scopes_kwargs(self._host, scopes)

        # Save the scopes.
        self._scopes = scopes

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )

        # If the credentials is service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

    # TODO(busunkim): This method is in the base transport
    # to avoid duplicating code across the transport classes. These functions
    # should be deleted once the minimum required versions of google-auth is increased.

    # TODO: Remove this function once google-auth >= 1.25.0 is required
    @classmethod
    def _get_scopes_kwargs(
        cls, host: str, scopes: Optional[Sequence[str]]
    ) -> Dict[str, Optional[Sequence[str]]]:
        """Returns scopes kwargs to pass to google-auth methods depending on the google-auth version"""

        scopes_kwargs = {}

        if _GOOGLE_AUTH_VERSION and (
            packaging.version.parse(_GOOGLE_AUTH_VERSION)
            >= packaging.version.parse("1.25.0")
        ):
            scopes_kwargs = {"scopes": scopes, "default_scopes": cls.AUTH_SCOPES}
        else:
            scopes_kwargs = {"scopes": scopes or cls.AUTH_SCOPES}

        return scopes_kwargs

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.get_table: gapic_v1.method.wrap_method(
                self.get_table, default_timeout=60.0, client_info=client_info,
            ),
            self.list_tables: gapic_v1.method.wrap_method(
                self.list_tables, default_timeout=60.0, client_info=client_info,
            ),
            self.get_workspace: gapic_v1.method.wrap_method(
                self.get_workspace, default_timeout=60.0, client_info=client_info,
            ),
            self.list_workspaces: gapic_v1.method.wrap_method(
                self.list_workspaces, default_timeout=60.0, client_info=client_info,
            ),
            self.get_row: gapic_v1.method.wrap_method(
                self.get_row, default_timeout=60.0, client_info=client_info,
            ),
            self.list_rows: gapic_v1.method.wrap_method(
                self.list_rows, default_timeout=60.0, client_info=client_info,
            ),
            self.create_row: gapic_v1.method.wrap_method(
                self.create_row, default_timeout=60.0, client_info=client_info,
            ),
            self.batch_create_rows: gapic_v1.method.wrap_method(
                self.batch_create_rows, default_timeout=60.0, client_info=client_info,
            ),
            self.update_row: gapic_v1.method.wrap_method(
                self.update_row, default_timeout=60.0, client_info=client_info,
            ),
            self.batch_update_rows: gapic_v1.method.wrap_method(
                self.batch_update_rows, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_row: gapic_v1.method.wrap_method(
                self.delete_row, default_timeout=60.0, client_info=client_info,
            ),
            self.batch_delete_rows: gapic_v1.method.wrap_method(
                self.batch_delete_rows, default_timeout=60.0, client_info=client_info,
            ),
        }

    @property
    def get_table(
        self,
    ) -> Callable[
        [tables.GetTableRequest], Union[tables.Table, Awaitable[tables.Table]]
    ]:
        raise NotImplementedError()

    @property
    def list_tables(
        self,
    ) -> Callable[
        [tables.ListTablesRequest],
        Union[tables.ListTablesResponse, Awaitable[tables.ListTablesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_workspace(
        self,
    ) -> Callable[
        [tables.GetWorkspaceRequest],
        Union[tables.Workspace, Awaitable[tables.Workspace]],
    ]:
        raise NotImplementedError()

    @property
    def list_workspaces(
        self,
    ) -> Callable[
        [tables.ListWorkspacesRequest],
        Union[tables.ListWorkspacesResponse, Awaitable[tables.ListWorkspacesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_row(
        self,
    ) -> Callable[[tables.GetRowRequest], Union[tables.Row, Awaitable[tables.Row]]]:
        raise NotImplementedError()

    @property
    def list_rows(
        self,
    ) -> Callable[
        [tables.ListRowsRequest],
        Union[tables.ListRowsResponse, Awaitable[tables.ListRowsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def create_row(
        self,
    ) -> Callable[[tables.CreateRowRequest], Union[tables.Row, Awaitable[tables.Row]]]:
        raise NotImplementedError()

    @property
    def batch_create_rows(
        self,
    ) -> Callable[
        [tables.BatchCreateRowsRequest],
        Union[
            tables.BatchCreateRowsResponse, Awaitable[tables.BatchCreateRowsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_row(
        self,
    ) -> Callable[[tables.UpdateRowRequest], Union[tables.Row, Awaitable[tables.Row]]]:
        raise NotImplementedError()

    @property
    def batch_update_rows(
        self,
    ) -> Callable[
        [tables.BatchUpdateRowsRequest],
        Union[
            tables.BatchUpdateRowsResponse, Awaitable[tables.BatchUpdateRowsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_row(
        self,
    ) -> Callable[
        [tables.DeleteRowRequest], Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]]
    ]:
        raise NotImplementedError()

    @property
    def batch_delete_rows(
        self,
    ) -> Callable[
        [tables.BatchDeleteRowsRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()


__all__ = ("TablesServiceTransport",)
