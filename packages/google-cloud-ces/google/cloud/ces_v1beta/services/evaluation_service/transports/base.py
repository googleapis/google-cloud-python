# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

from google.cloud.ces_v1beta import gapic_version as package_version
from google.cloud.ces_v1beta._compat import (
    ASYNC_WRAP_METHOD_SUPPORTS_KIND as _ASYNC_WRAP_METHOD_SUPPORTS_KIND,
)
from google.cloud.ces_v1beta._compat import (
    WRAP_METHOD_SUPPORTS_TRACING as _WRAP_METHOD_SUPPORTS_TRACING,
)

_ASYNC_WRAP_METHOD_SUPPORTS_TRACING = _WRAP_METHOD_SUPPORTS_TRACING
_WRAP_METHOD_SUPPORTS_KIND = _WRAP_METHOD_SUPPORTS_TRACING

import google.api_core
import google.auth  # type: ignore
import google.protobuf
import google.protobuf.empty_pb2 as empty_pb2  # type: ignore
from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, operations_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.ces_v1beta.types import evaluation, evaluation_service
from google.cloud.ces_v1beta.types import evaluation as gcc_evaluation

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)
DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class EvaluationServiceTransport(abc.ABC):
    """Abstract transport class for EvaluationService."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/ces",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    DEFAULT_HOST: str = "ces.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'ces.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): Deprecated. A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials. This argument will be
                removed in the next major version of this library.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            api_audience (Optional[str]): The intended audience for the API calls
                to the service that will be set when using certain 3rd party
                authentication flows. Audience is typically a resource identifier.
                If not set, the host value will be used as a default.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client, containing options such as
                custom OpenTelemetry tracer providers.
        """

        # Save the scopes.
        self._scopes = scopes
        if not hasattr(self, "_ignore_credentials"):
            self._ignore_credentials: bool = False

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file,
                scopes=scopes,
                quota_project_id=quota_project_id,
                default_scopes=self.AUTH_SCOPES,
            )
        elif credentials is None and not self._ignore_credentials:
            credentials, _ = google.auth.default(
                scopes=scopes,
                quota_project_id=quota_project_id,
                default_scopes=self.AUTH_SCOPES,
            )
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(
                    api_audience if api_audience else host
                )

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        self._client_options = client_options
        self._wrapped_methods: Dict[Callable, Callable] = {}

    @property
    def host(self):
        return self._host

    def _wrap_method(self, func, *args, **kwargs):
        """Wrap an RPC method with common client-level features.

        Applies retry, timeout, metadata, and tracing wrappers to the
        underlying RPC method callable. If the runtime `google-api-core`
        version supports tracing, transport attributes (`client_options` and
        `kind`) are injected. Otherwise, tracing-specific arguments are
        stripped for backward compatibility with older `google-api-core`
        versions.
        """
        if _WRAP_METHOD_SUPPORTS_TRACING:
            kwargs["client_options"] = self._client_options
            try:
                kind = self.kind
            except NotImplementedError:
                kind = None
            if kind:
                kwargs["kind"] = kind
            return gapic_v1.method.wrap_method(func, *args, **kwargs)
        # Fallback for older runtime versions of google-api-core:
        # - Era 1 (< 2.29.0): Neither tracing args nor `kind` are supported.
        # - Era 2 (>= 2.29.0, < 2.36.0): `kind` is supported (prevents REST from
        #   falling back to gRPC wrapping), but tracing args are not.
        # (These fallbacks can be removed once google-api-core < 2.36.0 is no longer supported.)
        for k in ["client_options", "method_name", "is_streaming"]:
            kwargs.pop(k, None)

        try:
            kind = self.kind
        except NotImplementedError:
            kind = None

        if _WRAP_METHOD_SUPPORTS_KIND and kind:
            kwargs["kind"] = kind
        else:
            kwargs.pop("kind", None)

        return gapic_v1.method.wrap_method(func, *args, **kwargs)

    def _wrap_async_method(self, func, *args, **kwargs):
        """Wrap an async RPC method with common client-level features.

        Applies asynchronous retry, timeout, metadata, and tracing wrappers
        to the underlying RPC method callable. If the runtime `google-api-core`
        version supports tracing, transport attributes (`client_options` and
        `kind`) are injected. Otherwise, tracing-specific arguments are
        stripped for backward compatibility with older `google-api-core`
        versions.
        """
        if _ASYNC_WRAP_METHOD_SUPPORTS_TRACING:
            kwargs["client_options"] = self._client_options
            try:
                kind = self.kind
            except NotImplementedError:
                kind = None
            if kind:
                kwargs["kind"] = kind
            return gapic_v1.method_async.wrap_method(func, *args, **kwargs)
        # Fallback for older runtime versions of google-api-core:
        # - Era 1 (< 2.29.0): Neither tracing args nor `kind` are supported.
        # - Era 2 (>= 2.29.0, < 2.36.0): `kind` is supported (prevents REST from
        #   falling back to gRPC wrapping), but tracing args are not.
        # (These fallbacks can be removed once google-api-core < 2.36.0 is no longer supported.)
        for k in ["client_options", "method_name", "is_streaming"]:
            kwargs.pop(k, None)

        try:
            kind = self.kind
        except NotImplementedError:
            kind = None

        if _ASYNC_WRAP_METHOD_SUPPORTS_KIND and kind:
            kwargs["kind"] = kind
        else:
            kwargs.pop("kind", None)

        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def _prep_wrapped_messages(self, client_info):
        """Precompute and cache wrapped methods for RPC dispatch."""
        self._wrapped_methods = {
            self.run_evaluation: self._wrap_method(
                self.run_evaluation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/RunEvaluation",
            ),
            self.upload_evaluation_audio: self._wrap_method(
                self.upload_evaluation_audio,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/UploadEvaluationAudio",
            ),
            self.create_evaluation: self._wrap_method(
                self.create_evaluation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/CreateEvaluation",
            ),
            self.generate_evaluation: self._wrap_method(
                self.generate_evaluation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/GenerateEvaluation",
            ),
            self.import_evaluations: self._wrap_method(
                self.import_evaluations,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ImportEvaluations",
            ),
            self.create_evaluation_dataset: self._wrap_method(
                self.create_evaluation_dataset,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/CreateEvaluationDataset",
            ),
            self.update_evaluation: self._wrap_method(
                self.update_evaluation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/UpdateEvaluation",
            ),
            self.update_evaluation_dataset: self._wrap_method(
                self.update_evaluation_dataset,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/UpdateEvaluationDataset",
            ),
            self.delete_evaluation: self._wrap_method(
                self.delete_evaluation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/DeleteEvaluation",
            ),
            self.delete_evaluation_result: self._wrap_method(
                self.delete_evaluation_result,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/DeleteEvaluationResult",
            ),
            self.delete_evaluation_dataset: self._wrap_method(
                self.delete_evaluation_dataset,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/DeleteEvaluationDataset",
            ),
            self.delete_evaluation_run: self._wrap_method(
                self.delete_evaluation_run,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/DeleteEvaluationRun",
            ),
            self.get_evaluation: self._wrap_method(
                self.get_evaluation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/GetEvaluation",
            ),
            self.get_evaluation_result: self._wrap_method(
                self.get_evaluation_result,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/GetEvaluationResult",
            ),
            self.get_evaluation_dataset: self._wrap_method(
                self.get_evaluation_dataset,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/GetEvaluationDataset",
            ),
            self.get_evaluation_run: self._wrap_method(
                self.get_evaluation_run,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/GetEvaluationRun",
            ),
            self.list_evaluations: self._wrap_method(
                self.list_evaluations,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ListEvaluations",
            ),
            self.list_evaluation_results: self._wrap_method(
                self.list_evaluation_results,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ListEvaluationResults",
            ),
            self.list_evaluation_datasets: self._wrap_method(
                self.list_evaluation_datasets,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ListEvaluationDatasets",
            ),
            self.list_evaluation_runs: self._wrap_method(
                self.list_evaluation_runs,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ListEvaluationRuns",
            ),
            self.list_evaluation_expectations: self._wrap_method(
                self.list_evaluation_expectations,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ListEvaluationExpectations",
            ),
            self.get_evaluation_expectation: self._wrap_method(
                self.get_evaluation_expectation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/GetEvaluationExpectation",
            ),
            self.create_evaluation_expectation: self._wrap_method(
                self.create_evaluation_expectation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/CreateEvaluationExpectation",
            ),
            self.update_evaluation_expectation: self._wrap_method(
                self.update_evaluation_expectation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/UpdateEvaluationExpectation",
            ),
            self.delete_evaluation_expectation: self._wrap_method(
                self.delete_evaluation_expectation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/DeleteEvaluationExpectation",
            ),
            self.create_scheduled_evaluation_run: self._wrap_method(
                self.create_scheduled_evaluation_run,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/CreateScheduledEvaluationRun",
            ),
            self.get_scheduled_evaluation_run: self._wrap_method(
                self.get_scheduled_evaluation_run,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/GetScheduledEvaluationRun",
            ),
            self.list_scheduled_evaluation_runs: self._wrap_method(
                self.list_scheduled_evaluation_runs,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ListScheduledEvaluationRuns",
            ),
            self.update_scheduled_evaluation_run: self._wrap_method(
                self.update_scheduled_evaluation_run,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/UpdateScheduledEvaluationRun",
            ),
            self.delete_scheduled_evaluation_run: self._wrap_method(
                self.delete_scheduled_evaluation_run,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/DeleteScheduledEvaluationRun",
            ),
            self.test_persona_voice: self._wrap_method(
                self.test_persona_voice,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/TestPersonaVoice",
            ),
            self.export_evaluations: self._wrap_method(
                self.export_evaluations,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ExportEvaluations",
            ),
            self.export_evaluation_runs: self._wrap_method(
                self.export_evaluation_runs,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ExportEvaluationRuns",
            ),
            self.export_evaluation_results: self._wrap_method(
                self.export_evaluation_results,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/ExportEvaluationResults",
            ),
            self.run_evaluation_result_metrics: self._wrap_method(
                self.run_evaluation_result_metrics,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.ces.v1beta.EvaluationService/RunEvaluationResultMetrics",
            ),
            self.get_location: self._wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.location.Locations/GetLocation",
            ),
            self.list_locations: self._wrap_method(
                self.list_locations,
                default_timeout=None,
                client_info=client_info,
                method_name="google.cloud.location.Locations/ListLocations",
            ),
            self.cancel_operation: self._wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.longrunning.Operations/CancelOperation",
            ),
            self.delete_operation: self._wrap_method(
                self.delete_operation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.longrunning.Operations/DeleteOperation",
            ),
            self.get_operation: self._wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
                method_name="google.longrunning.Operations/GetOperation",
            ),
            self.list_operations: self._wrap_method(
                self.list_operations,
                default_timeout=None,
                client_info=client_info,
                method_name="google.longrunning.Operations/ListOperations",
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def operations_client(self):
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def run_evaluation(
        self,
    ) -> Callable[
        [evaluation.RunEvaluationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def upload_evaluation_audio(
        self,
    ) -> Callable[
        [evaluation_service.UploadEvaluationAudioRequest],
        Union[
            evaluation_service.UploadEvaluationAudioResponse,
            Awaitable[evaluation_service.UploadEvaluationAudioResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_evaluation(
        self,
    ) -> Callable[
        [evaluation_service.CreateEvaluationRequest],
        Union[gcc_evaluation.Evaluation, Awaitable[gcc_evaluation.Evaluation]],
    ]:
        raise NotImplementedError()

    @property
    def generate_evaluation(
        self,
    ) -> Callable[
        [evaluation_service.GenerateEvaluationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def import_evaluations(
        self,
    ) -> Callable[
        [evaluation_service.ImportEvaluationsRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_evaluation_dataset(
        self,
    ) -> Callable[
        [evaluation_service.CreateEvaluationDatasetRequest],
        Union[evaluation.EvaluationDataset, Awaitable[evaluation.EvaluationDataset]],
    ]:
        raise NotImplementedError()

    @property
    def update_evaluation(
        self,
    ) -> Callable[
        [evaluation_service.UpdateEvaluationRequest],
        Union[gcc_evaluation.Evaluation, Awaitable[gcc_evaluation.Evaluation]],
    ]:
        raise NotImplementedError()

    @property
    def update_evaluation_dataset(
        self,
    ) -> Callable[
        [evaluation_service.UpdateEvaluationDatasetRequest],
        Union[evaluation.EvaluationDataset, Awaitable[evaluation.EvaluationDataset]],
    ]:
        raise NotImplementedError()

    @property
    def delete_evaluation(
        self,
    ) -> Callable[
        [evaluation_service.DeleteEvaluationRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def delete_evaluation_result(
        self,
    ) -> Callable[
        [evaluation_service.DeleteEvaluationResultRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def delete_evaluation_dataset(
        self,
    ) -> Callable[
        [evaluation_service.DeleteEvaluationDatasetRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def delete_evaluation_run(
        self,
    ) -> Callable[
        [evaluation_service.DeleteEvaluationRunRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_evaluation(
        self,
    ) -> Callable[
        [evaluation_service.GetEvaluationRequest],
        Union[evaluation.Evaluation, Awaitable[evaluation.Evaluation]],
    ]:
        raise NotImplementedError()

    @property
    def get_evaluation_result(
        self,
    ) -> Callable[
        [evaluation_service.GetEvaluationResultRequest],
        Union[evaluation.EvaluationResult, Awaitable[evaluation.EvaluationResult]],
    ]:
        raise NotImplementedError()

    @property
    def get_evaluation_dataset(
        self,
    ) -> Callable[
        [evaluation_service.GetEvaluationDatasetRequest],
        Union[evaluation.EvaluationDataset, Awaitable[evaluation.EvaluationDataset]],
    ]:
        raise NotImplementedError()

    @property
    def get_evaluation_run(
        self,
    ) -> Callable[
        [evaluation_service.GetEvaluationRunRequest],
        Union[evaluation.EvaluationRun, Awaitable[evaluation.EvaluationRun]],
    ]:
        raise NotImplementedError()

    @property
    def list_evaluations(
        self,
    ) -> Callable[
        [evaluation_service.ListEvaluationsRequest],
        Union[
            evaluation_service.ListEvaluationsResponse,
            Awaitable[evaluation_service.ListEvaluationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_evaluation_results(
        self,
    ) -> Callable[
        [evaluation_service.ListEvaluationResultsRequest],
        Union[
            evaluation_service.ListEvaluationResultsResponse,
            Awaitable[evaluation_service.ListEvaluationResultsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_evaluation_datasets(
        self,
    ) -> Callable[
        [evaluation_service.ListEvaluationDatasetsRequest],
        Union[
            evaluation_service.ListEvaluationDatasetsResponse,
            Awaitable[evaluation_service.ListEvaluationDatasetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_evaluation_runs(
        self,
    ) -> Callable[
        [evaluation_service.ListEvaluationRunsRequest],
        Union[
            evaluation_service.ListEvaluationRunsResponse,
            Awaitable[evaluation_service.ListEvaluationRunsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_evaluation_expectations(
        self,
    ) -> Callable[
        [evaluation_service.ListEvaluationExpectationsRequest],
        Union[
            evaluation_service.ListEvaluationExpectationsResponse,
            Awaitable[evaluation_service.ListEvaluationExpectationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_evaluation_expectation(
        self,
    ) -> Callable[
        [evaluation_service.GetEvaluationExpectationRequest],
        Union[
            evaluation.EvaluationExpectation,
            Awaitable[evaluation.EvaluationExpectation],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_evaluation_expectation(
        self,
    ) -> Callable[
        [evaluation_service.CreateEvaluationExpectationRequest],
        Union[
            evaluation.EvaluationExpectation,
            Awaitable[evaluation.EvaluationExpectation],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_evaluation_expectation(
        self,
    ) -> Callable[
        [evaluation_service.UpdateEvaluationExpectationRequest],
        Union[
            evaluation.EvaluationExpectation,
            Awaitable[evaluation.EvaluationExpectation],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_evaluation_expectation(
        self,
    ) -> Callable[
        [evaluation_service.DeleteEvaluationExpectationRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_scheduled_evaluation_run(
        self,
    ) -> Callable[
        [evaluation_service.CreateScheduledEvaluationRunRequest],
        Union[
            evaluation.ScheduledEvaluationRun,
            Awaitable[evaluation.ScheduledEvaluationRun],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_scheduled_evaluation_run(
        self,
    ) -> Callable[
        [evaluation_service.GetScheduledEvaluationRunRequest],
        Union[
            evaluation.ScheduledEvaluationRun,
            Awaitable[evaluation.ScheduledEvaluationRun],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_scheduled_evaluation_runs(
        self,
    ) -> Callable[
        [evaluation_service.ListScheduledEvaluationRunsRequest],
        Union[
            evaluation_service.ListScheduledEvaluationRunsResponse,
            Awaitable[evaluation_service.ListScheduledEvaluationRunsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_scheduled_evaluation_run(
        self,
    ) -> Callable[
        [evaluation_service.UpdateScheduledEvaluationRunRequest],
        Union[
            evaluation.ScheduledEvaluationRun,
            Awaitable[evaluation.ScheduledEvaluationRun],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_scheduled_evaluation_run(
        self,
    ) -> Callable[
        [evaluation_service.DeleteScheduledEvaluationRunRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def test_persona_voice(
        self,
    ) -> Callable[
        [evaluation_service.TestPersonaVoiceRequest],
        Union[
            evaluation_service.TestPersonaVoiceResponse,
            Awaitable[evaluation_service.TestPersonaVoiceResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def export_evaluations(
        self,
    ) -> Callable[
        [evaluation_service.ExportEvaluationsRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def export_evaluation_runs(
        self,
    ) -> Callable[
        [evaluation_service.ExportEvaluationRunsRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def export_evaluation_results(
        self,
    ) -> Callable[
        [evaluation_service.ExportEvaluationResultsRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def run_evaluation_result_metrics(
        self,
    ) -> Callable[
        [evaluation_service.RunEvaluationResultMetricsRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest],
        Union[
            operations_pb2.ListOperationsResponse,
            Awaitable[operations_pb2.ListOperationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_operation(
        self,
    ) -> Callable[
        [operations_pb2.GetOperationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_operation(
        self,
    ) -> Callable[
        [operations_pb2.CancelOperationRequest],
        None,
    ]:
        raise NotImplementedError()

    @property
    def delete_operation(
        self,
    ) -> Callable[
        [operations_pb2.DeleteOperationRequest],
        None,
    ]:
        raise NotImplementedError()

    @property
    def get_location(
        self,
    ) -> Callable[
        [locations_pb2.GetLocationRequest],
        Union[locations_pb2.Location, Awaitable[locations_pb2.Location]],
    ]:
        raise NotImplementedError()

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest],
        Union[
            locations_pb2.ListLocationsResponse,
            Awaitable[locations_pb2.ListLocationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("EvaluationServiceTransport",)
