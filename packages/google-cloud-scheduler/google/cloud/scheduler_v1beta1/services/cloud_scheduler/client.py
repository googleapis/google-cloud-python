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
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
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
from .transports.grpc import CloudSchedulerGrpcTransport
from .transports.grpc_asyncio import CloudSchedulerGrpcAsyncIOTransport


class CloudSchedulerClientMeta(type):
    """Metaclass for the CloudScheduler client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[CloudSchedulerTransport]]
    _transport_registry["grpc"] = CloudSchedulerGrpcTransport
    _transport_registry["grpc_asyncio"] = CloudSchedulerGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[CloudSchedulerTransport]:
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


class CloudSchedulerClient(metaclass=CloudSchedulerClientMeta):
    """The Cloud Scheduler API allows external entities to reliably
    schedule asynchronous jobs.
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

    DEFAULT_ENDPOINT = "cloudscheduler.googleapis.com"
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
            CloudSchedulerClient: The constructed client.
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
            CloudSchedulerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudSchedulerTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudSchedulerTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def job_path(project: str, location: str, job: str,) -> str:
        """Returns a fully-qualified job string."""
        return "projects/{project}/locations/{location}/jobs/{job}".format(
            project=project, location=location, job=job,
        )

    @staticmethod
    def parse_job_path(path: str) -> Dict[str, str]:
        """Parses a job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/jobs/(?P<job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def topic_path(project: str, topic: str,) -> str:
        """Returns a fully-qualified topic string."""
        return "projects/{project}/topics/{topic}".format(project=project, topic=topic,)

    @staticmethod
    def parse_topic_path(path: str) -> Dict[str, str]:
        """Parses a topic path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/topics/(?P<topic>.+?)$", path)
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

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
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
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, CloudSchedulerTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud scheduler client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, CloudSchedulerTransport]): The
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

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, CloudSchedulerTransport):
            # transport is a CloudSchedulerTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
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
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
            )

    def list_jobs(
        self,
        request: Union[cloudscheduler.ListJobsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobsPager:
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
            parent (str):
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
            google.cloud.scheduler_v1beta1.services.cloud_scheduler.pagers.ListJobsPager:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudscheduler.ListJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudscheduler.ListJobsRequest):
            request = cloudscheduler.ListJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

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

    def get_job(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudscheduler.GetJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudscheduler.GetJobRequest):
            request = cloudscheduler.GetJobRequest(request)
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

    def create_job(
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
            parent (str):
                Required. The location name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job (google.cloud.scheduler_v1beta1.types.Job):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudscheduler.CreateJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudscheduler.CreateJobRequest):
            request = cloudscheduler.CreateJobRequest(request)
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

    def update_job(
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
            job (google.cloud.scheduler_v1beta1.types.Job):
                Required. The new job properties.
                [name][google.cloud.scheduler.v1beta1.Job.name] must be
                specified.

                Output only fields cannot be modified using UpdateJob.
                Any value specified for an output only field will be
                ignored.

                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudscheduler.UpdateJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudscheduler.UpdateJobRequest):
            request = cloudscheduler.UpdateJobRequest(request)
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

    def delete_job(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudscheduler.DeleteJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudscheduler.DeleteJobRequest):
            request = cloudscheduler.DeleteJobRequest(request)
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

    def pause_job(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudscheduler.PauseJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudscheduler.PauseJobRequest):
            request = cloudscheduler.PauseJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.pause_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def resume_job(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudscheduler.ResumeJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudscheduler.ResumeJobRequest):
            request = cloudscheduler.ResumeJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resume_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def run_job(
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
            name (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudscheduler.RunJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudscheduler.RunJobRequest):
            request = cloudscheduler.RunJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-scheduler",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudSchedulerClient",)
