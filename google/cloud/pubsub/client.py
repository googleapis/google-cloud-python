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

from google.cloud.client import JSONClient
from google.cloud.environment_vars import DISABLE_GRPC
from google.cloud.pubsub.connection import Connection
from google.cloud.pubsub.connection import _PublisherAPI as JSONPublisherAPI
from google.cloud.pubsub.connection import _SubscriberAPI as JSONSubscriberAPI
from google.cloud.pubsub.connection import _IAMPolicyAPI
from google.cloud.pubsub.subscription import Subscription
from google.cloud.pubsub.topic import Topic

# pylint: disable=ungrouped-imports
try:
    from google.cloud.pubsub._gax import _PublisherAPI as GAXPublisherAPI
    from google.cloud.pubsub._gax import _SubscriberAPI as GAXSubscriberAPI
    from google.cloud.pubsub._gax import make_gax_publisher_api
    from google.cloud.pubsub._gax import make_gax_subscriber_api
except ImportError:  # pragma: NO COVER
    _HAVE_GAX = False
    GAXPublisherAPI = None
    GAXSubscriberAPI = None
    make_gax_publisher_api = None
    make_gax_subscriber_api = None
else:
    _HAVE_GAX = True
# pylint: enable=ungrouped-imports


_DISABLE_GAX = os.getenv(DISABLE_GRPC, False)
_USE_GAX = _HAVE_GAX and not _DISABLE_GAX


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: string
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a topic.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection
    _publisher_api = _subscriber_api = _iam_policy_api = None

    @property
    def publisher_api(self):
        """Helper for publisher-related API calls."""
        if self._publisher_api is None:
            if _USE_GAX:
                generated = make_gax_publisher_api(self.connection)
                self._publisher_api = GAXPublisherAPI(generated)
            else:
                self._publisher_api = JSONPublisherAPI(self.connection)
        return self._publisher_api

    @property
    def subscriber_api(self):
        """Helper for subscriber-related API calls."""
        if self._subscriber_api is None:
            if _USE_GAX:
                generated = make_gax_subscriber_api(self.connection)
                self._subscriber_api = GAXSubscriberAPI(generated)
            else:
                self._subscriber_api = JSONSubscriberAPI(self.connection)
        return self._subscriber_api

    @property
    def iam_policy_api(self):
        """Helper for IAM policy-related API calls."""
        if self._iam_policy_api is None:
            self._iam_policy_api = _IAMPolicyAPI(self.connection)
        return self._iam_policy_api

    def list_topics(self, page_size=None, page_token=None):
        """List topics for the project associated with this client.

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/list

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START client_list_topics]
           :end-before: [END client_list_topics]

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: tuple, (list, str)
        :returns: list of :class:`google.cloud.pubsub.topic.Topic`, plus a
                  "next page token" string:  if not None, indicates that
                  more topics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        api = self.publisher_api
        resources, next_token = api.list_topics(
            self.project, page_size, page_token)
        topics = [Topic.from_api_repr(resource, self)
                  for resource in resources]
        return topics, next_token

    def list_subscriptions(self, page_size=None, page_token=None):
        """List subscriptions for the project associated with this client.

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/list

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START client_list_subscriptions]
           :end-before: [END client_list_subscriptions]

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: tuple, (list, str)
        :returns: list of :class:`~.pubsub.subscription.Subscription`,
                  plus a "next page token" string:  if not None, indicates that
                  more topics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        api = self.subscriber_api
        resources, next_token = api.list_subscriptions(
            self.project, page_size, page_token)
        topics = {}
        subscriptions = [Subscription.from_api_repr(resource, self,
                                                    topics=topics)
                         for resource in resources]
        return subscriptions, next_token

    def topic(self, name, timestamp_messages=False):
        """Creates a topic bound to the current client.

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START client_topic]
           :end-before: [END client_topic]

        :type name: string
        :param name: the name of the topic to be constructed.

        :type timestamp_messages: boolean
        :param timestamp_messages: To be passed to ``Topic`` constructor.

        :rtype: :class:`google.cloud.pubsub.topic.Topic`
        :returns: Topic created with the current client.
        """
        return Topic(name, client=self, timestamp_messages=timestamp_messages)
