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

"""Interact with Google Cloud Pub/Sub via JSON-over-HTTP."""

import base64
import copy
import functools
import os

from google.cloud import _http
from google.cloud.environment_vars import PUBSUB_EMULATOR
from google.cloud.iterator import HTTPIterator

from google.cloud.pubsub import __version__
from google.cloud.pubsub._helpers import subscription_name_from_path
from google.cloud.pubsub.subscription import Subscription
from google.cloud.pubsub.topic import Topic


PUBSUB_API_HOST = 'pubsub.googleapis.com'
"""Pub / Sub API request host."""

_CLIENT_INFO = _http.CLIENT_INFO_TEMPLATE.format(__version__)


class Connection(_http.JSONConnection):
    """A connection to Google Cloud Pub/Sub via the JSON REST API.

    :type client: :class:`~google.cloud.pubsub.client.Client`
    :param client: The client that owns the current connection.
    """

    API_BASE_URL = 'https://' + PUBSUB_API_HOST
    """The base of the API call URL."""

    API_VERSION = 'v1'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = '{api_base_url}/{api_version}{path}'
    """A template for the URL of a particular API call."""

    _EXTRA_HEADERS = {
        _http.CLIENT_INFO_HEADER: _CLIENT_INFO,
    }

    def __init__(self, client):
        super(Connection, self).__init__(client)
        emulator_host = os.getenv(PUBSUB_EMULATOR)
        if emulator_host is None:
            self.host = self.__class__.API_BASE_URL
            self.api_base_url = self.__class__.API_BASE_URL
            self.in_emulator = False
        else:
            self.host = emulator_host
            self.api_base_url = 'http://' + emulator_host
            self.in_emulator = True

    def build_api_url(self, path, query_params=None,
                      api_base_url=None, api_version=None):
        """Construct an API url given a few components, some optional.

        Typically, you shouldn't need to use this method.

        :type path: str
        :param path: The path to the resource.

        :type query_params: dict or list
        :param query_params: A dictionary of keys and values (or list of
                             key-value pairs) to insert into the query
                             string of the URL.

        :type api_base_url: str
        :param api_base_url: The base URL for the API endpoint.
                             Typically you won't have to provide this.

        :type api_version: str
        :param api_version: The version of the API to call.
                            Typically you shouldn't provide this and instead
                            use the default for the library.

        :rtype: str
        :returns: The URL assembled from the pieces provided.
        """
        if api_base_url is None:
            api_base_url = self.api_base_url
        return super(Connection, self.__class__).build_api_url(
            path, query_params=query_params,
            api_base_url=api_base_url, api_version=api_version)


