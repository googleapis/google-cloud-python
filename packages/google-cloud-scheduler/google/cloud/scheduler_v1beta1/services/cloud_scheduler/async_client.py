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
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.scheduler_v1beta1.services.cloud_scheduler import pagers
from google.cloud.scheduler_v1beta1.types import cloudscheduler
from google.cloud.scheduler_v1beta1.types import job
from google.cloud.scheduler_v1beta1.types import job as gcs_job
from google.cloud.scheduler_v1beta1.types import target
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore

from .transports.base import CloudSchedulerTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CloudSchedulerGrpcAsyncIOTransport
from .client import CloudSchedulerClient


class CloudSchedulerAsyncClient:
    """The Cloud Scheduler API allows external entities to reliably
    schedule asynchronous jobs.
    """

    _client: CloudSchedulerClient

    DEFAULT_ENDPOINT = CloudSchedulerClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CloudSchedulerClient.DEFAULT_MTLS_ENDPOINT

    job_path = staticmethod(CloudSchedulerClient.job_path)
    parse_job_path = staticmethod(CloudSchedulerClient.parse_job_path)
    topic_path = staticmethod(CloudSchedulerClient.topic_path)
    parse_topic_path = staticmethod(CloudSchedulerClient.parse_topic_path)

    common_billing_account_path = staticmethod(
        CloudSchedulerClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CloudSchedulerClient.parse_common_billing_account_path
    )

    common_folder_path = staticmethod(CloudSchedulerClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        CloudSchedulerClient.parse_common_folder_path
    )

    common_organization_path = staticmethod(
        CloudSchedulerClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        CloudSchedulerClient.parse_common_organization_path
    )

    common_project_path = staticmethod(CloudSchedulerClient.common_project_path)
    parse_common_project_path = staticmethod(
        CloudSchedulerClient.parse_common_project_path
    )

    common_location_path = staticmethod(CloudSchedulerClient.common_location_path)
    parse_common_location_path = staticmethod(
        CloudSchedulerClient.parse_common_location_path
    )

    from_service_account_file = CloudSchedulerClient.from_service_account_file
    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudSchedulerTransport:
        """Return the transport used by the client instance.

        Returns:
            CloudSchedulerTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CloudSchedulerClient).get_transport_class, type(CloudSchedulerClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, CloudSchedulerTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the cloud scheduler client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudSchedulerTransport]): The
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

        self._client = CloudSchedulerClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_jobs(
        self,
        request: cloudscheduler.ListJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobsAsyncPager:
        r"""Lists jobs.

        Args:
            request (:class:`~.cloudscheduler.ListJobsRequest`):
                The request object. Request message for listing jobs
                using
                [ListJobs][google.cloud.scheduler.v1beta1.CloudScheduler.ListJobs].
            parent (:class:`str`):
                Required. The location name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListJobsAsyncPager:
                Response message for listing jobs using
                [ListJobs][google.cloud.scheduler.v1beta1.CloudScheduler.ListJobs].

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

        request = cloudscheduler.ListJobsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_jobs,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                ),
            ),
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
        response = pagers.ListJobsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_job(
        self,
        request: cloudscheduler.GetJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> job.Job:
        r"""Gets a job.

        Args:
            request (:class:`~.cloudscheduler.GetJobRequest`):
                The request object. Request message for
                [GetJob][google.cloud.scheduler.v1beta1.CloudScheduler.GetJob].
            name (:class:`str`):
                Required. The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.job.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

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

        request = cloudscheduler.GetJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_job,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                ),
            ),
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

    async def create_job(
        self,
        request: cloudscheduler.CreateJobRequest = None,
        *,
        parent: str = None,
        job: gcs_job.Job = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcs_job.Job:
        r"""Creates a job.

        Args:
            request (:class:`~.cloudscheduler.CreateJobRequest`):
                The request object. Request message for
                [CreateJob][google.cloud.scheduler.v1beta1.CloudScheduler.CreateJob].
            parent (:class:`str`):
                Required. The location name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job (:class:`~.gcs_job.Job`):
                Required. The job to add. The user can optionally
                specify a name for the job in
                [name][google.cloud.scheduler.v1beta1.Job.name].
                [name][google.cloud.scheduler.v1beta1.Job.name] cannot
                be the same as an existing job. If a name is not
                specified then the system will generate a random unique
                name that will be returned
                ([name][google.cloud.scheduler.v1beta1.Job.name]) in the
                response.
                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcs_job.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

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

        request = cloudscheduler.CreateJobRequest(request)

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

    async def update_job(
        self,
        request: cloudscheduler.UpdateJobRequest = None,
        *,
        job: gcs_job.Job = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcs_job.Job:
        r"""Updates a job.

        If successful, the updated
        [Job][google.cloud.scheduler.v1beta1.Job] is returned. If the
        job does not exist, ``NOT_FOUND`` is returned.

        If UpdateJob does not successfully return, it is possible for
        the job to be in an
        [Job.State.UPDATE_FAILED][google.cloud.scheduler.v1beta1.Job.State.UPDATE_FAILED]
        state. A job in this state may not be executed. If this happens,
        retry the UpdateJob request until a successful response is
        received.

        Args:
            request (:class:`~.cloudscheduler.UpdateJobRequest`):
                The request object. Request message for
                [UpdateJob][google.cloud.scheduler.v1beta1.CloudScheduler.UpdateJob].
            job (:class:`~.gcs_job.Job`):
                Required. The new job properties.
                [name][google.cloud.scheduler.v1beta1.Job.name] must be
                specified.

                Output only fields cannot be modified using UpdateJob.
                Any value specified for an output only field will be
                ignored.
                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                A  mask used to specify which fields
                of the job are being updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcs_job.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([job, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudscheduler.UpdateJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if job is not None:
            request.job = job
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_job,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("job.name", request.job.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_job(
        self,
        request: cloudscheduler.DeleteJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a job.

        Args:
            request (:class:`~.cloudscheduler.DeleteJobRequest`):
                The request object. Request message for deleting a job
                using
                [DeleteJob][google.cloud.scheduler.v1beta1.CloudScheduler.DeleteJob].
            name (:class:`str`):
                Required. The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
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

        request = cloudscheduler.DeleteJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_job,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                ),
            ),
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

    async def pause_job(
        self,
        request: cloudscheduler.PauseJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> job.Job:
        r"""Pauses a job.

        If a job is paused then the system will stop executing the job
        until it is re-enabled via
        [ResumeJob][google.cloud.scheduler.v1beta1.CloudScheduler.ResumeJob].
        The state of the job is stored in
        [state][google.cloud.scheduler.v1beta1.Job.state]; if paused it
        will be set to
        [Job.State.PAUSED][google.cloud.scheduler.v1beta1.Job.State.PAUSED].
        A job must be in
        [Job.State.ENABLED][google.cloud.scheduler.v1beta1.Job.State.ENABLED]
        to be paused.

        Args:
            request (:class:`~.cloudscheduler.PauseJobRequest`):
                The request object. Request message for
                [PauseJob][google.cloud.scheduler.v1beta1.CloudScheduler.PauseJob].
            name (:class:`str`):
                Required. The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.job.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

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

        request = cloudscheduler.PauseJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.pause_job,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                ),
            ),
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

    async def resume_job(
        self,
        request: cloudscheduler.ResumeJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> job.Job:
        r"""Resume a job.

        This method reenables a job after it has been
        [Job.State.PAUSED][google.cloud.scheduler.v1beta1.Job.State.PAUSED].
        The state of a job is stored in
        [Job.state][google.cloud.scheduler.v1beta1.Job.state]; after
        calling this method it will be set to
        [Job.State.ENABLED][google.cloud.scheduler.v1beta1.Job.State.ENABLED].
        A job must be in
        [Job.State.PAUSED][google.cloud.scheduler.v1beta1.Job.State.PAUSED]
        to be resumed.

        Args:
            request (:class:`~.cloudscheduler.ResumeJobRequest`):
                The request object. Request message for
                [ResumeJob][google.cloud.scheduler.v1beta1.CloudScheduler.ResumeJob].
            name (:class:`str`):
                Required. The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.job.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

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

        request = cloudscheduler.ResumeJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.resume_job,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                ),
            ),
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

    async def run_job(
        self,
        request: cloudscheduler.RunJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> job.Job:
        r"""Forces a job to run now.
        When this method is called, Cloud Scheduler will
        dispatch the job, even if the job is already running.

        Args:
            request (:class:`~.cloudscheduler.RunJobRequest`):
                The request object. Request message for forcing a job to
                run now using
                [RunJob][google.cloud.scheduler.v1beta1.CloudScheduler.RunJob].
            name (:class:`str`):
                Required. The job name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.job.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

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

        request = cloudscheduler.RunJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_job,
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-scheduler",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudSchedulerAsyncClient",)
