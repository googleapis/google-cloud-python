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

from google.api_core import operation as gac_operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.appengine_admin_v1.types import appengine
from google.cloud.appengine_admin_v1.types import application
from google.cloud.appengine_admin_v1.types import operation as ga_operation
from google.protobuf import duration_pb2  # type: ignore
from .transports.base import ApplicationsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ApplicationsGrpcAsyncIOTransport
from .client import ApplicationsClient


class ApplicationsAsyncClient:
    """Manages App Engine applications."""

    _client: ApplicationsClient

    DEFAULT_ENDPOINT = ApplicationsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ApplicationsClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        ApplicationsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ApplicationsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ApplicationsClient.common_folder_path)
    parse_common_folder_path = staticmethod(ApplicationsClient.parse_common_folder_path)
    common_organization_path = staticmethod(ApplicationsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        ApplicationsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ApplicationsClient.common_project_path)
    parse_common_project_path = staticmethod(
        ApplicationsClient.parse_common_project_path
    )
    common_location_path = staticmethod(ApplicationsClient.common_location_path)
    parse_common_location_path = staticmethod(
        ApplicationsClient.parse_common_location_path
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
            ApplicationsAsyncClient: The constructed client.
        """
        return ApplicationsClient.from_service_account_info.__func__(ApplicationsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ApplicationsAsyncClient: The constructed client.
        """
        return ApplicationsClient.from_service_account_file.__func__(ApplicationsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ApplicationsTransport:
        """Returns the transport used by the client instance.

        Returns:
            ApplicationsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ApplicationsClient).get_transport_class, type(ApplicationsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ApplicationsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the applications client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ApplicationsTransport]): The
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
        self._client = ApplicationsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_application(
        self,
        request: appengine.GetApplicationRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> application.Application:
        r"""Gets information about an application.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.GetApplicationRequest`):
                The request object. Request message for
                `Applications.GetApplication`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.Application:
                An Application resource contains the
                top-level configuration of an App Engine
                application.

        """
        # Create or coerce a protobuf request object.
        request = appengine.GetApplicationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_application,
            default_timeout=None,
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

    async def create_application(
        self,
        request: appengine.CreateApplicationRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates an App Engine application for a Google Cloud Platform
        project. Required fields:

        -  ``id`` - The ID of the target Cloud Platform project.
        -  *location* - The
           `region <https://cloud.google.com/appengine/docs/locations>`__
           where you want the App Engine application located.

        For more information about App Engine applications, see
        `Managing Projects, Applications, and
        Billing <https://cloud.google.com/appengine/docs/standard/python/console/>`__.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.CreateApplicationRequest`):
                The request object. Request message for
                `Applications.CreateApplication`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.appengine_admin_v1.types.Application` An Application resource contains the top-level configuration of an App
                   Engine application.

        """
        # Create or coerce a protobuf request object.
        request = appengine.CreateApplicationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_application,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            application.Application,
            metadata_type=ga_operation.OperationMetadataV1,
        )

        # Done; return the response.
        return response

    async def update_application(
        self,
        request: appengine.UpdateApplicationRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the specified Application resource. You can update the
        following fields:

        -  ``auth_domain`` - Google authentication domain for
           controlling user access to the application.
        -  ``default_cookie_expiration`` - Cookie expiration policy for
           the application.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.UpdateApplicationRequest`):
                The request object. Request message for
                `Applications.UpdateApplication`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.appengine_admin_v1.types.Application` An Application resource contains the top-level configuration of an App
                   Engine application.

        """
        # Create or coerce a protobuf request object.
        request = appengine.UpdateApplicationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_application,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            application.Application,
            metadata_type=ga_operation.OperationMetadataV1,
        )

        # Done; return the response.
        return response

    async def repair_application(
        self,
        request: appengine.RepairApplicationRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Recreates the required App Engine features for the specified App
        Engine application, for example a Cloud Storage bucket or App
        Engine service account. Use this method if you receive an error
        message about a missing feature, for example, *Error retrieving
        the App Engine service account*. If you have deleted your App
        Engine service account, this will not be able to recreate it.
        Instead, you should attempt to use the IAM undelete API if
        possible at
        https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/undelete?apix_params=%7B"name"%3A"projects%2F-%2FserviceAccounts%2Funique_id"%2C"resource"%3A%7B%7D%7D
        . If the deletion was recent, the numeric ID can be found in the
        Cloud Console Activity Log.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.RepairApplicationRequest`):
                The request object. Request message for
                'Applications.RepairApplication'.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.appengine_admin_v1.types.Application` An Application resource contains the top-level configuration of an App
                   Engine application.

        """
        # Create or coerce a protobuf request object.
        request = appengine.RepairApplicationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.repair_application,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            application.Application,
            metadata_type=ga_operation.OperationMetadataV1,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-appengine-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ApplicationsAsyncClient",)
