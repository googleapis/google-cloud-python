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

from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    pagers,
)
from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import RecaptchaEnterpriseServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import RecaptchaEnterpriseServiceGrpcAsyncIOTransport
from .client import RecaptchaEnterpriseServiceClient


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
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, RecaptchaEnterpriseServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
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
        request: recaptchaenterprise.CreateAssessmentRequest = None,
        *,
        parent: str = None,
        assessment: recaptchaenterprise.Assessment = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Assessment:
        r"""Creates an Assessment of the likelihood an event is
        legitimate.

        Args:
            request (:class:`google.cloud.recaptchaenterprise_v1.types.CreateAssessmentRequest`):
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
                A recaptcha assessment resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def annotate_assessment(
        self,
        request: recaptchaenterprise.AnnotateAssessmentRequest = None,
        *,
        name: str = None,
        annotation: recaptchaenterprise.AnnotateAssessmentRequest.Annotation = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.AnnotateAssessmentResponse:
        r"""Annotates a previously created Assessment to provide
        additional information on whether the event turned out
        to be authentic or fradulent.

        Args:
            request (:class:`google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentRequest`):
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
                Required. The annotation that will be
                assigned to the Event.

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
        # Sanity check: If we got a request object, we should *not* have
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_key(
        self,
        request: recaptchaenterprise.CreateKeyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Creates a new reCAPTCHA Enterprise key.

        Args:
            request (:class:`google.cloud.recaptchaenterprise_v1.types.CreateKeyRequest`):
                The request object. The create key request message.
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
        request = recaptchaenterprise.CreateKeyRequest(request)

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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_keys(
        self,
        request: recaptchaenterprise.ListKeysRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListKeysAsyncPager:
        r"""Returns the list of all keys that belong to a
        project.

        Args:
            request (:class:`google.cloud.recaptchaenterprise_v1.types.ListKeysRequest`):
                The request object. The list keys request message.
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
        request = recaptchaenterprise.ListKeysRequest(request)

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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListKeysAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_key(
        self,
        request: recaptchaenterprise.GetKeyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Returns the specified key.

        Args:
            request (:class:`google.cloud.recaptchaenterprise_v1.types.GetKeyRequest`):
                The request object. The get key request message.
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
        request = recaptchaenterprise.GetKeyRequest(request)

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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_key(
        self,
        request: recaptchaenterprise.UpdateKeyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Updates the specified key.

        Args:
            request (:class:`google.cloud.recaptchaenterprise_v1.types.UpdateKeyRequest`):
                The request object. The update key request message.
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
        request = recaptchaenterprise.UpdateKeyRequest(request)

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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_key(
        self,
        request: recaptchaenterprise.DeleteKeyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified key.

        Args:
            request (:class:`google.cloud.recaptchaenterprise_v1.types.DeleteKeyRequest`):
                The request object. The delete key request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = recaptchaenterprise.DeleteKeyRequest(request)

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
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-recaptcha-enterprise",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("RecaptchaEnterpriseServiceAsyncClient",)
