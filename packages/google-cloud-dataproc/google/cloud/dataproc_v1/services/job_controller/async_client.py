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

from google.api_core import operation
from google.api_core import operation_async
from google.cloud.dataproc_v1.services.job_controller import pagers
from google.cloud.dataproc_v1.types import jobs

from .transports.base import JobControllerTransport
from .transports.grpc_asyncio import JobControllerGrpcAsyncIOTransport
from .client import JobControllerClient


class JobControllerAsyncClient:
    """The JobController provides methods to manage jobs."""

    _client: JobControllerClient

    DEFAULT_ENDPOINT = JobControllerClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = JobControllerClient.DEFAULT_MTLS_ENDPOINT

    from_service_account_file = JobControllerClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(JobControllerClient).get_transport_class, type(JobControllerClient)
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, JobControllerTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the job controller client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.JobControllerTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = JobControllerClient(
            credentials=credentials, transport=transport, client_options=client_options,
        )

    async def submit_job(
        self,
        request: jobs.SubmitJobRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        job: jobs.Job = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> jobs.Job:
        r"""Submits a job to a cluster.

        Args:
            request (:class:`~.jobs.SubmitJobRequest`):
                The request object. A request to submit a job.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the job belongs
                to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job (:class:`~.jobs.Job`):
                Required. The job resource.
                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.jobs.Job:
                A Dataproc job resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, job]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = jobs.SubmitJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if job is not None:
            request.job = job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.submit_job,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
            ),
            default_timeout=900.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def submit_job_as_operation(
        self,
        request: jobs.SubmitJobRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        job: jobs.Job = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Submits job to a cluster.

        Args:
            request (:class:`~.jobs.SubmitJobRequest`):
                The request object. A request to submit a job.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the job belongs
                to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job (:class:`~.jobs.Job`):
                Required. The job resource.
                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.jobs.Job``: A Dataproc job resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, job]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = jobs.SubmitJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if job is not None:
            request.job = job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.submit_job_as_operation,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
            ),
            default_timeout=900.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            jobs.Job,
            metadata_type=jobs.JobMetadata,
        )

        # Done; return the response.
        return response

    async def get_job(
        self,
        request: jobs.GetJobRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        job_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> jobs.Job:
        r"""Gets the resource representation for a job in a
        project.

        Args:
            request (:class:`~.jobs.GetJobRequest`):
                The request object. A request to get the resource
                representation for a job in a project.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the job belongs
                to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_id (:class:`str`):
                Required. The job ID.
                This corresponds to the ``job_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.jobs.Job:
                A Dataproc job resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, job_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = jobs.GetJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if job_id is not None:
            request.job_id = job_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_job,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.InternalServerError,
                    exceptions.ServiceUnavailable,
                    exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=900.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_jobs(
        self,
        request: jobs.ListJobsRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobsAsyncPager:
        r"""Lists regions/{region}/jobs in a project.

        Args:
            request (:class:`~.jobs.ListJobsRequest`):
                The request object. A request to list jobs in a project.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the job belongs
                to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
                Optional. A filter constraining the jobs to list.
                Filters are case-sensitive and have the following
                syntax:

                [field = value] AND [field [= value]] ...

                where **field** is ``status.state`` or ``labels.[KEY]``,
                and ``[KEY]`` is a label key. **value** can be ``*`` to
                match all values. ``status.state`` can be either
                ``ACTIVE`` or ``NON_ACTIVE``. Only the logical ``AND``
                operator is supported; space-separated items are treated
                as having an implicit ``AND`` operator.

                Example filter:

                status.state = ACTIVE AND labels.env = staging AND
                labels.starred = \*
                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListJobsAsyncPager:
                A list of jobs in a project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, filter]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = jobs.ListJobsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if filter is not None:
            request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_jobs,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.InternalServerError,
                    exceptions.ServiceUnavailable,
                    exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=900.0,
            client_info=_client_info,
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

    async def update_job(
        self,
        request: jobs.UpdateJobRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> jobs.Job:
        r"""Updates a job in a project.

        Args:
            request (:class:`~.jobs.UpdateJobRequest`):
                The request object. A request to update a job.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.jobs.Job:
                A Dataproc job resource.
        """
        # Create or coerce a protobuf request object.

        request = jobs.UpdateJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_job,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
            ),
            default_timeout=900.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def cancel_job(
        self,
        request: jobs.CancelJobRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        job_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> jobs.Job:
        r"""Starts a job cancellation request. To access the job resource
        after cancellation, call
        `regions/{region}/jobs.list <https://cloud.google.com/dataproc/docs/reference/rest/v1/projects.regions.jobs/list>`__
        or
        `regions/{region}/jobs.get <https://cloud.google.com/dataproc/docs/reference/rest/v1/projects.regions.jobs/get>`__.

        Args:
            request (:class:`~.jobs.CancelJobRequest`):
                The request object. A request to cancel a job.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the job belongs
                to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_id (:class:`str`):
                Required. The job ID.
                This corresponds to the ``job_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.jobs.Job:
                A Dataproc job resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, region, job_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = jobs.CancelJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if job_id is not None:
            request.job_id = job_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_job,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    exceptions.InternalServerError,
                    exceptions.ServiceUnavailable,
                    exceptions.DeadlineExceeded,
                ),
            ),
            default_timeout=900.0,
            client_info=_client_info,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_job(
        self,
        request: jobs.DeleteJobRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        job_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the job from the project. If the job is active, the
        delete fails, and the response returns ``FAILED_PRECONDITION``.

        Args:
            request (:class:`~.jobs.DeleteJobRequest`):
                The request object. A request to delete a job.
            project_id (:class:`str`):
                Required. The ID of the Google Cloud
                Platform project that the job belongs
                to.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (:class:`str`):
                Required. The Dataproc region in
                which to handle the request.
                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_id (:class:`str`):
                Required. The job ID.
                This corresponds to the ``job_id`` field
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
        if request is not None and any([project_id, region, job_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = jobs.DeleteJobRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if region is not None:
            request.region = region
        if job_id is not None:
            request.job_id = job_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_job,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
            ),
            default_timeout=900.0,
            client_info=_client_info,
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dataproc",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("JobControllerAsyncClient",)
