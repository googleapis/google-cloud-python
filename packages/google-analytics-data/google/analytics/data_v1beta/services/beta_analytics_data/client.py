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

from google.analytics.data_v1beta import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.analytics.data_v1beta.services.beta_analytics_data import pagers
from google.analytics.data_v1beta.types import analytics_data_api, data

from .transports.base import DEFAULT_CLIENT_INFO, BetaAnalyticsDataTransport
from .transports.grpc import BetaAnalyticsDataGrpcTransport
from .transports.grpc_asyncio import BetaAnalyticsDataGrpcAsyncIOTransport
from .transports.rest import BetaAnalyticsDataRestTransport


class BetaAnalyticsDataClientMeta(type):
    """Metaclass for the BetaAnalyticsData client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[BetaAnalyticsDataTransport]]
    _transport_registry["grpc"] = BetaAnalyticsDataGrpcTransport
    _transport_registry["grpc_asyncio"] = BetaAnalyticsDataGrpcAsyncIOTransport
    _transport_registry["rest"] = BetaAnalyticsDataRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[BetaAnalyticsDataTransport]:
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


class BetaAnalyticsDataClient(metaclass=BetaAnalyticsDataClientMeta):
    """Google Analytics reporting data service."""

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

    DEFAULT_ENDPOINT = "analyticsdata.googleapis.com"
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
            BetaAnalyticsDataClient: The constructed client.
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
            BetaAnalyticsDataClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> BetaAnalyticsDataTransport:
        """Returns the transport used by the client instance.

        Returns:
            BetaAnalyticsDataTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def audience_export_path(
        property: str,
        audience_export: str,
    ) -> str:
        """Returns a fully-qualified audience_export string."""
        return "properties/{property}/audienceExports/{audience_export}".format(
            property=property,
            audience_export=audience_export,
        )

    @staticmethod
    def parse_audience_export_path(path: str) -> Dict[str, str]:
        """Parses a audience_export path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/audienceExports/(?P<audience_export>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def metadata_path(
        property: str,
    ) -> str:
        """Returns a fully-qualified metadata string."""
        return "properties/{property}/metadata".format(
            property=property,
        )

    @staticmethod
    def parse_metadata_path(path: str) -> Dict[str, str]:
        """Parses a metadata path into its component segments."""
        m = re.match(r"^properties/(?P<property>.+?)/metadata$", path)
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
        transport: Optional[Union[str, BetaAnalyticsDataTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the beta analytics data client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, BetaAnalyticsDataTransport]): The
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
        if isinstance(transport, BetaAnalyticsDataTransport):
            # transport is a BetaAnalyticsDataTransport instance.
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

    def run_report(
        self,
        request: Optional[Union[analytics_data_api.RunReportRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.RunReportResponse:
        r"""Returns a customized report of your Google Analytics event data.
        Reports contain statistics derived from data collected by the
        Google Analytics tracking code. The data returned from the API
        is as a table with columns for the requested dimensions and
        metrics. Metrics are individual measurements of user activity on
        your property, such as active users or event count. Dimensions
        break down metrics across some common criteria, such as country
        or event name.

        For a guide to constructing requests & understanding responses,
        see `Creating a
        Report <https://developers.google.com/analytics/devguides/reporting/data/v1/basics>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_run_report():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.RunReportRequest(
                )

                # Make the request
                response = client.run_report(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.RunReportRequest, dict]):
                The request object. The request to generate a report.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.types.RunReportResponse:
                The response report table
                corresponding to a request.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.RunReportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.RunReportRequest):
            request = analytics_data_api.RunReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_report]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("property", request.property),)),
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

    def run_pivot_report(
        self,
        request: Optional[Union[analytics_data_api.RunPivotReportRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.RunPivotReportResponse:
        r"""Returns a customized pivot report of your Google
        Analytics event data. Pivot reports are more advanced
        and expressive formats than regular reports. In a pivot
        report, dimensions are only visible if they are included
        in a pivot. Multiple pivots can be specified to further
        dissect your data.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_run_pivot_report():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.RunPivotReportRequest(
                )

                # Make the request
                response = client.run_pivot_report(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.RunPivotReportRequest, dict]):
                The request object. The request to generate a pivot
                report.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.types.RunPivotReportResponse:
                The response pivot report table
                corresponding to a pivot request.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.RunPivotReportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.RunPivotReportRequest):
            request = analytics_data_api.RunPivotReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_pivot_report]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("property", request.property),)),
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

    def batch_run_reports(
        self,
        request: Optional[
            Union[analytics_data_api.BatchRunReportsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.BatchRunReportsResponse:
        r"""Returns multiple reports in a batch. All reports must
        be for the same GA4 Property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_batch_run_reports():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.BatchRunReportsRequest(
                )

                # Make the request
                response = client.batch_run_reports(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.BatchRunReportsRequest, dict]):
                The request object. The batch request containing multiple
                report requests.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.types.BatchRunReportsResponse:
                The batch response containing
                multiple reports.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.BatchRunReportsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.BatchRunReportsRequest):
            request = analytics_data_api.BatchRunReportsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_run_reports]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("property", request.property),)),
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

    def batch_run_pivot_reports(
        self,
        request: Optional[
            Union[analytics_data_api.BatchRunPivotReportsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.BatchRunPivotReportsResponse:
        r"""Returns multiple pivot reports in a batch. All
        reports must be for the same GA4 Property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_batch_run_pivot_reports():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.BatchRunPivotReportsRequest(
                )

                # Make the request
                response = client.batch_run_pivot_reports(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.BatchRunPivotReportsRequest, dict]):
                The request object. The batch request containing multiple
                pivot report requests.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.types.BatchRunPivotReportsResponse:
                The batch response containing
                multiple pivot reports.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.BatchRunPivotReportsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.BatchRunPivotReportsRequest):
            request = analytics_data_api.BatchRunPivotReportsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_run_pivot_reports]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("property", request.property),)),
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

    def get_metadata(
        self,
        request: Optional[Union[analytics_data_api.GetMetadataRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.Metadata:
        r"""Returns metadata for dimensions and metrics available in
        reporting methods. Used to explore the dimensions and metrics.
        In this method, a Google Analytics GA4 Property Identifier is
        specified in the request, and the metadata response includes
        Custom dimensions and metrics as well as Universal metadata.

        For example if a custom metric with parameter name
        ``levels_unlocked`` is registered to a property, the Metadata
        response will contain ``customEvent:levels_unlocked``. Universal
        metadata are dimensions and metrics applicable to any property
        such as ``country`` and ``totalUsers``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_get_metadata():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.GetMetadataRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_metadata(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.GetMetadataRequest, dict]):
                The request object. Request for a property's dimension
                and metric metadata.
            name (str):
                Required. The resource name of the metadata to retrieve.
                This name field is specified in the URL path and not URL
                parameters. Property is a numeric Google Analytics GA4
                Property identifier. To learn more, see `where to find
                your Property
                ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.

                Example: properties/1234/metadata

                Set the Property ID to 0 for dimensions and metrics
                common to all properties. In this special mode, this
                method will not return custom dimensions and metrics.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.types.Metadata:
                The dimensions, metrics and
                comparisons currently accepted in
                reporting methods.

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
        # in a analytics_data_api.GetMetadataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.GetMetadataRequest):
            request = analytics_data_api.GetMetadataRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_metadata]

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

    def run_realtime_report(
        self,
        request: Optional[
            Union[analytics_data_api.RunRealtimeReportRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.RunRealtimeReportResponse:
        r"""Returns a customized report of realtime event data for your
        property. Events appear in realtime reports seconds after they
        have been sent to the Google Analytics. Realtime reports show
        events and usage data for the periods of time ranging from the
        present moment to 30 minutes ago (up to 60 minutes for Google
        Analytics 360 properties).

        For a guide to constructing realtime requests & understanding
        responses, see `Creating a Realtime
        Report <https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-basics>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_run_realtime_report():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.RunRealtimeReportRequest(
                )

                # Make the request
                response = client.run_realtime_report(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.RunRealtimeReportRequest, dict]):
                The request object. The request to generate a realtime
                report.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.types.RunRealtimeReportResponse:
                The response realtime report table
                corresponding to a request.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.RunRealtimeReportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.RunRealtimeReportRequest):
            request = analytics_data_api.RunRealtimeReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_realtime_report]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("property", request.property),)),
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

    def check_compatibility(
        self,
        request: Optional[
            Union[analytics_data_api.CheckCompatibilityRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.CheckCompatibilityResponse:
        r"""This compatibility method lists dimensions and
        metrics that can be added to a report request and
        maintain compatibility. This method fails if the
        request's dimensions and metrics are incompatible.

        In Google Analytics, reports fail if they request
        incompatible dimensions and/or metrics; in that case,
        you will need to remove dimensions and/or metrics from
        the incompatible report until the report is compatible.

        The Realtime and Core reports have different
        compatibility rules. This method checks compatibility
        for Core reports.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_check_compatibility():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.CheckCompatibilityRequest(
                )

                # Make the request
                response = client.check_compatibility(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.CheckCompatibilityRequest, dict]):
                The request object. The request for compatibility information for a report's
                dimensions and metrics. Check compatibility provides a
                preview of the compatibility of a report; fields shared
                with the ``runReport`` request should be the same values
                as in your ``runReport`` request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.types.CheckCompatibilityResponse:
                The compatibility response with the
                compatibility of each dimension &
                metric.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.CheckCompatibilityRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.CheckCompatibilityRequest):
            request = analytics_data_api.CheckCompatibilityRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.check_compatibility]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("property", request.property),)),
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

    def create_audience_export(
        self,
        request: Optional[
            Union[analytics_data_api.CreateAudienceExportRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        audience_export: Optional[analytics_data_api.AudienceExport] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates an audience export for later retrieval. This method
        quickly returns the audience export's resource name and
        initiates a long running asynchronous request to form an
        audience export. To export the users in an audience export,
        first create the audience export through this method and then
        send the audience resource name to the ``QueryAudienceExport``
        method.

        See `Creating an Audience
        Export <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-basics>`__
        for an introduction to Audience Exports with examples.

        An audience export is a snapshot of the users currently in the
        audience at the time of audience export creation. Creating
        audience exports for one audience on different days will return
        different results as users enter and exit the audience.

        Audiences in Google Analytics 4 allow you to segment your users
        in the ways that are important to your business. To learn more,
        see https://support.google.com/analytics/answer/9267572.
        Audience exports contain the users in each audience.

        Audience Export APIs have some methods at alpha and other
        methods at beta stability. The intention is to advance methods
        to beta stability after some feedback and adoption. To give your
        feedback on this API, complete the `Google Analytics Audience
        Export API Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__
        form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_create_audience_export():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                audience_export = data_v1beta.AudienceExport()
                audience_export.audience = "audience_value"

                request = data_v1beta.CreateAudienceExportRequest(
                    parent="parent_value",
                    audience_export=audience_export,
                )

                # Make the request
                operation = client.create_audience_export(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.CreateAudienceExportRequest, dict]):
                The request object. A request to create a new audience
                export.
            parent (str):
                Required. The parent resource where this audience export
                will be created. Format: ``properties/{property}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            audience_export (google.analytics.data_v1beta.types.AudienceExport):
                Required. The audience export to
                create.

                This corresponds to the ``audience_export`` field
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

                The result type for the operation will be :class:`google.analytics.data_v1beta.types.AudienceExport` An audience export is a list of users in an audience at the time of the
                   list's creation. One audience may have multiple
                   audience exports created for different days.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, audience_export])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a analytics_data_api.CreateAudienceExportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.CreateAudienceExportRequest):
            request = analytics_data_api.CreateAudienceExportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if audience_export is not None:
                request.audience_export = audience_export

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_audience_export]

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

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            analytics_data_api.AudienceExport,
            metadata_type=analytics_data_api.AudienceExportMetadata,
        )

        # Done; return the response.
        return response

    def query_audience_export(
        self,
        request: Optional[
            Union[analytics_data_api.QueryAudienceExportRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.QueryAudienceExportResponse:
        r"""Retrieves an audience export of users. After creating an
        audience, the users are not immediately available for exporting.
        First, a request to ``CreateAudienceExport`` is necessary to
        create an audience export of users, and then second, this method
        is used to retrieve the users in the audience export.

        See `Creating an Audience
        Export <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-basics>`__
        for an introduction to Audience Exports with examples.

        Audiences in Google Analytics 4 allow you to segment your users
        in the ways that are important to your business. To learn more,
        see https://support.google.com/analytics/answer/9267572.

        Audience Export APIs have some methods at alpha and other
        methods at beta stability. The intention is to advance methods
        to beta stability after some feedback and adoption. To give your
        feedback on this API, complete the `Google Analytics Audience
        Export API Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__
        form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_query_audience_export():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.QueryAudienceExportRequest(
                    name="name_value",
                )

                # Make the request
                response = client.query_audience_export(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.QueryAudienceExportRequest, dict]):
                The request object. A request to list users in an
                audience export.
            name (str):
                Required. The name of the audience export to retrieve
                users from. Format:
                ``properties/{property}/audienceExports/{audience_export}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.types.QueryAudienceExportResponse:
                A list of users in an audience
                export.

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
        # in a analytics_data_api.QueryAudienceExportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.QueryAudienceExportRequest):
            request = analytics_data_api.QueryAudienceExportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.query_audience_export]

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

    def get_audience_export(
        self,
        request: Optional[
            Union[analytics_data_api.GetAudienceExportRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.AudienceExport:
        r"""Gets configuration metadata about a specific audience export.
        This method can be used to understand an audience export after
        it has been created.

        See `Creating an Audience
        Export <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-basics>`__
        for an introduction to Audience Exports with examples.

        Audience Export APIs have some methods at alpha and other
        methods at beta stability. The intention is to advance methods
        to beta stability after some feedback and adoption. To give your
        feedback on this API, complete the `Google Analytics Audience
        Export API Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__
        form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_get_audience_export():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.GetAudienceExportRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_audience_export(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.GetAudienceExportRequest, dict]):
                The request object. A request to retrieve configuration
                metadata about a specific audience
                export.
            name (str):
                Required. The audience export resource name. Format:
                ``properties/{property}/audienceExports/{audience_export}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.types.AudienceExport:
                An audience export is a list of users
                in an audience at the time of the list's
                creation. One audience may have multiple
                audience exports created for different
                days.

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
        # in a analytics_data_api.GetAudienceExportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.GetAudienceExportRequest):
            request = analytics_data_api.GetAudienceExportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_audience_export]

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

    def list_audience_exports(
        self,
        request: Optional[
            Union[analytics_data_api.ListAudienceExportsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAudienceExportsPager:
        r"""Lists all audience exports for a property. This method can be
        used for you to find and reuse existing audience exports rather
        than creating unnecessary new audience exports. The same
        audience can have multiple audience exports that represent the
        export of users that were in an audience on different days.

        See `Creating an Audience
        Export <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-basics>`__
        for an introduction to Audience Exports with examples.

        Audience Export APIs have some methods at alpha and other
        methods at beta stability. The intention is to advance methods
        to beta stability after some feedback and adoption. To give your
        feedback on this API, complete the `Google Analytics Audience
        Export API Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__
        form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1beta

            def sample_list_audience_exports():
                # Create a client
                client = data_v1beta.BetaAnalyticsDataClient()

                # Initialize request argument(s)
                request = data_v1beta.ListAudienceExportsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_audience_exports(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.data_v1beta.types.ListAudienceExportsRequest, dict]):
                The request object. A request to list all audience
                exports for a property.
            parent (str):
                Required. All audience exports for this property will be
                listed in the response. Format:
                ``properties/{property}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1beta.services.beta_analytics_data.pagers.ListAudienceExportsPager:
                A list of all audience exports for a
                property.
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
        # in a analytics_data_api.ListAudienceExportsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, analytics_data_api.ListAudienceExportsRequest):
            request = analytics_data_api.ListAudienceExportsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_audience_exports]

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
        response = pagers.ListAudienceExportsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "BetaAnalyticsDataClient":
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


__all__ = ("BetaAnalyticsDataClient",)
