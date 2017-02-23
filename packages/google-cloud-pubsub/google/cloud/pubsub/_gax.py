# Copyright 2016 Google Inc.
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

"""GAX wrapper for Pubsub API requests."""

import functools

from google.cloud.gapic.pubsub.v1.publisher_client import PublisherClient
from google.cloud.gapic.pubsub.v1.subscriber_client import SubscriberClient
from google.gax import CallOptions
from google.gax import INITIAL_PAGE
from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.protobuf.json_format import MessageToDict
from google.cloud.proto.pubsub.v1.pubsub_pb2 import PubsubMessage
from google.cloud.proto.pubsub.v1.pubsub_pb2 import PushConfig
from grpc import insecure_channel
from grpc import StatusCode

from google.cloud._helpers import _to_bytes
from google.cloud._helpers import _pb_timestamp_to_rfc3339
from google.cloud._helpers import make_secure_channel
from google.cloud._http import DEFAULT_USER_AGENT
from google.cloud.exceptions import Conflict
from google.cloud.exceptions import NotFound
from google.cloud.iterator import GAXIterator
from google.cloud.pubsub import __version__
from google.cloud.pubsub._helpers import subscription_name_from_path
from google.cloud.pubsub.subscription import Subscription
from google.cloud.pubsub.topic import Topic


