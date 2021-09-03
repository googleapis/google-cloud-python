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
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.dialogflow_v2beta1.services.intents import pagers
from google.cloud.dialogflow_v2beta1.types import context
from google.cloud.dialogflow_v2beta1.types import intent
from google.cloud.dialogflow_v2beta1.types import intent as gcd_intent
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from .transports.base import IntentsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import IntentsGrpcAsyncIOTransport
from .client import IntentsClient


class IntentsAsyncClient:
    """Service for managing
    [Intents][google.cloud.dialogflow.v2beta1.Intent].
    """

    _client: IntentsClient

    DEFAULT_ENDPOINT = IntentsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = IntentsClient.DEFAULT_MTLS_ENDPOINT

    context_path = staticmethod(IntentsClient.context_path)
    parse_context_path = staticmethod(IntentsClient.parse_context_path)
    intent_path = staticmethod(IntentsClient.intent_path)
    parse_intent_path = staticmethod(IntentsClient.parse_intent_path)
    common_billing_account_path = staticmethod(
        IntentsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        IntentsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(IntentsClient.common_folder_path)
    parse_common_folder_path = staticmethod(IntentsClient.parse_common_folder_path)
    common_organization_path = staticmethod(IntentsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        IntentsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(IntentsClient.common_project_path)
    parse_common_project_path = staticmethod(IntentsClient.parse_common_project_path)
    common_location_path = staticmethod(IntentsClient.common_location_path)
    parse_common_location_path = staticmethod(IntentsClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            IntentsAsyncClient: The constructed client.
        """
        return IntentsClient.from_service_account_info.__func__(IntentsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            IntentsAsyncClient: The constructed client.
        """
        return IntentsClient.from_service_account_file.__func__(IntentsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> IntentsTransport:
        """Returns the transport used by the client instance.

        Returns:
            IntentsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(IntentsClient).get_transport_class, type(IntentsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, IntentsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the intents client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.IntentsTransport]): The
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
        self._client = IntentsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_intents(
        self,
        request: intent.ListIntentsRequest = None,
        *,
        parent: str = None,
        language_code: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListIntentsAsyncPager:
        r"""Returns the list of all intents in the specified
        agent.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.ListIntentsRequest`):
                The request object. The request message for
                [Intents.ListIntents][google.cloud.dialogflow.v2beta1.Intents.ListIntents].
            parent (:class:`str`):
                Required. The agent to list all intents from. Format:
                ``projects/<Project ID>/agent`` or
                ``projects/<Project ID>/locations/<Location ID>/agent``.

                Alternatively, you can specify the environment to list
                intents for. Format:
                ``projects/<Project ID>/agent/environments/<Environment ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agent/environments/<Environment ID>``.
                Note: training phrases of the intents will not be
                returned for non-draft environment.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            language_code (:class:`str`):
                Optional. The language used to access language-specific
                data. If not specified, the agent's default language is
                used. For more information, see `Multilingual intent and
                entity
                data <https://cloud.google.com/dialogflow/docs/agents-multilingual#intent-entity>`__.

                This corresponds to the ``language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.services.intents.pagers.ListIntentsAsyncPager:
                The response message for
                [Intents.ListIntents][google.cloud.dialogflow.v2beta1.Intents.ListIntents].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, language_code])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = intent.ListIntentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if language_code is not None:
            request.language_code = language_code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_intents,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListIntentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_intent(
        self,
        request: intent.GetIntentRequest = None,
        *,
        name: str = None,
        language_code: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> intent.Intent:
        r"""Retrieves the specified intent.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.GetIntentRequest`):
                The request object. The request message for
                [Intents.GetIntent][google.cloud.dialogflow.v2beta1.Intents.GetIntent].
            name (:class:`str`):
                Required. The name of the intent. Supported formats:

                -  ``projects/<Project ID>/agent/intents/<Intent ID>``
                -  ``projects/<Project ID>/locations/<Location ID>/agent/intents/<Intent ID>``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            language_code (:class:`str`):
                Optional. The language used to access language-specific
                data. If not specified, the agent's default language is
                used. For more information, see `Multilingual intent and
                entity
                data <https://cloud.google.com/dialogflow/docs/agents-multilingual#intent-entity>`__.

                This corresponds to the ``language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.Intent:
                An intent categorizes an end-user's intention for one conversation turn. For
                   each agent, you define many intents, where your
                   combined intents can handle a complete conversation.
                   When an end-user writes or says something, referred
                   to as an end-user expression or end-user input,
                   Dialogflow matches the end-user input to the best
                   intent in your agent. Matching an intent is also
                   known as intent classification.

                   For more information, see the [intent
                   guide](\ https://cloud.google.com/dialogflow/docs/intents-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, language_code])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = intent.GetIntentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if language_code is not None:
            request.language_code = language_code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_intent,
            default_timeout=None,
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

    async def create_intent(
        self,
        request: gcd_intent.CreateIntentRequest = None,
        *,
        parent: str = None,
        intent: gcd_intent.Intent = None,
        language_code: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_intent.Intent:
        r"""Creates an intent in the specified agent.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.CreateIntentRequest`):
                The request object. The request message for
                [Intents.CreateIntent][google.cloud.dialogflow.v2beta1.Intents.CreateIntent].
            parent (:class:`str`):
                Required. The agent to create a intent for. Supported
                formats:

                -  ``projects/<Project ID>/agent``
                -  ``projects/<Project ID>/locations/<Location ID>/agent``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            intent (:class:`google.cloud.dialogflow_v2beta1.types.Intent`):
                Required. The intent to create.
                This corresponds to the ``intent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            language_code (:class:`str`):
                Optional. The language used to access language-specific
                data. If not specified, the agent's default language is
                used. For more information, see `Multilingual intent and
                entity
                data <https://cloud.google.com/dialogflow/docs/agents-multilingual#intent-entity>`__.

                This corresponds to the ``language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.Intent:
                An intent categorizes an end-user's intention for one conversation turn. For
                   each agent, you define many intents, where your
                   combined intents can handle a complete conversation.
                   When an end-user writes or says something, referred
                   to as an end-user expression or end-user input,
                   Dialogflow matches the end-user input to the best
                   intent in your agent. Matching an intent is also
                   known as intent classification.

                   For more information, see the [intent
                   guide](\ https://cloud.google.com/dialogflow/docs/intents-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, intent, language_code])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_intent.CreateIntentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if intent is not None:
            request.intent = intent
        if language_code is not None:
            request.language_code = language_code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_intent,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_intent(
        self,
        request: gcd_intent.UpdateIntentRequest = None,
        *,
        intent: gcd_intent.Intent = None,
        update_mask: field_mask_pb2.FieldMask = None,
        language_code: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_intent.Intent:
        r"""Updates the specified intent.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.UpdateIntentRequest`):
                The request object. The request message for
                [Intents.UpdateIntent][google.cloud.dialogflow.v2beta1.Intents.UpdateIntent].
            intent (:class:`google.cloud.dialogflow_v2beta1.types.Intent`):
                Required. The intent to update.
                This corresponds to the ``intent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. The mask to control which
                fields get updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            language_code (:class:`str`):
                Optional. The language used to access language-specific
                data. If not specified, the agent's default language is
                used. For more information, see `Multilingual intent and
                entity
                data <https://cloud.google.com/dialogflow/docs/agents-multilingual#intent-entity>`__.

                This corresponds to the ``language_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.Intent:
                An intent categorizes an end-user's intention for one conversation turn. For
                   each agent, you define many intents, where your
                   combined intents can handle a complete conversation.
                   When an end-user writes or says something, referred
                   to as an end-user expression or end-user input,
                   Dialogflow matches the end-user input to the best
                   intent in your agent. Matching an intent is also
                   known as intent classification.

                   For more information, see the [intent
                   guide](\ https://cloud.google.com/dialogflow/docs/intents-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([intent, update_mask, language_code])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_intent.UpdateIntentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if intent is not None:
            request.intent = intent
        if update_mask is not None:
            request.update_mask = update_mask
        if language_code is not None:
            request.language_code = language_code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_intent,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("intent.name", request.intent.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_intent(
        self,
        request: intent.DeleteIntentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified intent and its direct or indirect followup
        intents.

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.DeleteIntentRequest`):
                The request object. The request message for
                [Intents.DeleteIntent][google.cloud.dialogflow.v2beta1.Intents.DeleteIntent].
            name (:class:`str`):
                Required. The name of the intent to delete. If this
                intent has direct or indirect followup intents, we also
                delete them.

                Supported formats:

                -  ``projects/<Project ID>/agent/intents/<Intent ID>``
                -  ``projects/<Project ID>/locations/<Location ID>/agent/intents/<Intent ID>``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = intent.DeleteIntentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_intent,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def batch_update_intents(
        self,
        request: intent.BatchUpdateIntentsRequest = None,
        *,
        parent: str = None,
        intent_batch_uri: str = None,
        intent_batch_inline: intent.IntentBatch = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates/Creates multiple intents in the specified agent.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``:
           [BatchUpdateIntentsResponse][google.cloud.dialogflow.v2beta1.BatchUpdateIntentsResponse]

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.BatchUpdateIntentsRequest`):
                The request object. The request message for
                [Intents.BatchUpdateIntents][google.cloud.dialogflow.v2beta1.Intents.BatchUpdateIntents].
            parent (:class:`str`):
                Required. The name of the agent to update or create
                intents in. Supported formats:

                -  ``projects/<Project ID>/agent``
                -  ``projects/<Project ID>/locations/<Location ID>/agent``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            intent_batch_uri (:class:`str`):
                The URI to a Google Cloud Storage
                file containing intents to update or
                create. The file format can either be a
                serialized proto (of IntentBatch type)
                or JSON object. Note: The URI must start
                with "gs://".

                This corresponds to the ``intent_batch_uri`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            intent_batch_inline (:class:`google.cloud.dialogflow_v2beta1.types.IntentBatch`):
                The collection of intents to update
                or create.

                This corresponds to the ``intent_batch_inline`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflow_v2beta1.types.BatchUpdateIntentsResponse`
                The response message for
                [Intents.BatchUpdateIntents][google.cloud.dialogflow.v2beta1.Intents.BatchUpdateIntents].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, intent_batch_uri, intent_batch_inline])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = intent.BatchUpdateIntentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if intent_batch_uri is not None:
            request.intent_batch_uri = intent_batch_uri
        if intent_batch_inline is not None:
            request.intent_batch_inline = intent_batch_inline

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_update_intents,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            intent.BatchUpdateIntentsResponse,
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response

    async def batch_delete_intents(
        self,
        request: intent.BatchDeleteIntentsRequest = None,
        *,
        parent: str = None,
        intents: Sequence[intent.Intent] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes intents in the specified agent.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/es/docs/how/long-running-operations>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``: An `Empty
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#empty>`__

        Note: You should always train an agent prior to sending it
        queries. See the `training
        documentation <https://cloud.google.com/dialogflow/es/docs/training>`__.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.BatchDeleteIntentsRequest`):
                The request object. The request message for
                [Intents.BatchDeleteIntents][google.cloud.dialogflow.v2beta1.Intents.BatchDeleteIntents].
            parent (:class:`str`):
                Required. The name of the agent to delete all entities
                types for. Supported formats:

                -  ``projects/<Project ID>/agent``
                -  ``projects/<Project ID>/locations/<Location ID>/agent``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            intents (:class:`Sequence[google.cloud.dialogflow_v2beta1.types.Intent]`):
                Required. The collection of intents to delete. Only
                intent ``name`` must be filled in.

                This corresponds to the ``intents`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, intents])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = intent.BatchDeleteIntentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if intents:
            request.intents.extend(intents)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_delete_intents,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("IntentsAsyncClient",)
