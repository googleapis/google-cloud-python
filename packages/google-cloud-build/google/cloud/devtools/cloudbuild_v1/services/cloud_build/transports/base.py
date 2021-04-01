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

from google.cloud.devtools.cloudbuild_v1.types import cloudbuild
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-devtools-cloudbuild",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


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
            self.create_build: gapic_v1.method.wrap_method(
                self.create_build, default_timeout=600.0, client_info=client_info,
            ),
            self.get_build: gapic_v1.method.wrap_method(
                self.get_build,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.list_builds: gapic_v1.method.wrap_method(
                self.list_builds,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.cancel_build: gapic_v1.method.wrap_method(
                self.cancel_build, default_timeout=600.0, client_info=client_info,
            ),
            self.retry_build: gapic_v1.method.wrap_method(
                self.retry_build, default_timeout=600.0, client_info=client_info,
            ),
            self.create_build_trigger: gapic_v1.method.wrap_method(
                self.create_build_trigger,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.get_build_trigger: gapic_v1.method.wrap_method(
                self.get_build_trigger,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.list_build_triggers: gapic_v1.method.wrap_method(
                self.list_build_triggers,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.delete_build_trigger: gapic_v1.method.wrap_method(
                self.delete_build_trigger,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.update_build_trigger: gapic_v1.method.wrap_method(
                self.update_build_trigger,
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.run_build_trigger: gapic_v1.method.wrap_method(
                self.run_build_trigger, default_timeout=600.0, client_info=client_info,
            ),
            self.receive_trigger_webhook: gapic_v1.method.wrap_method(
                self.receive_trigger_webhook,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_worker_pool: gapic_v1.method.wrap_method(
                self.create_worker_pool, default_timeout=600.0, client_info=client_info,
            ),
            self.get_worker_pool: gapic_v1.method.wrap_method(
                self.get_worker_pool,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
            self.delete_worker_pool: gapic_v1.method.wrap_method(
                self.delete_worker_pool, default_timeout=600.0, client_info=client_info,
            ),
            self.update_worker_pool: gapic_v1.method.wrap_method(
                self.update_worker_pool, default_timeout=600.0, client_info=client_info,
            ),
            self.list_worker_pools: gapic_v1.method.wrap_method(
                self.list_worker_pools,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=600.0,
                ),
                default_timeout=600.0,
                client_info=client_info,
            ),
        }

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
    def receive_trigger_webhook(
        self,
    ) -> typing.Callable[
        [cloudbuild.ReceiveTriggerWebhookRequest],
        typing.Union[
            cloudbuild.ReceiveTriggerWebhookResponse,
            typing.Awaitable[cloudbuild.ReceiveTriggerWebhookResponse],
        ],
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
