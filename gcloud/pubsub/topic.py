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

"""Define API Topics."""

import base64

from gcloud._helpers import _NOW
from gcloud._helpers import _RFC3339_MICROS
from gcloud.exceptions import NotFound
from gcloud.pubsub._helpers import topic_name_from_path
from gcloud.pubsub.subscription import Subscription


class Topic(object):
    """Topics are targets to which messages can be published.

    Subscribers then receive those messages.

    See:
    https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics

    :type name: string
    :param name: the name of the topic

    :type client: :class:`gcloud.pubsub.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the topic (which requires a project).

    :type timestamp_messages: boolean
    :param timestamp_messages: If true, the topic will add a ``timestamp`` key
                               to the attributes of each published message:
                               the value will be an RFC 3339 timestamp.
    """
    def __init__(self, name, client, timestamp_messages=False):
        self.name = name
        self._client = client
        self.timestamp_messages = timestamp_messages

    def subscription(self, name, ack_deadline=None, push_endpoint=None):
        """Creates a subscription bound to the current topic.

        :type name: string
        :param name: the name of the subscription

        :type ack_deadline: int
        :param ack_deadline: the deadline (in seconds) by which messages pulled
                             from the back-end must be acknowledged.

        :type push_endpoint: string
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end. If not set, the application must pull
                              messages.
        """
        return Subscription(name, self, ack_deadline=ack_deadline,
                            push_endpoint=push_endpoint)

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a topic given its API representation

        :type resource: dict
        :param resource: topic resource representation returned from the API

        :type client: :class:`gcloud.pubsub.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the topic.

        :rtype: :class:`gcloud.pubsub.topic.Topic`
        :returns: Topic parsed from ``resource``.
        :raises: :class:`ValueError` if ``client`` is not ``None`` and the
                 project from the resource does not agree with the project
                 from the client.
        """
        topic_name = topic_name_from_path(resource['name'], client.project)
        return cls(topic_name, client=client)

    @property
    def project(self):
        """Project bound to the topic."""
        return self._client.project

    @property
    def full_name(self):
        """Fully-qualified name used in topic / subscription APIs"""
        return 'projects/%s/topics/%s' % (self.project, self.name)

    @property
    def path(self):
        """URL path for the topic's APIs"""
        return '/%s' % (self.full_name)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :rtype: :class:`gcloud.pubsub.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def create(self, client=None):
        """API call:  create the topic via a PUT request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/create

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.
        """
        client = self._require_client(client)
        client.connection.api_request(method='PUT', path=self.path)

    def exists(self, client=None):
        """API call:  test for the existence of the topic via a GET request

        See
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/get

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.
        """
        client = self._require_client(client)

        try:
            client.connection.api_request(method='GET', path=self.path)
        except NotFound:
            return False
        else:
            return True

    def _timestamp_message(self, attrs):
        """Add a timestamp to ``attrs``, if the topic is so configured.

        If ``attrs`` already has the key, do nothing.

        Helper method for ``publish``/``Batch.publish``.
        """
        if self.timestamp_messages and 'timestamp' not in attrs:
            attrs['timestamp'] = _NOW().strftime(_RFC3339_MICROS)

    def publish(self, message, client=None, **attrs):
        """API call:  publish a message to a topic via a POST request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/publish

        :type message: bytes
        :param message: the message payload

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :type attrs: dict (string -> string)
        :param attrs: key-value pairs to send as message attributes

        :rtype: str
        :returns: message ID assigned by the server to the published message
        """
        client = self._require_client(client)

        self._timestamp_message(attrs)
        message_b = base64.b64encode(message).decode('ascii')
        message_data = {'data': message_b, 'attributes': attrs}
        data = {'messages': [message_data]}
        response = client.connection.api_request(
            method='POST', path='%s:publish' % (self.path,), data=data)
        return response['messageIds'][0]

    def batch(self, client=None):
        """Return a batch to use as a context manager.

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :rtype: :class:`Batch`
        :returns: A batch to use as a context manager.
        """
        client = self._require_client(client)
        return Batch(self, client)

    def delete(self, client=None):
        """API call:  delete the topic via a DELETE request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/delete

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)


class Batch(object):
    """Context manager:  collect messages to publish via a single API call.

    Helper returned by :meth:Topic.batch

    :type topic: :class:`gcloud.pubsub.topic.Topic`
    :param topic: the topic being published

    :type client: :class:`gcloud.pubsub.client.Client`
    :param client: The client to use.
    """
    def __init__(self, topic, client):
        self.topic = topic
        self.messages = []
        self.message_ids = []
        self.client = client

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()

    def __iter__(self):
        return iter(self.message_ids)

    def publish(self, message, **attrs):
        """Emulate publishing a message, but save it.

        :type message: bytes
        :param message: the message payload

        :type attrs: dict (string -> string)
        :param attrs: key-value pairs to send as message attributes
        """
        self.topic._timestamp_message(attrs)
        self.messages.append(
            {'data': base64.b64encode(message).decode('ascii'),
             'attributes': attrs})

    def commit(self, client=None):
        """Send saved messages as a single API call.

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current batch.
        """
        if client is None:
            client = self.client
        response = client.connection.api_request(
            method='POST', path='%s:publish' % self.topic.path,
            data={'messages': self.messages[:]})
        self.message_ids.extend(response['messageIds'])
        del self.messages[:]
