# Copyright 2017, Google Inc. All rights reserved.
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
#
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/pubsub/v1/pubsub.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.pubsub.v1 Subscriber API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers

from google.cloud.pubsub_v1.gapic import subscriber_client_config
from google.cloud.pubsub_v1.proto import pubsub_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import duration_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-pubsub', ).version


class SubscriberClient(object):
    """
    The service that an application uses to manipulate subscriptions and to
    consume messages from a subscription via the ``Pull`` method.
    """

    SERVICE_ADDRESS = 'pubsub.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/pubsub', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary
    _INTERFACE_NAME = ('google.pubsub.v1.Subscriber')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project, )

    @classmethod
    def snapshot_path(cls, project, snapshot):
        """Returns a fully-qualified snapshot resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/snapshots/{snapshot}',
            project=project,
            snapshot=snapshot, )

    @classmethod
    def subscription_path(cls, project, subscription):
        """Returns a fully-qualified subscription resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/subscriptions/{subscription}',
            project=project,
            subscription=subscription, )

    @classmethod
    def topic_path(cls, project, topic):
        """Returns a fully-qualified topic resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/topics/{topic}',
            project=project,
            topic=topic, )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=subscriber_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. If specified, then the ``credentials``
                argument is ignored.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict):
                A dictionary of call options for each method. If not specified
                the default configuration is used. Generally, you only need
                to set this if you're developing your own client library.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        if channel is not None and credentials is not None:
            raise ValueError(
                'channel and credentials arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__))

        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES)

        self.iam_policy_stub = (iam_policy_pb2.IAMPolicyStub(channel))
        self.subscriber_stub = (pubsub_pb2.SubscriberStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)

        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        interface_config = client_config['interfaces'][self._INTERFACE_NAME]
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            interface_config)

        self._create_subscription = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.CreateSubscription,
            default_retry=method_configs['CreateSubscription'].retry,
            default_timeout=method_configs['CreateSubscription'].timeout,
            client_info=client_info)
        self._get_subscription = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.GetSubscription,
            default_retry=method_configs['GetSubscription'].retry,
            default_timeout=method_configs['GetSubscription'].timeout,
            client_info=client_info)
        self._update_subscription = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.UpdateSubscription,
            default_retry=method_configs['UpdateSubscription'].retry,
            default_timeout=method_configs['UpdateSubscription'].timeout,
            client_info=client_info)
        self._list_subscriptions = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.ListSubscriptions,
            default_retry=method_configs['ListSubscriptions'].retry,
            default_timeout=method_configs['ListSubscriptions'].timeout,
            client_info=client_info)
        self._delete_subscription = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.DeleteSubscription,
            default_retry=method_configs['DeleteSubscription'].retry,
            default_timeout=method_configs['DeleteSubscription'].timeout,
            client_info=client_info)
        self._modify_ack_deadline = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.ModifyAckDeadline,
            default_retry=method_configs['ModifyAckDeadline'].retry,
            default_timeout=method_configs['ModifyAckDeadline'].timeout,
            client_info=client_info)
        self._acknowledge = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.Acknowledge,
            default_retry=method_configs['Acknowledge'].retry,
            default_timeout=method_configs['Acknowledge'].timeout,
            client_info=client_info)
        self._pull = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.Pull,
            default_retry=method_configs['Pull'].retry,
            default_timeout=method_configs['Pull'].timeout,
            client_info=client_info)
        self._streaming_pull = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.StreamingPull,
            default_retry=method_configs['StreamingPull'].retry,
            default_timeout=method_configs['StreamingPull'].timeout,
            client_info=client_info)
        self._modify_push_config = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.ModifyPushConfig,
            default_retry=method_configs['ModifyPushConfig'].retry,
            default_timeout=method_configs['ModifyPushConfig'].timeout,
            client_info=client_info)
        self._list_snapshots = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.ListSnapshots,
            default_retry=method_configs['ListSnapshots'].retry,
            default_timeout=method_configs['ListSnapshots'].timeout,
            client_info=client_info)
        self._create_snapshot = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.CreateSnapshot,
            default_retry=method_configs['CreateSnapshot'].retry,
            default_timeout=method_configs['CreateSnapshot'].timeout,
            client_info=client_info)
        self._update_snapshot = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.UpdateSnapshot,
            default_retry=method_configs['UpdateSnapshot'].retry,
            default_timeout=method_configs['UpdateSnapshot'].timeout,
            client_info=client_info)
        self._delete_snapshot = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.DeleteSnapshot,
            default_retry=method_configs['DeleteSnapshot'].retry,
            default_timeout=method_configs['DeleteSnapshot'].timeout,
            client_info=client_info)
        self._seek = google.api_core.gapic_v1.method.wrap_method(
            self.subscriber_stub.Seek,
            default_retry=method_configs['Seek'].retry,
            default_timeout=method_configs['Seek'].timeout,
            client_info=client_info)
        self._set_iam_policy = google.api_core.gapic_v1.method.wrap_method(
            self.iam_policy_stub.SetIamPolicy,
            default_retry=method_configs['SetIamPolicy'].retry,
            default_timeout=method_configs['SetIamPolicy'].timeout,
            client_info=client_info)
        self._get_iam_policy = google.api_core.gapic_v1.method.wrap_method(
            self.iam_policy_stub.GetIamPolicy,
            default_retry=method_configs['GetIamPolicy'].retry,
            default_timeout=method_configs['GetIamPolicy'].timeout,
            client_info=client_info)
        self._test_iam_permissions = google.api_core.gapic_v1.method.wrap_method(
            self.iam_policy_stub.TestIamPermissions,
            default_retry=method_configs['TestIamPermissions'].retry,
            default_timeout=method_configs['TestIamPermissions'].timeout,
            client_info=client_info)

    # Service calls
    def create_subscription(self,
                            name,
                            topic,
                            push_config=None,
                            ack_deadline_seconds=None,
                            retain_acked_messages=None,
                            message_retention_duration=None,
                            labels=None,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Creates a subscription to a given topic.
        If the subscription already exists, returns ``ALREADY_EXISTS``.
        If the corresponding topic doesn't exist, returns ``NOT_FOUND``.

        If the name is not provided in the request, the server will assign a random
        name for this subscription on the same project as the topic, conforming
        to the
        `resource name format <https://cloud.google.com/pubsub/docs/overview#names>`_.
        The generated name is populated in the returned Subscription object.
        Note that for REST API requests, you must specify a name in the request.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> name = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> response = client.create_subscription(name, topic)

        Args:
            name (str): The name of the subscription. It must have the format
                ``\"projects/{project}/subscriptions/{subscription}\"``. ``{subscription}`` must
                start with a letter, and contain only letters (``[A-Za-z]``), numbers
                (``[0-9]``), dashes (``-``), underscores (``_``), periods (``.``), tildes (``~``),
                plus (``+``) or percent signs (``%``). It must be between 3 and 255 characters
                in length, and it must not start with ``\"goog\"``.
            topic (str): The name of the topic from which this subscription is receiving messages.
                Format is ``projects/{project}/topics/{topic}``.
                The value of this field will be ``_deleted-topic_`` if the topic has been
                deleted.
            push_config (Union[dict, ~google.cloud.pubsub_v1.types.PushConfig]): If push delivery is used with this subscription, this field is
                used to configure it. An empty ``pushConfig`` signifies that the subscriber
                will pull and ack messages using API methods.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.PushConfig`
            ack_deadline_seconds (int): This value is the maximum time after a subscriber receives a message
                before the subscriber should acknowledge the message. After message
                delivery but before the ack deadline expires and before the message is
                acknowledged, it is an outstanding message and will not be delivered
                again during that time (on a best-effort basis).

                For pull subscriptions, this value is used as the initial value for the ack
                deadline. To override this value for a given message, call
                ``ModifyAckDeadline`` with the corresponding ``ack_id`` if using
                pull.
                The minimum custom deadline you can specify is 10 seconds.
                The maximum custom deadline you can specify is 600 seconds (10 minutes).
                If this parameter is 0, a default value of 10 seconds is used.

                For push delivery, this value is also used to set the request timeout for
                the call to the push endpoint.

                If the subscriber never acknowledges the message, the Pub/Sub
                system will eventually redeliver the message.
            retain_acked_messages (bool): Indicates whether to retain acknowledged messages. If true, then
                messages are not expunged from the subscription's backlog, even if they are
                acknowledged, until they fall out of the ``message_retention_duration``
                window.
            message_retention_duration (Union[dict, ~google.cloud.pubsub_v1.types.Duration]): How long to retain unacknowledged messages in the subscription's backlog,
                from the moment a message is published.
                If ``retain_acked_messages`` is true, then this also configures the retention
                of acknowledged messages, and thus configures how far back in time a ``Seek``
                can be done. Defaults to 7 days. Cannot be more than 7 days or less than 10
                minutes.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Duration`
            labels (dict[str -> str]): User labels.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.Subscription(
            name=name,
            topic=topic,
            push_config=push_config,
            ack_deadline_seconds=ack_deadline_seconds,
            retain_acked_messages=retain_acked_messages,
            message_retention_duration=message_retention_duration,
            labels=labels)
        return self._create_subscription(request, retry=retry, timeout=timeout)

    def get_subscription(self,
                         subscription,
                         retry=google.api_core.gapic_v1.method.DEFAULT,
                         timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Gets the configuration details of a subscription.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> response = client.get_subscription(subscription)

        Args:
            subscription (str): The name of the subscription to get.
                Format is ``projects/{project}/subscriptions/{sub}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.GetSubscriptionRequest(subscription=subscription)
        return self._get_subscription(request, retry=retry, timeout=timeout)

    def update_subscription(self,
                            subscription,
                            update_mask,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Updates an existing subscription. Note that certain properties of a
        subscription, such as its topic, are not modifiable.
        NOTE:  The style guide requires body: \"subscription\" instead of body: \"*\".
        Keeping the latter for internal consistency in V1, however it should be
        corrected in V2.  See
        https://cloud.google.com/apis/design/standard_methods#update for details.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = {}
            >>> update_mask = {}
            >>>
            >>> response = client.update_subscription(subscription, update_mask)

        Args:
            subscription (Union[dict, ~google.cloud.pubsub_v1.types.Subscription]): The updated subscription object.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Subscription`
            update_mask (Union[dict, ~google.cloud.pubsub_v1.types.FieldMask]): Indicates which fields in the provided subscription to update.
                Must be specified and non-empty.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.UpdateSubscriptionRequest(
            subscription=subscription, update_mask=update_mask)
        return self._update_subscription(request, retry=retry, timeout=timeout)

    def list_subscriptions(self,
                           project,
                           page_size=None,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Lists matching subscriptions.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> project = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_subscriptions(project):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_subscriptions(project, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project (str): The name of the cloud project that subscriptions belong to.
                Format is ``projects/{project}``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.pubsub_v1.types.Subscription` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.ListSubscriptionsRequest(
            project=project, page_size=page_size)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_subscriptions, retry=retry, timeout=timeout),
            request=request,
            items_field='subscriptions',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def delete_subscription(self,
                            subscription,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Deletes an existing subscription. All messages retained in the subscription
        are immediately dropped. Calls to ``Pull`` after deletion will return
        ``NOT_FOUND``. After a subscription is deleted, a new one may be created with
        the same name, but the new one has no association with the old
        subscription or its topic unless the same topic is specified.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> client.delete_subscription(subscription)

        Args:
            subscription (str): The subscription to delete.
                Format is ``projects/{project}/subscriptions/{sub}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.DeleteSubscriptionRequest(
            subscription=subscription)
        self._delete_subscription(request, retry=retry, timeout=timeout)

    def modify_ack_deadline(self,
                            subscription,
                            ack_ids,
                            ack_deadline_seconds,
                            retry=google.api_core.gapic_v1.method.DEFAULT,
                            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Modifies the ack deadline for a specific message. This method is useful
        to indicate that more time is needed to process a message by the
        subscriber, or to make the message available for redelivery if the
        processing was interrupted. Note that this does not modify the
        subscription-level ``ackDeadlineSeconds`` used for subsequent messages.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>> ack_ids = []
            >>> ack_deadline_seconds = 0
            >>>
            >>> client.modify_ack_deadline(subscription, ack_ids, ack_deadline_seconds)

        Args:
            subscription (str): The name of the subscription.
                Format is ``projects/{project}/subscriptions/{sub}``.
            ack_ids (list[str]): List of acknowledgment IDs.
            ack_deadline_seconds (int): The new ack deadline with respect to the time this request was sent to
                the Pub/Sub system. For example, if the value is 10, the new
                ack deadline will expire 10 seconds after the ``ModifyAckDeadline`` call
                was made. Specifying zero may immediately make the message available for
                another pull request.
                The minimum deadline you can specify is 0 seconds.
                The maximum deadline you can specify is 600 seconds (10 minutes).
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.ModifyAckDeadlineRequest(
            subscription=subscription,
            ack_ids=ack_ids,
            ack_deadline_seconds=ack_deadline_seconds)
        self._modify_ack_deadline(request, retry=retry, timeout=timeout)

    def acknowledge(self,
                    subscription,
                    ack_ids,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Acknowledges the messages associated with the ``ack_ids`` in the
        ``AcknowledgeRequest``. The Pub/Sub system can remove the relevant messages
        from the subscription.

        Acknowledging a message whose ack deadline has expired may succeed,
        but such a message may be redelivered later. Acknowledging a message more
        than once will not result in an error.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>> ack_ids = []
            >>>
            >>> client.acknowledge(subscription, ack_ids)

        Args:
            subscription (str): The subscription whose message is being acknowledged.
                Format is ``projects/{project}/subscriptions/{sub}``.
            ack_ids (list[str]): The acknowledgment ID for the messages being acknowledged that was returned
                by the Pub/Sub system in the ``Pull`` response. Must not be empty.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.AcknowledgeRequest(
            subscription=subscription, ack_ids=ack_ids)
        self._acknowledge(request, retry=retry, timeout=timeout)

    def pull(self,
             subscription,
             max_messages,
             return_immediately=None,
             retry=google.api_core.gapic_v1.method.DEFAULT,
             timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Pulls messages from the server. Returns an empty list if there are no
        messages available in the backlog. The server may return ``UNAVAILABLE`` if
        there are too many concurrent pull requests pending for the given
        subscription.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>> max_messages = 0
            >>>
            >>> response = client.pull(subscription, max_messages)

        Args:
            subscription (str): The subscription from which messages should be pulled.
                Format is ``projects/{project}/subscriptions/{sub}``.
            max_messages (int): The maximum number of messages returned for this request. The Pub/Sub
                system may return fewer than the number specified.
            return_immediately (bool): If this field set to true, the system will respond immediately even if
                it there are no messages available to return in the ``Pull`` response.
                Otherwise, the system may wait (for a bounded amount of time) until at
                least one message is available, rather than returning no messages. The
                client may cancel the request if it does not wish to wait any longer for
                the response.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.PullResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.PullRequest(
            subscription=subscription,
            max_messages=max_messages,
            return_immediately=return_immediately)
        return self._pull(request, retry=retry, timeout=timeout)

    def streaming_pull(self,
                       requests,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        (EXPERIMENTAL) StreamingPull is an experimental feature. This RPC will
        respond with UNIMPLEMENTED errors unless you have been invited to test
        this feature. Contact cloud-pubsub@google.com with any questions.

        Establishes a stream with the server, which sends messages down to the
        client. The client streams acknowledgements and ack deadline modifications
        back to the server. The server will close the stream and return the status
        on any error. The server may close the stream with status ``OK`` to reassign
        server-side resources, in which case, the client should re-establish the
        stream. ``UNAVAILABLE`` may also be returned in the case of a transient error
        (e.g., a server restart). These should also be retried by the client. Flow
        control can be achieved by configuring the underlying RPC channel.

        EXPERIMENTAL: This method interface might change in the future.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>> stream_ack_deadline_seconds = 0
            >>> request = {'subscription': subscription, 'stream_ack_deadline_seconds': stream_ack_deadline_seconds}
            >>>
            >>> requests = [request]
            >>> for element in client.streaming_pull(requests):
            ...     # process element
            ...     pass

        Args:
            requests (iterator[dict|google.cloud.pubsub_v1.proto.pubsub_pb2.StreamingPullRequest]): The input objects. If a dict is provided, it must be of the
                same form as the protobuf message :class:`~google.cloud.pubsub_v1.types.StreamingPullRequest`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            Iterable[~google.cloud.pubsub_v1.types.StreamingPullResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        return self._streaming_pull(requests, retry=retry, timeout=timeout)

    def modify_push_config(self,
                           subscription,
                           push_config,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Modifies the ``PushConfig`` for a specified subscription.

        This may be used to change a push subscription to a pull one (signified by
        an empty ``PushConfig``) or vice versa, or change the endpoint URL and other
        attributes of a push subscription. Messages will accumulate for delivery
        continuously through the call regardless of changes to the ``PushConfig``.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>> push_config = {}
            >>>
            >>> client.modify_push_config(subscription, push_config)

        Args:
            subscription (str): The name of the subscription.
                Format is ``projects/{project}/subscriptions/{sub}``.
            push_config (Union[dict, ~google.cloud.pubsub_v1.types.PushConfig]): The push configuration for future deliveries.

                An empty ``pushConfig`` indicates that the Pub/Sub system should
                stop pushing messages from the given subscription and allow
                messages to be pulled and acknowledged - effectively pausing
                the subscription if ``Pull`` is not called.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.PushConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.ModifyPushConfigRequest(
            subscription=subscription, push_config=push_config)
        self._modify_push_config(request, retry=retry, timeout=timeout)

    def list_snapshots(self,
                       project,
                       page_size=None,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Lists the existing snapshots.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> project = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_snapshots(project):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_snapshots(project, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project (str): The name of the cloud project that snapshots belong to.
                Format is ``projects/{project}``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.pubsub_v1.types.Snapshot` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.ListSnapshotsRequest(
            project=project, page_size=page_size)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_snapshots, retry=retry, timeout=timeout),
            request=request,
            items_field='snapshots',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def create_snapshot(self,
                        name,
                        subscription,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Creates a snapshot from the requested subscription.
        If the snapshot already exists, returns ``ALREADY_EXISTS``.
        If the requested subscription doesn't exist, returns ``NOT_FOUND``.

        If the name is not provided in the request, the server will assign a random
        name for this snapshot on the same project as the subscription, conforming
        to the
        `resource name format <https://cloud.google.com/pubsub/docs/overview#names>`_.
        The generated name is populated in the returned Snapshot object.
        Note that for REST API requests, you must specify a name in the request.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> name = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> response = client.create_snapshot(name, subscription)

        Args:
            name (str): Optional user-provided name for this snapshot.
                If the name is not provided in the request, the server will assign a random
                name for this snapshot on the same project as the subscription.
                Note that for REST API requests, you must specify a name.
                Format is ``projects/{project}/snapshots/{snap}``.
            subscription (str): The subscription whose backlog the snapshot retains.
                Specifically, the created snapshot is guaranteed to retain:

                * The existing backlog on the subscription. More precisely, this is
                  defined as the messages in the subscription's backlog that are
                  unacknowledged upon the successful completion of the
                  `CreateSnapshot` request; as well as:
                * Any messages published to the subscription's topic following the
                  successful completion of the CreateSnapshot request.

                Format is ``projects/{project}/subscriptions/{sub}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Snapshot` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.CreateSnapshotRequest(
            name=name, subscription=subscription)
        return self._create_snapshot(request, retry=retry, timeout=timeout)

    def update_snapshot(self,
                        snapshot,
                        update_mask,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Updates an existing snapshot. Note that certain properties of a snapshot
        are not modifiable.
        NOTE:  The style guide requires body: \"snapshot\" instead of body: \"*\".
        Keeping the latter for internal consistency in V1, however it should be
        corrected in V2.  See
        https://cloud.google.com/apis/design/standard_methods#update for details.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> snapshot = {}
            >>> update_mask = {}
            >>>
            >>> response = client.update_snapshot(snapshot, update_mask)

        Args:
            snapshot (Union[dict, ~google.cloud.pubsub_v1.types.Snapshot]): The updated snpashot object.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Snapshot`
            update_mask (Union[dict, ~google.cloud.pubsub_v1.types.FieldMask]): Indicates which fields in the provided snapshot to update.
                Must be specified and non-empty.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Snapshot` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.UpdateSnapshotRequest(
            snapshot=snapshot, update_mask=update_mask)
        return self._update_snapshot(request, retry=retry, timeout=timeout)

    def delete_snapshot(self,
                        snapshot,
                        retry=google.api_core.gapic_v1.method.DEFAULT,
                        timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Removes an existing snapshot. All messages retained in the snapshot
        are immediately dropped. After a snapshot is deleted, a new one may be
        created with the same name, but the new one has no association with the old
        snapshot or its subscription, unless the same subscription is specified.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> snapshot = client.snapshot_path('[PROJECT]', '[SNAPSHOT]')
            >>>
            >>> client.delete_snapshot(snapshot)

        Args:
            snapshot (str): The name of the snapshot to delete.
                Format is ``projects/{project}/snapshots/{snap}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.DeleteSnapshotRequest(snapshot=snapshot)
        self._delete_snapshot(request, retry=retry, timeout=timeout)

    def seek(self,
             subscription,
             time=None,
             snapshot=None,
             retry=google.api_core.gapic_v1.method.DEFAULT,
             timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Seeks an existing subscription to a point in time or to a given snapshot,
        whichever is provided in the request.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> response = client.seek(subscription)

        Args:
            subscription (str): The subscription to affect.
            time (Union[dict, ~google.cloud.pubsub_v1.types.Timestamp]): The time to seek to.
                Messages retained in the subscription that were published before this
                time are marked as acknowledged, and messages retained in the
                subscription that were published after this time are marked as
                unacknowledged. Note that this operation affects only those messages
                retained in the subscription (configured by the combination of
                ``message_retention_duration`` and ``retain_acked_messages``). For example,
                if ``time`` corresponds to a point before the message retention
                window (or to a point before the system's notion of the subscription
                creation time), only retained messages will be marked as unacknowledged,
                and already-expunged messages will not be restored.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Timestamp`
            snapshot (str): The snapshot to seek to. The snapshot's topic must be the same as that of
                the provided subscription.
                Format is ``projects/{project}/snapshots/{snap}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.SeekResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            time=time,
            snapshot=snapshot, )

        request = pubsub_pb2.SeekRequest(
            subscription=subscription, time=time, snapshot=snapshot)
        return self._seek(request, retry=retry, timeout=timeout)

    def set_iam_policy(self,
                       resource,
                       policy,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the access control policy on the specified resource. Replaces any
        existing policy.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.pubsub_v1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The size of
                the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy)
        return self._set_iam_policy(request, retry=retry, timeout=timeout)

    def get_iam_policy(self,
                       resource,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does not have a policy
        set.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        return self._get_iam_policy(request, retry=retry, timeout=timeout)

    def test_iam_permissions(self,
                             resource,
                             permissions,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns permissions that a caller has on the specified resource.
        If the resource does not exist, this will return an empty set of
        permissions, not a NOT_FOUND error.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see
                `IAM Overview <https://cloud.google.com/iam/docs/overview#permissions>`_.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions)
        return self._test_iam_permissions(
            request, retry=retry, timeout=timeout)
