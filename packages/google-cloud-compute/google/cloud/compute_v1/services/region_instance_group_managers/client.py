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

from google.cloud.compute_v1.services.region_instance_group_managers import pagers
from google.cloud.compute_v1.types import compute

from .transports.base import DEFAULT_CLIENT_INFO, RegionInstanceGroupManagersTransport
from .transports.rest import RegionInstanceGroupManagersRestTransport


class RegionInstanceGroupManagersClientMeta(type):
    """Metaclass for the RegionInstanceGroupManagers client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[RegionInstanceGroupManagersTransport]]
    _transport_registry["rest"] = RegionInstanceGroupManagersRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[RegionInstanceGroupManagersTransport]:
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


class RegionInstanceGroupManagersClient(
    metaclass=RegionInstanceGroupManagersClientMeta
):
    """The RegionInstanceGroupManagers API."""

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
            RegionInstanceGroupManagersClient: The constructed client.
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
            RegionInstanceGroupManagersClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> RegionInstanceGroupManagersTransport:
        """Returns the transport used by the client instance.

        Returns:
            RegionInstanceGroupManagersTransport: The transport used by the client
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
            _default_universe = RegionInstanceGroupManagersClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = RegionInstanceGroupManagersClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = (
                RegionInstanceGroupManagersClient._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=universe_domain
                )
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
        universe_domain = RegionInstanceGroupManagersClient._DEFAULT_UNIVERSE
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
            Union[
                str,
                RegionInstanceGroupManagersTransport,
                Callable[..., RegionInstanceGroupManagersTransport],
            ]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the region instance group managers client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,RegionInstanceGroupManagersTransport,Callable[..., RegionInstanceGroupManagersTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the RegionInstanceGroupManagersTransport constructor.
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
        ) = RegionInstanceGroupManagersClient._read_environment_variables()
        self._client_cert_source = (
            RegionInstanceGroupManagersClient._get_client_cert_source(
                self._client_options.client_cert_source, self._use_client_cert
            )
        )
        self._universe_domain = RegionInstanceGroupManagersClient._get_universe_domain(
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
        transport_provided = isinstance(transport, RegionInstanceGroupManagersTransport)
        if transport_provided:
            # transport is a RegionInstanceGroupManagersTransport instance.
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
            self._transport = cast(RegionInstanceGroupManagersTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or RegionInstanceGroupManagersClient._get_api_endpoint(
                self._client_options.api_endpoint,
                self._client_cert_source,
                self._universe_domain,
                self._use_mtls_endpoint,
            )
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
                Type[RegionInstanceGroupManagersTransport],
                Callable[..., RegionInstanceGroupManagersTransport],
            ] = (
                RegionInstanceGroupManagersClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(
                    Callable[..., RegionInstanceGroupManagersTransport], transport
                )
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

    def abandon_instances_unary(
        self,
        request: Optional[
            Union[compute.AbandonInstancesRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_abandon_instances_request_resource: Optional[
            compute.RegionInstanceGroupManagersAbandonInstancesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Flags the specified instances to be immediately
        removed from the managed instance group. Abandoning an
        instance does not delete the instance, but it does
        remove the instance from any target pools that are
        applied by the managed instance group. This method
        reduces the targetSize of the managed instance group by
        the number of instances that you abandon. This operation
        is marked as DONE when the action is scheduled even if
        the instances have not yet been removed from the group.
        You must separately verify the status of the abandoning
        action with the listmanagedinstances method. If the
        group is part of a backend service that has enabled
        connection draining, it can take up to 60 seconds after
        the connection draining duration has elapsed before the
        VM instance is removed or deleted. You can specify a
        maximum of 1000 instances with this method per request.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_abandon_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.AbandonInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.abandon_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.AbandonInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.AbandonInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_abandon_instances_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersAbandonInstancesRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_abandon_instances_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_abandon_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.AbandonInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.AbandonInstancesRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_abandon_instances_request_resource
                is not None
            ):
                request.region_instance_group_managers_abandon_instances_request_resource = (
                    region_instance_group_managers_abandon_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.abandon_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def abandon_instances(
        self,
        request: Optional[
            Union[compute.AbandonInstancesRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_abandon_instances_request_resource: Optional[
            compute.RegionInstanceGroupManagersAbandonInstancesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Flags the specified instances to be immediately
        removed from the managed instance group. Abandoning an
        instance does not delete the instance, but it does
        remove the instance from any target pools that are
        applied by the managed instance group. This method
        reduces the targetSize of the managed instance group by
        the number of instances that you abandon. This operation
        is marked as DONE when the action is scheduled even if
        the instances have not yet been removed from the group.
        You must separately verify the status of the abandoning
        action with the listmanagedinstances method. If the
        group is part of a backend service that has enabled
        connection draining, it can take up to 60 seconds after
        the connection draining duration has elapsed before the
        VM instance is removed or deleted. You can specify a
        maximum of 1000 instances with this method per request.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_abandon_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.AbandonInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.abandon_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.AbandonInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.AbandonInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_abandon_instances_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersAbandonInstancesRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_abandon_instances_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_abandon_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.AbandonInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.AbandonInstancesRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_abandon_instances_request_resource
                is not None
            ):
                request.region_instance_group_managers_abandon_instances_request_resource = (
                    region_instance_group_managers_abandon_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.abandon_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def apply_updates_to_instances_unary(
        self,
        request: Optional[
            Union[
                compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest, dict
            ]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_apply_updates_request_resource: Optional[
            compute.RegionInstanceGroupManagersApplyUpdatesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Apply updates to selected instances the managed
        instance group.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_apply_updates_to_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.apply_updates_to_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.ApplyUpdatesToInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request, should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group, should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_apply_updates_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersApplyUpdatesRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_apply_updates_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_apply_updates_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_apply_updates_request_resource
                is not None
            ):
                request.region_instance_group_managers_apply_updates_request_resource = (
                    region_instance_group_managers_apply_updates_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.apply_updates_to_instances
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def apply_updates_to_instances(
        self,
        request: Optional[
            Union[
                compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest, dict
            ]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_apply_updates_request_resource: Optional[
            compute.RegionInstanceGroupManagersApplyUpdatesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Apply updates to selected instances the managed
        instance group.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_apply_updates_to_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.apply_updates_to_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.ApplyUpdatesToInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request, should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group, should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_apply_updates_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersApplyUpdatesRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_apply_updates_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_apply_updates_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_apply_updates_request_resource
                is not None
            ):
                request.region_instance_group_managers_apply_updates_request_resource = (
                    region_instance_group_managers_apply_updates_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.apply_updates_to_instances
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def create_instances_unary(
        self,
        request: Optional[
            Union[compute.CreateInstancesRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_create_instances_request_resource: Optional[
            compute.RegionInstanceGroupManagersCreateInstancesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates instances with per-instance configurations in
        this regional managed instance group. Instances are
        created using the current instance template. The create
        instances operation is marked DONE if the
        createInstances request is successful. The underlying
        actions take additional time. You must separately verify
        the status of the creating or actions with the
        listmanagedinstances method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_create_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.CreateInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.create_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.CreateInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.CreateInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                The name of the region where the
                managed instance group is located. It
                should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group. It should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_create_instances_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersCreateInstancesRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_create_instances_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_create_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.CreateInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.CreateInstancesRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_create_instances_request_resource
                is not None
            ):
                request.region_instance_group_managers_create_instances_request_resource = (
                    region_instance_group_managers_create_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def create_instances(
        self,
        request: Optional[
            Union[compute.CreateInstancesRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_create_instances_request_resource: Optional[
            compute.RegionInstanceGroupManagersCreateInstancesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Creates instances with per-instance configurations in
        this regional managed instance group. Instances are
        created using the current instance template. The create
        instances operation is marked DONE if the
        createInstances request is successful. The underlying
        actions take additional time. You must separately verify
        the status of the creating or actions with the
        listmanagedinstances method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_create_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.CreateInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.create_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.CreateInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.CreateInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                The name of the region where the
                managed instance group is located. It
                should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group. It should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_create_instances_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersCreateInstancesRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_create_instances_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_create_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.CreateInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.CreateInstancesRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_create_instances_request_resource
                is not None
            ):
                request.region_instance_group_managers_create_instances_request_resource = (
                    region_instance_group_managers_create_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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
        request: Optional[
            Union[compute.DeleteRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes the specified managed instance group and all
        of the instances in that group.

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
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.DeleteRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.delete(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.Delete. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group to
                delete.

                This corresponds to the ``instance_group_manager`` field
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
        has_flattened_params = any([project, region, instance_group_manager])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.DeleteRegionInstanceGroupManagerRequest):
            request = compute.DeleteRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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
        request: Optional[
            Union[compute.DeleteRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Deletes the specified managed instance group and all
        of the instances in that group.

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
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.DeleteRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.delete(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.Delete. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group to
                delete.

                This corresponds to the ``instance_group_manager`` field
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
        has_flattened_params = any([project, region, instance_group_manager])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.DeleteRegionInstanceGroupManagerRequest):
            request = compute.DeleteRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def delete_instances_unary(
        self,
        request: Optional[
            Union[compute.DeleteInstancesRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_delete_instances_request_resource: Optional[
            compute.RegionInstanceGroupManagersDeleteInstancesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Flags the specified instances in the managed instance
        group to be immediately deleted. The instances are also
        removed from any target pools of which they were a
        member. This method reduces the targetSize of the
        managed instance group by the number of instances that
        you delete. The deleteInstances operation is marked DONE
        if the deleteInstances request is successful. The
        underlying actions take additional time. You must
        separately verify the status of the deleting action with
        the listmanagedinstances method. If the group is part of
        a backend service that has enabled connection draining,
        it can take up to 60 seconds after the connection
        draining duration has elapsed before the VM instance is
        removed or deleted. You can specify a maximum of 1000
        instances with this method per request.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_delete_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.DeleteInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.delete_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.DeleteInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_delete_instances_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersDeleteInstancesRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_delete_instances_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_delete_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.DeleteInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.DeleteInstancesRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_delete_instances_request_resource
                is not None
            ):
                request.region_instance_group_managers_delete_instances_request_resource = (
                    region_instance_group_managers_delete_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def delete_instances(
        self,
        request: Optional[
            Union[compute.DeleteInstancesRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_delete_instances_request_resource: Optional[
            compute.RegionInstanceGroupManagersDeleteInstancesRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Flags the specified instances in the managed instance
        group to be immediately deleted. The instances are also
        removed from any target pools of which they were a
        member. This method reduces the targetSize of the
        managed instance group by the number of instances that
        you delete. The deleteInstances operation is marked DONE
        if the deleteInstances request is successful. The
        underlying actions take additional time. You must
        separately verify the status of the deleting action with
        the listmanagedinstances method. If the group is part of
        a backend service that has enabled connection draining,
        it can take up to 60 seconds after the connection
        draining duration has elapsed before the VM instance is
        removed or deleted. You can specify a maximum of 1000
        instances with this method per request.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_delete_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.DeleteInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.delete_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.DeleteInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.DeleteInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_delete_instances_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersDeleteInstancesRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_delete_instances_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_delete_instances_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.DeleteInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.DeleteInstancesRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_delete_instances_request_resource
                is not None
            ):
                request.region_instance_group_managers_delete_instances_request_resource = (
                    region_instance_group_managers_delete_instances_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def delete_per_instance_configs_unary(
        self,
        request: Optional[
            Union[
                compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest, dict
            ]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_manager_delete_instance_config_req_resource: Optional[
            compute.RegionInstanceGroupManagerDeleteInstanceConfigReq
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Deletes selected per-instance configurations for the
        managed instance group.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_delete_per_instance_configs():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.delete_per_instance_configs(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.DeletePerInstanceConfigs.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request, should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group. It should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_manager_delete_instance_config_req_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagerDeleteInstanceConfigReq):
                The body resource for this request
                This corresponds to the ``region_instance_group_manager_delete_instance_config_req_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_manager_delete_instance_config_req_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest
        ):
            request = compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_manager_delete_instance_config_req_resource
                is not None
            ):
                request.region_instance_group_manager_delete_instance_config_req_resource = (
                    region_instance_group_manager_delete_instance_config_req_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_per_instance_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def delete_per_instance_configs(
        self,
        request: Optional[
            Union[
                compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest, dict
            ]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_manager_delete_instance_config_req_resource: Optional[
            compute.RegionInstanceGroupManagerDeleteInstanceConfigReq
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Deletes selected per-instance configurations for the
        managed instance group.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_delete_per_instance_configs():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.delete_per_instance_configs(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.DeletePerInstanceConfigs.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request, should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group. It should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_manager_delete_instance_config_req_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagerDeleteInstanceConfigReq):
                The body resource for this request
                This corresponds to the ``region_instance_group_manager_delete_instance_config_req_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_manager_delete_instance_config_req_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest
        ):
            request = compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_manager_delete_instance_config_req_resource
                is not None
            ):
                request.region_instance_group_manager_delete_instance_config_req_resource = (
                    region_instance_group_manager_delete_instance_config_req_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_per_instance_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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
        request: Optional[
            Union[compute.GetRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.InstanceGroupManager:
        r"""Returns all of the details about the specified
        managed instance group.

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
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.GetRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.get(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.GetRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.Get. See the
                method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group to
                return.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.types.InstanceGroupManager:
                Represents a Managed Instance Group
                resource. An instance group is a
                collection of VM instances that you can
                manage as a single entity. For more
                information, read Instance groups. For
                zonal Managed Instance Group, use the
                instanceGroupManagers resource. For
                regional Managed Instance Group, use the
                regionInstanceGroupManagers resource.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, region, instance_group_manager])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.GetRegionInstanceGroupManagerRequest):
            request = compute.GetRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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
        request: Optional[
            Union[compute.InsertRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager_resource: Optional[compute.InstanceGroupManager] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Creates a managed instance group using the
        information that you specify in the request. After the
        group is created, instances in the group are created
        using the specified instance template. This operation is
        marked as DONE when the group is created even if the
        instances in the group have not yet been created. You
        must separately verify the status of the individual
        instances with the listmanagedinstances method. A
        regional managed instance group can contain up to 2000
        instances.

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
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.InsertRegionInstanceGroupManagerRequest(
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.insert(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.InsertRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.Insert. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager_resource (google.cloud.compute_v1.types.InstanceGroupManager):
                The body resource for this request
                This corresponds to the ``instance_group_manager_resource`` field
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
        has_flattened_params = any([project, region, instance_group_manager_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.InsertRegionInstanceGroupManagerRequest):
            request = compute.InsertRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager_resource is not None:
                request.instance_group_manager_resource = (
                    instance_group_manager_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
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
        request: Optional[
            Union[compute.InsertRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager_resource: Optional[compute.InstanceGroupManager] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Creates a managed instance group using the
        information that you specify in the request. After the
        group is created, instances in the group are created
        using the specified instance template. This operation is
        marked as DONE when the group is created even if the
        instances in the group have not yet been created. You
        must separately verify the status of the individual
        instances with the listmanagedinstances method. A
        regional managed instance group can contain up to 2000
        instances.

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
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.InsertRegionInstanceGroupManagerRequest(
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.insert(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.InsertRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.Insert. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager_resource (google.cloud.compute_v1.types.InstanceGroupManager):
                The body resource for this request
                This corresponds to the ``instance_group_manager_resource`` field
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
        has_flattened_params = any([project, region, instance_group_manager_resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.InsertRegionInstanceGroupManagerRequest):
            request = compute.InsertRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager_resource is not None:
                request.instance_group_manager_resource = (
                    instance_group_manager_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.insert]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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
        request: Optional[
            Union[compute.ListRegionInstanceGroupManagersRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPager:
        r"""Retrieves the list of managed instance groups that
        are contained within the specified region.

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
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.ListRegionInstanceGroupManagersRequest(
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                page_result = client.list(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ListRegionInstanceGroupManagersRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.List. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.region_instance_group_managers.pagers.ListPager:
                Contains a list of managed instance
                groups.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, region])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.ListRegionInstanceGroupManagersRequest):
            request = compute.ListRegionInstanceGroupManagersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
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

    def list_errors(
        self,
        request: Optional[
            Union[compute.ListErrorsRegionInstanceGroupManagersRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListErrorsPager:
        r"""Lists all errors thrown by actions on instances for a
        given regional managed instance group. The filter and
        orderBy query parameters are not supported.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_list_errors():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.ListErrorsRegionInstanceGroupManagersRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                page_result = client.list_errors(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ListErrorsRegionInstanceGroupManagersRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.ListErrors.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request. This should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance group. It must be a
                string that meets the requirements in RFC1035, or an
                unsigned long integer: must match regexp pattern:
                (?:`a-z <?:[-a-z0-9]{0,61}[a-z0-9]>`__?)|1-9{0,19}.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.region_instance_group_managers.pagers.ListErrorsPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, region, instance_group_manager])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.ListErrorsRegionInstanceGroupManagersRequest
        ):
            request = compute.ListErrorsRegionInstanceGroupManagersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_errors]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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
        response = pagers.ListErrorsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_managed_instances(
        self,
        request: Optional[
            Union[compute.ListManagedInstancesRegionInstanceGroupManagersRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListManagedInstancesPager:
        r"""Lists the instances in the managed instance group and instances
        that are scheduled to be created. The list includes any current
        actions that the group has scheduled for its instances. The
        orderBy query parameter is not supported. The ``pageToken``
        query parameter is supported only if the group's
        ``listManagedInstancesResults`` field is set to ``PAGINATED``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_list_managed_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.ListManagedInstancesRegionInstanceGroupManagersRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                page_result = client.list_managed_instances(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ListManagedInstancesRegionInstanceGroupManagersRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.ListManagedInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.region_instance_group_managers.pagers.ListManagedInstancesPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, region, instance_group_manager])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.ListManagedInstancesRegionInstanceGroupManagersRequest
        ):
            request = compute.ListManagedInstancesRegionInstanceGroupManagersRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_managed_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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
        response = pagers.ListManagedInstancesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_per_instance_configs(
        self,
        request: Optional[
            Union[
                compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest, dict
            ]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPerInstanceConfigsPager:
        r"""Lists all of the per-instance configurations defined
        for the managed instance group. The orderBy query
        parameter is not supported.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_list_per_instance_configs():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.ListPerInstanceConfigsRegionInstanceGroupManagersRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                page_result = client.list_per_instance_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ListPerInstanceConfigsRegionInstanceGroupManagersRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.ListPerInstanceConfigs.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request, should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group. It should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.compute_v1.services.region_instance_group_managers.pagers.ListPerInstanceConfigsPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, region, instance_group_manager])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest
        ):
            request = compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_per_instance_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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
        response = pagers.ListPerInstanceConfigsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def patch_unary(
        self,
        request: Optional[
            Union[compute.PatchRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        instance_group_manager_resource: Optional[compute.InstanceGroupManager] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Updates a managed instance group using the
        information that you specify in the request. This
        operation is marked as DONE when the group is patched
        even if the instances in the group are still in the
        process of being patched. You must separately verify the
        status of the individual instances with the
        listmanagedinstances method. This method supports PATCH
        semantics and uses the JSON merge patch format and
        processing rules. If you update your group to specify a
        new template or instance configuration, it's possible
        that your intended specification for each VM in the
        group is different from the current state of that VM. To
        learn how to apply an updated configuration to the VMs
        in a MIG, see Updating instances in a MIG.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_patch():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.PatchRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.patch(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.PatchRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.Patch. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the instance group
                manager.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager_resource (google.cloud.compute_v1.types.InstanceGroupManager):
                The body resource for this request
                This corresponds to the ``instance_group_manager_resource`` field
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
            [project, region, instance_group_manager, instance_group_manager_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.PatchRegionInstanceGroupManagerRequest):
            request = compute.PatchRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if instance_group_manager_resource is not None:
                request.instance_group_manager_resource = (
                    instance_group_manager_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.patch]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def patch(
        self,
        request: Optional[
            Union[compute.PatchRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        instance_group_manager_resource: Optional[compute.InstanceGroupManager] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Updates a managed instance group using the
        information that you specify in the request. This
        operation is marked as DONE when the group is patched
        even if the instances in the group are still in the
        process of being patched. You must separately verify the
        status of the individual instances with the
        listmanagedinstances method. This method supports PATCH
        semantics and uses the JSON merge patch format and
        processing rules. If you update your group to specify a
        new template or instance configuration, it's possible
        that your intended specification for each VM in the
        group is different from the current state of that VM. To
        learn how to apply an updated configuration to the VMs
        in a MIG, see Updating instances in a MIG.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_patch():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.PatchRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.patch(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.PatchRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.Patch. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the instance group
                manager.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager_resource (google.cloud.compute_v1.types.InstanceGroupManager):
                The body resource for this request
                This corresponds to the ``instance_group_manager_resource`` field
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
            [project, region, instance_group_manager, instance_group_manager_resource]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.PatchRegionInstanceGroupManagerRequest):
            request = compute.PatchRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if instance_group_manager_resource is not None:
                request.instance_group_manager_resource = (
                    instance_group_manager_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.patch]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def patch_per_instance_configs_unary(
        self,
        request: Optional[
            Union[
                compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest, dict
            ]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_manager_patch_instance_config_req_resource: Optional[
            compute.RegionInstanceGroupManagerPatchInstanceConfigReq
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Inserts or patches per-instance configurations for
        the managed instance group. perInstanceConfig.name
        serves as a key used to distinguish whether to perform
        insert or patch.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_patch_per_instance_configs():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.patch_per_instance_configs(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.PatchPerInstanceConfigs.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request, should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group. It should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_manager_patch_instance_config_req_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagerPatchInstanceConfigReq):
                The body resource for this request
                This corresponds to the ``region_instance_group_manager_patch_instance_config_req_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_manager_patch_instance_config_req_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest
        ):
            request = compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_manager_patch_instance_config_req_resource
                is not None
            ):
                request.region_instance_group_manager_patch_instance_config_req_resource = (
                    region_instance_group_manager_patch_instance_config_req_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.patch_per_instance_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def patch_per_instance_configs(
        self,
        request: Optional[
            Union[
                compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest, dict
            ]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_manager_patch_instance_config_req_resource: Optional[
            compute.RegionInstanceGroupManagerPatchInstanceConfigReq
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Inserts or patches per-instance configurations for
        the managed instance group. perInstanceConfig.name
        serves as a key used to distinguish whether to perform
        insert or patch.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_patch_per_instance_configs():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.patch_per_instance_configs(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.PatchPerInstanceConfigs.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request, should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group. It should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_manager_patch_instance_config_req_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagerPatchInstanceConfigReq):
                The body resource for this request
                This corresponds to the ``region_instance_group_manager_patch_instance_config_req_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_manager_patch_instance_config_req_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest
        ):
            request = compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_manager_patch_instance_config_req_resource
                is not None
            ):
                request.region_instance_group_manager_patch_instance_config_req_resource = (
                    region_instance_group_manager_patch_instance_config_req_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.patch_per_instance_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def recreate_instances_unary(
        self,
        request: Optional[
            Union[compute.RecreateInstancesRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_recreate_request_resource: Optional[
            compute.RegionInstanceGroupManagersRecreateRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Flags the specified VM instances in the managed
        instance group to be immediately recreated. Each
        instance is recreated using the group's current
        configuration. This operation is marked as DONE when the
        flag is set even if the instances have not yet been
        recreated. You must separately verify the status of each
        instance by checking its currentAction field; for more
        information, see Checking the status of managed
        instances. If the group is part of a backend service
        that has enabled connection draining, it can take up to
        60 seconds after the connection draining duration has
        elapsed before the VM instance is removed or deleted.
        You can specify a maximum of 1000 instances with this
        method per request.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_recreate_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.RecreateInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.recreate_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.RecreateInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.RecreateInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_recreate_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersRecreateRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_recreate_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_recreate_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.RecreateInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.RecreateInstancesRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if region_instance_group_managers_recreate_request_resource is not None:
                request.region_instance_group_managers_recreate_request_resource = (
                    region_instance_group_managers_recreate_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.recreate_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def recreate_instances(
        self,
        request: Optional[
            Union[compute.RecreateInstancesRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_recreate_request_resource: Optional[
            compute.RegionInstanceGroupManagersRecreateRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Flags the specified VM instances in the managed
        instance group to be immediately recreated. Each
        instance is recreated using the group's current
        configuration. This operation is marked as DONE when the
        flag is set even if the instances have not yet been
        recreated. You must separately verify the status of each
        instance by checking its currentAction field; for more
        information, see Checking the status of managed
        instances. If the group is part of a backend service
        that has enabled connection draining, it can take up to
        60 seconds after the connection draining duration has
        elapsed before the VM instance is removed or deleted.
        You can specify a maximum of 1000 instances with this
        method per request.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_recreate_instances():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.RecreateInstancesRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.recreate_instances(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.RecreateInstancesRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.RecreateInstances.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_recreate_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersRecreateRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_recreate_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_recreate_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.RecreateInstancesRegionInstanceGroupManagerRequest
        ):
            request = compute.RecreateInstancesRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if region_instance_group_managers_recreate_request_resource is not None:
                request.region_instance_group_managers_recreate_request_resource = (
                    region_instance_group_managers_recreate_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.recreate_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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
        request: Optional[
            Union[compute.ResizeRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        size: Optional[int] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Changes the intended size of the managed instance
        group. If you increase the size, the group creates new
        instances using the current instance template. If you
        decrease the size, the group deletes one or more
        instances. The resize operation is marked DONE if the
        resize request is successful. The underlying actions
        take additional time. You must separately verify the
        status of the creating or deleting actions with the
        listmanagedinstances method. If the group is part of a
        backend service that has enabled connection draining, it
        can take up to 60 seconds after the connection draining
        duration has elapsed before the VM instance is removed
        or deleted.

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
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.ResizeRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                    size=443,
                )

                # Make the request
                response = client.resize(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ResizeRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.Resize. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            size (int):
                Number of instances that should exist
                in this instance group manager.

                This corresponds to the ``size`` field
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
        has_flattened_params = any([project, region, instance_group_manager, size])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.ResizeRegionInstanceGroupManagerRequest):
            request = compute.ResizeRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if size is not None:
                request.size = size

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resize]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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
        request: Optional[
            Union[compute.ResizeRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        size: Optional[int] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Changes the intended size of the managed instance
        group. If you increase the size, the group creates new
        instances using the current instance template. If you
        decrease the size, the group deletes one or more
        instances. The resize operation is marked DONE if the
        resize request is successful. The underlying actions
        take additional time. You must separately verify the
        status of the creating or deleting actions with the
        listmanagedinstances method. If the group is part of a
        backend service that has enabled connection draining, it
        can take up to 60 seconds after the connection draining
        duration has elapsed before the VM instance is removed
        or deleted.

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
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.ResizeRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                    size=443,
                )

                # Make the request
                response = client.resize(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.ResizeRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.Resize. See
                the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            size (int):
                Number of instances that should exist
                in this instance group manager.

                This corresponds to the ``size`` field
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
        has_flattened_params = any([project, region, instance_group_manager, size])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, compute.ResizeRegionInstanceGroupManagerRequest):
            request = compute.ResizeRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if size is not None:
                request.size = size

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resize]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def set_instance_template_unary(
        self,
        request: Optional[
            Union[compute.SetInstanceTemplateRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_set_template_request_resource: Optional[
            compute.RegionInstanceGroupManagersSetTemplateRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Sets the instance template to use when creating new
        instances or recreating instances in this group.
        Existing instances are not affected.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_set_instance_template():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.SetInstanceTemplateRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.set_instance_template(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.SetInstanceTemplateRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.SetInstanceTemplate.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_set_template_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersSetTemplateRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_set_template_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_set_template_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.SetInstanceTemplateRegionInstanceGroupManagerRequest
        ):
            request = compute.SetInstanceTemplateRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if region_instance_group_managers_set_template_request_resource is not None:
                request.region_instance_group_managers_set_template_request_resource = (
                    region_instance_group_managers_set_template_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_instance_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def set_instance_template(
        self,
        request: Optional[
            Union[compute.SetInstanceTemplateRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_set_template_request_resource: Optional[
            compute.RegionInstanceGroupManagersSetTemplateRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Sets the instance template to use when creating new
        instances or recreating instances in this group.
        Existing instances are not affected.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_set_instance_template():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.SetInstanceTemplateRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.set_instance_template(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.SetInstanceTemplateRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.SetInstanceTemplate.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_set_template_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersSetTemplateRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_set_template_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_set_template_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.SetInstanceTemplateRegionInstanceGroupManagerRequest
        ):
            request = compute.SetInstanceTemplateRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if region_instance_group_managers_set_template_request_resource is not None:
                request.region_instance_group_managers_set_template_request_resource = (
                    region_instance_group_managers_set_template_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_instance_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def set_target_pools_unary(
        self,
        request: Optional[
            Union[compute.SetTargetPoolsRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_set_target_pools_request_resource: Optional[
            compute.RegionInstanceGroupManagersSetTargetPoolsRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Modifies the target pools to which all new instances
        in this group are assigned. Existing instances in the
        group are not affected.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_set_target_pools():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.SetTargetPoolsRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.set_target_pools(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.SetTargetPoolsRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.SetTargetPools.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_set_target_pools_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersSetTargetPoolsRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_set_target_pools_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_set_target_pools_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.SetTargetPoolsRegionInstanceGroupManagerRequest
        ):
            request = compute.SetTargetPoolsRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_set_target_pools_request_resource
                is not None
            ):
                request.region_instance_group_managers_set_target_pools_request_resource = (
                    region_instance_group_managers_set_target_pools_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_target_pools]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def set_target_pools(
        self,
        request: Optional[
            Union[compute.SetTargetPoolsRegionInstanceGroupManagerRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_managers_set_target_pools_request_resource: Optional[
            compute.RegionInstanceGroupManagersSetTargetPoolsRequest
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Modifies the target pools to which all new instances
        in this group are assigned. Existing instances in the
        group are not affected.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_set_target_pools():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.SetTargetPoolsRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.set_target_pools(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.SetTargetPoolsRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.SetTargetPools.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                Name of the managed instance group.
                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_managers_set_target_pools_request_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagersSetTargetPoolsRequest):
                The body resource for this request
                This corresponds to the ``region_instance_group_managers_set_target_pools_request_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_managers_set_target_pools_request_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.SetTargetPoolsRegionInstanceGroupManagerRequest
        ):
            request = compute.SetTargetPoolsRegionInstanceGroupManagerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_managers_set_target_pools_request_resource
                is not None
            ):
                request.region_instance_group_managers_set_target_pools_request_resource = (
                    region_instance_group_managers_set_target_pools_request_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_target_pools]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def update_per_instance_configs_unary(
        self,
        request: Optional[
            Union[
                compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest, dict
            ]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_manager_update_instance_config_req_resource: Optional[
            compute.RegionInstanceGroupManagerUpdateInstanceConfigReq
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Inserts or updates per-instance configurations for
        the managed instance group. perInstanceConfig.name
        serves as a key used to distinguish whether to perform
        insert or patch.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_update_per_instance_configs():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.update_per_instance_configs(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.UpdatePerInstanceConfigs.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request, should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group. It should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_manager_update_instance_config_req_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagerUpdateInstanceConfigReq):
                The body resource for this request
                This corresponds to the ``region_instance_group_manager_update_instance_config_req_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_manager_update_instance_config_req_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest
        ):
            request = compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_manager_update_instance_config_req_resource
                is not None
            ):
                request.region_instance_group_manager_update_instance_config_req_resource = (
                    region_instance_group_manager_update_instance_config_req_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_per_instance_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

    def update_per_instance_configs(
        self,
        request: Optional[
            Union[
                compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest, dict
            ]
        ] = None,
        *,
        project: Optional[str] = None,
        region: Optional[str] = None,
        instance_group_manager: Optional[str] = None,
        region_instance_group_manager_update_instance_config_req_resource: Optional[
            compute.RegionInstanceGroupManagerUpdateInstanceConfigReq
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> extended_operation.ExtendedOperation:
        r"""Inserts or updates per-instance configurations for
        the managed instance group. perInstanceConfig.name
        serves as a key used to distinguish whether to perform
        insert or patch.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import compute_v1

            def sample_update_per_instance_configs():
                # Create a client
                client = compute_v1.RegionInstanceGroupManagersClient()

                # Initialize request argument(s)
                request = compute_v1.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest(
                    instance_group_manager="instance_group_manager_value",
                    project="project_value",
                    region="region_value",
                )

                # Make the request
                response = client.update_per_instance_configs(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.compute_v1.types.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest, dict]):
                The request object. A request message for
                RegionInstanceGroupManagers.UpdatePerInstanceConfigs.
                See the method description for details.
            project (str):
                Project ID for this request.
                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region (str):
                Name of the region scoping this
                request, should conform to RFC1035.

                This corresponds to the ``region`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_group_manager (str):
                The name of the managed instance
                group. It should conform to RFC1035.

                This corresponds to the ``instance_group_manager`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            region_instance_group_manager_update_instance_config_req_resource (google.cloud.compute_v1.types.RegionInstanceGroupManagerUpdateInstanceConfigReq):
                The body resource for this request
                This corresponds to the ``region_instance_group_manager_update_instance_config_req_resource`` field
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
            [
                project,
                region,
                instance_group_manager,
                region_instance_group_manager_update_instance_config_req_resource,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest
        ):
            request = compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if region is not None:
                request.region = region
            if instance_group_manager is not None:
                request.instance_group_manager = instance_group_manager
            if (
                region_instance_group_manager_update_instance_config_req_resource
                is not None
            ):
                request.region_instance_group_manager_update_instance_config_req_resource = (
                    region_instance_group_manager_update_instance_config_req_resource
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_per_instance_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    ("project", request.project),
                    ("region", request.region),
                    ("instance_group_manager", request.instance_group_manager),
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

        operation_service = self._transport._region_operations_client
        operation_request = compute.GetRegionOperationRequest()
        operation_request.project = request.project
        operation_request.region = request.region
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

    def __enter__(self) -> "RegionInstanceGroupManagersClient":
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


__all__ = ("RegionInstanceGroupManagersClient",)
