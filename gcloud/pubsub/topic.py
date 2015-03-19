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

""" Define API Topics."""

import base64

from gcloud.exceptions import NotFound


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
                        environment.
    """
    def __init__(self, name, project=None, connection=None):
        self.name = name
        self.project = project
        self.connection = connection

    @property
    def path(self):
        """URL path for the topic's APIs"""
        return '/projects/%s/topics/%s' % (self.project, self.name)

    def create(self):
        """API call:  create the topic via a PUT request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/create
        """
        self.connection.api_request(method='PUT', path=self.path)

    def exists(self):
        """API call:  test for the existence of the topic via a GET request

        See
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/get
        """
        try:
            self.connection.api_request(method='GET', path=self.path)
        except NotFound:
            return False
        else:
            return True

    def publish(self, message, **attrs):
        """API call:  publish a message to a topic via a POST request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/publish

        :type message: bytes
        :param message: the message payload

        :type attrs: dict (string -> string)
        :message attrs: key-value pairs to send as message attributes

        :rtype: str
        :returns: message ID assigned by the server to the published message
        """
        message_data = {'data': base64.b64encode(message), 'attributes': attrs}
        data = {'messages': [message_data]}
        response = self.connection.api_request(method='POST',
                                               path='%s:publish' % self.path,
                                               data=data)
        return response['messageIds'][0]

    def batch(self):
        """Return a batch to use as a context manager.

        :rtype: :class:_Batch
        """
        return _Batch(self)

    def delete(self):
        """API call:  delete the topic via a DELETE request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/delete
        """
        self.connection.api_request(method='DELETE', path=self.path)


class _Batch(object):
    """Context manager:  collect messages to publish via a single API call.

    Helper returned by :meth:Topic.batch
    """
    def __init__(self, topic):
        self.topic = topic
        self.messages = []
        self.message_ids = []

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
        self.messages.append(
            {'data': base64.b64encode(message), 'attributes': attrs})

    def commit(self):
        """Send saved messages as a single API call."""
        conn = self.topic.connection
        response = conn.api_request(method='POST',
                                    path='%s:publish' % self.topic.path,
                                    data={'messages': self.messages[:]})
        self.message_ids.extend(response['messageIds'])
        del self.messages[:]
