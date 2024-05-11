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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.dialogflowcx_v3beta1.types import test_case
from google.cloud.dialogflowcx_v3beta1.types import test_case as gcdc_test_case

from .base import DEFAULT_CLIENT_INFO, TestCasesTransport
from .grpc import TestCasesGrpcTransport


class TestCasesGrpcAsyncIOTransport(TestCasesTransport):
    """gRPC AsyncIO backend transport for TestCases.

    Service for managing [Test
    Cases][google.cloud.dialogflow.cx.v3beta1.TestCase] and [Test Case
    Results][google.cloud.dialogflow.cx.v3beta1.TestCaseResult].

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
        host: str = "dialogflow.googleapis.com",
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
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
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
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
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

        if isinstance(channel, aio.Channel):
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
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
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
    def list_test_cases(
        self,
    ) -> Callable[
        [test_case.ListTestCasesRequest], Awaitable[test_case.ListTestCasesResponse]
    ]:
        r"""Return a callable for the list test cases method over gRPC.

        Fetches a list of test cases for a given agent.

        Returns:
            Callable[[~.ListTestCasesRequest],
                    Awaitable[~.ListTestCasesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_test_cases" not in self._stubs:
            self._stubs["list_test_cases"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/ListTestCases",
                request_serializer=test_case.ListTestCasesRequest.serialize,
                response_deserializer=test_case.ListTestCasesResponse.deserialize,
            )
        return self._stubs["list_test_cases"]

    @property
    def batch_delete_test_cases(
        self,
    ) -> Callable[[test_case.BatchDeleteTestCasesRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the batch delete test cases method over gRPC.

        Batch deletes test cases.

        Returns:
            Callable[[~.BatchDeleteTestCasesRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_delete_test_cases" not in self._stubs:
            self._stubs["batch_delete_test_cases"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/BatchDeleteTestCases",
                request_serializer=test_case.BatchDeleteTestCasesRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["batch_delete_test_cases"]

    @property
    def get_test_case(
        self,
    ) -> Callable[[test_case.GetTestCaseRequest], Awaitable[test_case.TestCase]]:
        r"""Return a callable for the get test case method over gRPC.

        Gets a test case.

        Returns:
            Callable[[~.GetTestCaseRequest],
                    Awaitable[~.TestCase]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_test_case" not in self._stubs:
            self._stubs["get_test_case"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/GetTestCase",
                request_serializer=test_case.GetTestCaseRequest.serialize,
                response_deserializer=test_case.TestCase.deserialize,
            )
        return self._stubs["get_test_case"]

    @property
    def create_test_case(
        self,
    ) -> Callable[
        [gcdc_test_case.CreateTestCaseRequest], Awaitable[gcdc_test_case.TestCase]
    ]:
        r"""Return a callable for the create test case method over gRPC.

        Creates a test case for the given agent.

        Returns:
            Callable[[~.CreateTestCaseRequest],
                    Awaitable[~.TestCase]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_test_case" not in self._stubs:
            self._stubs["create_test_case"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/CreateTestCase",
                request_serializer=gcdc_test_case.CreateTestCaseRequest.serialize,
                response_deserializer=gcdc_test_case.TestCase.deserialize,
            )
        return self._stubs["create_test_case"]

    @property
    def update_test_case(
        self,
    ) -> Callable[
        [gcdc_test_case.UpdateTestCaseRequest], Awaitable[gcdc_test_case.TestCase]
    ]:
        r"""Return a callable for the update test case method over gRPC.

        Updates the specified test case.

        Returns:
            Callable[[~.UpdateTestCaseRequest],
                    Awaitable[~.TestCase]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_test_case" not in self._stubs:
            self._stubs["update_test_case"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/UpdateTestCase",
                request_serializer=gcdc_test_case.UpdateTestCaseRequest.serialize,
                response_deserializer=gcdc_test_case.TestCase.deserialize,
            )
        return self._stubs["update_test_case"]

    @property
    def run_test_case(
        self,
    ) -> Callable[[test_case.RunTestCaseRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the run test case method over gRPC.

        Kicks off a test case run.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [RunTestCaseMetadata][google.cloud.dialogflow.cx.v3beta1.RunTestCaseMetadata]
        -  ``response``:
           [RunTestCaseResponse][google.cloud.dialogflow.cx.v3beta1.RunTestCaseResponse]

        Returns:
            Callable[[~.RunTestCaseRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_test_case" not in self._stubs:
            self._stubs["run_test_case"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/RunTestCase",
                request_serializer=test_case.RunTestCaseRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["run_test_case"]

    @property
    def batch_run_test_cases(
        self,
    ) -> Callable[
        [test_case.BatchRunTestCasesRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the batch run test cases method over gRPC.

        Kicks off a batch run of test cases.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [BatchRunTestCasesMetadata][google.cloud.dialogflow.cx.v3beta1.BatchRunTestCasesMetadata]
        -  ``response``:
           [BatchRunTestCasesResponse][google.cloud.dialogflow.cx.v3beta1.BatchRunTestCasesResponse]

        Returns:
            Callable[[~.BatchRunTestCasesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_run_test_cases" not in self._stubs:
            self._stubs["batch_run_test_cases"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/BatchRunTestCases",
                request_serializer=test_case.BatchRunTestCasesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_run_test_cases"]

    @property
    def calculate_coverage(
        self,
    ) -> Callable[
        [test_case.CalculateCoverageRequest],
        Awaitable[test_case.CalculateCoverageResponse],
    ]:
        r"""Return a callable for the calculate coverage method over gRPC.

        Calculates the test coverage for an agent.

        Returns:
            Callable[[~.CalculateCoverageRequest],
                    Awaitable[~.CalculateCoverageResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "calculate_coverage" not in self._stubs:
            self._stubs["calculate_coverage"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/CalculateCoverage",
                request_serializer=test_case.CalculateCoverageRequest.serialize,
                response_deserializer=test_case.CalculateCoverageResponse.deserialize,
            )
        return self._stubs["calculate_coverage"]

    @property
    def import_test_cases(
        self,
    ) -> Callable[
        [test_case.ImportTestCasesRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the import test cases method over gRPC.

        Imports the test cases from a Cloud Storage bucket or a local
        file. It always creates new test cases and won't overwrite any
        existing ones. The provided ID in the imported test case is
        neglected.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [ImportTestCasesMetadata][google.cloud.dialogflow.cx.v3beta1.ImportTestCasesMetadata]
        -  ``response``:
           [ImportTestCasesResponse][google.cloud.dialogflow.cx.v3beta1.ImportTestCasesResponse]

        Returns:
            Callable[[~.ImportTestCasesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_test_cases" not in self._stubs:
            self._stubs["import_test_cases"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/ImportTestCases",
                request_serializer=test_case.ImportTestCasesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_test_cases"]

    @property
    def export_test_cases(
        self,
    ) -> Callable[
        [test_case.ExportTestCasesRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the export test cases method over gRPC.

        Exports the test cases under the agent to a Cloud Storage bucket
        or a local file. Filter can be applied to export a subset of
        test cases.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [ExportTestCasesMetadata][google.cloud.dialogflow.cx.v3beta1.ExportTestCasesMetadata]
        -  ``response``:
           [ExportTestCasesResponse][google.cloud.dialogflow.cx.v3beta1.ExportTestCasesResponse]

        Returns:
            Callable[[~.ExportTestCasesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_test_cases" not in self._stubs:
            self._stubs["export_test_cases"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/ExportTestCases",
                request_serializer=test_case.ExportTestCasesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_test_cases"]

    @property
    def list_test_case_results(
        self,
    ) -> Callable[
        [test_case.ListTestCaseResultsRequest],
        Awaitable[test_case.ListTestCaseResultsResponse],
    ]:
        r"""Return a callable for the list test case results method over gRPC.

        Fetches the list of run results for the given test
        case. A maximum of 100 results are kept for each test
        case.

        Returns:
            Callable[[~.ListTestCaseResultsRequest],
                    Awaitable[~.ListTestCaseResultsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_test_case_results" not in self._stubs:
            self._stubs["list_test_case_results"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/ListTestCaseResults",
                request_serializer=test_case.ListTestCaseResultsRequest.serialize,
                response_deserializer=test_case.ListTestCaseResultsResponse.deserialize,
            )
        return self._stubs["list_test_case_results"]

    @property
    def get_test_case_result(
        self,
    ) -> Callable[
        [test_case.GetTestCaseResultRequest], Awaitable[test_case.TestCaseResult]
    ]:
        r"""Return a callable for the get test case result method over gRPC.

        Gets a test case result.

        Returns:
            Callable[[~.GetTestCaseResultRequest],
                    Awaitable[~.TestCaseResult]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_test_case_result" not in self._stubs:
            self._stubs["get_test_case_result"] = self.grpc_channel.unary_unary(
                "/google.cloud.dialogflow.cx.v3beta1.TestCases/GetTestCaseResult",
                request_serializer=test_case.GetTestCaseResultRequest.serialize,
                response_deserializer=test_case.TestCaseResult.deserialize,
            )
        return self._stubs["get_test_case_result"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_test_cases: gapic_v1.method_async.wrap_method(
                self.list_test_cases,
                default_timeout=None,
                client_info=client_info,
            ),
            self.batch_delete_test_cases: gapic_v1.method_async.wrap_method(
                self.batch_delete_test_cases,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_test_case: gapic_v1.method_async.wrap_method(
                self.get_test_case,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_test_case: gapic_v1.method_async.wrap_method(
                self.create_test_case,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_test_case: gapic_v1.method_async.wrap_method(
                self.update_test_case,
                default_timeout=None,
                client_info=client_info,
            ),
            self.run_test_case: gapic_v1.method_async.wrap_method(
                self.run_test_case,
                default_timeout=None,
                client_info=client_info,
            ),
            self.batch_run_test_cases: gapic_v1.method_async.wrap_method(
                self.batch_run_test_cases,
                default_timeout=None,
                client_info=client_info,
            ),
            self.calculate_coverage: gapic_v1.method_async.wrap_method(
                self.calculate_coverage,
                default_timeout=None,
                client_info=client_info,
            ),
            self.import_test_cases: gapic_v1.method_async.wrap_method(
                self.import_test_cases,
                default_timeout=None,
                client_info=client_info,
            ),
            self.export_test_cases: gapic_v1.method_async.wrap_method(
                self.export_test_cases,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_test_case_results: gapic_v1.method_async.wrap_method(
                self.list_test_case_results,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_test_case_result: gapic_v1.method_async.wrap_method(
                self.get_test_case_result,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def close(self):
        return self.grpc_channel.close()

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]


__all__ = ("TestCasesGrpcAsyncIOTransport",)
