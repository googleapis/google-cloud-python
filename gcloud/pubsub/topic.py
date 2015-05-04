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
import datetime

from gcloud._helpers import get_default_project
from gcloud._helpers import _RFC3339_MICROS
from gcloud.exceptions import NotFound
from gcloud.pubsub._implicit_environ import get_default_connection

_NOW = datetime.datetime.utcnow


class Topic(object):
    """Topics are targets to which messages can be published.

    Subscribers then receive those messages.

    See:
    https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics

    :type name: string
    :param name: the name of the topic

    :type project: string
    :param project: the project to which the topic belongs.  If not passed,
                    falls back to the default inferred from the environment.

    :type connection: :class:gcloud.pubsub.connection.Connection
    :param connection: the connection to use.  If not passed,
                        falls back to the default inferred from the

    :type timestamp_messages: boolean
    :param timestamp_messages: If true, the topic will add a ``timestamp`` key
                               to the attributes of each published message:
                               the value will be an RFC 3339 timestamp.
    """
    def __init__(self, name, project=None, connection=None,
                 timestamp_messages=False):
        if project is None:
            project = get_default_project()
        if connection is None:
            connection = get_default_connection()
        self.name = name
        self.project = project
        self.connection = connection
        self.timestamp_messages = timestamp_messages

    @classmethod
    def from_api_repr(cls, resource, connection=None):
        """Factory:  construct a topic given its API representation

        :type resource: dict
        :param resource: topic resource representation returned from the API

        :type connection: :class:`gcloud.pubsub.connection.Connection` or None
        :param connection: the connection to use.  If not passed,
                           falls back to the default inferred from the
                           environment.

        :rtype: :class:`gcloud.pubsub.topic.Topic`
        """
        _, project, _, name = resource['name'].split('/')
        return cls(name, project, connection)

    @property
    def full_name(self):
        """Fully-qualified name used in topic / subscription APIs"""
        return 'projects/%s/topics/%s' % (self.project, self.name)

    @property
    def path(self):
        """URL path for the topic's APIs"""
        return '/%s' % (self.full_name)

    def create(self, connection=None):
        """API call:  create the topic via a PUT request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/create

        :type connection: :class:`gcloud.pubsub.connection.Connection` or None
        :param connection: the connection to use.  If not passed,
                           falls back to the ``connection`` attribute.
        """
        if connection is None:
            connection = self.connection

        connection.api_request(method='PUT', path=self.path)

    def exists(self, connection=None):
        """API call:  test for the existence of the topic via a GET request

        See
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/get

        :type connection: :class:`gcloud.pubsub.connection.Connection` or None
        :param connection: the connection to use.  If not passed,
                           falls back to the ``connection`` attribute.
        """
        if connection is None:
            connection = self.connection

        try:
            connection.api_request(method='GET', path=self.path)
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

    def publish(self, message, connection=None, **attrs):
        """API call:  publish a message to a topic via a POST request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/publish

        :type message: bytes
        :param message: the message payload

        :type connection: :class:`gcloud.pubsub.connection.Connection` or None
        :param connection: the connection to use.  If not passed,
                           falls back to the ``connection`` attribute.

        :type attrs: dict (string -> string)
        :message attrs: key-value pairs to send as message attributes

        :rtype: str
        :returns: message ID assigned by the server to the published message
        """
        if connection is None:
            connection = self.connection

        self._timestamp_message(attrs)
        message_b = base64.b64encode(message).decode('ascii')
        message_data = {'data': message_b, 'attributes': attrs}
        data = {'messages': [message_data]}
        response = connection.api_request(method='POST',
                                          path='%s:publish' % self.path,
                                          data=data)
        return response['messageIds'][0]

    def batch(self, connection=None):
        """Return a batch to use as a context manager.

        :type connection: :class:`gcloud.pubsub.connection.Connection` or None
        :param connection: the connection to use.  If not passed,
                           falls back to the ``connection`` attribute.

        :rtype: :class:Batch
        """
        if connection is None:
            return Batch(self)

        return Batch(self, connection=connection)

    def delete(self, connection=None):
        """API call:  delete the topic via a DELETE request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/delete

        :type connection: :class:`gcloud.pubsub.connection.Connection` or None
        :param connection: the connection to use.  If not passed,
                           falls back to the ``connection`` attribute.
        """
        if connection is None:
            connection = self.connection

        connection.api_request(method='DELETE', path=self.path)


class Batch(object):
    """Context manager:  collect messages to publish via a single API call.

    Helper returned by :meth:Topic.batch
    """
    def __init__(self, topic, connection=None):
        self.topic = topic
        self.messages = []
        self.message_ids = []
        if connection is None:
            connection = topic.connection
        self.connection = connection

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
        :message attrs: key-value pairs to send as message attributes
        """
        self.topic._timestamp_message(attrs)
        self.messages.append(
            {'data': base64.b64encode(message).decode('ascii'),
             'attributes': attrs})

    def commit(self, connection=None):
        """Send saved messages as a single API call.

        :type connection: :class:`gcloud.pubsub.connection.Connection` or None
        :param connection: the connection to use.  If not passed,
                           falls back to the ``connection`` attribute.
        """
        if connection is None:
            connection = self.connection
        response = connection.api_request(method='POST',
                                          path='%s:publish' % self.topic.path,
                                          data={'messages': self.messages[:]})
        self.message_ids.extend(response['messageIds'])
        del self.messages[:]
