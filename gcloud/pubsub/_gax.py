# Copyright 2016 Google Inc. All rights reserved.
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

# pylint: disable=import-error
from google.gax import CallOptions
from google.gax import INITIAL_PAGE
from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.pubsub.v1.pubsub_pb2 import PubsubMessage
from google.pubsub.v1.pubsub_pb2 import PushConfig
from grpc.beta.interfaces import StatusCode
# pylint: enable=import-error

from gcloud.exceptions import Conflict
from gcloud.exceptions import NotFound
from gcloud._helpers import _to_bytes


def _build_paging_options(page_token=None):
    """Helper for :meth:'_PublisherAPI.list_topics' et aliae."""
    if page_token is None:
        page_token = INITIAL_PAGE
    options = {'page_token': page_token}
    return CallOptions(**options)


class _PublisherAPI(object):
    """Helper mapping publisher-related APIs.

    :type gax_api: :class:`google.pubsub.v1.publisher_api.PublisherApi`
    :param gax_api: API object used to make GAX requests.
    """
    def __init__(self, gax_api):
        self._gax_api = gax_api

    def list_topics(self, project, page_size=0, page_token=None):
        """List topics for the project associated with this API.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/list

        :type project: string
        :param project: project ID

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: tuple, (list, str)
        :returns: list of ``Topic`` resource dicts, plus a
                  "next page token" string:  if not None, indicates that
                  more topics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        options = _build_paging_options(page_token)
        path = 'projects/%s' % (project,)
        page_iter = self._gax_api.list_topics(
            path, page_size=page_size, options=options)
        topics = [{'name': topic_pb.name} for topic_pb in page_iter.next()]
        token = page_iter.page_token or None
        return topics, token

    def topic_create(self, topic_path):
        """API call:  create a topic

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/create

        :type topic_path: string
        :param topic_path: fully-qualified path of the new topic, in format
                            ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :rtype: dict
        :returns: ``Topic`` resource returned from the API.
        :raises: :exc:`gcloud.exceptions.Conflict` if the topic already
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
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/get

        :type topic_path: string
        :param topic_path: fully-qualified path of the topic, in format
                        ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :rtype: dict
        :returns: ``Topic`` resource returned from the API.
        :raises: :exc:`gcloud.exceptions.NotFound` if the topic does not
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
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/create

        :type topic_path: string
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
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/publish

        :type topic_path: string
        :param topic_path: fully-qualified path of the topic, in format
                            ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type messages: list of dict
        :param messages: messages to be published.

        :rtype: list of string
        :returns: list of opaque IDs for published messages.
        :raises: :exc:`gcloud.exceptions.NotFound` if the topic does not
                    exist
        """
        options = CallOptions(is_bundling=False)
        message_pbs = [_message_pb_from_dict(message)
                       for message in messages]
        try:
            result = self._gax_api.publish(topic_path, message_pbs,
                                           options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(topic_path)
            raise
        return result.message_ids

    def topic_list_subscriptions(self, topic_path, page_size=0,
                                 page_token=None):
        """API call:  list subscriptions bound to a topic

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics.subscriptions/list

        :type topic_path: string
        :param topic_path: fully-qualified path of the topic, in format
                            ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type page_size: int
        :param page_size: maximum number of subscriptions to return, If not
                          passed, defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of subscriptions.
                           If not passed, the API will return the first page
                           of subscriptions.

        :rtype: list of strings
        :returns: fully-qualified names of subscriptions for the supplied
                topic.
        :raises: :exc:`gcloud.exceptions.NotFound` if the topic does not
                    exist
        """
        options = _build_paging_options(page_token)
        try:
            page_iter = self._gax_api.list_topic_subscriptions(
                topic_path, page_size=page_size, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(topic_path)
            raise
        subs = page_iter.next()
        token = page_iter.page_token or None
        return subs, token


class _SubscriberAPI(object):
    """Helper mapping subscriber-related APIs.

    :type gax_api: :class:`google.pubsub.v1.publisher_api.SubscriberApi`
    :param gax_api: API object used to make GAX requests.
    """
    def __init__(self, gax_api):
        self._gax_api = gax_api

    def list_subscriptions(self, project, page_size=0, page_token=None):
        """List subscriptions for the project associated with this API.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/list

        :type project: string
        :param project: project ID

        :type page_size: int
        :param page_size: maximum number of subscriptions to return, If not
                          passed, defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of subscriptions.
                           If not passed, the API will return the first page
                           of subscriptions.

        :rtype: tuple, (list, str)
        :returns: list of ``Subscription`` resource dicts, plus a
                  "next page token" string:  if not None, indicates that
                  more topics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        options = _build_paging_options(page_token)
        path = 'projects/%s' % (project,)
        page_iter = self._gax_api.list_subscriptions(
            path, page_size=page_size, options=options)
        subscriptions = [_subscription_pb_to_mapping(sub_pb)
                         for sub_pb in page_iter.next()]
        token = page_iter.page_token or None
        return subscriptions, token

    def subscription_create(self, subscription_path, topic_path,
                            ack_deadline=None, push_endpoint=None):
        """API call:  create a subscription

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/create

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type topic_path: string
        :param topic_path: the fully-qualified path of the topic being
                           subscribed, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type ack_deadline: int, or ``NoneType``
        :param ack_deadline: the deadline (in seconds) by which messages pulled
                             from the back-end must be acknowledged.

        :type push_endpoint: string, or ``NoneType``
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end.  If not set, the application must pull
                              messages.

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
                subscription_path, topic_path, push_config, ack_deadline)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.FAILED_PRECONDITION:
                raise Conflict(topic_path)
            raise
        return _subscription_pb_to_mapping(sub_pb)

    def subscription_get(self, subscription_path):
        """API call:  retrieve a subscription

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/get

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the subscription,
                                  in format
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
        return _subscription_pb_to_mapping(sub_pb)

    def subscription_delete(self, subscription_path):
        """API call:  delete a subscription

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/delete

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the subscription,
                                  in format
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
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type push_endpoint: string, or ``NoneType``
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end.  If not set, the application must pull
                              messages.
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
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type return_immediately: boolean
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
                subscription_path, max_messages, return_immediately)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(subscription_path)
            raise
        return [_received_message_pb_to_mapping(rmpb)
                for rmpb in response_pb.received_messages]

    def subscription_acknowledge(self, subscription_path, ack_ids):
        """API call:  acknowledge retrieved messages

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
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
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyAckDeadline

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
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


