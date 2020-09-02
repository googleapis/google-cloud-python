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

from google.cloud.tasks_v2beta3.types import cloudtasks
from google.cloud.tasks_v2beta3.types import queue
from google.cloud.tasks_v2beta3.types import queue as gct_queue
from google.cloud.tasks_v2beta3.types import task
from google.cloud.tasks_v2beta3.types import task as gct_task
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-tasks",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class CloudTasksTransport(abc.ABC):
    """Abstract transport class for CloudTasks."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "cloudtasks.googleapis.com",
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
            self.list_queues: gapic_v1.method.wrap_method(
                self.list_queues,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.get_queue: gapic_v1.method.wrap_method(
                self.get_queue,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.create_queue: gapic_v1.method.wrap_method(
                self.create_queue, default_timeout=10.0, client_info=client_info,
            ),
            self.update_queue: gapic_v1.method.wrap_method(
                self.update_queue, default_timeout=10.0, client_info=client_info,
            ),
            self.delete_queue: gapic_v1.method.wrap_method(
                self.delete_queue,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.purge_queue: gapic_v1.method.wrap_method(
                self.purge_queue, default_timeout=10.0, client_info=client_info,
            ),
            self.pause_queue: gapic_v1.method.wrap_method(
                self.pause_queue, default_timeout=10.0, client_info=client_info,
            ),
            self.resume_queue: gapic_v1.method.wrap_method(
                self.resume_queue, default_timeout=10.0, client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=10.0, client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.list_tasks: gapic_v1.method.wrap_method(
                self.list_tasks,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.get_task: gapic_v1.method.wrap_method(
                self.get_task,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.create_task: gapic_v1.method.wrap_method(
                self.create_task, default_timeout=10.0, client_info=client_info,
            ),
            self.delete_task: gapic_v1.method.wrap_method(
                self.delete_task,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=10.0,
                client_info=client_info,
            ),
            self.run_task: gapic_v1.method.wrap_method(
                self.run_task, default_timeout=10.0, client_info=client_info,
            ),
        }

    @property
    def list_queues(
        self,
    ) -> typing.Callable[
        [cloudtasks.ListQueuesRequest],
        typing.Union[
            cloudtasks.ListQueuesResponse,
            typing.Awaitable[cloudtasks.ListQueuesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_queue(
        self,
    ) -> typing.Callable[
        [cloudtasks.GetQueueRequest],
        typing.Union[queue.Queue, typing.Awaitable[queue.Queue]],
    ]:
        raise NotImplementedError()

    @property
    def create_queue(
        self,
    ) -> typing.Callable[
        [cloudtasks.CreateQueueRequest],
        typing.Union[gct_queue.Queue, typing.Awaitable[gct_queue.Queue]],
    ]:
        raise NotImplementedError()

    @property
    def update_queue(
        self,
    ) -> typing.Callable[
        [cloudtasks.UpdateQueueRequest],
        typing.Union[gct_queue.Queue, typing.Awaitable[gct_queue.Queue]],
    ]:
        raise NotImplementedError()

    @property
    def delete_queue(
        self,
    ) -> typing.Callable[
        [cloudtasks.DeleteQueueRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def purge_queue(
        self,
    ) -> typing.Callable[
        [cloudtasks.PurgeQueueRequest],
        typing.Union[queue.Queue, typing.Awaitable[queue.Queue]],
    ]:
        raise NotImplementedError()

    @property
    def pause_queue(
        self,
    ) -> typing.Callable[
        [cloudtasks.PauseQueueRequest],
        typing.Union[queue.Queue, typing.Awaitable[queue.Queue]],
    ]:
        raise NotImplementedError()

    @property
    def resume_queue(
        self,
    ) -> typing.Callable[
        [cloudtasks.ResumeQueueRequest],
        typing.Union[queue.Queue, typing.Awaitable[queue.Queue]],
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

    @property
    def list_tasks(
        self,
    ) -> typing.Callable[
        [cloudtasks.ListTasksRequest],
        typing.Union[
            cloudtasks.ListTasksResponse, typing.Awaitable[cloudtasks.ListTasksResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_task(
        self,
    ) -> typing.Callable[
        [cloudtasks.GetTaskRequest],
        typing.Union[task.Task, typing.Awaitable[task.Task]],
    ]:
        raise NotImplementedError()

    @property
    def create_task(
        self,
    ) -> typing.Callable[
        [cloudtasks.CreateTaskRequest],
        typing.Union[gct_task.Task, typing.Awaitable[gct_task.Task]],
    ]:
        raise NotImplementedError()

    @property
    def delete_task(
        self,
    ) -> typing.Callable[
        [cloudtasks.DeleteTaskRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def run_task(
        self,
    ) -> typing.Callable[
        [cloudtasks.RunTaskRequest],
        typing.Union[task.Task, typing.Awaitable[task.Task]],
    ]:
        raise NotImplementedError()


__all__ = ("CloudTasksTransport",)
