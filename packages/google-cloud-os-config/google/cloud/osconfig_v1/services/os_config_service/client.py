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
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.osconfig_v1.services.os_config_service import pagers
from google.cloud.osconfig_v1.types import patch_deployments
from google.cloud.osconfig_v1.types import patch_jobs
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import OsConfigServiceTransport
from .transports.grpc import OsConfigServiceGrpcTransport


class OsConfigServiceClientMeta(type):
    """Metaclass for the OsConfigService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[OsConfigServiceTransport]]
    _transport_registry["grpc"] = OsConfigServiceGrpcTransport

    def get_transport_class(cls, label: str = None) -> Type[OsConfigServiceTransport]:
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


class OsConfigServiceClient(metaclass=OsConfigServiceClientMeta):
    """OS Config API
    The OS Config service is a server-side component that you can
    use to manage package installations and patch jobs for virtual
    machine instances.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "osconfig.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
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
    def patch_deployment_path(project: str, patch_deployment: str) -> str:
        """Return a fully-qualified patch_deployment string."""
        return "projects/{project}/patchDeployments/{patch_deployment}".format(
            project=project, patch_deployment=patch_deployment
        )

    @staticmethod
    def parse_patch_deployment_path(path: str) -> Dict[str, str]:
        """Parse a patch_deployment path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/patchDeployments/(?P<patch_deployment>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, OsConfigServiceTransport] = None,
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the os config service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.OsConfigServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client.
                (2) If ``transport`` argument is None, ``client_options`` can be
                used to create a mutual TLS transport. If ``client_cert_source``
                is provided, mutual TLS transport will be created with the given
                ``api_endpoint`` or the default mTLS endpoint, and the client
                SSL credentials obtained from ``client_cert_source``.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, OsConfigServiceTransport):
            # transport is a OsConfigServiceTransport instance.
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        elif client_options is None or (
            client_options.api_endpoint is None
            and client_options.client_cert_source is None
        ):
            # Don't trigger mTLS if we get an empty ClientOptions.
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials, host=self.DEFAULT_ENDPOINT
            )
        else:
            # We have a non-empty ClientOptions. If client_cert_source is
            # provided, trigger mTLS with user provided endpoint or the default
            # mTLS endpoint.
            if client_options.client_cert_source:
                api_mtls_endpoint = (
                    client_options.api_endpoint
                    if client_options.api_endpoint
                    else self.DEFAULT_MTLS_ENDPOINT
                )
            else:
                api_mtls_endpoint = None

            api_endpoint = (
                client_options.api_endpoint
                if client_options.api_endpoint
                else self.DEFAULT_ENDPOINT
            )

            self._transport = OsConfigServiceGrpcTransport(
                credentials=credentials,
                host=api_endpoint,
                api_mtls_endpoint=api_mtls_endpoint,
                client_cert_source=client_options.client_cert_source,
            )

    def execute_patch_job(
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
            request (:class:`~.patch_jobs.ExecutePatchJobRequest`):
                The request object. A request message to initiate
                patching across Compute Engine instances.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.patch_jobs.PatchJob:
                A high level representation of a patch job that is
                either in progress or has completed.

                Instances details are not included in the job. To
                paginate through instance details, use
                ListPatchJobInstanceDetails.

                For more information about patch jobs, see `Creating
                patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/create-patch-job>`__.

        """
        # Create or coerce a protobuf request object.

        request = patch_jobs.ExecutePatchJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.execute_patch_job,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def get_patch_job(
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
            request (:class:`~.patch_jobs.GetPatchJobRequest`):
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
            ~.patch_jobs.PatchJob:
                A high level representation of a patch job that is
                either in progress or has completed.

                Instances details are not included in the job. To
                paginate through instance details, use
                ListPatchJobInstanceDetails.

                For more information about patch jobs, see `Creating
                patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/create-patch-job>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_patch_job,
            default_timeout=None,
            client_info=_client_info,
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

    def cancel_patch_job(
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
            request (:class:`~.patch_jobs.CancelPatchJobRequest`):
                The request object. Message for canceling a patch job.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.patch_jobs.PatchJob:
                A high level representation of a patch job that is
                either in progress or has completed.

                Instances details are not included in the job. To
                paginate through instance details, use
                ListPatchJobInstanceDetails.

                For more information about patch jobs, see `Creating
                patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/create-patch-job>`__.

        """
        # Create or coerce a protobuf request object.

        request = patch_jobs.CancelPatchJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.cancel_patch_job,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_patch_jobs(
        self,
        request: patch_jobs.ListPatchJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPatchJobsPager:
        r"""Get a list of patch jobs.

        Args:
            request (:class:`~.patch_jobs.ListPatchJobsRequest`):
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
            ~.pagers.ListPatchJobsPager:
                A response message for listing patch
                jobs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_patch_jobs,
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
        response = pagers.ListPatchJobsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def list_patch_job_instance_details(
        self,
        request: patch_jobs.ListPatchJobInstanceDetailsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPatchJobInstanceDetailsPager:
        r"""Get a list of instance details for a given patch job.

        Args:
            request (:class:`~.patch_jobs.ListPatchJobInstanceDetailsRequest`):
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
            ~.pagers.ListPatchJobInstanceDetailsPager:
                A response message for listing the
                instances details for a patch job.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_patch_job_instance_details,
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
        response = pagers.ListPatchJobInstanceDetailsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def create_patch_deployment(
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
            request (:class:`~.patch_deployments.CreatePatchDeploymentRequest`):
                The request object. A request message for creating a
                patch deployment.
            parent (:class:`str`):
                Required. The project to apply this patch deployment to
                in the form ``projects/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            patch_deployment (:class:`~.patch_deployments.PatchDeployment`):
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
            ~.patch_deployments.PatchDeployment:
                Patch deployments are configurations that individual
                patch jobs use to complete a patch. These configurations
                include instance filter, package repository settings,
                and a schedule. For more information about creating and
                managing patch deployments, see `Scheduling patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, patch_deployment, patch_deployment_id]):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_patch_deployment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def get_patch_deployment(
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
            request (:class:`~.patch_deployments.GetPatchDeploymentRequest`):
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
            ~.patch_deployments.PatchDeployment:
                Patch deployments are configurations that individual
                patch jobs use to complete a patch. These configurations
                include instance filter, package repository settings,
                and a schedule. For more information about creating and
                managing patch deployments, see `Scheduling patch
                jobs <https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_patch_deployment,
            default_timeout=None,
            client_info=_client_info,
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

    def list_patch_deployments(
        self,
        request: patch_deployments.ListPatchDeploymentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPatchDeploymentsPager:
        r"""Get a page of OS Config patch deployments.

        Args:
            request (:class:`~.patch_deployments.ListPatchDeploymentsRequest`):
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
            ~.pagers.ListPatchDeploymentsPager:
                A response message for listing patch
                deployments.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_patch_deployments,
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
        response = pagers.ListPatchDeploymentsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def delete_patch_deployment(
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
            request (:class:`~.patch_deployments.DeletePatchDeploymentRequest`):
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
        if request is not None and any([name]):
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
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_patch_deployment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-os-config").version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("OsConfigServiceClient",)
