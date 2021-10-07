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

from google.cloud.osconfig_v1.services.os_config_service import pagers
from google.cloud.osconfig_v1.types import patch_deployments
from google.cloud.osconfig_v1.types import patch_jobs
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import OsConfigServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import OsConfigServiceGrpcAsyncIOTransport
from .client import OsConfigServiceClient


class OsConfigServiceAsyncClient:
    """OS Config API
    The OS Config service is a server-side component that you can
    use to manage package installations and patch jobs for virtual
    machine instances.
    """

    _client: OsConfigServiceClient

    DEFAULT_ENDPOINT = OsConfigServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = OsConfigServiceClient.DEFAULT_MTLS_ENDPOINT

    instance_path = staticmethod(OsConfigServiceClient.instance_path)
    parse_instance_path = staticmethod(OsConfigServiceClient.parse_instance_path)
    patch_deployment_path = staticmethod(OsConfigServiceClient.patch_deployment_path)
    parse_patch_deployment_path = staticmethod(
        OsConfigServiceClient.parse_patch_deployment_path
    )
    patch_job_path = staticmethod(OsConfigServiceClient.patch_job_path)
    parse_patch_job_path = staticmethod(OsConfigServiceClient.parse_patch_job_path)
    common_billing_account_path = staticmethod(
        OsConfigServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        OsConfigServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(OsConfigServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        OsConfigServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        OsConfigServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        OsConfigServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(OsConfigServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        OsConfigServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(OsConfigServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        OsConfigServiceClient.parse_common_location_path
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
            OsConfigServiceAsyncClient: The constructed client.
        """
        return OsConfigServiceClient.from_service_account_info.__func__(OsConfigServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            OsConfigServiceAsyncClient: The constructed client.
        """
        return OsConfigServiceClient.from_service_account_file.__func__(OsConfigServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> OsConfigServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            OsConfigServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(OsConfigServiceClient).get_transport_class, type(OsConfigServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, OsConfigServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the os config service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.OsConfigServiceTransport]): The
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
        self._client = OsConfigServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def execute_patch_job(
        self,
        request: patch_jobs.ExecutePatchJobRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_jobs.PatchJob:
        r"""Patch VM instances by creating and running a patch
        job.

        Args:
            request (:class:`google.cloud.osconfig_v1.types.ExecutePatchJobRequest`):
                The request object. A request message to initiate
                patching across Compute Engine instances.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1.types.PatchJob:
                A high level representation of a patch job that is either in progress
                   or has completed.

                   Instance details are not included in the job. To
                   paginate through instance details, use
                   ListPatchJobInstanceDetails.

                   For more information about patch jobs, see [Creating
                   patch
                   jobs](\ https://cloud.google.com/compute/docs/os-patch-management/create-patch-job).

        """
        # Create or coerce a protobuf request object.
        request = patch_jobs.ExecutePatchJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.execute_patch_job,
            default_timeout=None,
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

    async def get_patch_job(
        self,
        request: patch_jobs.GetPatchJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_jobs.PatchJob:
        r"""Get the patch job. This can be used to track the
        progress of an ongoing patch job or review the details
        of completed jobs.

        Args:
            request (:class:`google.cloud.osconfig_v1.types.GetPatchJobRequest`):
                The request object. Request to get an active or
                completed patch job.
            name (:class:`str`):
                Required. Name of the patch in the form
                ``projects/*/patchJobs/*``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1.types.PatchJob:
                A high level representation of a patch job that is either in progress
                   or has completed.

                   Instance details are not included in the job. To
                   paginate through instance details, use
                   ListPatchJobInstanceDetails.

                   For more information about patch jobs, see [Creating
                   patch
                   jobs](\ https://cloud.google.com/compute/docs/os-patch-management/create-patch-job).

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

        request = patch_jobs.GetPatchJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_patch_job,
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

    async def cancel_patch_job(
        self,
        request: patch_jobs.CancelPatchJobRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_jobs.PatchJob:
        r"""Cancel a patch job. The patch job must be active.
        Canceled patch jobs cannot be restarted.

        Args:
            request (:class:`google.cloud.osconfig_v1.types.CancelPatchJobRequest`):
                The request object. Message for canceling a patch job.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1.types.PatchJob:
                A high level representation of a patch job that is either in progress
                   or has completed.

                   Instance details are not included in the job. To
                   paginate through instance details, use
                   ListPatchJobInstanceDetails.

                   For more information about patch jobs, see [Creating
                   patch
                   jobs](\ https://cloud.google.com/compute/docs/os-patch-management/create-patch-job).

        """
        # Create or coerce a protobuf request object.
        request = patch_jobs.CancelPatchJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_patch_job,
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

    async def list_patch_jobs(
        self,
        request: patch_jobs.ListPatchJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPatchJobsAsyncPager:
        r"""Get a list of patch jobs.

        Args:
            request (:class:`google.cloud.osconfig_v1.types.ListPatchJobsRequest`):
                The request object. A request message for listing patch
                jobs.
            parent (:class:`str`):
                Required. In the form of ``projects/*``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1.services.os_config_service.pagers.ListPatchJobsAsyncPager:
                A response message for listing patch
                jobs.
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

        request = patch_jobs.ListPatchJobsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_patch_jobs,
            default_timeout=None,
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
        response = pagers.ListPatchJobsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_patch_job_instance_details(
        self,
        request: patch_jobs.ListPatchJobInstanceDetailsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPatchJobInstanceDetailsAsyncPager:
        r"""Get a list of instance details for a given patch job.

        Args:
            request (:class:`google.cloud.osconfig_v1.types.ListPatchJobInstanceDetailsRequest`):
                The request object. Request to list details for all
                instances that are part of a patch job.
            parent (:class:`str`):
                Required. The parent for the instances are in the form
                of ``projects/*/patchJobs/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1.services.os_config_service.pagers.ListPatchJobInstanceDetailsAsyncPager:
                A response message for listing the
                instances details for a patch job.
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

        request = patch_jobs.ListPatchJobInstanceDetailsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_patch_job_instance_details,
            default_timeout=None,
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
        response = pagers.ListPatchJobInstanceDetailsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_patch_deployment(
        self,
        request: patch_deployments.CreatePatchDeploymentRequest = None,
        *,
        parent: str = None,
        patch_deployment: patch_deployments.PatchDeployment = None,
        patch_deployment_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_deployments.PatchDeployment:
        r"""Create an OS Config patch deployment.

        Args:
            request (:class:`google.cloud.osconfig_v1.types.CreatePatchDeploymentRequest`):
                The request object. A request message for creating a
                patch deployment.
            parent (:class:`str`):
                Required. The project to apply this patch deployment to
                in the form ``projects/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            patch_deployment (:class:`google.cloud.osconfig_v1.types.PatchDeployment`):
                Required. The patch deployment to
                create.

                This corresponds to the ``patch_deployment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            patch_deployment_id (:class:`str`):
                Required. A name for the patch deployment in the
                project. When creating a name the following rules apply:

                -  Must contain only lowercase letters, numbers, and
                   hyphens.
                -  Must start with a letter.
                -  Must be between 1-63 characters.
                -  Must end with a number or a letter.
                -  Must be unique within the project.


                This corresponds to the ``patch_deployment_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1.types.PatchDeployment:
                Patch deployments are configurations that individual patch jobs use to
                   complete a patch. These configurations include
                   instance filter, package repository settings, and a
                   schedule. For more information about creating and
                   managing patch deployments, see [Scheduling patch
                   jobs](\ https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, patch_deployment, patch_deployment_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = patch_deployments.CreatePatchDeploymentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if patch_deployment is not None:
            request.patch_deployment = patch_deployment
        if patch_deployment_id is not None:
            request.patch_deployment_id = patch_deployment_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_patch_deployment,
            default_timeout=None,
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

    async def get_patch_deployment(
        self,
        request: patch_deployments.GetPatchDeploymentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_deployments.PatchDeployment:
        r"""Get an OS Config patch deployment.

        Args:
            request (:class:`google.cloud.osconfig_v1.types.GetPatchDeploymentRequest`):
                The request object. A request message for retrieving a
                patch deployment.
            name (:class:`str`):
                Required. The resource name of the patch deployment in
                the form ``projects/*/patchDeployments/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1.types.PatchDeployment:
                Patch deployments are configurations that individual patch jobs use to
                   complete a patch. These configurations include
                   instance filter, package repository settings, and a
                   schedule. For more information about creating and
                   managing patch deployments, see [Scheduling patch
                   jobs](\ https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs).

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

        request = patch_deployments.GetPatchDeploymentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_patch_deployment,
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

    async def list_patch_deployments(
        self,
        request: patch_deployments.ListPatchDeploymentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPatchDeploymentsAsyncPager:
        r"""Get a page of OS Config patch deployments.

        Args:
            request (:class:`google.cloud.osconfig_v1.types.ListPatchDeploymentsRequest`):
                The request object. A request message for listing patch
                deployments.
            parent (:class:`str`):
                Required. The resource name of the parent in the form
                ``projects/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.osconfig_v1.services.os_config_service.pagers.ListPatchDeploymentsAsyncPager:
                A response message for listing patch
                deployments.
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

        request = patch_deployments.ListPatchDeploymentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_patch_deployments,
            default_timeout=None,
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
        response = pagers.ListPatchDeploymentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_patch_deployment(
        self,
        request: patch_deployments.DeletePatchDeploymentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete an OS Config patch deployment.

        Args:
            request (:class:`google.cloud.osconfig_v1.types.DeletePatchDeploymentRequest`):
                The request object. A request message for deleting a
                patch deployment.
            name (:class:`str`):
                Required. The resource name of the patch deployment in
                the form ``projects/*/patchDeployments/*``.

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

        request = patch_deployments.DeletePatchDeploymentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_patch_deployment,
            default_timeout=None,
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-os-config",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("OsConfigServiceAsyncClient",)
