# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.pubsub.v1 Subscriber API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.cloud.pubsub_v1.gapic import subscriber_client_config
from google.cloud.pubsub_v1.gapic.transports import subscriber_grpc_transport
from google.cloud.pubsub_v1.proto import pubsub_pb2
from google.cloud.pubsub_v1.proto import pubsub_pb2_grpc
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import iam_policy_pb2_grpc
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-pubsub").version


class SubscriberClient(object):
    """
    The service that an application uses to manipulate subscriptions and to
    consume messages from a subscription via the ``Pull`` method or by
    establishing a bi-directional stream using the ``StreamingPull`` method.
    """

    SERVICE_ADDRESS = "pubsub.googleapis.com:443"
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/pubsub",
    )

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.pubsub.v1.Subscriber"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SubscriberClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def snapshot_path(cls, project, snapshot):
        """Return a fully-qualified snapshot string."""
        return google.api_core.path_template.expand(
            "projects/{project}/snapshots/{snapshot}",
            project=project,
            snapshot=snapshot,
        )

    @classmethod
    def subscription_path(cls, project, subscription):
        """Return a fully-qualified subscription string."""
        return google.api_core.path_template.expand(
            "projects/{project}/subscriptions/{subscription}",
            project=project,
            subscription=subscription,
        )

    @classmethod
    def topic_path(cls, project, topic):
        """Return a fully-qualified topic string."""
        return google.api_core.path_template.expand(
            "projects/{project}/topics/{topic}", project=project, topic=topic
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.SubscriberGrpcTransport,
                    Callable[[~.Credentials, type], ~.SubscriberGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = subscriber_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=subscriber_grpc_transport.SubscriberGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = subscriber_grpc_transport.SubscriberGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def create_subscription(
        self,
        name,
        topic,
        push_config=None,
        ack_deadline_seconds=None,
        retain_acked_messages=None,
        message_retention_duration=None,
        labels=None,
        enable_message_ordering=None,
        expiration_policy=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a subscription to a given topic. See the resource name rules. If
        the subscription already exists, returns ``ALREADY_EXISTS``. If the
        corresponding topic doesn't exist, returns ``NOT_FOUND``.

        If the name is not provided in the request, the server will assign a
        random name for this subscription on the same project as the topic,
        conforming to the `resource name
        format <https://cloud.google.com/pubsub/docs/admin#resource_names>`__.
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
                `"projects/{project}/subscriptions/{subscription}"`. `{subscription}` must
                start with a letter, and contain only letters (`[A-Za-z]`), numbers
                (`[0-9]`), dashes (`-`), underscores (`_`), periods (`.`), tildes (`~`),
                plus (`+`) or percent signs (`%`). It must be between 3 and 255 characters
                in length, and it must not start with `"goog"`
            topic (str): The name of the topic from which this subscription is receiving
                messages. Format is ``projects/{project}/topics/{topic}``. The value of
                this field will be ``_deleted-topic_`` if the topic has been deleted.
            push_config (Union[dict, ~google.cloud.pubsub_v1.types.PushConfig]): If push delivery is used with this subscription, this field is used to
                configure it. An empty ``pushConfig`` signifies that the subscriber will
                pull and ack messages using API methods.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.PushConfig`
            ack_deadline_seconds (int): The approximate amount of time (on a best-effort basis) Pub/Sub waits
                for the subscriber to acknowledge receipt before resending the message.
                In the interval after the message is delivered and before it is
                acknowledged, it is considered to be outstanding. During that time
                period, the message will not be redelivered (on a best-effort basis).

                For pull subscriptions, this value is used as the initial value for the
                ack deadline. To override this value for a given message, call
                ``ModifyAckDeadline`` with the corresponding ``ack_id`` if using
                non-streaming pull or send the ``ack_id`` in a
                ``StreamingModifyAckDeadlineRequest`` if using streaming pull. The
                minimum custom deadline you can specify is 10 seconds. The maximum
                custom deadline you can specify is 600 seconds (10 minutes). If this
                parameter is 0, a default value of 10 seconds is used.

                For push delivery, this value is also used to set the request timeout
                for the call to the push endpoint.

                If the subscriber never acknowledges the message, the Pub/Sub system
                will eventually redeliver the message.
            retain_acked_messages (bool): Indicates whether to retain acknowledged messages. If true, then
                messages are not expunged from the subscription's backlog, even if they
                are acknowledged, until they fall out of the
                ``message_retention_duration`` window. This must be true if you would
                like to Seek to a timestamp.
            message_retention_duration (Union[dict, ~google.cloud.pubsub_v1.types.Duration]): How long to retain unacknowledged messages in the subscription's
                backlog, from the moment a message is published. If
                ``retain_acked_messages`` is true, then this also configures the
                retention of acknowledged messages, and thus configures how far back in
                time a ``Seek`` can be done. Defaults to 7 days. Cannot be more than 7
                days or less than 10 minutes.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Duration`
            labels (dict[str -> str]): See <a href="https://cloud.google.com/pubsub/docs/labels"> Creating and
                managing labels</a>.
            enable_message_ordering (bool): If true, messages published with the same ``ordering_key`` in
                ``PubsubMessage`` will be delivered to the subscribers in the order in
                which they are received by the Pub/Sub system. Otherwise, they may be
                delivered in any order. EXPERIMENTAL: This feature is part of a closed
                alpha release. This API might be changed in backward-incompatible ways
                and is not recommended for production use. It is not subject to any SLA
                or deprecation policy.
            expiration_policy (Union[dict, ~google.cloud.pubsub_v1.types.ExpirationPolicy]): A policy that specifies the conditions for this subscription's
                expiration. A subscription is considered active as long as any connected
                subscriber is successfully consuming messages from the subscription or
                is issuing operations on the subscription. If ``expiration_policy`` is
                not set, a *default policy* with ``ttl`` of 31 days will be used. The
                minimum allowed value for ``expiration_policy.ttl`` is 1 day.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.ExpirationPolicy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_subscription,
                default_retry=self._method_configs["CreateSubscription"].retry,
                default_timeout=self._method_configs["CreateSubscription"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.Subscription(
            name=name,
            topic=topic,
            push_config=push_config,
            ack_deadline_seconds=ack_deadline_seconds,
            retain_acked_messages=retain_acked_messages,
            message_retention_duration=message_retention_duration,
            labels=labels,
            enable_message_ordering=enable_message_ordering,
            expiration_policy=expiration_policy,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_subscription(
        self,
        subscription,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            subscription (str): The name of the subscription to get. Format is
                ``projects/{project}/subscriptions/{sub}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_subscription,
                default_retry=self._method_configs["GetSubscription"].retry,
                default_timeout=self._method_configs["GetSubscription"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.GetSubscriptionRequest(subscription=subscription)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_subscription(
        self,
        subscription,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing subscription. Note that certain properties of a
        subscription, such as its topic, are not modifiable.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> ack_deadline_seconds = 42
            >>> subscription = {'ack_deadline_seconds': ack_deadline_seconds}
            >>> paths_element = 'ack_deadline_seconds'
            >>> paths = [paths_element]
            >>> update_mask = {'paths': paths}
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_subscription,
                default_retry=self._method_configs["UpdateSubscription"].retry,
                default_timeout=self._method_configs["UpdateSubscription"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.UpdateSubscriptionRequest(
            subscription=subscription, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription.name", subscription.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_subscriptions(
        self,
        project,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists matching subscriptions.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> project = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_subscriptions(project):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_subscriptions(project).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project (str): The name of the project in which to list subscriptions. Format is
                ``projects/{project-id}``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.GRPCIterator` instance.
            An iterable of :class:`~google.cloud.pubsub_v1.types.Subscription` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_subscriptions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_subscriptions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_subscriptions,
                default_retry=self._method_configs["ListSubscriptions"].retry,
                default_timeout=self._method_configs["ListSubscriptions"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ListSubscriptionsRequest(
            project=project, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project", project)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_subscriptions"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="subscriptions",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_subscription(
        self,
        subscription,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an existing subscription. All messages retained in the
        subscription are immediately dropped. Calls to ``Pull`` after deletion
        will return ``NOT_FOUND``. After a subscription is deleted, a new one
        may be created with the same name, but the new one has no association
        with the old subscription or its topic unless the same topic is
        specified.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> client.delete_subscription(subscription)

        Args:
            subscription (str): The subscription to delete. Format is
                ``projects/{project}/subscriptions/{sub}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_subscription,
                default_retry=self._method_configs["DeleteSubscription"].retry,
                default_timeout=self._method_configs["DeleteSubscription"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.DeleteSubscriptionRequest(subscription=subscription)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def modify_ack_deadline(
        self,
        subscription,
        ack_ids,
        ack_deadline_seconds,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            >>>
            >>> # TODO: Initialize `ack_ids`:
            >>> ack_ids = []
            >>>
            >>> # TODO: Initialize `ack_deadline_seconds`:
            >>> ack_deadline_seconds = 0
            >>>
            >>> client.modify_ack_deadline(subscription, ack_ids, ack_deadline_seconds)

        Args:
            subscription (str): The name of the subscription. Format is
                ``projects/{project}/subscriptions/{sub}``.
            ack_ids (list[str]): List of acknowledgment IDs.
            ack_deadline_seconds (int): The new ack deadline with respect to the time this request was sent to
                the Pub/Sub system. For example, if the value is 10, the new ack
                deadline will expire 10 seconds after the ``ModifyAckDeadline`` call was
                made. Specifying zero might immediately make the message available for
                delivery to another subscriber client. This typically results in an
                increase in the rate of message redeliveries (that is, duplicates). The
                minimum deadline you can specify is 0 seconds. The maximum deadline you
                can specify is 600 seconds (10 minutes).
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "modify_ack_deadline" not in self._inner_api_calls:
            self._inner_api_calls[
                "modify_ack_deadline"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.modify_ack_deadline,
                default_retry=self._method_configs["ModifyAckDeadline"].retry,
                default_timeout=self._method_configs["ModifyAckDeadline"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ModifyAckDeadlineRequest(
            subscription=subscription,
            ack_ids=ack_ids,
            ack_deadline_seconds=ack_deadline_seconds,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["modify_ack_deadline"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def acknowledge(
        self,
        subscription,
        ack_ids,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Acknowledges the messages associated with the ``ack_ids`` in the
        ``AcknowledgeRequest``. The Pub/Sub system can remove the relevant
        messages from the subscription.

        Acknowledging a message whose ack deadline has expired may succeed, but
        such a message may be redelivered later. Acknowledging a message more
        than once will not result in an error.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `ack_ids`:
            >>> ack_ids = []
            >>>
            >>> client.acknowledge(subscription, ack_ids)

        Args:
            subscription (str): The subscription whose message is being acknowledged. Format is
                ``projects/{project}/subscriptions/{sub}``.
            ack_ids (list[str]): The acknowledgment ID for the messages being acknowledged that was
                returned by the Pub/Sub system in the ``Pull`` response. Must not be
                empty.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "acknowledge" not in self._inner_api_calls:
            self._inner_api_calls[
                "acknowledge"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.acknowledge,
                default_retry=self._method_configs["Acknowledge"].retry,
                default_timeout=self._method_configs["Acknowledge"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.AcknowledgeRequest(
            subscription=subscription, ack_ids=ack_ids
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["acknowledge"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def pull(
        self,
        subscription,
        max_messages,
        return_immediately=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Pulls messages from the server. The server may return ``UNAVAILABLE`` if
        there are too many concurrent pull requests pending for the given
        subscription.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `max_messages`:
            >>> max_messages = 0
            >>>
            >>> response = client.pull(subscription, max_messages)

        Args:
            subscription (str): The subscription from which messages should be pulled. Format is
                ``projects/{project}/subscriptions/{sub}``.
            max_messages (int): The maximum number of messages returned for this request. The Pub/Sub
                system may return fewer than the number specified.
            return_immediately (bool): If this field set to true, the system will respond immediately even if
                it there are no messages available to return in the ``Pull`` response.
                Otherwise, the system may wait (for a bounded amount of time) until at
                least one message is available, rather than returning no messages.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.PullResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "pull" not in self._inner_api_calls:
            self._inner_api_calls["pull"] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.pull,
                default_retry=self._method_configs["Pull"].retry,
                default_timeout=self._method_configs["Pull"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.PullRequest(
            subscription=subscription,
            max_messages=max_messages,
            return_immediately=return_immediately,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["pull"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def streaming_pull(
        self,
        requests,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Establishes a stream with the server, which sends messages down to the
        client. The client streams acknowledgements and ack deadline
        modifications back to the server. The server will close the stream and
        return the status on any error. The server may close the stream with
        status ``UNAVAILABLE`` to reassign server-side resources, in which case,
        the client should re-establish the stream. Flow control can be achieved
        by configuring the underlying RPC channel.

        EXPERIMENTAL: This method interface might change in the future.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `stream_ack_deadline_seconds`:
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
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.pubsub_v1.types.StreamingPullResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "streaming_pull" not in self._inner_api_calls:
            self._inner_api_calls[
                "streaming_pull"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.streaming_pull,
                default_retry=self._method_configs["StreamingPull"].retry,
                default_timeout=self._method_configs["StreamingPull"].timeout,
                client_info=self._client_info,
            )

        return self._inner_api_calls["streaming_pull"](
            requests, retry=retry, timeout=timeout, metadata=metadata
        )

    def modify_push_config(
        self,
        subscription,
        push_config,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Modifies the ``PushConfig`` for a specified subscription.

        This may be used to change a push subscription to a pull one (signified
        by an empty ``PushConfig``) or vice versa, or change the endpoint URL
        and other attributes of a push subscription. Messages will accumulate
        for delivery continuously through the call regardless of changes to the
        ``PushConfig``.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> subscription = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `push_config`:
            >>> push_config = {}
            >>>
            >>> client.modify_push_config(subscription, push_config)

        Args:
            subscription (str): The name of the subscription. Format is
                ``projects/{project}/subscriptions/{sub}``.
            push_config (Union[dict, ~google.cloud.pubsub_v1.types.PushConfig]): The push configuration for future deliveries.

                An empty ``pushConfig`` indicates that the Pub/Sub system should stop
                pushing messages from the given subscription and allow messages to be
                pulled and acknowledged - effectively pausing the subscription if
                ``Pull`` or ``StreamingPull`` is not called.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.PushConfig`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "modify_push_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "modify_push_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.modify_push_config,
                default_retry=self._method_configs["ModifyPushConfig"].retry,
                default_timeout=self._method_configs["ModifyPushConfig"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ModifyPushConfigRequest(
            subscription=subscription, push_config=push_config
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["modify_push_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_snapshots(
        self,
        project,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the existing snapshots. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> project = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_snapshots(project):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_snapshots(project).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project (str): The name of the project in which to list snapshots. Format is
                ``projects/{project-id}``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.GRPCIterator` instance.
            An iterable of :class:`~google.cloud.pubsub_v1.types.Snapshot` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_snapshots" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_snapshots"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_snapshots,
                default_retry=self._method_configs["ListSnapshots"].retry,
                default_timeout=self._method_configs["ListSnapshots"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ListSnapshotsRequest(project=project, page_size=page_size)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project", project)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_snapshots"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="snapshots",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_snapshot(
        self,
        name,
        subscription,
        labels=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a snapshot from the requested subscription. Snapshots are used
        in Seek operations, which allow you to manage message acknowledgments in
        bulk. That is, you can set the acknowledgment state of messages in an
        existing subscription to the state captured by a snapshot. If the
        snapshot already exists, returns ``ALREADY_EXISTS``. If the requested
        subscription doesn't exist, returns ``NOT_FOUND``. If the backlog in the
        subscription is too old -- and the resulting snapshot would expire in
        less than 1 hour -- then ``FAILED_PRECONDITION`` is returned. See also
        the ``Snapshot.expire_time`` field. If the name is not provided in the
        request, the server will assign a random name for this snapshot on the
        same project as the subscription, conforming to the `resource name
        format <https://cloud.google.com/pubsub/docs/admin#resource_names>`__.
        The generated name is populated in the returned Snapshot object. Note
        that for REST API requests, you must specify a name in the request.

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
            name (str): Optional user-provided name for this snapshot. If the name is not
                provided in the request, the server will assign a random name for this
                snapshot on the same project as the subscription. Note that for REST API
                requests, you must specify a name. See the resource name rules. Format
                is ``projects/{project}/snapshots/{snap}``.
            subscription (str): The subscription whose backlog the snapshot retains. Specifically, the
                created snapshot is guaranteed to retain: (a) The existing backlog on
                the subscription. More precisely, this is defined as the messages in the
                subscription's backlog that are unacknowledged upon the successful
                completion of the ``CreateSnapshot`` request; as well as: (b) Any
                messages published to the subscription's topic following the successful
                completion of the CreateSnapshot request. Format is
                ``projects/{project}/subscriptions/{sub}``.
            labels (dict[str -> str]): See <a href="https://cloud.google.com/pubsub/docs/labels"> Creating and
                managing labels</a>.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Snapshot` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_snapshot,
                default_retry=self._method_configs["CreateSnapshot"].retry,
                default_timeout=self._method_configs["CreateSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.CreateSnapshotRequest(
            name=name, subscription=subscription, labels=labels
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_snapshot(
        self,
        snapshot,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing snapshot. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> seconds = 123456
            >>> expire_time = {'seconds': seconds}
            >>> snapshot = {'expire_time': expire_time}
            >>> paths_element = 'expire_time'
            >>> paths = [paths_element]
            >>> update_mask = {'paths': paths}
            >>>
            >>> response = client.update_snapshot(snapshot, update_mask)

        Args:
            snapshot (Union[dict, ~google.cloud.pubsub_v1.types.Snapshot]): The updated snapshot object.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Snapshot`
            update_mask (Union[dict, ~google.cloud.pubsub_v1.types.FieldMask]): Indicates which fields in the provided snapshot to update.
                Must be specified and non-empty.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Snapshot` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_snapshot,
                default_retry=self._method_configs["UpdateSnapshot"].retry,
                default_timeout=self._method_configs["UpdateSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.UpdateSnapshotRequest(
            snapshot=snapshot, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("snapshot.name", snapshot.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_snapshot(
        self,
        snapshot,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Removes an existing snapshot. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot.<br><br>
        When the snapshot is deleted, all messages retained in the snapshot
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
            snapshot (str): The name of the snapshot to delete. Format is
                ``projects/{project}/snapshots/{snap}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_snapshot,
                default_retry=self._method_configs["DeleteSnapshot"].retry,
                default_timeout=self._method_configs["DeleteSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.DeleteSnapshotRequest(snapshot=snapshot)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("snapshot", snapshot)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def seek(
        self,
        subscription,
        time=None,
        snapshot=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Seeks an existing subscription to a point in time or to a given snapshot,
        whichever is provided in the request. Snapshots are used in
        <a href="https://cloud.google.com/pubsub/docs/replay-overview">Seek</a>
        operations, which allow
        you to manage message acknowledgments in bulk. That is, you can set the
        acknowledgment state of messages in an existing subscription to the state
        captured by a snapshot. Note that both the subscription and the snapshot
        must be on the same topic.

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
            time (Union[dict, ~google.cloud.pubsub_v1.types.Timestamp]): The time to seek to. Messages retained in the subscription that were
                published before this time are marked as acknowledged, and messages
                retained in the subscription that were published after this time are
                marked as unacknowledged. Note that this operation affects only those
                messages retained in the subscription (configured by the combination of
                ``message_retention_duration`` and ``retain_acked_messages``). For
                example, if ``time`` corresponds to a point before the message retention
                window (or to a point before the system's notion of the subscription
                creation time), only retained messages will be marked as unacknowledged,
                and already-expunged messages will not be restored.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Timestamp`
            snapshot (str): The snapshot to seek to. The snapshot's topic must be the same as that
                of the provided subscription. Format is
                ``projects/{project}/snapshots/{snap}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.SeekResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "seek" not in self._inner_api_calls:
            self._inner_api_calls["seek"] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.seek,
                default_retry=self._method_configs["Seek"].retry,
                default_timeout=self._method_configs["Seek"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(time=time, snapshot=snapshot)

        request = pubsub_pb2.SeekRequest(
            subscription=subscription, time=time, snapshot=snapshot
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription", subscription)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["seek"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_iam_policy(
        self,
        resource,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the access control policy on the specified resource. Replaces any
        existing policy.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                See the operation documentation for the appropriate value for this field.
            policy (Union[dict, ~google.cloud.pubsub_v1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_iam_policy,
                default_retry=self._method_configs["SetIamPolicy"].retry,
                default_timeout=self._method_configs["SetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
                See the operation documentation for the appropriate value for this field.
            options_ (Union[dict, ~google.cloud.pubsub_v1.types.GetPolicyOptions]): OPTIONAL: A ``GetPolicyOptions`` object for specifying options to
                ``GetIamPolicy``. This field is only used by Cloud IAM.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.GetPolicyOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_iam_policy,
                default_retry=self._method_configs["GetIamPolicy"].retry,
                default_timeout=self._method_configs["GetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource, options=options_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns permissions that a caller has on the specified resource. If the
        resource does not exist, this will return an empty set of permissions,
        not a NOT\_FOUND error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for authorization
        checking. This operation may "fail open" without warning.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.SubscriberClient()
            >>>
            >>> resource = client.subscription_path('[PROJECT]', '[SUBSCRIPTION]')
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                See the operation documentation for the appropriate value for this field.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "test_iam_permissions" not in self._inner_api_calls:
            self._inner_api_calls[
                "test_iam_permissions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.test_iam_permissions,
                default_retry=self._method_configs["TestIamPermissions"].retry,
                default_timeout=self._method_configs["TestIamPermissions"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
