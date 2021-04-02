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


class SubscriberTransport(abc.ABC):
    """Abstract transport class for Subscriber."""

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
            self.create_subscription: gapic_v1.method.wrap_method(
                self.create_subscription,
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
            self.get_subscription: gapic_v1.method.wrap_method(
                self.get_subscription,
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
            self.update_subscription: gapic_v1.method.wrap_method(
                self.update_subscription,
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
            self.list_subscriptions: gapic_v1.method.wrap_method(
                self.list_subscriptions,
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
            self.delete_subscription: gapic_v1.method.wrap_method(
                self.delete_subscription,
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
            self.modify_ack_deadline: gapic_v1.method.wrap_method(
                self.modify_ack_deadline,
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
            self.acknowledge: gapic_v1.method.wrap_method(
                self.acknowledge,
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
            self.pull: gapic_v1.method.wrap_method(
                self.pull,
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
            self.streaming_pull: gapic_v1.method.wrap_method(
                self.streaming_pull,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.Aborted,
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ResourceExhausted,
                        exceptions.ServiceUnavailable,
                    ),
                    deadline=900.0,
                ),
                default_timeout=900.0,
                client_info=client_info,
            ),
            self.modify_push_config: gapic_v1.method.wrap_method(
                self.modify_push_config,
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
            self.get_snapshot: gapic_v1.method.wrap_method(
                self.get_snapshot,
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
            self.list_snapshots: gapic_v1.method.wrap_method(
                self.list_snapshots,
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
            self.create_snapshot: gapic_v1.method.wrap_method(
                self.create_snapshot,
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
            self.update_snapshot: gapic_v1.method.wrap_method(
                self.update_snapshot,
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
            self.delete_snapshot: gapic_v1.method.wrap_method(
                self.delete_snapshot,
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
            self.seek: gapic_v1.method.wrap_method(
                self.seek,
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
        }

    @property
    def create_subscription(
        self,
    ) -> typing.Callable[
        [pubsub.Subscription],
        typing.Union[pubsub.Subscription, typing.Awaitable[pubsub.Subscription]],
    ]:
        raise NotImplementedError()

    @property
    def get_subscription(
        self,
    ) -> typing.Callable[
        [pubsub.GetSubscriptionRequest],
        typing.Union[pubsub.Subscription, typing.Awaitable[pubsub.Subscription]],
    ]:
        raise NotImplementedError()

    @property
    def update_subscription(
        self,
    ) -> typing.Callable[
        [pubsub.UpdateSubscriptionRequest],
        typing.Union[pubsub.Subscription, typing.Awaitable[pubsub.Subscription]],
    ]:
        raise NotImplementedError()

    @property
    def list_subscriptions(
        self,
    ) -> typing.Callable[
        [pubsub.ListSubscriptionsRequest],
        typing.Union[
            pubsub.ListSubscriptionsResponse,
            typing.Awaitable[pubsub.ListSubscriptionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_subscription(
        self,
    ) -> typing.Callable[
        [pubsub.DeleteSubscriptionRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def modify_ack_deadline(
        self,
    ) -> typing.Callable[
        [pubsub.ModifyAckDeadlineRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def acknowledge(
        self,
    ) -> typing.Callable[
        [pubsub.AcknowledgeRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def pull(
        self,
    ) -> typing.Callable[
        [pubsub.PullRequest],
        typing.Union[pubsub.PullResponse, typing.Awaitable[pubsub.PullResponse]],
    ]:
        raise NotImplementedError()

    @property
    def streaming_pull(
        self,
    ) -> typing.Callable[
        [pubsub.StreamingPullRequest],
        typing.Union[
            pubsub.StreamingPullResponse, typing.Awaitable[pubsub.StreamingPullResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def modify_push_config(
        self,
    ) -> typing.Callable[
        [pubsub.ModifyPushConfigRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_snapshot(
        self,
    ) -> typing.Callable[
        [pubsub.GetSnapshotRequest],
        typing.Union[pubsub.Snapshot, typing.Awaitable[pubsub.Snapshot]],
    ]:
        raise NotImplementedError()

    @property
    def list_snapshots(
        self,
    ) -> typing.Callable[
        [pubsub.ListSnapshotsRequest],
        typing.Union[
            pubsub.ListSnapshotsResponse, typing.Awaitable[pubsub.ListSnapshotsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_snapshot(
        self,
    ) -> typing.Callable[
        [pubsub.CreateSnapshotRequest],
        typing.Union[pubsub.Snapshot, typing.Awaitable[pubsub.Snapshot]],
    ]:
        raise NotImplementedError()

    @property
    def update_snapshot(
        self,
    ) -> typing.Callable[
        [pubsub.UpdateSnapshotRequest],
        typing.Union[pubsub.Snapshot, typing.Awaitable[pubsub.Snapshot]],
    ]:
        raise NotImplementedError()

    @property
    def delete_snapshot(
        self,
    ) -> typing.Callable[
        [pubsub.DeleteSnapshotRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def seek(
        self,
    ) -> typing.Callable[
        [pubsub.SeekRequest],
        typing.Union[pubsub.SeekResponse, typing.Awaitable[pubsub.SeekResponse]],
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


__all__ = ("SubscriberTransport",)
