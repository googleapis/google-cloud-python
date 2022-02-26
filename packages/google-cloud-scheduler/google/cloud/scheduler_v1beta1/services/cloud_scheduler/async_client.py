# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.scheduler_v1beta1.services.cloud_scheduler import pagers
from google.cloud.scheduler_v1beta1.types import cloudscheduler
from google.cloud.scheduler_v1beta1.types import job
from google.cloud.scheduler_v1beta1.types import job as gcs_job
from google.cloud.scheduler_v1beta1.types import target
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
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

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CloudSchedulerAsyncClient: The constructed client.
        """
        return CloudSchedulerClient.from_service_account_info.__func__(CloudSchedulerAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CloudSchedulerAsyncClient: The constructed client.
        """
        return CloudSchedulerClient.from_service_account_file.__func__(CloudSchedulerAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return CloudSchedulerClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> CloudSchedulerTransport:
        """Returns the transport used by the client instance.

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
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CloudSchedulerTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud scheduler client.

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
        request: Union[cloudscheduler.ListJobsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobsAsyncPager:
        r"""Lists jobs.

        .. code-block:: python

            from google.cloud import scheduler_v1beta1

            def sample_list_jobs():
                # Create a client
                client = scheduler_v1beta1.CloudSchedulerClient()

                # Initialize request argument(s)
                request = scheduler_v1beta1.ListJobsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_jobs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.scheduler_v1beta1.types.ListJobsRequest, dict]):
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
            google.cloud.scheduler_v1beta1.services.cloud_scheduler.pagers.ListJobsAsyncPager:
                Response message for listing jobs using
                [ListJobs][google.cloud.scheduler.v1beta1.CloudScheduler.ListJobs].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
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
        request: Union[cloudscheduler.GetJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> job.Job:
        r"""Gets a job.

        .. code-block:: python

            from google.cloud import scheduler_v1beta1

            def sample_get_job():
                # Create a client
                client = scheduler_v1beta1.CloudSchedulerClient()

                # Initialize request argument(s)
                request = scheduler_v1beta1.GetJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.scheduler_v1beta1.types.GetJobRequest, dict]):
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
            google.cloud.scheduler_v1beta1.types.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
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
        request: Union[cloudscheduler.CreateJobRequest, dict] = None,
        *,
        parent: str = None,
        job: gcs_job.Job = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcs_job.Job:
        r"""Creates a job.

        .. code-block:: python

            from google.cloud import scheduler_v1beta1

            def sample_create_job():
                # Create a client
                client = scheduler_v1beta1.CloudSchedulerClient()

                # Initialize request argument(s)
                request = scheduler_v1beta1.CreateJobRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.scheduler_v1beta1.types.CreateJobRequest, dict]):
                The request object. Request message for
                [CreateJob][google.cloud.scheduler.v1beta1.CloudScheduler.CreateJob].
            parent (:class:`str`):
                Required. The location name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job (:class:`google.cloud.scheduler_v1beta1.types.Job`):
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
            google.cloud.scheduler_v1beta1.types.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        request: Union[cloudscheduler.UpdateJobRequest, dict] = None,
        *,
        job: gcs_job.Job = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
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


        .. code-block:: python

            from google.cloud import scheduler_v1beta1

            def sample_update_job():
                # Create a client
                client = scheduler_v1beta1.CloudSchedulerClient()

                # Initialize request argument(s)
                request = scheduler_v1beta1.UpdateJobRequest(
                )

                # Make the request
                response = client.update_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.scheduler_v1beta1.types.UpdateJobRequest, dict]):
                The request object. Request message for
                [UpdateJob][google.cloud.scheduler.v1beta1.CloudScheduler.UpdateJob].
            job (:class:`google.cloud.scheduler_v1beta1.types.Job`):
                Required. The new job properties.
                [name][google.cloud.scheduler.v1beta1.Job.name] must be
                specified.

                Output only fields cannot be modified using UpdateJob.
                Any value specified for an output only field will be
                ignored.

                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.cloud.scheduler_v1beta1.types.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
        request: Union[cloudscheduler.DeleteJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a job.

        .. code-block:: python

            from google.cloud import scheduler_v1beta1

            def sample_delete_job():
                # Create a client
                client = scheduler_v1beta1.CloudSchedulerClient()

                # Initialize request argument(s)
                request = scheduler_v1beta1.DeleteJobRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_job(request=request)

        Args:
            request (Union[google.cloud.scheduler_v1beta1.types.DeleteJobRequest, dict]):
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
        # Quick check: If we got a request object, we should *not* have
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
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
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
        request: Union[cloudscheduler.PauseJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
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


        .. code-block:: python

            from google.cloud import scheduler_v1beta1

            def sample_pause_job():
                # Create a client
                client = scheduler_v1beta1.CloudSchedulerClient()

                # Initialize request argument(s)
                request = scheduler_v1beta1.PauseJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.pause_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.scheduler_v1beta1.types.PauseJobRequest, dict]):
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
            google.cloud.scheduler_v1beta1.types.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
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
        request: Union[cloudscheduler.ResumeJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
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


        .. code-block:: python

            from google.cloud import scheduler_v1beta1

            def sample_resume_job():
                # Create a client
                client = scheduler_v1beta1.CloudSchedulerClient()

                # Initialize request argument(s)
                request = scheduler_v1beta1.ResumeJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.resume_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.scheduler_v1beta1.types.ResumeJobRequest, dict]):
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
            google.cloud.scheduler_v1beta1.types.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
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
        request: Union[cloudscheduler.RunJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> job.Job:
        r"""Forces a job to run now.
        When this method is called, Cloud Scheduler will
        dispatch the job, even if the job is already running.


        .. code-block:: python

            from google.cloud import scheduler_v1beta1

            def sample_run_job():
                # Create a client
                client = scheduler_v1beta1.CloudSchedulerClient()

                # Initialize request argument(s)
                request = scheduler_v1beta1.RunJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.run_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.scheduler_v1beta1.types.RunJobRequest, dict]):
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
            google.cloud.scheduler_v1beta1.types.Job:
                Configuration for a job.
                The maximum allowed size for a job is
                100KB.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-scheduler",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudSchedulerAsyncClient",)
