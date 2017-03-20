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

"""Define API Topics."""

import base64
import json
import time

from google.cloud._helpers import _datetime_to_rfc3339
from google.cloud._helpers import _NOW
from google.cloud._helpers import _to_bytes
from google.cloud.exceptions import NotFound
from google.cloud.pubsub._helpers import topic_name_from_path
from google.cloud.pubsub.iam import Policy
from google.cloud.pubsub.subscription import Subscription


class Topic(object):
    """Topics are targets to which messages can be published.

    Subscribers then receive those messages.

    See:
    https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics

    :type name: str
    :param name: the name of the topic

    :type client: :class:`google.cloud.pubsub.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the topic (which requires a project).

    :type timestamp_messages: bool
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

        Example:  pull-mode subcription, default paramter values

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_subscription_defaults]
           :end-before: [END topic_subscription_defaults]

        Example:  pull-mode subcription, override ``ack_deadline`` default

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_subscription_ack90]
           :end-before: [END topic_subscription_ack90]

        Example:  push-mode subcription

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_subscription_push]
           :end-before: [END topic_subscription_push]

        :type name: str
        :param name: the name of the subscription

        :type ack_deadline: int
        :param ack_deadline: the deadline (in seconds) by which messages pulled
                             from the back-end must be acknowledged.

        :type push_endpoint: str
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end. If not set, the application must pull
                              messages.

        :rtype: :class:`Subscription`
        :returns: The subscription created with the passed in arguments.
        """
        return Subscription(name, self, ack_deadline=ack_deadline,
                            push_endpoint=push_endpoint)

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a topic given its API representation

        :type resource: dict
        :param resource: topic resource representation returned from the API

        :type client: :class:`google.cloud.pubsub.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the topic.

        :rtype: :class:`google.cloud.pubsub.topic.Topic`
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

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :rtype: :class:`google.cloud.pubsub.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def create(self, client=None):
        """API call:  create the topic via a PUT request

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/create

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_create]
           :end-before: [END topic_create]

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.
        """
        client = self._require_client(client)
        api = client.publisher_api
        api.topic_create(topic_path=self.full_name)

    def exists(self, client=None):
        """API call:  test for the existence of the topic via a GET request

        See
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/get

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_exists]
           :end-before: [END topic_exists]

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :rtype: bool
        :returns: Boolean indicating existence of the topic.
        """
        client = self._require_client(client)
        api = client.publisher_api

        try:
            api.topic_get(topic_path=self.full_name)
        except NotFound:
            return False
        else:
            return True

    def delete(self, client=None):
        """API call:  delete the topic via a DELETE request

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/delete

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_delete]
           :end-before: [END topic_delete]

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.
        """
        client = self._require_client(client)
        api = client.publisher_api
        api.topic_delete(topic_path=self.full_name)

    def _timestamp_message(self, attrs):
        """Add a timestamp to ``attrs``, if the topic is so configured.

        If ``attrs`` already has the key, do nothing.

        Helper method for ``publish``/``Batch.publish``.
        """
        if self.timestamp_messages and 'timestamp' not in attrs:
            attrs['timestamp'] = _datetime_to_rfc3339(_NOW())

    def publish(self, message, client=None, **attrs):
        """API call:  publish a message to a topic via a POST request

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/publish

        Example without message attributes:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_publish_simple_message]
           :end-before: [END topic_publish_simple_message]

        With message attributes:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_publish_message_with_attrs]
           :end-before: [END topic_publish_message_with_attrs]

        :type message: bytes
        :param message: the message payload

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :type attrs: dict (string -> string)
        :param attrs: key-value pairs to send as message attributes

        :rtype: str
        :returns: message ID assigned by the server to the published message
        """
        client = self._require_client(client)
        api = client.publisher_api

        self._timestamp_message(attrs)
        message_data = {'data': message, 'attributes': attrs}
        message_ids = api.topic_publish(self.full_name, [message_data])
        return message_ids[0]

    def batch(self, client=None, **kwargs):
        """Return a batch to use as a context manager.

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_batch]
           :end-before: [END topic_batch]

        .. note::

           The only API request happens during the ``__exit__()`` of the topic
           used as a context manager, and only if the block exits without
           raising an exception.

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :type kwargs: dict
        :param kwargs: Keyword arguments passed to the
                       :class:`~google.cloud.pubsub.topic.Batch` constructor.

        :rtype: :class:`Batch`
        :returns: A batch to use as a context manager.
        """
        client = self._require_client(client)
        return Batch(self, client, **kwargs)

    def list_subscriptions(self, page_size=None, page_token=None, client=None):
        """List subscriptions for the project associated with this client.

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics.subscriptions/list

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_list_subscriptions]
           :end-before: [END topic_list_subscriptions]

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of
                  :class:`~google.cloud.pubsub.subscription.Subscription`
                  accessible to the current topic.
        """
        client = self._require_client(client)
        api = client.publisher_api
        return api.topic_list_subscriptions(self, page_size, page_token)

    def get_iam_policy(self, client=None):
        """Fetch the IAM policy for the topic.

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/getIamPolicy

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_get_iam_policy]
           :end-before: [END topic_get_iam_policy]

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current batch.

        :rtype: :class:`google.cloud.pubsub.iam.Policy`
        :returns: policy created from the resource returned by the
                  ``getIamPolicy`` API request.
        """
        client = self._require_client(client)
        api = client.iam_policy_api
        resp = api.get_iam_policy(self.full_name)
        return Policy.from_api_repr(resp)

    def set_iam_policy(self, policy, client=None):
        """Update the IAM policy for the topic.

        See:
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/setIamPolicy

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_set_iam_policy]
           :end-before: [END topic_set_iam_policy]

        :type policy: :class:`google.cloud.pubsub.iam.Policy`
        :param policy: the new policy, typically fetched via
                       :meth:`get_iam_policy` and updated in place.

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current batch.

        :rtype: :class:`google.cloud.pubsub.iam.Policy`
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
        https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/testIamPermissions

        Example:

        .. literalinclude:: pubsub_snippets.py
           :start-after: [START topic_check_iam_permissions]
           :end-before: [END topic_check_iam_permissions]

        :type permissions: list of string
        :param permissions: list of permissions to be tested

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current batch.

        :rtype: sequence of string
        :returns: subset of ``permissions`` allowed by current IAM policy.
        """
        client = self._require_client(client)
        api = client.iam_policy_api
        return api.test_iam_permissions(
            self.full_name, list(permissions))


