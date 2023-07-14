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

from google.cloud.recaptchaenterprise_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    pagers,
)
from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise

from .client import RecaptchaEnterpriseServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, RecaptchaEnterpriseServiceTransport
from .transports.grpc_asyncio import RecaptchaEnterpriseServiceGrpcAsyncIOTransport


class RecaptchaEnterpriseServiceAsyncClient:
    """Service to determine the likelihood an event is legitimate."""

    _client: RecaptchaEnterpriseServiceClient

    DEFAULT_ENDPOINT = RecaptchaEnterpriseServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = RecaptchaEnterpriseServiceClient.DEFAULT_MTLS_ENDPOINT

    assessment_path = staticmethod(RecaptchaEnterpriseServiceClient.assessment_path)
    parse_assessment_path = staticmethod(
        RecaptchaEnterpriseServiceClient.parse_assessment_path
    )
    key_path = staticmethod(RecaptchaEnterpriseServiceClient.key_path)
    parse_key_path = staticmethod(RecaptchaEnterpriseServiceClient.parse_key_path)
    metrics_path = staticmethod(RecaptchaEnterpriseServiceClient.metrics_path)
    parse_metrics_path = staticmethod(
        RecaptchaEnterpriseServiceClient.parse_metrics_path
    )
    related_account_group_path = staticmethod(
        RecaptchaEnterpriseServiceClient.related_account_group_path
    )
    parse_related_account_group_path = staticmethod(
        RecaptchaEnterpriseServiceClient.parse_related_account_group_path
    )
    related_account_group_membership_path = staticmethod(
        RecaptchaEnterpriseServiceClient.related_account_group_membership_path
    )
    parse_related_account_group_membership_path = staticmethod(
        RecaptchaEnterpriseServiceClient.parse_related_account_group_membership_path
    )
    common_billing_account_path = staticmethod(
        RecaptchaEnterpriseServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        RecaptchaEnterpriseServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(
        RecaptchaEnterpriseServiceClient.common_folder_path
    )
    parse_common_folder_path = staticmethod(
        RecaptchaEnterpriseServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        RecaptchaEnterpriseServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        RecaptchaEnterpriseServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        RecaptchaEnterpriseServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        RecaptchaEnterpriseServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        RecaptchaEnterpriseServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        RecaptchaEnterpriseServiceClient.parse_common_location_path
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
            RecaptchaEnterpriseServiceAsyncClient: The constructed client.
        """
        return RecaptchaEnterpriseServiceClient.from_service_account_info.__func__(RecaptchaEnterpriseServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            RecaptchaEnterpriseServiceAsyncClient: The constructed client.
        """
        return RecaptchaEnterpriseServiceClient.from_service_account_file.__func__(RecaptchaEnterpriseServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return RecaptchaEnterpriseServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> RecaptchaEnterpriseServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            RecaptchaEnterpriseServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(RecaptchaEnterpriseServiceClient).get_transport_class,
        type(RecaptchaEnterpriseServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, RecaptchaEnterpriseServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the recaptcha enterprise service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.RecaptchaEnterpriseServiceTransport]): The
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
        self._client = RecaptchaEnterpriseServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_assessment(
        self,
        request: Optional[
            Union[recaptchaenterprise.CreateAssessmentRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        assessment: Optional[recaptchaenterprise.Assessment] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Assessment:
        r"""Creates an Assessment of the likelihood an event is
        legitimate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_create_assessment():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.CreateAssessmentRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_assessment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.CreateAssessmentRequest, dict]]):
                The request object. The create assessment request
                message.
            parent (:class:`str`):
                Required. The name of the project in
                which the assessment will be created, in
                the format "projects/{project}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            assessment (:class:`google.cloud.recaptchaenterprise_v1.types.Assessment`):
                Required. The assessment details.
                This corresponds to the ``assessment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Assessment:
                A reCAPTCHA Enterprise assessment
                resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, assessment])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.CreateAssessmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if assessment is not None:
            request.assessment = assessment

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_assessment,
            default_timeout=600.0,
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

    async def annotate_assessment(
        self,
        request: Optional[
            Union[recaptchaenterprise.AnnotateAssessmentRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        annotation: Optional[
            recaptchaenterprise.AnnotateAssessmentRequest.Annotation
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.AnnotateAssessmentResponse:
        r"""Annotates a previously created Assessment to provide
        additional information on whether the event turned out
        to be authentic or fraudulent.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_annotate_assessment():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.AnnotateAssessmentRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.annotate_assessment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentRequest, dict]]):
                The request object. The request message to annotate an
                Assessment.
            name (:class:`str`):
                Required. The resource name of the
                Assessment, in the format
                "projects/{project}/assessments/{assessment}".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            annotation (:class:`google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentRequest.Annotation`):
                Optional. The annotation that will be
                assigned to the Event. This field can be
                left empty to provide reasons that apply
                to an event without concluding whether
                the event is legitimate or fraudulent.

                This corresponds to the ``annotation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentResponse:
                Empty response for
                AnnotateAssessment.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, annotation])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.AnnotateAssessmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if annotation is not None:
            request.annotation = annotation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.annotate_assessment,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    async def create_key(
        self,
        request: Optional[Union[recaptchaenterprise.CreateKeyRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        key: Optional[recaptchaenterprise.Key] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Creates a new reCAPTCHA Enterprise key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_create_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                key = recaptchaenterprise_v1.Key()
                key.web_settings.integration_type = "INVISIBLE"

                request = recaptchaenterprise_v1.CreateKeyRequest(
                    parent="parent_value",
                    key=key,
                )

                # Make the request
                response = await client.create_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.CreateKeyRequest, dict]]):
                The request object. The create key request message.
            parent (:class:`str`):
                Required. The name of the project in
                which the key will be created, in the
                format "projects/{project}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            key (:class:`google.cloud.recaptchaenterprise_v1.types.Key`):
                Required. Information to create a
                reCAPTCHA Enterprise key.

                This corresponds to the ``key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, key])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.CreateKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if key is not None:
            request.key = key

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_key,
            default_timeout=600.0,
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

    async def list_keys(
        self,
        request: Optional[Union[recaptchaenterprise.ListKeysRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListKeysAsyncPager:
        r"""Returns the list of all keys that belong to a
        project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_list_keys():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.ListKeysRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_keys(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.ListKeysRequest, dict]]):
                The request object. The list keys request message.
            parent (:class:`str`):
                Required. The name of the project
                that contains the keys that will be
                listed, in the format
                "projects/{project}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.pagers.ListKeysAsyncPager:
                Response to request to list keys in a
                project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.ListKeysRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_keys,
            default_timeout=600.0,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListKeysAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def retrieve_legacy_secret_key(
        self,
        request: Optional[
            Union[recaptchaenterprise.RetrieveLegacySecretKeyRequest, dict]
        ] = None,
        *,
        key: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.RetrieveLegacySecretKeyResponse:
        r"""Returns the secret key related to the specified
        public key. You must use the legacy secret key only in a
        3rd party integration with legacy reCAPTCHA.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_retrieve_legacy_secret_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.RetrieveLegacySecretKeyRequest(
                    key="key_value",
                )

                # Make the request
                response = await client.retrieve_legacy_secret_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.RetrieveLegacySecretKeyRequest, dict]]):
                The request object. The retrieve legacy secret key
                request message.
            key (:class:`str`):
                Required. The public key name linked
                to the requested secret key in the
                format "projects/{project}/keys/{key}".

                This corresponds to the ``key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.RetrieveLegacySecretKeyResponse:
                Secret key is used only in legacy
                reCAPTCHA. It must be used in a 3rd
                party integration with legacy reCAPTCHA.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([key])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.RetrieveLegacySecretKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if key is not None:
            request.key = key

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.retrieve_legacy_secret_key,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("key", request.key),)),
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

    async def get_key(
        self,
        request: Optional[Union[recaptchaenterprise.GetKeyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Returns the specified key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_get_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.GetKeyRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.GetKeyRequest, dict]]):
                The request object. The get key request message.
            name (:class:`str`):
                Required. The name of the requested
                key, in the format
                "projects/{project}/keys/{key}".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.GetKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_key,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    async def update_key(
        self,
        request: Optional[Union[recaptchaenterprise.UpdateKeyRequest, dict]] = None,
        *,
        key: Optional[recaptchaenterprise.Key] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Updates the specified key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_update_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                key = recaptchaenterprise_v1.Key()
                key.web_settings.integration_type = "INVISIBLE"

                request = recaptchaenterprise_v1.UpdateKeyRequest(
                    key=key,
                )

                # Make the request
                response = await client.update_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.UpdateKeyRequest, dict]]):
                The request object. The update key request message.
            key (:class:`google.cloud.recaptchaenterprise_v1.types.Key`):
                Required. The key to update.
                This corresponds to the ``key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. The mask to control which
                fields of the key get updated. If the
                mask is not present, all fields will be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([key, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.UpdateKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if key is not None:
            request.key = key
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_key,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("key.name", request.key.name),)),
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

    async def delete_key(
        self,
        request: Optional[Union[recaptchaenterprise.DeleteKeyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_delete_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.DeleteKeyRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_key(request=request)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.DeleteKeyRequest, dict]]):
                The request object. The delete key request message.
            name (:class:`str`):
                Required. The name of the key to be
                deleted, in the format
                "projects/{project}/keys/{key}".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.DeleteKeyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_key,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def migrate_key(
        self,
        request: Optional[Union[recaptchaenterprise.MigrateKeyRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Migrates an existing key from reCAPTCHA to reCAPTCHA
        Enterprise. Once a key is migrated, it can be used from
        either product. SiteVerify requests are billed as
        CreateAssessment calls. You must be authenticated as one
        of the current owners of the reCAPTCHA Site Key, and
        your user must have the reCAPTCHA Enterprise Admin IAM
        role in the destination project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_migrate_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.MigrateKeyRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.migrate_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.MigrateKeyRequest, dict]]):
                The request object. The migrate key request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.
        request = recaptchaenterprise.MigrateKeyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.migrate_key,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    async def get_metrics(
        self,
        request: Optional[Union[recaptchaenterprise.GetMetricsRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Metrics:
        r"""Get some aggregated metrics for a Key. This data can
        be used to build dashboards.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_get_metrics():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.GetMetricsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_metrics(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.GetMetricsRequest, dict]]):
                The request object. The get metrics request message.
            name (:class:`str`):
                Required. The name of the requested
                metrics, in the format
                "projects/{project}/keys/{key}/metrics".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Metrics:
                Metrics for a single Key.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.GetMetricsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_metrics,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    async def list_related_account_groups(
        self,
        request: Optional[
            Union[recaptchaenterprise.ListRelatedAccountGroupsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRelatedAccountGroupsAsyncPager:
        r"""List groups of related accounts.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_list_related_account_groups():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.ListRelatedAccountGroupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_related_account_groups(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsRequest, dict]]):
                The request object. The request message to list related
                account groups.
            parent (:class:`str`):
                Required. The name of the project to
                list related account groups from, in the
                format "projects/{project}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.pagers.ListRelatedAccountGroupsAsyncPager:
                The response to a ListRelatedAccountGroups call.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.ListRelatedAccountGroupsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_related_account_groups,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListRelatedAccountGroupsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_related_account_group_memberships(
        self,
        request: Optional[
            Union[recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRelatedAccountGroupMembershipsAsyncPager:
        r"""Get memberships in a group of related accounts.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_list_related_account_group_memberships():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.ListRelatedAccountGroupMembershipsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_related_account_group_memberships(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsRequest, dict]]):
                The request object. The request message to list
                memberships in a related account group.
            parent (:class:`str`):
                Required. The resource name for the related account
                group in the format
                ``projects/{project}/relatedaccountgroups/{relatedaccountgroup}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.pagers.ListRelatedAccountGroupMembershipsAsyncPager:
                The response to a ListRelatedAccountGroupMemberships
                call.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_related_account_group_memberships,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListRelatedAccountGroupMembershipsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def search_related_account_group_memberships(
        self,
        request: Optional[
            Union[recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        hashed_account_id: Optional[bytes] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchRelatedAccountGroupMembershipsAsyncPager:
        r"""Search group memberships related to a given account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            async def sample_search_related_account_group_memberships():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceAsyncClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.SearchRelatedAccountGroupMembershipsRequest(
                    project="project_value",
                )

                # Make the request
                page_result = client.search_related_account_group_memberships(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsRequest, dict]]):
                The request object. The request message to search related
                account group memberships.
            project (:class:`str`):
                Required. The name of the project to
                search related account group memberships
                from. Specify the project name in the
                following format:

                "projects/{project}".

                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            hashed_account_id (:class:`bytes`):
                Optional. The unique stable hashed user identifier we
                should search connections to. The identifier should
                correspond to a ``hashed_account_id`` provided in a
                previous ``CreateAssessment`` or ``AnnotateAssessment``
                call.

                This corresponds to the ``hashed_account_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.pagers.SearchRelatedAccountGroupMembershipsAsyncPager:
                The response to a SearchRelatedAccountGroupMemberships
                call.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, hashed_account_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project is not None:
            request.project = project
        if hashed_account_id is not None:
            request.hashed_account_id = hashed_account_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_related_account_group_memberships,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project", request.project),)),
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
        response = pagers.SearchRelatedAccountGroupMembershipsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "RecaptchaEnterpriseServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("RecaptchaEnterpriseServiceAsyncClient",)
