# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import os
import re
from typing import (
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
import warnings

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import extended_operation, gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.compute_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.api_core import extended_operation  # type: ignore

from google.cloud.compute_v1.services.disks import pagers
from google.cloud.compute_v1.types import compute

from .transports.base import DEFAULT_CLIENT_INFO, DisksTransport
from .transports.rest import DisksRestTransport


class DisksClientMeta(type):
    """Metaclass for the Disks client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[DisksTransport]]
    _transport_registry["rest"] = DisksRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[DisksTransport]:
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


class DisksClient(metaclass=DisksClientMeta):
    """The Disks API."""

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

    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = "compute.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "compute.{UNIVERSE_DOMAIN}"
    _DEFAULT_UNIVERSE = "googleapis.com"

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DisksClient: The constructed client.
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
            DisksClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DisksTransport:
        """Returns the transport used by the client instance.

        Returns:
            DisksTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
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
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
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
        """Deprecated. Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
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

        warnings.warn(
            "get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning,
        )
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

    @staticmethod
    def _read_environment_variables():
        """Returns the environment variables used by the client.

        Returns:
            Tuple[bool, str, str]: returns the GOOGLE_API_USE_CLIENT_CERTIFICATE,
            GOOGLE_API_USE_MTLS_ENDPOINT, and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

        Raises:
            ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
                any of ["true", "false"].
            google.auth.exceptions.MutualTLSChannelError: If GOOGLE_API_USE_MTLS_ENDPOINT
                is not any of ["auto", "never", "always"].
        """
        use_client_cert = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )
        return use_client_cert == "true", use_mtls_endpoint, universe_domain_env

    @staticmethod
    def _get_client_cert_source(provided_cert_source, use_cert_flag):
        """Return the client cert source to be used by the client.

        Args:
            provided_cert_source (bytes): The client certificate source provided.
            use_cert_flag (bool): A flag indicating whether to use the client certificate.

        Returns:
            bytes or None: The client cert source to be used by the client.
        """
        client_cert_source = None
        if use_cert_flag:
            if provided_cert_source:
                client_cert_source = provided_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()
        return client_cert_source

    @staticmethod
    def _get_api_endpoint(
        api_override, client_cert_source, universe_domain, use_mtls_endpoint
    ):
        """Return the API endpoint used by the client.

        Args:
            api_override (str): The API endpoint override. If specified, this is always
                the return value of this function and the other arguments are not used.
            client_cert_source (bytes): The client certificate source used by the client.
            universe_domain (str): The universe domain used by the client.
            use_mtls_endpoint (str): How to use the mTLS endpoint, which depends also on the other parameters.
                Possible values are "always", "auto", or "never".

        Returns:
            str: The API endpoint to be used by the client.
        """
        if api_override is not None:
            api_endpoint = api_override
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            _default_universe = DisksClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = DisksClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = DisksClient._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=universe_domain
            )
        return api_endpoint

    @staticmethod
    def _get_universe_domain(
        client_universe_domain: Optional[str], universe_domain_env: Optional[str]
    ) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = DisksClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """

        # NOTE (b/349488459): universe validation is disabled until further notice.
        return True

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used by the client instance.
        """
        return self._universe_domain

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[str, DisksTransport, Callable[..., DisksTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the disks client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,DisksTransport,Callable[..., DisksTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the DisksTransport constructor.
                If set to None, a transport is chosen automatically.
                NOTE: "rest" transport functionality is currently in a
                beta state (preview). We welcome your feedback via an
                issue in this library's source repository.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that the ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client_options = client_options
        if isinstance(self._client_options, dict):
            self._client_options = client_options_lib.from_dict(self._client_options)
        if self._client_options is None:
            self._client_options = client_options_lib.ClientOptions()
        self._client_options = cast(
            client_options_lib.ClientOptions, self._client_options
        )

        universe_domain_opt = getattr(self._client_options, "universe_domain", None)

        (
            self._use_client_cert,
            self._use_mtls_endpoint,
            self._universe_domain_env,
        ) = DisksClient._read_environment_variables()
        self._client_cert_source = DisksClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = DisksClient._get_universe_domain(
            universe_domain_opt, self._universe_domain_env
        )
        self._api_endpoint = None  # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, DisksTransport)
        if transport_provided:
            # transport is a DisksTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(DisksTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = self._api_endpoint or DisksClient._get_api_endpoint(
            self._client_options.api_endpoint,
            self._client_cert_source,
            self._universe_domain,
            self._use_mtls_endpoint,
        )

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            transport_init: Union[
                Type[DisksTransport], Callable[..., DisksTransport]
            ] = (
                DisksClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., DisksTransport], transport)
            )
            # initialize with the provided callable or the passed in class
            self._transport = transport_init(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
            )

    def add_resource_policies_unary(
        self,
        request: Optional[Union[compute.AddResourcePoliciesDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disks_add_resource_policies_request_resource: Optional[
            compute.DisksAddResourcePoliciesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Adds existing resource policies to a disk. You can
        only add one policy which will be applied to this disk
        for scheduling snapshot creation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_add_resource_policies():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.AddResourcePoliciesDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.add_resource_policies(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.AddResourcePoliciesDiskRequest, dict]):
                The request object. A request message for
                Disks.AddResourcePolicies. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The disk name for this request.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_add_resource_policies_request_resource (google.cloud.compute_v1.types.DisksAddResourcePoliciesRequest):
                The body resource for this request
                This corresponds to the ``disks_add_resource_policies_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, disk, disks_add_resource_policies_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.AddResourcePoliciesDiskRequest):
            request = compute.AddResourcePoliciesDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disks_add_resource_policies_request_resource is not None:
                request.disks_add_resource_policies_request_resource = (
                    disks_add_resource_policies_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_resource_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def add_resource_policies(
        self,
        request: Optional[Union[compute.AddResourcePoliciesDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disks_add_resource_policies_request_resource: Optional[
            compute.DisksAddResourcePoliciesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Adds existing resource policies to a disk. You can
        only add one policy which will be applied to this disk
        for scheduling snapshot creation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_add_resource_policies():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.AddResourcePoliciesDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.add_resource_policies(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.AddResourcePoliciesDiskRequest, dict]):
                The request object. A request message for
                Disks.AddResourcePolicies. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The disk name for this request.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_add_resource_policies_request_resource (google.cloud.compute_v1.types.DisksAddResourcePoliciesRequest):
                The body resource for this request
                This corresponds to the ``disks_add_resource_policies_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, disk, disks_add_resource_policies_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.AddResourcePoliciesDiskRequest):
            request = compute.AddResourcePoliciesDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disks_add_resource_policies_request_resource is not None:
                request.disks_add_resource_policies_request_resource = (
                    disks_add_resource_policies_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_resource_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def aggregated_list(
        self,
        request: Optional[Union[compute.AggregatedListDisksRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.AggregatedListPager:
        r"""Retrieves an aggregated list of persistent disks. To prevent
        failure, Google recommends that you set the
        ``returnPartialSuccess`` parameter to ``true``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_aggregated_list():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.AggregatedListDisksRequest(
                    project="project_value",
                )

                # Make the request
                page_result = client.aggregated_list(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.AggregatedListDisksRequest, dict]):
                The request object. A request message for
                Disks.AggregatedList. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.disks.pagers.AggregatedListPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.AggregatedListDisksRequest):
            request = compute.AggregatedListDisksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.aggregated_list]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project", request.project),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.AggregatedListPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def bulk_insert_unary(
        self,
        request: Optional[Union[compute.BulkInsertDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        bulk_insert_disk_resource_resource: Optional[
            compute.BulkInsertDiskResource
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Bulk create a set of disks.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_bulk_insert():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.BulkInsertDiskRequest(
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.bulk_insert(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.BulkInsertDiskRequest, dict]):
                The request object. A request message for
                Disks.BulkInsert. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            bulk_insert_disk_resource_resource (google.cloud.compute_v1.types.BulkInsertDiskResource):
                The body resource for this request
                This corresponds to the ``bulk_insert_disk_resource_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, bulk_insert_disk_resource_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.BulkInsertDiskRequest):
            request = compute.BulkInsertDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if bulk_insert_disk_resource_resource is not None:
                request.bulk_insert_disk_resource_resource = (
                    bulk_insert_disk_resource_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.bulk_insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def bulk_insert(
        self,
        request: Optional[Union[compute.BulkInsertDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        bulk_insert_disk_resource_resource: Optional[
            compute.BulkInsertDiskResource
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Bulk create a set of disks.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_bulk_insert():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.BulkInsertDiskRequest(
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.bulk_insert(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.BulkInsertDiskRequest, dict]):
                The request object. A request message for
                Disks.BulkInsert. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            bulk_insert_disk_resource_resource (google.cloud.compute_v1.types.BulkInsertDiskResource):
                The body resource for this request
                This corresponds to the ``bulk_insert_disk_resource_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, bulk_insert_disk_resource_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.BulkInsertDiskRequest):
            request = compute.BulkInsertDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if bulk_insert_disk_resource_resource is not None:
                request.bulk_insert_disk_resource_resource = (
                    bulk_insert_disk_resource_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.bulk_insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def create_snapshot_unary(
        self,
        request: Optional[Union[compute.CreateSnapshotDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        snapshot_resource: Optional[compute.Snapshot] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates a snapshot of a specified persistent disk.
        For regular snapshot creation, consider using
        snapshots.insert instead, as that method supports more
        features, such as creating snapshots in a project
        different from the source disk project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_create_snapshot():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.CreateSnapshotDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.create_snapshot(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.CreateSnapshotDiskRequest, dict]):
                The request object. A request message for
                Disks.CreateSnapshot. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                Name of the persistent disk to
                snapshot.

                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            snapshot_resource (google.cloud.compute_v1.types.Snapshot):
                The body resource for this request
                This corresponds to the ``snapshot_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk, snapshot_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.CreateSnapshotDiskRequest):
            request = compute.CreateSnapshotDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if snapshot_resource is not None:
                request.snapshot_resource = snapshot_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_snapshot]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_snapshot(
        self,
        request: Optional[Union[compute.CreateSnapshotDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        snapshot_resource: Optional[compute.Snapshot] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Creates a snapshot of a specified persistent disk.
        For regular snapshot creation, consider using
        snapshots.insert instead, as that method supports more
        features, such as creating snapshots in a project
        different from the source disk project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_create_snapshot():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.CreateSnapshotDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.create_snapshot(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.CreateSnapshotDiskRequest, dict]):
                The request object. A request message for
                Disks.CreateSnapshot. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                Name of the persistent disk to
                snapshot.

                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            snapshot_resource (google.cloud.compute_v1.types.Snapshot):
                The body resource for this request
                This corresponds to the ``snapshot_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk, snapshot_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.CreateSnapshotDiskRequest):
            request = compute.CreateSnapshotDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if snapshot_resource is not None:
                request.snapshot_resource = snapshot_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_snapshot]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def delete_unary(
        self,
        request: Optional[Union[compute.DeleteDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes the specified persistent disk. Deleting a
        disk removes its data permanently and is irreversible.
        However, deleting a disk does not delete any snapshots
        previously made from the disk. You must separately
        delete snapshots.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_delete():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.DeleteDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.delete(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteDiskRequest, dict]):
                The request object. A request message for Disks.Delete.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                Name of the persistent disk to
                delete.

                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.DeleteDiskRequest):
            request = compute.DeleteDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete(
        self,
        request: Optional[Union[compute.DeleteDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Deletes the specified persistent disk. Deleting a
        disk removes its data permanently and is irreversible.
        However, deleting a disk does not delete any snapshots
        previously made from the disk. You must separately
        delete snapshots.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_delete():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.DeleteDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.delete(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteDiskRequest, dict]):
                The request object. A request message for Disks.Delete.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                Name of the persistent disk to
                delete.

                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.DeleteDiskRequest):
            request = compute.DeleteDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def get(
        self,
        request: Optional[Union[compute.GetDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Disk:
        r"""Returns the specified persistent disk.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_get():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.GetDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.get(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.GetDiskRequest, dict]):
                The request object. A request message for Disks.Get. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                Name of the persistent disk to
                return.

                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Disk:
                Represents a Persistent Disk resource. Google Compute
                Engine has two Disk resources: \*
                [Zonal](/compute/docs/reference/rest/v1/disks) \*
                [Regional](/compute/docs/reference/rest/v1/regionDisks)
                Persistent disks are required for running your VM
                instances. Create both boot and non-boot (data)
                persistent disks. For more information, read Persistent
                Disks. For more storage options, read Storage options.
                The disks resource represents a zonal persistent disk.
                For more information, read Zonal persistent disks. The
                regionDisks resource represents a regional persistent
                disk. For more information, read Regional resources.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.GetDiskRequest):
            request = compute.GetDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: Optional[Union[compute.GetIamPolicyDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Gets the access control policy for a resource. May be
        empty if no such policy or resource exists.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_get_iam_policy():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.GetIamPolicyDiskRequest(
                    project="project_value",
                    resource="resource_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.GetIamPolicyDiskRequest, dict]):
                The request object. A request message for
                Disks.GetIamPolicy. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                Policy is a collection of bindings. A binding binds one
                or more members, or principals, to a single role.
                Principals can be user accounts, service accounts,
                Google groups, and domains (such as G Suite). A role is
                a named list of permissions; each role can be an IAM
                predefined role or a user-created custom role. For some
                types of Google Cloud resources, a binding can also
                specify a condition, which is a logical expression that
                allows access to a resource only if the expression
                evaluates to true. A condition can add constraints based
                on attributes of the request, the resource, or both. To
                learn which resources support conditions in their IAM
                policies, see the [IAM
                documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).
                **JSON example:**
                :literal:`\` { "bindings": [ { "role": "roles/resourcemanager.organizationAdmin", "members": [ "user:mike@example.com", "group:admins@example.com", "domain:google.com", "serviceAccount:my-project-id@appspot.gserviceaccount.com" ] }, { "role": "roles/resourcemanager.organizationViewer", "members": [ "user:eve@example.com" ], "condition": { "title": "expirable access", "description": "Does not grant access after Sep 2020", "expression": "request.time < timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag": "BwWWja0YfJA=", "version": 3 }`\ \`
                **YAML example:**
                :literal:`\` bindings: - members: - user:mike@example.com - group:admins@example.com - domain:google.com - serviceAccount:my-project-id@appspot.gserviceaccount.com role: roles/resourcemanager.organizationAdmin - members: - user:eve@example.com role: roles/resourcemanager.organizationViewer condition: title: expirable access description: Does not grant access after Sep 2020 expression: request.time < timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA= version: 3`\ \`
                For a description of IAM and its features, see the [IAM
                documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.GetIamPolicyDiskRequest):
            request = compute.GetIamPolicyDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def insert_unary(
        self,
        request: Optional[Union[compute.InsertDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk_resource: Optional[compute.Disk] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates a persistent disk in the specified project
        using the data in the request. You can create a disk
        from a source (sourceImage, sourceSnapshot, or
        sourceDisk) or create an empty 500 GB data disk by
        omitting all properties. You can also create a disk that
        is larger than the default size by specifying the sizeGb
        property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_insert():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.InsertDiskRequest(
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.insert(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.InsertDiskRequest, dict]):
                The request object. A request message for Disks.Insert.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk_resource (google.cloud.compute_v1.types.Disk):
                The body resource for this request
                This corresponds to the ``disk_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.InsertDiskRequest):
            request = compute.InsertDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk_resource is not None:
                request.disk_resource = disk_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def insert(
        self,
        request: Optional[Union[compute.InsertDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk_resource: Optional[compute.Disk] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Creates a persistent disk in the specified project
        using the data in the request. You can create a disk
        from a source (sourceImage, sourceSnapshot, or
        sourceDisk) or create an empty 500 GB data disk by
        omitting all properties. You can also create a disk that
        is larger than the default size by specifying the sizeGb
        property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_insert():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.InsertDiskRequest(
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.insert(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.InsertDiskRequest, dict]):
                The request object. A request message for Disks.Insert.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk_resource (google.cloud.compute_v1.types.Disk):
                The body resource for this request
                This corresponds to the ``disk_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.InsertDiskRequest):
            request = compute.InsertDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk_resource is not None:
                request.disk_resource = disk_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def list(
        self,
        request: Optional[Union[compute.ListDisksRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPager:
        r"""Retrieves a list of persistent disks contained within
        the specified zone.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_list():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.ListDisksRequest(
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                page_result = client.list(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ListDisksRequest, dict]):
                The request object. A request message for Disks.List. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.disks.pagers.ListPager:
                A list of Disk resources.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.ListDisksRequest):
            request = compute.ListDisksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def remove_resource_policies_unary(
        self,
        request: Optional[
            Union[compute.RemoveResourcePoliciesDiskRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disks_remove_resource_policies_request_resource: Optional[
            compute.DisksRemoveResourcePoliciesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Removes resource policies from a disk.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_remove_resource_policies():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.RemoveResourcePoliciesDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.remove_resource_policies(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.RemoveResourcePoliciesDiskRequest, dict]):
                The request object. A request message for
                Disks.RemoveResourcePolicies. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The disk name for this request.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_remove_resource_policies_request_resource (google.cloud.compute_v1.types.DisksRemoveResourcePoliciesRequest):
                The body resource for this request
                This corresponds to the ``disks_remove_resource_policies_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, disk, disks_remove_resource_policies_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.RemoveResourcePoliciesDiskRequest):
            request = compute.RemoveResourcePoliciesDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disks_remove_resource_policies_request_resource is not None:
                request.disks_remove_resource_policies_request_resource = (
                    disks_remove_resource_policies_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_resource_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def remove_resource_policies(
        self,
        request: Optional[
            Union[compute.RemoveResourcePoliciesDiskRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disks_remove_resource_policies_request_resource: Optional[
            compute.DisksRemoveResourcePoliciesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Removes resource policies from a disk.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_remove_resource_policies():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.RemoveResourcePoliciesDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.remove_resource_policies(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.RemoveResourcePoliciesDiskRequest, dict]):
                The request object. A request message for
                Disks.RemoveResourcePolicies. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The disk name for this request.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_remove_resource_policies_request_resource (google.cloud.compute_v1.types.DisksRemoveResourcePoliciesRequest):
                The body resource for this request
                This corresponds to the ``disks_remove_resource_policies_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, disk, disks_remove_resource_policies_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.RemoveResourcePoliciesDiskRequest):
            request = compute.RemoveResourcePoliciesDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disks_remove_resource_policies_request_resource is not None:
                request.disks_remove_resource_policies_request_resource = (
                    disks_remove_resource_policies_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_resource_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def resize_unary(
        self,
        request: Optional[Union[compute.ResizeDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disks_resize_request_resource: Optional[compute.DisksResizeRequest] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Resizes the specified persistent disk. You can only
        increase the size of the disk.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_resize():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.ResizeDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.resize(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ResizeDiskRequest, dict]):
                The request object. A request message for Disks.Resize.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The name of the persistent disk.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_resize_request_resource (google.cloud.compute_v1.types.DisksResizeRequest):
                The body resource for this request
                This corresponds to the ``disks_resize_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk, disks_resize_request_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.ResizeDiskRequest):
            request = compute.ResizeDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disks_resize_request_resource is not None:
                request.disks_resize_request_resource = disks_resize_request_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resize]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def resize(
        self,
        request: Optional[Union[compute.ResizeDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disks_resize_request_resource: Optional[compute.DisksResizeRequest] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Resizes the specified persistent disk. You can only
        increase the size of the disk.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_resize():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.ResizeDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.resize(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ResizeDiskRequest, dict]):
                The request object. A request message for Disks.Resize.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The name of the persistent disk.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_resize_request_resource (google.cloud.compute_v1.types.DisksResizeRequest):
                The body resource for this request
                This corresponds to the ``disks_resize_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk, disks_resize_request_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.ResizeDiskRequest):
            request = compute.ResizeDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disks_resize_request_resource is not None:
                request.disks_resize_request_resource = disks_resize_request_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resize]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: Optional[Union[compute.SetIamPolicyDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        resource: Optional[str] = None,
        zone_set_policy_request_resource: Optional[compute.ZoneSetPolicyRequest] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Sets the access control policy on the specified
        resource. Replaces any existing policy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_set_iam_policy():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.SetIamPolicyDiskRequest(
                    project="project_value",
                    resource="resource_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.SetIamPolicyDiskRequest, dict]):
                The request object. A request message for
                Disks.SetIamPolicy. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone_set_policy_request_resource (google.cloud.compute_v1.types.ZoneSetPolicyRequest):
                The body resource for this request
                This corresponds to the ``zone_set_policy_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                Policy is a collection of bindings. A binding binds one
                or more members, or principals, to a single role.
                Principals can be user accounts, service accounts,
                Google groups, and domains (such as G Suite). A role is
                a named list of permissions; each role can be an IAM
                predefined role or a user-created custom role. For some
                types of Google Cloud resources, a binding can also
                specify a condition, which is a logical expression that
                allows access to a resource only if the expression
                evaluates to true. A condition can add constraints based
                on attributes of the request, the resource, or both. To
                learn which resources support conditions in their IAM
                policies, see the [IAM
                documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).
                **JSON example:**
                :literal:`\` { "bindings": [ { "role": "roles/resourcemanager.organizationAdmin", "members": [ "user:mike@example.com", "group:admins@example.com", "domain:google.com", "serviceAccount:my-project-id@appspot.gserviceaccount.com" ] }, { "role": "roles/resourcemanager.organizationViewer", "members": [ "user:eve@example.com" ], "condition": { "title": "expirable access", "description": "Does not grant access after Sep 2020", "expression": "request.time < timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag": "BwWWja0YfJA=", "version": 3 }`\ \`
                **YAML example:**
                :literal:`\` bindings: - members: - user:mike@example.com - group:admins@example.com - domain:google.com - serviceAccount:my-project-id@appspot.gserviceaccount.com role: roles/resourcemanager.organizationAdmin - members: - user:eve@example.com role: roles/resourcemanager.organizationViewer condition: title: expirable access description: Does not grant access after Sep 2020 expression: request.time < timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA= version: 3`\ \`
                For a description of IAM and its features, see the [IAM
                documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, resource, zone_set_policy_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.SetIamPolicyDiskRequest):
            request = compute.SetIamPolicyDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource
            if zone_set_policy_request_resource is not None:
                request.zone_set_policy_request_resource = (
                    zone_set_policy_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_labels_unary(
        self,
        request: Optional[Union[compute.SetLabelsDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        resource: Optional[str] = None,
        zone_set_labels_request_resource: Optional[compute.ZoneSetLabelsRequest] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets the labels on a disk. To learn more about
        labels, read the Labeling Resources documentation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_set_labels():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.SetLabelsDiskRequest(
                    project="project_value",
                    resource="resource_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.set_labels(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.SetLabelsDiskRequest, dict]):
                The request object. A request message for
                Disks.SetLabels. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone_set_labels_request_resource (google.cloud.compute_v1.types.ZoneSetLabelsRequest):
                The body resource for this request
                This corresponds to the ``zone_set_labels_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, resource, zone_set_labels_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.SetLabelsDiskRequest):
            request = compute.SetLabelsDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource
            if zone_set_labels_request_resource is not None:
                request.zone_set_labels_request_resource = (
                    zone_set_labels_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_labels]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_labels(
        self,
        request: Optional[Union[compute.SetLabelsDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        resource: Optional[str] = None,
        zone_set_labels_request_resource: Optional[compute.ZoneSetLabelsRequest] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets the labels on a disk. To learn more about
        labels, read the Labeling Resources documentation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_set_labels():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.SetLabelsDiskRequest(
                    project="project_value",
                    resource="resource_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.set_labels(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.SetLabelsDiskRequest, dict]):
                The request object. A request message for
                Disks.SetLabels. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone_set_labels_request_resource (google.cloud.compute_v1.types.ZoneSetLabelsRequest):
                The body resource for this request
                This corresponds to the ``zone_set_labels_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, resource, zone_set_labels_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.SetLabelsDiskRequest):
            request = compute.SetLabelsDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource
            if zone_set_labels_request_resource is not None:
                request.zone_set_labels_request_resource = (
                    zone_set_labels_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_labels]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def start_async_replication_unary(
        self,
        request: Optional[Union[compute.StartAsyncReplicationDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disks_start_async_replication_request_resource: Optional[
            compute.DisksStartAsyncReplicationRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Starts asynchronous replication. Must be invoked on
        the primary disk.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_start_async_replication():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.StartAsyncReplicationDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.start_async_replication(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.StartAsyncReplicationDiskRequest, dict]):
                The request object. A request message for
                Disks.StartAsyncReplication. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The name of the persistent disk.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_start_async_replication_request_resource (google.cloud.compute_v1.types.DisksStartAsyncReplicationRequest):
                The body resource for this request
                This corresponds to the ``disks_start_async_replication_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, disk, disks_start_async_replication_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.StartAsyncReplicationDiskRequest):
            request = compute.StartAsyncReplicationDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disks_start_async_replication_request_resource is not None:
                request.disks_start_async_replication_request_resource = (
                    disks_start_async_replication_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start_async_replication]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def start_async_replication(
        self,
        request: Optional[Union[compute.StartAsyncReplicationDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disks_start_async_replication_request_resource: Optional[
            compute.DisksStartAsyncReplicationRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Starts asynchronous replication. Must be invoked on
        the primary disk.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_start_async_replication():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.StartAsyncReplicationDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.start_async_replication(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.StartAsyncReplicationDiskRequest, dict]):
                The request object. A request message for
                Disks.StartAsyncReplication. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The name of the persistent disk.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_start_async_replication_request_resource (google.cloud.compute_v1.types.DisksStartAsyncReplicationRequest):
                The body resource for this request
                This corresponds to the ``disks_start_async_replication_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, disk, disks_start_async_replication_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.StartAsyncReplicationDiskRequest):
            request = compute.StartAsyncReplicationDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disks_start_async_replication_request_resource is not None:
                request.disks_start_async_replication_request_resource = (
                    disks_start_async_replication_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start_async_replication]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def stop_async_replication_unary(
        self,
        request: Optional[Union[compute.StopAsyncReplicationDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Stops asynchronous replication. Can be invoked either
        on the primary or on the secondary disk.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_stop_async_replication():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.StopAsyncReplicationDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.stop_async_replication(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.StopAsyncReplicationDiskRequest, dict]):
                The request object. A request message for
                Disks.StopAsyncReplication. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The name of the persistent disk.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.StopAsyncReplicationDiskRequest):
            request = compute.StopAsyncReplicationDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.stop_async_replication]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def stop_async_replication(
        self,
        request: Optional[Union[compute.StopAsyncReplicationDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Stops asynchronous replication. Can be invoked either
        on the primary or on the secondary disk.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_stop_async_replication():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.StopAsyncReplicationDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.stop_async_replication(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.StopAsyncReplicationDiskRequest, dict]):
                The request object. A request message for
                Disks.StopAsyncReplication. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The name of the persistent disk.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.StopAsyncReplicationDiskRequest):
            request = compute.StopAsyncReplicationDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.stop_async_replication]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def stop_group_async_replication_unary(
        self,
        request: Optional[
            Union[compute.StopGroupAsyncReplicationDiskRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disks_stop_group_async_replication_resource_resource: Optional[
            compute.DisksStopGroupAsyncReplicationResource
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Stops asynchronous replication for a consistency
        group of disks. Can be invoked either in the primary or
        secondary scope.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_stop_group_async_replication():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.StopGroupAsyncReplicationDiskRequest(
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.stop_group_async_replication(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.StopGroupAsyncReplicationDiskRequest, dict]):
                The request object. A request message for
                Disks.StopGroupAsyncReplication. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request. This must be the zone of the
                primary or secondary disks in the
                consistency group.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_stop_group_async_replication_resource_resource (google.cloud.compute_v1.types.DisksStopGroupAsyncReplicationResource):
                The body resource for this request
                This corresponds to the ``disks_stop_group_async_replication_resource_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, disks_stop_group_async_replication_resource_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.StopGroupAsyncReplicationDiskRequest):
            request = compute.StopGroupAsyncReplicationDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disks_stop_group_async_replication_resource_resource is not None:
                request.disks_stop_group_async_replication_resource_resource = (
                    disks_stop_group_async_replication_resource_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.stop_group_async_replication
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def stop_group_async_replication(
        self,
        request: Optional[
            Union[compute.StopGroupAsyncReplicationDiskRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disks_stop_group_async_replication_resource_resource: Optional[
            compute.DisksStopGroupAsyncReplicationResource
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Stops asynchronous replication for a consistency
        group of disks. Can be invoked either in the primary or
        secondary scope.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_stop_group_async_replication():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.StopGroupAsyncReplicationDiskRequest(
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.stop_group_async_replication(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.StopGroupAsyncReplicationDiskRequest, dict]):
                The request object. A request message for
                Disks.StopGroupAsyncReplication. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request. This must be the zone of the
                primary or secondary disks in the
                consistency group.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disks_stop_group_async_replication_resource_resource (google.cloud.compute_v1.types.DisksStopGroupAsyncReplicationResource):
                The body resource for this request
                This corresponds to the ``disks_stop_group_async_replication_resource_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, disks_stop_group_async_replication_resource_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.StopGroupAsyncReplicationDiskRequest):
            request = compute.StopGroupAsyncReplicationDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disks_stop_group_async_replication_resource_resource is not None:
                request.disks_stop_group_async_replication_resource_resource = (
                    disks_stop_group_async_replication_resource_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.stop_group_async_replication
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: Optional[Union[compute.TestIamPermissionsDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        resource: Optional[str] = None,
        test_permissions_request_resource: Optional[
            compute.TestPermissionsRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.TestPermissionsResponse:
        r"""Returns permissions that a caller has on the
        specified resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_test_iam_permissions():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.TestIamPermissionsDiskRequest(
                    project="project_value",
                    resource="resource_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.TestIamPermissionsDiskRequest, dict]):
                The request object. A request message for
                Disks.TestIamPermissions. See the method
                description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (str):
                Name or id of the resource for this
                request.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            test_permissions_request_resource (google.cloud.compute_v1.types.TestPermissionsRequest):
                The body resource for this request
                This corresponds to the ``test_permissions_request_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.TestPermissionsResponse:

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [project, zone, resource, test_permissions_request_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.TestIamPermissionsDiskRequest):
            request = compute.TestIamPermissionsDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if resource is not None:
                request.resource = resource
            if test_permissions_request_resource is not None:
                request.test_permissions_request_resource = (
                    test_permissions_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("resource", request.resource),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_unary(
        self,
        request: Optional[Union[compute.UpdateDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disk_resource: Optional[compute.Disk] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Updates the specified disk with the data included in the
        request. The update is performed only on selected fields
        included as part of update-mask. Only the following fields can
        be modified: user_license.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_update():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.UpdateDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.update(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateDiskRequest, dict]):
                The request object. A request message for Disks.Update.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The disk name for this request.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk_resource (google.cloud.compute_v1.types.Disk):
                The body resource for this request
                This corresponds to the ``disk_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk, disk_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.UpdateDiskRequest):
            request = compute.UpdateDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disk_resource is not None:
                request.disk_resource = disk_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update(
        self,
        request: Optional[Union[compute.UpdateDiskRequest, dict]] = None,
        *,
        project: Optional[str] = None,
        zone: Optional[str] = None,
        disk: Optional[str] = None,
        disk_resource: Optional[compute.Disk] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Updates the specified disk with the data included in the
        request. The update is performed only on selected fields
        included as part of update-mask. Only the following fields can
        be modified: user_license.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_update():
                # Create a client
                client = compute_v1.DisksClient()

                # Initialize request argument(s)
                request = compute_v1.UpdateDiskRequest(
                    disk="disk_value",
                    project="project_value",
                    zone="zone_value",
                )

                # Make the request
                response = client.update(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.UpdateDiskRequest, dict]):
                The request object. A request message for Disks.Update.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (str):
                The name of the zone for this
                request.

                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk (str):
                The disk name for this request.
                This corresponds to the ``disk`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            disk_resource (google.cloud.compute_v1.types.Disk):
                The body resource for this request
                This corresponds to the ``disk_resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.extended_operation.ExtendedOperation:
                An object representing a extended
                long-running operation.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, zone, disk, disk_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.UpdateDiskRequest):
            request = compute.UpdateDiskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if zone is not None:
                request.zone = zone
            if disk is not None:
                request.disk = disk
            if disk_resource is not None:
                request.disk_resource = disk_resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("zone", request.zone),
                    ("disk", request.disk),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        operation_service = self._transport._zone_operations_client
        operation_request = compute.GetZoneOperationRequest()
        operation_request.project = request.project
        operation_request.zone = request.zone
        operation_request.operation = response.name

        get_operation = functools.partial(operation_service.get, operation_request)
        # Cancel is not part of extended operations yet.
        cancel_operation = lambda: None

        # Note: this class is an implementation detail to provide a uniform
        # set of names for certain fields in the extended operation proto message.
        # See google.api_core.extended_operation.ExtendedOperation for details
        # on these properties and the  expected interface.
        class _CustomOperation(extended_operation.ExtendedOperation):
            @property
            def error_message(self):
                return self._extended_operation.http_error_message

            @property
            def error_code(self):
                return self._extended_operation.http_error_status_code

        response = _CustomOperation.make(get_operation, cancel_operation, response)

        # Done; return the response.
        return response

    def __enter__(self) -> "DisksClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("DisksClient",)
