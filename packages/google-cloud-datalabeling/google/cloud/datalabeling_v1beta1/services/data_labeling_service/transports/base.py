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

from google.cloud.datalabeling_v1beta1.types import annotation_spec_set
from google.cloud.datalabeling_v1beta1.types import (
    annotation_spec_set as gcd_annotation_spec_set,
)
from google.cloud.datalabeling_v1beta1.types import data_labeling_service
from google.cloud.datalabeling_v1beta1.types import dataset
from google.cloud.datalabeling_v1beta1.types import dataset as gcd_dataset
from google.cloud.datalabeling_v1beta1.types import evaluation
from google.cloud.datalabeling_v1beta1.types import evaluation_job
from google.cloud.datalabeling_v1beta1.types import evaluation_job as gcd_evaluation_job
from google.cloud.datalabeling_v1beta1.types import instruction
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-datalabeling",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class DataLabelingServiceTransport(abc.ABC):
    """Abstract transport class for DataLabelingService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "datalabeling.googleapis.com",
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

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=self._scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=self._scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_dataset: gapic_v1.method.wrap_method(
                self.create_dataset, default_timeout=30.0, client_info=client_info,
            ),
            self.get_dataset: gapic_v1.method.wrap_method(
                self.get_dataset,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_datasets: gapic_v1.method.wrap_method(
                self.list_datasets,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_dataset: gapic_v1.method.wrap_method(
                self.delete_dataset,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.import_data: gapic_v1.method.wrap_method(
                self.import_data, default_timeout=30.0, client_info=client_info,
            ),
            self.export_data: gapic_v1.method.wrap_method(
                self.export_data,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_data_item: gapic_v1.method.wrap_method(
                self.get_data_item,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_data_items: gapic_v1.method.wrap_method(
                self.list_data_items,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_annotated_dataset: gapic_v1.method.wrap_method(
                self.get_annotated_dataset,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_annotated_datasets: gapic_v1.method.wrap_method(
                self.list_annotated_datasets,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_annotated_dataset: gapic_v1.method.wrap_method(
                self.delete_annotated_dataset,
                default_timeout=None,
                client_info=client_info,
            ),
            self.label_image: gapic_v1.method.wrap_method(
                self.label_image, default_timeout=30.0, client_info=client_info,
            ),
            self.label_video: gapic_v1.method.wrap_method(
                self.label_video, default_timeout=30.0, client_info=client_info,
            ),
            self.label_text: gapic_v1.method.wrap_method(
                self.label_text, default_timeout=30.0, client_info=client_info,
            ),
            self.get_example: gapic_v1.method.wrap_method(
                self.get_example,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_examples: gapic_v1.method.wrap_method(
                self.list_examples,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_annotation_spec_set: gapic_v1.method.wrap_method(
                self.create_annotation_spec_set,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_annotation_spec_set: gapic_v1.method.wrap_method(
                self.get_annotation_spec_set,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_annotation_spec_sets: gapic_v1.method.wrap_method(
                self.list_annotation_spec_sets,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_annotation_spec_set: gapic_v1.method.wrap_method(
                self.delete_annotation_spec_set,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_instruction: gapic_v1.method.wrap_method(
                self.create_instruction, default_timeout=30.0, client_info=client_info,
            ),
            self.get_instruction: gapic_v1.method.wrap_method(
                self.get_instruction,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_instructions: gapic_v1.method.wrap_method(
                self.list_instructions,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_instruction: gapic_v1.method.wrap_method(
                self.delete_instruction,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_evaluation: gapic_v1.method.wrap_method(
                self.get_evaluation,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.search_evaluations: gapic_v1.method.wrap_method(
                self.search_evaluations,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.search_example_comparisons: gapic_v1.method.wrap_method(
                self.search_example_comparisons,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_evaluation_job: gapic_v1.method.wrap_method(
                self.create_evaluation_job,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_evaluation_job: gapic_v1.method.wrap_method(
                self.update_evaluation_job,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_evaluation_job: gapic_v1.method.wrap_method(
                self.get_evaluation_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.pause_evaluation_job: gapic_v1.method.wrap_method(
                self.pause_evaluation_job,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.resume_evaluation_job: gapic_v1.method.wrap_method(
                self.resume_evaluation_job,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_evaluation_job: gapic_v1.method.wrap_method(
                self.delete_evaluation_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_evaluation_jobs: gapic_v1.method.wrap_method(
                self.list_evaluation_jobs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=30.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
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
        [data_labeling_service.CreateDatasetRequest],
        typing.Union[gcd_dataset.Dataset, typing.Awaitable[gcd_dataset.Dataset]],
    ]:
        raise NotImplementedError()

    @property
    def get_dataset(
        self,
    ) -> typing.Callable[
        [data_labeling_service.GetDatasetRequest],
        typing.Union[dataset.Dataset, typing.Awaitable[dataset.Dataset]],
    ]:
        raise NotImplementedError()

    @property
    def list_datasets(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ListDatasetsRequest],
        typing.Union[
            data_labeling_service.ListDatasetsResponse,
            typing.Awaitable[data_labeling_service.ListDatasetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_dataset(
        self,
    ) -> typing.Callable[
        [data_labeling_service.DeleteDatasetRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def import_data(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ImportDataRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def export_data(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ExportDataRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_data_item(
        self,
    ) -> typing.Callable[
        [data_labeling_service.GetDataItemRequest],
        typing.Union[dataset.DataItem, typing.Awaitable[dataset.DataItem]],
    ]:
        raise NotImplementedError()

    @property
    def list_data_items(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ListDataItemsRequest],
        typing.Union[
            data_labeling_service.ListDataItemsResponse,
            typing.Awaitable[data_labeling_service.ListDataItemsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_annotated_dataset(
        self,
    ) -> typing.Callable[
        [data_labeling_service.GetAnnotatedDatasetRequest],
        typing.Union[
            dataset.AnnotatedDataset, typing.Awaitable[dataset.AnnotatedDataset]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_annotated_datasets(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ListAnnotatedDatasetsRequest],
        typing.Union[
            data_labeling_service.ListAnnotatedDatasetsResponse,
            typing.Awaitable[data_labeling_service.ListAnnotatedDatasetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_annotated_dataset(
        self,
    ) -> typing.Callable[
        [data_labeling_service.DeleteAnnotatedDatasetRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def label_image(
        self,
    ) -> typing.Callable[
        [data_labeling_service.LabelImageRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def label_video(
        self,
    ) -> typing.Callable[
        [data_labeling_service.LabelVideoRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def label_text(
        self,
    ) -> typing.Callable[
        [data_labeling_service.LabelTextRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_example(
        self,
    ) -> typing.Callable[
        [data_labeling_service.GetExampleRequest],
        typing.Union[dataset.Example, typing.Awaitable[dataset.Example]],
    ]:
        raise NotImplementedError()

    @property
    def list_examples(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ListExamplesRequest],
        typing.Union[
            data_labeling_service.ListExamplesResponse,
            typing.Awaitable[data_labeling_service.ListExamplesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_annotation_spec_set(
        self,
    ) -> typing.Callable[
        [data_labeling_service.CreateAnnotationSpecSetRequest],
        typing.Union[
            gcd_annotation_spec_set.AnnotationSpecSet,
            typing.Awaitable[gcd_annotation_spec_set.AnnotationSpecSet],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_annotation_spec_set(
        self,
    ) -> typing.Callable[
        [data_labeling_service.GetAnnotationSpecSetRequest],
        typing.Union[
            annotation_spec_set.AnnotationSpecSet,
            typing.Awaitable[annotation_spec_set.AnnotationSpecSet],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_annotation_spec_sets(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ListAnnotationSpecSetsRequest],
        typing.Union[
            data_labeling_service.ListAnnotationSpecSetsResponse,
            typing.Awaitable[data_labeling_service.ListAnnotationSpecSetsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_annotation_spec_set(
        self,
    ) -> typing.Callable[
        [data_labeling_service.DeleteAnnotationSpecSetRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_instruction(
        self,
    ) -> typing.Callable[
        [data_labeling_service.CreateInstructionRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_instruction(
        self,
    ) -> typing.Callable[
        [data_labeling_service.GetInstructionRequest],
        typing.Union[
            instruction.Instruction, typing.Awaitable[instruction.Instruction]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_instructions(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ListInstructionsRequest],
        typing.Union[
            data_labeling_service.ListInstructionsResponse,
            typing.Awaitable[data_labeling_service.ListInstructionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_instruction(
        self,
    ) -> typing.Callable[
        [data_labeling_service.DeleteInstructionRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_evaluation(
        self,
    ) -> typing.Callable[
        [data_labeling_service.GetEvaluationRequest],
        typing.Union[evaluation.Evaluation, typing.Awaitable[evaluation.Evaluation]],
    ]:
        raise NotImplementedError()

    @property
    def search_evaluations(
        self,
    ) -> typing.Callable[
        [data_labeling_service.SearchEvaluationsRequest],
        typing.Union[
            data_labeling_service.SearchEvaluationsResponse,
            typing.Awaitable[data_labeling_service.SearchEvaluationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def search_example_comparisons(
        self,
    ) -> typing.Callable[
        [data_labeling_service.SearchExampleComparisonsRequest],
        typing.Union[
            data_labeling_service.SearchExampleComparisonsResponse,
            typing.Awaitable[data_labeling_service.SearchExampleComparisonsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_evaluation_job(
        self,
    ) -> typing.Callable[
        [data_labeling_service.CreateEvaluationJobRequest],
        typing.Union[
            evaluation_job.EvaluationJob, typing.Awaitable[evaluation_job.EvaluationJob]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_evaluation_job(
        self,
    ) -> typing.Callable[
        [data_labeling_service.UpdateEvaluationJobRequest],
        typing.Union[
            gcd_evaluation_job.EvaluationJob,
            typing.Awaitable[gcd_evaluation_job.EvaluationJob],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_evaluation_job(
        self,
    ) -> typing.Callable[
        [data_labeling_service.GetEvaluationJobRequest],
        typing.Union[
            evaluation_job.EvaluationJob, typing.Awaitable[evaluation_job.EvaluationJob]
        ],
    ]:
        raise NotImplementedError()

    @property
    def pause_evaluation_job(
        self,
    ) -> typing.Callable[
        [data_labeling_service.PauseEvaluationJobRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def resume_evaluation_job(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ResumeEvaluationJobRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def delete_evaluation_job(
        self,
    ) -> typing.Callable[
        [data_labeling_service.DeleteEvaluationJobRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_evaluation_jobs(
        self,
    ) -> typing.Callable[
        [data_labeling_service.ListEvaluationJobsRequest],
        typing.Union[
            data_labeling_service.ListEvaluationJobsResponse,
            typing.Awaitable[data_labeling_service.ListEvaluationJobsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("DataLabelingServiceTransport",)
