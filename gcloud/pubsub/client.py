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

"""Convenience proxies

Define wrappers for ``api`` functions, :class:`gcloud.pubsub.topic.Topic`, and
:class:`gcloud.pubsub.subscription.Subscription`, passing the memoized
connection / project as needed.
"""

from gcloud._helpers import get_default_project
from gcloud._helpers import _ClientProxy
from gcloud.pubsub._implicit_environ import _require_connection
from gcloud.pubsub import api
from gcloud.pubsub.subscription import Subscription
from gcloud.pubsub.topic import Topic


class Client(object):
    """Wrap :mod:`gcloud.pubsub` API objects.

    :type connection: :class:`gcloud.pubsub.connection.Connection` or None
    :param connection: The configured connection. Defaults to one inferred
                       from the environment.

    :type project: str or None
    :param connection: The configured project. Defaults to the value inferred
                       from the environment.
    """

    def __init__(self, connection=None, project=None):
        self.connection = _require_connection(connection)
        if project is None:
            project = get_default_project()
        self.project = project

    def topic(self, name):
        """Proxy for :class:`gcloud.pubsub.topic.Topic`.

        :type name: string
        :param name: the name of the topic

        :rtype: :class:`_Topic`
        :returns: a proxy for a newly created Topic, using the passed name
                  and the client's project.
        """
        topic = Topic(name, self.project)
        return _Topic(topic, self)

    def list_topics(self, page_size=None, page_token=None):
        """Proxy for :func:`gcloud.pubsub.api.list_topics`.

        Passes configured connection and project.
        """
        topics, next_page_token = api.list_topics(
            page_size=page_size,
            page_token=page_token,
            connection=self.connection,
            project=self.project)
        proxies = [_Topic(topic, self) for topic in topics]
        return proxies, next_page_token

    def list_subscriptions(self, page_size=None, page_token=None,
                           topic_name=None):
        """Proxy for :func:`gcloud.pubsub.api.list_subscriptions`.

        Passes configured connection and project.
        """
        subscriptions, next_page_token = api.list_subscriptions(
            page_size=page_size,
            page_token=page_token,
            topic_name=topic_name,
            connection=self.connection,
            project=self.project)
        topics = dict([(sub.topic.name, _Topic(sub.topic, self))
                       for sub in subscriptions])
        proxies = [
            _Subscription(sub, self, topics[sub.topic.name])
            for sub in subscriptions]
        return proxies, next_page_token


class _Topic(_ClientProxy):
    """Proxy for :class:`gcloud.pubsub.topic.Topic`.

    :type wrapped: :class:`gcloud.pubsub.topic.Topic`
    :param wrapped: Topic being proxied.

    :type client: :class:`gcloud.pubsub.client.Client`
    :param client: Client used to pass connection / project.
    """
    def subscription(self, name, ack_deadline=None, push_endpoint=None):
        """ Proxy through to :class:`gcloud.pubsub.subscription.Subscription`.

        :rtype: :class:`_Subscription`
        """
        subscription = Subscription(
            name,
            self._wrapped,
            ack_deadline=ack_deadline,
            push_endpoint=push_endpoint)
        return _Subscription(subscription, self._client, self)


class _Subscription(_ClientProxy):
    """Proxy for :class:`gcloud.pubsub.subscription.Subscription`.

    :type wrapped: :class:`gcloud.pubsub.topic.Subscription`
    :param wrapped: Subscription being proxied.

    :type client: :class:`gcloud.pubsub.client.Client`
    :param client: Client used to pass connection / project.

    :type topic: :class:`gcloud.pubsub.client._Topic`
    :param topic: proxy for the wrapped subscription's topic.
    """
    def __init__(self, wrapped, client, topic):
        super(_Subscription, self).__init__(wrapped, client)
        self.topic = topic
