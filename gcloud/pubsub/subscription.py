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

""" Define API Subscriptions."""

from gcloud.exceptions import NotFound


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

    @property
    def path(self):
        """URL path for the subscription's APIs"""
        project = self.topic.project
        return '/projects/%s/subscriptions/%s' % (project, self.name)

    def create(self):
        """API call:  create the subscription via a PUT request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/create
        """
        data = {'topic': self.topic.path}

        if self.ack_deadline is not None:
            data['ackDeadline'] = self.ack_deadline

        if self.push_endpoint is not None:
            data['pushConfig'] = {'pushEndpoint': self.push_endpoint}

        conn = self.topic.connection
        conn.api_request(method='PUT', path=self.path, data=data)

    def exists(self):
        """API call:  test existence of the subsription via a GET request

        See
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/get
        """
        conn = self.topic.connection
        try:
            conn.api_request(method='GET',
                             path=self.path,
                             query_params={'fields': 'name'})
        except NotFound:
            return False
        else:
            return True

    def reload(self):
        """API call:  test existence of the subsription via a GET request

        See
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/get
        """
        conn = self.topic.connection
        data = conn.api_request(method='GET', path=self.path)
        self.ack_deadline = data.get('ackDeadline')
        push_config = data.get('pushConfig', {})
        self.push_endpoint = push_config.get('pushEndpoint')

    def modify_push_configuration(self, push_endpoint):
        """API call:  update the push endpoint for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/modifyPushConfig
        """
        data = {}
        config = data['pushConfig'] = {}
        if push_endpoint is not None:
            config['pushEndpoint'] = push_endpoint
        conn = self.topic.connection
        conn.api_request(method='POST',
                         path='%s:modifyPushConfig' % self.path,
                         data=data)
        self.push_endpoint = push_endpoint

    def pull(self, return_immediately=False, max_messages=1):
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

        :rtype: list of dict
        :returns: sequence of mappings, each containing keys ``ackId`` (the
                  ID to be used in a subsequent call to :meth:`acknowledge`)
                  and ``message``.
        """
        data = {'returnImmediately': return_immediately,
                'maxMessages': max_messages}
        conn = self.topic.connection
        response = conn.api_request(method='POST',
                                    path='%s:pull' % self.path,
                                    data=data)
        return response['receivedMessages']

    def acknowledge(self, ack_ids):
        """API call:  acknowledge retrieved messages for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/acknowledge

        :type ack_ids: list of string
        :param ack_ids: ack IDs of messages being acknowledged
        """
        data = {'ackIds': ack_ids}
        conn = self.topic.connection
        conn.api_request(method='POST',
                         path='%s:acknowledge' % self.path,
                         data=data)

    def modify_ack_deadline(self, ack_id, ack_deadline):
        """API call:  acknowledge retrieved messages for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/acknowledge

        :type ack_id: string
        :param ack_id: ack ID of message being updated

        :type ack_deadline: int
        :param ack_deadline: new deadline for the message, in seconds
        """
        data = {'ackId': ack_id, 'ackDeadlineSeconds': ack_deadline}
        conn = self.topic.connection
        conn.api_request(method='POST',
                         path='%s:modifyAckDeadline' % self.path,
                         data=data)

    def delete(self):
        """API call:  delete the subscription via a DELETE request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/subscriptions/delete
        """
        conn = self.topic.connection
        conn.api_request(method='DELETE', path=self.path)
