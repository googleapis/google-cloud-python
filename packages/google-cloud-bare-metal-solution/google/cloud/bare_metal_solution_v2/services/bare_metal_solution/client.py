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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.bare_metal_solution_v2.services.bare_metal_solution import pagers
from google.cloud.bare_metal_solution_v2.types import baremetalsolution
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import BareMetalSolutionTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import BareMetalSolutionGrpcTransport
from .transports.grpc_asyncio import BareMetalSolutionGrpcAsyncIOTransport


class BareMetalSolutionClientMeta(type):
    """Metaclass for the BareMetalSolution client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[BareMetalSolutionTransport]]
    _transport_registry["grpc"] = BareMetalSolutionGrpcTransport
    _transport_registry["grpc_asyncio"] = BareMetalSolutionGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[BareMetalSolutionTransport]:
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


class BareMetalSolutionClient(metaclass=BareMetalSolutionClientMeta):
    """Performs management operations on Bare Metal Solution servers.

    The ``baremetalsolution.googleapis.com`` service provides management
    capabilities for Bare Metal Solution servers. To access the API
    methods, you must assign Bare Metal Solution IAM roles containing
    the desired permissions to your staff in your Google Cloud project.
    You must also enable the Bare Metal Solution API. Once enabled, the
    methods act upon specific servers in your Bare Metal Solution
    environment.
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

    DEFAULT_ENDPOINT = "baremetalsolution.googleapis.com"
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
            BareMetalSolutionClient: The constructed client.
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
            BareMetalSolutionClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> BareMetalSolutionTransport:
        """Returns the transport used by the client instance.

        Returns:
            BareMetalSolutionTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def instance_path(project: str, location: str, instance: str,) -> str:
        """Returns a fully-qualified instance string."""
        return "projects/{project}/locations/{location}/instances/{instance}".format(
            project=project, location=location, instance=instance,
        )

    @staticmethod
    def parse_instance_path(path: str) -> Dict[str, str]:
        """Parses a instance path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/instances/(?P<instance>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def lun_path(project: str, location: str, volume: str, lun: str,) -> str:
        """Returns a fully-qualified lun string."""
        return "projects/{project}/locations/{location}/volumes/{volume}/luns/{lun}".format(
            project=project, location=location, volume=volume, lun=lun,
        )

    @staticmethod
    def parse_lun_path(path: str) -> Dict[str, str]:
        """Parses a lun path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/volumes/(?P<volume>.+?)/luns/(?P<lun>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def network_path(project: str, location: str, network: str,) -> str:
        """Returns a fully-qualified network string."""
        return "projects/{project}/locations/{location}/networks/{network}".format(
            project=project, location=location, network=network,
        )

    @staticmethod
    def parse_network_path(path: str) -> Dict[str, str]:
        """Parses a network path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/networks/(?P<network>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def snapshot_schedule_policy_path(
        project: str, location: str, snapshot_schedule_policy: str,
    ) -> str:
        """Returns a fully-qualified snapshot_schedule_policy string."""
        return "projects/{project}/locations/{location}/snapshotSchedulePolicies/{snapshot_schedule_policy}".format(
            project=project,
            location=location,
            snapshot_schedule_policy=snapshot_schedule_policy,
        )

    @staticmethod
    def parse_snapshot_schedule_policy_path(path: str) -> Dict[str, str]:
        """Parses a snapshot_schedule_policy path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/snapshotSchedulePolicies/(?P<snapshot_schedule_policy>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def volume_path(project: str, location: str, volume: str,) -> str:
        """Returns a fully-qualified volume string."""
        return "projects/{project}/locations/{location}/volumes/{volume}".format(
            project=project, location=location, volume=volume,
        )

    @staticmethod
    def parse_volume_path(path: str) -> Dict[str, str]:
        """Parses a volume path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/volumes/(?P<volume>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def volume_snapshot_path(
        project: str, location: str, volume: str, snapshot: str,
    ) -> str:
        """Returns a fully-qualified volume_snapshot string."""
        return "projects/{project}/locations/{location}/volumes/{volume}/snapshots/{snapshot}".format(
            project=project, location=location, volume=volume, snapshot=snapshot,
        )

    @staticmethod
    def parse_volume_snapshot_path(path: str) -> Dict[str, str]:
        """Parses a volume_snapshot path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/volumes/(?P<volume>.+?)/snapshots/(?P<snapshot>.+?)$",
            path,
        )
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
        transport: Union[str, BareMetalSolutionTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the bare metal solution client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, BareMetalSolutionTransport]): The
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
        if isinstance(transport, BareMetalSolutionTransport):
            # transport is a BareMetalSolutionTransport instance.
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

    def list_instances(
        self,
        request: Union[baremetalsolution.ListInstancesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstancesPager:
        r"""List servers in a given project and location.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_list_instances():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListInstancesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_instances(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListInstancesRequest, dict]):
                The request object. Message for requesting the list of
                servers.
            parent (str):
                Required. Parent value for
                ListInstancesRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListInstancesPager:
                Response message for the list of
                servers.
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
        # in a baremetalsolution.ListInstancesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.ListInstancesRequest):
            request = baremetalsolution.ListInstancesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListInstancesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_instance(
        self,
        request: Union[baremetalsolution.GetInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> baremetalsolution.Instance:
        r"""Get details about a single server.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_get_instance():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetInstanceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_instance(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetInstanceRequest, dict]):
                The request object. Message for requesting server
                information.
            name (str):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.Instance:
                A server.
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
        # in a baremetalsolution.GetInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.GetInstanceRequest):
            request = baremetalsolution.GetInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_instance]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def reset_instance(
        self,
        request: Union[baremetalsolution.ResetInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Perform an ungraceful, hard reset on a server.
        Equivalent to shutting the power off and then turning it
        back on.


        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_reset_instance():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ResetInstanceRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.reset_instance(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ResetInstanceRequest, dict]):
                The request object. Message requesting to reset a
                server.
            name (str):
                Required. Name of the resource.
                This corresponds to the ``name`` field
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

                The result type for the operation will be
                :class:`google.cloud.bare_metal_solution_v2.types.ResetInstanceResponse`
                Response message from resetting a server.

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
        # in a baremetalsolution.ResetInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.ResetInstanceRequest):
            request = baremetalsolution.ResetInstanceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reset_instance]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            baremetalsolution.ResetInstanceResponse,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_volumes(
        self,
        request: Union[baremetalsolution.ListVolumesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVolumesPager:
        r"""List storage volumes in a given project and location.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_list_volumes():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListVolumesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_volumes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListVolumesRequest, dict]):
                The request object. Message for requesting a list of
                storage volumes.
            parent (str):
                Required. Parent value for
                ListVolumesRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListVolumesPager:
                Response message containing the list
                of storage volumes.
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
        # in a baremetalsolution.ListVolumesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.ListVolumesRequest):
            request = baremetalsolution.ListVolumesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_volumes]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListVolumesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_volume(
        self,
        request: Union[baremetalsolution.GetVolumeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> baremetalsolution.Volume:
        r"""Get details of a single storage volume.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_get_volume():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetVolumeRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_volume(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetVolumeRequest, dict]):
                The request object. Message for requesting storage
                volume information.
            name (str):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.Volume:
                A storage volume.
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
        # in a baremetalsolution.GetVolumeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.GetVolumeRequest):
            request = baremetalsolution.GetVolumeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_volume]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_volume(
        self,
        request: Union[baremetalsolution.UpdateVolumeRequest, dict] = None,
        *,
        volume: baremetalsolution.Volume = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Update details of a single storage volume.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_update_volume():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.UpdateVolumeRequest(
                )

                # Make the request
                operation = client.update_volume(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.UpdateVolumeRequest, dict]):
                The request object. Message for updating a volume.
            volume (google.cloud.bare_metal_solution_v2.types.Volume):
                Required. The volume to update.

                The ``name`` field is used to identify the volume to
                update. Format:
                projects/{project}/locations/{location}/volumes/{volume}

                This corresponds to the ``volume`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to update. The only currently
                supported fields are: ``snapshot_auto_delete_behavior``
                ``snapshot_schedule_policy_name``

                This corresponds to the ``update_mask`` field
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

                The result type for the operation will be
                :class:`google.cloud.bare_metal_solution_v2.types.Volume`
                A storage volume.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([volume, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a baremetalsolution.UpdateVolumeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.UpdateVolumeRequest):
            request = baremetalsolution.UpdateVolumeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if volume is not None:
                request.volume = volume
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_volume]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("volume.name", request.volume.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            baremetalsolution.Volume,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_networks(
        self,
        request: Union[baremetalsolution.ListNetworksRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNetworksPager:
        r"""List network in a given project and location.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_list_networks():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListNetworksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_networks(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListNetworksRequest, dict]):
                The request object. Message for requesting a list of
                networks.
            parent (str):
                Required. Parent value for
                ListNetworksRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListNetworksPager:
                Response message containing the list
                of networks.
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
        # in a baremetalsolution.ListNetworksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.ListNetworksRequest):
            request = baremetalsolution.ListNetworksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_networks]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListNetworksPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_network(
        self,
        request: Union[baremetalsolution.GetNetworkRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> baremetalsolution.Network:
        r"""Get details of a single network.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_get_network():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetNetworkRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_network(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetNetworkRequest, dict]):
                The request object. Message for requesting network
                information.
            name (str):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.Network:
                A Network.
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
        # in a baremetalsolution.GetNetworkRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.GetNetworkRequest):
            request = baremetalsolution.GetNetworkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_network]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_snapshot_schedule_policies(
        self,
        request: Union[
            baremetalsolution.ListSnapshotSchedulePoliciesRequest, dict
        ] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSnapshotSchedulePoliciesPager:
        r"""List snapshot schedule policies in a given project
        and location.


        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_list_snapshot_schedule_policies():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListSnapshotSchedulePoliciesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_snapshot_schedule_policies(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListSnapshotSchedulePoliciesRequest, dict]):
                The request object. Message for requesting a list of
                snapshot schedule policies.
            parent (str):
                Required. The parent project
                containing the Snapshot Schedule
                Policies.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListSnapshotSchedulePoliciesPager:
                Response message containing the list
                of snapshot schedule policies.
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
        # in a baremetalsolution.ListSnapshotSchedulePoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, baremetalsolution.ListSnapshotSchedulePoliciesRequest
        ):
            request = baremetalsolution.ListSnapshotSchedulePoliciesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_snapshot_schedule_policies
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
        response = pagers.ListSnapshotSchedulePoliciesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_snapshot_schedule_policy(
        self,
        request: Union[baremetalsolution.GetSnapshotSchedulePolicyRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> baremetalsolution.SnapshotSchedulePolicy:
        r"""Get details of a single snapshot schedule policy.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_get_snapshot_schedule_policy():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetSnapshotSchedulePolicyRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_snapshot_schedule_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetSnapshotSchedulePolicyRequest, dict]):
                The request object. Message for requesting snapshot
                schedule policy information.
            name (str):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.SnapshotSchedulePolicy:
                A snapshot schedule policy.
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
        # in a baremetalsolution.GetSnapshotSchedulePolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.GetSnapshotSchedulePolicyRequest):
            request = baremetalsolution.GetSnapshotSchedulePolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_snapshot_schedule_policy
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_snapshot_schedule_policy(
        self,
        request: Union[
            baremetalsolution.CreateSnapshotSchedulePolicyRequest, dict
        ] = None,
        *,
        parent: str = None,
        snapshot_schedule_policy: baremetalsolution.SnapshotSchedulePolicy = None,
        snapshot_schedule_policy_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> baremetalsolution.SnapshotSchedulePolicy:
        r"""Create a snapshot schedule policy in the specified
        project.


        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_create_snapshot_schedule_policy():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.CreateSnapshotSchedulePolicyRequest(
                    parent="parent_value",
                    snapshot_schedule_policy_id="snapshot_schedule_policy_id_value",
                )

                # Make the request
                response = client.create_snapshot_schedule_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.CreateSnapshotSchedulePolicyRequest, dict]):
                The request object. Message for creating a snapshot
                schedule policy in a project.
            parent (str):
                Required. The parent project and
                location containing the
                SnapshotSchedulePolicy.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            snapshot_schedule_policy (google.cloud.bare_metal_solution_v2.types.SnapshotSchedulePolicy):
                Required. The SnapshotSchedulePolicy
                to create.

                This corresponds to the ``snapshot_schedule_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            snapshot_schedule_policy_id (str):
                Required. Snapshot policy ID
                This corresponds to the ``snapshot_schedule_policy_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.SnapshotSchedulePolicy:
                A snapshot schedule policy.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, snapshot_schedule_policy, snapshot_schedule_policy_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a baremetalsolution.CreateSnapshotSchedulePolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, baremetalsolution.CreateSnapshotSchedulePolicyRequest
        ):
            request = baremetalsolution.CreateSnapshotSchedulePolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if snapshot_schedule_policy is not None:
                request.snapshot_schedule_policy = snapshot_schedule_policy
            if snapshot_schedule_policy_id is not None:
                request.snapshot_schedule_policy_id = snapshot_schedule_policy_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_snapshot_schedule_policy
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_snapshot_schedule_policy(
        self,
        request: Union[
            baremetalsolution.UpdateSnapshotSchedulePolicyRequest, dict
        ] = None,
        *,
        snapshot_schedule_policy: baremetalsolution.SnapshotSchedulePolicy = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> baremetalsolution.SnapshotSchedulePolicy:
        r"""Update a snapshot schedule policy in the specified
        project.


        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_update_snapshot_schedule_policy():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.UpdateSnapshotSchedulePolicyRequest(
                )

                # Make the request
                response = client.update_snapshot_schedule_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.UpdateSnapshotSchedulePolicyRequest, dict]):
                The request object. Message for updating a snapshot
                schedule policy in a project.
            snapshot_schedule_policy (google.cloud.bare_metal_solution_v2.types.SnapshotSchedulePolicy):
                Required. The snapshot schedule policy to update.

                The ``name`` field is used to identify the snapshot
                schedule policy to update. Format:
                projects/{project}/locations/global/snapshotSchedulePolicies/{policy}

                This corresponds to the ``snapshot_schedule_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to
                update.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.SnapshotSchedulePolicy:
                A snapshot schedule policy.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([snapshot_schedule_policy, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a baremetalsolution.UpdateSnapshotSchedulePolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, baremetalsolution.UpdateSnapshotSchedulePolicyRequest
        ):
            request = baremetalsolution.UpdateSnapshotSchedulePolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if snapshot_schedule_policy is not None:
                request.snapshot_schedule_policy = snapshot_schedule_policy
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_snapshot_schedule_policy
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "snapshot_schedule_policy.name",
                        request.snapshot_schedule_policy.name,
                    ),
                )
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_snapshot_schedule_policy(
        self,
        request: Union[
            baremetalsolution.DeleteSnapshotSchedulePolicyRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete a named snapshot schedule policy.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_delete_snapshot_schedule_policy():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.DeleteSnapshotSchedulePolicyRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_snapshot_schedule_policy(request=request)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.DeleteSnapshotSchedulePolicyRequest, dict]):
                The request object. Message for deleting a snapshot
                schedule policy in a project.
            name (str):
                Required. The name of the snapshot
                schedule policy to delete.

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
        # in a baremetalsolution.DeleteSnapshotSchedulePolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, baremetalsolution.DeleteSnapshotSchedulePolicyRequest
        ):
            request = baremetalsolution.DeleteSnapshotSchedulePolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_snapshot_schedule_policy
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_volume_snapshot(
        self,
        request: Union[baremetalsolution.CreateVolumeSnapshotRequest, dict] = None,
        *,
        parent: str = None,
        volume_snapshot: baremetalsolution.VolumeSnapshot = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> baremetalsolution.VolumeSnapshot:
        r"""Create a storage volume snapshot in a containing
        volume.


        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_create_volume_snapshot():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.CreateVolumeSnapshotRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_volume_snapshot(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.CreateVolumeSnapshotRequest, dict]):
                The request object. Message for creating a volume
                snapshot.
            parent (str):
                Required. The volume to snapshot.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            volume_snapshot (google.cloud.bare_metal_solution_v2.types.VolumeSnapshot):
                Required. The volume snapshot to
                create. Only the description field may
                be specified.

                This corresponds to the ``volume_snapshot`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.VolumeSnapshot:
                Snapshot registered for a given
                storage volume.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, volume_snapshot])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a baremetalsolution.CreateVolumeSnapshotRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.CreateVolumeSnapshotRequest):
            request = baremetalsolution.CreateVolumeSnapshotRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if volume_snapshot is not None:
                request.volume_snapshot = volume_snapshot

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_volume_snapshot]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def restore_volume_snapshot(
        self,
        request: Union[baremetalsolution.RestoreVolumeSnapshotRequest, dict] = None,
        *,
        volume_snapshot: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Restore a storage volume snapshot to its containing
        volume.


        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_restore_volume_snapshot():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.RestoreVolumeSnapshotRequest(
                    volume_snapshot="volume_snapshot_value",
                )

                # Make the request
                operation = client.restore_volume_snapshot(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.RestoreVolumeSnapshotRequest, dict]):
                The request object. Message for restoring a volume
                snapshot.
            volume_snapshot (str):
                Required. Name of the resource.
                This corresponds to the ``volume_snapshot`` field
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

                The result type for the operation will be
                :class:`google.cloud.bare_metal_solution_v2.types.VolumeSnapshot`
                Snapshot registered for a given storage volume.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([volume_snapshot])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a baremetalsolution.RestoreVolumeSnapshotRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.RestoreVolumeSnapshotRequest):
            request = baremetalsolution.RestoreVolumeSnapshotRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if volume_snapshot is not None:
                request.volume_snapshot = volume_snapshot

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.restore_volume_snapshot]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("volume_snapshot", request.volume_snapshot),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            baremetalsolution.VolumeSnapshot,
            metadata_type=baremetalsolution.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_volume_snapshot(
        self,
        request: Union[baremetalsolution.DeleteVolumeSnapshotRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a storage volume snapshot for a given volume.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_delete_volume_snapshot():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.DeleteVolumeSnapshotRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_volume_snapshot(request=request)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.DeleteVolumeSnapshotRequest, dict]):
                The request object. Message for deleting named Volume
                snapshot.
            name (str):
                Required. The name of the snapshot to
                delete.

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
        # in a baremetalsolution.DeleteVolumeSnapshotRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.DeleteVolumeSnapshotRequest):
            request = baremetalsolution.DeleteVolumeSnapshotRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_volume_snapshot]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def get_volume_snapshot(
        self,
        request: Union[baremetalsolution.GetVolumeSnapshotRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> baremetalsolution.VolumeSnapshot:
        r"""Get details of a single storage volume snapshot.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_get_volume_snapshot():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetVolumeSnapshotRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_volume_snapshot(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetVolumeSnapshotRequest, dict]):
                The request object. Message for requesting storage
                volume snapshot information.
            name (str):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.VolumeSnapshot:
                Snapshot registered for a given
                storage volume.

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
        # in a baremetalsolution.GetVolumeSnapshotRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.GetVolumeSnapshotRequest):
            request = baremetalsolution.GetVolumeSnapshotRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_volume_snapshot]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_volume_snapshots(
        self,
        request: Union[baremetalsolution.ListVolumeSnapshotsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVolumeSnapshotsPager:
        r"""List storage volume snapshots for given storage
        volume.


        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_list_volume_snapshots():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListVolumeSnapshotsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_volume_snapshots(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListVolumeSnapshotsRequest, dict]):
                The request object. Message for requesting a list of
                storage volume snapshots.
            parent (str):
                Required. Parent value for
                ListVolumesRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListVolumeSnapshotsPager:
                Response message containing the list
                of storage volume snapshots.
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
        # in a baremetalsolution.ListVolumeSnapshotsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.ListVolumeSnapshotsRequest):
            request = baremetalsolution.ListVolumeSnapshotsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_volume_snapshots]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListVolumeSnapshotsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_lun(
        self,
        request: Union[baremetalsolution.GetLunRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> baremetalsolution.Lun:
        r"""Get details of a single storage logical unit
        number(LUN).


        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_get_lun():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.GetLunRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_lun(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.GetLunRequest, dict]):
                The request object. Message for requesting storage lun
                information.
            name (str):
                Required. Name of the resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.types.Lun:
                A storage volume logical unit number
                (LUN).

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
        # in a baremetalsolution.GetLunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.GetLunRequest):
            request = baremetalsolution.GetLunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_lun]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_luns(
        self,
        request: Union[baremetalsolution.ListLunsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListLunsPager:
        r"""List storage volume luns for given storage volume.

        .. code-block:: python

            from google.cloud import bare_metal_solution_v2

            def sample_list_luns():
                # Create a client
                client = bare_metal_solution_v2.BareMetalSolutionClient()

                # Initialize request argument(s)
                request = bare_metal_solution_v2.ListLunsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_luns(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bare_metal_solution_v2.types.ListLunsRequest, dict]):
                The request object. Message for requesting a list of
                storage volume luns.
            parent (str):
                Required. Parent value for
                ListLunsRequest.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bare_metal_solution_v2.services.bare_metal_solution.pagers.ListLunsPager:
                Response message containing the list
                of storage volume luns.
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
        # in a baremetalsolution.ListLunsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, baremetalsolution.ListLunsRequest):
            request = baremetalsolution.ListLunsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_luns]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListLunsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

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
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bare-metal-solution",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BareMetalSolutionClient",)
