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
from typing import (
    Callable,
    Dict,
    Iterable,
    Iterator,
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
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.speech_v2 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.speech_v2.services.speech import pagers
from google.cloud.speech_v2.types import cloud_speech

from .transports.base import DEFAULT_CLIENT_INFO, SpeechTransport
from .transports.grpc import SpeechGrpcTransport
from .transports.grpc_asyncio import SpeechGrpcAsyncIOTransport
from .transports.rest import SpeechRestTransport


class SpeechClientMeta(type):
    """Metaclass for the Speech client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[SpeechTransport]]
    _transport_registry["grpc"] = SpeechGrpcTransport
    _transport_registry["grpc_asyncio"] = SpeechGrpcAsyncIOTransport
    _transport_registry["rest"] = SpeechRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[SpeechTransport]:
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


class SpeechClient(metaclass=SpeechClientMeta):
    """Enables speech transcription and resource management."""

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
    DEFAULT_ENDPOINT = "speech.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "speech.{UNIVERSE_DOMAIN}"
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
            SpeechClient: The constructed client.
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
            SpeechClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SpeechTransport:
        """Returns the transport used by the client instance.

        Returns:
            SpeechTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def config_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified config string."""
        return "projects/{project}/locations/{location}/config".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_config_path(path: str) -> Dict[str, str]:
        """Parses a config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/config$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def crypto_key_path(
        project: str,
        location: str,
        key_ring: str,
        crypto_key: str,
    ) -> str:
        """Returns a fully-qualified crypto_key string."""
        return "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
        )

    @staticmethod
    def parse_crypto_key_path(path: str) -> Dict[str, str]:
        """Parses a crypto_key path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/keyRings/(?P<key_ring>.+?)/cryptoKeys/(?P<crypto_key>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def crypto_key_version_path(
        project: str,
        location: str,
        key_ring: str,
        crypto_key: str,
        crypto_key_version: str,
    ) -> str:
        """Returns a fully-qualified crypto_key_version string."""
        return "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}".format(
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
            crypto_key_version=crypto_key_version,
        )

    @staticmethod
    def parse_crypto_key_version_path(path: str) -> Dict[str, str]:
        """Parses a crypto_key_version path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/keyRings/(?P<key_ring>.+?)/cryptoKeys/(?P<crypto_key>.+?)/cryptoKeyVersions/(?P<crypto_key_version>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def custom_class_path(
        project: str,
        location: str,
        custom_class: str,
    ) -> str:
        """Returns a fully-qualified custom_class string."""
        return "projects/{project}/locations/{location}/customClasses/{custom_class}".format(
            project=project,
            location=location,
            custom_class=custom_class,
        )

    @staticmethod
    def parse_custom_class_path(path: str) -> Dict[str, str]:
        """Parses a custom_class path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/customClasses/(?P<custom_class>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def phrase_set_path(
        project: str,
        location: str,
        phrase_set: str,
    ) -> str:
        """Returns a fully-qualified phrase_set string."""
        return "projects/{project}/locations/{location}/phraseSets/{phrase_set}".format(
            project=project,
            location=location,
            phrase_set=phrase_set,
        )

    @staticmethod
    def parse_phrase_set_path(path: str) -> Dict[str, str]:
        """Parses a phrase_set path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/phraseSets/(?P<phrase_set>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def recognizer_path(
        project: str,
        location: str,
        recognizer: str,
    ) -> str:
        """Returns a fully-qualified recognizer string."""
        return (
            "projects/{project}/locations/{location}/recognizers/{recognizer}".format(
                project=project,
                location=location,
                recognizer=recognizer,
            )
        )

    @staticmethod
    def parse_recognizer_path(path: str) -> Dict[str, str]:
        """Parses a recognizer path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/recognizers/(?P<recognizer>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

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
            _default_universe = SpeechClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = SpeechClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = SpeechClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = SpeechClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    @staticmethod
    def _compare_universes(
        client_universe: str, credentials: ga_credentials.Credentials
    ) -> bool:
        """Returns True iff the universe domains used by the client and credentials match.

        Args:
            client_universe (str): The universe domain configured via the client options.
            credentials (ga_credentials.Credentials): The credentials being used in the client.

        Returns:
            bool: True iff client_universe matches the universe in credentials.

        Raises:
            ValueError: when client_universe does not match the universe in credentials.
        """

        default_universe = SpeechClient._DEFAULT_UNIVERSE
        credentials_universe = getattr(credentials, "universe_domain", default_universe)

        if client_universe != credentials_universe:
            raise ValueError(
                "The configured universe domain "
                f"({client_universe}) does not match the universe domain "
                f"found in the credentials ({credentials_universe}). "
                "If you haven't configured the universe domain explicitly, "
                f"`{default_universe}` is the default."
            )
        return True

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """
        self._is_universe_domain_valid = (
            self._is_universe_domain_valid
            or SpeechClient._compare_universes(
                self.universe_domain, self.transport._credentials
            )
        )
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

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[str, SpeechTransport, Callable[..., SpeechTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the speech client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,SpeechTransport,Callable[..., SpeechTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the SpeechTransport constructor.
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
        self._client_options = cast(
            client_options_lib.ClientOptions, self._client_options
        )

        universe_domain_opt = getattr(self._client_options, "universe_domain", None)

        (
            self._use_client_cert,
            self._use_mtls_endpoint,
            self._universe_domain_env,
        ) = SpeechClient._read_environment_variables()
        self._client_cert_source = SpeechClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = SpeechClient._get_universe_domain(
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
        transport_provided = isinstance(transport, SpeechTransport)
        if transport_provided:
            # transport is a SpeechTransport instance.
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
            self._transport = cast(SpeechTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = self._api_endpoint or SpeechClient._get_api_endpoint(
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
                Type[SpeechTransport], Callable[..., SpeechTransport]
            ] = (
                SpeechClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., SpeechTransport], transport)
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

    def create_recognizer(
        self,
        request: Optional[Union[cloud_speech.CreateRecognizerRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        recognizer: Optional[cloud_speech.Recognizer] = None,
        recognizer_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a [Recognizer][google.cloud.speech.v2.Recognizer].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_create_recognizer():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.CreateRecognizerRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_recognizer(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.CreateRecognizerRequest, dict]):
                The request object. Request message for the
                [CreateRecognizer][google.cloud.speech.v2.Speech.CreateRecognizer]
                method.
            parent (str):
                Required. The project and location where this Recognizer
                will be created. The expected format is
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            recognizer (google.cloud.speech_v2.types.Recognizer):
                Required. The Recognizer to create.
                This corresponds to the ``recognizer`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            recognizer_id (str):
                The ID to use for the Recognizer, which will become the
                final component of the Recognizer's resource name.

                This value should be 4-63 characters, and valid
                characters are /[a-z][0-9]-/.

                This corresponds to the ``recognizer_id`` field
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
                :class:`google.cloud.speech_v2.types.Recognizer` A
                Recognizer message. Stores recognition configuration and
                metadata.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, recognizer, recognizer_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.CreateRecognizerRequest):
            request = cloud_speech.CreateRecognizerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if recognizer is not None:
                request.recognizer = recognizer
            if recognizer_id is not None:
                request.recognizer_id = recognizer_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_recognizer]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.Recognizer,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_recognizers(
        self,
        request: Optional[Union[cloud_speech.ListRecognizersRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRecognizersPager:
        r"""Lists Recognizers.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_list_recognizers():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.ListRecognizersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_recognizers(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.ListRecognizersRequest, dict]):
                The request object. Request message for the
                [ListRecognizers][google.cloud.speech.v2.Speech.ListRecognizers]
                method.
            parent (str):
                Required. The project and location of Recognizers to
                list. The expected format is
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v2.services.speech.pagers.ListRecognizersPager:
                Response message for the
                   [ListRecognizers][google.cloud.speech.v2.Speech.ListRecognizers]
                   method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.ListRecognizersRequest):
            request = cloud_speech.ListRecognizersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_recognizers]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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
        response = pagers.ListRecognizersPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_recognizer(
        self,
        request: Optional[Union[cloud_speech.GetRecognizerRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_speech.Recognizer:
        r"""Returns the requested
        [Recognizer][google.cloud.speech.v2.Recognizer]. Fails with
        [NOT_FOUND][google.rpc.Code.NOT_FOUND] if the requested
        Recognizer doesn't exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_get_recognizer():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.GetRecognizerRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_recognizer(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.GetRecognizerRequest, dict]):
                The request object. Request message for the
                [GetRecognizer][google.cloud.speech.v2.Speech.GetRecognizer]
                method.
            name (str):
                Required. The name of the Recognizer to retrieve. The
                expected format is
                ``projects/{project}/locations/{location}/recognizers/{recognizer}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v2.types.Recognizer:
                A Recognizer message. Stores
                recognition configuration and metadata.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.GetRecognizerRequest):
            request = cloud_speech.GetRecognizerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_recognizer]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def update_recognizer(
        self,
        request: Optional[Union[cloud_speech.UpdateRecognizerRequest, dict]] = None,
        *,
        recognizer: Optional[cloud_speech.Recognizer] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the [Recognizer][google.cloud.speech.v2.Recognizer].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_update_recognizer():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.UpdateRecognizerRequest(
                )

                # Make the request
                operation = client.update_recognizer(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.UpdateRecognizerRequest, dict]):
                The request object. Request message for the
                [UpdateRecognizer][google.cloud.speech.v2.Speech.UpdateRecognizer]
                method.
            recognizer (google.cloud.speech_v2.types.Recognizer):
                Required. The Recognizer to update.

                The Recognizer's ``name`` field is used to identify the
                Recognizer to update. Format:
                ``projects/{project}/locations/{location}/recognizers/{recognizer}``.

                This corresponds to the ``recognizer`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to update. If empty, all non-default
                valued fields are considered for update. Use ``*`` to
                update the entire Recognizer resource.

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
                :class:`google.cloud.speech_v2.types.Recognizer` A
                Recognizer message. Stores recognition configuration and
                metadata.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([recognizer, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.UpdateRecognizerRequest):
            request = cloud_speech.UpdateRecognizerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if recognizer is not None:
                request.recognizer = recognizer
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_recognizer]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("recognizer.name", request.recognizer.name),)
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.Recognizer,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_recognizer(
        self,
        request: Optional[Union[cloud_speech.DeleteRecognizerRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes the [Recognizer][google.cloud.speech.v2.Recognizer].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_delete_recognizer():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.DeleteRecognizerRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_recognizer(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.DeleteRecognizerRequest, dict]):
                The request object. Request message for the
                [DeleteRecognizer][google.cloud.speech.v2.Speech.DeleteRecognizer]
                method.
            name (str):
                Required. The name of the Recognizer to delete. Format:
                ``projects/{project}/locations/{location}/recognizers/{recognizer}``

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
                :class:`google.cloud.speech_v2.types.Recognizer` A
                Recognizer message. Stores recognition configuration and
                metadata.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.DeleteRecognizerRequest):
            request = cloud_speech.DeleteRecognizerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_recognizer]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.Recognizer,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def undelete_recognizer(
        self,
        request: Optional[Union[cloud_speech.UndeleteRecognizerRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Undeletes the [Recognizer][google.cloud.speech.v2.Recognizer].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_undelete_recognizer():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.UndeleteRecognizerRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undelete_recognizer(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.UndeleteRecognizerRequest, dict]):
                The request object. Request message for the
                [UndeleteRecognizer][google.cloud.speech.v2.Speech.UndeleteRecognizer]
                method.
            name (str):
                Required. The name of the Recognizer to undelete.
                Format:
                ``projects/{project}/locations/{location}/recognizers/{recognizer}``

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
                :class:`google.cloud.speech_v2.types.Recognizer` A
                Recognizer message. Stores recognition configuration and
                metadata.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.UndeleteRecognizerRequest):
            request = cloud_speech.UndeleteRecognizerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.undelete_recognizer]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.Recognizer,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def recognize(
        self,
        request: Optional[Union[cloud_speech.RecognizeRequest, dict]] = None,
        *,
        recognizer: Optional[str] = None,
        config: Optional[cloud_speech.RecognitionConfig] = None,
        config_mask: Optional[field_mask_pb2.FieldMask] = None,
        content: Optional[bytes] = None,
        uri: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_speech.RecognizeResponse:
        r"""Performs synchronous Speech recognition: receive
        results after all audio has been sent and processed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_recognize():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.RecognizeRequest(
                    content=b'content_blob',
                    recognizer="recognizer_value",
                )

                # Make the request
                response = client.recognize(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.RecognizeRequest, dict]):
                The request object. Request message for the
                [Recognize][google.cloud.speech.v2.Speech.Recognize]
                method. Either ``content`` or ``uri`` must be supplied.
                Supplying both or neither returns
                [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].
                See `content
                limits <https://cloud.google.com/speech-to-text/quotas#content>`__.
            recognizer (str):
                Required. The name of the Recognizer to use during
                recognition. The expected format is
                ``projects/{project}/locations/{location}/recognizers/{recognizer}``.
                The {recognizer} segment may be set to ``_`` to use an
                empty implicit Recognizer.

                This corresponds to the ``recognizer`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config (google.cloud.speech_v2.types.RecognitionConfig):
                Features and audio metadata to use for the Automatic
                Speech Recognition. This field in combination with the
                [config_mask][google.cloud.speech.v2.RecognizeRequest.config_mask]
                field can be used to override parts of the
                [default_recognition_config][google.cloud.speech.v2.Recognizer.default_recognition_config]
                of the Recognizer resource.

                This corresponds to the ``config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields in
                [config][google.cloud.speech.v2.RecognizeRequest.config]
                that override the values in the
                [default_recognition_config][google.cloud.speech.v2.Recognizer.default_recognition_config]
                of the recognizer during this recognition request. If no
                mask is provided, all non-default valued fields in
                [config][google.cloud.speech.v2.RecognizeRequest.config]
                override the values in the recognizer for this
                recognition request. If a mask is provided, only the
                fields listed in the mask override the config in the
                recognizer for this recognition request. If a wildcard
                (``*``) is provided,
                [config][google.cloud.speech.v2.RecognizeRequest.config]
                completely overrides and replaces the config in the
                recognizer for this recognition request.

                This corresponds to the ``config_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            content (bytes):
                The audio data bytes encoded as specified in
                [RecognitionConfig][google.cloud.speech.v2.RecognitionConfig].
                As with all bytes fields, proto buffers use a pure
                binary representation, whereas JSON representations use
                base64.

                This corresponds to the ``content`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            uri (str):
                URI that points to a file that contains audio data bytes
                as specified in
                [RecognitionConfig][google.cloud.speech.v2.RecognitionConfig].
                The file must not be compressed (for example, gzip).
                Currently, only Google Cloud Storage URIs are supported,
                which must be specified in the following format:
                ``gs://bucket_name/object_name`` (other URI formats
                return
                [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT]).
                For more information, see `Request
                URIs <https://cloud.google.com/storage/docs/reference-uris>`__.

                This corresponds to the ``uri`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v2.types.RecognizeResponse:
                Response message for the
                   [Recognize][google.cloud.speech.v2.Speech.Recognize]
                   method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([recognizer, config, config_mask, content, uri])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.RecognizeRequest):
            request = cloud_speech.RecognizeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if recognizer is not None:
                request.recognizer = recognizer
            if config is not None:
                request.config = config
            if config_mask is not None:
                request.config_mask = config_mask
            if content is not None:
                request.content = content
            if uri is not None:
                request.uri = uri

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.recognize]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("recognizer", request.recognizer),)
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

    def streaming_recognize(
        self,
        requests: Optional[Iterator[cloud_speech.StreamingRecognizeRequest]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[cloud_speech.StreamingRecognizeResponse]:
        r"""Performs bidirectional streaming speech recognition:
        receive results while sending audio. This method is only
        available via the gRPC API (not REST).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_streaming_recognize():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.StreamingRecognizeRequest(
                    recognizer="recognizer_value",
                )

                # This method expects an iterator which contains
                # 'speech_v2.StreamingRecognizeRequest' objects
                # Here we create a generator that yields a single `request` for
                # demonstrative purposes.
                requests = [request]

                def request_generator():
                    for request in requests:
                        yield request

                # Make the request
                stream = client.streaming_recognize(requests=request_generator())

                # Handle the response
                for response in stream:
                    print(response)

        Args:
            requests (Iterator[google.cloud.speech_v2.types.StreamingRecognizeRequest]):
                The request object iterator. Request message for the
                [StreamingRecognize][google.cloud.speech.v2.Speech.StreamingRecognize]
                method. Multiple
                [StreamingRecognizeRequest][google.cloud.speech.v2.StreamingRecognizeRequest]
                messages are sent in one call.

                If the [Recognizer][google.cloud.speech.v2.Recognizer]
                referenced by
                [recognizer][google.cloud.speech.v2.StreamingRecognizeRequest.recognizer]
                contains a fully specified request configuration then
                the stream may only contain messages with only
                [audio][google.cloud.speech.v2.StreamingRecognizeRequest.audio]
                set.

                Otherwise the first message must contain a
                [recognizer][google.cloud.speech.v2.StreamingRecognizeRequest.recognizer]
                and a
                [streaming_config][google.cloud.speech.v2.StreamingRecognizeRequest.streaming_config]
                message that together fully specify the request
                configuration and must not contain
                [audio][google.cloud.speech.v2.StreamingRecognizeRequest.audio].
                All subsequent messages must only have
                [audio][google.cloud.speech.v2.StreamingRecognizeRequest.audio]
                set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.cloud.speech_v2.types.StreamingRecognizeResponse]:
                StreamingRecognizeResponse is the only message returned to the client by
                   StreamingRecognize. A series of zero or more
                   StreamingRecognizeResponse messages are streamed back
                   to the client. If there is no recognizable audio then
                   no messages are streamed back to the client.

                   Here are some examples of StreamingRecognizeResponses
                   that might be returned while processing audio:

                   1. results { alternatives { transcript: "tube" }
                      stability: 0.01 }
                   2. results { alternatives { transcript: "to be a" }
                      stability: 0.01 }
                   3. results { alternatives { transcript: "to be" }
                      stability: 0.9 } results { alternatives {
                      transcript: " or not to be" } stability: 0.01 }
                   4.

                      results { alternatives { transcript: "to be or not to be"
                         confidence: 0.92 }

                      alternatives { transcript: "to bee or not to bee" }
                         is_final: true }

                   5. results { alternatives { transcript: " that's" }
                      stability: 0.01 }
                   6. results { alternatives { transcript: " that is" }
                      stability: 0.9 } results { alternatives {
                      transcript: " the question" } stability: 0.01 }
                   7.

                      results { alternatives { transcript: " that is the question"
                         confidence: 0.98 }

                      alternatives { transcript: " that was the question" }
                         is_final: true }

                   Notes:

                   -  Only two of the above responses #4 and #7 contain
                      final results; they are indicated by
                      is_final: true. Concatenating these together
                      generates the full transcript: "to be or not to be
                      that is the question".
                   -  The others contain interim results. #3 and #6
                      contain two interim \`results`: the first portion
                      has a high stability and is less likely to change;
                      the second portion has a low stability and is very
                      likely to change. A UI designer might choose to
                      show only high stability results.
                   -  The specific stability and confidence values shown
                      above are only for illustrative purposes. Actual
                      values may vary.
                   -

                      In each response, only one of these fields will be set:
                         error, speech_event_type, or one or more
                         (repeated) results.

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.streaming_recognize]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            requests,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def batch_recognize(
        self,
        request: Optional[Union[cloud_speech.BatchRecognizeRequest, dict]] = None,
        *,
        recognizer: Optional[str] = None,
        config: Optional[cloud_speech.RecognitionConfig] = None,
        config_mask: Optional[field_mask_pb2.FieldMask] = None,
        files: Optional[
            MutableSequence[cloud_speech.BatchRecognizeFileMetadata]
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Performs batch asynchronous speech recognition: send
        a request with N audio files and receive a long running
        operation that can be polled to see when the
        transcriptions are finished.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_batch_recognize():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.BatchRecognizeRequest(
                    recognizer="recognizer_value",
                )

                # Make the request
                operation = client.batch_recognize(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.BatchRecognizeRequest, dict]):
                The request object. Request message for the
                [BatchRecognize][google.cloud.speech.v2.Speech.BatchRecognize]
                method.
            recognizer (str):
                Required. The name of the Recognizer to use during
                recognition. The expected format is
                ``projects/{project}/locations/{location}/recognizers/{recognizer}``.
                The {recognizer} segment may be set to ``_`` to use an
                empty implicit Recognizer.

                This corresponds to the ``recognizer`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config (google.cloud.speech_v2.types.RecognitionConfig):
                Features and audio metadata to use for the Automatic
                Speech Recognition. This field in combination with the
                [config_mask][google.cloud.speech.v2.BatchRecognizeRequest.config_mask]
                field can be used to override parts of the
                [default_recognition_config][google.cloud.speech.v2.Recognizer.default_recognition_config]
                of the Recognizer resource.

                This corresponds to the ``config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields in
                [config][google.cloud.speech.v2.BatchRecognizeRequest.config]
                that override the values in the
                [default_recognition_config][google.cloud.speech.v2.Recognizer.default_recognition_config]
                of the recognizer during this recognition request. If no
                mask is provided, all given fields in
                [config][google.cloud.speech.v2.BatchRecognizeRequest.config]
                override the values in the recognizer for this
                recognition request. If a mask is provided, only the
                fields listed in the mask override the config in the
                recognizer for this recognition request. If a wildcard
                (``*``) is provided,
                [config][google.cloud.speech.v2.BatchRecognizeRequest.config]
                completely overrides and replaces the config in the
                recognizer for this recognition request.

                This corresponds to the ``config_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            files (MutableSequence[google.cloud.speech_v2.types.BatchRecognizeFileMetadata]):
                Audio files with file metadata for
                ASR. The maximum number of files allowed
                to be specified is 15.

                This corresponds to the ``files`` field
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

                The result type for the operation will be :class:`google.cloud.speech_v2.types.BatchRecognizeResponse` Response message for
                   [BatchRecognize][google.cloud.speech.v2.Speech.BatchRecognize]
                   that is packaged into a longrunning
                   [Operation][google.longrunning.Operation].

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([recognizer, config, config_mask, files])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.BatchRecognizeRequest):
            request = cloud_speech.BatchRecognizeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if recognizer is not None:
                request.recognizer = recognizer
            if config is not None:
                request.config = config
            if config_mask is not None:
                request.config_mask = config_mask
            if files is not None:
                request.files = files

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_recognize]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("recognizer", request.recognizer),)
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.BatchRecognizeResponse,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_config(
        self,
        request: Optional[Union[cloud_speech.GetConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_speech.Config:
        r"""Returns the requested [Config][google.cloud.speech.v2.Config].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_get_config():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.GetConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.GetConfigRequest, dict]):
                The request object. Request message for the
                [GetConfig][google.cloud.speech.v2.Speech.GetConfig]
                method.
            name (str):
                Required. The name of the config to retrieve. There is
                exactly one config resource per project per location.
                The expected format is
                ``projects/{project}/locations/{location}/config``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v2.types.Config:
                Message representing the config for the Speech-to-Text API. This includes an
                   optional [KMS
                   key](\ https://cloud.google.com/kms/docs/resource-hierarchy#keys)
                   with which incoming data will be encrypted.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.GetConfigRequest):
            request = cloud_speech.GetConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def update_config(
        self,
        request: Optional[Union[cloud_speech.UpdateConfigRequest, dict]] = None,
        *,
        config: Optional[cloud_speech.Config] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_speech.Config:
        r"""Updates the [Config][google.cloud.speech.v2.Config].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_update_config():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.UpdateConfigRequest(
                )

                # Make the request
                response = client.update_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.UpdateConfigRequest, dict]):
                The request object. Request message for the
                [UpdateConfig][google.cloud.speech.v2.Speech.UpdateConfig]
                method.
            config (google.cloud.speech_v2.types.Config):
                Required. The config to update.

                The config's ``name`` field is used to identify the
                config to be updated. The expected format is
                ``projects/{project}/locations/{location}/config``.

                This corresponds to the ``config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v2.types.Config:
                Message representing the config for the Speech-to-Text API. This includes an
                   optional [KMS
                   key](\ https://cloud.google.com/kms/docs/resource-hierarchy#keys)
                   with which incoming data will be encrypted.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.UpdateConfigRequest):
            request = cloud_speech.UpdateConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if config is not None:
                request.config = config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("config.name", request.config.name),)
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

    def create_custom_class(
        self,
        request: Optional[Union[cloud_speech.CreateCustomClassRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        custom_class: Optional[cloud_speech.CustomClass] = None,
        custom_class_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a [CustomClass][google.cloud.speech.v2.CustomClass].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_create_custom_class():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.CreateCustomClassRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_custom_class(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.CreateCustomClassRequest, dict]):
                The request object. Request message for the
                [CreateCustomClass][google.cloud.speech.v2.Speech.CreateCustomClass]
                method.
            parent (str):
                Required. The project and location where this
                CustomClass will be created. The expected format is
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_class (google.cloud.speech_v2.types.CustomClass):
                Required. The CustomClass to create.
                This corresponds to the ``custom_class`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_class_id (str):
                The ID to use for the CustomClass, which will become the
                final component of the CustomClass's resource name.

                This value should be 4-63 characters, and valid
                characters are /[a-z][0-9]-/.

                This corresponds to the ``custom_class_id`` field
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

                The result type for the operation will be :class:`google.cloud.speech_v2.types.CustomClass` CustomClass for biasing in speech recognition. Used to define a set of words
                   or phrases that represents a common concept or theme
                   likely to appear in your audio, for example a list of
                   passenger ship names.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, custom_class, custom_class_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.CreateCustomClassRequest):
            request = cloud_speech.CreateCustomClassRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if custom_class is not None:
                request.custom_class = custom_class
            if custom_class_id is not None:
                request.custom_class_id = custom_class_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_custom_class]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.CustomClass,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_custom_classes(
        self,
        request: Optional[Union[cloud_speech.ListCustomClassesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCustomClassesPager:
        r"""Lists CustomClasses.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_list_custom_classes():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.ListCustomClassesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_custom_classes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.ListCustomClassesRequest, dict]):
                The request object. Request message for the
                [ListCustomClasses][google.cloud.speech.v2.Speech.ListCustomClasses]
                method.
            parent (str):
                Required. The project and location of CustomClass
                resources to list. The expected format is
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v2.services.speech.pagers.ListCustomClassesPager:
                Response message for the
                   [ListCustomClasses][google.cloud.speech.v2.Speech.ListCustomClasses]
                   method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.ListCustomClassesRequest):
            request = cloud_speech.ListCustomClassesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_custom_classes]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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
        response = pagers.ListCustomClassesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_custom_class(
        self,
        request: Optional[Union[cloud_speech.GetCustomClassRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_speech.CustomClass:
        r"""Returns the requested
        [CustomClass][google.cloud.speech.v2.CustomClass].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_get_custom_class():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.GetCustomClassRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_custom_class(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.GetCustomClassRequest, dict]):
                The request object. Request message for the
                [GetCustomClass][google.cloud.speech.v2.Speech.GetCustomClass]
                method.
            name (str):
                Required. The name of the CustomClass to retrieve. The
                expected format is
                ``projects/{project}/locations/{location}/customClasses/{custom_class}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v2.types.CustomClass:
                CustomClass for biasing in speech
                recognition. Used to define a set of
                words or phrases that represents a
                common concept or theme likely to appear
                in your audio, for example a list of
                passenger ship names.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.GetCustomClassRequest):
            request = cloud_speech.GetCustomClassRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_custom_class]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def update_custom_class(
        self,
        request: Optional[Union[cloud_speech.UpdateCustomClassRequest, dict]] = None,
        *,
        custom_class: Optional[cloud_speech.CustomClass] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the [CustomClass][google.cloud.speech.v2.CustomClass].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_update_custom_class():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.UpdateCustomClassRequest(
                )

                # Make the request
                operation = client.update_custom_class(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.UpdateCustomClassRequest, dict]):
                The request object. Request message for the
                [UpdateCustomClass][google.cloud.speech.v2.Speech.UpdateCustomClass]
                method.
            custom_class (google.cloud.speech_v2.types.CustomClass):
                Required. The CustomClass to update.

                The CustomClass's ``name`` field is used to identify the
                CustomClass to update. Format:
                ``projects/{project}/locations/{location}/customClasses/{custom_class}``.

                This corresponds to the ``custom_class`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated. If
                empty, all fields are considered for
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
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.speech_v2.types.CustomClass` CustomClass for biasing in speech recognition. Used to define a set of words
                   or phrases that represents a common concept or theme
                   likely to appear in your audio, for example a list of
                   passenger ship names.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([custom_class, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.UpdateCustomClassRequest):
            request = cloud_speech.UpdateCustomClassRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if custom_class is not None:
                request.custom_class = custom_class
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_custom_class]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("custom_class.name", request.custom_class.name),)
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.CustomClass,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_custom_class(
        self,
        request: Optional[Union[cloud_speech.DeleteCustomClassRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes the [CustomClass][google.cloud.speech.v2.CustomClass].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_delete_custom_class():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.DeleteCustomClassRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_custom_class(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.DeleteCustomClassRequest, dict]):
                The request object. Request message for the
                [DeleteCustomClass][google.cloud.speech.v2.Speech.DeleteCustomClass]
                method.
            name (str):
                Required. The name of the CustomClass to delete. Format:
                ``projects/{project}/locations/{location}/customClasses/{custom_class}``

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

                The result type for the operation will be :class:`google.cloud.speech_v2.types.CustomClass` CustomClass for biasing in speech recognition. Used to define a set of words
                   or phrases that represents a common concept or theme
                   likely to appear in your audio, for example a list of
                   passenger ship names.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.DeleteCustomClassRequest):
            request = cloud_speech.DeleteCustomClassRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_custom_class]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.CustomClass,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def undelete_custom_class(
        self,
        request: Optional[Union[cloud_speech.UndeleteCustomClassRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Undeletes the [CustomClass][google.cloud.speech.v2.CustomClass].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_undelete_custom_class():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.UndeleteCustomClassRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undelete_custom_class(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.UndeleteCustomClassRequest, dict]):
                The request object. Request message for the
                [UndeleteCustomClass][google.cloud.speech.v2.Speech.UndeleteCustomClass]
                method.
            name (str):
                Required. The name of the CustomClass to undelete.
                Format:
                ``projects/{project}/locations/{location}/customClasses/{custom_class}``

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

                The result type for the operation will be :class:`google.cloud.speech_v2.types.CustomClass` CustomClass for biasing in speech recognition. Used to define a set of words
                   or phrases that represents a common concept or theme
                   likely to appear in your audio, for example a list of
                   passenger ship names.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.UndeleteCustomClassRequest):
            request = cloud_speech.UndeleteCustomClassRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.undelete_custom_class]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.CustomClass,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def create_phrase_set(
        self,
        request: Optional[Union[cloud_speech.CreatePhraseSetRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        phrase_set: Optional[cloud_speech.PhraseSet] = None,
        phrase_set_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a [PhraseSet][google.cloud.speech.v2.PhraseSet].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_create_phrase_set():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.CreatePhraseSetRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_phrase_set(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.CreatePhraseSetRequest, dict]):
                The request object. Request message for the
                [CreatePhraseSet][google.cloud.speech.v2.Speech.CreatePhraseSet]
                method.
            parent (str):
                Required. The project and location where this PhraseSet
                will be created. The expected format is
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            phrase_set (google.cloud.speech_v2.types.PhraseSet):
                Required. The PhraseSet to create.
                This corresponds to the ``phrase_set`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            phrase_set_id (str):
                The ID to use for the PhraseSet, which will become the
                final component of the PhraseSet's resource name.

                This value should be 4-63 characters, and valid
                characters are /[a-z][0-9]-/.

                This corresponds to the ``phrase_set_id`` field
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

                The result type for the operation will be :class:`google.cloud.speech_v2.types.PhraseSet` PhraseSet for biasing in speech recognition. A PhraseSet is used to provide
                   "hints" to the speech recognizer to favor specific
                   words and phrases in the results.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, phrase_set, phrase_set_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.CreatePhraseSetRequest):
            request = cloud_speech.CreatePhraseSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if phrase_set is not None:
                request.phrase_set = phrase_set
            if phrase_set_id is not None:
                request.phrase_set_id = phrase_set_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_phrase_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.PhraseSet,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_phrase_sets(
        self,
        request: Optional[Union[cloud_speech.ListPhraseSetsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPhraseSetsPager:
        r"""Lists PhraseSets.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_list_phrase_sets():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.ListPhraseSetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_phrase_sets(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.ListPhraseSetsRequest, dict]):
                The request object. Request message for the
                [ListPhraseSets][google.cloud.speech.v2.Speech.ListPhraseSets]
                method.
            parent (str):
                Required. The project and location of PhraseSet
                resources to list. The expected format is
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v2.services.speech.pagers.ListPhraseSetsPager:
                Response message for the
                   [ListPhraseSets][google.cloud.speech.v2.Speech.ListPhraseSets]
                   method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.ListPhraseSetsRequest):
            request = cloud_speech.ListPhraseSetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_phrase_sets]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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
        response = pagers.ListPhraseSetsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_phrase_set(
        self,
        request: Optional[Union[cloud_speech.GetPhraseSetRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_speech.PhraseSet:
        r"""Returns the requested
        [PhraseSet][google.cloud.speech.v2.PhraseSet].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_get_phrase_set():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.GetPhraseSetRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_phrase_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.GetPhraseSetRequest, dict]):
                The request object. Request message for the
                [GetPhraseSet][google.cloud.speech.v2.Speech.GetPhraseSet]
                method.
            name (str):
                Required. The name of the PhraseSet to retrieve. The
                expected format is
                ``projects/{project}/locations/{location}/phraseSets/{phrase_set}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.speech_v2.types.PhraseSet:
                PhraseSet for biasing in speech
                recognition. A PhraseSet is used to
                provide "hints" to the speech recognizer
                to favor specific words and phrases in
                the results.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.GetPhraseSetRequest):
            request = cloud_speech.GetPhraseSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_phrase_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def update_phrase_set(
        self,
        request: Optional[Union[cloud_speech.UpdatePhraseSetRequest, dict]] = None,
        *,
        phrase_set: Optional[cloud_speech.PhraseSet] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the [PhraseSet][google.cloud.speech.v2.PhraseSet].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_update_phrase_set():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.UpdatePhraseSetRequest(
                )

                # Make the request
                operation = client.update_phrase_set(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.UpdatePhraseSetRequest, dict]):
                The request object. Request message for the
                [UpdatePhraseSet][google.cloud.speech.v2.Speech.UpdatePhraseSet]
                method.
            phrase_set (google.cloud.speech_v2.types.PhraseSet):
                Required. The PhraseSet to update.

                The PhraseSet's ``name`` field is used to identify the
                PhraseSet to update. Format:
                ``projects/{project}/locations/{location}/phraseSets/{phrase_set}``.

                This corresponds to the ``phrase_set`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to update. If empty, all non-default
                valued fields are considered for update. Use ``*`` to
                update the entire PhraseSet resource.

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

                The result type for the operation will be :class:`google.cloud.speech_v2.types.PhraseSet` PhraseSet for biasing in speech recognition. A PhraseSet is used to provide
                   "hints" to the speech recognizer to favor specific
                   words and phrases in the results.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([phrase_set, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.UpdatePhraseSetRequest):
            request = cloud_speech.UpdatePhraseSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if phrase_set is not None:
                request.phrase_set = phrase_set
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_phrase_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("phrase_set.name", request.phrase_set.name),)
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.PhraseSet,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_phrase_set(
        self,
        request: Optional[Union[cloud_speech.DeletePhraseSetRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes the [PhraseSet][google.cloud.speech.v2.PhraseSet].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_delete_phrase_set():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.DeletePhraseSetRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_phrase_set(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.DeletePhraseSetRequest, dict]):
                The request object. Request message for the
                [DeletePhraseSet][google.cloud.speech.v2.Speech.DeletePhraseSet]
                method.
            name (str):
                Required. The name of the PhraseSet to delete. Format:
                ``projects/{project}/locations/{location}/phraseSets/{phrase_set}``

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

                The result type for the operation will be :class:`google.cloud.speech_v2.types.PhraseSet` PhraseSet for biasing in speech recognition. A PhraseSet is used to provide
                   "hints" to the speech recognizer to favor specific
                   words and phrases in the results.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.DeletePhraseSetRequest):
            request = cloud_speech.DeletePhraseSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_phrase_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.PhraseSet,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def undelete_phrase_set(
        self,
        request: Optional[Union[cloud_speech.UndeletePhraseSetRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Undeletes the [PhraseSet][google.cloud.speech.v2.PhraseSet].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import speech_v2

            def sample_undelete_phrase_set():
                # Create a client
                client = speech_v2.SpeechClient()

                # Initialize request argument(s)
                request = speech_v2.UndeletePhraseSetRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undelete_phrase_set(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.speech_v2.types.UndeletePhraseSetRequest, dict]):
                The request object. Request message for the
                [UndeletePhraseSet][google.cloud.speech.v2.Speech.UndeletePhraseSet]
                method.
            name (str):
                Required. The name of the PhraseSet to undelete. Format:
                ``projects/{project}/locations/{location}/phraseSets/{phrase_set}``

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

                The result type for the operation will be :class:`google.cloud.speech_v2.types.PhraseSet` PhraseSet for biasing in speech recognition. A PhraseSet is used to provide
                   "hints" to the speech recognizer to favor specific
                   words and phrases in the results.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, cloud_speech.UndeletePhraseSetRequest):
            request = cloud_speech.UndeletePhraseSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.undelete_phrase_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloud_speech.PhraseSet,
            metadata_type=cloud_speech.OperationMetadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "SpeechClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_operations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_operation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def get_location(
        self,
        request: Optional[locations_pb2.GetLocationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.Location:
                Location object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.GetLocationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_location]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def list_locations(
        self,
        request: Optional[locations_pb2.ListLocationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.ListLocationsResponse:
                Response message for ``ListLocations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.ListLocationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_locations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("SpeechClient",)
