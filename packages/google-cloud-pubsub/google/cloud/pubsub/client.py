# Copyright 2015 Google Inc.
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

"""Client for interacting with the Google Cloud Pub/Sub API."""

import os

from google.cloud.client import ClientWithProject
from google.cloud.environment_vars import DISABLE_GRPC
from google.cloud.pubsub._http import Connection
from google.cloud.pubsub._http import _PublisherAPI as JSONPublisherAPI
from google.cloud.pubsub._http import _SubscriberAPI as JSONSubscriberAPI
from google.cloud.pubsub._http import _IAMPolicyAPI
from google.cloud.pubsub.subscription import Subscription
from google.cloud.pubsub.topic import Topic

try:
    from google.cloud.pubsub._gax import _PublisherAPI as GAXPublisherAPI
    from google.cloud.pubsub._gax import _SubscriberAPI as GAXSubscriberAPI
    from google.cloud.pubsub._gax import make_gax_publisher_api
    from google.cloud.pubsub._gax import make_gax_subscriber_api
except ImportError:  # pragma: NO COVER
    _HAVE_GRPC = False
    GAXPublisherAPI = None
    GAXSubscriberAPI = None
    make_gax_publisher_api = None
    make_gax_subscriber_api = None
else:
    _HAVE_GRPC = True


_DISABLE_GRPC = os.getenv(DISABLE_GRPC, False)
_USE_GRPC = _HAVE_GRPC and not _DISABLE_GRPC


class Client(ClientWithProject):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a topic.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``_http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type _http: :class:`~httplib2.Http`
    :param _http: (Optional) HTTP object to make requests. Can be any object
                  that defines ``request()`` with the same interface as
                  :meth:`~httplib2.Http.request`. If not passed, an
                  ``_http`` object is created that is bound to the
                  ``credentials`` for the current object.
                  This parameter should be considered private, and could
                  change in the future.

    :type _use_grpc: bool
    :param _use_grpc: (Optional) Explicitly specifies whether
                      to use the gRPC transport (via GAX) or HTTP. If unset,
                      falls back to the ``GOOGLE_CLOUD_DISABLE_GRPC``
                      environment variable.
                      This parameter should be considered private, and could
                      change in the future.
    """

    _publisher_api = None
    _subscriber_api = None
    _iam_policy_api = None

    SCOPE = ('https://www.googleapis.com/auth/pubsub',
             'https://www.googleapis.com/auth/cloud-platform')
    """The scopes required for authenticating as a Cloud Pub/Sub consumer."""

    def __init__(self, project=None, credentials=None,
                 _http=None, _use_grpc=None):
        super(Client, self).__init__(
            project=project, credentials=credentials, _http=_http)
        self._connection = Connection(self)
        if _use_grpc is None:
            self._use_grpc = _USE_GRPC
        else:
            self._use_grpc = _use_grpc

    @property
    def publisher_api(self):
        """Helper for publisher-related API calls."""
        if self._publisher_api is None:
            if self._use_grpc:
                if self._connection.in_emulator:
                    generated = make_gax_publisher_api(
                        host=self._connection.host)
                else:
                    generated = make_gax_publisher_api(
                        credentials=self._credentials)
                self._publisher_api = GAXPublisherAPI(generated, self)
            else:
                self._publisher_api = JSONPublisherAPI(self)
        return self._publisher_api

    @property
    def subscriber_api(self):
        """Helper for subscriber-related API calls."""
        if self._subscriber_api is None:
            if self._use_grpc:
                if self._connection.in_emulator:
                    generated = make_gax_subscriber_api(
                        host=self._connection.host)
                else:
                    generated = make_gax_subscriber_api(
                        credentials=self._credentials)
                self._subscriber_api = GAXSubscriberAPI(generated, self)
            else:
                self._subscriber_api = JSONSubscriberAPI(self)
        return self._subscriber_api

    @property
    def iam_policy_api(self):
        """Helper for IAM policy-related API calls."""
        if self._iam_policy_api is None:
            self._iam_policy_api = _IAMPolicyAPI(self)
        return self._iam_policy_api

    def list_topics(self, page_size=None, page_token=None):
        """List topics for the project associated with this client.

        See
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/list

        Example:

        .. literalinclude:: snippets.py
           :start-after: [START client_list_topics]
           :end-before: [END client_list_topics]

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.pubsub.topic.Topic`
                  accessible to the current API.
        """
        api = self.publisher_api
        return api.list_topics(
            self.project, page_size, page_token)

    def list_subscriptions(self, page_size=None, page_token=None):
        """List subscriptions for the project associated with this client.

        See
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/list

        Example:

        .. literalinclude:: snippets.py
           :start-after: [START client_list_subscriptions]
           :end-before: [END client_list_subscriptions]

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of
                  :class:`~google.cloud.pubsub.subscription.Subscription`
                  accessible to the current client.
        """
        api = self.subscriber_api
        return api.list_subscriptions(
            self.project, page_size, page_token)

    def list_snapshots(self, page_size=None, page_token=None):
        """List snapshots for the project associated with this API.

        See
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.snapshots/list

        :type project: str
        :param project: project ID

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.pubsub.snapshot.Snapshot`
                  accessible to the current API.
        """
        api = self.subscriber_api
        return api.list_snapshots(
            self.project, page_size, page_token)

    def topic(self, name, timestamp_messages=False):
        """Creates a topic bound to the current client.

        Example:

        .. literalinclude:: snippets.py
           :start-after: [START client_topic]
           :end-before: [END client_topic]
           :dedent: 4

        :type name: str
        :param name: the name of the topic to be constructed.

        :type timestamp_messages: bool
        :param timestamp_messages: To be passed to ``Topic`` constructor.

        :rtype: :class:`google.cloud.pubsub.topic.Topic`
        :returns: Topic created with the current client.
        """
        return Topic(name, client=self, timestamp_messages=timestamp_messages)

    def subscription(self, name, ack_deadline=None, push_endpoint=None,
                     retain_acked_messages=None,
                     message_retention_duration=None):
        """Creates a subscription bound to the current client.

        Example:

        .. literalinclude:: snippets.py
           :start-after: [START client_subscription]
           :end-before: [END client_subscription]
           :dedent: 4

        :type name: str
        :param name: the name of the subscription to be constructed.

        :type ack_deadline: int
        :param ack_deadline: (Optional) The deadline (in seconds) by which
                             messages pulledfrom the back-end must be
                             acknowledged.

        :type push_endpoint: str
        :param push_endpoint:
            (Optional) URL to which messages will be pushed by the back-end.
            If not set, the application must pull messages.

        :type retain_acked_messages: bool
        :param retain_acked_messages:
            (Optional) Whether to retain acked messages. If set, acked messages
            are retained in the subscription's backlog for a duration indicated
            by ``message_retention_duration``.

        :type message_retention_duration: :class:`datetime.timedelta`
        :param message_retention_duration:
            (Optional) Whether to retain acked messages. If set, acked messages
            are retained in the subscription's backlog for a duration indicated
            by ``message_retention_duration``. If unset, defaults to 7 days.

        :rtype: :class:`~google.cloud.pubsub.subscription.Subscription`
        :returns: Subscription created with the current client.
        """
        return Subscription(
            name, ack_deadline=ack_deadline, push_endpoint=push_endpoint,
            retain_acked_messages=retain_acked_messages,
            message_retention_duration=message_retention_duration, client=self)
