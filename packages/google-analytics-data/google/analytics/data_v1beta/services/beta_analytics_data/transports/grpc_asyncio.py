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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.analytics.data_v1beta.types import analytics_data_api

from .base import DEFAULT_CLIENT_INFO, BetaAnalyticsDataTransport
from .grpc import BetaAnalyticsDataGrpcTransport


class BetaAnalyticsDataGrpcAsyncIOTransport(BetaAnalyticsDataTransport):
    """gRPC AsyncIO backend transport for BetaAnalyticsData.

    Google Analytics reporting data service.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "analyticsdata.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "analyticsdata.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[aio.Channel] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
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
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
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
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

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
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
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

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def run_report(
        self,
    ) -> Callable[
        [analytics_data_api.RunReportRequest],
        Awaitable[analytics_data_api.RunReportResponse],
    ]:
        r"""Return a callable for the run report method over gRPC.

        Returns a customized report of your Google Analytics event data.
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

        Returns:
            Callable[[~.RunReportRequest],
                    Awaitable[~.RunReportResponse]]:
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
        Awaitable[analytics_data_api.RunPivotReportResponse],
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
                    Awaitable[~.RunPivotReportResponse]]:
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
        Awaitable[analytics_data_api.BatchRunReportsResponse],
    ]:
        r"""Return a callable for the batch run reports method over gRPC.

        Returns multiple reports in a batch. All reports must
        be for the same GA4 Property.

        Returns:
            Callable[[~.BatchRunReportsRequest],
                    Awaitable[~.BatchRunReportsResponse]]:
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
        Awaitable[analytics_data_api.BatchRunPivotReportsResponse],
    ]:
        r"""Return a callable for the batch run pivot reports method over gRPC.

        Returns multiple pivot reports in a batch. All
        reports must be for the same GA4 Property.

        Returns:
            Callable[[~.BatchRunPivotReportsRequest],
                    Awaitable[~.BatchRunPivotReportsResponse]]:
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
    ) -> Callable[
        [analytics_data_api.GetMetadataRequest], Awaitable[analytics_data_api.Metadata]
    ]:
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
                    Awaitable[~.Metadata]]:
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
        Awaitable[analytics_data_api.RunRealtimeReportResponse],
    ]:
        r"""Return a callable for the run realtime report method over gRPC.

        Returns a customized report of realtime event data for your
        property. Events appear in realtime reports seconds after they
        have been sent to the Google Analytics. Realtime reports show
        events and usage data for the periods of time ranging from the
        present moment to 30 minutes ago (up to 60 minutes for Google
        Analytics 360 properties).

        For a guide to constructing realtime requests & understanding
        responses, see `Creating a Realtime
        Report <https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-basics>`__.

        Returns:
            Callable[[~.RunRealtimeReportRequest],
                    Awaitable[~.RunRealtimeReportResponse]]:
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

    @property
    def check_compatibility(
        self,
    ) -> Callable[
        [analytics_data_api.CheckCompatibilityRequest],
        Awaitable[analytics_data_api.CheckCompatibilityResponse],
    ]:
        r"""Return a callable for the check compatibility method over gRPC.

        This compatibility method lists dimensions and
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

        Returns:
            Callable[[~.CheckCompatibilityRequest],
                    Awaitable[~.CheckCompatibilityResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "check_compatibility" not in self._stubs:
            self._stubs["check_compatibility"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/CheckCompatibility",
                request_serializer=analytics_data_api.CheckCompatibilityRequest.serialize,
                response_deserializer=analytics_data_api.CheckCompatibilityResponse.deserialize,
            )
        return self._stubs["check_compatibility"]

    @property
    def create_audience_export(
        self,
    ) -> Callable[
        [analytics_data_api.CreateAudienceExportRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create audience export method over gRPC.

        Creates an audience export for later retrieval. This method
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

        Returns:
            Callable[[~.CreateAudienceExportRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_audience_export" not in self._stubs:
            self._stubs["create_audience_export"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/CreateAudienceExport",
                request_serializer=analytics_data_api.CreateAudienceExportRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_audience_export"]

    @property
    def query_audience_export(
        self,
    ) -> Callable[
        [analytics_data_api.QueryAudienceExportRequest],
        Awaitable[analytics_data_api.QueryAudienceExportResponse],
    ]:
        r"""Return a callable for the query audience export method over gRPC.

        Retrieves an audience export of users. After creating an
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

        Returns:
            Callable[[~.QueryAudienceExportRequest],
                    Awaitable[~.QueryAudienceExportResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "query_audience_export" not in self._stubs:
            self._stubs["query_audience_export"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/QueryAudienceExport",
                request_serializer=analytics_data_api.QueryAudienceExportRequest.serialize,
                response_deserializer=analytics_data_api.QueryAudienceExportResponse.deserialize,
            )
        return self._stubs["query_audience_export"]

    @property
    def get_audience_export(
        self,
    ) -> Callable[
        [analytics_data_api.GetAudienceExportRequest],
        Awaitable[analytics_data_api.AudienceExport],
    ]:
        r"""Return a callable for the get audience export method over gRPC.

        Gets configuration metadata about a specific audience export.
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

        Returns:
            Callable[[~.GetAudienceExportRequest],
                    Awaitable[~.AudienceExport]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_audience_export" not in self._stubs:
            self._stubs["get_audience_export"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/GetAudienceExport",
                request_serializer=analytics_data_api.GetAudienceExportRequest.serialize,
                response_deserializer=analytics_data_api.AudienceExport.deserialize,
            )
        return self._stubs["get_audience_export"]

    @property
    def list_audience_exports(
        self,
    ) -> Callable[
        [analytics_data_api.ListAudienceExportsRequest],
        Awaitable[analytics_data_api.ListAudienceExportsResponse],
    ]:
        r"""Return a callable for the list audience exports method over gRPC.

        Lists all audience exports for a property. This method can be
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

        Returns:
            Callable[[~.ListAudienceExportsRequest],
                    Awaitable[~.ListAudienceExportsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_audience_exports" not in self._stubs:
            self._stubs["list_audience_exports"] = self.grpc_channel.unary_unary(
                "/google.analytics.data.v1beta.BetaAnalyticsData/ListAudienceExports",
                request_serializer=analytics_data_api.ListAudienceExportsRequest.serialize,
                response_deserializer=analytics_data_api.ListAudienceExportsResponse.deserialize,
            )
        return self._stubs["list_audience_exports"]

    def close(self):
        return self.grpc_channel.close()


__all__ = ("BetaAnalyticsDataGrpcAsyncIOTransport",)