class _PublisherAPI(object):
    """Helper mapping publisher-related APIs.

    :type client: :class:`~google.cloud.pubsub.client.Client`
    :param client: the client used to make API requests.
    """

    def __init__(self, client):
        self._client = client
        self.api_request = client._connection.api_request

    def list_topics(self, project, page_size=None, page_token=None):
        """API call:  list topics for a given project

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/list

        :type project: str
        :param project: project ID

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.pubsub.topic.Topic`
                  accessible to the current client.
        """
        extra_params = {}
        if page_size is not None:
            extra_params['pageSize'] = page_size
        path = '/projects/%s/topics' % (project,)

        return HTTPIterator(
            client=self._client, path=path, item_to_value=_item_to_topic,
            items_key='topics', page_token=page_token,
            extra_params=extra_params)

    def topic_create(self, topic_path):
        """API call:  create a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/create

        :type topic_path: str
        :param topic_path: the fully-qualified path of the new topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :rtype: dict
        :returns: ``Topic`` resource returned from the API.
        """
        return self.api_request(method='PUT', path='/%s' % (topic_path,))

    def topic_get(self, topic_path):
        """API call:  retrieve a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/get

        :type topic_path: str
        :param topic_path: the fully-qualified path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :rtype: dict
        :returns: ``Topic`` resource returned from the API.
        """
        return self.api_request(method='GET', path='/%s' % (topic_path,))

    def topic_delete(self, topic_path):
        """API call:  delete a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/delete

        :type topic_path: str
        :param topic_path: the fully-qualified path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.
        """
        self.api_request(method='DELETE', path='/%s' % (topic_path,))

    def topic_publish(self, topic_path, messages):
        """API call:  publish one or more messages to a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/publish

        :type topic_path: str
        :param topic_path: the fully-qualified path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type messages: list of dict
        :param messages: messages to be published.

        :rtype: list of string
        :returns: list of opaque IDs for published messages.
        """
        messages_to_send = copy.deepcopy(messages)
        _transform_messages_base64(messages_to_send, _base64_unicode)
        data = {'messages': messages_to_send}
        response = self.api_request(
            method='POST', path='/%s:publish' % (topic_path,), data=data)
        return response['messageIds']

    def topic_list_subscriptions(self, topic, page_size=None, page_token=None):
        """API call:  list subscriptions bound to a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics.subscriptions/list

        :type topic: :class:`~google.cloud.pubsub.topic.Topic`
        :param topic: The topic that owns the subscriptions.

        :type page_size: int
        :param page_size: maximum number of subscriptions to return, If not
                          passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: list of strings
        :returns: fully-qualified names of subscriptions for the supplied
                  topic.
        """
        extra_params = {}
        if page_size is not None:
            extra_params['pageSize'] = page_size
        path = '/%s/subscriptions' % (topic.full_name,)

        iterator = HTTPIterator(
            client=self._client, path=path,
            item_to_value=_item_to_subscription_for_topic,
            items_key='subscriptions',
            page_token=page_token, extra_params=extra_params)
        iterator.topic = topic
        return iterator


