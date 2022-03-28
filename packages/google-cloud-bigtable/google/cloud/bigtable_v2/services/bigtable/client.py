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
from typing import Dict, Optional, Iterable, Sequence, Tuple, Type, Union
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

from google.cloud.bigtable_v2.types import bigtable
from google.cloud.bigtable_v2.types import data
from .transports.base import BigtableTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import BigtableGrpcTransport
from .transports.grpc_asyncio import BigtableGrpcAsyncIOTransport


class BigtableClientMeta(type):
    """Metaclass for the Bigtable client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[BigtableTransport]]
    _transport_registry["grpc"] = BigtableGrpcTransport
    _transport_registry["grpc_asyncio"] = BigtableGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: str = None,
    ) -> Type[BigtableTransport]:
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


class BigtableClient(metaclass=BigtableClientMeta):
    """Service for reading from and writing to existing Bigtable
    tables.
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

    DEFAULT_ENDPOINT = "bigtable.googleapis.com"
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
            BigtableClient: The constructed client.
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
            BigtableClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> BigtableTransport:
        """Returns the transport used by the client instance.

        Returns:
            BigtableTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def instance_path(
        project: str,
        instance: str,
    ) -> str:
        """Returns a fully-qualified instance string."""
        return "projects/{project}/instances/{instance}".format(
            project=project,
            instance=instance,
        )

    @staticmethod
    def parse_instance_path(path: str) -> Dict[str, str]:
        """Parses a instance path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def table_path(
        project: str,
        instance: str,
        table: str,
    ) -> str:
        """Returns a fully-qualified table string."""
        return "projects/{project}/instances/{instance}/tables/{table}".format(
            project=project,
            instance=instance,
            table=table,
        )

    @staticmethod
    def parse_table_path(path: str) -> Dict[str, str]:
        """Parses a table path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)/tables/(?P<table>.+?)$",
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
        transport: Union[str, BigtableTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the bigtable client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, BigtableTransport]): The
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
        if isinstance(transport, BigtableTransport):
            # transport is a BigtableTransport instance.
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

    def read_rows(
        self,
        request: Union[bigtable.ReadRowsRequest, dict] = None,
        *,
        table_name: str = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[bigtable.ReadRowsResponse]:
        r"""Streams back the contents of all requested rows in
        key order, optionally applying the same Reader filter to
        each. Depending on their size, rows and cells may be
        broken up across multiple responses, but atomicity of
        each row will still be preserved. See the
        ReadRowsResponse documentation for details.

        Args:
            request (Union[google.cloud.bigtable_v2.types.ReadRowsRequest, dict]):
                The request object. Request message for
                Bigtable.ReadRows.
            table_name (str):
                Required. The unique name of the table from which to
                read. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (str):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.cloud.bigtable_v2.types.ReadRowsResponse]:
                Response message for
                Bigtable.ReadRows.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable.ReadRowsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable.ReadRowsRequest):
            request = bigtable.ReadRowsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if table_name is not None:
                request.table_name = table_name
            if app_profile_id is not None:
                request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.read_rows]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<table_name>projects/[^/]+/instances/[^/]+/tables/[^/]+)$"
        )
        regex_match = routing_param_regex.match(request.table_name)
        if regex_match and regex_match.group("table_name"):
            header_params["table_name"] = regex_match.group("table_name")

        if request.app_profile_id:
            header_params["app_profile_id"] = request.app_profile_id

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def sample_row_keys(
        self,
        request: Union[bigtable.SampleRowKeysRequest, dict] = None,
        *,
        table_name: str = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[bigtable.SampleRowKeysResponse]:
        r"""Returns a sample of row keys in the table. The
        returned row keys will delimit contiguous sections of
        the table of approximately equal size, which can be used
        to break up the data for distributed tasks like
        mapreduces.

        Args:
            request (Union[google.cloud.bigtable_v2.types.SampleRowKeysRequest, dict]):
                The request object. Request message for
                Bigtable.SampleRowKeys.
            table_name (str):
                Required. The unique name of the table from which to
                sample row keys. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (str):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.cloud.bigtable_v2.types.SampleRowKeysResponse]:
                Response message for
                Bigtable.SampleRowKeys.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable.SampleRowKeysRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable.SampleRowKeysRequest):
            request = bigtable.SampleRowKeysRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if table_name is not None:
                request.table_name = table_name
            if app_profile_id is not None:
                request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.sample_row_keys]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<table_name>projects/[^/]+/instances/[^/]+/tables/[^/]+)$"
        )
        regex_match = routing_param_regex.match(request.table_name)
        if regex_match and regex_match.group("table_name"):
            header_params["table_name"] = regex_match.group("table_name")

        if request.app_profile_id:
            header_params["app_profile_id"] = request.app_profile_id

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def mutate_row(
        self,
        request: Union[bigtable.MutateRowRequest, dict] = None,
        *,
        table_name: str = None,
        row_key: bytes = None,
        mutations: Sequence[data.Mutation] = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable.MutateRowResponse:
        r"""Mutates a row atomically. Cells already present in the row are
        left unchanged unless explicitly changed by ``mutation``.

        Args:
            request (Union[google.cloud.bigtable_v2.types.MutateRowRequest, dict]):
                The request object. Request message for
                Bigtable.MutateRow.
            table_name (str):
                Required. The unique name of the table to which the
                mutation should be applied. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            row_key (bytes):
                Required. The key of the row to which
                the mutation should be applied.

                This corresponds to the ``row_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mutations (Sequence[google.cloud.bigtable_v2.types.Mutation]):
                Required. Changes to be atomically
                applied to the specified row. Entries
                are applied in order, meaning that
                earlier mutations can be masked by later
                ones. Must contain at least one entry
                and at most 100000.

                This corresponds to the ``mutations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (str):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_v2.types.MutateRowResponse:
                Response message for
                Bigtable.MutateRow.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, row_key, mutations, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable.MutateRowRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable.MutateRowRequest):
            request = bigtable.MutateRowRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if table_name is not None:
                request.table_name = table_name
            if row_key is not None:
                request.row_key = row_key
            if mutations is not None:
                request.mutations = mutations
            if app_profile_id is not None:
                request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.mutate_row]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<table_name>projects/[^/]+/instances/[^/]+/tables/[^/]+)$"
        )
        regex_match = routing_param_regex.match(request.table_name)
        if regex_match and regex_match.group("table_name"):
            header_params["table_name"] = regex_match.group("table_name")

        if request.app_profile_id:
            header_params["app_profile_id"] = request.app_profile_id

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def mutate_rows(
        self,
        request: Union[bigtable.MutateRowsRequest, dict] = None,
        *,
        table_name: str = None,
        entries: Sequence[bigtable.MutateRowsRequest.Entry] = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[bigtable.MutateRowsResponse]:
        r"""Mutates multiple rows in a batch. Each individual row
        is mutated atomically as in MutateRow, but the entire
        batch is not executed atomically.

        Args:
            request (Union[google.cloud.bigtable_v2.types.MutateRowsRequest, dict]):
                The request object. Request message for
                BigtableService.MutateRows.
            table_name (str):
                Required. The unique name of the
                table to which the mutations should be
                applied.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entries (Sequence[google.cloud.bigtable_v2.types.MutateRowsRequest.Entry]):
                Required. The row keys and
                corresponding mutations to be applied in
                bulk. Each entry is applied as an atomic
                mutation, but the entries may be applied
                in arbitrary order (even between entries
                for the same row). At least one entry
                must be specified, and in total the
                entries can contain at most 100000
                mutations.

                This corresponds to the ``entries`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (str):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.cloud.bigtable_v2.types.MutateRowsResponse]:
                Response message for
                BigtableService.MutateRows.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, entries, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable.MutateRowsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable.MutateRowsRequest):
            request = bigtable.MutateRowsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if table_name is not None:
                request.table_name = table_name
            if entries is not None:
                request.entries = entries
            if app_profile_id is not None:
                request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.mutate_rows]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<table_name>projects/[^/]+/instances/[^/]+/tables/[^/]+)$"
        )
        regex_match = routing_param_regex.match(request.table_name)
        if regex_match and regex_match.group("table_name"):
            header_params["table_name"] = regex_match.group("table_name")

        if request.app_profile_id:
            header_params["app_profile_id"] = request.app_profile_id

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def check_and_mutate_row(
        self,
        request: Union[bigtable.CheckAndMutateRowRequest, dict] = None,
        *,
        table_name: str = None,
        row_key: bytes = None,
        predicate_filter: data.RowFilter = None,
        true_mutations: Sequence[data.Mutation] = None,
        false_mutations: Sequence[data.Mutation] = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable.CheckAndMutateRowResponse:
        r"""Mutates a row atomically based on the output of a
        predicate Reader filter.

        Args:
            request (Union[google.cloud.bigtable_v2.types.CheckAndMutateRowRequest, dict]):
                The request object. Request message for
                Bigtable.CheckAndMutateRow.
            table_name (str):
                Required. The unique name of the table to which the
                conditional mutation should be applied. Values are of
                the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            row_key (bytes):
                Required. The key of the row to which
                the conditional mutation should be
                applied.

                This corresponds to the ``row_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            predicate_filter (google.cloud.bigtable_v2.types.RowFilter):
                The filter to be applied to the contents of the
                specified row. Depending on whether or not any results
                are yielded, either ``true_mutations`` or
                ``false_mutations`` will be executed. If unset, checks
                that the row contains any values at all.

                This corresponds to the ``predicate_filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            true_mutations (Sequence[google.cloud.bigtable_v2.types.Mutation]):
                Changes to be atomically applied to the specified row if
                ``predicate_filter`` yields at least one cell when
                applied to ``row_key``. Entries are applied in order,
                meaning that earlier mutations can be masked by later
                ones. Must contain at least one entry if
                ``false_mutations`` is empty, and at most 100000.

                This corresponds to the ``true_mutations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            false_mutations (Sequence[google.cloud.bigtable_v2.types.Mutation]):
                Changes to be atomically applied to the specified row if
                ``predicate_filter`` does not yield any cells when
                applied to ``row_key``. Entries are applied in order,
                meaning that earlier mutations can be masked by later
                ones. Must contain at least one entry if
                ``true_mutations`` is empty, and at most 100000.

                This corresponds to the ``false_mutations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (str):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_v2.types.CheckAndMutateRowResponse:
                Response message for
                Bigtable.CheckAndMutateRow.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [
                table_name,
                row_key,
                predicate_filter,
                true_mutations,
                false_mutations,
                app_profile_id,
            ]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable.CheckAndMutateRowRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable.CheckAndMutateRowRequest):
            request = bigtable.CheckAndMutateRowRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if table_name is not None:
                request.table_name = table_name
            if row_key is not None:
                request.row_key = row_key
            if predicate_filter is not None:
                request.predicate_filter = predicate_filter
            if true_mutations is not None:
                request.true_mutations = true_mutations
            if false_mutations is not None:
                request.false_mutations = false_mutations
            if app_profile_id is not None:
                request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.check_and_mutate_row]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<table_name>projects/[^/]+/instances/[^/]+/tables/[^/]+)$"
        )
        regex_match = routing_param_regex.match(request.table_name)
        if regex_match and regex_match.group("table_name"):
            header_params["table_name"] = regex_match.group("table_name")

        if request.app_profile_id:
            header_params["app_profile_id"] = request.app_profile_id

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def ping_and_warm(
        self,
        request: Union[bigtable.PingAndWarmRequest, dict] = None,
        *,
        name: str = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable.PingAndWarmResponse:
        r"""Warm up associated instance metadata for this
        connection. This call is not required but may be useful
        for connection keep-alive.

        Args:
            request (Union[google.cloud.bigtable_v2.types.PingAndWarmRequest, dict]):
                The request object. Request message for client
                connection keep-alive and warming.
            name (str):
                Required. The unique name of the instance to check
                permissions for as well as respond. Values are of the
                form ``projects/<project>/instances/<instance>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (str):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_v2.types.PingAndWarmResponse:
                Response message for
                Bigtable.PingAndWarm connection
                keepalive and warming.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable.PingAndWarmRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable.PingAndWarmRequest):
            request = bigtable.PingAndWarmRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if app_profile_id is not None:
                request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.ping_and_warm]

        header_params = {}

        routing_param_regex = re.compile("^(?P<name>projects/[^/]+/instances/[^/]+)$")
        regex_match = routing_param_regex.match(request.name)
        if regex_match and regex_match.group("name"):
            header_params["name"] = regex_match.group("name")

        if request.app_profile_id:
            header_params["app_profile_id"] = request.app_profile_id

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def read_modify_write_row(
        self,
        request: Union[bigtable.ReadModifyWriteRowRequest, dict] = None,
        *,
        table_name: str = None,
        row_key: bytes = None,
        rules: Sequence[data.ReadModifyWriteRule] = None,
        app_profile_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable.ReadModifyWriteRowResponse:
        r"""Modifies a row atomically on the server. The method
        reads the latest existing timestamp and value from the
        specified columns and writes a new entry based on
        pre-defined read/modify/write rules. The new value for
        the timestamp is the greater of the existing timestamp
        or the current server time. The method returns the new
        contents of all modified cells.

        Args:
            request (Union[google.cloud.bigtable_v2.types.ReadModifyWriteRowRequest, dict]):
                The request object. Request message for
                Bigtable.ReadModifyWriteRow.
            table_name (str):
                Required. The unique name of the table to which the
                read/modify/write rules should be applied. Values are of
                the form
                ``projects/<project>/instances/<instance>/tables/<table>``.

                This corresponds to the ``table_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            row_key (bytes):
                Required. The key of the row to which
                the read/modify/write rules should be
                applied.

                This corresponds to the ``row_key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rules (Sequence[google.cloud.bigtable_v2.types.ReadModifyWriteRule]):
                Required. Rules specifying how the
                specified row's contents are to be
                transformed into writes. Entries are
                applied in order, meaning that earlier
                rules will affect the results of later
                ones.

                This corresponds to the ``rules`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (str):
                This value specifies routing for
                replication. If not specified, the
                "default" application profile will be
                used.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_v2.types.ReadModifyWriteRowResponse:
                Response message for
                Bigtable.ReadModifyWriteRow.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_name, row_key, rules, app_profile_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a bigtable.ReadModifyWriteRowRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, bigtable.ReadModifyWriteRowRequest):
            request = bigtable.ReadModifyWriteRowRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if table_name is not None:
                request.table_name = table_name
            if row_key is not None:
                request.row_key = row_key
            if rules is not None:
                request.rules = rules
            if app_profile_id is not None:
                request.app_profile_id = app_profile_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.read_modify_write_row]

        header_params = {}

        routing_param_regex = re.compile(
            "^(?P<table_name>projects/[^/]+/instances/[^/]+/tables/[^/]+)$"
        )
        regex_match = routing_param_regex.match(request.table_name)
        if regex_match and regex_match.group("table_name"):
            header_params["table_name"] = regex_match.group("table_name")

        if request.app_profile_id:
            header_params["app_profile_id"] = request.app_profile_id

        if header_params:
            metadata = tuple(metadata) + (
                gapic_v1.routing_header.to_grpc_metadata(header_params),
            )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
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
            "google-cloud-bigtable",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BigtableClient",)
