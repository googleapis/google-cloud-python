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

from google.cloud.visionai_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.visionai_v1.services.warehouse import pagers
from google.cloud.visionai_v1.types import warehouse

from .transports.base import DEFAULT_CLIENT_INFO, WarehouseTransport
from .transports.grpc import WarehouseGrpcTransport
from .transports.grpc_asyncio import WarehouseGrpcAsyncIOTransport
from .transports.rest import WarehouseRestTransport


class WarehouseClientMeta(type):
    """Metaclass for the Warehouse client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[WarehouseTransport]]
    _transport_registry["grpc"] = WarehouseGrpcTransport
    _transport_registry["grpc_asyncio"] = WarehouseGrpcAsyncIOTransport
    _transport_registry["rest"] = WarehouseRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[WarehouseTransport]:
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


class WarehouseClient(metaclass=WarehouseClientMeta):
    """Service that manages media content + metadata for streaming."""

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
    DEFAULT_ENDPOINT = "visionai.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "visionai.{UNIVERSE_DOMAIN}"
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
            WarehouseClient: The constructed client.
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
            WarehouseClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> WarehouseTransport:
        """Returns the transport used by the client instance.

        Returns:
            WarehouseTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def annotation_path(
        project_number: str,
        location: str,
        corpus: str,
        asset: str,
        annotation: str,
    ) -> str:
        """Returns a fully-qualified annotation string."""
        return "projects/{project_number}/locations/{location}/corpora/{corpus}/assets/{asset}/annotations/{annotation}".format(
            project_number=project_number,
            location=location,
            corpus=corpus,
            asset=asset,
            annotation=annotation,
        )

    @staticmethod
    def parse_annotation_path(path: str) -> Dict[str, str]:
        """Parses a annotation path into its component segments."""
        m = re.match(
            r"^projects/(?P<project_number>.+?)/locations/(?P<location>.+?)/corpora/(?P<corpus>.+?)/assets/(?P<asset>.+?)/annotations/(?P<annotation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def asset_path(
        project_number: str,
        location: str,
        corpus: str,
        asset: str,
    ) -> str:
        """Returns a fully-qualified asset string."""
        return "projects/{project_number}/locations/{location}/corpora/{corpus}/assets/{asset}".format(
            project_number=project_number,
            location=location,
            corpus=corpus,
            asset=asset,
        )

    @staticmethod
    def parse_asset_path(path: str) -> Dict[str, str]:
        """Parses a asset path into its component segments."""
        m = re.match(
            r"^projects/(?P<project_number>.+?)/locations/(?P<location>.+?)/corpora/(?P<corpus>.+?)/assets/(?P<asset>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def collection_path(
        project_number: str,
        location: str,
        corpus: str,
        collection: str,
    ) -> str:
        """Returns a fully-qualified collection string."""
        return "projects/{project_number}/locations/{location}/corpora/{corpus}/collections/{collection}".format(
            project_number=project_number,
            location=location,
            corpus=corpus,
            collection=collection,
        )

    @staticmethod
    def parse_collection_path(path: str) -> Dict[str, str]:
        """Parses a collection path into its component segments."""
        m = re.match(
            r"^projects/(?P<project_number>.+?)/locations/(?P<location>.+?)/corpora/(?P<corpus>.+?)/collections/(?P<collection>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def corpus_path(
        project_number: str,
        location: str,
        corpus: str,
    ) -> str:
        """Returns a fully-qualified corpus string."""
        return "projects/{project_number}/locations/{location}/corpora/{corpus}".format(
            project_number=project_number,
            location=location,
            corpus=corpus,
        )

    @staticmethod
    def parse_corpus_path(path: str) -> Dict[str, str]:
        """Parses a corpus path into its component segments."""
        m = re.match(
            r"^projects/(?P<project_number>.+?)/locations/(?P<location>.+?)/corpora/(?P<corpus>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def data_schema_path(
        project_number: str,
        location: str,
        corpus: str,
        data_schema: str,
    ) -> str:
        """Returns a fully-qualified data_schema string."""
        return "projects/{project_number}/locations/{location}/corpora/{corpus}/dataSchemas/{data_schema}".format(
            project_number=project_number,
            location=location,
            corpus=corpus,
            data_schema=data_schema,
        )

    @staticmethod
    def parse_data_schema_path(path: str) -> Dict[str, str]:
        """Parses a data_schema path into its component segments."""
        m = re.match(
            r"^projects/(?P<project_number>.+?)/locations/(?P<location>.+?)/corpora/(?P<corpus>.+?)/dataSchemas/(?P<data_schema>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def index_path(
        project_number: str,
        location: str,
        corpus: str,
        index: str,
    ) -> str:
        """Returns a fully-qualified index string."""
        return "projects/{project_number}/locations/{location}/corpora/{corpus}/indexes/{index}".format(
            project_number=project_number,
            location=location,
            corpus=corpus,
            index=index,
        )

    @staticmethod
    def parse_index_path(path: str) -> Dict[str, str]:
        """Parses a index path into its component segments."""
        m = re.match(
            r"^projects/(?P<project_number>.+?)/locations/(?P<location>.+?)/corpora/(?P<corpus>.+?)/indexes/(?P<index>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def index_endpoint_path(
        project: str,
        location: str,
        index_endpoint: str,
    ) -> str:
        """Returns a fully-qualified index_endpoint string."""
        return "projects/{project}/locations/{location}/indexEndpoints/{index_endpoint}".format(
            project=project,
            location=location,
            index_endpoint=index_endpoint,
        )

    @staticmethod
    def parse_index_endpoint_path(path: str) -> Dict[str, str]:
        """Parses a index_endpoint path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/indexEndpoints/(?P<index_endpoint>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def search_config_path(
        project_number: str,
        location: str,
        corpus: str,
        search_config: str,
    ) -> str:
        """Returns a fully-qualified search_config string."""
        return "projects/{project_number}/locations/{location}/corpora/{corpus}/searchConfigs/{search_config}".format(
            project_number=project_number,
            location=location,
            corpus=corpus,
            search_config=search_config,
        )

    @staticmethod
    def parse_search_config_path(path: str) -> Dict[str, str]:
        """Parses a search_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project_number>.+?)/locations/(?P<location>.+?)/corpora/(?P<corpus>.+?)/searchConfigs/(?P<search_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def search_hypernym_path(
        project_number: str,
        location: str,
        corpus: str,
        search_hypernym: str,
    ) -> str:
        """Returns a fully-qualified search_hypernym string."""
        return "projects/{project_number}/locations/{location}/corpora/{corpus}/searchHypernyms/{search_hypernym}".format(
            project_number=project_number,
            location=location,
            corpus=corpus,
            search_hypernym=search_hypernym,
        )

    @staticmethod
    def parse_search_hypernym_path(path: str) -> Dict[str, str]:
        """Parses a search_hypernym path into its component segments."""
        m = re.match(
            r"^projects/(?P<project_number>.+?)/locations/(?P<location>.+?)/corpora/(?P<corpus>.+?)/searchHypernyms/(?P<search_hypernym>.+?)$",
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
            _default_universe = WarehouseClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = WarehouseClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = WarehouseClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = WarehouseClient._DEFAULT_UNIVERSE
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

        default_universe = WarehouseClient._DEFAULT_UNIVERSE
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
            or WarehouseClient._compare_universes(
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
            Union[str, WarehouseTransport, Callable[..., WarehouseTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the warehouse client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,WarehouseTransport,Callable[..., WarehouseTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the WarehouseTransport constructor.
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
        ) = WarehouseClient._read_environment_variables()
        self._client_cert_source = WarehouseClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = WarehouseClient._get_universe_domain(
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
        transport_provided = isinstance(transport, WarehouseTransport)
        if transport_provided:
            # transport is a WarehouseTransport instance.
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
            self._transport = cast(WarehouseTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = self._api_endpoint or WarehouseClient._get_api_endpoint(
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
                Type[WarehouseTransport], Callable[..., WarehouseTransport]
            ] = (
                WarehouseClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., WarehouseTransport], transport)
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

    def create_asset(
        self,
        request: Optional[Union[warehouse.CreateAssetRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        asset: Optional[warehouse.Asset] = None,
        asset_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Asset:
        r"""Creates an asset inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_create_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.CreateAssetRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_asset(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.CreateAssetRequest, dict]):
                The request object. Request message for
                CreateAssetRequest.
            parent (str):
                Required. The parent resource where this asset will be
                created. Format:
                ``projects/{project_number}/locations/{location_id}/corpora/{corpus_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            asset (google.cloud.visionai_v1.types.Asset):
                Required. The asset to create.
                This corresponds to the ``asset`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            asset_id (str):
                Optional. The ID to use for the asset, which will become
                the final component of the asset's resource name if user
                choose to specify. Otherwise, asset id will be generated
                by system.

                This value should be up to 63 characters, and valid
                characters are /[a-z][0-9]-/. The first character must
                be a letter, the last could be a letter or a number.

                This corresponds to the ``asset_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.Asset:
                An asset is a resource in corpus. It
                represents a media object inside corpus,
                contains metadata and another resource
                annotation. Different feature could be
                applied to the asset to generate
                annotations. User could specified
                annotation related to the target asset.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, asset, asset_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.CreateAssetRequest):
            request = warehouse.CreateAssetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if asset is not None:
                request.asset = asset
            if asset_id is not None:
                request.asset_id = asset_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_asset]

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

        # Done; return the response.
        return response

    def update_asset(
        self,
        request: Optional[Union[warehouse.UpdateAssetRequest, dict]] = None,
        *,
        asset: Optional[warehouse.Asset] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Asset:
        r"""Updates an asset inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_update_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.UpdateAssetRequest(
                )

                # Make the request
                response = client.update_asset(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UpdateAssetRequest, dict]):
                The request object. Request message for UpdateAsset.
            asset (google.cloud.visionai_v1.types.Asset):
                Required. The asset to update.

                The asset's ``name`` field is used to identify the asset
                to be updated. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/assets/{asset}``

                This corresponds to the ``asset`` field
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
            google.cloud.visionai_v1.types.Asset:
                An asset is a resource in corpus. It
                represents a media object inside corpus,
                contains metadata and another resource
                annotation. Different feature could be
                applied to the asset to generate
                annotations. User could specified
                annotation related to the target asset.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([asset, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UpdateAssetRequest):
            request = warehouse.UpdateAssetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if asset is not None:
                request.asset = asset
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_asset]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("asset.name", request.asset.name),)
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

    def get_asset(
        self,
        request: Optional[Union[warehouse.GetAssetRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Asset:
        r"""Reads an asset inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_get_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GetAssetRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_asset(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GetAssetRequest, dict]):
                The request object. Request message for GetAsset.
            name (str):
                Required. The name of the asset to retrieve. Format:
                projects/{project_number}/locations/{location}/corpora/{corpus}/assets/{asset}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.Asset:
                An asset is a resource in corpus. It
                represents a media object inside corpus,
                contains metadata and another resource
                annotation. Different feature could be
                applied to the asset to generate
                annotations. User could specified
                annotation related to the target asset.

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
        if not isinstance(request, warehouse.GetAssetRequest):
            request = warehouse.GetAssetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_asset]

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

    def list_assets(
        self,
        request: Optional[Union[warehouse.ListAssetsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAssetsPager:
        r"""Lists an list of assets inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_list_assets():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ListAssetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_assets(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ListAssetsRequest, dict]):
                The request object. Request message for ListAssets.
            parent (str):
                Required. The parent, which owns this collection of
                assets. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ListAssetsPager:
                Response message for ListAssets.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        if not isinstance(request, warehouse.ListAssetsRequest):
            request = warehouse.ListAssetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_assets]

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
        response = pagers.ListAssetsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_asset(
        self,
        request: Optional[Union[warehouse.DeleteAssetRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes asset inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_delete_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.DeleteAssetRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_asset(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeleteAssetRequest, dict]):
                The request object. Request message for DeleteAsset.
            name (str):
                Required. The name of the asset to delete. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/assets/{asset}``

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

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

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
        if not isinstance(request, warehouse.DeleteAssetRequest):
            request = warehouse.DeleteAssetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_asset]

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
            empty_pb2.Empty,
            metadata_type=warehouse.DeleteAssetMetadata,
        )

        # Done; return the response.
        return response

    def upload_asset(
        self,
        request: Optional[Union[warehouse.UploadAssetRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Upload asset by specifing the asset Cloud Storage
        uri. For video warehouse, it requires users who call
        this API have read access to the cloud storage file.
        Once it is uploaded, it can be retrieved by
        GenerateRetrievalUrl API which by default, only can
        retrieve cloud storage files from the same project of
        the warehouse. To allow retrieval cloud storage files
        that are in a separate project, it requires to find the
        vision ai service account (Go to IAM, check checkbox to
        show "Include Google-provided role grants", search for
        "Cloud Vision AI Service Agent") and grant the read
        access of the cloud storage files to that service
        account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_upload_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.UploadAssetRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.upload_asset(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UploadAssetRequest, dict]):
                The request object. Request message for UploadAsset.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.visionai_v1.types.UploadAssetResponse`
                Response message for UploadAsset.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UploadAssetRequest):
            request = warehouse.UploadAssetRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.upload_asset]

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
            warehouse.UploadAssetResponse,
            metadata_type=warehouse.UploadAssetMetadata,
        )

        # Done; return the response.
        return response

    def generate_retrieval_url(
        self,
        request: Optional[Union[warehouse.GenerateRetrievalUrlRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.GenerateRetrievalUrlResponse:
        r"""Generates a signed url for downloading the asset.
        For video warehouse, please see comment of UploadAsset
        about how to allow retrieval of cloud storage files in a
        different project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_generate_retrieval_url():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GenerateRetrievalUrlRequest(
                    name="name_value",
                )

                # Make the request
                response = client.generate_retrieval_url(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GenerateRetrievalUrlRequest, dict]):
                The request object. Request message for
                GenerateRetrievalUrl API.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.GenerateRetrievalUrlResponse:
                Response message for
                GenerateRetrievalUrl API.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.GenerateRetrievalUrlRequest):
            request = warehouse.GenerateRetrievalUrlRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.generate_retrieval_url]

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

    def analyze_asset(
        self,
        request: Optional[Union[warehouse.AnalyzeAssetRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Analyze asset to power search capability.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_analyze_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.AnalyzeAssetRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.analyze_asset(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.AnalyzeAssetRequest, dict]):
                The request object. Request message for AnalyzeAsset.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.visionai_v1.types.AnalyzeAssetResponse`
                Response message for AnalyzeAsset.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.AnalyzeAssetRequest):
            request = warehouse.AnalyzeAssetRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.analyze_asset]

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
            warehouse.AnalyzeAssetResponse,
            metadata_type=warehouse.AnalyzeAssetMetadata,
        )

        # Done; return the response.
        return response

    def index_asset(
        self,
        request: Optional[Union[warehouse.IndexAssetRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Index one asset for search. Supported corpus type:
        Corpus.Type.VIDEO_ON_DEMAND

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_index_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.IndexAssetRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.index_asset(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.IndexAssetRequest, dict]):
                The request object. Request message for IndexAsset.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.visionai_v1.types.IndexAssetResponse`
                Response message for IndexAsset.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.IndexAssetRequest):
            request = warehouse.IndexAssetRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.index_asset]

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
            warehouse.IndexAssetResponse,
            metadata_type=warehouse.IndexAssetMetadata,
        )

        # Done; return the response.
        return response

    def remove_index_asset(
        self,
        request: Optional[Union[warehouse.RemoveIndexAssetRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Remove one asset's index data for search. Supported corpus type:
        Corpus.Type.VIDEO_ON_DEMAND

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_remove_index_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.RemoveIndexAssetRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.remove_index_asset(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.RemoveIndexAssetRequest, dict]):
                The request object. Request message for RemoveIndexAsset.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.visionai_v1.types.RemoveIndexAssetResponse`
                Response message for RemoveIndexAsset.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.RemoveIndexAssetRequest):
            request = warehouse.RemoveIndexAssetRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_index_asset]

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
            warehouse.RemoveIndexAssetResponse,
            metadata_type=warehouse.RemoveIndexAssetMetadata,
        )

        # Done; return the response.
        return response

    def view_indexed_assets(
        self,
        request: Optional[Union[warehouse.ViewIndexedAssetsRequest, dict]] = None,
        *,
        index: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ViewIndexedAssetsPager:
        r"""Lists assets inside an index.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_view_indexed_assets():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ViewIndexedAssetsRequest(
                    index="index_value",
                )

                # Make the request
                page_result = client.view_indexed_assets(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ViewIndexedAssetsRequest, dict]):
                The request object. Request message for
                ViewIndexedAssets.
            index (str):
                Required. The index that owns this collection of assets.
                Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/indexes/{index}``

                This corresponds to the ``index`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ViewIndexedAssetsPager:
                Response message for
                ViewIndexedAssets.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([index])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.ViewIndexedAssetsRequest):
            request = warehouse.ViewIndexedAssetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if index is not None:
                request.index = index

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.view_indexed_assets]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("index", request.index),)),
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
        response = pagers.ViewIndexedAssetsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_index(
        self,
        request: Optional[Union[warehouse.CreateIndexRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        index: Optional[warehouse.Index] = None,
        index_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates an Index under the corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_create_index():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                index = visionai_v1.Index()
                index.entire_corpus = True

                request = visionai_v1.CreateIndexRequest(
                    parent="parent_value",
                    index=index,
                )

                # Make the request
                operation = client.create_index(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.CreateIndexRequest, dict]):
                The request object. Message for creating an Index.
            parent (str):
                Required. Value for the parent. The resource name of the
                Corpus under which this index is created. Format:
                ``projects/{project_number}/locations/{location_id}/corpora/{corpus_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            index (google.cloud.visionai_v1.types.Index):
                Required. The index being created.
                This corresponds to the ``index`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            index_id (str):
                Optional. The ID for the index. This will become the
                final resource name for the index. If the user does not
                specify this value, it will be generated by system.

                This value should be up to 63 characters, and valid
                characters are /[a-z][0-9]-/. The first character must
                be a letter, the last could be a letter or a number.

                This corresponds to the ``index_id`` field
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

                The result type for the operation will be :class:`google.cloud.visionai_v1.types.Index` An Index is a resource in Corpus. It contains an indexed version of the
                   assets and annotations. When deployed to an endpoint,
                   it will allow users to search the Index.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, index, index_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.CreateIndexRequest):
            request = warehouse.CreateIndexRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if index is not None:
                request.index = index
            if index_id is not None:
                request.index_id = index_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_index]

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
            warehouse.Index,
            metadata_type=warehouse.CreateIndexMetadata,
        )

        # Done; return the response.
        return response

    def update_index(
        self,
        request: Optional[Union[warehouse.UpdateIndexRequest, dict]] = None,
        *,
        index: Optional[warehouse.Index] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates an Index under the corpus. Users can perform a
        metadata-only update or trigger a full index rebuild with
        different update_mask values.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_update_index():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                index = visionai_v1.Index()
                index.entire_corpus = True

                request = visionai_v1.UpdateIndexRequest(
                    index=index,
                )

                # Make the request
                operation = client.update_index(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UpdateIndexRequest, dict]):
                The request object. Request message for UpdateIndex.
            index (google.cloud.visionai_v1.types.Index):
                Required. The resource being updated.
                This corresponds to the ``index`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to specify the fields to be
                overwritten in the Index resource by the update. The
                fields specified in the update_mask are relative to the
                resource, not the full request. A field of the resource
                will be overwritten if it is in the mask. Empty field
                mask is not allowed. If the mask is "*", it triggers a
                full update of the index, and also a whole rebuild of
                index data.

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

                The result type for the operation will be :class:`google.cloud.visionai_v1.types.Index` An Index is a resource in Corpus. It contains an indexed version of the
                   assets and annotations. When deployed to an endpoint,
                   it will allow users to search the Index.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([index, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UpdateIndexRequest):
            request = warehouse.UpdateIndexRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if index is not None:
                request.index = index
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_index]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("index.name", request.index.name),)
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
            warehouse.Index,
            metadata_type=warehouse.UpdateIndexMetadata,
        )

        # Done; return the response.
        return response

    def get_index(
        self,
        request: Optional[Union[warehouse.GetIndexRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Index:
        r"""Gets the details of a single Index under a Corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_get_index():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GetIndexRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_index(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GetIndexRequest, dict]):
                The request object. Request message for getting an Index.
            name (str):
                Required. Name of the Index resource. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/indexes/{index}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.Index:
                An Index is a resource in Corpus. It
                contains an indexed version of the
                assets and annotations. When deployed to
                an endpoint, it will allow users to
                search the Index.

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
        if not isinstance(request, warehouse.GetIndexRequest):
            request = warehouse.GetIndexRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_index]

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

    def list_indexes(
        self,
        request: Optional[Union[warehouse.ListIndexesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListIndexesPager:
        r"""List all Indexes in a given Corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_list_indexes():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ListIndexesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_indexes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ListIndexesRequest, dict]):
                The request object. Request message for listing Indexes.
            parent (str):
                Required. The parent corpus that owns this collection of
                indexes. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ListIndexesPager:
                Response message for ListIndexes.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        if not isinstance(request, warehouse.ListIndexesRequest):
            request = warehouse.ListIndexesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_indexes]

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
        response = pagers.ListIndexesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_index(
        self,
        request: Optional[Union[warehouse.DeleteIndexRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Delete a single Index. In order to delete an index,
        the caller must make sure that it is not deployed to any
        index endpoint.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_delete_index():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.DeleteIndexRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_index(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeleteIndexRequest, dict]):
                The request object. Request message for DeleteIndex.
            name (str):
                Required. The name of the index to delete. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/indexes/{index}``

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

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

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
        if not isinstance(request, warehouse.DeleteIndexRequest):
            request = warehouse.DeleteIndexRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_index]

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
            empty_pb2.Empty,
            metadata_type=warehouse.DeleteIndexMetadata,
        )

        # Done; return the response.
        return response

    def create_corpus(
        self,
        request: Optional[Union[warehouse.CreateCorpusRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        corpus: Optional[warehouse.Corpus] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a corpus inside a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_create_corpus():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                corpus = visionai_v1.Corpus()
                corpus.display_name = "display_name_value"

                request = visionai_v1.CreateCorpusRequest(
                    parent="parent_value",
                    corpus=corpus,
                )

                # Make the request
                operation = client.create_corpus(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.CreateCorpusRequest, dict]):
                The request object. Request message of CreateCorpus API.
            parent (str):
                Required. Form:
                ``projects/{project_number}/locations/{location_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            corpus (google.cloud.visionai_v1.types.Corpus):
                Required. The corpus to be created.
                This corresponds to the ``corpus`` field
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

                The result type for the operation will be :class:`google.cloud.visionai_v1.types.Corpus` Corpus is a set of media contents for management.
                   Within a corpus, media shares the same data schema.
                   Search is also restricted within a single corpus.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, corpus])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.CreateCorpusRequest):
            request = warehouse.CreateCorpusRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if corpus is not None:
                request.corpus = corpus

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_corpus]

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
            warehouse.Corpus,
            metadata_type=warehouse.CreateCorpusMetadata,
        )

        # Done; return the response.
        return response

    def get_corpus(
        self,
        request: Optional[Union[warehouse.GetCorpusRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Corpus:
        r"""Gets corpus details inside a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_get_corpus():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GetCorpusRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_corpus(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GetCorpusRequest, dict]):
                The request object. Request message for GetCorpus.
            name (str):
                Required. The resource name of the
                corpus to retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.Corpus:
                Corpus is a set of media contents for
                management. Within a corpus, media
                shares the same data schema. Search is
                also restricted within a single corpus.

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
        if not isinstance(request, warehouse.GetCorpusRequest):
            request = warehouse.GetCorpusRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_corpus]

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

    def update_corpus(
        self,
        request: Optional[Union[warehouse.UpdateCorpusRequest, dict]] = None,
        *,
        corpus: Optional[warehouse.Corpus] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Corpus:
        r"""Updates a corpus in a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_update_corpus():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                corpus = visionai_v1.Corpus()
                corpus.display_name = "display_name_value"

                request = visionai_v1.UpdateCorpusRequest(
                    corpus=corpus,
                )

                # Make the request
                response = client.update_corpus(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UpdateCorpusRequest, dict]):
                The request object. Request message for UpdateCorpus.
            corpus (google.cloud.visionai_v1.types.Corpus):
                Required. The corpus which replaces
                the resource on the server.

                This corresponds to the ``corpus`` field
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
            google.cloud.visionai_v1.types.Corpus:
                Corpus is a set of media contents for
                management. Within a corpus, media
                shares the same data schema. Search is
                also restricted within a single corpus.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([corpus, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UpdateCorpusRequest):
            request = warehouse.UpdateCorpusRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if corpus is not None:
                request.corpus = corpus
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_corpus]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("corpus.name", request.corpus.name),)
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

    def list_corpora(
        self,
        request: Optional[Union[warehouse.ListCorporaRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCorporaPager:
        r"""Lists all corpora in a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_list_corpora():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ListCorporaRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_corpora(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ListCorporaRequest, dict]):
                The request object. Request message for ListCorpora.
            parent (str):
                Required. The resource name of the
                project from which to list corpora.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ListCorporaPager:
                Response message for ListCorpora.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        if not isinstance(request, warehouse.ListCorporaRequest):
            request = warehouse.ListCorporaRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_corpora]

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
        response = pagers.ListCorporaPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_corpus(
        self,
        request: Optional[Union[warehouse.DeleteCorpusRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a corpus only if its empty.
        Returns empty response.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_delete_corpus():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.DeleteCorpusRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_corpus(request=request)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeleteCorpusRequest, dict]):
                The request object. Request message for DeleteCorpus.
            name (str):
                Required. The resource name of the
                corpus to delete.

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
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.DeleteCorpusRequest):
            request = warehouse.DeleteCorpusRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_corpus]

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

    def analyze_corpus(
        self,
        request: Optional[Union[warehouse.AnalyzeCorpusRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Analyzes a corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_analyze_corpus():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.AnalyzeCorpusRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.analyze_corpus(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.AnalyzeCorpusRequest, dict]):
                The request object. Request message for AnalyzeCorpus.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.visionai_v1.types.AnalyzeCorpusResponse`
                The response message for AnalyzeCorpus LRO.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.AnalyzeCorpusRequest):
            request = warehouse.AnalyzeCorpusRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.analyze_corpus]

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
            warehouse.AnalyzeCorpusResponse,
            metadata_type=warehouse.AnalyzeCorpusMetadata,
        )

        # Done; return the response.
        return response

    def create_data_schema(
        self,
        request: Optional[Union[warehouse.CreateDataSchemaRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        data_schema: Optional[warehouse.DataSchema] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.DataSchema:
        r"""Creates data schema inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_create_data_schema():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                data_schema = visionai_v1.DataSchema()
                data_schema.key = "key_value"

                request = visionai_v1.CreateDataSchemaRequest(
                    parent="parent_value",
                    data_schema=data_schema,
                )

                # Make the request
                response = client.create_data_schema(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.CreateDataSchemaRequest, dict]):
                The request object. Request message for CreateDataSchema.
            parent (str):
                Required. The parent resource where this data schema
                will be created. Format:
                ``projects/{project_number}/locations/{location_id}/corpora/{corpus_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            data_schema (google.cloud.visionai_v1.types.DataSchema):
                Required. The data schema to create.
                This corresponds to the ``data_schema`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.DataSchema:
                Data schema indicates how the user
                specified annotation is interpreted in
                the system.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, data_schema])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.CreateDataSchemaRequest):
            request = warehouse.CreateDataSchemaRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if data_schema is not None:
                request.data_schema = data_schema

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_data_schema]

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

        # Done; return the response.
        return response

    def update_data_schema(
        self,
        request: Optional[Union[warehouse.UpdateDataSchemaRequest, dict]] = None,
        *,
        data_schema: Optional[warehouse.DataSchema] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.DataSchema:
        r"""Updates data schema inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_update_data_schema():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                data_schema = visionai_v1.DataSchema()
                data_schema.key = "key_value"

                request = visionai_v1.UpdateDataSchemaRequest(
                    data_schema=data_schema,
                )

                # Make the request
                response = client.update_data_schema(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UpdateDataSchemaRequest, dict]):
                The request object. Request message for UpdateDataSchema.
            data_schema (google.cloud.visionai_v1.types.DataSchema):
                Required. The data schema's ``name`` field is used to
                identify the data schema to be updated. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/dataSchemas/{data_schema}``

                This corresponds to the ``data_schema`` field
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
            google.cloud.visionai_v1.types.DataSchema:
                Data schema indicates how the user
                specified annotation is interpreted in
                the system.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([data_schema, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UpdateDataSchemaRequest):
            request = warehouse.UpdateDataSchemaRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if data_schema is not None:
                request.data_schema = data_schema
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_data_schema]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("data_schema.name", request.data_schema.name),)
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

    def get_data_schema(
        self,
        request: Optional[Union[warehouse.GetDataSchemaRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.DataSchema:
        r"""Gets data schema inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_get_data_schema():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GetDataSchemaRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_data_schema(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GetDataSchemaRequest, dict]):
                The request object. Request message for GetDataSchema.
            name (str):
                Required. The name of the data schema to retrieve.
                Format:
                ``projects/{project_number}/locations/{location_id}/corpora/{corpus_id}/dataSchemas/{data_schema_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.DataSchema:
                Data schema indicates how the user
                specified annotation is interpreted in
                the system.

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
        if not isinstance(request, warehouse.GetDataSchemaRequest):
            request = warehouse.GetDataSchemaRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_data_schema]

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

    def delete_data_schema(
        self,
        request: Optional[Union[warehouse.DeleteDataSchemaRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes data schema inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_delete_data_schema():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.DeleteDataSchemaRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_data_schema(request=request)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeleteDataSchemaRequest, dict]):
                The request object. Request message for DeleteDataSchema.
            name (str):
                Required. The name of the data schema to delete. Format:
                ``projects/{project_number}/locations/{location_id}/corpora/{corpus_id}/dataSchemas/{data_schema_id}``

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
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.DeleteDataSchemaRequest):
            request = warehouse.DeleteDataSchemaRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_data_schema]

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

    def list_data_schemas(
        self,
        request: Optional[Union[warehouse.ListDataSchemasRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDataSchemasPager:
        r"""Lists a list of data schemas inside corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_list_data_schemas():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ListDataSchemasRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_data_schemas(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ListDataSchemasRequest, dict]):
                The request object. Request message for ListDataSchemas.
            parent (str):
                Required. The parent, which owns this collection of data
                schemas. Format:
                ``projects/{project_number}/locations/{location_id}/corpora/{corpus_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ListDataSchemasPager:
                Response message for ListDataSchemas.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        if not isinstance(request, warehouse.ListDataSchemasRequest):
            request = warehouse.ListDataSchemasRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_data_schemas]

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
        response = pagers.ListDataSchemasPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_annotation(
        self,
        request: Optional[Union[warehouse.CreateAnnotationRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        annotation: Optional[warehouse.Annotation] = None,
        annotation_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Annotation:
        r"""Creates annotation inside asset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_create_annotation():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.CreateAnnotationRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_annotation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.CreateAnnotationRequest, dict]):
                The request object. Request message for CreateAnnotation.
            parent (str):
                Required. The parent resource where this annotation will
                be created. Format:
                ``projects/{project_number}/locations/{location_id}/corpora/{corpus_id}/assets/{asset_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            annotation (google.cloud.visionai_v1.types.Annotation):
                Required. The annotation to create.
                This corresponds to the ``annotation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            annotation_id (str):
                Optional. The ID to use for the annotation, which will
                become the final component of the annotation's resource
                name if user choose to specify. Otherwise, annotation id
                will be generated by system.

                This value should be up to 63 characters, and valid
                characters are /[a-z][0-9]-/. The first character must
                be a letter, the last could be a letter or a number.

                This corresponds to the ``annotation_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.Annotation:
                An annotation is a resource in asset.
                It represents a key-value mapping of
                content in asset.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, annotation, annotation_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.CreateAnnotationRequest):
            request = warehouse.CreateAnnotationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if annotation is not None:
                request.annotation = annotation
            if annotation_id is not None:
                request.annotation_id = annotation_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_annotation]

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

        # Done; return the response.
        return response

    def get_annotation(
        self,
        request: Optional[Union[warehouse.GetAnnotationRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Annotation:
        r"""Reads annotation inside asset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_get_annotation():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GetAnnotationRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_annotation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GetAnnotationRequest, dict]):
                The request object. Request message for GetAnnotation
                API.
            name (str):
                Required. The name of the annotation to retrieve.
                Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/assets/{asset}/annotations/{annotation}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.Annotation:
                An annotation is a resource in asset.
                It represents a key-value mapping of
                content in asset.

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
        if not isinstance(request, warehouse.GetAnnotationRequest):
            request = warehouse.GetAnnotationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_annotation]

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

    def list_annotations(
        self,
        request: Optional[Union[warehouse.ListAnnotationsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAnnotationsPager:
        r"""Lists a list of annotations inside asset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_list_annotations():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ListAnnotationsRequest(
                )

                # Make the request
                page_result = client.list_annotations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ListAnnotationsRequest, dict]):
                The request object. Request message for GetAnnotation
                API.
            parent (str):
                The parent, which owns this collection of annotations.
                Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/assets/{asset}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ListAnnotationsPager:
                Request message for ListAnnotations
                API.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        if not isinstance(request, warehouse.ListAnnotationsRequest):
            request = warehouse.ListAnnotationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_annotations]

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
        response = pagers.ListAnnotationsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_annotation(
        self,
        request: Optional[Union[warehouse.UpdateAnnotationRequest, dict]] = None,
        *,
        annotation: Optional[warehouse.Annotation] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Annotation:
        r"""Updates annotation inside asset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_update_annotation():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.UpdateAnnotationRequest(
                )

                # Make the request
                response = client.update_annotation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UpdateAnnotationRequest, dict]):
                The request object. Request message for UpdateAnnotation
                API.
            annotation (google.cloud.visionai_v1.types.Annotation):
                Required. The annotation to update. The annotation's
                ``name`` field is used to identify the annotation to be
                updated. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/assets/{asset}/annotations/{annotation}``

                This corresponds to the ``annotation`` field
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
            google.cloud.visionai_v1.types.Annotation:
                An annotation is a resource in asset.
                It represents a key-value mapping of
                content in asset.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([annotation, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UpdateAnnotationRequest):
            request = warehouse.UpdateAnnotationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if annotation is not None:
                request.annotation = annotation
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_annotation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("annotation.name", request.annotation.name),)
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

    def delete_annotation(
        self,
        request: Optional[Union[warehouse.DeleteAnnotationRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes annotation inside asset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_delete_annotation():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.DeleteAnnotationRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_annotation(request=request)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeleteAnnotationRequest, dict]):
                The request object. Request message for DeleteAnnotation
                API.
            name (str):
                Required. The name of the annotation to delete. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/assets/{asset}/annotations/{annotation}``

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
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.DeleteAnnotationRequest):
            request = warehouse.DeleteAnnotationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_annotation]

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

    def ingest_asset(
        self,
        requests: Optional[Iterator[warehouse.IngestAssetRequest]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[warehouse.IngestAssetResponse]:
        r"""Ingests data for the asset. It is not allowed to
        ingest a data chunk which is already expired according
        to TTL. This method is only available via the gRPC API
        (not HTTP since bi-directional streaming is not
        supported via HTTP).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_ingest_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                config = visionai_v1.Config()
                config.asset = "asset_value"

                request = visionai_v1.IngestAssetRequest(
                    config=config,
                )

                # This method expects an iterator which contains
                # 'visionai_v1.IngestAssetRequest' objects
                # Here we create a generator that yields a single `request` for
                # demonstrative purposes.
                requests = [request]

                def request_generator():
                    for request in requests:
                        yield request

                # Make the request
                stream = client.ingest_asset(requests=request_generator())

                # Handle the response
                for response in stream:
                    print(response)

        Args:
            requests (Iterator[google.cloud.visionai_v1.types.IngestAssetRequest]):
                The request object iterator. Request message for IngestAsset API.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.cloud.visionai_v1.types.IngestAssetResponse]:
                Response message for IngestAsset API.
        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.ingest_asset]

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

    def clip_asset(
        self,
        request: Optional[Union[warehouse.ClipAssetRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.ClipAssetResponse:
        r"""Supported by STREAM_VIDEO corpus type. Generates clips for
        downloading. The api takes in a time range, and generates a clip
        of the first content available after start_time and before
        end_time, which may overflow beyond these bounds. Returned clips
        are truncated if the total size of the clips are larger than
        100MB.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_clip_asset():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ClipAssetRequest(
                    name="name_value",
                )

                # Make the request
                response = client.clip_asset(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ClipAssetRequest, dict]):
                The request object. Request message for ClipAsset API.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.ClipAssetResponse:
                Response message for ClipAsset API.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.ClipAssetRequest):
            request = warehouse.ClipAssetRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.clip_asset]

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

    def generate_hls_uri(
        self,
        request: Optional[Union[warehouse.GenerateHlsUriRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.GenerateHlsUriResponse:
        r"""Generates a uri for an HLS manifest. The api takes in
        a collection of time ranges, and generates a URI for an
        HLS manifest that covers all the requested time ranges.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_generate_hls_uri():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GenerateHlsUriRequest(
                    name="name_value",
                )

                # Make the request
                response = client.generate_hls_uri(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GenerateHlsUriRequest, dict]):
                The request object. Request message for GenerateHlsUri
                API.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.GenerateHlsUriResponse:
                Response message for GenerateHlsUri
                API.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.GenerateHlsUriRequest):
            request = warehouse.GenerateHlsUriRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.generate_hls_uri]

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

    def import_assets(
        self,
        request: Optional[Union[warehouse.ImportAssetsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Imports assets (images plus annotations) from a meta
        file on cloud storage. Each row in the meta file is
        corresponding to an image (specified by a cloud storage
        uri) and its annotations.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_import_assets():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ImportAssetsRequest(
                    assets_gcs_uri="assets_gcs_uri_value",
                    parent="parent_value",
                )

                # Make the request
                operation = client.import_assets(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ImportAssetsRequest, dict]):
                The request object. The request message for ImportAssets.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.visionai_v1.types.ImportAssetsResponse`
                The response message for ImportAssets LRO.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.ImportAssetsRequest):
            request = warehouse.ImportAssetsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.import_assets]

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
            warehouse.ImportAssetsResponse,
            metadata_type=warehouse.ImportAssetsMetadata,
        )

        # Done; return the response.
        return response

    def create_search_config(
        self,
        request: Optional[Union[warehouse.CreateSearchConfigRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        search_config: Optional[warehouse.SearchConfig] = None,
        search_config_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.SearchConfig:
        r"""Creates a search configuration inside a corpus.

        Please follow the rules below to create a valid
        CreateSearchConfigRequest. --- General Rules ---

        1. Request.search_config_id must not be associated with an
           existing SearchConfig.
        2. Request must contain at least one non-empty
           search_criteria_property or facet_property.
        3. mapped_fields must not be empty, and must map to existing UGA
           keys.
        4. All mapped_fields must be of the same type.
        5. All mapped_fields must share the same granularity.
        6. All mapped_fields must share the same semantic SearchConfig
           match options. For property-specific rules, please reference
           the comments for FacetProperty and SearchCriteriaProperty.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_create_search_config():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.CreateSearchConfigRequest(
                    parent="parent_value",
                    search_config_id="search_config_id_value",
                )

                # Make the request
                response = client.create_search_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.CreateSearchConfigRequest, dict]):
                The request object. Request message for
                CreateSearchConfig.
            parent (str):
                Required. The parent resource where this search
                configuration will be created. Format:
                ``projects/{project_number}/locations/{location_id}/corpora/{corpus_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            search_config (google.cloud.visionai_v1.types.SearchConfig):
                Required. The search config to
                create.

                This corresponds to the ``search_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            search_config_id (str):
                Required. ID to use for the new search config. Will
                become the final component of the SearchConfig's
                resource name. This value should be up to 63 characters,
                and valid characters are /[a-z][0-9]-_/. The first
                character must be a letter, the last could be a letter
                or a number.

                This corresponds to the ``search_config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.SearchConfig:
                SearchConfig stores different
                properties that will affect search
                behaviors and search results.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, search_config, search_config_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.CreateSearchConfigRequest):
            request = warehouse.CreateSearchConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if search_config is not None:
                request.search_config = search_config
            if search_config_id is not None:
                request.search_config_id = search_config_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_search_config]

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

        # Done; return the response.
        return response

    def update_search_config(
        self,
        request: Optional[Union[warehouse.UpdateSearchConfigRequest, dict]] = None,
        *,
        search_config: Optional[warehouse.SearchConfig] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.SearchConfig:
        r"""Updates a search configuration inside a corpus.

        Please follow the rules below to create a valid
        UpdateSearchConfigRequest. --- General Rules ---

        1. Request.search_configuration.name must already exist.
        2. Request must contain at least one non-empty
           search_criteria_property or facet_property.
        3. mapped_fields must not be empty, and must map to existing UGA
           keys.
        4. All mapped_fields must be of the same type.
        5. All mapped_fields must share the same granularity.
        6. All mapped_fields must share the same semantic SearchConfig
           match options. For property-specific rules, please reference
           the comments for FacetProperty and SearchCriteriaProperty.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_update_search_config():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.UpdateSearchConfigRequest(
                )

                # Make the request
                response = client.update_search_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UpdateSearchConfigRequest, dict]):
                The request object. Request message for
                UpdateSearchConfig.
            search_config (google.cloud.visionai_v1.types.SearchConfig):
                Required. The search configuration to update.

                The search configuration's ``name`` field is used to
                identify the resource to be updated. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/searchConfigs/{search_config}``

                This corresponds to the ``search_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated. If
                left unset, all field paths will be
                updated/overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.SearchConfig:
                SearchConfig stores different
                properties that will affect search
                behaviors and search results.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([search_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UpdateSearchConfigRequest):
            request = warehouse.UpdateSearchConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if search_config is not None:
                request.search_config = search_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_search_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("search_config.name", request.search_config.name),)
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

    def get_search_config(
        self,
        request: Optional[Union[warehouse.GetSearchConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.SearchConfig:
        r"""Gets a search configuration inside a corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_get_search_config():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GetSearchConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_search_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GetSearchConfigRequest, dict]):
                The request object. Request message for GetSearchConfig.
            name (str):
                Required. The name of the search configuration to
                retrieve. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/searchConfigs/{search_config}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.SearchConfig:
                SearchConfig stores different
                properties that will affect search
                behaviors and search results.

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
        if not isinstance(request, warehouse.GetSearchConfigRequest):
            request = warehouse.GetSearchConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_search_config]

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

    def delete_search_config(
        self,
        request: Optional[Union[warehouse.DeleteSearchConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a search configuration inside a corpus.

        For a DeleteSearchConfigRequest to be valid,
        Request.search_configuration.name must already exist.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_delete_search_config():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.DeleteSearchConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_search_config(request=request)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeleteSearchConfigRequest, dict]):
                The request object. Request message for
                DeleteSearchConfig.
            name (str):
                Required. The name of the search configuration to
                delete. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/searchConfigs/{search_config}``

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
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.DeleteSearchConfigRequest):
            request = warehouse.DeleteSearchConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_search_config]

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

    def list_search_configs(
        self,
        request: Optional[Union[warehouse.ListSearchConfigsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSearchConfigsPager:
        r"""Lists all search configurations inside a corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_list_search_configs():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ListSearchConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_search_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ListSearchConfigsRequest, dict]):
                The request object. Request message for
                ListSearchConfigs.
            parent (str):
                Required. The parent, which owns this collection of
                search configurations. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ListSearchConfigsPager:
                Response message for
                ListSearchConfigs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        if not isinstance(request, warehouse.ListSearchConfigsRequest):
            request = warehouse.ListSearchConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_search_configs]

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
        response = pagers.ListSearchConfigsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_search_hypernym(
        self,
        request: Optional[Union[warehouse.CreateSearchHypernymRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        search_hypernym: Optional[warehouse.SearchHypernym] = None,
        search_hypernym_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.SearchHypernym:
        r"""Creates a SearchHypernym inside a corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_create_search_hypernym():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.CreateSearchHypernymRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_search_hypernym(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.CreateSearchHypernymRequest, dict]):
                The request object. Request message for creating
                SearchHypernym.
            parent (str):
                Required. The parent resource where this SearchHypernym
                will be created. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            search_hypernym (google.cloud.visionai_v1.types.SearchHypernym):
                Required. The SearchHypernym to
                create.

                This corresponds to the ``search_hypernym`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            search_hypernym_id (str):
                Optional. The search hypernym id.
                If omitted, a random UUID will be
                generated.

                This corresponds to the ``search_hypernym_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.SearchHypernym:
                Search resource: SearchHypernym.
                   For example, { hypernym: "vehicle" hyponyms:
                   ["sedan", "truck"] } This means in SMART_SEARCH mode,
                   searching for "vehicle" will also return results with
                   "sedan" or "truck" as annotations.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, search_hypernym, search_hypernym_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.CreateSearchHypernymRequest):
            request = warehouse.CreateSearchHypernymRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if search_hypernym is not None:
                request.search_hypernym = search_hypernym
            if search_hypernym_id is not None:
                request.search_hypernym_id = search_hypernym_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_search_hypernym]

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

        # Done; return the response.
        return response

    def update_search_hypernym(
        self,
        request: Optional[Union[warehouse.UpdateSearchHypernymRequest, dict]] = None,
        *,
        search_hypernym: Optional[warehouse.SearchHypernym] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.SearchHypernym:
        r"""Updates a SearchHypernym inside a corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_update_search_hypernym():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.UpdateSearchHypernymRequest(
                )

                # Make the request
                response = client.update_search_hypernym(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UpdateSearchHypernymRequest, dict]):
                The request object. Request message for updating
                SearchHypernym.
            search_hypernym (google.cloud.visionai_v1.types.SearchHypernym):
                Required. The SearchHypernym to update. The search
                hypernym's ``name`` field is used to identify the search
                hypernym to be updated. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/searchHypernyms/{search_hypernym}``

                This corresponds to the ``search_hypernym`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated. If
                left unset, all field paths will be
                updated/overwritten.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.SearchHypernym:
                Search resource: SearchHypernym.
                   For example, { hypernym: "vehicle" hyponyms:
                   ["sedan", "truck"] } This means in SMART_SEARCH mode,
                   searching for "vehicle" will also return results with
                   "sedan" or "truck" as annotations.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([search_hypernym, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UpdateSearchHypernymRequest):
            request = warehouse.UpdateSearchHypernymRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if search_hypernym is not None:
                request.search_hypernym = search_hypernym
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_search_hypernym]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("search_hypernym.name", request.search_hypernym.name),)
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

    def get_search_hypernym(
        self,
        request: Optional[Union[warehouse.GetSearchHypernymRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.SearchHypernym:
        r"""Gets a SearchHypernym inside a corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_get_search_hypernym():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GetSearchHypernymRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_search_hypernym(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GetSearchHypernymRequest, dict]):
                The request object. Request message for getting
                SearchHypernym.
            name (str):
                Required. The name of the SearchHypernym to retrieve.
                Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/searchHypernyms/{search_hypernym}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.SearchHypernym:
                Search resource: SearchHypernym.
                   For example, { hypernym: "vehicle" hyponyms:
                   ["sedan", "truck"] } This means in SMART_SEARCH mode,
                   searching for "vehicle" will also return results with
                   "sedan" or "truck" as annotations.

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
        if not isinstance(request, warehouse.GetSearchHypernymRequest):
            request = warehouse.GetSearchHypernymRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_search_hypernym]

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

    def delete_search_hypernym(
        self,
        request: Optional[Union[warehouse.DeleteSearchHypernymRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a SearchHypernym inside a corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_delete_search_hypernym():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.DeleteSearchHypernymRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_search_hypernym(request=request)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeleteSearchHypernymRequest, dict]):
                The request object. Request message for deleting
                SearchHypernym.
            name (str):
                Required. The name of the SearchHypernym to delete.
                Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/searchHypernyms/{search_hypernym}``

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
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.DeleteSearchHypernymRequest):
            request = warehouse.DeleteSearchHypernymRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_search_hypernym]

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

    def list_search_hypernyms(
        self,
        request: Optional[Union[warehouse.ListSearchHypernymsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSearchHypernymsPager:
        r"""Lists SearchHypernyms inside a corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_list_search_hypernyms():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ListSearchHypernymsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_search_hypernyms(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ListSearchHypernymsRequest, dict]):
                The request object. Request message for listing
                SearchHypernyms.
            parent (str):
                Required. The parent, which owns this collection of
                SearchHypernyms. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ListSearchHypernymsPager:
                Response message for listing
                SearchHypernyms.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        if not isinstance(request, warehouse.ListSearchHypernymsRequest):
            request = warehouse.ListSearchHypernymsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_search_hypernyms]

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
        response = pagers.ListSearchHypernymsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_assets(
        self,
        request: Optional[Union[warehouse.SearchAssetsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchAssetsPager:
        r"""Search media asset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_search_assets():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.SearchAssetsRequest(
                    corpus="corpus_value",
                )

                # Make the request
                page_result = client.search_assets(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.SearchAssetsRequest, dict]):
                The request object. Request message for SearchAssets.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.SearchAssetsPager:
                Response message for SearchAssets.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.SearchAssetsRequest):
            request = warehouse.SearchAssetsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_assets]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("corpus", request.corpus),)),
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
        response = pagers.SearchAssetsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_index_endpoint(
        self,
        request: Optional[Union[warehouse.SearchIndexEndpointRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchIndexEndpointPager:
        r"""Search a deployed index endpoint (IMAGE corpus type
        only).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_search_index_endpoint():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                image_query = visionai_v1.ImageQuery()
                image_query.input_image = b'input_image_blob'

                request = visionai_v1.SearchIndexEndpointRequest(
                    image_query=image_query,
                    index_endpoint="index_endpoint_value",
                )

                # Make the request
                page_result = client.search_index_endpoint(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.SearchIndexEndpointRequest, dict]):
                The request object. Request message for
                SearchIndexEndpoint.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.SearchIndexEndpointPager:
                Response message for
                SearchIndexEndpoint.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.SearchIndexEndpointRequest):
            request = warehouse.SearchIndexEndpointRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_index_endpoint]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("index_endpoint", request.index_endpoint),)
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
        response = pagers.SearchIndexEndpointPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_index_endpoint(
        self,
        request: Optional[Union[warehouse.CreateIndexEndpointRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        index_endpoint: Optional[warehouse.IndexEndpoint] = None,
        index_endpoint_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates an IndexEndpoint.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_create_index_endpoint():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.CreateIndexEndpointRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_index_endpoint(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.CreateIndexEndpointRequest, dict]):
                The request object. Request message for
                CreateIndexEndpoint.
            parent (str):
                Required. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            index_endpoint (google.cloud.visionai_v1.types.IndexEndpoint):
                Required. The resource being created.
                This corresponds to the ``index_endpoint`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            index_endpoint_id (str):
                Optional. The ID to use for the
                IndexEndpoint, which will become the
                final component of the IndexEndpoint's
                resource name if the user specifies it.
                Otherwise, IndexEndpoint id will be
                autogenerated.

                This value should be up to 63
                characters, and valid characters are
                a-z, 0-9 and dash (-). The first
                character must be a letter, the last
                must be a letter or a number.

                This corresponds to the ``index_endpoint_id`` field
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
                :class:`google.cloud.visionai_v1.types.IndexEndpoint`
                Message representing IndexEndpoint resource. Indexes are
                deployed into it.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, index_endpoint, index_endpoint_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.CreateIndexEndpointRequest):
            request = warehouse.CreateIndexEndpointRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if index_endpoint is not None:
                request.index_endpoint = index_endpoint
            if index_endpoint_id is not None:
                request.index_endpoint_id = index_endpoint_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_index_endpoint]

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
            warehouse.IndexEndpoint,
            metadata_type=warehouse.CreateIndexEndpointMetadata,
        )

        # Done; return the response.
        return response

    def get_index_endpoint(
        self,
        request: Optional[Union[warehouse.GetIndexEndpointRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.IndexEndpoint:
        r"""Gets an IndexEndpoint.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_get_index_endpoint():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GetIndexEndpointRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_index_endpoint(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GetIndexEndpointRequest, dict]):
                The request object. Request message for GetIndexEndpoint.
            name (str):
                Required. Name of the IndexEndpoint
                resource.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.IndexEndpoint:
                Message representing IndexEndpoint
                resource. Indexes are deployed into it.

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
        if not isinstance(request, warehouse.GetIndexEndpointRequest):
            request = warehouse.GetIndexEndpointRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_index_endpoint]

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

    def list_index_endpoints(
        self,
        request: Optional[Union[warehouse.ListIndexEndpointsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListIndexEndpointsPager:
        r"""Lists all IndexEndpoints in a project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_list_index_endpoints():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ListIndexEndpointsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_index_endpoints(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ListIndexEndpointsRequest, dict]):
                The request object. Request message for
                ListIndexEndpoints.
            parent (str):
                Required. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ListIndexEndpointsPager:
                Response message for
                ListIndexEndpoints.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        if not isinstance(request, warehouse.ListIndexEndpointsRequest):
            request = warehouse.ListIndexEndpointsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_index_endpoints]

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
        response = pagers.ListIndexEndpointsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_index_endpoint(
        self,
        request: Optional[Union[warehouse.UpdateIndexEndpointRequest, dict]] = None,
        *,
        index_endpoint: Optional[warehouse.IndexEndpoint] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates an IndexEndpoint.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_update_index_endpoint():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.UpdateIndexEndpointRequest(
                )

                # Make the request
                operation = client.update_index_endpoint(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UpdateIndexEndpointRequest, dict]):
                The request object. Request message for
                UpdateIndexEndpoint.
            index_endpoint (google.cloud.visionai_v1.types.IndexEndpoint):
                Required. The resource being updated.
                This corresponds to the ``index_endpoint`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to specify the fields to be
                overwritten in the IndexEndpoint resource by the update.
                The fields specified in the update_mask are relative to
                the resource, not the full request. A field of the
                resource will be overwritten if it is in the mask. Empty
                field mask is not allowed. If the mask is "*", then this
                is a full replacement of the resource.

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
                :class:`google.cloud.visionai_v1.types.IndexEndpoint`
                Message representing IndexEndpoint resource. Indexes are
                deployed into it.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([index_endpoint, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UpdateIndexEndpointRequest):
            request = warehouse.UpdateIndexEndpointRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if index_endpoint is not None:
                request.index_endpoint = index_endpoint
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_index_endpoint]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("index_endpoint.name", request.index_endpoint.name),)
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
            warehouse.IndexEndpoint,
            metadata_type=warehouse.UpdateIndexEndpointMetadata,
        )

        # Done; return the response.
        return response

    def delete_index_endpoint(
        self,
        request: Optional[Union[warehouse.DeleteIndexEndpointRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes an IndexEndpoint.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_delete_index_endpoint():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.DeleteIndexEndpointRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_index_endpoint(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeleteIndexEndpointRequest, dict]):
                The request object. Request message for
                DeleteIndexEndpoint.
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

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

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
        if not isinstance(request, warehouse.DeleteIndexEndpointRequest):
            request = warehouse.DeleteIndexEndpointRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_index_endpoint]

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
            empty_pb2.Empty,
            metadata_type=warehouse.DeleteIndexEndpointMetadata,
        )

        # Done; return the response.
        return response

    def deploy_index(
        self,
        request: Optional[Union[warehouse.DeployIndexRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deploys an Index to IndexEndpoint.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_deploy_index():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                deployed_index = visionai_v1.DeployedIndex()
                deployed_index.index = "index_value"

                request = visionai_v1.DeployIndexRequest(
                    index_endpoint="index_endpoint_value",
                    deployed_index=deployed_index,
                )

                # Make the request
                operation = client.deploy_index(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeployIndexRequest, dict]):
                The request object. Request message for DeployIndex.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.visionai_v1.types.DeployIndexResponse`
                DeployIndex response once the operation is done.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.DeployIndexRequest):
            request = warehouse.DeployIndexRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.deploy_index]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("index_endpoint", request.index_endpoint),)
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
            warehouse.DeployIndexResponse,
            metadata_type=warehouse.DeployIndexMetadata,
        )

        # Done; return the response.
        return response

    def undeploy_index(
        self,
        request: Optional[Union[warehouse.UndeployIndexRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Undeploys an Index from IndexEndpoint.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_undeploy_index():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.UndeployIndexRequest(
                    index_endpoint="index_endpoint_value",
                )

                # Make the request
                operation = client.undeploy_index(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UndeployIndexRequest, dict]):
                The request object. Request message for
                UndeployIndexEndpoint.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.visionai_v1.types.UndeployIndexResponse`
                UndeployIndex response once the operation is done.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UndeployIndexRequest):
            request = warehouse.UndeployIndexRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.undeploy_index]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("index_endpoint", request.index_endpoint),)
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
            warehouse.UndeployIndexResponse,
            metadata_type=warehouse.UndeployIndexMetadata,
        )

        # Done; return the response.
        return response

    def create_collection(
        self,
        request: Optional[Union[warehouse.CreateCollectionRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        collection: Optional[warehouse.Collection] = None,
        collection_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_create_collection():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.CreateCollectionRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_collection(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.CreateCollectionRequest, dict]):
                The request object. Request message for CreateCollection.
            parent (str):
                Required. The parent resource where this collection will
                be created. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            collection (google.cloud.visionai_v1.types.Collection):
                Required. The collection resource to
                be created.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            collection_id (str):
                Optional. The ID to use for the collection, which will
                become the final component of the resource name if user
                choose to specify. Otherwise, collection id will be
                generated by system.

                This value should be up to 55 characters, and valid
                characters are /[a-z][0-9]-/. The first character must
                be a letter, the last could be a letter or a number.

                This corresponds to the ``collection_id`` field
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

                The result type for the operation will be :class:`google.cloud.visionai_v1.types.Collection` A collection is a resource in a corpus. It serves as a container of
                   references to original resources.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, collection, collection_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.CreateCollectionRequest):
            request = warehouse.CreateCollectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if collection is not None:
                request.collection = collection
            if collection_id is not None:
                request.collection_id = collection_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_collection]

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
            warehouse.Collection,
            metadata_type=warehouse.CreateCollectionMetadata,
        )

        # Done; return the response.
        return response

    def delete_collection(
        self,
        request: Optional[Union[warehouse.DeleteCollectionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_delete_collection():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.DeleteCollectionRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_collection(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.DeleteCollectionRequest, dict]):
                The request object. Request message for
                DeleteCollectionRequest.
            name (str):
                Required. The name of the collection to delete. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/collections/{collection}``

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

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

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
        if not isinstance(request, warehouse.DeleteCollectionRequest):
            request = warehouse.DeleteCollectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_collection]

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
            empty_pb2.Empty,
            metadata_type=warehouse.DeleteCollectionMetadata,
        )

        # Done; return the response.
        return response

    def get_collection(
        self,
        request: Optional[Union[warehouse.GetCollectionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Collection:
        r"""Gets a collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_get_collection():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.GetCollectionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_collection(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.GetCollectionRequest, dict]):
                The request object. Request message for
                GetCollectionRequest.
            name (str):
                Required. The name of the collection to retrieve.
                Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/collections/{collection}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.Collection:
                A collection is a resource in a
                corpus. It serves as a container of
                references to original resources.

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
        if not isinstance(request, warehouse.GetCollectionRequest):
            request = warehouse.GetCollectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_collection]

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

    def update_collection(
        self,
        request: Optional[Union[warehouse.UpdateCollectionRequest, dict]] = None,
        *,
        collection: Optional[warehouse.Collection] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.Collection:
        r"""Updates a collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_update_collection():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.UpdateCollectionRequest(
                )

                # Make the request
                response = client.update_collection(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.UpdateCollectionRequest, dict]):
                The request object. Request message for
                UpdateCollectionRequest.
            collection (google.cloud.visionai_v1.types.Collection):
                Required. The collection to update.

                The collection's ``name`` field is used to identify the
                collection to be updated. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/collections/{collection}``

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated.

                -  Unset ``update_mask`` or set ``update_mask`` to be a
                   single "*" only will update all updatable fields with
                   the value provided in ``collection``.
                -  To update ``display_name`` value to empty string, set
                   it in the ``collection`` to empty string, and set
                   ``update_mask`` with "display_name". Same applies to
                   other updatable string fields in the ``collection``.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.Collection:
                A collection is a resource in a
                corpus. It serves as a container of
                references to original resources.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.UpdateCollectionRequest):
            request = warehouse.UpdateCollectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if collection is not None:
                request.collection = collection
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_collection]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("collection.name", request.collection.name),)
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

    def list_collections(
        self,
        request: Optional[Union[warehouse.ListCollectionsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCollectionsPager:
        r"""Lists collections inside a corpus.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_list_collections():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ListCollectionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_collections(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ListCollectionsRequest, dict]):
                The request object. Request message for ListCollections.
            parent (str):
                Required. The parent corpus. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ListCollectionsPager:
                Response message for ListCollections.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        if not isinstance(request, warehouse.ListCollectionsRequest):
            request = warehouse.ListCollectionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_collections]

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
        response = pagers.ListCollectionsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def add_collection_item(
        self,
        request: Optional[Union[warehouse.AddCollectionItemRequest, dict]] = None,
        *,
        item: Optional[warehouse.CollectionItem] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.AddCollectionItemResponse:
        r"""Adds an item into a Collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_add_collection_item():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                item = visionai_v1.CollectionItem()
                item.collection = "collection_value"
                item.type_ = "ASSET"
                item.item_resource = "item_resource_value"

                request = visionai_v1.AddCollectionItemRequest(
                    item=item,
                )

                # Make the request
                response = client.add_collection_item(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.AddCollectionItemRequest, dict]):
                The request object. Request message for
                AddCollectionItem.
            item (google.cloud.visionai_v1.types.CollectionItem):
                Required. The item to be added.
                This corresponds to the ``item`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.AddCollectionItemResponse:
                Response message for
                AddCollectionItem.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([item])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.AddCollectionItemRequest):
            request = warehouse.AddCollectionItemRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if item is not None:
                request.item = item

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.add_collection_item]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("item.collection", request.item.collection),)
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

    def remove_collection_item(
        self,
        request: Optional[Union[warehouse.RemoveCollectionItemRequest, dict]] = None,
        *,
        item: Optional[warehouse.CollectionItem] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> warehouse.RemoveCollectionItemResponse:
        r"""Removes an item from a collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_remove_collection_item():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                item = visionai_v1.CollectionItem()
                item.collection = "collection_value"
                item.type_ = "ASSET"
                item.item_resource = "item_resource_value"

                request = visionai_v1.RemoveCollectionItemRequest(
                    item=item,
                )

                # Make the request
                response = client.remove_collection_item(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.RemoveCollectionItemRequest, dict]):
                The request object. Request message for
                RemoveCollectionItem.
            item (google.cloud.visionai_v1.types.CollectionItem):
                Required. The item to be removed.
                This corresponds to the ``item`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.types.RemoveCollectionItemResponse:
                Request message for
                RemoveCollectionItem.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([item])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.RemoveCollectionItemRequest):
            request = warehouse.RemoveCollectionItemRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if item is not None:
                request.item = item

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.remove_collection_item]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("item.collection", request.item.collection),)
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

    def view_collection_items(
        self,
        request: Optional[Union[warehouse.ViewCollectionItemsRequest, dict]] = None,
        *,
        collection: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ViewCollectionItemsPager:
        r"""View items inside a collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import visionai_v1

            def sample_view_collection_items():
                # Create a client
                client = visionai_v1.WarehouseClient()

                # Initialize request argument(s)
                request = visionai_v1.ViewCollectionItemsRequest(
                    collection="collection_value",
                )

                # Make the request
                page_result = client.view_collection_items(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.visionai_v1.types.ViewCollectionItemsRequest, dict]):
                The request object. Request message for
                ViewCollectionItems.
            collection (str):
                Required. The collection to view. Format:
                ``projects/{project_number}/locations/{location}/corpora/{corpus}/collections/{collection}``

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.visionai_v1.services.warehouse.pagers.ViewCollectionItemsPager:
                Response message for
                ViewCollectionItems.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, warehouse.ViewCollectionItemsRequest):
            request = warehouse.ViewCollectionItemsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if collection is not None:
                request.collection = collection

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.view_collection_items]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("collection", request.collection),)
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
        response = pagers.ViewCollectionItemsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "WarehouseClient":
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


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("WarehouseClient",)