class _PublisherAPI(object):
    """Helper mapping publisher-related APIs.

    :type gax_api: :class:`.publisher_client.PublisherClient`
    :param gax_api: API object used to make GAX requests.

    :type client: :class:`~google.cloud.pubsub.client.Client`
    :param client: The client that owns this API object.
    """

    def __init__(self, gax_api, client):
        self._gax_api = gax_api
        self._client = client

    def list_topics(self, project, page_size=0, page_token=None):
        """List topics for the project associated with this API.

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
                  accessible to the current API.
        """
        if page_token is None:
            page_token = INITIAL_PAGE
        options = CallOptions(page_token=page_token)
        path = 'projects/%s' % (project,)
        page_iter = self._gax_api.list_topics(
            path, page_size=page_size, options=options)
        return GAXIterator(self._client, page_iter, _item_to_topic)

    def topic_create(self, topic_path):
        """API call:  create a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/create

        :type topic_path: str
        :param topic_path: fully-qualified path of the new topic, in format
                            ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :rtype: dict
        :returns: ``Topic`` resource returned from the API.
        :raises: :exc:`google.cloud.exceptions.Conflict` if the topic already
                    exists
        """
        try:
            topic_pb = self._gax_api.create_topic(topic_path)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.FAILED_PRECONDITION:
                raise Conflict(topic_path)
            raise
        return {'name': topic_pb.name}

    def topic_get(self, topic_path):
        """API call:  retrieve a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/get

        :type topic_path: str
        :param topic_path: fully-qualified path of the topic, in format
                        ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :rtype: dict
        :returns: ``Topic`` resource returned from the API.
        :raises: :exc:`google.cloud.exceptions.NotFound` if the topic does not
                    exist
        """
        try:
            topic_pb = self._gax_api.get_topic(topic_path)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(topic_path)
            raise
        return {'name': topic_pb.name}

    def topic_delete(self, topic_path):
        """API call:  delete a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/create

        :type topic_path: str
        :param topic_path: fully-qualified path of the new topic, in format
                            ``projects/<PROJECT>/topics/<TOPIC_NAME>``.
        """
        try:
            self._gax_api.delete_topic(topic_path)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(topic_path)
            raise

    def topic_publish(self, topic_path, messages):
        """API call:  publish one or more messages to a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/publish

        :type topic_path: str
        :param topic_path: fully-qualified path of the topic, in format
                            ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type messages: list of dict
        :param messages: messages to be published.

        :rtype: list of string
        :returns: list of opaque IDs for published messages.
        :raises: :exc:`google.cloud.exceptions.NotFound` if the topic does not
                    exist
        """
        options = CallOptions(is_bundling=False)
        message_pbs = [_message_pb_from_mapping(message)
                       for message in messages]
        try:
            result = self._gax_api.publish(topic_path, message_pbs,
                                           options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(topic_path)
            raise
        return result.message_ids

    def topic_list_subscriptions(self, topic, page_size=0, page_token=None):
        """API call:  list subscriptions bound to a topic

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics.subscriptions/list

        :type topic: :class:`~google.cloud.pubsub.topic.Topic`
        :param topic: The topic that owns the subscriptions.

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
        :raises: :exc:`~google.cloud.exceptions.NotFound` if the topic does
                  not exist.
        """
        if page_token is None:
            page_token = INITIAL_PAGE
        options = CallOptions(page_token=page_token)
        topic_path = topic.full_name
        try:
            page_iter = self._gax_api.list_topic_subscriptions(
                topic_path, page_size=page_size, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(topic_path)
            raise

        iterator = GAXIterator(self._client, page_iter,
                               _item_to_subscription_for_topic)
        iterator.topic = topic
        return iterator


class _SubscriberAPI(object):
    """Helper mapping subscriber-related APIs.

    :type gax_api: :class:`.publisher_client.SubscriberClient`
    :param gax_api: API object used to make GAX requests.

    :type client: :class:`~google.cloud.pubsub.client.Client`
    :param client: The client that owns this API object.
    """
    def __init__(self, gax_api, client):
        self._gax_api = gax_api
        self._client = client

    def list_subscriptions(self, project, page_size=0, page_token=None):
        """List subscriptions for the project associated with this API.

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
        if page_token is None:
            page_token = INITIAL_PAGE
        options = CallOptions(page_token=page_token)
        path = 'projects/%s' % (project,)
        page_iter = self._gax_api.list_subscriptions(
            path, page_size=page_size, options=options)

        # We attach a mutable topics dictionary so that as topic
        # objects are created by Subscription.from_api_repr, they
        # can be re-used by other subscriptions from the same topic.
        topics = {}
        item_to_value = functools.partial(
            _item_to_sub_for_client, topics=topics)
        return GAXIterator(self._client, page_iter, item_to_value)

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
        if push_endpoint is not None:
            push_config = PushConfig(push_endpoint=push_endpoint)
        else:
            push_config = None

        if ack_deadline is None:
            ack_deadline = 0

        try:
            sub_pb = self._gax_api.create_subscription(
                subscription_path, topic_path,
                push_config=push_config, ack_deadline_seconds=ack_deadline)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.FAILED_PRECONDITION:
                raise Conflict(topic_path)
            raise
        return MessageToDict(sub_pb)

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
        try:
            sub_pb = self._gax_api.get_subscription(subscription_path)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(subscription_path)
            raise
        return MessageToDict(sub_pb)

    def subscription_delete(self, subscription_path):
        """API call:  delete a subscription

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/delete

        :type subscription_path: str
        :param subscription_path:
            the fully-qualified path of the subscription, in format
            ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.
        """
        try:
            self._gax_api.delete_subscription(subscription_path)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(subscription_path)
            raise

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
        push_config = PushConfig(push_endpoint=push_endpoint)
        try:
            self._gax_api.modify_push_config(subscription_path, push_config)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(subscription_path)
            raise

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
        try:
            response_pb = self._gax_api.pull(
                subscription_path, max_messages,
                return_immediately=return_immediately)
        except GaxError as exc:
            code = exc_to_code(exc.cause)
            if code == StatusCode.NOT_FOUND:
                raise NotFound(subscription_path)
            elif code == StatusCode.DEADLINE_EXCEEDED:
                # NOTE: The JSON-over-HTTP API returns a 200 with an empty
                #       response when ``return_immediately`` is ``False``, so
                #       we "mutate" the gRPC error into a non-error to conform.
                if not return_immediately:
                    return []
            raise
        return [_received_message_pb_to_mapping(rmpb)
                for rmpb in response_pb.received_messages]

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
        try:
            self._gax_api.acknowledge(subscription_path, ack_ids)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(subscription_path)
            raise

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
        try:
            self._gax_api.modify_ack_deadline(
                subscription_path, ack_ids, ack_deadline)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(subscription_path)
            raise


def _message_pb_from_mapping(message):
    """Helper for :meth:`_PublisherAPI.topic_publish`.

    Performs "impedance matching" between the protobuf attrs and the keys
    expected in the JSON API.
    """
    return PubsubMessage(data=_to_bytes(message['data']),
                         attributes=message['attributes'])


def _message_pb_to_mapping(message_pb):
    """Helper for :meth:`pull`, et aliae

    Performs "impedance matching" between the protobuf attrs and the keys
    expected in the JSON API.
    """
    return {
        'messageId': message_pb.message_id,
        'data': message_pb.data,
        'attributes': message_pb.attributes,
        'publishTime': _pb_timestamp_to_rfc3339(message_pb.publish_time),
    }


def _received_message_pb_to_mapping(received_message_pb):
    """Helper for :meth:`pull`, et aliae

    Performs "impedance matching" between the protobuf attrs and the keys
    expected in the JSON API.
    """
    return {
        'ackId': received_message_pb.ack_id,
        'message': _message_pb_to_mapping(
            received_message_pb.message),
    }


def make_gax_publisher_api(credentials=None, host=None):
    """Create an instance of the GAX Publisher API.

    If the ``credentials`` are omitted, then we create an insecure
    ``channel`` pointing at the local Pub / Sub emulator.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) Credentials for getting access
                        tokens.

    :type host: str
    :param host: (Optional) The host for an insecure channel. Only
                 used if ``credentials`` are omitted.

    :rtype: :class:`.publisher_client.PublisherClient`
    :returns: A publisher API instance with the proper channel.
    """
    if credentials is None:
        channel = insecure_channel(host)
    else:
        channel = make_secure_channel(
            credentials, DEFAULT_USER_AGENT,
            PublisherClient.SERVICE_ADDRESS)
    return PublisherClient(
        channel=channel, lib_name='gccl', lib_version=__version__)


def make_gax_subscriber_api(credentials=None, host=None):
    """Create an instance of the GAX Subscriber API.

    If the ``credentials`` are omitted, then we create an insecure
    ``channel`` pointing at the local Pub / Sub emulator.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) Credentials for getting access
                        tokens.

    :type host: str
    :param host: (Optional) The host for an insecure channel. Only
                 used if ``credentials`` are omitted.

    :rtype: :class:`.subscriber_client.SubscriberClient`
    :returns: A subscriber API instance with the proper channel.
    """
    if credentials is None:
        channel = insecure_channel(host)
    else:
        channel = make_secure_channel(
            credentials, DEFAULT_USER_AGENT,
            SubscriberClient.SERVICE_ADDRESS)
    return SubscriberClient(
        channel=channel, lib_name='gccl', lib_version=__version__)


def _item_to_topic(iterator, resource):
    """Convert a protobuf topic to the native object.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: :class:`.pubsub_pb2.Topic`
    :param resource: A topic returned from the API.

    :rtype: :class:`~google.cloud.pubsub.topic.Topic`
    :returns: The next topic in the page.
    """
    return Topic.from_api_repr(
        {'name': resource.name}, iterator.client)


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


def _item_to_sub_for_client(iterator, sub_pb, topics):
    """Convert a subscription protobuf to the native object.

    .. note::

       This method does not have the correct signature to be used as
       the ``item_to_value`` argument to
       :class:`~google.cloud.iterator.Iterator`. It is intended to be
       patched with a mutable topics argument that can be updated
       on subsequent calls. For an example, see how the method is
       used above in :meth:`_SubscriberAPI.list_subscriptions`.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type sub_pb: :class:`.pubsub_pb2.Subscription`
    :param sub_pb: A subscription returned from the API.

    :type topics: dict
    :param topics: A dictionary of topics to be used (and modified)
                   as new subscriptions are created bound to topics.

    :rtype: :class:`~google.cloud.pubsub.subscription.Subscription`
    :returns: The next subscription in the page.
    """
    resource = MessageToDict(sub_pb)
    return Subscription.from_api_repr(
        resource, iterator.client, topics=topics)
