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
from gcloud.pubsub.iam import Policy
from gcloud.pubsub.message import Message


class Subscription(object):
    """Subscriptions receive messages published to their topics.

    See:
    https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions

    :type name: string
    :param name: the name of the subscription

    :type topic: :class:`gcloud.pubsub.topic.Topic` or ``NoneType``
    :param topic: the topic to which the subscription belongs;  if ``None``,
                  the subscription's topic has been deleted.

    :type ack_deadline: int
    :param ack_deadline: the deadline (in seconds) by which messages pulled
                         from the back-end must be acknowledged.

    :type push_endpoint: string
    :param push_endpoint: URL to which messages will be pushed by the back-end.
                          If not set, the application must pull messages.

    :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
    :param client: the client to use.  If not passed, falls back to the
                   ``client`` stored on the topic.
    """

    _DELETED_TOPIC_PATH = '_deleted-topic_'
    """Value of ``projects.subscriptions.topic`` when topic has been deleted.

    See:
    https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions#Subscription.FIELDS.topic
    """

    def __init__(self, name, topic=None, ack_deadline=None, push_endpoint=None,
                 client=None):

        if client is None and topic is None:
            raise TypeError("Pass only one of 'topic' or 'client'.")

        if client is not None and topic is not None:
            raise TypeError("Pass only one of 'topic' or 'client'.")

        self.name = name
        self.topic = topic
        self._client = client or topic._client
        self._project = self._client.project
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
        if topic_path == cls._DELETED_TOPIC_PATH:
            topic = None
        else:
            topic = topics.get(topic_path)
            if topic is None:
                # NOTE: This duplicates behavior from Topic.from_api_repr to
                #       avoid an import cycle.
                topic_name = topic_name_from_path(topic_path, client.project)
                topic = topics[topic_path] = client.topic(topic_name)
        _, _, _, name = resource['name'].split('/')
        ack_deadline = resource.get('ackDeadlineSeconds')
        push_config = resource.get('pushConfig', {})
        push_endpoint = push_config.get('pushEndpoint')
        if topic is None:
            return cls(name, ack_deadline=ack_deadline,
                       push_endpoint=push_endpoint, client=client)
        return cls(name, topic, ack_deadline, push_endpoint)

    @property
    def project(self):
        """Project bound to the subscription."""
        return self._client.project

    @property
    def full_name(self):
        """Fully-qualified name used in subscription APIs"""
        return 'projects/%s/subscriptions/%s' % (self.project, self.name)

    @property
    def path(self):
        """URL path for the subscription's APIs"""
        return '/%s' % (self.full_name,)

    def auto_ack(self, return_immediately=False, max_messages=1, client=None):
        """:class:`AutoAck` factory

        :type return_immediately: boolean
        :param return_immediately: passed through to :meth:`Subscription.pull`

        :type max_messages: int
        :param max_messages: passed through to :meth:`Subscription.pull`

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: passed through to :meth:`Subscription.pull` and
                      :meth:`Subscription.acknowledge`.

        :rtype: :class:`AutoAck`
        :returns: the instance created for the given ``ack_id`` and ``message``
        """
        return AutoAck(self, return_immediately, max_messages, client)

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
            client = self._client
        return client

    def create(self, client=None):
        """API call:  create the subscription via a PUT request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/create

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_create]
           :end-before: [END subscription_create]

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        api = client.subscriber_api
        api.subscription_create(
            self.full_name, self.topic.full_name, self.ack_deadline,
            self.push_endpoint)

    def exists(self, client=None):
        """API call:  test existence of the subscription via a GET request

        See
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/get

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_exists]
           :end-before: [END subscription_exists]

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.

        :rtype: bool
        :returns: Boolean indicating existence of the subscription.
        """
        client = self._require_client(client)
        api = client.subscriber_api
        try:
            api.subscription_get(self.full_name)
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  sync local subscription configuration via a GET request

        See
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/get

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_reload]
           :end-before: [END subscription_reload]

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        api = client.subscriber_api
        data = api.subscription_get(self.full_name)
        self.ack_deadline = data.get('ackDeadlineSeconds')
        push_config = data.get('pushConfig', {})
        self.push_endpoint = push_config.get('pushEndpoint')

    def delete(self, client=None):
        """API call:  delete the subscription via a DELETE request.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/delete

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_delete]
           :end-before: [END subscription_delete]

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        api = client.subscriber_api
        api.subscription_delete(self.full_name)

    def modify_push_configuration(self, push_endpoint, client=None):
        """API call:  update the push endpoint for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyPushConfig

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_push_pull]
           :end-before: [END subscription_push_pull]

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_pull_push]
           :end-before: [END subscription_pull_push]

        :type push_endpoint: string
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end.  If None, the application must pull
                              messages.

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        api = client.subscriber_api
        api.subscription_modify_push_config(self.full_name, push_endpoint)
        self.push_endpoint = push_endpoint

    def pull(self, return_immediately=False, max_messages=1, client=None):
        """API call:  retrieve messages for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/pull

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_pull]
           :end-before: [END subscription_pull]

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
        api = client.subscriber_api
        response = api.subscription_pull(
            self.full_name, return_immediately, max_messages)
        return [(info['ackId'], Message.from_api_repr(info['message']))
                for info in response]

    def acknowledge(self, ack_ids, client=None):
        """API call:  acknowledge retrieved messages for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/acknowledge

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_acknowledge]
           :end-before: [END subscription_acknowledge]

        :type ack_ids: list of string
        :param ack_ids: ack IDs of messages being acknowledged

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        api = client.subscriber_api
        api.subscription_acknowledge(self.full_name, ack_ids)

    def modify_ack_deadline(self, ack_ids, ack_deadline, client=None):
        """API call:  update acknowledgement deadline for a retrieved message.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyAckDeadline

        :type ack_ids: list of string
        :param ack_ids: ack IDs of messages being updated

        :type ack_deadline: int
        :param ack_deadline: new deadline for the message, in seconds

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.
        """
        client = self._require_client(client)
        api = client.subscriber_api
        api.subscription_modify_ack_deadline(
            self.full_name, ack_ids, ack_deadline)

    def get_iam_policy(self, client=None):
        """Fetch the IAM policy for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/getIamPolicy

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_get_iam_policy]
           :end-before: [END subscription_get_iam_policy]

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.

        :rtype: :class:`gcloud.pubsub.iam.Policy`
        :returns: policy created from the resource returned by the
                  ``getIamPolicy`` API request.
        """
        client = self._require_client(client)
        api = client.iam_policy_api
        resp = api.get_iam_policy(self.full_name)
        return Policy.from_api_repr(resp)

    def set_iam_policy(self, policy, client=None):
        """Update the IAM policy for the subscription.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/setIamPolicy

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_set_iam_policy]
           :end-before: [END subscription_set_iam_policy]

        :type policy: :class:`gcloud.pubsub.iam.Policy`
        :param policy: the new policy, typically fetched via
                       :meth:`get_iam_policy` and updated in place.

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.

        :rtype: :class:`gcloud.pubsub.iam.Policy`
        :returns: updated policy created from the resource returned by the
                  ``setIamPolicy`` API request.
        """
        client = self._require_client(client)
        api = client.iam_policy_api
        resource = policy.to_api_repr()
        resp = api.set_iam_policy(self.full_name, resource)
        return Policy.from_api_repr(resp)

    def check_iam_permissions(self, permissions, client=None):
        """Verify permissions allowed for the current user.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/testIamPermissions

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START subscription_check_iam_permissions]
           :end-before: [END subscription_check_iam_permissions]

        :type permissions: list of string
        :param permissions: list of permissions to be tested

        :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current subscription's topic.

        :rtype: sequence of string
        :returns: subset of ``permissions`` allowed by current IAM policy.
        """
        client = self._require_client(client)
        api = client.iam_policy_api
        return api.test_iam_permissions(
            self.full_name, list(permissions))


class AutoAck(dict):
    """Wrapper for :meth:`Subscription.pull` results.

    Mapping, tracks messages still-to-be-acknowledged.

    When used as a context manager, acknowledges all messages still in the
    mapping on `__exit__`.  When processing the pulled messsages, application
    code MUST delete messages from the :class:`AutoAck` mapping which are not
    successfully processed, e.g.:

    .. code-block: python

       with AutoAck(subscription) as ack:  # calls ``subscription.pull``
           for ack_id, message in ack.items():
               try:
                   do_something_with(message):
               except:
                   del ack[ack_id]

    :type subscription: :class:`Subscription`
    :param subscription: subcription to be pulled.

    :type return_immediately: boolean
    :param return_immediately: passed through to :meth:`Subscription.pull`

    :type max_messages: int
    :param max_messages: passed through to :meth:`Subscription.pull`

    :type client: :class:`gcloud.pubsub.client.Client` or ``NoneType``
    :param client: passed through to :meth:`Subscription.pull` and
                   :meth:`Subscription.acknowledge`.
    """
    def __init__(self, subscription,
                 return_immediately=False, max_messages=1, client=None):
        super(AutoAck, self).__init__()
        self._subscription = subscription
        self._return_immediately = return_immediately
        self._max_messages = max_messages
        self._client = client

    def __enter__(self):
        items = self._subscription.pull(
            self._return_immediately, self._max_messages, self._client)
        self.update(items)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._subscription.acknowledge(list(self), self._client)
