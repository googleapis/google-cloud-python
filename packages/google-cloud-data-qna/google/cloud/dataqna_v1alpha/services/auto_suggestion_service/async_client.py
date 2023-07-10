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

from google.cloud.dataqna_v1alpha import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.dataqna_v1alpha.types import auto_suggestion_service

from .client import AutoSuggestionServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, AutoSuggestionServiceTransport
from .transports.grpc_asyncio import AutoSuggestionServiceGrpcAsyncIOTransport


class AutoSuggestionServiceAsyncClient:
    """This stateless API provides automatic suggestions for natural
    language queries for the data sources in the provided project and
    location.

    The service provides a resourceless operation ``suggestQueries``
    that can be called to get a list of suggestions for a given
    incomplete query and scope (or list of scopes) under which the query
    is to be interpreted.

    There are two types of suggestions, ENTITY for single entity
    suggestions and TEMPLATE for full sentences. By default, both types
    are returned.

    Example Request:

    ::

       GetSuggestions({
         parent: "locations/us/projects/my-project"
         scopes:
         "//bigquery.googleapis.com/projects/my-project/datasets/my-dataset/tables/my-table"
         query: "top it"
       })

    The service will retrieve information based on the given scope(s)
    and give suggestions based on that (e.g. "top item" for "top it" if
    "item" is a known dimension for the provided scope).

    ::

       suggestions {
         suggestion_info {
           annotated_suggestion {
             text_formatted: "top item by sum of usd_revenue_net"
             markups {
               type: DIMENSION
               start_char_index: 4
               length: 4
             }
             markups {
               type: METRIC
               start_char_index: 19
               length: 15
             }
           }
           query_matches {
             start_char_index: 0
             length: 6
           }
         }
         suggestion_type: TEMPLATE
         ranking_score: 0.9
       }
       suggestions {
         suggestion_info {
           annotated_suggestion {
             text_formatted: "item"
             markups {
               type: DIMENSION
               start_char_index: 4
               length: 2
             }
           }
           query_matches {
             start_char_index: 0
             length: 6
           }
         }
         suggestion_type: ENTITY
         ranking_score: 0.8
       }
    """

    _client: AutoSuggestionServiceClient

    DEFAULT_ENDPOINT = AutoSuggestionServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AutoSuggestionServiceClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        AutoSuggestionServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AutoSuggestionServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AutoSuggestionServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AutoSuggestionServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AutoSuggestionServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AutoSuggestionServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AutoSuggestionServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        AutoSuggestionServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        AutoSuggestionServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        AutoSuggestionServiceClient.parse_common_location_path
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
            AutoSuggestionServiceAsyncClient: The constructed client.
        """
        return AutoSuggestionServiceClient.from_service_account_info.__func__(AutoSuggestionServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AutoSuggestionServiceAsyncClient: The constructed client.
        """
        return AutoSuggestionServiceClient.from_service_account_file.__func__(AutoSuggestionServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return AutoSuggestionServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> AutoSuggestionServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            AutoSuggestionServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AutoSuggestionServiceClient).get_transport_class,
        type(AutoSuggestionServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, AutoSuggestionServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the auto suggestion service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AutoSuggestionServiceTransport]): The
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
        self._client = AutoSuggestionServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def suggest_queries(
        self,
        request: Optional[
            Union[auto_suggestion_service.SuggestQueriesRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> auto_suggestion_service.SuggestQueriesResponse:
        r"""Gets a list of suggestions based on a prefix string.
        AutoSuggestion tolerance should be less than 1 second.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataqna_v1alpha

            async def sample_suggest_queries():
                # Create a client
                client = dataqna_v1alpha.AutoSuggestionServiceAsyncClient()

                # Initialize request argument(s)
                request = dataqna_v1alpha.SuggestQueriesRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.suggest_queries(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.dataqna_v1alpha.types.SuggestQueriesRequest, dict]]):
                The request object. Request for query suggestions.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataqna_v1alpha.types.SuggestQueriesResponse:
                Response to SuggestQueries.
        """
        # Create or coerce a protobuf request object.
        request = auto_suggestion_service.SuggestQueriesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.suggest_queries,
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

    async def __aenter__(self) -> "AutoSuggestionServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AutoSuggestionServiceAsyncClient",)
