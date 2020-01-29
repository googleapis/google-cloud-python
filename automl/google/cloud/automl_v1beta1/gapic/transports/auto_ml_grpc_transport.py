# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.cloud.automl_v1beta1.proto import service_pb2_grpc


class AutoMlGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.automl.v1beta1 AutoMl API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="automl.googleapis.com:443"
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
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {"auto_ml_stub": service_pb2_grpc.AutoMlStub(channel)}

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="automl.googleapis.com:443", credentials=None, **kwargs
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
        """Return the gRPC stub for :meth:`AutoMlClient.create_dataset`.

        Creates a dataset.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].CreateDataset

    @property
    def update_dataset(self):
        """Return the gRPC stub for :meth:`AutoMlClient.update_dataset`.

        Updates a dataset.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].UpdateDataset

    @property
    def get_dataset(self):
        """Return the gRPC stub for :meth:`AutoMlClient.get_dataset`.

        Gets a dataset.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].GetDataset

    @property
    def list_datasets(self):
        """Return the gRPC stub for :meth:`AutoMlClient.list_datasets`.

        Lists datasets in a project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].ListDatasets

    @property
    def delete_dataset(self):
        """Return the gRPC stub for :meth:`AutoMlClient.delete_dataset`.

        Deletes a dataset and all of its contents. Returns empty response in the
        ``response`` field when it completes, and ``delete_details`` in the
        ``metadata`` field.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].DeleteDataset

    @property
    def import_data(self):
        """Return the gRPC stub for :meth:`AutoMlClient.import_data`.

        Imports data into a dataset. For Tables this method can only be called
        on an empty Dataset.

        For Tables:

        -  A ``schema_inference_version`` parameter must be explicitly set.
           Returns an empty response in the ``response`` field when it
           completes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].ImportData

    @property
    def export_data(self):
        """Return the gRPC stub for :meth:`AutoMlClient.export_data`.

        Exports dataset's data to the provided output location. Returns an empty
        response in the ``response`` field when it completes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].ExportData

    @property
    def create_model(self):
        """Return the gRPC stub for :meth:`AutoMlClient.create_model`.

        Creates a model. Returns a Model in the ``response`` field when it
        completes. When you create a model, several model evaluations are
        created for it: a global evaluation, and one evaluation for each
        annotation spec.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].CreateModel

    @property
    def get_model(self):
        """Return the gRPC stub for :meth:`AutoMlClient.get_model`.

        Gets a model.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].GetModel

    @property
    def list_models(self):
        """Return the gRPC stub for :meth:`AutoMlClient.list_models`.

        Lists models.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].ListModels

    @property
    def delete_model(self):
        """Return the gRPC stub for :meth:`AutoMlClient.delete_model`.

        Deletes a model. Returns ``google.protobuf.Empty`` in the ``response``
        field when it completes, and ``delete_details`` in the ``metadata``
        field.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].DeleteModel

    @property
    def deploy_model(self):
        """Return the gRPC stub for :meth:`AutoMlClient.deploy_model`.

        Deploys a model. If a model is already deployed, deploying it with the
        same parameters has no effect. Deploying with different parametrs (as
        e.g. changing

        ``node_number``) will reset the deployment state without pausing the
        model's availability.

        Only applicable for Text Classification, Image Object Detection and
        Tables; all other domains manage deployment automatically.

        Returns an empty response in the ``response`` field when it completes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].DeployModel

    @property
    def undeploy_model(self):
        """Return the gRPC stub for :meth:`AutoMlClient.undeploy_model`.

        Undeploys a model. If the model is not deployed this method has no
        effect.

        Only applicable for Text Classification, Image Object Detection and
        Tables; all other domains manage deployment automatically.

        Returns an empty response in the ``response`` field when it completes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].UndeployModel

    @property
    def get_model_evaluation(self):
        """Return the gRPC stub for :meth:`AutoMlClient.get_model_evaluation`.

        Gets a model evaluation.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].GetModelEvaluation

    @property
    def export_model(self):
        """Return the gRPC stub for :meth:`AutoMlClient.export_model`.

        Exports a trained, "export-able", model to a user specified Google Cloud
        Storage location. A model is considered export-able if and only if it
        has an export format defined for it in

        ``ModelExportOutputConfig``.

        Returns an empty response in the ``response`` field when it completes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].ExportModel

    @property
    def export_evaluated_examples(self):
        """Return the gRPC stub for :meth:`AutoMlClient.export_evaluated_examples`.

        Exports examples on which the model was evaluated (i.e. which were in
        the TEST set of the dataset the model was created from), together with
        their ground truth annotations and the annotations created (predicted)
        by the model. The examples, ground truth and predictions are exported in
        the state they were at the moment the model was evaluated.

        This export is available only for 30 days since the model evaluation is
        created.

        Currently only available for Tables.

        Returns an empty response in the ``response`` field when it completes.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].ExportEvaluatedExamples

    @property
    def list_model_evaluations(self):
        """Return the gRPC stub for :meth:`AutoMlClient.list_model_evaluations`.

        Lists model evaluations.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].ListModelEvaluations

    @property
    def get_annotation_spec(self):
        """Return the gRPC stub for :meth:`AutoMlClient.get_annotation_spec`.

        Gets an annotation spec.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].GetAnnotationSpec

    @property
    def get_table_spec(self):
        """Return the gRPC stub for :meth:`AutoMlClient.get_table_spec`.

        Gets a table spec.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].GetTableSpec

    @property
    def list_table_specs(self):
        """Return the gRPC stub for :meth:`AutoMlClient.list_table_specs`.

        Lists table specs in a dataset.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].ListTableSpecs

    @property
    def update_table_spec(self):
        """Return the gRPC stub for :meth:`AutoMlClient.update_table_spec`.

        Updates a table spec.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].UpdateTableSpec

    @property
    def get_column_spec(self):
        """Return the gRPC stub for :meth:`AutoMlClient.get_column_spec`.

        Gets a column spec.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].GetColumnSpec

    @property
    def list_column_specs(self):
        """Return the gRPC stub for :meth:`AutoMlClient.list_column_specs`.

        Lists column specs in a table spec.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].ListColumnSpecs

    @property
    def update_column_spec(self):
        """Return the gRPC stub for :meth:`AutoMlClient.update_column_spec`.

        Updates a column spec.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["auto_ml_stub"].UpdateColumnSpec
