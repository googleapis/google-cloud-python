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

from google import auth  #  type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.firestore_admin_v1.types import field
from google.cloud.firestore_admin_v1.types import firestore_admin
from google.cloud.firestore_admin_v1.types import index
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


class FirestoreAdminTransport(abc.ABC):
    """Abstract transport class for FirestoreAdmin."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/datastore",
    )

    def __init__(
        self,
        *,
        host: str = "firestore.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
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
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes
            )
        elif credentials is None:
            credentials, _ = auth.default(scopes=scopes)

        # Save the credentials.
        self._credentials = credentials

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_index(
        self,
    ) -> typing.Callable[
        [firestore_admin.CreateIndexRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_indexes(
        self,
    ) -> typing.Callable[
        [firestore_admin.ListIndexesRequest],
        typing.Union[
            firestore_admin.ListIndexesResponse,
            typing.Awaitable[firestore_admin.ListIndexesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_index(
        self,
    ) -> typing.Callable[
        [firestore_admin.GetIndexRequest],
        typing.Union[index.Index, typing.Awaitable[index.Index]],
    ]:
        raise NotImplementedError()

    @property
    def delete_index(
        self,
    ) -> typing.Callable[
        [firestore_admin.DeleteIndexRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_field(
        self,
    ) -> typing.Callable[
        [firestore_admin.GetFieldRequest],
        typing.Union[field.Field, typing.Awaitable[field.Field]],
    ]:
        raise NotImplementedError()

    @property
    def update_field(
        self,
    ) -> typing.Callable[
        [firestore_admin.UpdateFieldRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_fields(
        self,
    ) -> typing.Callable[
        [firestore_admin.ListFieldsRequest],
        typing.Union[
            firestore_admin.ListFieldsResponse,
            typing.Awaitable[firestore_admin.ListFieldsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def export_documents(
        self,
    ) -> typing.Callable[
        [firestore_admin.ExportDocumentsRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def import_documents(
        self,
    ) -> typing.Callable[
        [firestore_admin.ImportDocumentsRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("FirestoreAdminTransport",)
