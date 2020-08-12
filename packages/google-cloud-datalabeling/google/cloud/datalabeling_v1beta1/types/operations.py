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


from google.cloud.datalabeling_v1beta1.types import dataset as gcd_dataset
from google.cloud.datalabeling_v1beta1.types import human_annotation_config
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.datalabeling.v1beta1",
    manifest={
        "ImportDataOperationResponse",
        "ExportDataOperationResponse",
        "ImportDataOperationMetadata",
        "ExportDataOperationMetadata",
        "LabelOperationMetadata",
        "LabelImageClassificationOperationMetadata",
        "LabelImageBoundingBoxOperationMetadata",
        "LabelImageOrientedBoundingBoxOperationMetadata",
        "LabelImageBoundingPolyOperationMetadata",
        "LabelImagePolylineOperationMetadata",
        "LabelImageSegmentationOperationMetadata",
        "LabelVideoClassificationOperationMetadata",
        "LabelVideoObjectDetectionOperationMetadata",
        "LabelVideoObjectTrackingOperationMetadata",
        "LabelVideoEventOperationMetadata",
        "LabelTextClassificationOperationMetadata",
        "LabelTextEntityExtractionOperationMetadata",
        "CreateInstructionMetadata",
    },
)


class ImportDataOperationResponse(proto.Message):
    r"""Response used for ImportData longrunning operation.

    Attributes:
        dataset (str):
            Ouptut only. The name of imported dataset.
        total_count (int):
            Output only. Total number of examples
            requested to import
        import_count (int):
            Output only. Number of examples imported
            successfully.
    """

    dataset = proto.Field(proto.STRING, number=1)

    total_count = proto.Field(proto.INT32, number=2)

    import_count = proto.Field(proto.INT32, number=3)


class ExportDataOperationResponse(proto.Message):
    r"""Response used for ExportDataset longrunning operation.

    Attributes:
        dataset (str):
            Ouptut only. The name of dataset. "projects/*/datasets/*".
        total_count (int):
            Output only. Total number of examples
            requested to export
        export_count (int):
            Output only. Number of examples exported
            successfully.
        label_stats (~.gcd_dataset.LabelStats):
            Output only. Statistic infos of labels in the
            exported dataset.
        output_config (~.gcd_dataset.OutputConfig):
            Output only. output_config in the ExportData request.
    """

    dataset = proto.Field(proto.STRING, number=1)

    total_count = proto.Field(proto.INT32, number=2)

    export_count = proto.Field(proto.INT32, number=3)

    label_stats = proto.Field(proto.MESSAGE, number=4, message=gcd_dataset.LabelStats,)

    output_config = proto.Field(
        proto.MESSAGE, number=5, message=gcd_dataset.OutputConfig,
    )


class ImportDataOperationMetadata(proto.Message):
    r"""Metadata of an ImportData operation.

    Attributes:
        dataset (str):
            Output only. The name of imported dataset.
            "projects/*/datasets/*".
        partial_failures (Sequence[~.status.Status]):
            Output only. Partial failures encountered.
            E.g. single files that couldn't be read.
            Status details field will contain standard GCP
            error details.
        create_time (~.timestamp.Timestamp):
            Output only. Timestamp when import dataset
            request was created.
    """

    dataset = proto.Field(proto.STRING, number=1)

    partial_failures = proto.RepeatedField(
        proto.MESSAGE, number=2, message=status.Status,
    )

    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)


class ExportDataOperationMetadata(proto.Message):
    r"""Metadata of an ExportData operation.

    Attributes:
        dataset (str):
            Output only. The name of dataset to be exported.
            "projects/*/datasets/*".
        partial_failures (Sequence[~.status.Status]):
            Output only. Partial failures encountered.
            E.g. single files that couldn't be read.
            Status details field will contain standard GCP
            error details.
        create_time (~.timestamp.Timestamp):
            Output only. Timestamp when export dataset
            request was created.
    """

    dataset = proto.Field(proto.STRING, number=1)

    partial_failures = proto.RepeatedField(
        proto.MESSAGE, number=2, message=status.Status,
    )

    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)


