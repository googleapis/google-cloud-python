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
from gcloud.pubsub.connection import Connection
from gcloud.pubsub.subscription import Subscription
from gcloud.pubsub.topic import Topic


class Client(object):
    """Wrap :mod:`gcloud.pubsub` API objects.

    :type connection: :class:`gcloud.pubsub.connection.Connection` or None
    :param connection: The configured connection. Defaults to one inferred
                       from the environment.

    :type project: str or None
    :param project: The configured project. Defaults to the value inferred
                    from the environment.
    """

    def __init__(self, connection=None, project=None):
        self.connection = _require_connection(connection)
        if project is None:
            project = get_default_project()
        self.project = project

    @classmethod
    def from_service_account_json(cls, json_credentials_path, project=None,
                                  *args, **kwargs):
        """Factory to retrieve JSON credentials while creating connection.

        :type json_credentials_path: string
        :param json_credentials_path: The path to a private key file (this file
                                      was given to you when you created the
                                      service account). This file must contain
                                      a JSON object with a private key and
                                      other credentials information (downloaded
                                      from the Google APIs console).

        :type project: str or None
        :param project: The configured project. Defaults to the value inferred
                        from the environment.

        :rtype: :class:`gcloud.pubsub.client.Client`
        :returns: A client, configured with a connection created with the
                  retrieved JSON credentials, and the supplied project.
        """
        connection = Connection.from_service_account_json(
            json_credentials_path, *args, **kwargs)
        return cls(connection=connection, project=project)

    @classmethod
    def from_service_account_p12(cls, client_email, private_key_path,
                                 project=None, *args, **kwargs):
        """Factory to retrieve P12 credentials while creating connection.

        .. note::
          Unless you have an explicit reason to use a PKCS12 key for your
          service account, we recommend using a JSON key.

        :type client_email: string
        :param client_email: The e-mail attached to the service account.

        :type private_key_path: string
        :param private_key_path: The path to a private key file (this file was
                                 given to you when you created the service
                                 account). This file must be in P12 format.

        :type project: str or None
        :param project: The configured project. Defaults to the value inferred
                        from the environment.

        :rtype: :class:`gcloud.pubsub.client.Client`
        :returns: A client, configured with a connection created with the
                  retrieved P12 credentials, and the supplied project.
        """
        connection = Connection.from_service_account_p12(
            client_email, private_key_path, *args, **kwargs)
        return cls(connection=connection, project=project)

    @classmethod
    def from_environment(cls, project=None, *args, **kwargs):
        """Factory to retrieve implicit credentials while creating connection.

        :rtype: :class:`gcloud.pubsub.client.Client`
        :returns: The connection created with the retrieved implicit
                  credentials.
        :returns: A client, configured with a connection created with the
                  retrieved implicit credentials, and the supplied project
        """
        connection = Connection.from_environment(*args, **kwargs)
        return cls(connection=connection, project=project)

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
