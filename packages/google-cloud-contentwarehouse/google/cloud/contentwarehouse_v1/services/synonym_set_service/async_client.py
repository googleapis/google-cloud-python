# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import re
from typing import (
    Callable,
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
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.contentwarehouse_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.longrunning import operations_pb2  # type: ignore

from google.cloud.contentwarehouse_v1.services.synonym_set_service import pagers
from google.cloud.contentwarehouse_v1.types import (
    synonymset,
    synonymset_service_request,
)

from .client import SynonymSetServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, SynonymSetServiceTransport
from .transports.grpc_asyncio import SynonymSetServiceGrpcAsyncIOTransport


class SynonymSetServiceAsyncClient:
    """A Service that manage/custom customer specified SynonymSets."""

    _client: SynonymSetServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = SynonymSetServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SynonymSetServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = SynonymSetServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = SynonymSetServiceClient._DEFAULT_UNIVERSE

    location_path = staticmethod(SynonymSetServiceClient.location_path)
    parse_location_path = staticmethod(SynonymSetServiceClient.parse_location_path)
    synonym_set_path = staticmethod(SynonymSetServiceClient.synonym_set_path)
    parse_synonym_set_path = staticmethod(
        SynonymSetServiceClient.parse_synonym_set_path
    )
    common_billing_account_path = staticmethod(
        SynonymSetServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        SynonymSetServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(SynonymSetServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        SynonymSetServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        SynonymSetServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        SynonymSetServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(SynonymSetServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        SynonymSetServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(SynonymSetServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        SynonymSetServiceClient.parse_common_location_path
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
            SynonymSetServiceAsyncClient: The constructed client.
        """
        return SynonymSetServiceClient.from_service_account_info.__func__(SynonymSetServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            SynonymSetServiceAsyncClient: The constructed client.
        """
        return SynonymSetServiceClient.from_service_account_file.__func__(SynonymSetServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return SynonymSetServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> SynonymSetServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            SynonymSetServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = SynonymSetServiceClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                SynonymSetServiceTransport,
                Callable[..., SynonymSetServiceTransport],
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the synonym set service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,SynonymSetServiceTransport,Callable[..., SynonymSetServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the SynonymSetServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = SynonymSetServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_synonym_set(
        self,
        request: Optional[
            Union[synonymset_service_request.CreateSynonymSetRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        synonym_set: Optional[synonymset.SynonymSet] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> synonymset.SynonymSet:
        r"""Creates a SynonymSet for a single context. Throws an
        ALREADY_EXISTS exception if a synonymset already exists for the
        context.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_create_synonym_set():
                # Create a client
                client = contentwarehouse_v1.SynonymSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.CreateSynonymSetRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_synonym_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.CreateSynonymSetRequest, dict]]):
                The request object. Request message for
                SynonymSetService.CreateSynonymSet.
            parent (:class:`str`):
                Required. The parent name. Format:
                projects/{project_number}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            synonym_set (:class:`google.cloud.contentwarehouse_v1.types.SynonymSet`):
                Required. The synonymSet to be
                created for a context

                This corresponds to the ``synonym_set`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.SynonymSet:
                Represents a list of synonyms for a
                given context. For example a context
                "sales" could contain:

                Synonym 1: sale, invoice, bill, order
                Synonym 2: money, credit, finance,
                payment Synonym 3: shipping, freight,
                transport
                Each SynonymSets should be disjoint

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, synonym_set])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, synonymset_service_request.CreateSynonymSetRequest):
            request = synonymset_service_request.CreateSynonymSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if synonym_set is not None:
            request.synonym_set = synonym_set

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.create_synonym_set
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_synonym_set(
        self,
        request: Optional[
            Union[synonymset_service_request.GetSynonymSetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> synonymset.SynonymSet:
        r"""Gets a SynonymSet for a particular context. Throws a NOT_FOUND
        exception if the Synonymset does not exist

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_get_synonym_set():
                # Create a client
                client = contentwarehouse_v1.SynonymSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.GetSynonymSetRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_synonym_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.GetSynonymSetRequest, dict]]):
                The request object. Request message for
                SynonymSetService.GetSynonymSet. Will
                return synonymSet for a certain context.
            name (:class:`str`):
                Required. The name of the synonymSet to retrieve Format:
                projects/{project_number}/locations/{location}/synonymSets/{context}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.SynonymSet:
                Represents a list of synonyms for a
                given context. For example a context
                "sales" could contain:

                Synonym 1: sale, invoice, bill, order
                Synonym 2: money, credit, finance,
                payment Synonym 3: shipping, freight,
                transport
                Each SynonymSets should be disjoint

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, synonymset_service_request.GetSynonymSetRequest):
            request = synonymset_service_request.GetSynonymSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.get_synonym_set
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_synonym_set(
        self,
        request: Optional[
            Union[synonymset_service_request.UpdateSynonymSetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        synonym_set: Optional[synonymset.SynonymSet] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> synonymset.SynonymSet:
        r"""Remove the existing SynonymSet for the context and replaces it
        with a new one. Throws a NOT_FOUND exception if the SynonymSet
        is not found.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_update_synonym_set():
                # Create a client
                client = contentwarehouse_v1.SynonymSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.UpdateSynonymSetRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.update_synonym_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.UpdateSynonymSetRequest, dict]]):
                The request object. Request message for
                SynonymSetService.UpdateSynonymSet.
                Removes the SynonymSet for the specified
                context and replaces it with the
                SynonymSet in this request.
            name (:class:`str`):
                Required. The name of the synonymSet to update Format:
                projects/{project_number}/locations/{location}/synonymSets/{context}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            synonym_set (:class:`google.cloud.contentwarehouse_v1.types.SynonymSet`):
                Required. The synonymSet to be
                updated for the customer

                This corresponds to the ``synonym_set`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.types.SynonymSet:
                Represents a list of synonyms for a
                given context. For example a context
                "sales" could contain:

                Synonym 1: sale, invoice, bill, order
                Synonym 2: money, credit, finance,
                payment Synonym 3: shipping, freight,
                transport
                Each SynonymSets should be disjoint

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, synonym_set])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, synonymset_service_request.UpdateSynonymSetRequest):
            request = synonymset_service_request.UpdateSynonymSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if synonym_set is not None:
            request.synonym_set = synonym_set

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.update_synonym_set
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_synonym_set(
        self,
        request: Optional[
            Union[synonymset_service_request.DeleteSynonymSetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a SynonymSet for a given context. Throws a NOT_FOUND
        exception if the SynonymSet is not found.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_delete_synonym_set():
                # Create a client
                client = contentwarehouse_v1.SynonymSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.DeleteSynonymSetRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_synonym_set(request=request)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.DeleteSynonymSetRequest, dict]]):
                The request object. Request message for
                SynonymSetService.DeleteSynonymSet.
            name (:class:`str`):
                Required. The name of the synonymSet to delete Format:
                projects/{project_number}/locations/{location}/synonymSets/{context}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, synonymset_service_request.DeleteSynonymSetRequest):
            request = synonymset_service_request.DeleteSynonymSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.delete_synonym_set
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_synonym_sets(
        self,
        request: Optional[
            Union[synonymset_service_request.ListSynonymSetsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSynonymSetsAsyncPager:
        r"""Returns all SynonymSets (for all contexts) for the
        specified location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contentwarehouse_v1

            async def sample_list_synonym_sets():
                # Create a client
                client = contentwarehouse_v1.SynonymSetServiceAsyncClient()

                # Initialize request argument(s)
                request = contentwarehouse_v1.ListSynonymSetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_synonym_sets(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.contentwarehouse_v1.types.ListSynonymSetsRequest, dict]]):
                The request object. Request message for
                SynonymSetService.ListSynonymSets. Will
                return all synonymSets belonging to the
                customer project.
            parent (:class:`str`):
                Required. The parent name. Format:
                projects/{project_number}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contentwarehouse_v1.services.synonym_set_service.pagers.ListSynonymSetsAsyncPager:
                Response message for
                SynonymSetService.ListSynonymSets.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, synonymset_service_request.ListSynonymSetsRequest):
            request = synonymset_service_request.ListSynonymSetsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_synonym_sets
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListSynonymSetsAsyncPager(
            method=rpc,
            request=request,
            response=response,
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
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
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
        rpc = self.transport._wrapped_methods[self._client._transport.get_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "SynonymSetServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("SynonymSetServiceAsyncClient",)
