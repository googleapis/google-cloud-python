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
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

from google.cloud.automl_v1beta1 import gapic_version as package_version

import google.auth  # type: ignore
import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account # type: ignore

from google.cloud.automl_v1beta1.types import annotation_spec
from google.cloud.automl_v1beta1.types import column_spec
from google.cloud.automl_v1beta1.types import column_spec as gca_column_spec
from google.cloud.automl_v1beta1.types import dataset
from google.cloud.automl_v1beta1.types import dataset as gca_dataset
from google.cloud.automl_v1beta1.types import model
from google.cloud.automl_v1beta1.types import model_evaluation
from google.cloud.automl_v1beta1.types import service
from google.cloud.automl_v1beta1.types import table_spec
from google.cloud.automl_v1beta1.types import table_spec as gca_table_spec
from google.longrunning import operations_pb2 # type: ignore

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


class AutoMlTransport(abc.ABC):
    """Abstract transport class for AutoMl."""

    AUTH_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
    )

    DEFAULT_HOST: str = 'automl.googleapis.com'
    def __init__(
            self, *,
            host: str = DEFAULT_HOST,
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            api_audience: Optional[str] = None,
            **kwargs,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'automl.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
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
        """

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes
        if not hasattr(self, "_ignore_credentials"):
            self._ignore_credentials: bool = False

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs("'credentials_file' and 'credentials' are mutually exclusive")

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                                credentials_file,
                                **scopes_kwargs,
                                quota_project_id=quota_project_id
                            )
        elif credentials is None and not self._ignore_credentials:
            credentials, _ = google.auth.default(**scopes_kwargs, quota_project_id=quota_project_id)
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(api_audience if api_audience else host)

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if always_use_jwt_access and isinstance(credentials, service_account.Credentials) and hasattr(service_account.Credentials, "with_always_use_jwt_access"):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ':' not in host:
            host += ':443'
        self._host = host

    @property
    def host(self):
        return self._host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_dataset: gapic_v1.method.wrap_method(
                self.create_dataset,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_dataset: gapic_v1.method.wrap_method(
                self.get_dataset,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_datasets: gapic_v1.method.wrap_method(
                self.list_datasets,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.update_dataset: gapic_v1.method.wrap_method(
                self.update_dataset,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.delete_dataset: gapic_v1.method.wrap_method(
                self.delete_dataset,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.import_data: gapic_v1.method.wrap_method(
                self.import_data,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.export_data: gapic_v1.method.wrap_method(
                self.export_data,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_annotation_spec: gapic_v1.method.wrap_method(
                self.get_annotation_spec,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_table_spec: gapic_v1.method.wrap_method(
                self.get_table_spec,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_table_specs: gapic_v1.method.wrap_method(
                self.list_table_specs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.update_table_spec: gapic_v1.method.wrap_method(
                self.update_table_spec,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_column_spec: gapic_v1.method.wrap_method(
                self.get_column_spec,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_column_specs: gapic_v1.method.wrap_method(
                self.list_column_specs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.update_column_spec: gapic_v1.method.wrap_method(
                self.update_column_spec,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.create_model: gapic_v1.method.wrap_method(
                self.create_model,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_model: gapic_v1.method.wrap_method(
                self.get_model,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_models: gapic_v1.method.wrap_method(
                self.list_models,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.delete_model: gapic_v1.method.wrap_method(
                self.delete_model,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.deploy_model: gapic_v1.method.wrap_method(
                self.deploy_model,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.undeploy_model: gapic_v1.method.wrap_method(
                self.undeploy_model,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.export_model: gapic_v1.method.wrap_method(
                self.export_model,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.export_evaluated_examples: gapic_v1.method.wrap_method(
                self.export_evaluated_examples,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.get_model_evaluation: gapic_v1.method.wrap_method(
                self.get_model_evaluation,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=5.0,
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.list_model_evaluations: gapic_v1.method.wrap_method(
                self.list_model_evaluations,
                default_timeout=5.0,
                client_info=client_info,
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
    def create_dataset(self) -> Callable[
            [service.CreateDatasetRequest],
            Union[
                gca_dataset.Dataset,
                Awaitable[gca_dataset.Dataset]
            ]]:
        raise NotImplementedError()

    @property
    def get_dataset(self) -> Callable[
            [service.GetDatasetRequest],
            Union[
                dataset.Dataset,
                Awaitable[dataset.Dataset]
            ]]:
        raise NotImplementedError()

    @property
    def list_datasets(self) -> Callable[
            [service.ListDatasetsRequest],
            Union[
                service.ListDatasetsResponse,
                Awaitable[service.ListDatasetsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def update_dataset(self) -> Callable[
            [service.UpdateDatasetRequest],
            Union[
                gca_dataset.Dataset,
                Awaitable[gca_dataset.Dataset]
            ]]:
        raise NotImplementedError()

    @property
    def delete_dataset(self) -> Callable[
            [service.DeleteDatasetRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def import_data(self) -> Callable[
            [service.ImportDataRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def export_data(self) -> Callable[
            [service.ExportDataRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def get_annotation_spec(self) -> Callable[
            [service.GetAnnotationSpecRequest],
            Union[
                annotation_spec.AnnotationSpec,
                Awaitable[annotation_spec.AnnotationSpec]
            ]]:
        raise NotImplementedError()

    @property
    def get_table_spec(self) -> Callable[
            [service.GetTableSpecRequest],
            Union[
                table_spec.TableSpec,
                Awaitable[table_spec.TableSpec]
            ]]:
        raise NotImplementedError()

    @property
    def list_table_specs(self) -> Callable[
            [service.ListTableSpecsRequest],
            Union[
                service.ListTableSpecsResponse,
                Awaitable[service.ListTableSpecsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def update_table_spec(self) -> Callable[
            [service.UpdateTableSpecRequest],
            Union[
                gca_table_spec.TableSpec,
                Awaitable[gca_table_spec.TableSpec]
            ]]:
        raise NotImplementedError()

    @property
    def get_column_spec(self) -> Callable[
            [service.GetColumnSpecRequest],
            Union[
                column_spec.ColumnSpec,
                Awaitable[column_spec.ColumnSpec]
            ]]:
        raise NotImplementedError()

    @property
    def list_column_specs(self) -> Callable[
            [service.ListColumnSpecsRequest],
            Union[
                service.ListColumnSpecsResponse,
                Awaitable[service.ListColumnSpecsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def update_column_spec(self) -> Callable[
            [service.UpdateColumnSpecRequest],
            Union[
                gca_column_spec.ColumnSpec,
                Awaitable[gca_column_spec.ColumnSpec]
            ]]:
        raise NotImplementedError()

    @property
    def create_model(self) -> Callable[
            [service.CreateModelRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def get_model(self) -> Callable[
            [service.GetModelRequest],
            Union[
                model.Model,
                Awaitable[model.Model]
            ]]:
        raise NotImplementedError()

    @property
    def list_models(self) -> Callable[
            [service.ListModelsRequest],
            Union[
                service.ListModelsResponse,
                Awaitable[service.ListModelsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def delete_model(self) -> Callable[
            [service.DeleteModelRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def deploy_model(self) -> Callable[
            [service.DeployModelRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def undeploy_model(self) -> Callable[
            [service.UndeployModelRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def export_model(self) -> Callable[
            [service.ExportModelRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def export_evaluated_examples(self) -> Callable[
            [service.ExportEvaluatedExamplesRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def get_model_evaluation(self) -> Callable[
            [service.GetModelEvaluationRequest],
            Union[
                model_evaluation.ModelEvaluation,
                Awaitable[model_evaluation.ModelEvaluation]
            ]]:
        raise NotImplementedError()

    @property
    def list_model_evaluations(self) -> Callable[
            [service.ListModelEvaluationsRequest],
            Union[
                service.ListModelEvaluationsResponse,
                Awaitable[service.ListModelEvaluationsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = (
    'AutoMlTransport',
)
