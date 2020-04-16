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
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    pagers,
)
from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import RecaptchaEnterpriseServiceTransport
from .transports.grpc import RecaptchaEnterpriseServiceGrpcTransport


class RecaptchaEnterpriseServiceClientMeta(type):
    """Metaclass for the RecaptchaEnterpriseService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[RecaptchaEnterpriseServiceTransport]]
    _transport_registry["grpc"] = RecaptchaEnterpriseServiceGrpcTransport

    def get_transport_class(
        cls, label: str = None
    ) -> Type[RecaptchaEnterpriseServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class RecaptchaEnterpriseServiceClient(metaclass=RecaptchaEnterpriseServiceClientMeta):
    """Service to determine the likelihood an event is legitimate."""

    DEFAULT_OPTIONS = ClientOptions.ClientOptions(
        api_endpoint="recaptchaenterprise.googleapis.com"
    )

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
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def key_path(project: str, key: str) -> str:
        """Return a fully-qualified key string."""
        return "projects/{project}/keys/{key}".format(project=project, key=key)

    @staticmethod
    def assessment_path(project: str, assessment: str) -> str:
        """Return a fully-qualified assessment string."""
        return "projects/{project}/assessments/{assessment}".format(
            project=project, assessment=assessment
        )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, RecaptchaEnterpriseServiceTransport] = None,
        client_options: ClientOptions = DEFAULT_OPTIONS,
    ) -> None:
        """Instantiate the recaptcha enterprise service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.RecaptchaEnterpriseServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, RecaptchaEnterpriseServiceTransport):
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                host=client_options.api_endpoint
                or "recaptchaenterprise.googleapis.com",
            )

    def create_assessment(
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
            request (:class:`~.recaptchaenterprise.CreateAssessmentRequest`):
                The request object. The create assessment request
                message.
            parent (:class:`str`):
                Required. The name of the project in
                which the assessment will be created, in
                the format "projects/{project}".
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            assessment (:class:`~.recaptchaenterprise.Assessment`):
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
            ~.recaptchaenterprise.Assessment:
                A recaptcha assessment resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, assessment]):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_assessment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def annotate_assessment(
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
            request (:class:`~.recaptchaenterprise.AnnotateAssessmentRequest`):
                The request object. The request message to annotate an
                Assessment.
            name (:class:`str`):
                Required. The resource name of the
                Assessment, in the format
                "projects/{project}/assessments/{assessment}".
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            annotation (:class:`~.recaptchaenterprise.AnnotateAssessmentRequest.Annotation`):
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
            ~.recaptchaenterprise.AnnotateAssessmentResponse:
                Empty response for
                AnnotateAssessment.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, annotation]):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.annotate_assessment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def create_key(
        self,
        request: recaptchaenterprise.CreateKeyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Creates a new reCAPTCHA Enterprise key.

        Args:
            request (:class:`~.recaptchaenterprise.CreateKeyRequest`):
                The request object. The create key request message.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.recaptchaenterprise.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.

        request = recaptchaenterprise.CreateKeyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_key, default_timeout=None, client_info=_client_info
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_keys(
        self,
        request: recaptchaenterprise.ListKeysRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListKeysPager:
        r"""Returns the list of all keys that belong to a
        project.

        Args:
            request (:class:`~.recaptchaenterprise.ListKeysRequest`):
                The request object. The list keys request message.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListKeysPager:
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_keys, default_timeout=None, client_info=_client_info
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListKeysPager(method=rpc, request=request, response=response)

        # Done; return the response.
        return response

    def get_key(
        self,
        request: recaptchaenterprise.GetKeyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Returns the specified key.

        Args:
            request (:class:`~.recaptchaenterprise.GetKeyRequest`):
                The request object. The get key request message.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.recaptchaenterprise.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.

        request = recaptchaenterprise.GetKeyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_key, default_timeout=None, client_info=_client_info
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def update_key(
        self,
        request: recaptchaenterprise.UpdateKeyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Updates the specified key.

        Args:
            request (:class:`~.recaptchaenterprise.UpdateKeyRequest`):
                The request object. The update key request message.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.recaptchaenterprise.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.

        request = recaptchaenterprise.UpdateKeyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_key, default_timeout=None, client_info=_client_info
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def delete_key(
        self,
        request: recaptchaenterprise.DeleteKeyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified key.

        Args:
            request (:class:`~.recaptchaenterprise.DeleteKeyRequest`):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_key, default_timeout=None, client_info=_client_info
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-recaptcha-enterprise"
        ).version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("RecaptchaEnterpriseServiceClient",)
