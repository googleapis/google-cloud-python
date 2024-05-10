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
import functools
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

from google.cloud.binaryauthorization_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.cloud.binaryauthorization_v1.types import service

from .client import ValidationHelperV1Client
from .transports.base import DEFAULT_CLIENT_INFO, ValidationHelperV1Transport
from .transports.grpc_asyncio import ValidationHelperV1GrpcAsyncIOTransport


class ValidationHelperV1AsyncClient:
    """BinAuthz Attestor verification"""

    _client: ValidationHelperV1Client

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = ValidationHelperV1Client.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ValidationHelperV1Client.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = ValidationHelperV1Client._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = ValidationHelperV1Client._DEFAULT_UNIVERSE

    common_billing_account_path = staticmethod(
        ValidationHelperV1Client.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ValidationHelperV1Client.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ValidationHelperV1Client.common_folder_path)
    parse_common_folder_path = staticmethod(
        ValidationHelperV1Client.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ValidationHelperV1Client.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ValidationHelperV1Client.parse_common_organization_path
    )
    common_project_path = staticmethod(ValidationHelperV1Client.common_project_path)
    parse_common_project_path = staticmethod(
        ValidationHelperV1Client.parse_common_project_path
    )
    common_location_path = staticmethod(ValidationHelperV1Client.common_location_path)
    parse_common_location_path = staticmethod(
        ValidationHelperV1Client.parse_common_location_path
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
            ValidationHelperV1AsyncClient: The constructed client.
        """
        return ValidationHelperV1Client.from_service_account_info.__func__(ValidationHelperV1AsyncClient, info, *args, **kwargs)  # type: ignore

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
            ValidationHelperV1AsyncClient: The constructed client.
        """
        return ValidationHelperV1Client.from_service_account_file.__func__(ValidationHelperV1AsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return ValidationHelperV1Client.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ValidationHelperV1Transport:
        """Returns the transport used by the client instance.

        Returns:
            ValidationHelperV1Transport: The transport used by the client instance.
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

    get_transport_class = functools.partial(
        type(ValidationHelperV1Client).get_transport_class,
        type(ValidationHelperV1Client),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                ValidationHelperV1Transport,
                Callable[..., ValidationHelperV1Transport],
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the validation helper v1 async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ValidationHelperV1Transport,Callable[..., ValidationHelperV1Transport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ValidationHelperV1Transport constructor.
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
        self._client = ValidationHelperV1Client(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def validate_attestation_occurrence(
        self,
        request: Optional[
            Union[service.ValidateAttestationOccurrenceRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.ValidateAttestationOccurrenceResponse:
        r"""Returns whether the given Attestation for the given
        image URI was signed by the given Attestor

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import binaryauthorization_v1

            async def sample_validate_attestation_occurrence():
                # Create a client
                client = binaryauthorization_v1.ValidationHelperV1AsyncClient()

                # Initialize request argument(s)
                request = binaryauthorization_v1.ValidateAttestationOccurrenceRequest(
                    attestor="attestor_value",
                    occurrence_note="occurrence_note_value",
                    occurrence_resource_uri="occurrence_resource_uri_value",
                )

                # Make the request
                response = await client.validate_attestation_occurrence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.binaryauthorization_v1.types.ValidateAttestationOccurrenceRequest, dict]]):
                The request object. Request message for
                [ValidationHelperV1.ValidateAttestationOccurrence][google.cloud.binaryauthorization.v1.ValidationHelperV1.ValidateAttestationOccurrence].
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.binaryauthorization_v1.types.ValidateAttestationOccurrenceResponse:
                Response message for
                   [ValidationHelperV1.ValidateAttestationOccurrence][google.cloud.binaryauthorization.v1.ValidationHelperV1.ValidateAttestationOccurrence].

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, service.ValidateAttestationOccurrenceRequest):
            request = service.ValidateAttestationOccurrenceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.validate_attestation_occurrence
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("attestor", request.attestor),)),
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

    async def __aenter__(self) -> "ValidationHelperV1AsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ValidationHelperV1AsyncClient",)
