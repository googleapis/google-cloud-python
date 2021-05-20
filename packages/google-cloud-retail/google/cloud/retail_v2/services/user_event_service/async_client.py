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

from google.api import httpbody_pb2  # type: ignore
from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.retail_v2.types import common
from google.cloud.retail_v2.types import import_config
from google.cloud.retail_v2.types import purge_config
from google.cloud.retail_v2.types import user_event
from google.cloud.retail_v2.types import user_event_service
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import UserEventServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import UserEventServiceGrpcAsyncIOTransport
from .client import UserEventServiceClient


class UserEventServiceAsyncClient:
    """Service for ingesting end user actions on the customer
    website.
    """

    _client: UserEventServiceClient

    DEFAULT_ENDPOINT = UserEventServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = UserEventServiceClient.DEFAULT_MTLS_ENDPOINT

    product_path = staticmethod(UserEventServiceClient.product_path)
    parse_product_path = staticmethod(UserEventServiceClient.parse_product_path)
    common_billing_account_path = staticmethod(
        UserEventServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        UserEventServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(UserEventServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        UserEventServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        UserEventServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        UserEventServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(UserEventServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        UserEventServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(UserEventServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        UserEventServiceClient.parse_common_location_path
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
            UserEventServiceAsyncClient: The constructed client.
        """
        return UserEventServiceClient.from_service_account_info.__func__(UserEventServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            UserEventServiceAsyncClient: The constructed client.
        """
        return UserEventServiceClient.from_service_account_file.__func__(UserEventServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> UserEventServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            UserEventServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(UserEventServiceClient).get_transport_class, type(UserEventServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, UserEventServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the user event service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.UserEventServiceTransport]): The
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
        self._client = UserEventServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def write_user_event(
        self,
        request: user_event_service.WriteUserEventRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> user_event.UserEvent:
        r"""Writes a single user event.

        Args:
            request (:class:`google.cloud.retail_v2.types.WriteUserEventRequest`):
                The request object. Request message for WriteUserEvent
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.types.UserEvent:
                UserEvent captures all metadata
                information Retail API needs to know
                about how end users interact with
                customers' website.

        """
        # Create or coerce a protobuf request object.
        request = user_event_service.WriteUserEventRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.write_user_event,
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

    async def collect_user_event(
        self,
        request: user_event_service.CollectUserEventRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> httpbody_pb2.HttpBody:
        r"""Writes a single user event from the browser. This
        uses a GET request to due to browser restriction of
        POST-ing to a 3rd party domain.
        This method is used only by the Retail API JavaScript
        pixel and Google Tag Manager. Users should not call this
        method directly.

        Args:
            request (:class:`google.cloud.retail_v2.types.CollectUserEventRequest`):
                The request object. Request message for CollectUserEvent
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.httpbody_pb2.HttpBody:
                Message that represents an arbitrary HTTP body. It should only be used for
                   payload formats that can't be represented as JSON,
                   such as raw binary or an HTML page.

                   This message can be used both in streaming and
                   non-streaming API methods in the request as well as
                   the response.

                   It can be used as a top-level request field, which is
                   convenient if one wants to extract parameters from
                   either the URL or HTTP template into the request
                   fields and also want access to the raw HTTP body.

                   Example:

                      message GetResourceRequest {
                         // A unique request id. string request_id = 1;

                         // The raw HTTP body is bound to this field.
                         google.api.HttpBody http_body = 2;

                      }

                      service ResourceService {
                         rpc GetResource(GetResourceRequest) returns
                         (google.api.HttpBody); rpc
                         UpdateResource(google.api.HttpBody) returns
                         (google.protobuf.Empty);

                      }

                   Example with streaming methods:

                      service CaldavService {
                         rpc GetCalendar(stream google.api.HttpBody)
                            returns (stream google.api.HttpBody);

                         rpc UpdateCalendar(stream google.api.HttpBody)
                            returns (stream google.api.HttpBody);

                      }

                   Use of this type only changes how the request and
                   response bodies are handled, all other features will
                   continue to work unchanged.

        """
        # Create or coerce a protobuf request object.
        request = user_event_service.CollectUserEventRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.collect_user_event,
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

    async def purge_user_events(
        self,
        request: purge_config.PurgeUserEventsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes permanently all user events specified by the
        filter provided. Depending on the number of events
        specified by the filter, this operation could take hours
        or days to complete. To test a filter, use the list
        command first.

        Args:
            request (:class:`google.cloud.retail_v2.types.PurgeUserEventsRequest`):
                The request object. Request message for PurgeUserEvents
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2.types.PurgeUserEventsResponse` Response of the PurgeUserEventsRequest. If the long running operation is
                   successfully done, then this message is returned by
                   the google.longrunning.Operations.response field.

        """
        # Create or coerce a protobuf request object.
        request = purge_config.PurgeUserEventsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.purge_user_events,
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
            purge_config.PurgeUserEventsResponse,
            metadata_type=purge_config.PurgeMetadata,
        )

        # Done; return the response.
        return response

    async def import_user_events(
        self,
        request: import_config.ImportUserEventsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Bulk import of User events. Request processing might
        be synchronous. Events that already exist are skipped.
        Use this method for backfilling historical user events.
        Operation.response is of type ImportResponse. Note that
        it is possible for a subset of the items to be
        successfully inserted. Operation.metadata is of type
        ImportMetadata.

        Args:
            request (:class:`google.cloud.retail_v2.types.ImportUserEventsRequest`):
                The request object. Request message for the
                ImportUserEvents request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2.types.ImportUserEventsResponse` Response of the ImportUserEventsRequest. If the long running
                   operation was successful, then this message is
                   returned by the
                   google.longrunning.Operations.response field if the
                   operation was successful.

        """
        # Create or coerce a protobuf request object.
        request = import_config.ImportUserEventsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_user_events,
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
            import_config.ImportUserEventsResponse,
            metadata_type=import_config.ImportMetadata,
        )

        # Done; return the response.
        return response

    async def rejoin_user_events(
        self,
        request: user_event_service.RejoinUserEventsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Triggers a user event rejoin operation with latest
        product catalog. Events will not be annotated with
        detailed product information if product is missing from
        the catalog at the time the user event is ingested, and
        these events are stored as unjoined events with a
        limited usage on training and serving. This API can be
        used to trigger a 'join' operation on specified events
        with latest version of product catalog. It can also be
        used to correct events joined with wrong product
        catalog.

        Args:
            request (:class:`google.cloud.retail_v2.types.RejoinUserEventsRequest`):
                The request object. Request message for RejoinUserEvents
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.retail_v2.types.RejoinUserEventsResponse`
                Response message for RejoinUserEvents method.

        """
        # Create or coerce a protobuf request object.
        request = user_event_service.RejoinUserEventsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.rejoin_user_events,
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
            user_event_service.RejoinUserEventsResponse,
            metadata_type=user_event_service.RejoinUserEventsMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-retail",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("UserEventServiceAsyncClient",)
