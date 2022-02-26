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

from google.cloud.osconfig_v1.services.os_config_service import pagers
from google.cloud.osconfig_v1.types import patch_deployments
from google.cloud.osconfig_v1.types import patch_jobs
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import OsConfigServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import OsConfigServiceGrpcTransport
from .transports.grpc_asyncio import OsConfigServiceGrpcAsyncIOTransport


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
    _transport_registry["grpc_asyncio"] = OsConfigServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[OsConfigServiceTransport]:
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


class OsConfigServiceClient(metaclass=OsConfigServiceClientMeta):
    """OS Config API
    The OS Config service is a server-side component that you can
    use to manage package installations and patch jobs for virtual
    machine instances.
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

    DEFAULT_ENDPOINT = "osconfig.googleapis.com"
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
            OsConfigServiceClient: The constructed client.
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
            OsConfigServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> OsConfigServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            OsConfigServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def instance_path(project: str, zone: str, instance: str,) -> str:
        """Returns a fully-qualified instance string."""
        return "projects/{project}/zones/{zone}/instances/{instance}".format(
            project=project, zone=zone, instance=instance,
        )

    @staticmethod
    def parse_instance_path(path: str) -> Dict[str, str]:
        """Parses a instance path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/zones/(?P<zone>.+?)/instances/(?P<instance>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def patch_deployment_path(project: str, patch_deployment: str,) -> str:
        """Returns a fully-qualified patch_deployment string."""
        return "projects/{project}/patchDeployments/{patch_deployment}".format(
            project=project, patch_deployment=patch_deployment,
        )

    @staticmethod
    def parse_patch_deployment_path(path: str) -> Dict[str, str]:
        """Parses a patch_deployment path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/patchDeployments/(?P<patch_deployment>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def patch_job_path(project: str, patch_job: str,) -> str:
        """Returns a fully-qualified patch_job string."""
        return "projects/{project}/patchJobs/{patch_job}".format(
            project=project, patch_job=patch_job,
        )

    @staticmethod
    def parse_patch_job_path(path: str) -> Dict[str, str]:
        """Parses a patch_job path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/patchJobs/(?P<patch_job>.+?)$", path)
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
        transport: Union[str, OsConfigServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the os config service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, OsConfigServiceTransport]): The
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
        if isinstance(transport, OsConfigServiceTransport):
            # transport is a OsConfigServiceTransport instance.
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

    def execute_patch_job(
        self,
        request: Union[patch_jobs.ExecutePatchJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_jobs.PatchJob:
        r"""Patch VM instances by creating and running a patch
        job.


        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_execute_patch_job():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.ExecutePatchJobRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.execute_patch_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.ExecutePatchJobRequest, dict]):
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
        # Minor optimization to avoid making a copy if the user passes
        # in a patch_jobs.ExecutePatchJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_jobs.ExecutePatchJobRequest):
            request = patch_jobs.ExecutePatchJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.execute_patch_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_patch_job(
        self,
        request: Union[patch_jobs.GetPatchJobRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_jobs.PatchJob:
        r"""Get the patch job. This can be used to track the
        progress of an ongoing patch job or review the details
        of completed jobs.


        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_get_patch_job():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.GetPatchJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_patch_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.GetPatchJobRequest, dict]):
                The request object. Request to get an active or
                completed patch job.
            name (str):
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a patch_jobs.GetPatchJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_jobs.GetPatchJobRequest):
            request = patch_jobs.GetPatchJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_patch_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def cancel_patch_job(
        self,
        request: Union[patch_jobs.CancelPatchJobRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_jobs.PatchJob:
        r"""Cancel a patch job. The patch job must be active.
        Canceled patch jobs cannot be restarted.


        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_cancel_patch_job():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.CancelPatchJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.cancel_patch_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.CancelPatchJobRequest, dict]):
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
        # Minor optimization to avoid making a copy if the user passes
        # in a patch_jobs.CancelPatchJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_jobs.CancelPatchJobRequest):
            request = patch_jobs.CancelPatchJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_patch_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_patch_jobs(
        self,
        request: Union[patch_jobs.ListPatchJobsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPatchJobsPager:
        r"""Get a list of patch jobs.

        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_list_patch_jobs():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.ListPatchJobsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_patch_jobs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.ListPatchJobsRequest, dict]):
                The request object. A request message for listing patch
                jobs.
            parent (str):
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
            google.cloud.osconfig_v1.services.os_config_service.pagers.ListPatchJobsPager:
                A response message for listing patch
                jobs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a patch_jobs.ListPatchJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_jobs.ListPatchJobsRequest):
            request = patch_jobs.ListPatchJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_patch_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPatchJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_patch_job_instance_details(
        self,
        request: Union[patch_jobs.ListPatchJobInstanceDetailsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPatchJobInstanceDetailsPager:
        r"""Get a list of instance details for a given patch job.

        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_list_patch_job_instance_details():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.ListPatchJobInstanceDetailsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_patch_job_instance_details(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.ListPatchJobInstanceDetailsRequest, dict]):
                The request object. Request to list details for all
                instances that are part of a patch job.
            parent (str):
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
            google.cloud.osconfig_v1.services.os_config_service.pagers.ListPatchJobInstanceDetailsPager:
                A response message for listing the
                instances details for a patch job.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a patch_jobs.ListPatchJobInstanceDetailsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_jobs.ListPatchJobInstanceDetailsRequest):
            request = patch_jobs.ListPatchJobInstanceDetailsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_patch_job_instance_details
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPatchJobInstanceDetailsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_patch_deployment(
        self,
        request: Union[patch_deployments.CreatePatchDeploymentRequest, dict] = None,
        *,
        parent: str = None,
        patch_deployment: patch_deployments.PatchDeployment = None,
        patch_deployment_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_deployments.PatchDeployment:
        r"""Create an OS Config patch deployment.

        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_create_patch_deployment():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.CreatePatchDeploymentRequest(
                    parent="parent_value",
                    patch_deployment_id="patch_deployment_id_value",
                )

                # Make the request
                response = client.create_patch_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.CreatePatchDeploymentRequest, dict]):
                The request object. A request message for creating a
                patch deployment.
            parent (str):
                Required. The project to apply this patch deployment to
                in the form ``projects/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            patch_deployment (google.cloud.osconfig_v1.types.PatchDeployment):
                Required. The patch deployment to
                create.

                This corresponds to the ``patch_deployment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            patch_deployment_id (str):
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, patch_deployment, patch_deployment_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a patch_deployments.CreatePatchDeploymentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_deployments.CreatePatchDeploymentRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.create_patch_deployment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_patch_deployment(
        self,
        request: Union[patch_deployments.GetPatchDeploymentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_deployments.PatchDeployment:
        r"""Get an OS Config patch deployment.

        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_get_patch_deployment():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.GetPatchDeploymentRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_patch_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.GetPatchDeploymentRequest, dict]):
                The request object. A request message for retrieving a
                patch deployment.
            name (str):
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a patch_deployments.GetPatchDeploymentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_deployments.GetPatchDeploymentRequest):
            request = patch_deployments.GetPatchDeploymentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_patch_deployment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_patch_deployments(
        self,
        request: Union[patch_deployments.ListPatchDeploymentsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPatchDeploymentsPager:
        r"""Get a page of OS Config patch deployments.

        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_list_patch_deployments():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.ListPatchDeploymentsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_patch_deployments(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.ListPatchDeploymentsRequest, dict]):
                The request object. A request message for listing patch
                deployments.
            parent (str):
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
            google.cloud.osconfig_v1.services.os_config_service.pagers.ListPatchDeploymentsPager:
                A response message for listing patch
                deployments.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a patch_deployments.ListPatchDeploymentsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_deployments.ListPatchDeploymentsRequest):
            request = patch_deployments.ListPatchDeploymentsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_patch_deployments]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPatchDeploymentsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_patch_deployment(
        self,
        request: Union[patch_deployments.DeletePatchDeploymentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete an OS Config patch deployment.

        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_delete_patch_deployment():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.DeletePatchDeploymentRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_patch_deployment(request=request)

        Args:
            request (Union[google.cloud.osconfig_v1.types.DeletePatchDeploymentRequest, dict]):
                The request object. A request message for deleting a
                patch deployment.
            name (str):
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a patch_deployments.DeletePatchDeploymentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_deployments.DeletePatchDeploymentRequest):
            request = patch_deployments.DeletePatchDeploymentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_patch_deployment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def update_patch_deployment(
        self,
        request: Union[patch_deployments.UpdatePatchDeploymentRequest, dict] = None,
        *,
        patch_deployment: patch_deployments.PatchDeployment = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_deployments.PatchDeployment:
        r"""Update an OS Config patch deployment.

        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_update_patch_deployment():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.UpdatePatchDeploymentRequest(
                )

                # Make the request
                response = client.update_patch_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.UpdatePatchDeploymentRequest, dict]):
                The request object. A request message for updating a
                patch deployment.
            patch_deployment (google.cloud.osconfig_v1.types.PatchDeployment):
                Required. The patch deployment to
                Update.

                This corresponds to the ``patch_deployment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. Field mask that controls
                which fields of the patch deployment
                should be updated.

                This corresponds to the ``update_mask`` field
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([patch_deployment, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a patch_deployments.UpdatePatchDeploymentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_deployments.UpdatePatchDeploymentRequest):
            request = patch_deployments.UpdatePatchDeploymentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if patch_deployment is not None:
                request.patch_deployment = patch_deployment
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_patch_deployment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("patch_deployment.name", request.patch_deployment.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def pause_patch_deployment(
        self,
        request: Union[patch_deployments.PausePatchDeploymentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_deployments.PatchDeployment:
        r"""Change state of patch deployment to "PAUSED".
        Patch deployment in paused state doesn't generate patch
        jobs.


        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_pause_patch_deployment():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.PausePatchDeploymentRequest(
                    name="name_value",
                )

                # Make the request
                response = client.pause_patch_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.PausePatchDeploymentRequest, dict]):
                The request object. A request message for pausing a
                patch deployment.
            name (str):
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a patch_deployments.PausePatchDeploymentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_deployments.PausePatchDeploymentRequest):
            request = patch_deployments.PausePatchDeploymentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.pause_patch_deployment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def resume_patch_deployment(
        self,
        request: Union[patch_deployments.ResumePatchDeploymentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> patch_deployments.PatchDeployment:
        r"""Change state of patch deployment back to "ACTIVE".
        Patch deployment in active state continues to generate
        patch jobs.


        .. code-block:: python

            from google.cloud import osconfig_v1

            def sample_resume_patch_deployment():
                # Create a client
                client = osconfig_v1.OsConfigServiceClient()

                # Initialize request argument(s)
                request = osconfig_v1.ResumePatchDeploymentRequest(
                    name="name_value",
                )

                # Make the request
                response = client.resume_patch_deployment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.osconfig_v1.types.ResumePatchDeploymentRequest, dict]):
                The request object. A request message for resuming a
                patch deployment.
            name (str):
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a patch_deployments.ResumePatchDeploymentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, patch_deployments.ResumePatchDeploymentRequest):
            request = patch_deployments.ResumePatchDeploymentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resume_patch_deployment]

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
        gapic_version=pkg_resources.get_distribution("google-cloud-os-config",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("OsConfigServiceClient",)
