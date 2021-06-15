# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import timeout as timeouts  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.pubsub_v1.services.publisher import pagers
from google.pubsub_v1.types import pubsub
from google.pubsub_v1.types import TimeoutType
from .transports.base import PublisherTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import PublisherGrpcAsyncIOTransport
from .client import PublisherClient


class PublisherAsyncClient:
    """The service that an application uses to manipulate topics,
    and to send messages to a topic.
    """

    _client: PublisherClient

    DEFAULT_ENDPOINT = PublisherClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = PublisherClient.DEFAULT_MTLS_ENDPOINT

    schema_path = staticmethod(PublisherClient.schema_path)
    parse_schema_path = staticmethod(PublisherClient.parse_schema_path)
    subscription_path = staticmethod(PublisherClient.subscription_path)
    parse_subscription_path = staticmethod(PublisherClient.parse_subscription_path)
    topic_path = staticmethod(PublisherClient.topic_path)
    parse_topic_path = staticmethod(PublisherClient.parse_topic_path)

    common_billing_account_path = staticmethod(
        PublisherClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        PublisherClient.parse_common_billing_account_path
    )

    common_folder_path = staticmethod(PublisherClient.common_folder_path)
    parse_common_folder_path = staticmethod(PublisherClient.parse_common_folder_path)

    common_organization_path = staticmethod(PublisherClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        PublisherClient.parse_common_organization_path
    )

    common_project_path = staticmethod(PublisherClient.common_project_path)
    parse_common_project_path = staticmethod(PublisherClient.parse_common_project_path)

    common_location_path = staticmethod(PublisherClient.common_location_path)
    parse_common_location_path = staticmethod(
        PublisherClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            PublisherAsyncClient: The constructed client.
        """
        return PublisherClient.from_service_account_info.__func__(PublisherAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            PublisherAsyncClient: The constructed client.
        """
        return PublisherClient.from_service_account_file.__func__(PublisherAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> PublisherTransport:
        """Return the transport used by the client instance.

        Returns:
            PublisherTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(PublisherClient).get_transport_class, type(PublisherClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, PublisherTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the publisher client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.PublisherTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = PublisherClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_topic(
        self,
        request: pubsub.Topic = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pubsub.Topic:
        r"""Creates the given topic with the given name. See the [resource
        name rules]
        (https://cloud.google.com/pubsub/docs/admin#resource_names).

        Args:
            request (:class:`google.pubsub_v1.types.Topic`):
                The request object. A topic resource.
            name (:class:`str`):
                Required. The name of the topic. It must have the format
                ``"projects/{project}/topics/{topic}"``. ``{topic}``
                must start with a letter, and contain only letters
                (``[A-Za-z]``), numbers (``[0-9]``), dashes (``-``),
                underscores (``_``), periods (``.``), tildes (``~``),
                plus (``+``) or percent signs (``%``). It must be
                between 3 and 255 characters in length, and it must not
                start with ``"goog"``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.pubsub_v1.types.Topic:
                A topic resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = pubsub.Topic(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_topic,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_topic(
        self,
        request: pubsub.UpdateTopicRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pubsub.Topic:
        r"""Updates an existing topic. Note that certain
        properties of a topic are not modifiable.

        Args:
            request (:class:`google.pubsub_v1.types.UpdateTopicRequest`):
                The request object. Request for the UpdateTopic method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.pubsub_v1.types.Topic:
                A topic resource.
        """
        # Create or coerce a protobuf request object.

        request = pubsub.UpdateTopicRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_topic,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("topic.name", request.topic.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def publish(
        self,
        request: pubsub.PublishRequest = None,
        *,
        topic: str = None,
        messages: Sequence[pubsub.PubsubMessage] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pubsub.PublishResponse:
        r"""Adds one or more messages to the topic. Returns ``NOT_FOUND`` if
        the topic does not exist.

        Args:
            request (:class:`google.pubsub_v1.types.PublishRequest`):
                The request object. Request for the Publish method.
            topic (:class:`str`):
                Required. The messages in the request will be published
                on this topic. Format is
                ``projects/{project}/topics/{topic}``.

                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            messages (:class:`Sequence[google.pubsub_v1.types.PubsubMessage]`):
                Required. The messages to publish.
                This corresponds to the ``messages`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.pubsub_v1.types.PublishResponse:
                Response for the Publish method.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([topic, messages])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = pubsub.PublishRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic

        if messages:
            request.messages.extend(messages)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.publish,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.Cancelled,
                    exceptions.DeadlineExceeded,
                    exceptions.InternalServerError,
                    exceptions.ResourceExhausted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", request.topic),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_topic(
        self,
        request: pubsub.GetTopicRequest = None,
        *,
        topic: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pubsub.Topic:
        r"""Gets the configuration of a topic.

        Args:
            request (:class:`google.pubsub_v1.types.GetTopicRequest`):
                The request object. Request for the GetTopic method.
            topic (:class:`str`):
                Required. The name of the topic to get. Format is
                ``projects/{project}/topics/{topic}``.

                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.pubsub_v1.types.Topic:
                A topic resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([topic])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = pubsub.GetTopicRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_topic,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", request.topic),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_topics(
        self,
        request: pubsub.ListTopicsRequest = None,
        *,
        project: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTopicsAsyncPager:
        r"""Lists matching topics.

        Args:
            request (:class:`google.pubsub_v1.types.ListTopicsRequest`):
                The request object. Request for the `ListTopics` method.
            project (:class:`str`):
                Required. The name of the project in which to list
                topics. Format is ``projects/{project-id}``.

                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.pubsub_v1.services.publisher.pagers.ListTopicsAsyncPager:
                Response for the ListTopics method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = pubsub.ListTopicsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project is not None:
            request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_topics,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project", request.project),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTopicsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_topic_subscriptions(
        self,
        request: pubsub.ListTopicSubscriptionsRequest = None,
        *,
        topic: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTopicSubscriptionsAsyncPager:
        r"""Lists the names of the attached subscriptions on this
        topic.

        Args:
            request (:class:`google.pubsub_v1.types.ListTopicSubscriptionsRequest`):
                The request object. Request for the
                `ListTopicSubscriptions` method.
            topic (:class:`str`):
                Required. The name of the topic that subscriptions are
                attached to. Format is
                ``projects/{project}/topics/{topic}``.

                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.pubsub_v1.services.publisher.pagers.ListTopicSubscriptionsAsyncPager:
                Response for the ListTopicSubscriptions method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([topic])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = pubsub.ListTopicSubscriptionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_topic_subscriptions,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", request.topic),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTopicSubscriptionsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_topic_snapshots(
        self,
        request: pubsub.ListTopicSnapshotsRequest = None,
        *,
        topic: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTopicSnapshotsAsyncPager:
        r"""Lists the names of the snapshots on this topic. Snapshots are
        used in
        `Seek <https://cloud.google.com/pubsub/docs/replay-overview>`__
        operations, which allow you to manage message acknowledgments in
        bulk. That is, you can set the acknowledgment state of messages
        in an existing subscription to the state captured by a snapshot.

        Args:
            request (:class:`google.pubsub_v1.types.ListTopicSnapshotsRequest`):
                The request object. Request for the `ListTopicSnapshots`
                method.
            topic (:class:`str`):
                Required. The name of the topic that snapshots are
                attached to. Format is
                ``projects/{project}/topics/{topic}``.

                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.pubsub_v1.services.publisher.pagers.ListTopicSnapshotsAsyncPager:
                Response for the ListTopicSnapshots method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([topic])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = pubsub.ListTopicSnapshotsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_topic_snapshots,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.Aborted,
                    exceptions.ServiceUnavailable,
                    exceptions.Unknown,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", request.topic),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTopicSnapshotsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_topic(
        self,
        request: pubsub.DeleteTopicRequest = None,
        *,
        topic: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the topic with the given name. Returns ``NOT_FOUND`` if
        the topic does not exist. After a topic is deleted, a new topic
        may be created with the same name; this is an entirely new topic
        with none of the old configuration or subscriptions. Existing
        subscriptions to this topic are not deleted, but their ``topic``
        field is set to ``_deleted-topic_``.

        Args:
            request (:class:`google.pubsub_v1.types.DeleteTopicRequest`):
                The request object. Request for the `DeleteTopic`
                method.
            topic (:class:`str`):
                Required. Name of the topic to delete. Format is
                ``projects/{project}/topics/{topic}``.

                This corresponds to the ``topic`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([topic])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = pubsub.DeleteTopicRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if topic is not None:
            request.topic = topic

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_topic,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", request.topic),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def detach_subscription(
        self,
        request: pubsub.DetachSubscriptionRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pubsub.DetachSubscriptionResponse:
        r"""Detaches a subscription from this topic. All messages retained
        in the subscription are dropped. Subsequent ``Pull`` and
        ``StreamingPull`` requests will return FAILED_PRECONDITION. If
        the subscription is a push subscription, pushes to the endpoint
        will stop.

        Args:
            request (:class:`google.pubsub_v1.types.DetachSubscriptionRequest`):
                The request object. Request for the DetachSubscription
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.pubsub_v1.types.DetachSubscriptionResponse:
                Response for the DetachSubscription
                method. Reserved for future use.

        """
        # Create or coerce a protobuf request object.

        request = pubsub.DetachSubscriptionRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.detach_subscription,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("subscription", request.subscription),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def set_iam_policy(
        self,
        request: iam_policy.SetIamPolicyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy.Policy:
        r"""Sets the IAM access control policy on the specified
        function. Replaces any existing policy.
        Args:
            request (:class:`~.iam_policy.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.
                **JSON Example**
                ::
                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }
                **YAML Example**
                ::
                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy.SetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_iam_policy(
        self,
        request: iam_policy.GetIamPolicyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy.Policy:
        r"""Gets the IAM access control policy for a function.
        Returns an empty policy if the function exists and does
        not have a policy set.
        Args:
            request (:class:`~.iam_policy.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.
                **JSON Example**
                ::
                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }
                **YAML Example**
                ::
                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')
                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy.GetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def test_iam_permissions(
        self,
        request: iam_policy.TestIamPermissionsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: TimeoutType = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy.TestIamPermissionsResponse:
        r"""Tests the specified permissions against the IAM access control
        policy for a function. If the function does not exist, this will
        return an empty set of permissions, not a NOT_FOUND error.
        Args:
            request (:class:`~.iam_policy.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (TimeoutType):
                The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.iam_policy.TestIamPermissionsResponse:
                Response message for ``TestIamPermissions`` method.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.test_iam_permissions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        client_library_version=pkg_resources.get_distribution(
            "google-cloud-pubsub",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("PublisherAsyncClient",)
