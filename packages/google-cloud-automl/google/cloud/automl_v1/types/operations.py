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
import proto  # type: ignore

from google.cloud.automl_v1.types import io
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.automl.v1",
    manifest={
        "OperationMetadata",
        "DeleteOperationMetadata",
        "DeployModelOperationMetadata",
        "UndeployModelOperationMetadata",
        "CreateDatasetOperationMetadata",
        "CreateModelOperationMetadata",
        "ImportDataOperationMetadata",
        "ExportDataOperationMetadata",
        "BatchPredictOperationMetadata",
        "ExportModelOperationMetadata",
    },
)


class OperationMetadata(proto.Message):
    r"""Metadata used across all long running operations returned by
    AutoML API.

    Attributes:
        delete_details (google.cloud.automl_v1.types.DeleteOperationMetadata):
            Details of a Delete operation.
        deploy_model_details (google.cloud.automl_v1.types.DeployModelOperationMetadata):
            Details of a DeployModel operation.
        undeploy_model_details (google.cloud.automl_v1.types.UndeployModelOperationMetadata):
            Details of an UndeployModel operation.
        create_model_details (google.cloud.automl_v1.types.CreateModelOperationMetadata):
            Details of CreateModel operation.
        create_dataset_details (google.cloud.automl_v1.types.CreateDatasetOperationMetadata):
            Details of CreateDataset operation.
        import_data_details (google.cloud.automl_v1.types.ImportDataOperationMetadata):
            Details of ImportData operation.
        batch_predict_details (google.cloud.automl_v1.types.BatchPredictOperationMetadata):
            Details of BatchPredict operation.
        export_data_details (google.cloud.automl_v1.types.ExportDataOperationMetadata):
            Details of ExportData operation.
        export_model_details (google.cloud.automl_v1.types.ExportModelOperationMetadata):
            Details of ExportModel operation.
        progress_percent (int):
            Output only. Progress of operation. Range: [0, 100]. Not
            used currently.
        partial_failures (Sequence[google.rpc.status_pb2.Status]):
            Output only. Partial failures encountered.
            E.g. single files that couldn't be read.
            This field should never exceed 20 entries.
            Status details field will contain standard GCP
            error details.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the operation was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the operation was
            updated for the last time.
    """

    delete_details = proto.Field(
        proto.MESSAGE, number=8, oneof="details", message="DeleteOperationMetadata",
    )
    deploy_model_details = proto.Field(
        proto.MESSAGE,
        number=24,
        oneof="details",
        message="DeployModelOperationMetadata",
    )
    undeploy_model_details = proto.Field(
        proto.MESSAGE,
        number=25,
        oneof="details",
        message="UndeployModelOperationMetadata",
    )
    create_model_details = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="details",
        message="CreateModelOperationMetadata",
    )
    create_dataset_details = proto.Field(
        proto.MESSAGE,
        number=30,
        oneof="details",
        message="CreateDatasetOperationMetadata",
    )
    import_data_details = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="details",
        message="ImportDataOperationMetadata",
    )
    batch_predict_details = proto.Field(
        proto.MESSAGE,
        number=16,
        oneof="details",
        message="BatchPredictOperationMetadata",
    )
    export_data_details = proto.Field(
        proto.MESSAGE,
        number=21,
        oneof="details",
        message="ExportDataOperationMetadata",
    )
    export_model_details = proto.Field(
        proto.MESSAGE,
        number=22,
        oneof="details",
        message="ExportModelOperationMetadata",
    )
    progress_percent = proto.Field(proto.INT32, number=13,)
    partial_failures = proto.RepeatedField(
        proto.MESSAGE, number=2, message=status_pb2.Status,
    )
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)


class DeleteOperationMetadata(proto.Message):
    r"""Details of operations that perform deletes of any entities.    """


class DeployModelOperationMetadata(proto.Message):
    r"""Details of DeployModel operation.    """


class UndeployModelOperationMetadata(proto.Message):
    r"""Details of UndeployModel operation.    """


class CreateDatasetOperationMetadata(proto.Message):
    r"""Details of CreateDataset operation.    """


class CreateModelOperationMetadata(proto.Message):
    r"""Details of CreateModel operation.    """


class ImportDataOperationMetadata(proto.Message):
    r"""Details of ImportData operation.    """


class ExportDataOperationMetadata(proto.Message):
    r"""Details of ExportData operation.
    Attributes:
        output_info (google.cloud.automl_v1.types.ExportDataOperationMetadata.ExportDataOutputInfo):
            Output only. Information further describing
            this export data's output.
    """

    class ExportDataOutputInfo(proto.Message):
        r"""Further describes this export data's output. Supplements
        [OutputConfig][google.cloud.automl.v1.OutputConfig].

        Attributes:
            gcs_output_directory (str):
                The full path of the Google Cloud Storage
                directory created, into which the exported data
                is written.
        """

        gcs_output_directory = proto.Field(
            proto.STRING, number=1, oneof="output_location",
        )

    output_info = proto.Field(proto.MESSAGE, number=1, message=ExportDataOutputInfo,)


class BatchPredictOperationMetadata(proto.Message):
    r"""Details of BatchPredict operation.
    Attributes:
        input_config (google.cloud.automl_v1.types.BatchPredictInputConfig):
            Output only. The input config that was given
            upon starting this batch predict operation.
        output_info (google.cloud.automl_v1.types.BatchPredictOperationMetadata.BatchPredictOutputInfo):
            Output only. Information further describing
            this batch predict's output.
    """

    class BatchPredictOutputInfo(proto.Message):
        r"""Further describes this batch predict's output. Supplements

        [BatchPredictOutputConfig][google.cloud.automl.v1.BatchPredictOutputConfig].

        Attributes:
            gcs_output_directory (str):
                The full path of the Google Cloud Storage
                directory created, into which the prediction
                output is written.
        """

        gcs_output_directory = proto.Field(
            proto.STRING, number=1, oneof="output_location",
        )

    input_config = proto.Field(
        proto.MESSAGE, number=1, message=io.BatchPredictInputConfig,
    )
    output_info = proto.Field(proto.MESSAGE, number=2, message=BatchPredictOutputInfo,)


class ExportModelOperationMetadata(proto.Message):
    r"""Details of ExportModel operation.
    Attributes:
        output_info (google.cloud.automl_v1.types.ExportModelOperationMetadata.ExportModelOutputInfo):
            Output only. Information further describing
            the output of this model export.
    """

    class ExportModelOutputInfo(proto.Message):
        r"""Further describes the output of model export. Supplements
        [ModelExportOutputConfig][google.cloud.automl.v1.ModelExportOutputConfig].

        Attributes:
            gcs_output_directory (str):
                The full path of the Google Cloud Storage
                directory created, into which the model will be
                exported.
        """

        gcs_output_directory = proto.Field(proto.STRING, number=1,)

    output_info = proto.Field(proto.MESSAGE, number=2, message=ExportModelOutputInfo,)


__all__ = tuple(sorted(__protobuf__.manifest))
