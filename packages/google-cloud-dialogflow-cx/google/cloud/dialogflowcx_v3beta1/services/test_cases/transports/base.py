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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.dialogflowcx_v3beta1.types import test_case
from google.cloud.dialogflowcx_v3beta1.types import test_case as gcdc_test_case
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class TestCasesTransport(abc.ABC):
    """Abstract transport class for TestCases."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/dialogflow",
    )

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_test_cases: gapic_v1.method.wrap_method(
                self.list_test_cases, default_timeout=None, client_info=client_info,
            ),
            self.batch_delete_test_cases: gapic_v1.method.wrap_method(
                self.batch_delete_test_cases,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_test_case: gapic_v1.method.wrap_method(
                self.get_test_case, default_timeout=None, client_info=client_info,
            ),
            self.create_test_case: gapic_v1.method.wrap_method(
                self.create_test_case, default_timeout=None, client_info=client_info,
            ),
            self.update_test_case: gapic_v1.method.wrap_method(
                self.update_test_case, default_timeout=None, client_info=client_info,
            ),
            self.run_test_case: gapic_v1.method.wrap_method(
                self.run_test_case, default_timeout=None, client_info=client_info,
            ),
            self.batch_run_test_cases: gapic_v1.method.wrap_method(
                self.batch_run_test_cases,
                default_timeout=None,
                client_info=client_info,
            ),
            self.calculate_coverage: gapic_v1.method.wrap_method(
                self.calculate_coverage, default_timeout=None, client_info=client_info,
            ),
            self.import_test_cases: gapic_v1.method.wrap_method(
                self.import_test_cases, default_timeout=None, client_info=client_info,
            ),
            self.export_test_cases: gapic_v1.method.wrap_method(
                self.export_test_cases, default_timeout=None, client_info=client_info,
            ),
            self.list_test_case_results: gapic_v1.method.wrap_method(
                self.list_test_case_results,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_test_cases(
        self,
    ) -> typing.Callable[
        [test_case.ListTestCasesRequest],
        typing.Union[
            test_case.ListTestCasesResponse,
            typing.Awaitable[test_case.ListTestCasesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def batch_delete_test_cases(
        self,
    ) -> typing.Callable[
        [test_case.BatchDeleteTestCasesRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_test_case(
        self,
    ) -> typing.Callable[
        [test_case.GetTestCaseRequest],
        typing.Union[test_case.TestCase, typing.Awaitable[test_case.TestCase]],
    ]:
        raise NotImplementedError()

    @property
    def create_test_case(
        self,
    ) -> typing.Callable[
        [gcdc_test_case.CreateTestCaseRequest],
        typing.Union[
            gcdc_test_case.TestCase, typing.Awaitable[gcdc_test_case.TestCase]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_test_case(
        self,
    ) -> typing.Callable[
        [gcdc_test_case.UpdateTestCaseRequest],
        typing.Union[
            gcdc_test_case.TestCase, typing.Awaitable[gcdc_test_case.TestCase]
        ],
    ]:
        raise NotImplementedError()

    @property
    def run_test_case(
        self,
    ) -> typing.Callable[
        [test_case.RunTestCaseRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def batch_run_test_cases(
        self,
    ) -> typing.Callable[
        [test_case.BatchRunTestCasesRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def calculate_coverage(
        self,
    ) -> typing.Callable[
        [test_case.CalculateCoverageRequest],
        typing.Union[
            test_case.CalculateCoverageResponse,
            typing.Awaitable[test_case.CalculateCoverageResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def import_test_cases(
        self,
    ) -> typing.Callable[
        [test_case.ImportTestCasesRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def export_test_cases(
        self,
    ) -> typing.Callable[
        [test_case.ExportTestCasesRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_test_case_results(
        self,
    ) -> typing.Callable[
        [test_case.ListTestCaseResultsRequest],
        typing.Union[
            test_case.ListTestCaseResultsResponse,
            typing.Awaitable[test_case.ListTestCaseResultsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("TestCasesTransport",)
