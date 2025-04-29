# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from http import HTTPStatus
import json
import logging as std_logging
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
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.oracledatabase_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.oracledatabase_v1.services.oracle_database import pagers
from google.cloud.oracledatabase_v1.types import (
    autonomous_database_character_set,
    autonomous_db_backup,
    autonomous_db_version,
    db_node,
    db_server,
    db_system_shape,
    entitlement,
    exadata_infra,
    gi_version,
    oracledatabase,
    vm_cluster,
)
from google.cloud.oracledatabase_v1.types import (
    autonomous_database as gco_autonomous_database,
)
from google.cloud.oracledatabase_v1.types import autonomous_database

from .transports.base import DEFAULT_CLIENT_INFO, OracleDatabaseTransport
from .transports.grpc import OracleDatabaseGrpcTransport
from .transports.grpc_asyncio import OracleDatabaseGrpcAsyncIOTransport
from .transports.rest import OracleDatabaseRestTransport


class OracleDatabaseClientMeta(type):
    """Metaclass for the OracleDatabase client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[OracleDatabaseTransport]]
    _transport_registry["grpc"] = OracleDatabaseGrpcTransport
    _transport_registry["grpc_asyncio"] = OracleDatabaseGrpcAsyncIOTransport
    _transport_registry["rest"] = OracleDatabaseRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[OracleDatabaseTransport]:
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


class OracleDatabaseClient(metaclass=OracleDatabaseClientMeta):
    """Service describing handlers for resources"""

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
    DEFAULT_ENDPOINT = "oracledatabase.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "oracledatabase.{UNIVERSE_DOMAIN}"
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
            OracleDatabaseClient: The constructed client.
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
            OracleDatabaseClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> OracleDatabaseTransport:
        """Returns the transport used by the client instance.

        Returns:
            OracleDatabaseTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def autonomous_database_path(
        project: str,
        location: str,
        autonomous_database: str,
    ) -> str:
        """Returns a fully-qualified autonomous_database string."""
        return "projects/{project}/locations/{location}/autonomousDatabases/{autonomous_database}".format(
            project=project,
            location=location,
            autonomous_database=autonomous_database,
        )

    @staticmethod
    def parse_autonomous_database_path(path: str) -> Dict[str, str]:
        """Parses a autonomous_database path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/autonomousDatabases/(?P<autonomous_database>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def autonomous_database_backup_path(
        project: str,
        location: str,
        autonomous_database_backup: str,
    ) -> str:
        """Returns a fully-qualified autonomous_database_backup string."""
        return "projects/{project}/locations/{location}/autonomousDatabaseBackups/{autonomous_database_backup}".format(
            project=project,
            location=location,
            autonomous_database_backup=autonomous_database_backup,
        )

    @staticmethod
    def parse_autonomous_database_backup_path(path: str) -> Dict[str, str]:
        """Parses a autonomous_database_backup path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/autonomousDatabaseBackups/(?P<autonomous_database_backup>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def autonomous_database_character_set_path(
        project: str,
        location: str,
        autonomous_database_character_set: str,
    ) -> str:
        """Returns a fully-qualified autonomous_database_character_set string."""
        return "projects/{project}/locations/{location}/autonomousDatabaseCharacterSets/{autonomous_database_character_set}".format(
            project=project,
            location=location,
            autonomous_database_character_set=autonomous_database_character_set,
        )

    @staticmethod
    def parse_autonomous_database_character_set_path(path: str) -> Dict[str, str]:
        """Parses a autonomous_database_character_set path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/autonomousDatabaseCharacterSets/(?P<autonomous_database_character_set>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def autonomous_db_version_path(
        project: str,
        location: str,
        autonomous_db_version: str,
    ) -> str:
        """Returns a fully-qualified autonomous_db_version string."""
        return "projects/{project}/locations/{location}/autonomousDbVersions/{autonomous_db_version}".format(
            project=project,
            location=location,
            autonomous_db_version=autonomous_db_version,
        )

    @staticmethod
    def parse_autonomous_db_version_path(path: str) -> Dict[str, str]:
        """Parses a autonomous_db_version path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/autonomousDbVersions/(?P<autonomous_db_version>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def cloud_exadata_infrastructure_path(
        project: str,
        location: str,
        cloud_exadata_infrastructure: str,
    ) -> str:
        """Returns a fully-qualified cloud_exadata_infrastructure string."""
        return "projects/{project}/locations/{location}/cloudExadataInfrastructures/{cloud_exadata_infrastructure}".format(
            project=project,
            location=location,
            cloud_exadata_infrastructure=cloud_exadata_infrastructure,
        )

    @staticmethod
    def parse_cloud_exadata_infrastructure_path(path: str) -> Dict[str, str]:
        """Parses a cloud_exadata_infrastructure path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/cloudExadataInfrastructures/(?P<cloud_exadata_infrastructure>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def cloud_vm_cluster_path(
        project: str,
        location: str,
        cloud_vm_cluster: str,
    ) -> str:
        """Returns a fully-qualified cloud_vm_cluster string."""
        return "projects/{project}/locations/{location}/cloudVmClusters/{cloud_vm_cluster}".format(
            project=project,
            location=location,
            cloud_vm_cluster=cloud_vm_cluster,
        )

    @staticmethod
    def parse_cloud_vm_cluster_path(path: str) -> Dict[str, str]:
        """Parses a cloud_vm_cluster path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/cloudVmClusters/(?P<cloud_vm_cluster>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def db_node_path(
        project: str,
        location: str,
        cloud_vm_cluster: str,
        db_node: str,
    ) -> str:
        """Returns a fully-qualified db_node string."""
        return "projects/{project}/locations/{location}/cloudVmClusters/{cloud_vm_cluster}/dbNodes/{db_node}".format(
            project=project,
            location=location,
            cloud_vm_cluster=cloud_vm_cluster,
            db_node=db_node,
        )

    @staticmethod
    def parse_db_node_path(path: str) -> Dict[str, str]:
        """Parses a db_node path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/cloudVmClusters/(?P<cloud_vm_cluster>.+?)/dbNodes/(?P<db_node>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def db_server_path(
        project: str,
        location: str,
        cloud_exadata_infrastructure: str,
        db_server: str,
    ) -> str:
        """Returns a fully-qualified db_server string."""
        return "projects/{project}/locations/{location}/cloudExadataInfrastructures/{cloud_exadata_infrastructure}/dbServers/{db_server}".format(
            project=project,
            location=location,
            cloud_exadata_infrastructure=cloud_exadata_infrastructure,
            db_server=db_server,
        )

    @staticmethod
    def parse_db_server_path(path: str) -> Dict[str, str]:
        """Parses a db_server path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/cloudExadataInfrastructures/(?P<cloud_exadata_infrastructure>.+?)/dbServers/(?P<db_server>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def db_system_shape_path(
        project: str,
        location: str,
        db_system_shape: str,
    ) -> str:
        """Returns a fully-qualified db_system_shape string."""
        return "projects/{project}/locations/{location}/dbSystemShapes/{db_system_shape}".format(
            project=project,
            location=location,
            db_system_shape=db_system_shape,
        )

    @staticmethod
    def parse_db_system_shape_path(path: str) -> Dict[str, str]:
        """Parses a db_system_shape path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/dbSystemShapes/(?P<db_system_shape>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def entitlement_path(
        project: str,
        location: str,
        entitlement: str,
    ) -> str:
        """Returns a fully-qualified entitlement string."""
        return (
            "projects/{project}/locations/{location}/entitlements/{entitlement}".format(
                project=project,
                location=location,
                entitlement=entitlement,
            )
        )

    @staticmethod
    def parse_entitlement_path(path: str) -> Dict[str, str]:
        """Parses a entitlement path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/entitlements/(?P<entitlement>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def gi_version_path(
        project: str,
        location: str,
        gi_version: str,
    ) -> str:
        """Returns a fully-qualified gi_version string."""
        return "projects/{project}/locations/{location}/giVersions/{gi_version}".format(
            project=project,
            location=location,
            gi_version=gi_version,
        )

    @staticmethod
    def parse_gi_version_path(path: str) -> Dict[str, str]:
        """Parses a gi_version path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/giVersions/(?P<gi_version>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def network_path(
        project: str,
        network: str,
    ) -> str:
        """Returns a fully-qualified network string."""
        return "projects/{project}/global/networks/{network}".format(
            project=project,
            network=network,
        )

    @staticmethod
    def parse_network_path(path: str) -> Dict[str, str]:
        """Parses a network path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/global/networks/(?P<network>.+?)$", path
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
            _default_universe = OracleDatabaseClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = OracleDatabaseClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = OracleDatabaseClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        universe_domain = OracleDatabaseClient._DEFAULT_UNIVERSE
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

    def _add_cred_info_for_auth_errors(
        self, error: core_exceptions.GoogleAPICallError
    ) -> None:
        """Adds credential info string to error details for 401/403/404 errors.

        Args:
            error (google.api_core.exceptions.GoogleAPICallError): The error to add the cred info.
        """
        if error.code not in [
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
        ]:
            return

        cred = self._transport._credentials

        # get_cred_info is only available in google-auth>=2.35.0
        if not hasattr(cred, "get_cred_info"):
            return

        # ignore the type check since pypy test fails when get_cred_info
        # is not available
        cred_info = cred.get_cred_info()  # type: ignore
        if cred_info and hasattr(error._details, "append"):
            error._details.append(json.dumps(cred_info))

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
            Union[str, OracleDatabaseTransport, Callable[..., OracleDatabaseTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the oracle database client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,OracleDatabaseTransport,Callable[..., OracleDatabaseTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the OracleDatabaseTransport constructor.
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
        ) = OracleDatabaseClient._read_environment_variables()
        self._client_cert_source = OracleDatabaseClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = OracleDatabaseClient._get_universe_domain(
            universe_domain_opt, self._universe_domain_env
        )
        self._api_endpoint = None  # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        if CLIENT_LOGGING_SUPPORTED:  # pragma: NO COVER
            # Setup logging.
            client_logging.initialize_logging()

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, OracleDatabaseTransport)
        if transport_provided:
            # transport is a OracleDatabaseTransport instance.
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
            self._transport = cast(OracleDatabaseTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or OracleDatabaseClient._get_api_endpoint(
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
                Type[OracleDatabaseTransport], Callable[..., OracleDatabaseTransport]
            ] = (
                OracleDatabaseClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., OracleDatabaseTransport], transport)
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

        if "async" not in str(self._transport):
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                std_logging.DEBUG
            ):  # pragma: NO COVER
                _LOGGER.debug(
                    "Created client `google.cloud.oracledatabase_v1.OracleDatabaseClient`.",
                    extra={
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "universeDomain": getattr(
                            self._transport._credentials, "universe_domain", ""
                        ),
                        "credentialsType": f"{type(self._transport._credentials).__module__}.{type(self._transport._credentials).__qualname__}",
                        "credentialsInfo": getattr(
                            self.transport._credentials, "get_cred_info", lambda: None
                        )(),
                    }
                    if hasattr(self._transport, "_credentials")
                    else {
                        "serviceName": "google.cloud.oracledatabase.v1.OracleDatabase",
                        "credentialsType": None,
                    },
                )

    def list_cloud_exadata_infrastructures(
        self,
        request: Optional[
            Union[oracledatabase.ListCloudExadataInfrastructuresRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListCloudExadataInfrastructuresPager:
        r"""Lists Exadata Infrastructures in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_cloud_exadata_infrastructures():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListCloudExadataInfrastructuresRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_cloud_exadata_infrastructures(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListCloudExadataInfrastructuresRequest, dict]):
                The request object. The request for ``CloudExadataInfrastructures.List``.
            parent (str):
                Required. The parent value for
                CloudExadataInfrastructure in the
                following format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListCloudExadataInfrastructuresPager:
                The response for CloudExadataInfrastructures.list.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, oracledatabase.ListCloudExadataInfrastructuresRequest
        ):
            request = oracledatabase.ListCloudExadataInfrastructuresRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_cloud_exadata_infrastructures
        ]

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
        response = pagers.ListCloudExadataInfrastructuresPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_cloud_exadata_infrastructure(
        self,
        request: Optional[
            Union[oracledatabase.GetCloudExadataInfrastructureRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> exadata_infra.CloudExadataInfrastructure:
        r"""Gets details of a single Exadata Infrastructure.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_get_cloud_exadata_infrastructure():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.GetCloudExadataInfrastructureRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_cloud_exadata_infrastructure(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.GetCloudExadataInfrastructureRequest, dict]):
                The request object. The request for ``CloudExadataInfrastructure.Get``.
            name (str):
                Required. The name of the Cloud Exadata Infrastructure
                in the following format:
                projects/{project}/locations/{location}/cloudExadataInfrastructures/{cloud_exadata_infrastructure}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.types.CloudExadataInfrastructure:
                Represents CloudExadataInfrastructure
                resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/CloudExadataInfrastructure/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.GetCloudExadataInfrastructureRequest):
            request = oracledatabase.GetCloudExadataInfrastructureRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_cloud_exadata_infrastructure
        ]

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

    def create_cloud_exadata_infrastructure(
        self,
        request: Optional[
            Union[oracledatabase.CreateCloudExadataInfrastructureRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        cloud_exadata_infrastructure: Optional[
            exadata_infra.CloudExadataInfrastructure
        ] = None,
        cloud_exadata_infrastructure_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Creates a new Exadata Infrastructure in a given
        project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_create_cloud_exadata_infrastructure():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.CreateCloudExadataInfrastructureRequest(
                    parent="parent_value",
                    cloud_exadata_infrastructure_id="cloud_exadata_infrastructure_id_value",
                )

                # Make the request
                operation = client.create_cloud_exadata_infrastructure(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.CreateCloudExadataInfrastructureRequest, dict]):
                The request object. The request for ``CloudExadataInfrastructure.Create``.
            parent (str):
                Required. The parent value for
                CloudExadataInfrastructure in the
                following format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cloud_exadata_infrastructure (google.cloud.oracledatabase_v1.types.CloudExadataInfrastructure):
                Required. Details of the Exadata
                Infrastructure instance to create.

                This corresponds to the ``cloud_exadata_infrastructure`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cloud_exadata_infrastructure_id (str):
                Required. The ID of the Exadata Infrastructure to
                create. This value is restricted to
                (^`a-z <[a-z0-9-]{0,61}[a-z0-9]>`__?$) and must be a
                maximum of 63 characters in length. The value must start
                with a letter and end with a letter or a number.

                This corresponds to the ``cloud_exadata_infrastructure_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.oracledatabase_v1.types.CloudExadataInfrastructure` Represents CloudExadataInfrastructure resource.
                   https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/CloudExadataInfrastructure/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [
            parent,
            cloud_exadata_infrastructure,
            cloud_exadata_infrastructure_id,
        ]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, oracledatabase.CreateCloudExadataInfrastructureRequest
        ):
            request = oracledatabase.CreateCloudExadataInfrastructureRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if cloud_exadata_infrastructure is not None:
                request.cloud_exadata_infrastructure = cloud_exadata_infrastructure
            if cloud_exadata_infrastructure_id is not None:
                request.cloud_exadata_infrastructure_id = (
                    cloud_exadata_infrastructure_id
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_cloud_exadata_infrastructure
        ]

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
            exadata_infra.CloudExadataInfrastructure,
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_cloud_exadata_infrastructure(
        self,
        request: Optional[
            Union[oracledatabase.DeleteCloudExadataInfrastructureRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Deletes a single Exadata Infrastructure.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_delete_cloud_exadata_infrastructure():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.DeleteCloudExadataInfrastructureRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_cloud_exadata_infrastructure(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.DeleteCloudExadataInfrastructureRequest, dict]):
                The request object. The request for ``CloudExadataInfrastructure.Delete``.
            name (str):
                Required. The name of the Cloud Exadata Infrastructure
                in the following format:
                projects/{project}/locations/{location}/cloudExadataInfrastructures/{cloud_exadata_infrastructure}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

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
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, oracledatabase.DeleteCloudExadataInfrastructureRequest
        ):
            request = oracledatabase.DeleteCloudExadataInfrastructureRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_cloud_exadata_infrastructure
        ]

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
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_cloud_vm_clusters(
        self,
        request: Optional[
            Union[oracledatabase.ListCloudVmClustersRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListCloudVmClustersPager:
        r"""Lists the VM Clusters in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_cloud_vm_clusters():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListCloudVmClustersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_cloud_vm_clusters(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListCloudVmClustersRequest, dict]):
                The request object. The request for ``CloudVmCluster.List``.
            parent (str):
                Required. The name of the parent in
                the following format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListCloudVmClustersPager:
                The response for CloudVmCluster.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.ListCloudVmClustersRequest):
            request = oracledatabase.ListCloudVmClustersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_cloud_vm_clusters]

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
        response = pagers.ListCloudVmClustersPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_cloud_vm_cluster(
        self,
        request: Optional[Union[oracledatabase.GetCloudVmClusterRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> vm_cluster.CloudVmCluster:
        r"""Gets details of a single VM Cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_get_cloud_vm_cluster():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.GetCloudVmClusterRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_cloud_vm_cluster(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.GetCloudVmClusterRequest, dict]):
                The request object. The request for ``CloudVmCluster.Get``.
            name (str):
                Required. The name of the Cloud VM Cluster in the
                following format:
                projects/{project}/locations/{location}/cloudVmClusters/{cloud_vm_cluster}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.types.CloudVmCluster:
                Details of the Cloud VM Cluster
                resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/CloudVmCluster/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.GetCloudVmClusterRequest):
            request = oracledatabase.GetCloudVmClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_cloud_vm_cluster]

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

    def create_cloud_vm_cluster(
        self,
        request: Optional[
            Union[oracledatabase.CreateCloudVmClusterRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        cloud_vm_cluster: Optional[vm_cluster.CloudVmCluster] = None,
        cloud_vm_cluster_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Creates a new VM Cluster in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_create_cloud_vm_cluster():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                cloud_vm_cluster = oracledatabase_v1.CloudVmCluster()
                cloud_vm_cluster.exadata_infrastructure = "exadata_infrastructure_value"
                cloud_vm_cluster.cidr = "cidr_value"
                cloud_vm_cluster.backup_subnet_cidr = "backup_subnet_cidr_value"
                cloud_vm_cluster.network = "network_value"

                request = oracledatabase_v1.CreateCloudVmClusterRequest(
                    parent="parent_value",
                    cloud_vm_cluster_id="cloud_vm_cluster_id_value",
                    cloud_vm_cluster=cloud_vm_cluster,
                )

                # Make the request
                operation = client.create_cloud_vm_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.CreateCloudVmClusterRequest, dict]):
                The request object. The request for ``CloudVmCluster.Create``.
            parent (str):
                Required. The name of the parent in
                the following format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cloud_vm_cluster (google.cloud.oracledatabase_v1.types.CloudVmCluster):
                Required. The resource being created
                This corresponds to the ``cloud_vm_cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cloud_vm_cluster_id (str):
                Required. The ID of the VM Cluster to create. This value
                is restricted to (^`a-z <[a-z0-9-]{0,61}[a-z0-9]>`__?$)
                and must be a maximum of 63 characters in length. The
                value must start with a letter and end with a letter or
                a number.

                This corresponds to the ``cloud_vm_cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.oracledatabase_v1.types.CloudVmCluster` Details of the Cloud VM Cluster resource.
                   https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/CloudVmCluster/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, cloud_vm_cluster, cloud_vm_cluster_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.CreateCloudVmClusterRequest):
            request = oracledatabase.CreateCloudVmClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if cloud_vm_cluster is not None:
                request.cloud_vm_cluster = cloud_vm_cluster
            if cloud_vm_cluster_id is not None:
                request.cloud_vm_cluster_id = cloud_vm_cluster_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_cloud_vm_cluster]

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
            vm_cluster.CloudVmCluster,
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_cloud_vm_cluster(
        self,
        request: Optional[
            Union[oracledatabase.DeleteCloudVmClusterRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Deletes a single VM Cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_delete_cloud_vm_cluster():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.DeleteCloudVmClusterRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_cloud_vm_cluster(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.DeleteCloudVmClusterRequest, dict]):
                The request object. The request for ``CloudVmCluster.Delete``.
            name (str):
                Required. The name of the Cloud VM Cluster in the
                following format:
                projects/{project}/locations/{location}/cloudVmClusters/{cloud_vm_cluster}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

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
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.DeleteCloudVmClusterRequest):
            request = oracledatabase.DeleteCloudVmClusterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_cloud_vm_cluster]

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
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_entitlements(
        self,
        request: Optional[Union[oracledatabase.ListEntitlementsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListEntitlementsPager:
        r"""Lists the entitlements in a given project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_entitlements():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListEntitlementsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_entitlements(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListEntitlementsRequest, dict]):
                The request object. The request for ``Entitlement.List``.
            parent (str):
                Required. The parent value for the
                entitlement in the following format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListEntitlementsPager:
                The response for Entitlement.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.ListEntitlementsRequest):
            request = oracledatabase.ListEntitlementsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_entitlements]

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
        response = pagers.ListEntitlementsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_db_servers(
        self,
        request: Optional[Union[oracledatabase.ListDbServersRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListDbServersPager:
        r"""Lists the database servers of an Exadata
        Infrastructure instance.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_db_servers():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListDbServersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_db_servers(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListDbServersRequest, dict]):
                The request object. The request for ``DbServer.List``.
            parent (str):
                Required. The parent value for
                database server in the following format:
                projects/{project}/locations/{location}/cloudExadataInfrastructures/{cloudExadataInfrastructure}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListDbServersPager:
                The response for DbServer.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.ListDbServersRequest):
            request = oracledatabase.ListDbServersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_db_servers]

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
        response = pagers.ListDbServersPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_db_nodes(
        self,
        request: Optional[Union[oracledatabase.ListDbNodesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListDbNodesPager:
        r"""Lists the database nodes of a VM Cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_db_nodes():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListDbNodesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_db_nodes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListDbNodesRequest, dict]):
                The request object. The request for ``DbNode.List``.
            parent (str):
                Required. The parent value for
                database node in the following format:
                projects/{project}/locations/{location}/cloudVmClusters/{cloudVmCluster}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListDbNodesPager:
                The response for DbNode.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.ListDbNodesRequest):
            request = oracledatabase.ListDbNodesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_db_nodes]

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
        response = pagers.ListDbNodesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_gi_versions(
        self,
        request: Optional[Union[oracledatabase.ListGiVersionsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListGiVersionsPager:
        r"""Lists all the valid Oracle Grid Infrastructure (GI)
        versions for the given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_gi_versions():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListGiVersionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_gi_versions(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListGiVersionsRequest, dict]):
                The request object. The request for ``GiVersion.List``.
            parent (str):
                Required. The parent value for Grid
                Infrastructure Version in the following
                format: Format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListGiVersionsPager:
                The response for GiVersion.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.ListGiVersionsRequest):
            request = oracledatabase.ListGiVersionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_gi_versions]

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
        response = pagers.ListGiVersionsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_db_system_shapes(
        self,
        request: Optional[Union[oracledatabase.ListDbSystemShapesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListDbSystemShapesPager:
        r"""Lists the database system shapes available for the
        project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_db_system_shapes():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListDbSystemShapesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_db_system_shapes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListDbSystemShapesRequest, dict]):
                The request object. The request for ``DbSystemShape.List``.
            parent (str):
                Required. The parent value for
                Database System Shapes in the following
                format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListDbSystemShapesPager:
                The response for DbSystemShape.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.ListDbSystemShapesRequest):
            request = oracledatabase.ListDbSystemShapesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_db_system_shapes]

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
        response = pagers.ListDbSystemShapesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_autonomous_databases(
        self,
        request: Optional[
            Union[oracledatabase.ListAutonomousDatabasesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListAutonomousDatabasesPager:
        r"""Lists the Autonomous Databases in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_autonomous_databases():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListAutonomousDatabasesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_autonomous_databases(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListAutonomousDatabasesRequest, dict]):
                The request object. The request for ``AutonomousDatabase.List``.
            parent (str):
                Required. The parent value for the
                Autonomous Database in the following
                format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListAutonomousDatabasesPager:
                The response for AutonomousDatabase.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.ListAutonomousDatabasesRequest):
            request = oracledatabase.ListAutonomousDatabasesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_autonomous_databases
        ]

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
        response = pagers.ListAutonomousDatabasesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_autonomous_database(
        self,
        request: Optional[
            Union[oracledatabase.GetAutonomousDatabaseRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> autonomous_database.AutonomousDatabase:
        r"""Gets the details of a single Autonomous Database.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_get_autonomous_database():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.GetAutonomousDatabaseRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_autonomous_database(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.GetAutonomousDatabaseRequest, dict]):
                The request object. The request for ``AutonomousDatabase.Get``.
            name (str):
                Required. The name of the Autonomous Database in the
                following format:
                projects/{project}/locations/{location}/autonomousDatabases/{autonomous_database}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.types.AutonomousDatabase:
                Details of the Autonomous Database
                resource.
                https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/AutonomousDatabase/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.GetAutonomousDatabaseRequest):
            request = oracledatabase.GetAutonomousDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_autonomous_database]

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

    def create_autonomous_database(
        self,
        request: Optional[
            Union[oracledatabase.CreateAutonomousDatabaseRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        autonomous_database: Optional[
            gco_autonomous_database.AutonomousDatabase
        ] = None,
        autonomous_database_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Creates a new Autonomous Database in a given project
        and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_create_autonomous_database():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.CreateAutonomousDatabaseRequest(
                    parent="parent_value",
                    autonomous_database_id="autonomous_database_id_value",
                )

                # Make the request
                operation = client.create_autonomous_database(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.CreateAutonomousDatabaseRequest, dict]):
                The request object. The request for ``AutonomousDatabase.Create``.
            parent (str):
                Required. The name of the parent in
                the following format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            autonomous_database (google.cloud.oracledatabase_v1.types.AutonomousDatabase):
                Required. The Autonomous Database
                being created.

                This corresponds to the ``autonomous_database`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            autonomous_database_id (str):
                Required. The ID of the Autonomous Database to create.
                This value is restricted to
                (^`a-z <[a-z0-9-]{0,61}[a-z0-9]>`__?$) and must be a
                maximum of 63 characters in length. The value must start
                with a letter and end with a letter or a number.

                This corresponds to the ``autonomous_database_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.oracledatabase_v1.types.AutonomousDatabase` Details of the Autonomous Database resource.
                   https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/AutonomousDatabase/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, autonomous_database, autonomous_database_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.CreateAutonomousDatabaseRequest):
            request = oracledatabase.CreateAutonomousDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if autonomous_database is not None:
                request.autonomous_database = autonomous_database
            if autonomous_database_id is not None:
                request.autonomous_database_id = autonomous_database_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_autonomous_database
        ]

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
            gco_autonomous_database.AutonomousDatabase,
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_autonomous_database(
        self,
        request: Optional[
            Union[oracledatabase.DeleteAutonomousDatabaseRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Deletes a single Autonomous Database.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_delete_autonomous_database():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.DeleteAutonomousDatabaseRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_autonomous_database(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.DeleteAutonomousDatabaseRequest, dict]):
                The request object. The request for ``AutonomousDatabase.Delete``.
            name (str):
                Required. The name of the resource in the following
                format:
                projects/{project}/locations/{location}/autonomousDatabases/{autonomous_database}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

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
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.DeleteAutonomousDatabaseRequest):
            request = oracledatabase.DeleteAutonomousDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_autonomous_database
        ]

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
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def restore_autonomous_database(
        self,
        request: Optional[
            Union[oracledatabase.RestoreAutonomousDatabaseRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        restore_time: Optional[timestamp_pb2.Timestamp] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Restores a single Autonomous Database.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_restore_autonomous_database():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.RestoreAutonomousDatabaseRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.restore_autonomous_database(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.RestoreAutonomousDatabaseRequest, dict]):
                The request object. The request for ``AutonomousDatabase.Restore``.
            name (str):
                Required. The name of the Autonomous Database in the
                following format:
                projects/{project}/locations/{location}/autonomousDatabases/{autonomous_database}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            restore_time (google.protobuf.timestamp_pb2.Timestamp):
                Required. The time and date to
                restore the database to.

                This corresponds to the ``restore_time`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.oracledatabase_v1.types.AutonomousDatabase` Details of the Autonomous Database resource.
                   https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/AutonomousDatabase/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name, restore_time]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.RestoreAutonomousDatabaseRequest):
            request = oracledatabase.RestoreAutonomousDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if restore_time is not None:
                request.restore_time = restore_time

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.restore_autonomous_database
        ]

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
            autonomous_database.AutonomousDatabase,
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def generate_autonomous_database_wallet(
        self,
        request: Optional[
            Union[oracledatabase.GenerateAutonomousDatabaseWalletRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        type_: Optional[autonomous_database.GenerateType] = None,
        is_regional: Optional[bool] = None,
        password: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> oracledatabase.GenerateAutonomousDatabaseWalletResponse:
        r"""Generates a wallet for an Autonomous Database.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_generate_autonomous_database_wallet():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.GenerateAutonomousDatabaseWalletRequest(
                    name="name_value",
                    password="password_value",
                )

                # Make the request
                response = client.generate_autonomous_database_wallet(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.GenerateAutonomousDatabaseWalletRequest, dict]):
                The request object. The request for ``AutonomousDatabase.GenerateWallet``.
            name (str):
                Required. The name of the Autonomous Database in the
                following format:
                projects/{project}/locations/{location}/autonomousDatabases/{autonomous_database}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            type_ (google.cloud.oracledatabase_v1.types.GenerateType):
                Optional. The type of wallet
                generation for the Autonomous Database.
                The default value is SINGLE.

                This corresponds to the ``type_`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            is_regional (bool):
                Optional. True when requesting
                regional connection strings in PDB
                connect info, applicable to cross-region
                Data Guard only.

                This corresponds to the ``is_regional`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            password (str):
                Required. The password used to
                encrypt the keys inside the wallet. The
                password must be a minimum of 8
                characters.

                This corresponds to the ``password`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.types.GenerateAutonomousDatabaseWalletResponse:
                The response for AutonomousDatabase.GenerateWallet.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name, type_, is_regional, password]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, oracledatabase.GenerateAutonomousDatabaseWalletRequest
        ):
            request = oracledatabase.GenerateAutonomousDatabaseWalletRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if type_ is not None:
                request.type_ = type_
            if is_regional is not None:
                request.is_regional = is_regional
            if password is not None:
                request.password = password

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.generate_autonomous_database_wallet
        ]

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

    def list_autonomous_db_versions(
        self,
        request: Optional[
            Union[oracledatabase.ListAutonomousDbVersionsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListAutonomousDbVersionsPager:
        r"""Lists all the available Autonomous Database versions
        for a project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_autonomous_db_versions():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListAutonomousDbVersionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_autonomous_db_versions(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListAutonomousDbVersionsRequest, dict]):
                The request object. The request for ``AutonomousDbVersion.List``.
            parent (str):
                Required. The parent value for the
                Autonomous Database in the following
                format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListAutonomousDbVersionsPager:
                The response for AutonomousDbVersion.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.ListAutonomousDbVersionsRequest):
            request = oracledatabase.ListAutonomousDbVersionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_autonomous_db_versions
        ]

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
        response = pagers.ListAutonomousDbVersionsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_autonomous_database_character_sets(
        self,
        request: Optional[
            Union[oracledatabase.ListAutonomousDatabaseCharacterSetsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListAutonomousDatabaseCharacterSetsPager:
        r"""Lists Autonomous Database Character Sets in a given
        project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_autonomous_database_character_sets():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListAutonomousDatabaseCharacterSetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_autonomous_database_character_sets(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseCharacterSetsRequest, dict]):
                The request object. The request for ``AutonomousDatabaseCharacterSet.List``.
            parent (str):
                Required. The parent value for the
                Autonomous Database in the following
                format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListAutonomousDatabaseCharacterSetsPager:
                The response for AutonomousDatabaseCharacterSet.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, oracledatabase.ListAutonomousDatabaseCharacterSetsRequest
        ):
            request = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_autonomous_database_character_sets
        ]

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
        response = pagers.ListAutonomousDatabaseCharacterSetsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_autonomous_database_backups(
        self,
        request: Optional[
            Union[oracledatabase.ListAutonomousDatabaseBackupsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListAutonomousDatabaseBackupsPager:
        r"""Lists the long-term and automatic backups of an
        Autonomous Database.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_list_autonomous_database_backups():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.ListAutonomousDatabaseBackupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_autonomous_database_backups(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.ListAutonomousDatabaseBackupsRequest, dict]):
                The request object. The request for ``AutonomousDatabaseBackup.List``.
            parent (str):
                Required. The parent value for
                ListAutonomousDatabaseBackups in the
                following format:
                projects/{project}/locations/{location}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.cloud.oracledatabase_v1.services.oracle_database.pagers.ListAutonomousDatabaseBackupsPager:
                The response for AutonomousDatabaseBackup.List.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.ListAutonomousDatabaseBackupsRequest):
            request = oracledatabase.ListAutonomousDatabaseBackupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_autonomous_database_backups
        ]

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
        response = pagers.ListAutonomousDatabaseBackupsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def stop_autonomous_database(
        self,
        request: Optional[
            Union[oracledatabase.StopAutonomousDatabaseRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Stops an Autonomous Database.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_stop_autonomous_database():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.StopAutonomousDatabaseRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.stop_autonomous_database(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.StopAutonomousDatabaseRequest, dict]):
                The request object. The request for ``AutonomousDatabase.Stop``.
            name (str):
                Required. The name of the Autonomous Database in the
                following format:
                projects/{project}/locations/{location}/autonomousDatabases/{autonomous_database}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.oracledatabase_v1.types.AutonomousDatabase` Details of the Autonomous Database resource.
                   https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/AutonomousDatabase/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.StopAutonomousDatabaseRequest):
            request = oracledatabase.StopAutonomousDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.stop_autonomous_database]

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
            autonomous_database.AutonomousDatabase,
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def start_autonomous_database(
        self,
        request: Optional[
            Union[oracledatabase.StartAutonomousDatabaseRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Starts an Autonomous Database.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_start_autonomous_database():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.StartAutonomousDatabaseRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.start_autonomous_database(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.StartAutonomousDatabaseRequest, dict]):
                The request object. The request for ``AutonomousDatabase.Start``.
            name (str):
                Required. The name of the Autonomous Database in the
                following format:
                projects/{project}/locations/{location}/autonomousDatabases/{autonomous_database}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.oracledatabase_v1.types.AutonomousDatabase` Details of the Autonomous Database resource.
                   https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/AutonomousDatabase/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.StartAutonomousDatabaseRequest):
            request = oracledatabase.StartAutonomousDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.start_autonomous_database
        ]

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
            autonomous_database.AutonomousDatabase,
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def restart_autonomous_database(
        self,
        request: Optional[
            Union[oracledatabase.RestartAutonomousDatabaseRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operation.Operation:
        r"""Restarts an Autonomous Database.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import oracledatabase_v1

            def sample_restart_autonomous_database():
                # Create a client
                client = oracledatabase_v1.OracleDatabaseClient()

                # Initialize request argument(s)
                request = oracledatabase_v1.RestartAutonomousDatabaseRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.restart_autonomous_database(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.oracledatabase_v1.types.RestartAutonomousDatabaseRequest, dict]):
                The request object. The request for ``AutonomousDatabase.Restart``.
            name (str):
                Required. The name of the Autonomous Database in the
                following format:
                projects/{project}/locations/{location}/autonomousDatabases/{autonomous_database}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.oracledatabase_v1.types.AutonomousDatabase` Details of the Autonomous Database resource.
                   https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/AutonomousDatabase/

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, oracledatabase.RestartAutonomousDatabaseRequest):
            request = oracledatabase.RestartAutonomousDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.restart_autonomous_database
        ]

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
            autonomous_database.AutonomousDatabase,
            metadata_type=oracledatabase.OperationMetadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "OracleDatabaseClient":
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
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

        try:
            # Send the request.
            response = rpc(
                request,
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            )

            # Done; return the response.
            return response
        except core_exceptions.GoogleAPICallError as e:
            self._add_cred_info_for_auth_errors(e)
            raise e

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
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

        try:
            # Send the request.
            response = rpc(
                request,
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            )

            # Done; return the response.
            return response
        except core_exceptions.GoogleAPICallError as e:
            self._add_cred_info_for_auth_errors(e)
            raise e

    def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
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
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
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
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
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

        try:
            # Send the request.
            response = rpc(
                request,
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            )

            # Done; return the response.
            return response
        except core_exceptions.GoogleAPICallError as e:
            self._add_cred_info_for_auth_errors(e)
            raise e

    def list_locations(
        self,
        request: Optional[locations_pb2.ListLocationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
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

        try:
            # Send the request.
            response = rpc(
                request,
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            )

            # Done; return the response.
            return response
        except core_exceptions.GoogleAPICallError as e:
            self._add_cred_info_for_auth_errors(e)
            raise e


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("OracleDatabaseClient",)
