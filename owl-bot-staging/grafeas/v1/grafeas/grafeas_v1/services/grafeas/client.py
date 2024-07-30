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
import os
import re
from typing import Dict, Callable, Mapping, MutableMapping, MutableSequence, Optional, Sequence, Tuple, Type, Union, cast
import warnings

from grafeas.grafeas_v1 import gapic_version as package_version

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials             # type: ignore
from google.auth.transport import mtls                            # type: ignore
from google.auth.transport.grpc import SslCredentials             # type: ignore
from google.auth.exceptions import MutualTLSChannelError          # type: ignore
from google.oauth2 import service_account                         # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from grafeas.grafeas_v1.services.grafeas import pagers
from grafeas.grafeas_v1.types import attestation
from grafeas.grafeas_v1.types import build
from grafeas.grafeas_v1.types import common
from grafeas.grafeas_v1.types import compliance
from grafeas.grafeas_v1.types import deployment
from grafeas.grafeas_v1.types import discovery
from grafeas.grafeas_v1.types import dsse_attestation
from grafeas.grafeas_v1.types import grafeas
from grafeas.grafeas_v1.types import image
from grafeas.grafeas_v1.types import package
from grafeas.grafeas_v1.types import sbom
from grafeas.grafeas_v1.types import upgrade
from grafeas.grafeas_v1.types import vex
from grafeas.grafeas_v1.types import vulnerability
from .transports.base import GrafeasTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import GrafeasGrpcTransport
from .transports.grpc_asyncio import GrafeasGrpcAsyncIOTransport
from .transports.rest import GrafeasRestTransport


class GrafeasClientMeta(type):
    """Metaclass for the Grafeas client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """
    _transport_registry = OrderedDict()  # type: Dict[str, Type[GrafeasTransport]]
    _transport_registry["grpc"] = GrafeasGrpcTransport
    _transport_registry["grpc_asyncio"] = GrafeasGrpcAsyncIOTransport
    _transport_registry["rest"] = GrafeasRestTransport

    def get_transport_class(cls,
            label: Optional[str] = None,
        ) -> Type[GrafeasTransport]:
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