class _SubscriberAPI(object):
    """Helper mapping subscriber-related APIs.

    :type client: :class:`~google.cloud.pubsub.client.Client`
    :param client: the client used to make API requests.
    """

    def __init__(self, client):
        self._client = client
        self.api_request = client._connection.api_request

    def list_subscriptions(self, project, page_size=None, page_token=None):
        """API call:  list subscriptions for a given project

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/list

        :type project: str
        :param project: project ID

        :type page_size: int
        :param page_size: maximum number of subscriptions to return, If not
                          passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of subscriptions.
                           If not passed, the API will return the first page
                           of subscriptions.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of
                  :class:`~google.cloud.pubsub.subscription.Subscription`
                  accessible to the current API.
        """
        extra_params = {}
        if page_size is not None:
            extra_params['pageSize'] = page_size
        path = '/projects/%s/subscriptions' % (project,)

        # We attach a mutable topics dictionary so that as topic
        # objects are created by Subscription.from_api_repr, they
        # can be re-used by other subscriptions from the same topic.
        topics = {}
        item_to_value = functools.partial(
            _item_to_sub_for_client, topics=topics)
        return HTTPIterator(
            client=self._client, path=path, item_to_value=item_to_value,
            items_key='subscriptions', page_token=page_token,
            extra_params=extra_params)

    def subscription_create(self, subscription_path, topic_path,
                            ack_deadline=None, push_endpoint=None):
        """API call:  create a subscription

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/create

        :type subscription_path: str
        :param subscription_path:
            the fully-qualified path of the new subscription, in format
            ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type topic_path: str
        :param topic_path: the fully-qualified path of the topic being
                           subscribed, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type ack_deadline: int
        :param ack_deadline:
            (Optional) the deadline (in seconds) by which messages pulled from
            the back-end must be acknowledged.

        :type push_endpoint: str
        :param push_endpoint:
            (Optional) URL to which messages will be pushed by the back-end.
            If not set, the application must pull messages.

        :rtype: dict
        :returns: ``Subscription`` resource returned from the API.
        """
        path = '/%s' % (subscription_path,)
        resource = {'topic': topic_path}

        if ack_deadline is not None:
            resource['ackDeadlineSeconds'] = ack_deadline

        if push_endpoint is not None:
            resource['pushConfig'] = {'pushEndpoint': push_endpoint}

        return self.api_request(method='PUT', path=path, data=resource)

    def subscription_get(self, subscription_path):
        """API call:  retrieve a subscription

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/get

        :type subscription_path: str
        :param subscription_path:
            the fully-qualified path of the subscription, in format
            ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :rtype: dict
        :returns: ``Subscription`` resource returned from the API.
        """
        path = '/%s' % (subscription_path,)
        return self.api_request(method='GET', path=path)

    def subscription_delete(self, subscription_path):
        """API call:  delete a subscription

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/delete

        :type subscription_path: str
        :param subscription_path:
            the fully-qualified path of the subscription, in format
            ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.
        """
        path = '/%s' % (subscription_path,)
        self.api_request(method='DELETE', path=path)

    def subscription_modify_push_config(self, subscription_path,
                                        push_endpoint):
        """API call:  update push config of a subscription

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: str
        :param subscription_path:
            the fully-qualified path of the new subscription, in format
            ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type push_endpoint: str
        :param push_endpoint:
            (Optional) URL to which messages will be pushed by the back-end.
            If not set, the application must pull messages.
        """
        path = '/%s:modifyPushConfig' % (subscription_path,)
        resource = {'pushConfig': {'pushEndpoint': push_endpoint}}
        self.api_request(method='POST', path=path, data=resource)

    def subscription_pull(self, subscription_path, return_immediately=False,
                          max_messages=1):
        """API call:  retrieve messages for a subscription

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: str
        :param subscription_path:
            the fully-qualified path of the new subscription, in format
            ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type return_immediately: bool
        :param return_immediately: if True, the back-end returns even if no
                                   messages are available;  if False, the API
                                   call blocks until one or more messages are
                                   available.

        :type max_messages: int
        :param max_messages: the maximum number of messages to return.

        :rtype: list of dict
        :returns:  the ``receivedMessages`` element of the response.
        """
        path = '/%s:pull' % (subscription_path,)
        data = {
            'returnImmediately': return_immediately,
            'maxMessages': max_messages,
        }
        response = self.api_request(method='POST', path=path, data=data)
        messages = response.get('receivedMessages', ())
        _transform_messages_base64(messages, base64.b64decode, 'message')
        return messages

    def subscription_acknowledge(self, subscription_path, ack_ids):
        """API call:  acknowledge retrieved messages

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: str
        :param subscription_path:
            the fully-qualified path of the new subscription, in format
            ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type ack_ids: list of string
        :param ack_ids: ack IDs of messages being acknowledged
        """
        path = '/%s:acknowledge' % (subscription_path,)
        data = {
            'ackIds': ack_ids,
        }
        self.api_request(method='POST', path=path, data=data)

    def subscription_modify_ack_deadline(self, subscription_path, ack_ids,
                                         ack_deadline):
        """API call:  update ack deadline for retrieved messages

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/modifyAckDeadline

        :type subscription_path: str
        :param subscription_path:
            the fully-qualified path of the new subscription, in format
            ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type ack_ids: list of string
        :param ack_ids: ack IDs of messages being acknowledged

        :type ack_deadline: int
        :param ack_deadline: the deadline (in seconds) by which messages pulled
                            from the back-end must be acknowledged.
        """
        path = '/%s:modifyAckDeadline' % (subscription_path,)
        data = {
            'ackIds': ack_ids,
            'ackDeadlineSeconds': ack_deadline,
        }
        self.api_request(method='POST', path=path, data=data)


