# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import google.api_core.grpc_helpers
import google.api_core.operations_v1

from google.cloud.datalabeling_v1beta1.proto import data_labeling_service_pb2_grpc


class DataLabelingServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.datalabeling.v1beta1 DataLabelingService API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="datalabeling.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "data_labeling_service_stub": data_labeling_service_pb2_grpc.DataLabelingServiceStub(
                channel
            )
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="datalabeling.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_dataset(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.create_dataset`.

        Creates dataset. If success return a Dataset resource.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].CreateDataset

    @property
    def get_dataset(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.get_dataset`.

        Gets dataset by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].GetDataset

    @property
    def list_datasets(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.list_datasets`.

        Lists datasets under a project. Pagination is supported.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ListDatasets

    @property
    def delete_dataset(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.delete_dataset`.

        Deletes a dataset by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].DeleteDataset

    @property
    def import_data(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.import_data`.

        Imports data into dataset based on source locations defined in request.
        It can be called multiple times for the same dataset. Each dataset can
        only have one long running operation running on it. For example, no
        labeling task (also long running operation) can be started while
        importing is still ongoing. Vice versa.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ImportData

    @property
    def export_data(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.export_data`.

        Exports data and annotations from dataset.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ExportData

    @property
    def get_data_item(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.get_data_item`.

        Gets a data item in a dataset by resource name. This API can be
        called after data are imported into dataset.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].GetDataItem

    @property
    def list_data_items(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.list_data_items`.

        Lists data items in a dataset. This API can be called after data
        are imported into dataset. Pagination is supported.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ListDataItems

    @property
    def get_annotated_dataset(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.get_annotated_dataset`.

        Gets an annotated dataset by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].GetAnnotatedDataset

    @property
    def list_annotated_datasets(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.list_annotated_datasets`.

        Lists annotated datasets for a dataset. Pagination is supported.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ListAnnotatedDatasets

    @property
    def label_image(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.label_image`.

        Starts a labeling task for image. The type of image labeling task is
        configured by feature in the request.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].LabelImage

    @property
    def label_video(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.label_video`.

        Starts a labeling task for video. The type of video labeling task is
        configured by feature in the request.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].LabelVideo

    @property
    def label_text(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.label_text`.

        Starts a labeling task for text. The type of text labeling task is
        configured by feature in the request.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].LabelText

    @property
    def get_example(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.get_example`.

        Gets an example by resource name, including both data and annotation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].GetExample

    @property
    def list_examples(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.list_examples`.

        Lists examples in an annotated dataset. Pagination is supported.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ListExamples

    @property
    def create_annotation_spec_set(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.create_annotation_spec_set`.

        Creates an annotation spec set by providing a set of labels.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].CreateAnnotationSpecSet

    @property
    def get_annotation_spec_set(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.get_annotation_spec_set`.

        Gets an annotation spec set by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].GetAnnotationSpecSet

    @property
    def list_annotation_spec_sets(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.list_annotation_spec_sets`.

        Lists annotation spec sets for a project. Pagination is supported.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ListAnnotationSpecSets

    @property
    def delete_annotation_spec_set(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.delete_annotation_spec_set`.

        Deletes an annotation spec set by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].DeleteAnnotationSpecSet

    @property
    def create_instruction(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.create_instruction`.

        Creates an instruction for how data should be labeled.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].CreateInstruction

    @property
    def get_instruction(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.get_instruction`.

        Gets an instruction by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].GetInstruction

    @property
    def list_instructions(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.list_instructions`.

        Lists instructions for a project. Pagination is supported.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ListInstructions

    @property
    def delete_instruction(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.delete_instruction`.

        Deletes an instruction object by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].DeleteInstruction

    @property
    def get_evaluation(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.get_evaluation`.

        Gets an evaluation by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].GetEvaluation

    @property
    def search_evaluations(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.search_evaluations`.

        Searchs evaluations within a project. Supported filter: evaluation\_job,
        evaluation\_time.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].SearchEvaluations

    @property
    def search_example_comparisons(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.search_example_comparisons`.

        Searchs example comparisons in evaluation, in format of examples
        of both ground truth and prediction(s). It is represented as a search with
        evaluation id.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].SearchExampleComparisons

    @property
    def create_evaluation_job(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.create_evaluation_job`.

        Creates an evaluation job.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].CreateEvaluationJob

    @property
    def update_evaluation_job(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.update_evaluation_job`.

        Updates an evaluation job.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].UpdateEvaluationJob

    @property
    def get_evaluation_job(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.get_evaluation_job`.

        Gets an evaluation job by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].GetEvaluationJob

    @property
    def pause_evaluation_job(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.pause_evaluation_job`.

        Pauses an evaluation job. Pausing a evaluation job that is already in
        PAUSED state will be a no-op.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].PauseEvaluationJob

    @property
    def resume_evaluation_job(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.resume_evaluation_job`.

        Resumes a paused evaluation job. Deleted evaluation job can't be resumed.
        Resuming a running evaluation job will be a no-op.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ResumeEvaluationJob

    @property
    def delete_evaluation_job(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.delete_evaluation_job`.

        Stops and deletes an evaluation job.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].DeleteEvaluationJob

    @property
    def list_evaluation_jobs(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.list_evaluation_jobs`.

        Lists all evaluation jobs within a project with possible filters.
        Pagination is supported.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].ListEvaluationJobs

    @property
    def delete_annotated_dataset(self):
        """Return the gRPC stub for :meth:`DataLabelingServiceClient.delete_annotated_dataset`.

        Deletes an annotated dataset by resource name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["data_labeling_service_stub"].DeleteAnnotatedDataset