class GrafeasClient(metaclass=GrafeasClientMeta):
    """`Grafeas <https://grafeas.io>`__ API.

    Retrieves analysis results of Cloud components such as Docker
    container images.

    Analysis results are stored as a series of occurrences. An
    ``Occurrence`` contains information about a specific analysis
    instance on a resource. An occurrence refers to a ``Note``. A note
    contains details describing the analysis and is generally stored in
    a separate project, called a ``Provider``. Multiple occurrences can
    refer to the same note.

    For example, an SSL vulnerability could affect multiple images. In
    this case, there would be one note for the vulnerability and an
    occurrence for each image with the vulnerability referring to that
    note.
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

    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = "containeranalysis.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "containeranalysis.{UNIVERSE_DOMAIN}"
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
            GrafeasClient: The constructed client.
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
            GrafeasClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> GrafeasTransport:
        """Returns the transport used by the client instance.

        Returns:
            GrafeasTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def note_path(project: str,note: str,) -> str:
        """Returns a fully-qualified note string."""
        return "projects/{project}/notes/{note}".format(project=project, note=note, )

    @staticmethod
    def parse_note_path(path: str) -> Dict[str,str]:
        """Parses a note path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/notes/(?P<note>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def occurrence_path(project: str,occurrence: str,) -> str:
        """Returns a fully-qualified occurrence string."""
        return "projects/{project}/occurrences/{occurrence}".format(project=project, occurrence=occurrence, )

    @staticmethod
    def parse_occurrence_path(path: str) -> Dict[str,str]:
        """Parses a occurrence path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/occurrences/(?P<occurrence>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project, )

    @staticmethod
    def parse_project_path(path: str) -> Dict[str,str]:
        """Parses a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str, ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(billing_account=billing_account, )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str,str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str, ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder, )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str,str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str, ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization, )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str,str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str, ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project, )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str,str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str, ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(project=project, location=location, )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str,str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(cls, client_options: Optional[client_options_lib.ClientOptions] = None):
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

        warnings.warn("get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError("Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`")
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError("Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`")

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
        elif use_mtls_endpoint == "always" or (use_mtls_endpoint == "auto" and client_cert_source):
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
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false").lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError("Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`")
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError("Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`")
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
    def _get_api_endpoint(api_override, client_cert_source, universe_domain, use_mtls_endpoint):
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
        elif use_mtls_endpoint == "always" or (use_mtls_endpoint == "auto" and client_cert_source):
            _default_universe = GrafeasClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(f"mTLS is not supported in any universe other than {_default_universe}.")
            api_endpoint = GrafeasClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = GrafeasClient._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=universe_domain)
        return api_endpoint

    @staticmethod
    def _get_universe_domain(client_universe_domain: Optional[str], universe_domain_env: Optional[str]) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = GrafeasClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    @staticmethod
    def _compare_universes(client_universe: str,
                           credentials: ga_credentials.Credentials) -> bool:
        """Returns True iff the universe domains used by the client and credentials match.

        Args:
            client_universe (str): The universe domain configured via the client options.
            credentials (ga_credentials.Credentials): The credentials being used in the client.

        Returns:
            bool: True iff client_universe matches the universe in credentials.

        Raises:
            ValueError: when client_universe does not match the universe in credentials.
        """

        default_universe = GrafeasClient._DEFAULT_UNIVERSE
        credentials_universe = getattr(credentials, "universe_domain", default_universe)

        if client_universe != credentials_universe:
            raise ValueError("The configured universe domain "
                f"({client_universe}) does not match the universe domain "
                f"found in the credentials ({credentials_universe}). "
                "If you haven't configured the universe domain explicitly, "
                f"`{default_universe}` is the default.")
        return True

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """
        self._is_universe_domain_valid = (self._is_universe_domain_valid or
            GrafeasClient._compare_universes(self.universe_domain, self.transport._credentials))
        return self._is_universe_domain_valid

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

    def __init__(self, *,
            credentials: Optional[ga_credentials.Credentials] = None,
            transport: Optional[Union[str, GrafeasTransport, Callable[..., GrafeasTransport]]] = None,
            client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the grafeas client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,GrafeasTransport,Callable[..., GrafeasTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the GrafeasTransport constructor.
                If set to None, a transport is chosen automatically.
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
        self._client_options = cast(client_options_lib.ClientOptions, self._client_options)

        universe_domain_opt = getattr(self._client_options, 'universe_domain', None)

        self._use_client_cert, self._use_mtls_endpoint, self._universe_domain_env = GrafeasClient._read_environment_variables()
        self._client_cert_source = GrafeasClient._get_client_cert_source(self._client_options.client_cert_source, self._use_client_cert)
        self._universe_domain = GrafeasClient._get_universe_domain(universe_domain_opt, self._universe_domain_env)
        self._api_endpoint = None # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError("client_options.api_key and credentials are mutually exclusive")

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, GrafeasTransport)
        if transport_provided:
            # transport is a GrafeasTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError("When providing a transport instance, "
                                 "provide its credentials directly.")
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(GrafeasTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (self._api_endpoint or
            GrafeasClient._get_api_endpoint(
                self._client_options.api_endpoint,
                self._client_cert_source,
                self._universe_domain,
                self._use_mtls_endpoint))

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(google.auth._default, "get_api_key_credentials"):
                credentials = google.auth._default.get_api_key_credentials(api_key_value)

            transport_init: Union[Type[GrafeasTransport], Callable[..., GrafeasTransport]] = (
                type(self).get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., GrafeasTransport], transport)
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

    def get_occurrence(self,
            request: Optional[Union[grafeas.GetOccurrenceRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> grafeas.Occurrence:
        r"""Gets the specified occurrence.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_get_occurrence():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.GetOccurrenceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_occurrence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.GetOccurrenceRequest, dict]):
                The request object. Request to get an occurrence.
            name (str):
                The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Occurrence:
                An instance of an analysis type that
                has been found on a resource.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.GetOccurrenceRequest):
            request = grafeas.GetOccurrenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_occurrence]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    def list_occurrences(self,
            request: Optional[Union[grafeas.ListOccurrencesRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            filter: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListOccurrencesPager:
        r"""Lists occurrences for the specified project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_list_occurrences():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.ListOccurrencesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_occurrences(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.ListOccurrencesRequest, dict]):
                The request object. Request to list occurrences.
            parent (str):
                The name of the project to list occurrences for in the
                form of ``projects/[PROJECT_ID]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                The filter expression.
                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.services.grafeas.pagers.ListOccurrencesPager:
                Response for listing occurrences.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.ListOccurrencesRequest):
            request = grafeas.ListOccurrencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_occurrences]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
        response = pagers.ListOccurrencesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_occurrence(self,
            request: Optional[Union[grafeas.DeleteOccurrenceRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Deletes the specified occurrence. For example, use
        this method to delete an occurrence when the occurrence
        is no longer applicable for the given resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_delete_occurrence():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.DeleteOccurrenceRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_occurrence(request=request)

        Args:
            request (Union[grafeas.grafeas_v1.types.DeleteOccurrenceRequest, dict]):
                The request object. Request to delete an occurrence.
            name (str):
                The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.DeleteOccurrenceRequest):
            request = grafeas.DeleteOccurrenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_occurrence]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_occurrence(self,
            request: Optional[Union[grafeas.CreateOccurrenceRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            occurrence: Optional[grafeas.Occurrence] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> grafeas.Occurrence:
        r"""Creates a new occurrence.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_create_occurrence():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.CreateOccurrenceRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_occurrence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.CreateOccurrenceRequest, dict]):
                The request object. Request to create a new occurrence.
            parent (str):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the occurrence is
                to be created.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            occurrence (grafeas.grafeas_v1.types.Occurrence):
                The occurrence to create.
                This corresponds to the ``occurrence`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Occurrence:
                An instance of an analysis type that
                has been found on a resource.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, occurrence])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.CreateOccurrenceRequest):
            request = grafeas.CreateOccurrenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if occurrence is not None:
                request.occurrence = occurrence

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_occurrence]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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

    def batch_create_occurrences(self,
            request: Optional[Union[grafeas.BatchCreateOccurrencesRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            occurrences: Optional[MutableSequence[grafeas.Occurrence]] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> grafeas.BatchCreateOccurrencesResponse:
        r"""Creates new occurrences in batch.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_batch_create_occurrences():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.BatchCreateOccurrencesRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.batch_create_occurrences(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.BatchCreateOccurrencesRequest, dict]):
                The request object. Request to create occurrences in
                batch.
            parent (str):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the occurrences
                are to be created.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            occurrences (MutableSequence[grafeas.grafeas_v1.types.Occurrence]):
                The occurrences to create. Max
                allowed length is 1000.

                This corresponds to the ``occurrences`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.BatchCreateOccurrencesResponse:
                Response for creating occurrences in
                batch.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, occurrences])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.BatchCreateOccurrencesRequest):
            request = grafeas.BatchCreateOccurrencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if occurrences is not None:
                request.occurrences = occurrences

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_create_occurrences]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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

    def update_occurrence(self,
            request: Optional[Union[grafeas.UpdateOccurrenceRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            occurrence: Optional[grafeas.Occurrence] = None,
            update_mask: Optional[field_mask_pb2.FieldMask] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> grafeas.Occurrence:
        r"""Updates the specified occurrence.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_update_occurrence():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.UpdateOccurrenceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.update_occurrence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.UpdateOccurrenceRequest, dict]):
                The request object. Request to update an occurrence.
            name (str):
                The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            occurrence (grafeas.grafeas_v1.types.Occurrence):
                The updated occurrence.
                This corresponds to the ``occurrence`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Occurrence:
                An instance of an analysis type that
                has been found on a resource.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, occurrence, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.UpdateOccurrenceRequest):
            request = grafeas.UpdateOccurrenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if occurrence is not None:
                request.occurrence = occurrence
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_occurrence]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    def get_occurrence_note(self,
            request: Optional[Union[grafeas.GetOccurrenceNoteRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> grafeas.Note:
        r"""Gets the note attached to the specified occurrence.
        Consumer projects can use this method to get a note that
        belongs to a provider project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_get_occurrence_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.GetOccurrenceNoteRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_occurrence_note(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.GetOccurrenceNoteRequest, dict]):
                The request object. Request to get the note to which the
                specified occurrence is attached.
            name (str):
                The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Note:
                A type of analysis that can be done
                for a resource.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.GetOccurrenceNoteRequest):
            request = grafeas.GetOccurrenceNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_occurrence_note]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    def get_note(self,
            request: Optional[Union[grafeas.GetNoteRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> grafeas.Note:
        r"""Gets the specified note.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_get_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.GetNoteRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_note(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.GetNoteRequest, dict]):
                The request object. Request to get a note.
            name (str):
                The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Note:
                A type of analysis that can be done
                for a resource.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.GetNoteRequest):
            request = grafeas.GetNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_note]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    def list_notes(self,
            request: Optional[Union[grafeas.ListNotesRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            filter: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListNotesPager:
        r"""Lists notes for the specified project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_list_notes():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.ListNotesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_notes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.ListNotesRequest, dict]):
                The request object. Request to list notes.
            parent (str):
                The name of the project to list notes for in the form of
                ``projects/[PROJECT_ID]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                The filter expression.
                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.services.grafeas.pagers.ListNotesPager:
                Response for listing notes.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.ListNotesRequest):
            request = grafeas.ListNotesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_notes]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
        response = pagers.ListNotesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_note(self,
            request: Optional[Union[grafeas.DeleteNoteRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Deletes the specified note.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_delete_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.DeleteNoteRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_note(request=request)

        Args:
            request (Union[grafeas.grafeas_v1.types.DeleteNoteRequest, dict]):
                The request object. Request to delete a note.
            name (str):
                The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.DeleteNoteRequest):
            request = grafeas.DeleteNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_note]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_note(self,
            request: Optional[Union[grafeas.CreateNoteRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            note_id: Optional[str] = None,
            note: Optional[grafeas.Note] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> grafeas.Note:
        r"""Creates a new note.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_create_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.CreateNoteRequest(
                    parent="parent_value",
                    note_id="note_id_value",
                )

                # Make the request
                response = client.create_note(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.CreateNoteRequest, dict]):
                The request object. Request to create a new note.
            parent (str):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the note is to be
                created.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            note_id (str):
                The ID to use for this note.
                This corresponds to the ``note_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            note (grafeas.grafeas_v1.types.Note):
                The note to create.
                This corresponds to the ``note`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Note:
                A type of analysis that can be done
                for a resource.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, note_id, note])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.CreateNoteRequest):
            request = grafeas.CreateNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if note_id is not None:
                request.note_id = note_id
            if note is not None:
                request.note = note

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_note]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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

    def batch_create_notes(self,
            request: Optional[Union[grafeas.BatchCreateNotesRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            notes: Optional[MutableMapping[str, grafeas.Note]] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> grafeas.BatchCreateNotesResponse:
        r"""Creates new notes in batch.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_batch_create_notes():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.BatchCreateNotesRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.batch_create_notes(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.BatchCreateNotesRequest, dict]):
                The request object. Request to create notes in batch.
            parent (str):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the notes are to
                be created.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            notes (MutableMapping[str, grafeas.grafeas_v1.types.Note]):
                The notes to create. Max allowed
                length is 1000.

                This corresponds to the ``notes`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.BatchCreateNotesResponse:
                Response for creating notes in batch.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, notes])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.BatchCreateNotesRequest):
            request = grafeas.BatchCreateNotesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if notes is not None:
                request.notes = notes

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_create_notes]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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

    def update_note(self,
            request: Optional[Union[grafeas.UpdateNoteRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            note: Optional[grafeas.Note] = None,
            update_mask: Optional[field_mask_pb2.FieldMask] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> grafeas.Note:
        r"""Updates the specified note.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_update_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.UpdateNoteRequest(
                    name="name_value",
                )

                # Make the request
                response = client.update_note(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.UpdateNoteRequest, dict]):
                The request object. Request to update a note.
            name (str):
                The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            note (grafeas.grafeas_v1.types.Note):
                The updated note.
                This corresponds to the ``note`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Note:
                A type of analysis that can be done
                for a resource.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, note, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.UpdateNoteRequest):
            request = grafeas.UpdateNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if note is not None:
                request.note = note
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_note]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    def list_note_occurrences(self,
            request: Optional[Union[grafeas.ListNoteOccurrencesRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            filter: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListNoteOccurrencesPager:
        r"""Lists occurrences referencing the specified note.
        Provider projects can use this method to get all
        occurrences across consumer projects referencing the
        specified note.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from grafeas import grafeas_v1

            def sample_list_note_occurrences():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.ListNoteOccurrencesRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.list_note_occurrences(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.ListNoteOccurrencesRequest, dict]):
                The request object. Request to list occurrences for a
                note.
            name (str):
                The name of the note to list occurrences for in the form
                of ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                The filter expression.
                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.services.grafeas.pagers.ListNoteOccurrencesPager:
                Response for listing occurrences for
                a note.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, filter])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, grafeas.ListNoteOccurrencesRequest):
            request = grafeas.ListNoteOccurrencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_note_occurrences]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
        response = pagers.ListNoteOccurrencesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "GrafeasClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()







DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


__all__ = (
    "GrafeasClient",
)