class LabelOperationMetadata(proto.Message):
    r"""Metadata of a labeling operation, such as LabelImage or
    LabelVideo. Next tag: 20

    Attributes:
        image_classification_details (~.operations.LabelImageClassificationOperationMetadata):
            Details of label image classification
            operation.
        image_bounding_box_details (~.operations.LabelImageBoundingBoxOperationMetadata):
            Details of label image bounding box
            operation.
        image_bounding_poly_details (~.operations.LabelImageBoundingPolyOperationMetadata):
            Details of label image bounding poly
            operation.
        image_oriented_bounding_box_details (~.operations.LabelImageOrientedBoundingBoxOperationMetadata):
            Details of label image oriented bounding box
            operation.
        image_polyline_details (~.operations.LabelImagePolylineOperationMetadata):
            Details of label image polyline operation.
        image_segmentation_details (~.operations.LabelImageSegmentationOperationMetadata):
            Details of label image segmentation
            operation.
        video_classification_details (~.operations.LabelVideoClassificationOperationMetadata):
            Details of label video classification
            operation.
        video_object_detection_details (~.operations.LabelVideoObjectDetectionOperationMetadata):
            Details of label video object detection
            operation.
        video_object_tracking_details (~.operations.LabelVideoObjectTrackingOperationMetadata):
            Details of label video object tracking
            operation.
        video_event_details (~.operations.LabelVideoEventOperationMetadata):
            Details of label video event operation.
        text_classification_details (~.operations.LabelTextClassificationOperationMetadata):
            Details of label text classification
            operation.
        text_entity_extraction_details (~.operations.LabelTextEntityExtractionOperationMetadata):
            Details of label text entity extraction
            operation.
        progress_percent (int):
            Output only. Progress of label operation. Range: [0, 100].
        partial_failures (Sequence[~.status.Status]):
            Output only. Partial failures encountered.
            E.g. single files that couldn't be read.
            Status details field will contain standard GCP
            error details.
        create_time (~.timestamp.Timestamp):
            Output only. Timestamp when labeling request
            was created.
    """

    image_classification_details = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="details",
        message="LabelImageClassificationOperationMetadata",
    )

    image_bounding_box_details = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="details",
        message="LabelImageBoundingBoxOperationMetadata",
    )

    image_bounding_poly_details = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="details",
        message="LabelImageBoundingPolyOperationMetadata",
    )

    image_oriented_bounding_box_details = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="details",
        message="LabelImageOrientedBoundingBoxOperationMetadata",
    )

    image_polyline_details = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="details",
        message="LabelImagePolylineOperationMetadata",
    )

    image_segmentation_details = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="details",
        message="LabelImageSegmentationOperationMetadata",
    )

    video_classification_details = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="details",
        message="LabelVideoClassificationOperationMetadata",
    )

    video_object_detection_details = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="details",
        message="LabelVideoObjectDetectionOperationMetadata",
    )

    video_object_tracking_details = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="details",
        message="LabelVideoObjectTrackingOperationMetadata",
    )

    video_event_details = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="details",
        message="LabelVideoEventOperationMetadata",
    )

    text_classification_details = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="details",
        message="LabelTextClassificationOperationMetadata",
    )

    text_entity_extraction_details = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="details",
        message="LabelTextEntityExtractionOperationMetadata",
    )

    progress_percent = proto.Field(proto.INT32, number=1)

    partial_failures = proto.RepeatedField(
        proto.MESSAGE, number=2, message=status.Status,
    )

    create_time = proto.Field(proto.MESSAGE, number=16, message=timestamp.Timestamp,)


class LabelImageClassificationOperationMetadata(proto.Message):
    r"""Metadata of a LabelImageClassification operation.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelImageBoundingBoxOperationMetadata(proto.Message):
    r"""Details of a LabelImageBoundingBox operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelImageOrientedBoundingBoxOperationMetadata(proto.Message):
    r"""Details of a LabelImageOrientedBoundingBox operation
    metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelImageBoundingPolyOperationMetadata(proto.Message):
    r"""Details of LabelImageBoundingPoly operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelImagePolylineOperationMetadata(proto.Message):
    r"""Details of LabelImagePolyline operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelImageSegmentationOperationMetadata(proto.Message):
    r"""Details of a LabelImageSegmentation operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelVideoClassificationOperationMetadata(proto.Message):
    r"""Details of a LabelVideoClassification operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelVideoObjectDetectionOperationMetadata(proto.Message):
    r"""Details of a LabelVideoObjectDetection operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelVideoObjectTrackingOperationMetadata(proto.Message):
    r"""Details of a LabelVideoObjectTracking operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelVideoEventOperationMetadata(proto.Message):
    r"""Details of a LabelVideoEvent operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelTextClassificationOperationMetadata(proto.Message):
    r"""Details of a LabelTextClassification operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class LabelTextEntityExtractionOperationMetadata(proto.Message):
    r"""Details of a LabelTextEntityExtraction operation metadata.

    Attributes:
        basic_config (~.human_annotation_config.HumanAnnotationConfig):
            Basic human annotation config used in
            labeling request.
    """

    basic_config = proto.Field(
        proto.MESSAGE, number=1, message=human_annotation_config.HumanAnnotationConfig,
    )


class CreateInstructionMetadata(proto.Message):
    r"""Metadata of a CreateInstruction operation.

    Attributes:
        instruction (str):
            The name of the created Instruction.
            projects/{project_id}/instructions/{instruction_id}
        partial_failures (Sequence[~.status.Status]):
            Partial failures encountered.
            E.g. single files that couldn't be read.
            Status details field will contain standard GCP
            error details.
        create_time (~.timestamp.Timestamp):
            Timestamp when create instruction request was
            created.
    """

    instruction = proto.Field(proto.STRING, number=1)

    partial_failures = proto.RepeatedField(
        proto.MESSAGE, number=2, message=status.Status,
    )

    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
