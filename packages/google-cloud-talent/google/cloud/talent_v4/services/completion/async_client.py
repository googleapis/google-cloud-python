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

from google.cloud.talent_v4.types import common
from google.cloud.talent_v4.types import completion_service
from .transports.base import CompletionTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CompletionGrpcAsyncIOTransport
from .client import CompletionClient


class CompletionAsyncClient:
    """A service handles auto completion."""

    _client: CompletionClient

    DEFAULT_ENDPOINT = CompletionClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CompletionClient.DEFAULT_MTLS_ENDPOINT

    company_path = staticmethod(CompletionClient.company_path)
    parse_company_path = staticmethod(CompletionClient.parse_company_path)
    tenant_path = staticmethod(CompletionClient.tenant_path)
    parse_tenant_path = staticmethod(CompletionClient.parse_tenant_path)
    common_billing_account_path = staticmethod(
        CompletionClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CompletionClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CompletionClient.common_folder_path)
    parse_common_folder_path = staticmethod(CompletionClient.parse_common_folder_path)
    common_organization_path = staticmethod(CompletionClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        CompletionClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CompletionClient.common_project_path)
    parse_common_project_path = staticmethod(CompletionClient.parse_common_project_path)
    common_location_path = staticmethod(CompletionClient.common_location_path)
    parse_common_location_path = staticmethod(
        CompletionClient.parse_common_location_path
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
            CompletionAsyncClient: The constructed client.
        """
        return CompletionClient.from_service_account_info.__func__(CompletionAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CompletionAsyncClient: The constructed client.
        """
        return CompletionClient.from_service_account_file.__func__(CompletionAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CompletionTransport:
        """Returns the transport used by the client instance.

        Returns:
            CompletionTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CompletionClient).get_transport_class, type(CompletionClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CompletionTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the completion client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CompletionTransport]): The
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
        self._client = CompletionClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def complete_query(
        self,
        request: completion_service.CompleteQueryRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> completion_service.CompleteQueryResponse:
        r"""Completes the specified prefix with keyword
        suggestions. Intended for use by a job search auto-
        complete search box.

        Args:
            request (:class:`google.cloud.talent_v4.types.CompleteQueryRequest`):
                The request object. Auto-complete parameters.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.CompleteQueryResponse:
                Response of auto-complete query.
        """
        # Create or coerce a protobuf request object.
        request = completion_service.CompleteQueryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.complete_query,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("tenant", request.tenant),)),
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


__all__ = ("CompletionAsyncClient",)
