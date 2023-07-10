# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.websecurityscanner_v1beta import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.websecurityscanner_v1beta.services.web_security_scanner import pagers
from google.cloud.websecurityscanner_v1beta.types import (
    scan_run,
    scan_run_error_trace,
    scan_run_warning_trace,
    web_security_scanner,
)
from google.cloud.websecurityscanner_v1beta.types import (
    crawled_url,
    finding,
    finding_addon,
    finding_type_stats,
)
from google.cloud.websecurityscanner_v1beta.types import scan_config as gcw_scan_config
from google.cloud.websecurityscanner_v1beta.types import scan_config

from .transports.base import DEFAULT_CLIENT_INFO, WebSecurityScannerTransport
from .transports.grpc import WebSecurityScannerGrpcTransport
from .transports.grpc_asyncio import WebSecurityScannerGrpcAsyncIOTransport
from .transports.rest import WebSecurityScannerRestTransport


class WebSecurityScannerClientMeta(type):
    """Metaclass for the WebSecurityScanner client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[WebSecurityScannerTransport]]
    _transport_registry["grpc"] = WebSecurityScannerGrpcTransport
    _transport_registry["grpc_asyncio"] = WebSecurityScannerGrpcAsyncIOTransport
    _transport_registry["rest"] = WebSecurityScannerRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[WebSecurityScannerTransport]:
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


class WebSecurityScannerClient(metaclass=WebSecurityScannerClientMeta):
    """Cloud Web Security Scanner Service identifies security
    vulnerabilities in web applications hosted on Google Cloud
    Platform. It crawls your application, and attempts to exercise
    as many user inputs and event handlers as possible.
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

    DEFAULT_ENDPOINT = "websecurityscanner.googleapis.com"
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
            WebSecurityScannerClient: The constructed client.
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
            WebSecurityScannerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> WebSecurityScannerTransport:
        """Returns the transport used by the client instance.

        Returns:
            WebSecurityScannerTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def finding_path(
        project: str,
        scan_config: str,
        scan_run: str,
        finding: str,
    ) -> str:
        """Returns a fully-qualified finding string."""
        return "projects/{project}/scanConfigs/{scan_config}/scanRuns/{scan_run}/findings/{finding}".format(
            project=project,
            scan_config=scan_config,
            scan_run=scan_run,
            finding=finding,
        )

    @staticmethod
    def parse_finding_path(path: str) -> Dict[str, str]:
        """Parses a finding path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/scanConfigs/(?P<scan_config>.+?)/scanRuns/(?P<scan_run>.+?)/findings/(?P<finding>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def scan_config_path(
        project: str,
        scan_config: str,
    ) -> str:
        """Returns a fully-qualified scan_config string."""
        return "projects/{project}/scanConfigs/{scan_config}".format(
            project=project,
            scan_config=scan_config,
        )

    @staticmethod
    def parse_scan_config_path(path: str) -> Dict[str, str]:
        """Parses a scan_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/scanConfigs/(?P<scan_config>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def scan_run_path(
        project: str,
        scan_config: str,
        scan_run: str,
    ) -> str:
        """Returns a fully-qualified scan_run string."""
        return (
            "projects/{project}/scanConfigs/{scan_config}/scanRuns/{scan_run}".format(
                project=project,
                scan_config=scan_config,
                scan_run=scan_run,
            )
        )

    @staticmethod
    def parse_scan_run_path(path: str) -> Dict[str, str]:
        """Parses a scan_run path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/scanConfigs/(?P<scan_config>.+?)/scanRuns/(?P<scan_run>.+?)$",
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
        transport: Optional[Union[str, WebSecurityScannerTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the web security scanner client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, WebSecurityScannerTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
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
        client_options = cast(client_options_lib.ClientOptions, client_options)

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
        if isinstance(transport, WebSecurityScannerTransport):
            # transport is a WebSecurityScannerTransport instance.
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
                api_audience=client_options.api_audience,
            )

    def create_scan_config(
        self,
        request: Optional[
            Union[web_security_scanner.CreateScanConfigRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        scan_config: Optional[gcw_scan_config.ScanConfig] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcw_scan_config.ScanConfig:
        r"""Creates a new ScanConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_create_scan_config():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                scan_config = websecurityscanner_v1beta.ScanConfig()
                scan_config.display_name = "display_name_value"
                scan_config.starting_urls = ['starting_urls_value1', 'starting_urls_value2']

                request = websecurityscanner_v1beta.CreateScanConfigRequest(
                    parent="parent_value",
                    scan_config=scan_config,
                )

                # Make the request
                response = client.create_scan_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.CreateScanConfigRequest, dict]):
                The request object. Request for the ``CreateScanConfig`` method.
            parent (str):
                Required. The parent resource name
                where the scan is created, which should
                be a project resource name in the format
                'projects/{projectId}'.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            scan_config (google.cloud.websecurityscanner_v1beta.types.ScanConfig):
                Required. The ScanConfig to be
                created.

                This corresponds to the ``scan_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.types.ScanConfig:
                A ScanConfig resource contains the
                configurations to launch a scan.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, scan_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a web_security_scanner.CreateScanConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.CreateScanConfigRequest):
            request = web_security_scanner.CreateScanConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if scan_config is not None:
                request.scan_config = scan_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_scan_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

    def delete_scan_config(
        self,
        request: Optional[
            Union[web_security_scanner.DeleteScanConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an existing ScanConfig and its child
        resources.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_delete_scan_config():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.DeleteScanConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_scan_config(request=request)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.DeleteScanConfigRequest, dict]):
                The request object. Request for the ``DeleteScanConfig`` method.
            name (str):
                Required. The resource name of the
                ScanConfig to be deleted. The name
                follows the format of
                'projects/{projectId}/scanConfigs/{scanConfigId}'.

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
        # in a web_security_scanner.DeleteScanConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.DeleteScanConfigRequest):
            request = web_security_scanner.DeleteScanConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_scan_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_scan_config(
        self,
        request: Optional[
            Union[web_security_scanner.GetScanConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> scan_config.ScanConfig:
        r"""Gets a ScanConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_get_scan_config():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.GetScanConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_scan_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.GetScanConfigRequest, dict]):
                The request object. Request for the ``GetScanConfig`` method.
            name (str):
                Required. The resource name of the
                ScanConfig to be returned. The name
                follows the format of
                'projects/{projectId}/scanConfigs/{scanConfigId}'.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.types.ScanConfig:
                A ScanConfig resource contains the
                configurations to launch a scan.

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
        # in a web_security_scanner.GetScanConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.GetScanConfigRequest):
            request = web_security_scanner.GetScanConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_scan_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def list_scan_configs(
        self,
        request: Optional[
            Union[web_security_scanner.ListScanConfigsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListScanConfigsPager:
        r"""Lists ScanConfigs under a given project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_list_scan_configs():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.ListScanConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_scan_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.ListScanConfigsRequest, dict]):
                The request object. Request for the ``ListScanConfigs`` method.
            parent (str):
                Required. The parent resource name,
                which should be a project resource name
                in the format 'projects/{projectId}'.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.services.web_security_scanner.pagers.ListScanConfigsPager:
                Response for the ListScanConfigs method.

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
        # in a web_security_scanner.ListScanConfigsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.ListScanConfigsRequest):
            request = web_security_scanner.ListScanConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_scan_configs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListScanConfigsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_scan_config(
        self,
        request: Optional[
            Union[web_security_scanner.UpdateScanConfigRequest, dict]
        ] = None,
        *,
        scan_config: Optional[gcw_scan_config.ScanConfig] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcw_scan_config.ScanConfig:
        r"""Updates a ScanConfig. This method support partial
        update of a ScanConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_update_scan_config():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                scan_config = websecurityscanner_v1beta.ScanConfig()
                scan_config.display_name = "display_name_value"
                scan_config.starting_urls = ['starting_urls_value1', 'starting_urls_value2']

                request = websecurityscanner_v1beta.UpdateScanConfigRequest(
                    scan_config=scan_config,
                )

                # Make the request
                response = client.update_scan_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.UpdateScanConfigRequest, dict]):
                The request object. Request for the ``UpdateScanConfigRequest`` method.
            scan_config (google.cloud.websecurityscanner_v1beta.types.ScanConfig):
                Required. The ScanConfig to be
                updated. The name field must be set to
                identify the resource to be updated. The
                values of fields not covered by the mask
                will be ignored.

                This corresponds to the ``scan_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.types.ScanConfig:
                A ScanConfig resource contains the
                configurations to launch a scan.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([scan_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a web_security_scanner.UpdateScanConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.UpdateScanConfigRequest):
            request = web_security_scanner.UpdateScanConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if scan_config is not None:
                request.scan_config = scan_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_scan_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("scan_config.name", request.scan_config.name),)
            ),
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

    def start_scan_run(
        self,
        request: Optional[Union[web_security_scanner.StartScanRunRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> scan_run.ScanRun:
        r"""Start a ScanRun according to the given ScanConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_start_scan_run():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.StartScanRunRequest(
                    name="name_value",
                )

                # Make the request
                response = client.start_scan_run(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.StartScanRunRequest, dict]):
                The request object. Request for the ``StartScanRun`` method.
            name (str):
                Required. The resource name of the
                ScanConfig to be used. The name follows
                the format of
                'projects/{projectId}/scanConfigs/{scanConfigId}'.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.types.ScanRun:
                A ScanRun is a output-only resource
                representing an actual run of the scan.
                Next id: 12

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
        # in a web_security_scanner.StartScanRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.StartScanRunRequest):
            request = web_security_scanner.StartScanRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start_scan_run]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def get_scan_run(
        self,
        request: Optional[Union[web_security_scanner.GetScanRunRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> scan_run.ScanRun:
        r"""Gets a ScanRun.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_get_scan_run():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.GetScanRunRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_scan_run(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.GetScanRunRequest, dict]):
                The request object. Request for the ``GetScanRun`` method.
            name (str):
                Required. The resource name of the
                ScanRun to be returned. The name follows
                the format of
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.types.ScanRun:
                A ScanRun is a output-only resource
                representing an actual run of the scan.
                Next id: 12

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
        # in a web_security_scanner.GetScanRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.GetScanRunRequest):
            request = web_security_scanner.GetScanRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_scan_run]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def list_scan_runs(
        self,
        request: Optional[Union[web_security_scanner.ListScanRunsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListScanRunsPager:
        r"""Lists ScanRuns under a given ScanConfig, in
        descending order of ScanRun stop time.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_list_scan_runs():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.ListScanRunsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_scan_runs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.ListScanRunsRequest, dict]):
                The request object. Request for the ``ListScanRuns`` method.
            parent (str):
                Required. The parent resource name,
                which should be a scan resource name in
                the format
                'projects/{projectId}/scanConfigs/{scanConfigId}'.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.services.web_security_scanner.pagers.ListScanRunsPager:
                Response for the ListScanRuns method.

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
        # in a web_security_scanner.ListScanRunsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.ListScanRunsRequest):
            request = web_security_scanner.ListScanRunsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_scan_runs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListScanRunsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def stop_scan_run(
        self,
        request: Optional[Union[web_security_scanner.StopScanRunRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> scan_run.ScanRun:
        r"""Stops a ScanRun. The stopped ScanRun is returned.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_stop_scan_run():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.StopScanRunRequest(
                    name="name_value",
                )

                # Make the request
                response = client.stop_scan_run(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.StopScanRunRequest, dict]):
                The request object. Request for the ``StopScanRun`` method.
            name (str):
                Required. The resource name of the
                ScanRun to be stopped. The name follows
                the format of
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.types.ScanRun:
                A ScanRun is a output-only resource
                representing an actual run of the scan.
                Next id: 12

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
        # in a web_security_scanner.StopScanRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.StopScanRunRequest):
            request = web_security_scanner.StopScanRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.stop_scan_run]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def list_crawled_urls(
        self,
        request: Optional[
            Union[web_security_scanner.ListCrawledUrlsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCrawledUrlsPager:
        r"""List CrawledUrls under a given ScanRun.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_list_crawled_urls():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.ListCrawledUrlsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_crawled_urls(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.ListCrawledUrlsRequest, dict]):
                The request object. Request for the ``ListCrawledUrls`` method.
            parent (str):
                Required. The parent resource name,
                which should be a scan run resource name
                in the format
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.services.web_security_scanner.pagers.ListCrawledUrlsPager:
                Response for the ListCrawledUrls method.

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
        # in a web_security_scanner.ListCrawledUrlsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.ListCrawledUrlsRequest):
            request = web_security_scanner.ListCrawledUrlsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_crawled_urls]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCrawledUrlsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_finding(
        self,
        request: Optional[Union[web_security_scanner.GetFindingRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> finding.Finding:
        r"""Gets a Finding.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_get_finding():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.GetFindingRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_finding(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.GetFindingRequest, dict]):
                The request object. Request for the ``GetFinding`` method.
            name (str):
                Required. The resource name of the
                Finding to be returned. The name follows
                the format of
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}/findings/{findingId}'.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.types.Finding:
                A Finding resource represents a
                vulnerability instance identified during
                a ScanRun.

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
        # in a web_security_scanner.GetFindingRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.GetFindingRequest):
            request = web_security_scanner.GetFindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_finding]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
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

    def list_findings(
        self,
        request: Optional[Union[web_security_scanner.ListFindingsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        filter: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListFindingsPager:
        r"""List Findings under a given ScanRun.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_list_findings():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.ListFindingsRequest(
                    parent="parent_value",
                    filter="filter_value",
                )

                # Make the request
                page_result = client.list_findings(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.ListFindingsRequest, dict]):
                The request object. Request for the ``ListFindings`` method.
            parent (str):
                Required. The parent resource name,
                which should be a scan run resource name
                in the format
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Required. The filter expression. The expression must be
                in the format: . Supported field: 'finding_type'.
                Supported operator: '='.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.services.web_security_scanner.pagers.ListFindingsPager:
                Response for the ListFindings method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a web_security_scanner.ListFindingsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.ListFindingsRequest):
            request = web_security_scanner.ListFindingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_findings]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListFindingsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_finding_type_stats(
        self,
        request: Optional[
            Union[web_security_scanner.ListFindingTypeStatsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> web_security_scanner.ListFindingTypeStatsResponse:
        r"""List all FindingTypeStats under a given ScanRun.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import websecurityscanner_v1beta

            def sample_list_finding_type_stats():
                # Create a client
                client = websecurityscanner_v1beta.WebSecurityScannerClient()

                # Initialize request argument(s)
                request = websecurityscanner_v1beta.ListFindingTypeStatsRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.list_finding_type_stats(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.websecurityscanner_v1beta.types.ListFindingTypeStatsRequest, dict]):
                The request object. Request for the ``ListFindingTypeStats`` method.
            parent (str):
                Required. The parent resource name,
                which should be a scan run resource name
                in the format
                'projects/{projectId}/scanConfigs/{scanConfigId}/scanRuns/{scanRunId}'.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.websecurityscanner_v1beta.types.ListFindingTypeStatsResponse:
                Response for the ListFindingTypeStats method.
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
        # in a web_security_scanner.ListFindingTypeStatsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, web_security_scanner.ListFindingTypeStatsRequest):
            request = web_security_scanner.ListFindingTypeStatsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_finding_type_stats]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
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

    def __enter__(self) -> "WebSecurityScannerClient":
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


__all__ = ("WebSecurityScannerClient",)
