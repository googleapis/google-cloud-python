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
from google.auth import credentials  # type: ignore

from google.cloud.logging_v2.types import logging_config
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-logging",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class ConfigServiceV2Transport(abc.ABC):
    """Abstract transport class for ConfigServiceV2."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
        "https://www.googleapis.com/auth/logging.admin",
        "https://www.googleapis.com/auth/logging.read",
    )

    def __init__(
        self,
        *,
        host: str = "logging.googleapis.com",
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

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_buckets: gapic_v1.method.wrap_method(
                self.list_buckets, default_timeout=None, client_info=client_info,
            ),
            self.get_bucket: gapic_v1.method.wrap_method(
                self.get_bucket, default_timeout=None, client_info=client_info,
            ),
            self.create_bucket: gapic_v1.method.wrap_method(
                self.create_bucket, default_timeout=None, client_info=client_info,
            ),
            self.update_bucket: gapic_v1.method.wrap_method(
                self.update_bucket, default_timeout=None, client_info=client_info,
            ),
            self.delete_bucket: gapic_v1.method.wrap_method(
                self.delete_bucket, default_timeout=None, client_info=client_info,
            ),
            self.undelete_bucket: gapic_v1.method.wrap_method(
                self.undelete_bucket, default_timeout=None, client_info=client_info,
            ),
            self.list_views: gapic_v1.method.wrap_method(
                self.list_views, default_timeout=None, client_info=client_info,
            ),
            self.get_view: gapic_v1.method.wrap_method(
                self.get_view, default_timeout=None, client_info=client_info,
            ),
            self.create_view: gapic_v1.method.wrap_method(
                self.create_view, default_timeout=None, client_info=client_info,
            ),
            self.update_view: gapic_v1.method.wrap_method(
                self.update_view, default_timeout=None, client_info=client_info,
            ),
            self.delete_view: gapic_v1.method.wrap_method(
                self.delete_view, default_timeout=None, client_info=client_info,
            ),
            self.list_sinks: gapic_v1.method.wrap_method(
                self.list_sinks,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_sink: gapic_v1.method.wrap_method(
                self.get_sink,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_sink: gapic_v1.method.wrap_method(
                self.create_sink, default_timeout=120.0, client_info=client_info,
            ),
            self.update_sink: gapic_v1.method.wrap_method(
                self.update_sink,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_sink: gapic_v1.method.wrap_method(
                self.delete_sink,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_exclusions: gapic_v1.method.wrap_method(
                self.list_exclusions,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_exclusion: gapic_v1.method.wrap_method(
                self.get_exclusion,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_exclusion: gapic_v1.method.wrap_method(
                self.create_exclusion, default_timeout=120.0, client_info=client_info,
            ),
            self.update_exclusion: gapic_v1.method.wrap_method(
                self.update_exclusion, default_timeout=120.0, client_info=client_info,
            ),
            self.delete_exclusion: gapic_v1.method.wrap_method(
                self.delete_exclusion,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_cmek_settings: gapic_v1.method.wrap_method(
                self.get_cmek_settings, default_timeout=None, client_info=client_info,
            ),
            self.update_cmek_settings: gapic_v1.method.wrap_method(
                self.update_cmek_settings,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def list_buckets(
        self,
    ) -> typing.Callable[
        [logging_config.ListBucketsRequest],
        typing.Union[
            logging_config.ListBucketsResponse,
            typing.Awaitable[logging_config.ListBucketsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_bucket(
        self,
    ) -> typing.Callable[
        [logging_config.GetBucketRequest],
        typing.Union[
            logging_config.LogBucket, typing.Awaitable[logging_config.LogBucket]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_bucket(
        self,
    ) -> typing.Callable[
        [logging_config.CreateBucketRequest],
        typing.Union[
            logging_config.LogBucket, typing.Awaitable[logging_config.LogBucket]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_bucket(
        self,
    ) -> typing.Callable[
        [logging_config.UpdateBucketRequest],
        typing.Union[
            logging_config.LogBucket, typing.Awaitable[logging_config.LogBucket]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_bucket(
        self,
    ) -> typing.Callable[
        [logging_config.DeleteBucketRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def undelete_bucket(
        self,
    ) -> typing.Callable[
        [logging_config.UndeleteBucketRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_views(
        self,
    ) -> typing.Callable[
        [logging_config.ListViewsRequest],
        typing.Union[
            logging_config.ListViewsResponse,
            typing.Awaitable[logging_config.ListViewsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_view(
        self,
    ) -> typing.Callable[
        [logging_config.GetViewRequest],
        typing.Union[logging_config.LogView, typing.Awaitable[logging_config.LogView]],
    ]:
        raise NotImplementedError()

    @property
    def create_view(
        self,
    ) -> typing.Callable[
        [logging_config.CreateViewRequest],
        typing.Union[logging_config.LogView, typing.Awaitable[logging_config.LogView]],
    ]:
        raise NotImplementedError()

    @property
    def update_view(
        self,
    ) -> typing.Callable[
        [logging_config.UpdateViewRequest],
        typing.Union[logging_config.LogView, typing.Awaitable[logging_config.LogView]],
    ]:
        raise NotImplementedError()

    @property
    def delete_view(
        self,
    ) -> typing.Callable[
        [logging_config.DeleteViewRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_sinks(
        self,
    ) -> typing.Callable[
        [logging_config.ListSinksRequest],
        typing.Union[
            logging_config.ListSinksResponse,
            typing.Awaitable[logging_config.ListSinksResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_sink(
        self,
    ) -> typing.Callable[
        [logging_config.GetSinkRequest],
        typing.Union[logging_config.LogSink, typing.Awaitable[logging_config.LogSink]],
    ]:
        raise NotImplementedError()

    @property
    def create_sink(
        self,
    ) -> typing.Callable[
        [logging_config.CreateSinkRequest],
        typing.Union[logging_config.LogSink, typing.Awaitable[logging_config.LogSink]],
    ]:
        raise NotImplementedError()

    @property
    def update_sink(
        self,
    ) -> typing.Callable[
        [logging_config.UpdateSinkRequest],
        typing.Union[logging_config.LogSink, typing.Awaitable[logging_config.LogSink]],
    ]:
        raise NotImplementedError()

    @property
    def delete_sink(
        self,
    ) -> typing.Callable[
        [logging_config.DeleteSinkRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_exclusions(
        self,
    ) -> typing.Callable[
        [logging_config.ListExclusionsRequest],
        typing.Union[
            logging_config.ListExclusionsResponse,
            typing.Awaitable[logging_config.ListExclusionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_exclusion(
        self,
    ) -> typing.Callable[
        [logging_config.GetExclusionRequest],
        typing.Union[
            logging_config.LogExclusion, typing.Awaitable[logging_config.LogExclusion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_exclusion(
        self,
    ) -> typing.Callable[
        [logging_config.CreateExclusionRequest],
        typing.Union[
            logging_config.LogExclusion, typing.Awaitable[logging_config.LogExclusion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_exclusion(
        self,
    ) -> typing.Callable[
        [logging_config.UpdateExclusionRequest],
        typing.Union[
            logging_config.LogExclusion, typing.Awaitable[logging_config.LogExclusion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_exclusion(
        self,
    ) -> typing.Callable[
        [logging_config.DeleteExclusionRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_cmek_settings(
        self,
    ) -> typing.Callable[
        [logging_config.GetCmekSettingsRequest],
        typing.Union[
            logging_config.CmekSettings, typing.Awaitable[logging_config.CmekSettings]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_cmek_settings(
        self,
    ) -> typing.Callable[
        [logging_config.UpdateCmekSettingsRequest],
        typing.Union[
            logging_config.CmekSettings, typing.Awaitable[logging_config.CmekSettings]
        ],
    ]:
        raise NotImplementedError()


__all__ = ("ConfigServiceV2Transport",)
