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

from google.cloud.talent_v4beta1.services.application_service import pagers
from google.cloud.talent_v4beta1.types import application
from google.cloud.talent_v4beta1.types import application as gct_application
from google.cloud.talent_v4beta1.types import application_service
from google.cloud.talent_v4beta1.types import common
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from .transports.base import ApplicationServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ApplicationServiceGrpcAsyncIOTransport
from .client import ApplicationServiceClient


class ApplicationServiceAsyncClient:
    """A service that handles application management, including CRUD
    and enumeration.
    """

    _client: ApplicationServiceClient

    DEFAULT_ENDPOINT = ApplicationServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ApplicationServiceClient.DEFAULT_MTLS_ENDPOINT

    application_path = staticmethod(ApplicationServiceClient.application_path)
    parse_application_path = staticmethod(
        ApplicationServiceClient.parse_application_path
    )
    company_path = staticmethod(ApplicationServiceClient.company_path)
    parse_company_path = staticmethod(ApplicationServiceClient.parse_company_path)
    job_path = staticmethod(ApplicationServiceClient.job_path)
    parse_job_path = staticmethod(ApplicationServiceClient.parse_job_path)
    profile_path = staticmethod(ApplicationServiceClient.profile_path)
    parse_profile_path = staticmethod(ApplicationServiceClient.parse_profile_path)
    common_billing_account_path = staticmethod(
        ApplicationServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ApplicationServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ApplicationServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ApplicationServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ApplicationServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ApplicationServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ApplicationServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ApplicationServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(ApplicationServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        ApplicationServiceClient.parse_common_location_path
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
            ApplicationServiceAsyncClient: The constructed client.
        """
        return ApplicationServiceClient.from_service_account_info.__func__(ApplicationServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ApplicationServiceAsyncClient: The constructed client.
        """
        return ApplicationServiceClient.from_service_account_file.__func__(ApplicationServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ApplicationServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ApplicationServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ApplicationServiceClient).get_transport_class,
        type(ApplicationServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ApplicationServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the application service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ApplicationServiceTransport]): The
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
        self._client = ApplicationServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_application(
        self,
        request: application_service.CreateApplicationRequest = None,
        *,
        parent: str = None,
        application: gct_application.Application = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_application.Application:
        r"""Creates a new application entity.

        Args:
            request (:class:`google.cloud.talent_v4beta1.types.CreateApplicationRequest`):
                The request object. The Request of the CreateApplication
                method.
            parent (:class:`str`):
                Required. Resource name of the profile under which the
                application is created.

                The format is
                "projects/{project_id}/tenants/{tenant_id}/profiles/{profile_id}".
                For example, "projects/foo/tenants/bar/profiles/baz".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            application (:class:`google.cloud.talent_v4beta1.types.Application`):
                Required. The application to be
                created.

                This corresponds to the ``application`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4beta1.types.Application:
                Resource that represents a job
                application record of a candidate.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, application])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = application_service.CreateApplicationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if application is not None:
            request.application = application

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_application,
            default_timeout=30.0,
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

    async def get_application(
        self,
        request: application_service.GetApplicationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> application.Application:
        r"""Retrieves specified application.

        Args:
            request (:class:`google.cloud.talent_v4beta1.types.GetApplicationRequest`):
                The request object. Request for getting a application by
                name.
            name (:class:`str`):
                Required. The resource name of the application to be
                retrieved.

                The format is
                "projects/{project_id}/tenants/{tenant_id}/profiles/{profile_id}/applications/{application_id}".
                For example,
                "projects/foo/tenants/bar/profiles/baz/applications/qux".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4beta1.types.Application:
                Resource that represents a job
                application record of a candidate.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = application_service.GetApplicationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_application,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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

    async def update_application(
        self,
        request: application_service.UpdateApplicationRequest = None,
        *,
        application: gct_application.Application = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_application.Application:
        r"""Updates specified application.

        Args:
            request (:class:`google.cloud.talent_v4beta1.types.UpdateApplicationRequest`):
                The request object. Request for updating a specified
                application.
            application (:class:`google.cloud.talent_v4beta1.types.Application`):
                Required. The application resource to
                replace the current resource in the
                system.

                This corresponds to the ``application`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4beta1.types.Application:
                Resource that represents a job
                application record of a candidate.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([application])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = application_service.UpdateApplicationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if application is not None:
            request.application = application

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_application,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("application.name", request.application.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_application(
        self,
        request: application_service.DeleteApplicationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes specified application.

        Args:
            request (:class:`google.cloud.talent_v4beta1.types.DeleteApplicationRequest`):
                The request object. Request to delete a application.
            name (:class:`str`):
                Required. The resource name of the application to be
                deleted.

                The format is
                "projects/{project_id}/tenants/{tenant_id}/profiles/{profile_id}/applications/{application_id}".
                For example,
                "projects/foo/tenants/bar/profiles/baz/applications/qux".

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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = application_service.DeleteApplicationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_application,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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

    async def list_applications(
        self,
        request: application_service.ListApplicationsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListApplicationsAsyncPager:
        r"""Lists all applications associated with the profile.

        Args:
            request (:class:`google.cloud.talent_v4beta1.types.ListApplicationsRequest`):
                The request object. List applications for which the
                client has ACL visibility.
            parent (:class:`str`):
                Required. Resource name of the profile under which the
                application is created.

                The format is
                "projects/{project_id}/tenants/{tenant_id}/profiles/{profile_id}",
                for example, "projects/foo/tenants/bar/profiles/baz".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4beta1.services.application_service.pagers.ListApplicationsAsyncPager:
                The List applications response
                object.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = application_service.ListApplicationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_applications,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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
        response = pagers.ListApplicationsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-talent",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ApplicationServiceAsyncClient",)
