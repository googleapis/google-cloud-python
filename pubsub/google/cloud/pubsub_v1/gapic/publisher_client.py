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

"""Accesses the google.pubsub.v1 Publisher API."""

import collections
from copy import deepcopy
import functools
import pkg_resources
import six
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.path_template
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.pubsub_v1.gapic import publisher_client_config
from google.cloud.pubsub_v1.gapic.transports import publisher_grpc_transport
from google.cloud.pubsub_v1.proto import pubsub_pb2
from google.cloud.pubsub_v1.proto import pubsub_pb2_grpc
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import iam_policy_pb2_grpc
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-pubsub").version


# TODO: remove conditional import after Python 2 support is dropped
if six.PY3:
    from collections.abc import Mapping
else:
    from collections import Mapping


def _merge_dict(d1, d2):
    # Modifies d1 in-place to take values from d2
    # if the nested keys from d2 are present in d1.
    # https://stackoverflow.com/a/10704003/4488789
    for k, v2 in d2.items():
        v1 = d1.get(k)  # returns None if v1 has no such key
        if v1 is None:
            raise Exception("{} is not recognized by client_config".format(k))
        if isinstance(v1, Mapping) and isinstance(v2, Mapping):
            _merge_dict(v1, v2)
        else:
            d1[k] = v2
    return d1


