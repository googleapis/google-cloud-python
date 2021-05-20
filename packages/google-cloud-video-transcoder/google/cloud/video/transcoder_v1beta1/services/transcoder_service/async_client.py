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

from google.cloud.video.transcoder_v1beta1.services.transcoder_service import pagers
from google.cloud.video.transcoder_v1beta1.types import resources
from google.cloud.video.transcoder_v1beta1.types import services
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import TranscoderServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import TranscoderServiceGrpcAsyncIOTransport
from .client import TranscoderServiceClient


class TranscoderServiceAsyncClient:
    """Using the Transcoder API, you can queue asynchronous jobs for
    transcoding media into various output formats. Output formats
    may include different streaming standards such as HTTP Live
    Streaming (HLS) and Dynamic Adaptive Streaming over HTTP (DASH).
    You can also customize jobs using advanced features such as
    Digital Rights Management (DRM), audio equalization, content
    concatenation, and digital ad-stitch ready content generation.
    """

    _client: TranscoderServiceClient

    DEFAULT_ENDPOINT = TranscoderServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TranscoderServiceClient.DEFAULT_MTLS_ENDPOINT

    job_path = staticmethod(TranscoderServiceClient.job_path)
    parse_job_path = staticmethod(TranscoderServiceClient.parse_job_path)
    job_template_path = staticmethod(TranscoderServiceClient.job_template_path)
    parse_job_template_path = staticmethod(
        TranscoderServiceClient.parse_job_template_path
    )
    common_billing_account_path = staticmethod(
        TranscoderServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        TranscoderServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(TranscoderServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        TranscoderServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        TranscoderServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        TranscoderServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(TranscoderServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        TranscoderServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(TranscoderServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        TranscoderServiceClient.parse_common_location_path
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
            TranscoderServiceAsyncClient: The constructed client.
        """
        return TranscoderServiceClient.from_service_account_info.__func__(TranscoderServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            TranscoderServiceAsyncClient: The constructed client.
        """
        return TranscoderServiceClient.from_service_account_file.__func__(TranscoderServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> TranscoderServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            TranscoderServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(TranscoderServiceClient).get_transport_class, type(TranscoderServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, TranscoderServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the transcoder service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TranscoderServiceTransport]): The
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
        self._client = TranscoderServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_job(
        self,
        request: services.CreateJobRequest = None,
        *,
        parent: str = None,
        job: resources.Job = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Job:
        r"""Creates a job in the specified region.

        Args:
            request (:class:`google.cloud.video.transcoder_v1beta1.types.CreateJobRequest`):
                The request object. Request message for
                `TranscoderService.CreateJob`.
            parent (:class:`str`):
                Required. The parent location to create and process this
                job. Format: ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job (:class:`google.cloud.video.transcoder_v1beta1.types.Job`):
                Required. Parameters for creating
                transcoding job.

                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.transcoder_v1beta1.types.Job:
                Transcoding job resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = services.CreateJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if job is not None:
            request.job = job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_job,
            default_timeout=60.0,
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

    async def list_jobs(
        self,
        request: services.ListJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobsAsyncPager:
        r"""Lists jobs in the specified region.

        Args:
            request (:class:`google.cloud.video.transcoder_v1beta1.types.ListJobsRequest`):
                The request object. Request message for
                `TranscoderService.ListJobs`. The parent location from
                which to retrieve the collection of jobs.
            parent (:class:`str`):
                Required. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.transcoder_v1beta1.services.transcoder_service.pagers.ListJobsAsyncPager:
                Response message for TranscoderService.ListJobs.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = services.ListJobsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_jobs,
            default_timeout=60.0,
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
        response = pagers.ListJobsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_job(
        self,
        request: services.GetJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Job:
        r"""Returns the job data.

        Args:
            request (:class:`google.cloud.video.transcoder_v1beta1.types.GetJobRequest`):
                The request object. Request message for
                `TranscoderService.GetJob`.
            name (:class:`str`):
                Required. The name of the job to retrieve. Format:
                ``projects/{project}/locations/{location}/jobs/{job}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.transcoder_v1beta1.types.Job:
                Transcoding job resource.
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

        request = services.GetJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_job,
            default_timeout=60.0,
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

    async def delete_job(
        self,
        request: services.DeleteJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a job.

        Args:
            request (:class:`google.cloud.video.transcoder_v1beta1.types.DeleteJobRequest`):
                The request object. Request message for
                `TranscoderService.DeleteJob`.
            name (:class:`str`):
                Required. The name of the job to delete. Format:
                ``projects/{project}/locations/{location}/jobs/{job}``

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

        request = services.DeleteJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_job,
            default_timeout=60.0,
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

    async def create_job_template(
        self,
        request: services.CreateJobTemplateRequest = None,
        *,
        parent: str = None,
        job_template: resources.JobTemplate = None,
        job_template_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.JobTemplate:
        r"""Creates a job template in the specified region.

        Args:
            request (:class:`google.cloud.video.transcoder_v1beta1.types.CreateJobTemplateRequest`):
                The request object. Request message for
                `TranscoderService.CreateJobTemplate`.
            parent (:class:`str`):
                Required. The parent location to create this job
                template. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_template (:class:`google.cloud.video.transcoder_v1beta1.types.JobTemplate`):
                Required. Parameters for creating job
                template.

                This corresponds to the ``job_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_template_id (:class:`str`):
                Required. The ID to use for the job template, which will
                become the final component of the job template's
                resource name.

                This value should be 4-63 characters, and valid
                characters must match the regular expression
                ``[a-zA-Z][a-zA-Z0-9_-]*``.

                This corresponds to the ``job_template_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.transcoder_v1beta1.types.JobTemplate:
                Transcoding job template resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, job_template, job_template_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = services.CreateJobTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if job_template is not None:
            request.job_template = job_template
        if job_template_id is not None:
            request.job_template_id = job_template_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_job_template,
            default_timeout=60.0,
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

    async def list_job_templates(
        self,
        request: services.ListJobTemplatesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobTemplatesAsyncPager:
        r"""Lists job templates in the specified region.

        Args:
            request (:class:`google.cloud.video.transcoder_v1beta1.types.ListJobTemplatesRequest`):
                The request object. Request message for
                `TranscoderService.ListJobTemplates`.
            parent (:class:`str`):
                Required. The parent location from which to retrieve the
                collection of job templates. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.transcoder_v1beta1.services.transcoder_service.pagers.ListJobTemplatesAsyncPager:
                Response message for TranscoderService.ListJobTemplates.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = services.ListJobTemplatesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_job_templates,
            default_timeout=60.0,
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
        response = pagers.ListJobTemplatesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_job_template(
        self,
        request: services.GetJobTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.JobTemplate:
        r"""Returns the job template data.

        Args:
            request (:class:`google.cloud.video.transcoder_v1beta1.types.GetJobTemplateRequest`):
                The request object. Request message for
                `TranscoderService.GetJobTemplate`.
            name (:class:`str`):
                Required. The name of the job template to retrieve.
                Format:
                ``projects/{project}/locations/{location}/jobTemplates/{job_template}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.video.transcoder_v1beta1.types.JobTemplate:
                Transcoding job template resource.
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

        request = services.GetJobTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_job_template,
            default_timeout=60.0,
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

    async def delete_job_template(
        self,
        request: services.DeleteJobTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a job template.

        Args:
            request (:class:`google.cloud.video.transcoder_v1beta1.types.DeleteJobTemplateRequest`):
                The request object. Request message for
                `TranscoderService.DeleteJobTemplate`.
            name (:class:`str`):
                Required. The name of the job template to delete.
                ``projects/{project}/locations/{location}/jobTemplates/{job_template}``

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

        request = services.DeleteJobTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_job_template,
            default_timeout=60.0,
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
            "google-cloud-video-transcoder",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TranscoderServiceAsyncClient",)
