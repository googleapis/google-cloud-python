# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import logging as std_logging
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
import google.protobuf

from google.shopping.merchant_issueresolution_v1beta import (
    gapic_version as package_version,
)

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.shopping.merchant_issueresolution_v1beta.types import issueresolution

from .client import IssueResolutionServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, IssueResolutionServiceTransport
from .transports.grpc_asyncio import IssueResolutionServiceGrpcAsyncIOTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class IssueResolutionServiceAsyncClient:
    """Service to provide an issue resolution content for account
    issues and product issues.
    """

    _client: IssueResolutionServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = IssueResolutionServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = IssueResolutionServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = IssueResolutionServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = IssueResolutionServiceClient._DEFAULT_UNIVERSE

    account_path = staticmethod(IssueResolutionServiceClient.account_path)
    parse_account_path = staticmethod(IssueResolutionServiceClient.parse_account_path)
    product_path = staticmethod(IssueResolutionServiceClient.product_path)
    parse_product_path = staticmethod(IssueResolutionServiceClient.parse_product_path)
    common_billing_account_path = staticmethod(
        IssueResolutionServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        IssueResolutionServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(IssueResolutionServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        IssueResolutionServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        IssueResolutionServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        IssueResolutionServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(IssueResolutionServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        IssueResolutionServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        IssueResolutionServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        IssueResolutionServiceClient.parse_common_location_path
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
            IssueResolutionServiceAsyncClient: The constructed client.
        """
        return IssueResolutionServiceClient.from_service_account_info.__func__(IssueResolutionServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            IssueResolutionServiceAsyncClient: The constructed client.
        """
        return IssueResolutionServiceClient.from_service_account_file.__func__(IssueResolutionServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return IssueResolutionServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> IssueResolutionServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            IssueResolutionServiceTransport: The transport used by the client instance.
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

    get_transport_class = IssueResolutionServiceClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                IssueResolutionServiceTransport,
                Callable[..., IssueResolutionServiceTransport],
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the issue resolution service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,IssueResolutionServiceTransport,Callable[..., IssueResolutionServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the IssueResolutionServiceTransport constructor.
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
        self._client = IssueResolutionServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

        if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        ):  # pragma: NO COVER
            _LOGGER.debug(
                "Created client `google.shopping.merchant.issueresolution_v1beta.IssueResolutionServiceAsyncClient`.",
                extra={
                    "serviceName": "google.shopping.merchant.issueresolution.v1beta.IssueResolutionService",
                    "universeDomain": getattr(
                        self._client._transport._credentials, "universe_domain", ""
                    ),
                    "credentialsType": f"{type(self._client._transport._credentials).__module__}.{type(self._client._transport._credentials).__qualname__}",
                    "credentialsInfo": getattr(
                        self.transport._credentials, "get_cred_info", lambda: None
                    )(),
                }
                if hasattr(self._client._transport, "_credentials")
                else {
                    "serviceName": "google.shopping.merchant.issueresolution.v1beta.IssueResolutionService",
                    "credentialsType": None,
                },
            )

    async def render_account_issues(
        self,
        request: Optional[
            Union[issueresolution.RenderAccountIssuesRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> issueresolution.RenderAccountIssuesResponse:
        r"""Provide a list of business's account issues with an
        issue resolution content and available actions. This
        content and actions are meant to be rendered and shown
        in third-party applications.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_issueresolution_v1beta

            async def sample_render_account_issues():
                # Create a client
                client = merchant_issueresolution_v1beta.IssueResolutionServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_issueresolution_v1beta.RenderAccountIssuesRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.render_account_issues(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_issueresolution_v1beta.types.RenderAccountIssuesRequest, dict]]):
                The request object. Request to provide issue resolution
                content and actions for business's
                account issues.
            name (:class:`str`):
                Required. The account to fetch issues for. Format:
                ``accounts/{account}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.shopping.merchant_issueresolution_v1beta.types.RenderAccountIssuesResponse:
                Response containing an issue
                resolution content and actions for
                listed account issues.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, issueresolution.RenderAccountIssuesRequest):
            request = issueresolution.RenderAccountIssuesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.render_account_issues
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

    async def render_product_issues(
        self,
        request: Optional[
            Union[issueresolution.RenderProductIssuesRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> issueresolution.RenderProductIssuesResponse:
        r"""Provide a list of issues for business's product with
        an issue resolution content and available actions. This
        content and actions are meant to be rendered and shown
        in third-party applications.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_issueresolution_v1beta

            async def sample_render_product_issues():
                # Create a client
                client = merchant_issueresolution_v1beta.IssueResolutionServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_issueresolution_v1beta.RenderProductIssuesRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.render_product_issues(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_issueresolution_v1beta.types.RenderProductIssuesRequest, dict]]):
                The request object. Request to provide an issue
                resolution content and actions for
                product issues of business's product.
            name (:class:`str`):
                Required. The name of the product to fetch issues for.
                Format: ``accounts/{account}/products/{product}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.shopping.merchant_issueresolution_v1beta.types.RenderProductIssuesResponse:
                Response containing an issue
                resolution content and actions for
                listed product issues.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, issueresolution.RenderProductIssuesRequest):
            request = issueresolution.RenderProductIssuesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.render_product_issues
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

    async def trigger_action(
        self,
        request: Optional[Union[issueresolution.TriggerActionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> issueresolution.TriggerActionResponse:
        r"""Start an action. The action can be requested by a business in
        third-party application. Before the business can request the
        action, the third-party application needs to show them action
        specific content and display a user input form.

        The action can be successfully started only once all
        ``required`` inputs are provided. If any ``required`` input is
        missing, or invalid value was provided, the service will return
        400 error. Validation errors will contain
        [Ids][google.shopping.merchant.issueresolution.v1beta.InputField.id]
        for all problematic field together with translated, human
        readable error messages that can be shown to the user.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_issueresolution_v1beta

            async def sample_trigger_action():
                # Create a client
                client = merchant_issueresolution_v1beta.IssueResolutionServiceAsyncClient()

                # Initialize request argument(s)
                payload = merchant_issueresolution_v1beta.TriggerActionPayload()
                payload.action_context = "action_context_value"
                payload.action_input.action_flow_id = "action_flow_id_value"
                payload.action_input.input_values.text_input_value.value = "value_value"
                payload.action_input.input_values.input_field_id = "input_field_id_value"

                request = merchant_issueresolution_v1beta.TriggerActionRequest(
                    name="name_value",
                    payload=payload,
                )

                # Make the request
                response = await client.trigger_action(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_issueresolution_v1beta.types.TriggerActionRequest, dict]]):
                The request object. Request to start the selected action
            name (:class:`str`):
                Required. The business's account that is triggering the
                action. Format: ``accounts/{account}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.shopping.merchant_issueresolution_v1beta.types.TriggerActionResponse:
                Response informing about the started
                action.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, issueresolution.TriggerActionRequest):
            request = issueresolution.TriggerActionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.trigger_action
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

    async def __aenter__(self) -> "IssueResolutionServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


__all__ = ("IssueResolutionServiceAsyncClient",)
