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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.automl_v1.types import dataset as gca_dataset
from google.cloud.automl_v1.types import image
from google.cloud.automl_v1.types import io
from google.cloud.automl_v1.types import model as gca_model
from google.cloud.automl_v1.types import model_evaluation as gca_model_evaluation
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.automl.v1',
    manifest={
        'CreateDatasetRequest',
        'GetDatasetRequest',
        'ListDatasetsRequest',
        'ListDatasetsResponse',
        'UpdateDatasetRequest',
        'DeleteDatasetRequest',
        'ImportDataRequest',
        'ExportDataRequest',
        'GetAnnotationSpecRequest',
        'CreateModelRequest',
        'GetModelRequest',
        'ListModelsRequest',
        'ListModelsResponse',
        'DeleteModelRequest',
        'UpdateModelRequest',
        'DeployModelRequest',
        'UndeployModelRequest',
        'ExportModelRequest',
        'GetModelEvaluationRequest',
        'ListModelEvaluationsRequest',
        'ListModelEvaluationsResponse',
    },
)


class CreateDatasetRequest(proto.Message):
    r"""Request message for
    [AutoMl.CreateDataset][google.cloud.automl.v1.AutoMl.CreateDataset].

    Attributes:
        parent (str):
            Required. The resource name of the project to
            create the dataset for.
        dataset (google.cloud.automl_v1.types.Dataset):
            Required. The dataset to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset: gca_dataset.Dataset = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gca_dataset.Dataset,
    )


class GetDatasetRequest(proto.Message):
    r"""Request message for
    [AutoMl.GetDataset][google.cloud.automl.v1.AutoMl.GetDataset].

    Attributes:
        name (str):
            Required. The resource name of the dataset to
            retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListDatasetsRequest(proto.Message):
    r"""Request message for
    [AutoMl.ListDatasets][google.cloud.automl.v1.AutoMl.ListDatasets].

    Attributes:
        parent (str):
            Required. The resource name of the project
            from which to list datasets.
        filter (str):
            An expression for filtering the results of the request.

            -  ``dataset_metadata`` - for existence of the case (e.g.
               ``image_classification_dataset_metadata:*``). Some
               examples of using the filter are:

            -  ``translation_dataset_metadata:*`` --> The dataset has
               ``translation_dataset_metadata``.
        page_size (int):
            Requested page size. Server may return fewer
            results than requested. If unspecified, server
            will pick a default size.
        page_token (str):
            A token identifying a page of results for the server to
            return Typically obtained via
            [ListDatasetsResponse.next_page_token][google.cloud.automl.v1.ListDatasetsResponse.next_page_token]
            of the previous
            [AutoMl.ListDatasets][google.cloud.automl.v1.AutoMl.ListDatasets]
            call.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=3,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=4,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListDatasetsResponse(proto.Message):
    r"""Response message for
    [AutoMl.ListDatasets][google.cloud.automl.v1.AutoMl.ListDatasets].

    Attributes:
        datasets (MutableSequence[google.cloud.automl_v1.types.Dataset]):
            The datasets read.
        next_page_token (str):
            A token to retrieve next page of results. Pass to
            [ListDatasetsRequest.page_token][google.cloud.automl.v1.ListDatasetsRequest.page_token]
            to obtain that page.
    """

    @property
    def raw_page(self):
        return self

    datasets: MutableSequence[gca_dataset.Dataset] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gca_dataset.Dataset,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class UpdateDatasetRequest(proto.Message):
    r"""Request message for
    [AutoMl.UpdateDataset][google.cloud.automl.v1.AutoMl.UpdateDataset]

    Attributes:
        dataset (google.cloud.automl_v1.types.Dataset):
            Required. The dataset which replaces the
            resource on the server.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The update mask applies to the
            resource.
    """

    dataset: gca_dataset.Dataset = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gca_dataset.Dataset,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteDatasetRequest(proto.Message):
    r"""Request message for
    [AutoMl.DeleteDataset][google.cloud.automl.v1.AutoMl.DeleteDataset].

    Attributes:
        name (str):
            Required. The resource name of the dataset to
            delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ImportDataRequest(proto.Message):
    r"""Request message for
    [AutoMl.ImportData][google.cloud.automl.v1.AutoMl.ImportData].

    Attributes:
        name (str):
            Required. Dataset name. Dataset must already
            exist. All imported annotations and examples
            will be added.
        input_config (google.cloud.automl_v1.types.InputConfig):
            Required. The desired input location and its
            domain specific semantics, if any.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    input_config: io.InputConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        message=io.InputConfig,
    )


class ExportDataRequest(proto.Message):
    r"""Request message for
    [AutoMl.ExportData][google.cloud.automl.v1.AutoMl.ExportData].

    Attributes:
        name (str):
            Required. The resource name of the dataset.
        output_config (google.cloud.automl_v1.types.OutputConfig):
            Required. The desired output location.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    output_config: io.OutputConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        message=io.OutputConfig,
    )


