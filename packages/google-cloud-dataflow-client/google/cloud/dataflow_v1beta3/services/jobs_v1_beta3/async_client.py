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

from google.cloud.dataflow_v1beta3.services.jobs_v1_beta3 import pagers
from google.cloud.dataflow_v1beta3.types import environment
from google.cloud.dataflow_v1beta3.types import jobs
from google.cloud.dataflow_v1beta3.types import snapshots
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import JobsV1Beta3Transport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import JobsV1Beta3GrpcAsyncIOTransport
from .client import JobsV1Beta3Client


class JobsV1Beta3AsyncClient:
    """Provides a method to create and modify Google Cloud Dataflow
    jobs. A Job is a multi-stage computation graph run by the Cloud
    Dataflow service.
    """

    _client: JobsV1Beta3Client

    DEFAULT_ENDPOINT = JobsV1Beta3Client.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = JobsV1Beta3Client.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        JobsV1Beta3Client.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        JobsV1Beta3Client.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(JobsV1Beta3Client.common_folder_path)
    parse_common_folder_path = staticmethod(JobsV1Beta3Client.parse_common_folder_path)
    common_organization_path = staticmethod(JobsV1Beta3Client.common_organization_path)
    parse_common_organization_path = staticmethod(
        JobsV1Beta3Client.parse_common_organization_path
    )
    common_project_path = staticmethod(JobsV1Beta3Client.common_project_path)
    parse_common_project_path = staticmethod(
        JobsV1Beta3Client.parse_common_project_path
    )
    common_location_path = staticmethod(JobsV1Beta3Client.common_location_path)
    parse_common_location_path = staticmethod(
        JobsV1Beta3Client.parse_common_location_path
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
            JobsV1Beta3AsyncClient: The constructed client.
        """
        return JobsV1Beta3Client.from_service_account_info.__func__(JobsV1Beta3AsyncClient, info, *args, **kwargs)  # type: ignore

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
            JobsV1Beta3AsyncClient: The constructed client.
        """
        return JobsV1Beta3Client.from_service_account_file.__func__(JobsV1Beta3AsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> JobsV1Beta3Transport:
        """Returns the transport used by the client instance.

        Returns:
            JobsV1Beta3Transport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(JobsV1Beta3Client).get_transport_class, type(JobsV1Beta3Client)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, JobsV1Beta3Transport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the jobs v1 beta3 client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.JobsV1Beta3Transport]): The
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
        self._client = JobsV1Beta3Client(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_job(
        self,
        request: jobs.CreateJobRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> jobs.Job:
        r"""Creates a Cloud Dataflow job.

        To create a job, we recommend using
        ``projects.locations.jobs.create`` with a [regional endpoint]
        (https://cloud.google.com/dataflow/docs/concepts/regional-endpoints).
        Using ``projects.jobs.create`` is not recommended, as your job
        will always start in ``us-central1``.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.CreateJobRequest`):
                The request object. Request to create a Cloud Dataflow
                job.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.types.Job:
                Defines a job to be run by the Cloud
                Dataflow service. nextID: 26

        """
        # Create or coerce a protobuf request object.
        request = jobs.CreateJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_job,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_job(
        self,
        request: jobs.GetJobRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> jobs.Job:
        r"""Gets the state of the specified Cloud Dataflow job.

        To get the state of a job, we recommend using
        ``projects.locations.jobs.get`` with a [regional endpoint]
        (https://cloud.google.com/dataflow/docs/concepts/regional-endpoints).
        Using ``projects.jobs.get`` is not recommended, as you can only
        get the state of jobs that are running in ``us-central1``.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.GetJobRequest`):
                The request object. Request to get the state of a Cloud
                Dataflow job.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.types.Job:
                Defines a job to be run by the Cloud
                Dataflow service. nextID: 26

        """
        # Create or coerce a protobuf request object.
        request = jobs.GetJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_job,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

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
        r"""Updates the state of an existing Cloud Dataflow job.

        To update the state of an existing job, we recommend using
        ``projects.locations.jobs.update`` with a [regional endpoint]
        (https://cloud.google.com/dataflow/docs/concepts/regional-endpoints).
        Using ``projects.jobs.update`` is not recommended, as you can
        only update the state of jobs that are running in
        ``us-central1``.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.UpdateJobRequest`):
                The request object. Request to update a Cloud Dataflow
                job.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.types.Job:
                Defines a job to be run by the Cloud
                Dataflow service. nextID: 26

        """
        # Create or coerce a protobuf request object.
        request = jobs.UpdateJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_job,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_jobs(
        self,
        request: jobs.ListJobsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobsAsyncPager:
        r"""List the jobs of a project.

        To list the jobs of a project in a region, we recommend using
        ``projects.locations.jobs.list`` with a [regional endpoint]
        (https://cloud.google.com/dataflow/docs/concepts/regional-endpoints).
        To list the all jobs across all regions, use
        ``projects.jobs.aggregated``. Using ``projects.jobs.list`` is
        not recommended, as you can only get the list of jobs that are
        running in ``us-central1``.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.ListJobsRequest`):
                The request object. Request to list Cloud Dataflow jobs.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.services.jobs_v1_beta3.pagers.ListJobsAsyncPager:
                Response to a request to list Cloud
                Dataflow jobs in a project. This might
                be a partial response, depending on the
                page size in the ListJobsRequest.
                However, if the project does not have
                any jobs, an instance of
                ListJobsResponse is not returned and the
                requests's response body is empty {}.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = jobs.ListJobsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_jobs,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
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

    async def aggregated_list_jobs(
        self,
        request: jobs.ListJobsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.AggregatedListJobsAsyncPager:
        r"""List the jobs of a project across all regions.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.ListJobsRequest`):
                The request object. Request to list Cloud Dataflow jobs.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.services.jobs_v1_beta3.pagers.AggregatedListJobsAsyncPager:
                Response to a request to list Cloud
                Dataflow jobs in a project. This might
                be a partial response, depending on the
                page size in the ListJobsRequest.
                However, if the project does not have
                any jobs, an instance of
                ListJobsResponse is not returned and the
                requests's response body is empty {}.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = jobs.ListJobsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.aggregated_list_jobs,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.AggregatedListJobsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def check_active_jobs(
        self,
        request: jobs.CheckActiveJobsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> jobs.CheckActiveJobsResponse:
        r"""Check for existence of active jobs in the given
        project across all regions.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.CheckActiveJobsRequest`):
                The request object. Request to check is active jobs
                exists for a project
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.types.CheckActiveJobsResponse:
                Response for CheckActiveJobsRequest.
        """
        # Create or coerce a protobuf request object.
        request = jobs.CheckActiveJobsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.check_active_jobs,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def snapshot_job(
        self,
        request: jobs.SnapshotJobRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> snapshots.Snapshot:
        r"""Snapshot the state of a streaming job.

        Args:
            request (:class:`google.cloud.dataflow_v1beta3.types.SnapshotJobRequest`):
                The request object. Request to create a snapshot of a
                job.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataflow_v1beta3.types.Snapshot:
                Represents a snapshot of a job.
        """
        # Create or coerce a protobuf request object.
        request = jobs.SnapshotJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.snapshot_job,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dataflow-client",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("JobsV1Beta3AsyncClient",)
