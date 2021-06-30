# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import gapic_v1  # type: ignore
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.analytics.data_v1beta.types import analytics_data_api
from .base import BetaAnalyticsDataTransport, DEFAULT_CLIENT_INFO


class BetaAnalyticsDataGrpcTransport(BetaAnalyticsDataTransport):
    """gRPC backend transport for BetaAnalyticsData.

    Google Analytics reporting data service.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "analyticsdata.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "analyticsdata.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def run_report(
        self,
    ) -> Callable[
        [analytics_data_api.RunReportRequest], analytics_data_api.RunReportResponse
    ]:
        r"""Return a callable for the run report method over gRPC.

        Returns a customized report of your Google Analytics
        event data. Reports contain statistics derived from data
        collected by the Google Analytics tracking code. The
        data returned from the API is as a table with columns
        for the requested dimensions and metrics. Metrics are
        individual measurements of user activity on your
        property, such as active users or event count.
        Dimensions break down metrics across some common
        criteria, such as country or event name.

        Returns:
            Callable[[~.RunReportRequest],
                    ~.RunReportResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_report" not in self._stubs:
            self._stubs["run_report"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/RunReport",
                request_serializer=analytics_data_api.RunReportRequest.serialize,
                response_deserializer=analytics_data_api.RunReportResponse.deserialize,
            )
        return self._stubs["run_report"]

    @property
    def run_pivot_report(
        self,
    ) -> Callable[
        [analytics_data_api.RunPivotReportRequest],
        analytics_data_api.RunPivotReportResponse,
    ]:
        r"""Return a callable for the run pivot report method over gRPC.

        Returns a customized pivot report of your Google
        Analytics event data. Pivot reports are more advanced
        and expressive formats than regular reports. In a pivot
        report, dimensions are only visible if they are included
        in a pivot. Multiple pivots can be specified to further
        dissect your data.

        Returns:
            Callable[[~.RunPivotReportRequest],
                    ~.RunPivotReportResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_pivot_report" not in self._stubs:
            self._stubs["run_pivot_report"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/RunPivotReport",
                request_serializer=analytics_data_api.RunPivotReportRequest.serialize,
                response_deserializer=analytics_data_api.RunPivotReportResponse.deserialize,
            )
        return self._stubs["run_pivot_report"]

    @property
    def batch_run_reports(
        self,
    ) -> Callable[
        [analytics_data_api.BatchRunReportsRequest],
        analytics_data_api.BatchRunReportsResponse,
    ]:
        r"""Return a callable for the batch run reports method over gRPC.

        Returns multiple reports in a batch. All reports must
        be for the same GA4 Property.

        Returns:
            Callable[[~.BatchRunReportsRequest],
                    ~.BatchRunReportsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_run_reports" not in self._stubs:
            self._stubs["batch_run_reports"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/BatchRunReports",
                request_serializer=analytics_data_api.BatchRunReportsRequest.serialize,
                response_deserializer=analytics_data_api.BatchRunReportsResponse.deserialize,
            )
        return self._stubs["batch_run_reports"]

    @property
    def batch_run_pivot_reports(
        self,
    ) -> Callable[
        [analytics_data_api.BatchRunPivotReportsRequest],
        analytics_data_api.BatchRunPivotReportsResponse,
    ]:
        r"""Return a callable for the batch run pivot reports method over gRPC.

        Returns multiple pivot reports in a batch. All
        reports must be for the same GA4 Property.

        Returns:
            Callable[[~.BatchRunPivotReportsRequest],
                    ~.BatchRunPivotReportsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_run_pivot_reports" not in self._stubs:
            self._stubs["batch_run_pivot_reports"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/BatchRunPivotReports",
                request_serializer=analytics_data_api.BatchRunPivotReportsRequest.serialize,
                response_deserializer=analytics_data_api.BatchRunPivotReportsResponse.deserialize,
            )
        return self._stubs["batch_run_pivot_reports"]

    @property
    def get_metadata(
        self,
    ) -> Callable[[analytics_data_api.GetMetadataRequest], analytics_data_api.Metadata]:
        r"""Return a callable for the get metadata method over gRPC.

        Returns metadata for dimensions and metrics available in
        reporting methods. Used to explore the dimensions and metrics.
        In this method, a Google Analytics GA4 Property Identifier is
        specified in the request, and the metadata response includes
        Custom dimensions and metrics as well as Universal metadata.

        For example if a custom metric with parameter name
        ``levels_unlocked`` is registered to a property, the Metadata
        response will contain ``customEvent:levels_unlocked``. Universal
        metadata are dimensions and metrics applicable to any property
        such as ``country`` and ``totalUsers``.

        Returns:
            Callable[[~.GetMetadataRequest],
                    ~.Metadata]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_metadata" not in self._stubs:
            self._stubs["get_metadata"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/GetMetadata",
                request_serializer=analytics_data_api.GetMetadataRequest.serialize,
                response_deserializer=analytics_data_api.Metadata.deserialize,
            )
        return self._stubs["get_metadata"]

    @property
    def run_realtime_report(
        self,
    ) -> Callable[
        [analytics_data_api.RunRealtimeReportRequest],
        analytics_data_api.RunRealtimeReportResponse,
    ]:
        r"""Return a callable for the run realtime report method over gRPC.

        The Google Analytics Realtime API returns a
        customized report of realtime event data for your
        property. These reports show events and usage from the
        last 30 minutes.

        Returns:
            Callable[[~.RunRealtimeReportRequest],
                    ~.RunRealtimeReportResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_realtime_report" not in self._stubs:
            self._stubs["run_realtime_report"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/RunRealtimeReport",
                request_serializer=analytics_data_api.RunRealtimeReportRequest.serialize,
                response_deserializer=analytics_data_api.RunRealtimeReportResponse.deserialize,
            )
        return self._stubs["run_realtime_report"]


__all__ = ("BetaAnalyticsDataGrpcTransport",)
