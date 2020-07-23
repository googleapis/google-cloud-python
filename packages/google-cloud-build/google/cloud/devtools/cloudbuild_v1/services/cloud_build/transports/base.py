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

from google import auth
from google.api_core import exceptions  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.devtools.cloudbuild_v1.types import cloudbuild
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


class CloudBuildTransport(abc.ABC):
    """Abstract transport class for CloudBuild."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "cloudbuild.googleapis.com",
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
    def create_build(
        self,
    ) -> typing.Callable[
        [cloudbuild.CreateBuildRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_build(
        self,
    ) -> typing.Callable[
        [cloudbuild.GetBuildRequest],
        typing.Union[cloudbuild.Build, typing.Awaitable[cloudbuild.Build]],
    ]:
        raise NotImplementedError()

    @property
    def list_builds(
        self,
    ) -> typing.Callable[
        [cloudbuild.ListBuildsRequest],
        typing.Union[
            cloudbuild.ListBuildsResponse,
            typing.Awaitable[cloudbuild.ListBuildsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def cancel_build(
        self,
    ) -> typing.Callable[
        [cloudbuild.CancelBuildRequest],
        typing.Union[cloudbuild.Build, typing.Awaitable[cloudbuild.Build]],
    ]:
        raise NotImplementedError()

    @property
    def retry_build(
        self,
    ) -> typing.Callable[
        [cloudbuild.RetryBuildRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_build_trigger(
        self,
    ) -> typing.Callable[
        [cloudbuild.CreateBuildTriggerRequest],
        typing.Union[
            cloudbuild.BuildTrigger, typing.Awaitable[cloudbuild.BuildTrigger]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_build_trigger(
        self,
    ) -> typing.Callable[
        [cloudbuild.GetBuildTriggerRequest],
        typing.Union[
            cloudbuild.BuildTrigger, typing.Awaitable[cloudbuild.BuildTrigger]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_build_triggers(
        self,
    ) -> typing.Callable[
        [cloudbuild.ListBuildTriggersRequest],
        typing.Union[
            cloudbuild.ListBuildTriggersResponse,
            typing.Awaitable[cloudbuild.ListBuildTriggersResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_build_trigger(
        self,
    ) -> typing.Callable[
        [cloudbuild.DeleteBuildTriggerRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_build_trigger(
        self,
    ) -> typing.Callable[
        [cloudbuild.UpdateBuildTriggerRequest],
        typing.Union[
            cloudbuild.BuildTrigger, typing.Awaitable[cloudbuild.BuildTrigger]
        ],
    ]:
        raise NotImplementedError()

    @property
    def run_build_trigger(
        self,
    ) -> typing.Callable[
        [cloudbuild.RunBuildTriggerRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_worker_pool(
        self,
    ) -> typing.Callable[
        [cloudbuild.CreateWorkerPoolRequest],
        typing.Union[cloudbuild.WorkerPool, typing.Awaitable[cloudbuild.WorkerPool]],
    ]:
        raise NotImplementedError()

    @property
    def get_worker_pool(
        self,
    ) -> typing.Callable[
        [cloudbuild.GetWorkerPoolRequest],
        typing.Union[cloudbuild.WorkerPool, typing.Awaitable[cloudbuild.WorkerPool]],
    ]:
        raise NotImplementedError()

    @property
    def delete_worker_pool(
        self,
    ) -> typing.Callable[
        [cloudbuild.DeleteWorkerPoolRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_worker_pool(
        self,
    ) -> typing.Callable[
        [cloudbuild.UpdateWorkerPoolRequest],
        typing.Union[cloudbuild.WorkerPool, typing.Awaitable[cloudbuild.WorkerPool]],
    ]:
        raise NotImplementedError()

    @property
    def list_worker_pools(
        self,
    ) -> typing.Callable[
        [cloudbuild.ListWorkerPoolsRequest],
        typing.Union[
            cloudbuild.ListWorkerPoolsResponse,
            typing.Awaitable[cloudbuild.ListWorkerPoolsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("CloudBuildTransport",)