class _IAMPolicyAPI(object):
    """Helper mapping IAM policy-related APIs.

    :type client: :class:`~google.cloud.pubsub.client.Client`
    :param client: the client used to make API requests.
    """

    def __init__(self, client):
        self.api_request = client._connection.api_request

    def get_iam_policy(self, target_path):
        """API call:  fetch the IAM policy for the target

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/getIamPolicy
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/getIamPolicy

        :type target_path: str
        :param target_path: the path of the target object.

        :rtype: dict
        :returns: the resource returned by the ``getIamPolicy`` API request.
        """
        path = '/%s:getIamPolicy' % (target_path,)
        return self.api_request(method='GET', path=path)

    def set_iam_policy(self, target_path, policy):
        """API call:  update the IAM policy for the target

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/setIamPolicy
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/setIamPolicy

        :type target_path: str
        :param target_path: the path of the target object.

        :type policy: dict
        :param policy: the new policy resource.

        :rtype: dict
        :returns: the resource returned by the ``setIamPolicy`` API request.
        """
        wrapped = {'policy': policy}
        path = '/%s:setIamPolicy' % (target_path,)
        return self.api_request(method='POST', path=path, data=wrapped)

    def test_iam_permissions(self, target_path, permissions):
        """API call:  test permissions

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/testIamPermissions
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/testIamPermissions

        :type target_path: str
        :param target_path: the path of the target object.

        :type permissions: list of string
        :param permissions: the permissions to check

        :rtype: dict
        :returns: the resource returned by the ``getIamPolicy`` API request.
        """
        wrapped = {'permissions': permissions}
        path = '/%s:testIamPermissions' % (target_path,)
        resp = self.api_request(method='POST', path=path, data=wrapped)
        return resp.get('permissions', [])


def _base64_unicode(value):
    """Helper to base64 encode and make JSON serializable.

    :type value: str
    :param value: String value to be base64 encoded and made serializable.

    :rtype: str
    :returns: Base64 encoded string/unicode value.
    """
    as_bytes = base64.b64encode(value)
    return as_bytes.decode('ascii')


def _transform_messages_base64(messages, transform, key=None):
    """Helper for base64 encoding and decoding messages.

    :type messages: list
    :param messages: List of dictionaries with message data.

    :type transform: :class:`~types.FunctionType`
    :param transform: Function to encode/decode the message data.

    :type key: str
    :param key: Index to access messages.
    """
    for message in messages:
        if key is not None:
            message = message[key]
        if 'data' in message:
            message['data'] = transform(message['data'])


def _item_to_topic(iterator, resource):
    """Convert a JSON topic to the native object.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: A topic returned from the API.

    :rtype: :class:`~google.cloud.pubsub.topic.Topic`
    :returns: The next topic in the page.
    """
    return Topic.from_api_repr(resource, iterator.client)


def _item_to_subscription_for_topic(iterator, subscription_path):
    """Convert a subscription name to the native object.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type subscription_path: str
    :param subscription_path: Subscription path returned from the API.

    :rtype: :class:`~google.cloud.pubsub.subscription.Subscription`
    :returns: The next subscription in the page.
    """
    subscription_name = subscription_name_from_path(
        subscription_path, iterator.client.project)
    return Subscription(subscription_name, iterator.topic)


def _item_to_sub_for_client(iterator, resource, topics):
    """Convert a subscription to the native object.

    .. note::

       This method does not have the correct signature to be used as
       the ``item_to_value`` argument to
       :class:`~google.cloud.iterator.Iterator`. It is intended to be
       patched with a mutable topics argument that can be updated
       on subsequent calls. For an example, see how the method is
       used above in :meth:`_SubscriberAPI.list_subscriptions`.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: A subscription returned from the API.

    :type topics: dict
    :param topics: A dictionary of topics to be used (and modified)
                   as new subscriptions are created bound to topics.

    :rtype: :class:`~google.cloud.pubsub.subscription.Subscription`
    :returns: The next subscription in the page.
    """
    return Subscription.from_api_repr(
        resource, iterator.client, topics=topics)