class GetAnnotationSpecRequest(proto.Message):
    r"""Request message for
    [AutoMl.GetAnnotationSpec][google.cloud.automl.v1.AutoMl.GetAnnotationSpec].

    Attributes:
        name (str):
            Required. The resource name of the annotation
            spec to retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateModelRequest(proto.Message):
    r"""Request message for
    [AutoMl.CreateModel][google.cloud.automl.v1.AutoMl.CreateModel].

    Attributes:
        parent (str):
            Required. Resource name of the parent project
            where the model is being created.
        model (google.cloud.automl_v1.types.Model):
            Required. The model to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    model: gca_model.Model = proto.Field(
        proto.MESSAGE,
        number=4,
        message=gca_model.Model,
    )


class GetModelRequest(proto.Message):
    r"""Request message for
    [AutoMl.GetModel][google.cloud.automl.v1.AutoMl.GetModel].

    Attributes:
        name (str):
            Required. Resource name of the model.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListModelsRequest(proto.Message):
    r"""Request message for
    [AutoMl.ListModels][google.cloud.automl.v1.AutoMl.ListModels].

    Attributes:
        parent (str):
            Required. Resource name of the project, from
            which to list the models.
        filter (str):
            An expression for filtering the results of the request.

            -  ``model_metadata`` - for existence of the case (e.g.
               ``video_classification_model_metadata:*``).

            -  ``dataset_id`` - for = or !=. Some examples of using the
               filter are:

            -  ``image_classification_model_metadata:*`` --> The model
               has ``image_classification_model_metadata``.

            -  ``dataset_id=5`` --> The model was created from a dataset
               with ID 5.
        page_size (int):
            Requested page size.
        page_token (str):
            A token identifying a page of results for the server to
            return Typically obtained via
            [ListModelsResponse.next_page_token][google.cloud.automl.v1.ListModelsResponse.next_page_token]
            of the previous
            [AutoMl.ListModels][google.cloud.automl.v1.AutoMl.ListModels]
            call.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=3,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=4,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListModelsResponse(proto.Message):
    r"""Response message for
    [AutoMl.ListModels][google.cloud.automl.v1.AutoMl.ListModels].

    Attributes:
        model (MutableSequence[google.cloud.automl_v1.types.Model]):
            List of models in the requested page.
        next_page_token (str):
            A token to retrieve next page of results. Pass to
            [ListModelsRequest.page_token][google.cloud.automl.v1.ListModelsRequest.page_token]
            to obtain that page.
    """

    @property
    def raw_page(self):
        return self

    model: MutableSequence[gca_model.Model] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gca_model.Model,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteModelRequest(proto.Message):
    r"""Request message for
    [AutoMl.DeleteModel][google.cloud.automl.v1.AutoMl.DeleteModel].

    Attributes:
        name (str):
            Required. Resource name of the model being
            deleted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateModelRequest(proto.Message):
    r"""Request message for
    [AutoMl.UpdateModel][google.cloud.automl.v1.AutoMl.UpdateModel]

    Attributes:
        model (google.cloud.automl_v1.types.Model):
            Required. The model which replaces the
            resource on the server.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The update mask applies to the
            resource.
    """

    model: gca_model.Model = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gca_model.Model,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeployModelRequest(proto.Message):
    r"""Request message for
    [AutoMl.DeployModel][google.cloud.automl.v1.AutoMl.DeployModel].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        image_object_detection_model_deployment_metadata (google.cloud.automl_v1.types.ImageObjectDetectionModelDeploymentMetadata):
            Model deployment metadata specific to Image
            Object Detection.

            This field is a member of `oneof`_ ``model_deployment_metadata``.
        image_classification_model_deployment_metadata (google.cloud.automl_v1.types.ImageClassificationModelDeploymentMetadata):
            Model deployment metadata specific to Image
            Classification.

            This field is a member of `oneof`_ ``model_deployment_metadata``.
        name (str):
            Required. Resource name of the model to
            deploy.
    """

    image_object_detection_model_deployment_metadata: image.ImageObjectDetectionModelDeploymentMetadata = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof='model_deployment_metadata',
        message=image.ImageObjectDetectionModelDeploymentMetadata,
    )
    image_classification_model_deployment_metadata: image.ImageClassificationModelDeploymentMetadata = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof='model_deployment_metadata',
        message=image.ImageClassificationModelDeploymentMetadata,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UndeployModelRequest(proto.Message):
    r"""Request message for
    [AutoMl.UndeployModel][google.cloud.automl.v1.AutoMl.UndeployModel].

    Attributes:
        name (str):
            Required. Resource name of the model to
            undeploy.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ExportModelRequest(proto.Message):
    r"""Request message for
    [AutoMl.ExportModel][google.cloud.automl.v1.AutoMl.ExportModel].
    Models need to be enabled for exporting, otherwise an error code
    will be returned.

    Attributes:
        name (str):
            Required. The resource name of the model to
            export.
        output_config (google.cloud.automl_v1.types.ModelExportOutputConfig):
            Required. The desired output location and
            configuration.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    output_config: io.ModelExportOutputConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        message=io.ModelExportOutputConfig,
    )


class GetModelEvaluationRequest(proto.Message):
    r"""Request message for
    [AutoMl.GetModelEvaluation][google.cloud.automl.v1.AutoMl.GetModelEvaluation].

    Attributes:
        name (str):
            Required. Resource name for the model
            evaluation.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListModelEvaluationsRequest(proto.Message):
    r"""Request message for
    [AutoMl.ListModelEvaluations][google.cloud.automl.v1.AutoMl.ListModelEvaluations].

    Attributes:
        parent (str):
            Required. Resource name of the model to list
            the model evaluations for. If modelId is set as
            "-", this will list model evaluations from
            across all models of the parent location.
        filter (str):
            Required. An expression for filtering the results of the
            request.

            -  ``annotation_spec_id`` - for =, != or existence. See
               example below for the last.

            Some examples of using the filter are:

            -  ``annotation_spec_id!=4`` --> The model evaluation was
               done for annotation spec with ID different than 4.
            -  ``NOT annotation_spec_id:*`` --> The model evaluation was
               done for aggregate of all annotation specs.
        page_size (int):
            Requested page size.
        page_token (str):
            A token identifying a page of results for the server to
            return. Typically obtained via
            [ListModelEvaluationsResponse.next_page_token][google.cloud.automl.v1.ListModelEvaluationsResponse.next_page_token]
            of the previous
            [AutoMl.ListModelEvaluations][google.cloud.automl.v1.AutoMl.ListModelEvaluations]
            call.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=3,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=4,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListModelEvaluationsResponse(proto.Message):
    r"""Response message for
    [AutoMl.ListModelEvaluations][google.cloud.automl.v1.AutoMl.ListModelEvaluations].

    Attributes:
        model_evaluation (MutableSequence[google.cloud.automl_v1.types.ModelEvaluation]):
            List of model evaluations in the requested
            page.
        next_page_token (str):
            A token to retrieve next page of results. Pass to the
            [ListModelEvaluationsRequest.page_token][google.cloud.automl.v1.ListModelEvaluationsRequest.page_token]
            field of a new
            [AutoMl.ListModelEvaluations][google.cloud.automl.v1.AutoMl.ListModelEvaluations]
            request to obtain that page.
    """

    @property
    def raw_page(self):
        return self

    model_evaluation: MutableSequence[gca_model_evaluation.ModelEvaluation] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gca_model_evaluation.ModelEvaluation,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
