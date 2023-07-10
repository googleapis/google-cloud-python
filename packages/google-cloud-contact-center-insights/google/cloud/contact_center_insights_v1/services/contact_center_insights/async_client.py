# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.contact_center_insights_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.contact_center_insights_v1.services.contact_center_insights import (
    pagers,
)
from google.cloud.contact_center_insights_v1.types import (
    contact_center_insights,
    resources,
)

from .client import ContactCenterInsightsClient
from .transports.base import DEFAULT_CLIENT_INFO, ContactCenterInsightsTransport
from .transports.grpc_asyncio import ContactCenterInsightsGrpcAsyncIOTransport


class ContactCenterInsightsAsyncClient:
    """An API that lets users analyze and explore their business
    conversation data.
    """

    _client: ContactCenterInsightsClient

    DEFAULT_ENDPOINT = ContactCenterInsightsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ContactCenterInsightsClient.DEFAULT_MTLS_ENDPOINT

    analysis_path = staticmethod(ContactCenterInsightsClient.analysis_path)
    parse_analysis_path = staticmethod(ContactCenterInsightsClient.parse_analysis_path)
    conversation_path = staticmethod(ContactCenterInsightsClient.conversation_path)
    parse_conversation_path = staticmethod(
        ContactCenterInsightsClient.parse_conversation_path
    )
    conversation_profile_path = staticmethod(
        ContactCenterInsightsClient.conversation_profile_path
    )
    parse_conversation_profile_path = staticmethod(
        ContactCenterInsightsClient.parse_conversation_profile_path
    )
    issue_path = staticmethod(ContactCenterInsightsClient.issue_path)
    parse_issue_path = staticmethod(ContactCenterInsightsClient.parse_issue_path)
    issue_model_path = staticmethod(ContactCenterInsightsClient.issue_model_path)
    parse_issue_model_path = staticmethod(
        ContactCenterInsightsClient.parse_issue_model_path
    )
    participant_path = staticmethod(ContactCenterInsightsClient.participant_path)
    parse_participant_path = staticmethod(
        ContactCenterInsightsClient.parse_participant_path
    )
    phrase_matcher_path = staticmethod(ContactCenterInsightsClient.phrase_matcher_path)
    parse_phrase_matcher_path = staticmethod(
        ContactCenterInsightsClient.parse_phrase_matcher_path
    )
    settings_path = staticmethod(ContactCenterInsightsClient.settings_path)
    parse_settings_path = staticmethod(ContactCenterInsightsClient.parse_settings_path)
    view_path = staticmethod(ContactCenterInsightsClient.view_path)
    parse_view_path = staticmethod(ContactCenterInsightsClient.parse_view_path)
    common_billing_account_path = staticmethod(
        ContactCenterInsightsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ContactCenterInsightsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ContactCenterInsightsClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ContactCenterInsightsClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ContactCenterInsightsClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ContactCenterInsightsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ContactCenterInsightsClient.common_project_path)
    parse_common_project_path = staticmethod(
        ContactCenterInsightsClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        ContactCenterInsightsClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        ContactCenterInsightsClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ContactCenterInsightsAsyncClient: The constructed client.
        """
        return ContactCenterInsightsClient.from_service_account_info.__func__(ContactCenterInsightsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ContactCenterInsightsAsyncClient: The constructed client.
        """
        return ContactCenterInsightsClient.from_service_account_file.__func__(ContactCenterInsightsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return ContactCenterInsightsClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ContactCenterInsightsTransport:
        """Returns the transport used by the client instance.

        Returns:
            ContactCenterInsightsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ContactCenterInsightsClient).get_transport_class,
        type(ContactCenterInsightsClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, ContactCenterInsightsTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the contact center insights client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ContactCenterInsightsTransport]): The
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
        self._client = ContactCenterInsightsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.CreateConversationRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        conversation: Optional[resources.Conversation] = None,
        conversation_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Conversation:
        r"""Creates a conversation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_create_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CreateConversationRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_conversation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.CreateConversationRequest, dict]]):
                The request object. Request to create a conversation.
            parent (:class:`str`):
                Required. The parent resource of the
                conversation.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            conversation (:class:`google.cloud.contact_center_insights_v1.types.Conversation`):
                Required. The conversation resource
                to create.

                This corresponds to the ``conversation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            conversation_id (:class:`str`):
                A unique ID for the new conversation. This ID will
                become the final component of the conversation's
                resource name. If no ID is specified, a server-generated
                ID will be used.

                This value should be 4-64 characters and must match the
                regular expression ``^[a-z0-9-]{4,64}$``. Valid
                characters are ``[a-z][0-9]-``

                This corresponds to the ``conversation_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Conversation:
                The conversation resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, conversation, conversation_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.CreateConversationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if conversation is not None:
            request.conversation = conversation
        if conversation_id is not None:
            request.conversation_id = conversation_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_conversation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def upload_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.UploadConversationRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Create a longrunning conversation upload operation.
        This method differs from CreateConversation by allowing
        audio transcription and optional DLP redaction.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_upload_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UploadConversationRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.upload_conversation(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.UploadConversationRequest, dict]]):
                The request object. Request to upload a conversation.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.contact_center_insights_v1.types.Conversation`
                The conversation resource.

        """
        # Create or coerce a protobuf request object.
        request = contact_center_insights.UploadConversationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.upload_conversation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            resources.Conversation,
            metadata_type=contact_center_insights.UploadConversationMetadata,
        )

        # Done; return the response.
        return response

    async def update_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateConversationRequest, dict]
        ] = None,
        *,
        conversation: Optional[resources.Conversation] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Conversation:
        r"""Updates a conversation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_update_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateConversationRequest(
                )

                # Make the request
                response = await client.update_conversation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.UpdateConversationRequest, dict]]):
                The request object. The request to update a conversation.
            conversation (:class:`google.cloud.contact_center_insights_v1.types.Conversation`):
                Required. The new values for the
                conversation.

                This corresponds to the ``conversation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Conversation:
                The conversation resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([conversation, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.UpdateConversationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if conversation is not None:
            request.conversation = conversation
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_conversation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("conversation.name", request.conversation.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.GetConversationRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Conversation:
        r"""Gets a conversation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_get_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetConversationRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_conversation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.GetConversationRequest, dict]]):
                The request object. The request to get a conversation.
            name (:class:`str`):
                Required. The name of the
                conversation to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Conversation:
                The conversation resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.GetConversationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_conversation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_conversations(
        self,
        request: Optional[
            Union[contact_center_insights.ListConversationsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConversationsAsyncPager:
        r"""Lists conversations.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_list_conversations():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListConversationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_conversations(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.ListConversationsRequest, dict]]):
                The request object. Request to list conversations.
            parent (:class:`str`):
                Required. The parent resource of the
                conversation.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.services.contact_center_insights.pagers.ListConversationsAsyncPager:
                The response of listing
                conversations.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.ListConversationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_conversations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListConversationsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteConversationRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a conversation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_delete_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteConversationRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_conversation(request=request)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.DeleteConversationRequest, dict]]):
                The request object. The request to delete a conversation.
            name (:class:`str`):
                Required. The name of the
                conversation to delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.DeleteConversationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_conversation,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def create_analysis(
        self,
        request: Optional[
            Union[contact_center_insights.CreateAnalysisRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        analysis: Optional[resources.Analysis] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates an analysis. The long running operation is
        done when the analysis has completed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_create_analysis():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CreateAnalysisRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_analysis(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.CreateAnalysisRequest, dict]]):
                The request object. The request to create an analysis.
            parent (:class:`str`):
                Required. The parent resource of the
                analysis.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            analysis (:class:`google.cloud.contact_center_insights_v1.types.Analysis`):
                Required. The analysis to create.
                This corresponds to the ``analysis`` field
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
                :class:`google.cloud.contact_center_insights_v1.types.Analysis`
                The analysis resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, analysis])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.CreateAnalysisRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if analysis is not None:
            request.analysis = analysis

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_analysis,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            resources.Analysis,
            metadata_type=contact_center_insights.CreateAnalysisOperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_analysis(
        self,
        request: Optional[
            Union[contact_center_insights.GetAnalysisRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Analysis:
        r"""Gets an analysis.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_get_analysis():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetAnalysisRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_analysis(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.GetAnalysisRequest, dict]]):
                The request object. The request to get an analysis.
            name (:class:`str`):
                Required. The name of the analysis to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Analysis:
                The analysis resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.GetAnalysisRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_analysis,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_analyses(
        self,
        request: Optional[
            Union[contact_center_insights.ListAnalysesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAnalysesAsyncPager:
        r"""Lists analyses.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_list_analyses():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListAnalysesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_analyses(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.ListAnalysesRequest, dict]]):
                The request object. The request to list analyses.
            parent (:class:`str`):
                Required. The parent resource of the
                analyses.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.services.contact_center_insights.pagers.ListAnalysesAsyncPager:
                The response to list analyses.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.ListAnalysesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_analyses,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListAnalysesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_analysis(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteAnalysisRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an analysis.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_delete_analysis():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteAnalysisRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_analysis(request=request)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.DeleteAnalysisRequest, dict]]):
                The request object. The request to delete an analysis.
            name (:class:`str`):
                Required. The name of the analysis to
                delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.DeleteAnalysisRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_analysis,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def bulk_analyze_conversations(
        self,
        request: Optional[
            Union[contact_center_insights.BulkAnalyzeConversationsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        filter: Optional[str] = None,
        analysis_percentage: Optional[float] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Analyzes multiple conversations in a single request.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_bulk_analyze_conversations():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.BulkAnalyzeConversationsRequest(
                    parent="parent_value",
                    filter="filter_value",
                    analysis_percentage=0.20170000000000002,
                )

                # Make the request
                operation = client.bulk_analyze_conversations(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.BulkAnalyzeConversationsRequest, dict]]):
                The request object. The request to analyze conversations
                in bulk.
            parent (:class:`str`):
                Required. The parent resource to
                create analyses in.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
                Required. Filter used to select the
                subset of conversations to analyze.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            analysis_percentage (:class:`float`):
                Required. Percentage of selected conversation to
                analyze, between [0, 100].

                This corresponds to the ``analysis_percentage`` field
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
                :class:`google.cloud.contact_center_insights_v1.types.BulkAnalyzeConversationsResponse`
                The response for a bulk analyze conversations operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter, analysis_percentage])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.BulkAnalyzeConversationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if filter is not None:
            request.filter = filter
        if analysis_percentage is not None:
            request.analysis_percentage = analysis_percentage

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.bulk_analyze_conversations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            contact_center_insights.BulkAnalyzeConversationsResponse,
            metadata_type=contact_center_insights.BulkAnalyzeConversationsMetadata,
        )

        # Done; return the response.
        return response

    async def ingest_conversations(
        self,
        request: Optional[
            Union[contact_center_insights.IngestConversationsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Imports conversations and processes them according to
        the user's configuration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_ingest_conversations():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                gcs_source = contact_center_insights_v1.GcsSource()
                gcs_source.bucket_uri = "bucket_uri_value"

                transcript_object_config = contact_center_insights_v1.TranscriptObjectConfig()
                transcript_object_config.medium = "CHAT"

                request = contact_center_insights_v1.IngestConversationsRequest(
                    gcs_source=gcs_source,
                    transcript_object_config=transcript_object_config,
                    parent="parent_value",
                )

                # Make the request
                operation = client.ingest_conversations(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.IngestConversationsRequest, dict]]):
                The request object. The request to ingest conversations.
            parent (:class:`str`):
                Required. The parent resource for new
                conversations.

                This corresponds to the ``parent`` field
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
                :class:`google.cloud.contact_center_insights_v1.types.IngestConversationsResponse`
                The response to an IngestConversations operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.IngestConversationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.ingest_conversations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            contact_center_insights.IngestConversationsResponse,
            metadata_type=contact_center_insights.IngestConversationsMetadata,
        )

        # Done; return the response.
        return response

    async def export_insights_data(
        self,
        request: Optional[
            Union[contact_center_insights.ExportInsightsDataRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Export insights data to a destination defined in the
        request body.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_export_insights_data():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                big_query_destination = contact_center_insights_v1.BigQueryDestination()
                big_query_destination.dataset = "dataset_value"

                request = contact_center_insights_v1.ExportInsightsDataRequest(
                    big_query_destination=big_query_destination,
                    parent="parent_value",
                )

                # Make the request
                operation = client.export_insights_data(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.ExportInsightsDataRequest, dict]]):
                The request object. The request to export insights.
            parent (:class:`str`):
                Required. The parent resource to
                export data from.

                This corresponds to the ``parent`` field
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
                :class:`google.cloud.contact_center_insights_v1.types.ExportInsightsDataResponse`
                Response for an export insights operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.ExportInsightsDataRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_insights_data,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            contact_center_insights.ExportInsightsDataResponse,
            metadata_type=contact_center_insights.ExportInsightsDataMetadata,
        )

        # Done; return the response.
        return response

    async def create_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.CreateIssueModelRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        issue_model: Optional[resources.IssueModel] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates an issue model.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_create_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CreateIssueModelRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_issue_model(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.CreateIssueModelRequest, dict]]):
                The request object. The request to create an issue model.
            parent (:class:`str`):
                Required. The parent resource of the
                issue model.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            issue_model (:class:`google.cloud.contact_center_insights_v1.types.IssueModel`):
                Required. The issue model to create.
                This corresponds to the ``issue_model`` field
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
                :class:`google.cloud.contact_center_insights_v1.types.IssueModel`
                The issue model resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, issue_model])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.CreateIssueModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if issue_model is not None:
            request.issue_model = issue_model

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_issue_model,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            resources.IssueModel,
            metadata_type=contact_center_insights.CreateIssueModelMetadata,
        )

        # Done; return the response.
        return response

    async def update_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateIssueModelRequest, dict]
        ] = None,
        *,
        issue_model: Optional[resources.IssueModel] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.IssueModel:
        r"""Updates an issue model.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_update_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateIssueModelRequest(
                )

                # Make the request
                response = await client.update_issue_model(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.UpdateIssueModelRequest, dict]]):
                The request object. The request to update an issue model.
            issue_model (:class:`google.cloud.contact_center_insights_v1.types.IssueModel`):
                Required. The new values for the
                issue model.

                This corresponds to the ``issue_model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.IssueModel:
                The issue model resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([issue_model, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.UpdateIssueModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if issue_model is not None:
            request.issue_model = issue_model
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_issue_model,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("issue_model.name", request.issue_model.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.GetIssueModelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.IssueModel:
        r"""Gets an issue model.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_get_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetIssueModelRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_issue_model(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.GetIssueModelRequest, dict]]):
                The request object. The request to get an issue model.
            name (:class:`str`):
                Required. The name of the issue model
                to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.IssueModel:
                The issue model resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.GetIssueModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_issue_model,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_issue_models(
        self,
        request: Optional[
            Union[contact_center_insights.ListIssueModelsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> contact_center_insights.ListIssueModelsResponse:
        r"""Lists issue models.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_list_issue_models():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListIssueModelsRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.list_issue_models(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.ListIssueModelsRequest, dict]]):
                The request object. Request to list issue models.
            parent (:class:`str`):
                Required. The parent resource of the
                issue model.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.ListIssueModelsResponse:
                The response of listing issue models.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.ListIssueModelsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_issue_models,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteIssueModelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes an issue model.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_delete_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteIssueModelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_issue_model(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.DeleteIssueModelRequest, dict]]):
                The request object. The request to delete an issue model.
            name (:class:`str`):
                Required. The name of the issue model
                to delete.

                This corresponds to the ``name`` field
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

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.DeleteIssueModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_issue_model,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=contact_center_insights.DeleteIssueModelMetadata,
        )

        # Done; return the response.
        return response

    async def deploy_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.DeployIssueModelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deploys an issue model. Returns an error if a model
        is already deployed. An issue model can only be used in
        analysis after it has been deployed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_deploy_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeployIssueModelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.deploy_issue_model(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.DeployIssueModelRequest, dict]]):
                The request object. The request to deploy an issue model.
            name (:class:`str`):
                Required. The issue model to deploy.
                This corresponds to the ``name`` field
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
                :class:`google.cloud.contact_center_insights_v1.types.DeployIssueModelResponse`
                The response to deploy an issue model.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.DeployIssueModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.deploy_issue_model,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            contact_center_insights.DeployIssueModelResponse,
            metadata_type=contact_center_insights.DeployIssueModelMetadata,
        )

        # Done; return the response.
        return response

    async def undeploy_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.UndeployIssueModelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Undeploys an issue model.
        An issue model can not be used in analysis after it has
        been undeployed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_undeploy_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UndeployIssueModelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undeploy_issue_model(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.UndeployIssueModelRequest, dict]]):
                The request object. The request to undeploy an issue
                model.
            name (:class:`str`):
                Required. The issue model to
                undeploy.

                This corresponds to the ``name`` field
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
                :class:`google.cloud.contact_center_insights_v1.types.UndeployIssueModelResponse`
                The response to undeploy an issue model.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.UndeployIssueModelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.undeploy_issue_model,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            contact_center_insights.UndeployIssueModelResponse,
            metadata_type=contact_center_insights.UndeployIssueModelMetadata,
        )

        # Done; return the response.
        return response

    async def get_issue(
        self,
        request: Optional[Union[contact_center_insights.GetIssueRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Issue:
        r"""Gets an issue.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_get_issue():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetIssueRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_issue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.GetIssueRequest, dict]]):
                The request object. The request to get an issue.
            name (:class:`str`):
                Required. The name of the issue to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Issue:
                The issue resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.GetIssueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_issue,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_issues(
        self,
        request: Optional[
            Union[contact_center_insights.ListIssuesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> contact_center_insights.ListIssuesResponse:
        r"""Lists issues.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_list_issues():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListIssuesRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.list_issues(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.ListIssuesRequest, dict]]):
                The request object. Request to list issues.
            parent (:class:`str`):
                Required. The parent resource of the
                issue.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.ListIssuesResponse:
                The response of listing issues.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.ListIssuesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_issues,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_issue(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateIssueRequest, dict]
        ] = None,
        *,
        issue: Optional[resources.Issue] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Issue:
        r"""Updates an issue.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_update_issue():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateIssueRequest(
                )

                # Make the request
                response = await client.update_issue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.UpdateIssueRequest, dict]]):
                The request object. The request to update an issue.
            issue (:class:`google.cloud.contact_center_insights_v1.types.Issue`):
                Required. The new values for the
                issue.

                This corresponds to the ``issue`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Issue:
                The issue resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([issue, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.UpdateIssueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if issue is not None:
            request.issue = issue
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_issue,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("issue.name", request.issue.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_issue(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteIssueRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an issue.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_delete_issue():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteIssueRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_issue(request=request)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.DeleteIssueRequest, dict]]):
                The request object. The request to delete an issue.
            name (:class:`str`):
                Required. The name of the issue to
                delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.DeleteIssueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_issue,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def calculate_issue_model_stats(
        self,
        request: Optional[
            Union[contact_center_insights.CalculateIssueModelStatsRequest, dict]
        ] = None,
        *,
        issue_model: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> contact_center_insights.CalculateIssueModelStatsResponse:
        r"""Gets an issue model's statistics.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_calculate_issue_model_stats():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CalculateIssueModelStatsRequest(
                    issue_model="issue_model_value",
                )

                # Make the request
                response = await client.calculate_issue_model_stats(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.CalculateIssueModelStatsRequest, dict]]):
                The request object. Request to get statistics of an issue
                model.
            issue_model (:class:`str`):
                Required. The resource name of the
                issue model to query against.

                This corresponds to the ``issue_model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.CalculateIssueModelStatsResponse:
                Response of querying an issue model's
                statistics.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([issue_model])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.CalculateIssueModelStatsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if issue_model is not None:
            request.issue_model = issue_model

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.calculate_issue_model_stats,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("issue_model", request.issue_model),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_phrase_matcher(
        self,
        request: Optional[
            Union[contact_center_insights.CreatePhraseMatcherRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        phrase_matcher: Optional[resources.PhraseMatcher] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.PhraseMatcher:
        r"""Creates a phrase matcher.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_create_phrase_matcher():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                phrase_matcher = contact_center_insights_v1.PhraseMatcher()
                phrase_matcher.type_ = "ANY_OF"

                request = contact_center_insights_v1.CreatePhraseMatcherRequest(
                    parent="parent_value",
                    phrase_matcher=phrase_matcher,
                )

                # Make the request
                response = await client.create_phrase_matcher(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.CreatePhraseMatcherRequest, dict]]):
                The request object. Request to create a phrase matcher.
            parent (:class:`str`):
                Required. The parent resource of the phrase matcher.
                Required. The location to create a phrase matcher for.
                Format:
                ``projects/<Project ID>/locations/<Location ID>`` or
                ``projects/<Project Number>/locations/<Location ID>``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            phrase_matcher (:class:`google.cloud.contact_center_insights_v1.types.PhraseMatcher`):
                Required. The phrase matcher resource
                to create.

                This corresponds to the ``phrase_matcher`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.PhraseMatcher:
                The phrase matcher resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, phrase_matcher])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.CreatePhraseMatcherRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if phrase_matcher is not None:
            request.phrase_matcher = phrase_matcher

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_phrase_matcher,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_phrase_matcher(
        self,
        request: Optional[
            Union[contact_center_insights.GetPhraseMatcherRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.PhraseMatcher:
        r"""Gets a phrase matcher.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_get_phrase_matcher():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetPhraseMatcherRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_phrase_matcher(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.GetPhraseMatcherRequest, dict]]):
                The request object. The request to get a a phrase
                matcher.
            name (:class:`str`):
                Required. The name of the phrase
                matcher to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.PhraseMatcher:
                The phrase matcher resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.GetPhraseMatcherRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_phrase_matcher,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_phrase_matchers(
        self,
        request: Optional[
            Union[contact_center_insights.ListPhraseMatchersRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPhraseMatchersAsyncPager:
        r"""Lists phrase matchers.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_list_phrase_matchers():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListPhraseMatchersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_phrase_matchers(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.ListPhraseMatchersRequest, dict]]):
                The request object. Request to list phrase matchers.
            parent (:class:`str`):
                Required. The parent resource of the
                phrase matcher.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.services.contact_center_insights.pagers.ListPhraseMatchersAsyncPager:
                The response of listing phrase
                matchers.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.ListPhraseMatchersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_phrase_matchers,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListPhraseMatchersAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_phrase_matcher(
        self,
        request: Optional[
            Union[contact_center_insights.DeletePhraseMatcherRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a phrase matcher.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_delete_phrase_matcher():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeletePhraseMatcherRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_phrase_matcher(request=request)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.DeletePhraseMatcherRequest, dict]]):
                The request object. The request to delete a phrase
                matcher.
            name (:class:`str`):
                Required. The name of the phrase
                matcher to delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.DeletePhraseMatcherRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_phrase_matcher,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def update_phrase_matcher(
        self,
        request: Optional[
            Union[contact_center_insights.UpdatePhraseMatcherRequest, dict]
        ] = None,
        *,
        phrase_matcher: Optional[resources.PhraseMatcher] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.PhraseMatcher:
        r"""Updates a phrase matcher.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_update_phrase_matcher():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                phrase_matcher = contact_center_insights_v1.PhraseMatcher()
                phrase_matcher.type_ = "ANY_OF"

                request = contact_center_insights_v1.UpdatePhraseMatcherRequest(
                    phrase_matcher=phrase_matcher,
                )

                # Make the request
                response = await client.update_phrase_matcher(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.UpdatePhraseMatcherRequest, dict]]):
                The request object. The request to update a phrase
                matcher.
            phrase_matcher (:class:`google.cloud.contact_center_insights_v1.types.PhraseMatcher`):
                Required. The new values for the
                phrase matcher.

                This corresponds to the ``phrase_matcher`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.PhraseMatcher:
                The phrase matcher resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([phrase_matcher, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.UpdatePhraseMatcherRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if phrase_matcher is not None:
            request.phrase_matcher = phrase_matcher
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_phrase_matcher,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("phrase_matcher.name", request.phrase_matcher.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def calculate_stats(
        self,
        request: Optional[
            Union[contact_center_insights.CalculateStatsRequest, dict]
        ] = None,
        *,
        location: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> contact_center_insights.CalculateStatsResponse:
        r"""Gets conversation statistics.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_calculate_stats():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CalculateStatsRequest(
                    location="location_value",
                )

                # Make the request
                response = await client.calculate_stats(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.CalculateStatsRequest, dict]]):
                The request object. The request for calculating
                conversation statistics.
            location (:class:`str`):
                Required. The location of the
                conversations.

                This corresponds to the ``location`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.CalculateStatsResponse:
                The response for calculating
                conversation statistics.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([location])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.CalculateStatsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if location is not None:
            request.location = location

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.calculate_stats,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("location", request.location),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_settings(
        self,
        request: Optional[
            Union[contact_center_insights.GetSettingsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Settings:
        r"""Gets project-level settings.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_get_settings():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetSettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.GetSettingsRequest, dict]]):
                The request object. The request to get project-level
                settings.
            name (:class:`str`):
                Required. The name of the settings
                resource to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Settings:
                The settings resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.GetSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_settings,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_settings(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateSettingsRequest, dict]
        ] = None,
        *,
        settings: Optional[resources.Settings] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Settings:
        r"""Updates project-level settings.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_update_settings():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateSettingsRequest(
                )

                # Make the request
                response = await client.update_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.UpdateSettingsRequest, dict]]):
                The request object. The request to update project-level
                settings.
            settings (:class:`google.cloud.contact_center_insights_v1.types.Settings`):
                Required. The new settings values.
                This corresponds to the ``settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Settings:
                The settings resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.UpdateSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if settings is not None:
            request.settings = settings
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_settings,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("settings.name", request.settings.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_view(
        self,
        request: Optional[
            Union[contact_center_insights.CreateViewRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        view: Optional[resources.View] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.View:
        r"""Creates a view.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_create_view():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CreateViewRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_view(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.CreateViewRequest, dict]]):
                The request object. The request to create a view.
            parent (:class:`str`):
                Required. The parent resource of the view. Required. The
                location to create a view for. Format:
                ``projects/<Project ID>/locations/<Location ID>`` or
                ``projects/<Project Number>/locations/<Location ID>``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            view (:class:`google.cloud.contact_center_insights_v1.types.View`):
                Required. The view resource to
                create.

                This corresponds to the ``view`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.View:
                The View resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, view])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.CreateViewRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if view is not None:
            request.view = view

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_view,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_view(
        self,
        request: Optional[Union[contact_center_insights.GetViewRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.View:
        r"""Gets a view.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_get_view():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetViewRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_view(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.GetViewRequest, dict]]):
                The request object. The request to get a view.
            name (:class:`str`):
                Required. The name of the view to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.View:
                The View resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.GetViewRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_view,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_views(
        self,
        request: Optional[Union[contact_center_insights.ListViewsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListViewsAsyncPager:
        r"""Lists views.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_list_views():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListViewsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_views(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.ListViewsRequest, dict]]):
                The request object. The request to list views.
            parent (:class:`str`):
                Required. The parent resource of the
                views.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.services.contact_center_insights.pagers.ListViewsAsyncPager:
                The response of listing views.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.ListViewsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_views,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListViewsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_view(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateViewRequest, dict]
        ] = None,
        *,
        view: Optional[resources.View] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.View:
        r"""Updates a view.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_update_view():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateViewRequest(
                )

                # Make the request
                response = await client.update_view(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.UpdateViewRequest, dict]]):
                The request object. The request to update a view.
            view (:class:`google.cloud.contact_center_insights_v1.types.View`):
                Required. The new view.
                This corresponds to the ``view`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.View:
                The View resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([view, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.UpdateViewRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if view is not None:
            request.view = view
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_view,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("view.name", request.view.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_view(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteViewRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a view.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            async def sample_delete_view():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsAsyncClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteViewRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_view(request=request)

        Args:
            request (Optional[Union[google.cloud.contact_center_insights_v1.types.DeleteViewRequest, dict]]):
                The request object. The request to delete a view.
            name (:class:`str`):
                Required. The name of the view to
                delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = contact_center_insights.DeleteViewRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_view,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.list_operations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.cancel_operation,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def __aenter__(self) -> "ContactCenterInsightsAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ContactCenterInsightsAsyncClient",)
