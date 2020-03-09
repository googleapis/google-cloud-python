# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from google.cloud.recommendationengine_v1beta1.services.prediction_api_key_registry import (
    pagers,
)
from google.cloud.recommendationengine_v1beta1.types import (
    prediction_apikey_registry_service,
)

from .transports.base import PredictionApiKeyRegistryTransport
from .transports.grpc import PredictionApiKeyRegistryGrpcTransport


class PredictionApiKeyRegistryClientMeta(type):
    """Metaclass for the PredictionApiKeyRegistry client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[PredictionApiKeyRegistryTransport]]
    _transport_registry["grpc"] = PredictionApiKeyRegistryGrpcTransport

    def get_transport_class(
        cls, label: str = None
    ) -> Type[PredictionApiKeyRegistryTransport]:
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


class PredictionApiKeyRegistryClient(metaclass=PredictionApiKeyRegistryClientMeta):
    """Service for registering API keys for use with the ``predict``
    method. If you use an API key to request predictions, you must first
    register the API key. Otherwise, your prediction request is
    rejected. If you use OAuth to authenticate your ``predict`` method
    call, you do not need to register an API key. You can register up to
    20 API keys per project.
    """

    DEFAULT_OPTIONS = ClientOptions.ClientOptions(
        api_endpoint="recommendationengine.googleapis.com"
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

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, PredictionApiKeyRegistryTransport] = None,
        client_options: ClientOptions = DEFAULT_OPTIONS,
    ) -> None:
        """Instantiate the prediction api key registry client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.PredictionApiKeyRegistryTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, PredictionApiKeyRegistryTransport):
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
                or "recommendationengine.googleapis.com",
            )

    def create_prediction_api_key_registration(
        self,
        request: prediction_apikey_registry_service.CreatePredictionApiKeyRegistrationRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> prediction_apikey_registry_service.PredictionApiKeyRegistration:
        r"""Register an API key for use with predict method.

        Args:
            request (:class:`~.prediction_apikey_registry_service.CreatePredictionApiKeyRegistrationRequest`):
                The request object. Request message for the
                `CreatePredictionApiKeyRegistration` method.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.prediction_apikey_registry_service.PredictionApiKeyRegistration:
                Registered Api Key.
        """
        # Create or coerce a protobuf request object.

        request = prediction_apikey_registry_service.CreatePredictionApiKeyRegistrationRequest(
            request
        )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_prediction_api_key_registration,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_prediction_api_key_registrations(
        self,
        request: prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPredictionApiKeyRegistrationsPager:
        r"""List the registered apiKeys for use with predict
        method.

        Args:
            request (:class:`~.prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest`):
                The request object. Request message for the
                `ListPredictionApiKeyRegistrations`.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListPredictionApiKeyRegistrationsPager:
                Response message for the
                ``ListPredictionApiKeyRegistrations``.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.

        request = prediction_apikey_registry_service.ListPredictionApiKeyRegistrationsRequest(
            request
        )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_prediction_api_key_registrations,
            default_timeout=None,
            client_info=_client_info,
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
        response = pagers.ListPredictionApiKeyRegistrationsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def delete_prediction_api_key_registration(
        self,
        request: prediction_apikey_registry_service.DeletePredictionApiKeyRegistrationRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Unregister an apiKey from using for predict method.

        Args:
            request (:class:`~.prediction_apikey_registry_service.DeletePredictionApiKeyRegistrationRequest`):
                The request object. Request message for
                `DeletePredictionApiKeyRegistration` method.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.

        request = prediction_apikey_registry_service.DeletePredictionApiKeyRegistrationRequest(
            request
        )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_prediction_api_key_registration,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-recommendations-ai"
        ).version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("PredictionApiKeyRegistryClient",)