class Batch(object):
    """Context manager:  collect messages to publish via a single API call.

    Helper returned by :meth:Topic.batch

    :type topic: :class:`google.cloud.pubsub.topic.Topic`
    :param topic: the topic being published

    :param client: The client to use.
    :type client: :class:`google.cloud.pubsub.client.Client`

    :param max_interval: The maximum interval, in seconds, before the batch
                         will automatically commit. Note that this does not
                         run a background loop; it just checks when each
                         message is published. Therefore, this is intended
                         for situations where messages are published at
                         reasonably regular intervals. Defaults to infinity
                         (off).
    :type max_interval: float

    :param max_messages: The maximum number of messages to hold in the batch
                         before automatically commiting. Defaults to infinity
                         (off).
    :type max_messages: float

    :param max_size: The maximum size that the serialized messages can be
                     before automatically commiting. Defaults to 9 MB
                     (slightly less than the API limit).
    :type max_size: int
    """
    _INFINITY = float('inf')

    def __init__(self, topic, client, max_interval=_INFINITY,
                 max_messages=_INFINITY, max_size=1024 * 1024 * 9):
        self.topic = topic
        self.client = client
        self.messages = []
        self.message_ids = []

        # Set the autocommit rules. If the interval or number of messages
        # is exceeded, then the .publish() method will imply a commit.
        self._max_interval = max_interval
        self._max_messages = max_messages
        self._max_size = max_size

        # Set up the initial state, initializing messages, the starting
        # timestamp, etc.
        self._reset_state()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()

    def __iter__(self):
        return iter(self.message_ids)

    def _reset_state(self):
        """Reset the state of this batch."""

        del self.messages[:]
        self._start_timestamp = time.time()
        self._current_size = 0

    def publish(self, message, **attrs):
        """Emulate publishing a message, but save it.

        :type message: bytes
        :param message: the message payload

        :type attrs: dict (string -> string)
        :param attrs: key-value pairs to send as message attributes
        """
        self.topic._timestamp_message(attrs)

        # Append the message to the list of messages..
        item = {'attributes': attrs, 'data': message}
        self.messages.append(item)

        # Determine the approximate size of the message, and increment
        # the current batch size appropriately.
        encoded = base64.b64encode(_to_bytes(message))
        encoded += base64.b64encode(
            json.dumps(attrs, ensure_ascii=False).encode('utf8'),
        )
        self._current_size += len(encoded)

        # If too much time has elapsed since the first message
        # was added, autocommit.
        now = time.time()
        if now - self._start_timestamp > self._max_interval:
            self.commit()
            return

        # If the number of messages on the list is greater than the
        # maximum allowed, autocommit (with the batch's client).
        if len(self.messages) >= self._max_messages:
            self.commit()
            return

        # If we have reached the max size, autocommit.
        if self._current_size >= self._max_size:
            self.commit()
            return

    def commit(self, client=None):
        """Send saved messages as a single API call.

        :type client: :class:`~google.cloud.pubsub.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current batch.
        """
        if not self.messages:
            return

        if client is None:
            client = self.client
        api = client.publisher_api
        message_ids = api.topic_publish(self.topic.full_name, self.messages[:])
        self.message_ids.extend(message_ids)
        self._reset_state()