class PublisherClient(object):
    """
    The service that an application uses to manipulate topics, and to send
    messages to a topic.
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
    _INTERFACE_NAME = "google.pubsub.v1.Publisher"

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
            PublisherClient: The constructed client.
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
            transport (Union[~.PublisherGrpcTransport,
                    Callable[[~.Credentials, type], ~.PublisherGrpcTransport]): A transport
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
            client_config (dict): A dictionary of call options for
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
        default_client_config = deepcopy(publisher_client_config.config)

        if client_config is None:
            client_config = default_client_config
        else:
            client_config = _merge_dict(default_client_config, client_config)

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
                    default_class=publisher_grpc_transport.PublisherGrpcTransport,
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
            self.transport = publisher_grpc_transport.PublisherGrpcTransport(
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
    def create_topic(
        self,
        name,
        labels=None,
        message_storage_policy=None,
        kms_key_name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates the given topic with the given name. See the resource name
        rules.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> name = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> response = client.create_topic(name)

        Args:
            name (str): The name of the topic. It must have the format
                `"projects/{project}/topics/{topic}"`. `{topic}` must start with a letter,
                and contain only letters (`[A-Za-z]`), numbers (`[0-9]`), dashes (`-`),
                underscores (`_`), periods (`.`), tildes (`~`), plus (`+`) or percent
                signs (`%`). It must be between 3 and 255 characters in length, and it
                must not start with `"goog"`.
            labels (dict[str -> str]): See <a href="https://cloud.google.com/pubsub/docs/labels"> Creating and
                managing labels</a>.
            message_storage_policy (Union[dict, ~google.cloud.pubsub_v1.types.MessageStoragePolicy]): Policy constraining the set of Google Cloud Platform regions where messages
                published to the topic may be stored. If not present, then no constraints
                are in effect.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.MessageStoragePolicy`
            kms_key_name (str): The resource name of the Cloud KMS CryptoKey to be used to protect
                access to messages published on this topic.

                The expected format is
                ``projects/*/locations/*/keyRings/*/cryptoKeys/*``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Topic` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_topic" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_topic"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_topic,
                default_retry=self._method_configs["CreateTopic"].retry,
                default_timeout=self._method_configs["CreateTopic"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.Topic(
            name=name,
            labels=labels,
            message_storage_policy=message_storage_policy,
            kms_key_name=kms_key_name,
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

        return self._inner_api_calls["create_topic"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_topic(
        self,
        topic,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing topic. Note that certain properties of a
        topic are not modifiable.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> # TODO: Initialize `topic`:
            >>> topic = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_topic(topic, update_mask)

        Args:
            topic (Union[dict, ~google.cloud.pubsub_v1.types.Topic]): The updated topic object.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Topic`
            update_mask (Union[dict, ~google.cloud.pubsub_v1.types.FieldMask]): Indicates which fields in the provided topic to update. Must be
                specified and non-empty. Note that if ``update_mask`` contains
                "message\_storage\_policy" then the new value will be determined based
                on the policy configured at the project or organization level. The
                ``message_storage_policy`` must not be set in the ``topic`` provided
                above.

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
            A :class:`~google.cloud.pubsub_v1.types.Topic` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_topic" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_topic"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_topic,
                default_retry=self._method_configs["UpdateTopic"].retry,
                default_timeout=self._method_configs["UpdateTopic"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.UpdateTopicRequest(topic=topic, update_mask=update_mask)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("topic.name", topic.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_topic"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def publish(
        self,
        topic,
        messages,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Adds one or more messages to the topic. Returns ``NOT_FOUND`` if the
        topic does not exist.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>> data = b''
            >>> messages_element = {'data': data}
            >>> messages = [messages_element]
            >>>
            >>> response = client.publish(topic, messages)

        Args:
            topic (str): The messages in the request will be published on this topic. Format is
                ``projects/{project}/topics/{topic}``.
            messages (list[Union[dict, ~google.cloud.pubsub_v1.types.PubsubMessage]]): The messages to publish.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.PubsubMessage`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.PublishResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "publish" not in self._inner_api_calls:
            self._inner_api_calls[
                "publish"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.publish,
                default_retry=self._method_configs["Publish"].retry,
                default_timeout=self._method_configs["Publish"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.PublishRequest(topic=topic, messages=messages)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("topic", topic)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["publish"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_topic(
        self,
        topic,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the configuration of a topic.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> response = client.get_topic(topic)

        Args:
            topic (str): The name of the topic to get. Format is
                ``projects/{project}/topics/{topic}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Topic` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_topic" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_topic"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_topic,
                default_retry=self._method_configs["GetTopic"].retry,
                default_timeout=self._method_configs["GetTopic"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.GetTopicRequest(topic=topic)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("topic", topic)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_topic"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_topics(
        self,
        project,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists matching topics.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> project = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_topics(project):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_topics(project).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project (str): The name of the project in which to list topics. Format is
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
            An iterable of :class:`~google.cloud.pubsub_v1.types.Topic` instances.
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
        if "list_topics" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_topics"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_topics,
                default_retry=self._method_configs["ListTopics"].retry,
                default_timeout=self._method_configs["ListTopics"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ListTopicsRequest(project=project, page_size=page_size)
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
                self._inner_api_calls["list_topics"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="topics",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def list_topic_subscriptions(
        self,
        topic,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the names of the subscriptions on this topic.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_topic_subscriptions(topic):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_topic_subscriptions(topic).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            topic (str): The name of the topic that subscriptions are attached to. Format is
                ``projects/{project}/topics/{topic}``.
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
            An iterable of :class:`str` instances.
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
        if "list_topic_subscriptions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_topic_subscriptions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_topic_subscriptions,
                default_retry=self._method_configs["ListTopicSubscriptions"].retry,
                default_timeout=self._method_configs["ListTopicSubscriptions"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.ListTopicSubscriptionsRequest(
            topic=topic, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("topic", topic)]
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
                self._inner_api_calls["list_topic_subscriptions"],
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

    def delete_topic(
        self,
        topic,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the topic with the given name. Returns ``NOT_FOUND`` if the
        topic does not exist. After a topic is deleted, a new topic may be
        created with the same name; this is an entirely new topic with none of
        the old configuration or subscriptions. Existing subscriptions to this
        topic are not deleted, but their ``topic`` field is set to
        ``_deleted-topic_``.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> client.delete_topic(topic)

        Args:
            topic (str): Name of the topic to delete. Format is
                ``projects/{project}/topics/{topic}``.
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
        if "delete_topic" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_topic"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_topic,
                default_retry=self._method_configs["DeleteTopic"].retry,
                default_timeout=self._method_configs["DeleteTopic"].timeout,
                client_info=self._client_info,
            )

        request = pubsub_pb2.DeleteTopicRequest(topic=topic)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("topic", topic)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_topic"](
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
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> resource = client.topic_path('[PROJECT]', '[TOPIC]')
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
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> resource = client.topic_path('[PROJECT]', '[TOPIC]')
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
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> resource = client.topic_path('[PROJECT]', '[TOPIC]')
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
