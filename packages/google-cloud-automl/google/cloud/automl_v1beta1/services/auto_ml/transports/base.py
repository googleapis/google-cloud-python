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
from google.longrunning import operations_pb2 as operations  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-automl",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class AutoMlTransport(abc.ABC):
    """Abstract transport class for AutoMl."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "automl.googleapis.com",
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
            self.create_dataset: gapic_v1.method.wrap_method(
                self.create_dataset, default_timeout=5.0, client_info=client_info,
            ),
            self.get_dataset: gapic_v1.method.wrap_method(
                self.get_dataset,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
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
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.update_dataset: gapic_v1.method.wrap_method(
                self.update_dataset, default_timeout=5.0, client_info=client_info,
            ),
            self.delete_dataset: gapic_v1.method.wrap_method(
                self.delete_dataset,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.import_data: gapic_v1.method.wrap_method(
                self.import_data, default_timeout=5.0, client_info=client_info,
            ),
            self.export_data: gapic_v1.method.wrap_method(
                self.export_data, default_timeout=5.0, client_info=client_info,
            ),
            self.get_annotation_spec: gapic_v1.method.wrap_method(
                self.get_annotation_spec,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
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
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
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
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.update_table_spec: gapic_v1.method.wrap_method(
                self.update_table_spec, default_timeout=5.0, client_info=client_info,
            ),
            self.get_column_spec: gapic_v1.method.wrap_method(
                self.get_column_spec,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
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
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.update_column_spec: gapic_v1.method.wrap_method(
                self.update_column_spec, default_timeout=5.0, client_info=client_info,
            ),
            self.create_model: gapic_v1.method.wrap_method(
                self.create_model, default_timeout=5.0, client_info=client_info,
            ),
            self.get_model: gapic_v1.method.wrap_method(
                self.get_model,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
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
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
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
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
                ),
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.deploy_model: gapic_v1.method.wrap_method(
                self.deploy_model, default_timeout=5.0, client_info=client_info,
            ),
            self.undeploy_model: gapic_v1.method.wrap_method(
                self.undeploy_model, default_timeout=5.0, client_info=client_info,
            ),
            self.export_model: gapic_v1.method.wrap_method(
                self.export_model, default_timeout=5.0, client_info=client_info,
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
                        exceptions.ServiceUnavailable, exceptions.DeadlineExceeded,
                    ),
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

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_dataset(
        self,
    ) -> typing.Callable[
        [service.CreateDatasetRequest],
        typing.Union[gca_dataset.Dataset, typing.Awaitable[gca_dataset.Dataset]],
    ]:
        raise NotImplementedError()

    @property
    def get_dataset(
        self,
    ) -> typing.Callable[
        [service.GetDatasetRequest],
        typing.Union[dataset.Dataset, typing.Awaitable[dataset.Dataset]],
    ]:
        raise NotImplementedError()

    @property
    def list_datasets(
        self,
    ) -> typing.Callable[
        [service.ListDatasetsRequest],
        typing.Union[
            service.ListDatasetsResponse, typing.Awaitable[service.ListDatasetsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_dataset(
        self,
    ) -> typing.Callable[
        [service.UpdateDatasetRequest],
        typing.Union[gca_dataset.Dataset, typing.Awaitable[gca_dataset.Dataset]],
    ]:
        raise NotImplementedError()

    @property
    def delete_dataset(
        self,
    ) -> typing.Callable[
        [service.DeleteDatasetRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def import_data(
        self,
    ) -> typing.Callable[
        [service.ImportDataRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def export_data(
        self,
    ) -> typing.Callable[
        [service.ExportDataRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_annotation_spec(
        self,
    ) -> typing.Callable[
        [service.GetAnnotationSpecRequest],
        typing.Union[
            annotation_spec.AnnotationSpec,
            typing.Awaitable[annotation_spec.AnnotationSpec],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_table_spec(
        self,
    ) -> typing.Callable[
        [service.GetTableSpecRequest],
        typing.Union[table_spec.TableSpec, typing.Awaitable[table_spec.TableSpec]],
    ]:
        raise NotImplementedError()

    @property
    def list_table_specs(
        self,
    ) -> typing.Callable[
        [service.ListTableSpecsRequest],
        typing.Union[
            service.ListTableSpecsResponse,
            typing.Awaitable[service.ListTableSpecsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_table_spec(
        self,
    ) -> typing.Callable[
        [service.UpdateTableSpecRequest],
        typing.Union[
            gca_table_spec.TableSpec, typing.Awaitable[gca_table_spec.TableSpec]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_column_spec(
        self,
    ) -> typing.Callable[
        [service.GetColumnSpecRequest],
        typing.Union[column_spec.ColumnSpec, typing.Awaitable[column_spec.ColumnSpec]],
    ]:
        raise NotImplementedError()

    @property
    def list_column_specs(
        self,
    ) -> typing.Callable[
        [service.ListColumnSpecsRequest],
        typing.Union[
            service.ListColumnSpecsResponse,
            typing.Awaitable[service.ListColumnSpecsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_column_spec(
        self,
    ) -> typing.Callable[
        [service.UpdateColumnSpecRequest],
        typing.Union[
            gca_column_spec.ColumnSpec, typing.Awaitable[gca_column_spec.ColumnSpec]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_model(
        self,
    ) -> typing.Callable[
        [service.CreateModelRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_model(
        self,
    ) -> typing.Callable[
        [service.GetModelRequest],
        typing.Union[model.Model, typing.Awaitable[model.Model]],
    ]:
        raise NotImplementedError()

    @property
    def list_models(
        self,
    ) -> typing.Callable[
        [service.ListModelsRequest],
        typing.Union[
            service.ListModelsResponse, typing.Awaitable[service.ListModelsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_model(
        self,
    ) -> typing.Callable[
        [service.DeleteModelRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def deploy_model(
        self,
    ) -> typing.Callable[
        [service.DeployModelRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def undeploy_model(
        self,
    ) -> typing.Callable[
        [service.UndeployModelRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def export_model(
        self,
    ) -> typing.Callable[
        [service.ExportModelRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def export_evaluated_examples(
        self,
    ) -> typing.Callable[
        [service.ExportEvaluatedExamplesRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_model_evaluation(
        self,
    ) -> typing.Callable[
        [service.GetModelEvaluationRequest],
        typing.Union[
            model_evaluation.ModelEvaluation,
            typing.Awaitable[model_evaluation.ModelEvaluation],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_model_evaluations(
        self,
    ) -> typing.Callable[
        [service.ListModelEvaluationsRequest],
        typing.Union[
            service.ListModelEvaluationsResponse,
            typing.Awaitable[service.ListModelEvaluationsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("AutoMlTransport",)
