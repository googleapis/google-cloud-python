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

from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore
from google.pubsub_v1.types import pubsub


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        client_library_version=pkg_resources.get_distribution(
            "google-cloud-pubsub",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class PublisherTransport(abc.ABC):
    """Abstract transport class for Publisher."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/pubsub",
    )

    def __init__(
        self,
        *,
        host: str = "pubsub.googleapis.com",
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
            self.create_topic: gapic_v1.method.wrap_method(
                self.create_topic,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_topic: gapic_v1.method.wrap_method(
                self.update_topic,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.publish: gapic_v1.method.wrap_method(
                self.publish,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.Aborted,
                        exceptions.Cancelled,
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ResourceExhausted,
                        exceptions.ServiceUnavailable,
                        exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_topic: gapic_v1.method.wrap_method(
                self.get_topic,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.Aborted,
                        exceptions.ServiceUnavailable,
                        exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_topics: gapic_v1.method.wrap_method(
                self.list_topics,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.Aborted,
                        exceptions.ServiceUnavailable,
                        exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_topic_subscriptions: gapic_v1.method.wrap_method(
                self.list_topic_subscriptions,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.Aborted,
                        exceptions.ServiceUnavailable,
                        exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_topic_snapshots: gapic_v1.method.wrap_method(
                self.list_topic_snapshots,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.Aborted,
                        exceptions.ServiceUnavailable,
                        exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_topic: gapic_v1.method.wrap_method(
                self.delete_topic,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.detach_subscription: gapic_v1.method.wrap_method(
                self.detach_subscription,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    @property
    def create_topic(
        self,
    ) -> typing.Callable[
        [pubsub.Topic], typing.Union[pubsub.Topic, typing.Awaitable[pubsub.Topic]]
    ]:
        raise NotImplementedError()

    @property
    def update_topic(
        self,
    ) -> typing.Callable[
        [pubsub.UpdateTopicRequest],
        typing.Union[pubsub.Topic, typing.Awaitable[pubsub.Topic]],
    ]:
        raise NotImplementedError()

    @property
    def publish(
        self,
    ) -> typing.Callable[
        [pubsub.PublishRequest],
        typing.Union[pubsub.PublishResponse, typing.Awaitable[pubsub.PublishResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_topic(
        self,
    ) -> typing.Callable[
        [pubsub.GetTopicRequest],
        typing.Union[pubsub.Topic, typing.Awaitable[pubsub.Topic]],
    ]:
        raise NotImplementedError()

    @property
    def list_topics(
        self,
    ) -> typing.Callable[
        [pubsub.ListTopicsRequest],
        typing.Union[
            pubsub.ListTopicsResponse, typing.Awaitable[pubsub.ListTopicsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_topic_subscriptions(
        self,
    ) -> typing.Callable[
        [pubsub.ListTopicSubscriptionsRequest],
        typing.Union[
            pubsub.ListTopicSubscriptionsResponse,
            typing.Awaitable[pubsub.ListTopicSubscriptionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_topic_snapshots(
        self,
    ) -> typing.Callable[
        [pubsub.ListTopicSnapshotsRequest],
        typing.Union[
            pubsub.ListTopicSnapshotsResponse,
            typing.Awaitable[pubsub.ListTopicSnapshotsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_topic(
        self,
    ) -> typing.Callable[
        [pubsub.DeleteTopicRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def detach_subscription(
        self,
    ) -> typing.Callable[
        [pubsub.DetachSubscriptionRequest],
        typing.Union[
            pubsub.DetachSubscriptionResponse,
            typing.Awaitable[pubsub.DetachSubscriptionResponse],
        ],
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
    def get_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.GetIamPolicyRequest],
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


__all__ = ("PublisherTransport",)
