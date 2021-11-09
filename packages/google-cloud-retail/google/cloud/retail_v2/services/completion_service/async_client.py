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

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.retail_v2.types import completion_service
from google.cloud.retail_v2.types import import_config
from .transports.base import CompletionServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CompletionServiceGrpcAsyncIOTransport
from .client import CompletionServiceClient


class CompletionServiceAsyncClient:
    """Auto-completion service for retail.

    This feature is only available for users who have Retail Search
    enabled. Please submit a form
    `here <https://cloud.google.com/contact>`__ to contact cloud sales
    if you are interested in using Retail Search.
    """

    _client: CompletionServiceClient

    DEFAULT_ENDPOINT = CompletionServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CompletionServiceClient.DEFAULT_MTLS_ENDPOINT

    catalog_path = staticmethod(CompletionServiceClient.catalog_path)
    parse_catalog_path = staticmethod(CompletionServiceClient.parse_catalog_path)
    common_billing_account_path = staticmethod(
        CompletionServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CompletionServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CompletionServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        CompletionServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        CompletionServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        CompletionServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CompletionServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        CompletionServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(CompletionServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        CompletionServiceClient.parse_common_location_path
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
            CompletionServiceAsyncClient: The constructed client.
        """
        return CompletionServiceClient.from_service_account_info.__func__(CompletionServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CompletionServiceAsyncClient: The constructed client.
        """
        return CompletionServiceClient.from_service_account_file.__func__(CompletionServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CompletionServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            CompletionServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CompletionServiceClient).get_transport_class, type(CompletionServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CompletionServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the completion service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CompletionServiceTransport]): The
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
        self._client = CompletionServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def complete_query(
        self,
        request: Union[completion_service.CompleteQueryRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> completion_service.CompleteQueryResponse:
        r"""Completes the specified prefix with keyword suggestions.

        This feature is only available for users who have Retail Search
        enabled. Please submit a form
        `here <https://cloud.google.com/contact>`__ to contact cloud
        sales if you are interested in using Retail Search.

        Args:
            request (Union[google.cloud.retail_v2.types.CompleteQueryRequest, dict]):
                The request object. Auto-complete parameters.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.retail_v2.types.CompleteQueryResponse:
                Response of the auto-complete query.
        """
        # Create or coerce a protobuf request object.
        request = completion_service.CompleteQueryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.complete_query,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("catalog", request.catalog),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def import_completion_data(
        self,
        request: Union[import_config.ImportCompletionDataRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Bulk import of processed completion dataset.

        Request processing may be synchronous. Partial updating is not
        supported.

        This feature is only available for users who have Retail Search
        enabled. Please submit a form
        `here <https://cloud.google.com/contact>`__ to contact cloud
        sales if you are interested in using Retail Search.

        Args:
            request (Union[google.cloud.retail_v2.types.ImportCompletionDataRequest, dict]):
                The request object. Request message for
                ImportCompletionData methods.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.retail_v2.types.ImportCompletionDataResponse` Response of the
                   [ImportCompletionDataRequest][google.cloud.retail.v2.ImportCompletionDataRequest].
                   If the long running operation is done, this message
                   is returned by the
                   google.longrunning.Operations.response field if the
                   operation is successful.

        """
        # Create or coerce a protobuf request object.
        request = import_config.ImportCompletionDataRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_completion_data,
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
            import_config.ImportCompletionDataResponse,
            metadata_type=import_config.ImportMetadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-retail",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CompletionServiceAsyncClient",)
