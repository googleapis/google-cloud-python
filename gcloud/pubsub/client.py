# Copyright 2015 Google Inc. All rights reserved.
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


from gcloud.client import JSONClient
from gcloud.pubsub.connection import Connection
from gcloud.pubsub.subscription import Subscription
from gcloud.pubsub.topic import Topic


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

    def list_topics(self, page_size=None, page_token=None):
        """List topics for the project associated with this client.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/list

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.pubsub.topic.Topic`, plus a
                  "next page token" string:  if not None, indicates that
                  more topics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/topics' % (self.project,)
        resp = self.connection.api_request(method='GET', path=path,
                                           query_params=params)
        topics = [Topic.from_api_repr(resource, self)
                  for resource in resp['topics']]
        return topics, resp.get('nextPageToken')

    def list_subscriptions(self, page_size=None, page_token=None,
                           topic_name=None):
        """List subscriptions for the project associated with this client.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/list

        and (where ``topic_name`` is passed):
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/subscriptions/list

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :type topic_name: string
        :param topic_name: limit results to subscriptions bound to the given
                           topic.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.pubsub.subscription.Subscription`,
                  plus a "next page token" string:  if not None, indicates that
                  more topics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        if topic_name is None:
            path = '/projects/%s/subscriptions' % (self.project,)
        else:
            path = '/projects/%s/topics/%s/subscriptions' % (self.project,
                                                             topic_name)

        resp = self.connection.api_request(method='GET', path=path,
                                           query_params=params)
        topics = {}
        subscriptions = [Subscription.from_api_repr(resource, self,
                                                    topics=topics)
                         for resource in resp['subscriptions']]
        return subscriptions, resp.get('nextPageToken')

    def topic(self, name, timestamp_messages=False):
        """Creates a topic bound to the current client.

        :type name: string
        :param name: the name of the topic to be constructed.

        :type timestamp_messages: boolean
        :param timestamp_messages: To be passed to ``Topic`` constructor.

        :rtype: :class:`gcloud.pubsub.topic.Topic`
        :returns: Topic created with the current client.
        """
        return Topic(name, client=self, timestamp_messages=timestamp_messages)
