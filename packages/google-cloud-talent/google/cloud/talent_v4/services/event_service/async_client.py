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

from google.cloud.talent_v4.types import event
from google.cloud.talent_v4.types import event_service
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import EventServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import EventServiceGrpcAsyncIOTransport
from .client import EventServiceClient


class EventServiceAsyncClient:
    """A service handles client event report."""

    _client: EventServiceClient

    DEFAULT_ENDPOINT = EventServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = EventServiceClient.DEFAULT_MTLS_ENDPOINT

    tenant_path = staticmethod(EventServiceClient.tenant_path)
    parse_tenant_path = staticmethod(EventServiceClient.parse_tenant_path)
    common_billing_account_path = staticmethod(
        EventServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        EventServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(EventServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(EventServiceClient.parse_common_folder_path)
    common_organization_path = staticmethod(EventServiceClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        EventServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(EventServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        EventServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(EventServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        EventServiceClient.parse_common_location_path
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
            EventServiceAsyncClient: The constructed client.
        """
        return EventServiceClient.from_service_account_info.__func__(EventServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            EventServiceAsyncClient: The constructed client.
        """
        return EventServiceClient.from_service_account_file.__func__(EventServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> EventServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            EventServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(EventServiceClient).get_transport_class, type(EventServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, EventServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the event service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.EventServiceTransport]): The
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
        self._client = EventServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_client_event(
        self,
        request: event_service.CreateClientEventRequest = None,
        *,
        parent: str = None,
        client_event: event.ClientEvent = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> event.ClientEvent:
        r"""Report events issued when end user interacts with customer's
        application that uses Cloud Talent Solution. You may inspect the
        created events in `self service
        tools <https://console.cloud.google.com/talent-solution/overview>`__.
        `Learn
        more <https://cloud.google.com/talent-solution/docs/management-tools>`__
        about self service tools.

        Args:
            request (:class:`google.cloud.talent_v4.types.CreateClientEventRequest`):
                The request object. The report event request.
            parent (:class:`str`):
                Required. Resource name of the tenant under which the
                event is created.

                The format is
                "projects/{project_id}/tenants/{tenant_id}", for
                example, "projects/foo/tenants/bar".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            client_event (:class:`google.cloud.talent_v4.types.ClientEvent`):
                Required. Events issued when end user
                interacts with customer's application
                that uses Cloud Talent Solution.

                This corresponds to the ``client_event`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.ClientEvent:
                An event issued when an end user
                interacts with the application that
                implements Cloud Talent Solution.
                Providing this information improves the
                quality of results for the API clients,
                enabling the service to perform
                optimally. The number of events sent
                must be consistent with other calls,
                such as job searches, issued to the
                service by the client.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, client_event])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = event_service.CreateClientEventRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if client_event is not None:
            request.client_event = client_event

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_client_event,
            default_timeout=30.0,
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-talent",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("EventServiceAsyncClient",)
