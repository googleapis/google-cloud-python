# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import pkg_resources

import google.auth  # type: ignore
import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.bigtable_v2.types import bigtable

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigtable",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class BigtableTransport(abc.ABC):
    """Abstract transport class for Bigtable."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/bigtable.data",
        "https://www.googleapis.com/auth/bigtable.data.readonly",
        "https://www.googleapis.com/auth/cloud-bigtable.data",
        "https://www.googleapis.com/auth/cloud-bigtable.data.readonly",
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
    )

    DEFAULT_HOST: str = "bigtable.googleapis.com"

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

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

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

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.read_rows: gapic_v1.method.wrap_method(
                self.read_rows,
                default_timeout=43200.0,
                client_info=client_info,
            ),
            self.sample_row_keys: gapic_v1.method.wrap_method(
                self.sample_row_keys,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.mutate_row: gapic_v1.method.wrap_method(
                self.mutate_row,
                default_retry=retries.Retry(
                    initial=0.01,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.mutate_rows: gapic_v1.method.wrap_method(
                self.mutate_rows,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.check_and_mutate_row: gapic_v1.method.wrap_method(
                self.check_and_mutate_row,
                default_timeout=20.0,
                client_info=client_info,
            ),
            self.ping_and_warm: gapic_v1.method.wrap_method(
                self.ping_and_warm,
                default_timeout=None,
                client_info=client_info,
            ),
            self.read_modify_write_row: gapic_v1.method.wrap_method(
                self.read_modify_write_row,
                default_timeout=20.0,
                client_info=client_info,
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def read_rows(
        self,
    ) -> Callable[
        [bigtable.ReadRowsRequest],
        Union[bigtable.ReadRowsResponse, Awaitable[bigtable.ReadRowsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def sample_row_keys(
        self,
    ) -> Callable[
        [bigtable.SampleRowKeysRequest],
        Union[
            bigtable.SampleRowKeysResponse, Awaitable[bigtable.SampleRowKeysResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def mutate_row(
        self,
    ) -> Callable[
        [bigtable.MutateRowRequest],
        Union[bigtable.MutateRowResponse, Awaitable[bigtable.MutateRowResponse]],
    ]:
        raise NotImplementedError()

    @property
    def mutate_rows(
        self,
    ) -> Callable[
        [bigtable.MutateRowsRequest],
        Union[bigtable.MutateRowsResponse, Awaitable[bigtable.MutateRowsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def check_and_mutate_row(
        self,
    ) -> Callable[
        [bigtable.CheckAndMutateRowRequest],
        Union[
            bigtable.CheckAndMutateRowResponse,
            Awaitable[bigtable.CheckAndMutateRowResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def ping_and_warm(
        self,
    ) -> Callable[
        [bigtable.PingAndWarmRequest],
        Union[bigtable.PingAndWarmResponse, Awaitable[bigtable.PingAndWarmResponse]],
    ]:
        raise NotImplementedError()

    @property
    def read_modify_write_row(
        self,
    ) -> Callable[
        [bigtable.ReadModifyWriteRowRequest],
        Union[
            bigtable.ReadModifyWriteRowResponse,
            Awaitable[bigtable.ReadModifyWriteRowResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("BigtableTransport",)