def _message_pb_from_dict(message):
    """Helper for :meth:`_PublisherAPI.topic_publish`."""
    return PubsubMessage(data=_to_bytes(message['data']),
                         attributes=message['attributes'])


def _subscription_pb_to_mapping(sub_pb):
    """Helper for :meth:`list_subscriptions`, et aliae

    Ideally, would use a function from :mod:`protobuf.json_format`, but
    the right one isn't public.  See:
    https://github.com/google/protobuf/issues/1351
    """
    mapping = {
        'name': sub_pb.name,
        'topic': sub_pb.topic,
        'ackDeadlineSeconds': sub_pb.ack_deadline_seconds,
    }
    if sub_pb.push_config.push_endpoint != '':
        mapping['pushConfig'] = {
            'pushEndpoint': sub_pb.push_config.push_endpoint,
        }
    return mapping


def _message_pb_to_mapping(message_pb):
    """Helper for :meth:`pull`, et aliae

    Ideally, would use a function from :mod:`protobuf.json_format`, but
    the right one isn't public.  See:
    https://github.com/google/protobuf/issues/1351
    """
    return {
        'messageId': message_pb.message_id,
        'data': message_pb.data,
        'attributes': message_pb.attributes,
    }


def _received_message_pb_to_mapping(received_message_pb):
    """Helper for :meth:`pull`, et aliae

    Ideally, would use a function from :mod:`protobuf.json_format`, but
    the right one isn't public.  See:
    https://github.com/google/protobuf/issues/1351
    """
    return {
        'ackId': received_message_pb.ack_id,
        'message': _message_pb_to_mapping(
            received_message_pb.message),
    }
