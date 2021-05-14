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

from google.cloud.dialogflow_v2.types import fulfillment
from google.cloud.dialogflow_v2.types import fulfillment as gcd_fulfillment
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import FulfillmentsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import FulfillmentsGrpcAsyncIOTransport
from .client import FulfillmentsClient


class FulfillmentsAsyncClient:
    """Service for managing
    [Fulfillments][google.cloud.dialogflow.v2.Fulfillment].
    """

    _client: FulfillmentsClient

    DEFAULT_ENDPOINT = FulfillmentsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = FulfillmentsClient.DEFAULT_MTLS_ENDPOINT

    fulfillment_path = staticmethod(FulfillmentsClient.fulfillment_path)
    parse_fulfillment_path = staticmethod(FulfillmentsClient.parse_fulfillment_path)
    common_billing_account_path = staticmethod(
        FulfillmentsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        FulfillmentsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(FulfillmentsClient.common_folder_path)
    parse_common_folder_path = staticmethod(FulfillmentsClient.parse_common_folder_path)
    common_organization_path = staticmethod(FulfillmentsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        FulfillmentsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(FulfillmentsClient.common_project_path)
    parse_common_project_path = staticmethod(
        FulfillmentsClient.parse_common_project_path
    )
    common_location_path = staticmethod(FulfillmentsClient.common_location_path)
    parse_common_location_path = staticmethod(
        FulfillmentsClient.parse_common_location_path
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
            FulfillmentsAsyncClient: The constructed client.
        """
        return FulfillmentsClient.from_service_account_info.__func__(FulfillmentsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            FulfillmentsAsyncClient: The constructed client.
        """
        return FulfillmentsClient.from_service_account_file.__func__(FulfillmentsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> FulfillmentsTransport:
        """Returns the transport used by the client instance.

        Returns:
            FulfillmentsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(FulfillmentsClient).get_transport_class, type(FulfillmentsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, FulfillmentsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the fulfillments client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.FulfillmentsTransport]): The
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
        self._client = FulfillmentsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_fulfillment(
        self,
        request: fulfillment.GetFulfillmentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> fulfillment.Fulfillment:
        r"""Retrieves the fulfillment.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.GetFulfillmentRequest`):
                The request object. The request message for
                [Fulfillments.GetFulfillment][google.cloud.dialogflow.v2.Fulfillments.GetFulfillment].
            name (:class:`str`):
                Required. The name of the fulfillment. Format:
                ``projects/<Project ID>/agent/fulfillment``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Fulfillment:
                By default, your agent responds to a matched intent with a static response.
                   As an alternative, you can provide a more dynamic
                   response by using fulfillment. When you enable
                   fulfillment for an intent, Dialogflow responds to
                   that intent by calling a service that you define. For
                   example, if an end-user wants to schedule a haircut
                   on Friday, your service can check your database and
                   respond to the end-user with availability information
                   for Friday.

                   For more information, see the [fulfillment
                   guide](\ https://cloud.google.com/dialogflow/docs/fulfillment-overview).

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

        request = fulfillment.GetFulfillmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_fulfillment,
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

    async def update_fulfillment(
        self,
        request: gcd_fulfillment.UpdateFulfillmentRequest = None,
        *,
        fulfillment: gcd_fulfillment.Fulfillment = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_fulfillment.Fulfillment:
        r"""Updates the fulfillment.

        Args:
            request (:class:`google.cloud.dialogflow_v2.types.UpdateFulfillmentRequest`):
                The request object. The request message for
                [Fulfillments.UpdateFulfillment][google.cloud.dialogflow.v2.Fulfillments.UpdateFulfillment].
            fulfillment (:class:`google.cloud.dialogflow_v2.types.Fulfillment`):
                Required. The fulfillment to update.
                This corresponds to the ``fulfillment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to control which
                fields get updated. If the mask is not
                present, all fields will be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Fulfillment:
                By default, your agent responds to a matched intent with a static response.
                   As an alternative, you can provide a more dynamic
                   response by using fulfillment. When you enable
                   fulfillment for an intent, Dialogflow responds to
                   that intent by calling a service that you define. For
                   example, if an end-user wants to schedule a haircut
                   on Friday, your service can check your database and
                   respond to the end-user with availability information
                   for Friday.

                   For more information, see the [fulfillment
                   guide](\ https://cloud.google.com/dialogflow/docs/fulfillment-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([fulfillment, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_fulfillment.UpdateFulfillmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if fulfillment is not None:
            request.fulfillment = fulfillment
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_fulfillment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("fulfillment.name", request.fulfillment.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

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


__all__ = ("FulfillmentsAsyncClient",)
