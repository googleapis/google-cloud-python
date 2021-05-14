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
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.talent_v4.services.job_service import pagers
from google.cloud.talent_v4.types import common
from google.cloud.talent_v4.types import histogram
from google.cloud.talent_v4.types import job
from google.cloud.talent_v4.types import job as gct_job
from google.cloud.talent_v4.types import job_service
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import JobServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import JobServiceGrpcTransport
from .transports.grpc_asyncio import JobServiceGrpcAsyncIOTransport


class JobServiceClientMeta(type):
    """Metaclass for the JobService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[JobServiceTransport]]
    _transport_registry["grpc"] = JobServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = JobServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[JobServiceTransport]:
        """Returns an appropriate transport class.

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


class JobServiceClient(metaclass=JobServiceClientMeta):
    """A service handles job management, including job CRUD,
    enumeration and search.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

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

    DEFAULT_ENDPOINT = "jobs.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
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
            JobServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            JobServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> JobServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            JobServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def company_path(project: str, tenant: str, company: str,) -> str:
        """Returns a fully-qualified company string."""
        return "projects/{project}/tenants/{tenant}/companies/{company}".format(
            project=project, tenant=tenant, company=company,
        )

    @staticmethod
    def parse_company_path(path: str) -> Dict[str, str]:
        """Parses a company path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/tenants/(?P<tenant>.+?)/companies/(?P<company>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def job_path(project: str, tenant: str, job: str,) -> str:
        """Returns a fully-qualified job string."""
        return "projects/{project}/tenants/{tenant}/jobs/{job}".format(
            project=project, tenant=tenant, job=job,
        )

    @staticmethod
    def parse_job_path(path: str) -> Dict[str, str]:
        """Parses a job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/tenants/(?P<tenant>.+?)/jobs/(?P<job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def tenant_path(project: str, tenant: str,) -> str:
        """Returns a fully-qualified tenant string."""
        return "projects/{project}/tenants/{tenant}".format(
            project=project, tenant=tenant,
        )

    @staticmethod
    def parse_tenant_path(path: str) -> Dict[str, str]:
        """Parses a tenant path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/tenants/(?P<tenant>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, JobServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the job service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, JobServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                if is_mtls:
                    api_endpoint = self.DEFAULT_MTLS_ENDPOINT
                else:
                    api_endpoint = self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, JobServiceTransport):
            # transport is a JobServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def create_job(
        self,
        request: job_service.CreateJobRequest = None,
        *,
        parent: str = None,
        job: gct_job.Job = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_job.Job:
        r"""Creates a new job.
        Typically, the job becomes searchable within 10 seconds,
        but it may take up to 5 minutes.

        Args:
            request (google.cloud.talent_v4.types.CreateJobRequest):
                The request object. Create job request.
            parent (str):
                Required. The resource name of the tenant under which
                the job is created.

                The format is
                "projects/{project_id}/tenants/{tenant_id}". For
                example, "projects/foo/tenants/bar".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job (google.cloud.talent_v4.types.Job):
                Required. The Job to be created.
                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.Job:
                A Job resource represents a job posting (also referred to as a "job listing"
                   or "job requisition"). A job belongs to a
                   [Company][google.cloud.talent.v4.Company], which is
                   the hiring entity responsible for the job.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.CreateJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.CreateJobRequest):
            request = job_service.CreateJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if job is not None:
                request.job = job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_create_jobs(
        self,
        request: job_service.BatchCreateJobsRequest = None,
        *,
        parent: str = None,
        jobs: Sequence[job.Job] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Begins executing a batch create jobs operation.

        Args:
            request (google.cloud.talent_v4.types.BatchCreateJobsRequest):
                The request object. Request to create a batch of jobs.
            parent (str):
                Required. The resource name of the tenant under which
                the job is created.

                The format is
                "projects/{project_id}/tenants/{tenant_id}". For
                example, "projects/foo/tenants/bar".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            jobs (Sequence[google.cloud.talent_v4.types.Job]):
                Required. The jobs to be created.
                A maximum of 200 jobs can be created in
                a batch.

                This corresponds to the ``jobs`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.talent_v4.types.BatchCreateJobsResponse` The result of [JobService.BatchCreateJobs][google.cloud.talent.v4.JobService.BatchCreateJobs]. It's used to
                   replace
                   [google.longrunning.Operation.response][google.longrunning.Operation.response]
                   in case of success.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, jobs])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.BatchCreateJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.BatchCreateJobsRequest):
            request = job_service.BatchCreateJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if jobs is not None:
                request.jobs = jobs

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_create_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            job_service.BatchCreateJobsResponse,
            metadata_type=common.BatchOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_job(
        self,
        request: job_service.GetJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> job.Job:
        r"""Retrieves the specified job, whose status is OPEN or
        recently EXPIRED within the last 90 days.

        Args:
            request (google.cloud.talent_v4.types.GetJobRequest):
                The request object. Get job request.
            name (str):
                Required. The resource name of the job to retrieve.

                The format is
                "projects/{project_id}/tenants/{tenant_id}/jobs/{job_id}".
                For example, "projects/foo/tenants/bar/jobs/baz".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.Job:
                A Job resource represents a job posting (also referred to as a "job listing"
                   or "job requisition"). A job belongs to a
                   [Company][google.cloud.talent.v4.Company], which is
                   the hiring entity responsible for the job.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.GetJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.GetJobRequest):
            request = job_service.GetJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_job(
        self,
        request: job_service.UpdateJobRequest = None,
        *,
        job: gct_job.Job = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_job.Job:
        r"""Updates specified job.
        Typically, updated contents become visible in search
        results within 10 seconds, but it may take up to 5
        minutes.

        Args:
            request (google.cloud.talent_v4.types.UpdateJobRequest):
                The request object. Update job request.
            job (google.cloud.talent_v4.types.Job):
                Required. The Job to be updated.
                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Strongly recommended for the best service experience.

                If
                [update_mask][google.cloud.talent.v4.UpdateJobRequest.update_mask]
                is provided, only the specified fields in
                [job][google.cloud.talent.v4.UpdateJobRequest.job] are
                updated. Otherwise all the fields are updated.

                A field mask to restrict the fields that are updated.
                Only top level fields of
                [Job][google.cloud.talent.v4.Job] are supported.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.Job:
                A Job resource represents a job posting (also referred to as a "job listing"
                   or "job requisition"). A job belongs to a
                   [Company][google.cloud.talent.v4.Company], which is
                   the hiring entity responsible for the job.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.UpdateJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.UpdateJobRequest):
            request = job_service.UpdateJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if job is not None:
                request.job = job
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("job.name", request.job.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_update_jobs(
        self,
        request: job_service.BatchUpdateJobsRequest = None,
        *,
        parent: str = None,
        jobs: Sequence[job.Job] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Begins executing a batch update jobs operation.

        Args:
            request (google.cloud.talent_v4.types.BatchUpdateJobsRequest):
                The request object. Request to update a batch of jobs.
            parent (str):
                Required. The resource name of the tenant under which
                the job is created.

                The format is
                "projects/{project_id}/tenants/{tenant_id}". For
                example, "projects/foo/tenants/bar".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            jobs (Sequence[google.cloud.talent_v4.types.Job]):
                Required. The jobs to be updated.
                A maximum of 200 jobs can be updated in
                a batch.

                This corresponds to the ``jobs`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.talent_v4.types.BatchUpdateJobsResponse` The result of [JobService.BatchUpdateJobs][google.cloud.talent.v4.JobService.BatchUpdateJobs]. It's used to
                   replace
                   [google.longrunning.Operation.response][google.longrunning.Operation.response]
                   in case of success.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, jobs])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.BatchUpdateJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.BatchUpdateJobsRequest):
            request = job_service.BatchUpdateJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if jobs is not None:
                request.jobs = jobs

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_update_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            job_service.BatchUpdateJobsResponse,
            metadata_type=common.BatchOperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_job(
        self,
        request: job_service.DeleteJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified job.
        Typically, the job becomes unsearchable within 10
        seconds, but it may take up to 5 minutes.

        Args:
            request (google.cloud.talent_v4.types.DeleteJobRequest):
                The request object. Delete job request.
            name (str):
                Required. The resource name of the job to be deleted.

                The format is
                "projects/{project_id}/tenants/{tenant_id}/jobs/{job_id}".
                For example, "projects/foo/tenants/bar/jobs/baz".

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

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.DeleteJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.DeleteJobRequest):
            request = job_service.DeleteJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def batch_delete_jobs(
        self,
        request: job_service.BatchDeleteJobsRequest = None,
        *,
        parent: str = None,
        names: Sequence[str] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Begins executing a batch delete jobs operation.

        Args:
            request (google.cloud.talent_v4.types.BatchDeleteJobsRequest):
                The request object. Request to delete a batch of jobs.
            parent (str):
                Required. The resource name of the tenant under which
                the job is created.

                The format is
                "projects/{project_id}/tenants/{tenant_id}". For
                example, "projects/foo/tenants/bar".

                The parent of all of the jobs specified in ``names``
                must match this field.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            names (Sequence[str]):
                The names of the jobs to delete.

                The format is
                "projects/{project_id}/tenants/{tenant_id}/jobs/{job_id}".
                For example, "projects/foo/tenants/bar/jobs/baz".

                A maximum of 200 jobs can be deleted in a batch.

                This corresponds to the ``names`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.talent_v4.types.BatchDeleteJobsResponse` The result of [JobService.BatchDeleteJobs][google.cloud.talent.v4.JobService.BatchDeleteJobs]. It's used to
                   replace
                   [google.longrunning.Operation.response][google.longrunning.Operation.response]
                   in case of success.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, names])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.BatchDeleteJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.BatchDeleteJobsRequest):
            request = job_service.BatchDeleteJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if names is not None:
                request.names = names

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_delete_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            job_service.BatchDeleteJobsResponse,
            metadata_type=common.BatchOperationMetadata,
        )

        # Done; return the response.
        return response

    def list_jobs(
        self,
        request: job_service.ListJobsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobsPager:
        r"""Lists jobs by filter.

        Args:
            request (google.cloud.talent_v4.types.ListJobsRequest):
                The request object. List jobs request.
            parent (str):
                Required. The resource name of the tenant under which
                the job is created.

                The format is
                "projects/{project_id}/tenants/{tenant_id}". For
                example, "projects/foo/tenants/bar".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Required. The filter string specifies the jobs to be
                enumerated.

                Supported operator: =, AND

                The fields eligible for filtering are:

                -  ``companyName`` (Required)
                -  ``requisitionId``
                -  ``status`` Available values: OPEN, EXPIRED, ALL.
                   Defaults to OPEN if no value is specified.

                Sample Query:

                -  companyName =
                   "projects/foo/tenants/bar/companies/baz"
                -  companyName =
                   "projects/foo/tenants/bar/companies/baz" AND
                   requisitionId = "req-1"
                -  companyName =
                   "projects/foo/tenants/bar/companies/baz" AND status =
                   "EXPIRED"

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.services.job_service.pagers.ListJobsPager:
                List jobs response.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.ListJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.ListJobsRequest):
            request = job_service.ListJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_jobs(
        self,
        request: job_service.SearchJobsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> job_service.SearchJobsResponse:
        r"""Searches for jobs using the provided
        [SearchJobsRequest][google.cloud.talent.v4.SearchJobsRequest].

        This call constrains the
        [visibility][google.cloud.talent.v4.Job.visibility] of jobs
        present in the database, and only returns jobs that the caller
        has permission to search against.

        Args:
            request (google.cloud.talent_v4.types.SearchJobsRequest):
                The request object. The Request body of the `SearchJobs`
                call.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.SearchJobsResponse:
                Response for SearchJob method.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.SearchJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.SearchJobsRequest):
            request = job_service.SearchJobsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def search_jobs_for_alert(
        self,
        request: job_service.SearchJobsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> job_service.SearchJobsResponse:
        r"""Searches for jobs using the provided
        [SearchJobsRequest][google.cloud.talent.v4.SearchJobsRequest].

        This API call is intended for the use case of targeting passive
        job seekers (for example, job seekers who have signed up to
        receive email alerts about potential job opportunities), it has
        different algorithmic adjustments that are designed to
        specifically target passive job seekers.

        This call constrains the
        [visibility][google.cloud.talent.v4.Job.visibility] of jobs
        present in the database, and only returns jobs the caller has
        permission to search against.

        Args:
            request (google.cloud.talent_v4.types.SearchJobsRequest):
                The request object. The Request body of the `SearchJobs`
                call.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.talent_v4.types.SearchJobsResponse:
                Response for SearchJob method.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a job_service.SearchJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, job_service.SearchJobsRequest):
            request = job_service.SearchJobsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_jobs_for_alert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-talent",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("JobServiceClient",)
