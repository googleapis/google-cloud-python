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

"""Define API Subscriptions."""

from gcloud.exceptions import NotFound
from gcloud.pubsub._helpers import topic_name_from_path
from gcloud.pubsub.message import Message


class Subscription(object):
    """Subscriptions receive messages published to their topics.

    See:
    https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions

    :type name: string
    :param name: the name of the subscription

    :type topic: :class:`gcloud.pubsub.topic.Topic`
    :param topic: the topic to which the subscription belongs..

    :type ack_deadline: int
    :param ack_deadline: the deadline (in seconds) by which messages pulled
                         from the back-end must be acknowledged.

    :type push_endpoint: string
    :param push_endpoint: URL to which messages will be pushed by the back-end.
                          If not set, the application must pull messages.
    """
    def __init__(self, name, topic, ack_deadline=None, push_endpoint=None):
        self.name = name
        self.topic = topic
        self.ack_deadline = ack_deadline
        self.push_endpoint = push_endpoint

    @classmethod
    def from_api_repr(cls, resource, client, topics=None):
        """Factory:  construct a topic given its API representation

        :type resource: dict
        :param resource: topic resource representation returned from the API

        :type client: :class:`gcloud.pubsub.client.Client`
        :param client: Client which holds credentials and project
                       configuration for a topic.

        :type topics: dict or None
        :param topics: A mapping of topic names -> topics.  If not passed,
                       the subscription will have a newly-created topic.

        :rtype: :class:`gcloud.pubsub.subscription.Subscription`
        :returns: Subscription parsed from ``resource``.
        """
        if topics is None:
            topics = {}
        topic_path = resource['topic']
        topic = topics.get(topic_path)
        if topic is None:
            # NOTE: This duplicates behavior from Topic.from_api_repr to avoid
            #       an import cycle.
            topic_name = topic_name_from_path(topic_path, client.project)
            topic = topics[topic_path] = client.topic(topic_name)
        _, _, _, name = resource['name'].split('/')
        ack_deadline = resource.get('ackDeadlineSeconds')
        push_config = resource.get('pushConfig', {})
        push_endpoint = push_config.get('pushEndpoint')
        return cls(name, topic, ack_deadline, push_endpoint)

    @property
    def path(self):
        """URL path for the subscription's APIs"""
        project = self.topic.project
        return '/projects/%s/subscriptions/%s' % (project, self.name)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the topic of the
                       current subscription.

        :rtype: :class:`gcloud.pubsub.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self.topic._client
        return client

    def create(self, client=None):
        """API call:  create the subscription via a PUT request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/create

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        data = {'topic': self.topic.full_name}

        if self.ack_deadline is not None:
            data['ackDeadline'] = self.ack_deadline

        if self.push_endpoint is not None:
            data['pushConfig'] = {'pushEndpoint': self.push_endpoint}

        client = self._require_client(client)
        client.connection.api_request(method='PUT', path=self.path, data=data)

    def exists(self, client=None):
        """API call:  test existence of the subscription via a GET request

        See
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/get

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        try:
            client.connection.api_request(method='GET', path=self.path)
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  sync local subscription configuration via a GET request

        See
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/get

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        data = client.connection.api_request(method='GET', path=self.path)
        self.ack_deadline = data.get('ackDeadline')
        push_config = data.get('pushConfig', {})
        self.push_endpoint = push_config.get('pushEndpoint')

    def modify_push_configuration(self, push_endpoint, client=None):
        """API call:  update the push endpoint for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/modifyPushConfig

        :type push_endpoint: string
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end.  If None, the application must pull
                              messages.

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        data = {}
        config = data['pushConfig'] = {}
        if push_endpoint is not None:
            config['pushEndpoint'] = push_endpoint
        client.connection.api_request(
            method='POST', path='%s:modifyPushConfig' % (self.path,),
            data=data)
        self.push_endpoint = push_endpoint

    def pull(self, return_immediately=False, max_messages=1, client=None):
        """API call:  retrieve messages for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/pull

        :type return_immediately: boolean
        :param return_immediately: if True, the back-end returns even if no
                                   messages are available;  if False, the API
                                   call blocks until one or more messages are
                                   available.

        :type max_messages: int
        :param max_messages: the maximum number of messages to return.

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.

        :rtype: list of (ack_id, message) tuples
        :returns: sequence of tuples: ``ack_id`` is the ID to be used in a
                  subsequent call to :meth:`acknowledge`, and ``message``
                  is an instance of :class:`gcloud.pubsub.message.Message`.
        """
        client = self._require_client(client)
        data = {'returnImmediately': return_immediately,
                'maxMessages': max_messages}
        response = client.connection.api_request(
            method='POST', path='%s:pull' % (self.path,), data=data)
        return [(info['ackId'], Message.from_api_repr(info['message']))
                for info in response.get('receivedMessages', ())]

    def acknowledge(self, ack_ids, client=None):
        """API call:  acknowledge retrieved messages for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/acknowledge

        :type ack_ids: list of string
        :param ack_ids: ack IDs of messages being acknowledged

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        data = {'ackIds': ack_ids}
        client.connection.api_request(
            method='POST', path='%s:acknowledge' % (self.path,), data=data)

    def modify_ack_deadline(self, ack_id, ack_deadline, client=None):
        """API call:  update acknowledgement deadline for a retrieved message.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/acknowledge

        :type ack_id: string
        :param ack_id: ack ID of message being updated

        :type ack_deadline: int
        :param ack_deadline: new deadline for the message, in seconds

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        data = {'ackIds': [ack_id], 'ackDeadlineSeconds': ack_deadline}
        client.connection.api_request(
            method='POST', path='%s:modifyAckDeadline' % (self.path,),
            data=data)

    def delete(self, client=None):
        """API call:  delete the subscription via a DELETE request.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/delete

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)
