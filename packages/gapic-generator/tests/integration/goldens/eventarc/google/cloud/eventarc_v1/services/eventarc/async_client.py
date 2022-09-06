# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials   # type: ignore
from google.oauth2 import service_account              # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.eventarc_v1.services.eventarc import pagers
from google.cloud.eventarc_v1.types import eventarc
from google.cloud.eventarc_v1.types import trigger
from google.cloud.eventarc_v1.types import trigger as gce_trigger
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import EventarcTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import EventarcGrpcAsyncIOTransport
from .client import EventarcClient


class EventarcAsyncClient:
    """Eventarc allows users to subscribe to various events that are
    provided by Google Cloud services and forward them to supported
    destinations.
    """

    _client: EventarcClient

    DEFAULT_ENDPOINT = EventarcClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = EventarcClient.DEFAULT_MTLS_ENDPOINT

    service_path = staticmethod(EventarcClient.service_path)
    parse_service_path = staticmethod(EventarcClient.parse_service_path)
    service_account_path = staticmethod(EventarcClient.service_account_path)
    parse_service_account_path = staticmethod(EventarcClient.parse_service_account_path)
    trigger_path = staticmethod(EventarcClient.trigger_path)
    parse_trigger_path = staticmethod(EventarcClient.parse_trigger_path)
    common_billing_account_path = staticmethod(EventarcClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(EventarcClient.parse_common_billing_account_path)
    common_folder_path = staticmethod(EventarcClient.common_folder_path)
    parse_common_folder_path = staticmethod(EventarcClient.parse_common_folder_path)
    common_organization_path = staticmethod(EventarcClient.common_organization_path)
    parse_common_organization_path = staticmethod(EventarcClient.parse_common_organization_path)
    common_project_path = staticmethod(EventarcClient.common_project_path)
    parse_common_project_path = staticmethod(EventarcClient.parse_common_project_path)
    common_location_path = staticmethod(EventarcClient.common_location_path)
    parse_common_location_path = staticmethod(EventarcClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            EventarcAsyncClient: The constructed client.
        """
        return EventarcClient.from_service_account_info.__func__(EventarcAsyncClient, info, *args, **kwargs)  # type: ignore

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
            EventarcAsyncClient: The constructed client.
        """
        return EventarcClient.from_service_account_file.__func__(EventarcAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(cls, client_options: Optional[ClientOptions] = None):
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
        default mTLS endpoint; if the environment variabel is "never", use the default API
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
        return EventarcClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> EventarcTransport:
        """Returns the transport used by the client instance.

        Returns:
            EventarcTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(type(EventarcClient).get_transport_class, type(EventarcClient))

    def __init__(self, *,
            credentials: ga_credentials.Credentials = None,
            transport: Union[str, EventarcTransport] = "grpc_asyncio",
            client_options: ClientOptions = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the eventarc client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.EventarcTransport]): The
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
        self._client = EventarcClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,

        )

    async def get_trigger(self,
            request: Union[eventarc.GetTriggerRequest, dict] = None,
            *,
            name: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> trigger.Trigger:
        r"""Get a single trigger.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import eventarc_v1

            async def sample_get_trigger():
                # Create a client
                client = eventarc_v1.EventarcAsyncClient()

                # Initialize request argument(s)
                request = eventarc_v1.GetTriggerRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_trigger(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.GetTriggerRequest, dict]):
                The request object. The request message for the
                GetTrigger method.
            name (:class:`str`):
                Required. The name of the trigger to
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
            google.cloud.eventarc_v1.types.Trigger:
                A representation of the trigger
                resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = eventarc.GetTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_trigger,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    async def list_triggers(self,
            request: Union[eventarc.ListTriggersRequest, dict] = None,
            *,
            parent: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListTriggersAsyncPager:
        r"""List triggers.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import eventarc_v1

            async def sample_list_triggers():
                # Create a client
                client = eventarc_v1.EventarcAsyncClient()

                # Initialize request argument(s)
                request = eventarc_v1.ListTriggersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_triggers(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.ListTriggersRequest, dict]):
                The request object. The request message for the
                ListTriggers method.
            parent (:class:`str`):
                Required. The parent collection to
                list triggers on.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.eventarc_v1.services.eventarc.pagers.ListTriggersAsyncPager:
                The response message for the
                ListTriggers method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = eventarc.ListTriggersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_triggers,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
        response = pagers.ListTriggersAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_trigger(self,
            request: Union[eventarc.CreateTriggerRequest, dict] = None,
            *,
            parent: str = None,
            trigger: gce_trigger.Trigger = None,
            trigger_id: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Create a new trigger in a particular project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import eventarc_v1

            async def sample_create_trigger():
                # Create a client
                client = eventarc_v1.EventarcAsyncClient()

                # Initialize request argument(s)
                trigger = eventarc_v1.Trigger()
                trigger.name = "name_value"
                trigger.event_filters.attribute = "attribute_value"
                trigger.event_filters.value = "value_value"
                trigger.destination.cloud_run.service = "service_value"
                trigger.destination.cloud_run.region = "region_value"

                request = eventarc_v1.CreateTriggerRequest(
                    parent="parent_value",
                    trigger=trigger,
                    trigger_id="trigger_id_value",
                    validate_only=True,
                )

                # Make the request
                operation = client.create_trigger(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.CreateTriggerRequest, dict]):
                The request object. The request message for the
                CreateTrigger method.
            parent (:class:`str`):
                Required. The parent collection in
                which to add this trigger.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger (:class:`google.cloud.eventarc_v1.types.Trigger`):
                Required. The trigger to create.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (:class:`str`):
                Required. The user-provided ID to be
                assigned to the trigger.

                This corresponds to the ``trigger_id`` field
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
                :class:`google.cloud.eventarc_v1.types.Trigger` A
                representation of the trigger resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, trigger, trigger_id])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = eventarc.CreateTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if trigger is not None:
            request.trigger = trigger
        if trigger_id is not None:
            request.trigger_id = trigger_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_trigger,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
            gce_trigger.Trigger,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_trigger(self,
            request: Union[eventarc.UpdateTriggerRequest, dict] = None,
            *,
            trigger: gce_trigger.Trigger = None,
            update_mask: field_mask_pb2.FieldMask = None,
            allow_missing: bool = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Update a single trigger.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import eventarc_v1

            async def sample_update_trigger():
                # Create a client
                client = eventarc_v1.EventarcAsyncClient()

                # Initialize request argument(s)
                request = eventarc_v1.UpdateTriggerRequest(
                    validate_only=True,
                )

                # Make the request
                operation = client.update_trigger(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.UpdateTriggerRequest, dict]):
                The request object. The request message for the
                UpdateTrigger method.
            trigger (:class:`google.cloud.eventarc_v1.types.Trigger`):
                The trigger to be updated.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The fields to be updated; only fields explicitly
                provided will be updated. If no field mask is provided,
                all provided fields in the request will be updated. To
                update all fields, provide a field mask of "*".

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            allow_missing (:class:`bool`):
                If set to true, and the trigger is not found, a new
                trigger will be created. In this situation,
                ``update_mask`` is ignored.

                This corresponds to the ``allow_missing`` field
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
                :class:`google.cloud.eventarc_v1.types.Trigger` A
                representation of the trigger resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([trigger, update_mask, allow_missing])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = eventarc.UpdateTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if trigger is not None:
            request.trigger = trigger
        if update_mask is not None:
            request.update_mask = update_mask
        if allow_missing is not None:
            request.allow_missing = allow_missing

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_trigger,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("trigger.name", request.trigger.name),
            )),
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
            gce_trigger.Trigger,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_trigger(self,
            request: Union[eventarc.DeleteTriggerRequest, dict] = None,
            *,
            name: str = None,
            allow_missing: bool = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Delete a single trigger.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import eventarc_v1

            async def sample_delete_trigger():
                # Create a client
                client = eventarc_v1.EventarcAsyncClient()

                # Initialize request argument(s)
                request = eventarc_v1.DeleteTriggerRequest(
                    name="name_value",
                    validate_only=True,
                )

                # Make the request
                operation = client.delete_trigger(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.DeleteTriggerRequest, dict]):
                The request object. The request message for the
                DeleteTrigger method.
            name (:class:`str`):
                Required. The name of the trigger to
                be deleted.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            allow_missing (:class:`bool`):
                If set to true, and the trigger is
                not found, the request will succeed but
                no action will be taken on the server.

                This corresponds to the ``allow_missing`` field
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
                :class:`google.cloud.eventarc_v1.types.Trigger` A
                representation of the trigger resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, allow_missing])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = eventarc.DeleteTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if allow_missing is not None:
            request.allow_missing = allow_missing

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_trigger,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
            trigger.Trigger,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-eventarc",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = (
    "EventarcAsyncClient",
)
