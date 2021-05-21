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

from google.cloud.automl_v1beta1.types import image
from google.cloud.automl_v1beta1.types import tables
from google.cloud.automl_v1beta1.types import text
from google.cloud.automl_v1beta1.types import translation
from google.cloud.automl_v1beta1.types import video
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.automl.v1beta1", manifest={"Dataset",},
)


class Dataset(proto.Message):
    r"""A workspace for solving a single, particular machine learning
    (ML) problem. A workspace contains examples that may be
    annotated.

    Attributes:
        translation_dataset_metadata (google.cloud.automl_v1beta1.types.TranslationDatasetMetadata):
            Metadata for a dataset used for translation.
        image_classification_dataset_metadata (google.cloud.automl_v1beta1.types.ImageClassificationDatasetMetadata):
            Metadata for a dataset used for image
            classification.
        text_classification_dataset_metadata (google.cloud.automl_v1beta1.types.TextClassificationDatasetMetadata):
            Metadata for a dataset used for text
            classification.
        image_object_detection_dataset_metadata (google.cloud.automl_v1beta1.types.ImageObjectDetectionDatasetMetadata):
            Metadata for a dataset used for image object
            detection.
        video_classification_dataset_metadata (google.cloud.automl_v1beta1.types.VideoClassificationDatasetMetadata):
            Metadata for a dataset used for video
            classification.
        video_object_tracking_dataset_metadata (google.cloud.automl_v1beta1.types.VideoObjectTrackingDatasetMetadata):
            Metadata for a dataset used for video object
            tracking.
        text_extraction_dataset_metadata (google.cloud.automl_v1beta1.types.TextExtractionDatasetMetadata):
            Metadata for a dataset used for text
            extraction.
        text_sentiment_dataset_metadata (google.cloud.automl_v1beta1.types.TextSentimentDatasetMetadata):
            Metadata for a dataset used for text
            sentiment.
        tables_dataset_metadata (google.cloud.automl_v1beta1.types.TablesDatasetMetadata):
            Metadata for a dataset used for Tables.
        name (str):
            Output only. The resource name of the dataset. Form:
            ``projects/{project_id}/locations/{location_id}/datasets/{dataset_id}``
        display_name (str):
            Required. The name of the dataset to show in the interface.
            The name can be up to 32 characters long and can consist
            only of ASCII Latin letters A-Z and a-z, underscores (_),
            and ASCII digits 0-9.
        description (str):
            User-provided description of the dataset. The
            description can be up to 25000 characters long.
        example_count (int):
            Output only. The number of examples in the
            dataset.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this dataset was
            created.
        etag (str):
            Used to perform consistent read-modify-write
            updates. If not set, a blind "overwrite" update
            happens.
    """

    translation_dataset_metadata = proto.Field(
        proto.MESSAGE,
        number=23,
        oneof="dataset_metadata",
        message=translation.TranslationDatasetMetadata,
    )
    image_classification_dataset_metadata = proto.Field(
        proto.MESSAGE,
        number=24,
        oneof="dataset_metadata",
        message=image.ImageClassificationDatasetMetadata,
    )
    text_classification_dataset_metadata = proto.Field(
        proto.MESSAGE,
        number=25,
        oneof="dataset_metadata",
        message=text.TextClassificationDatasetMetadata,
    )
    image_object_detection_dataset_metadata = proto.Field(
        proto.MESSAGE,
        number=26,
        oneof="dataset_metadata",
        message=image.ImageObjectDetectionDatasetMetadata,
    )
    video_classification_dataset_metadata = proto.Field(
        proto.MESSAGE,
        number=31,
        oneof="dataset_metadata",
        message=video.VideoClassificationDatasetMetadata,
    )
    video_object_tracking_dataset_metadata = proto.Field(
        proto.MESSAGE,
        number=29,
        oneof="dataset_metadata",
        message=video.VideoObjectTrackingDatasetMetadata,
    )
    text_extraction_dataset_metadata = proto.Field(
        proto.MESSAGE,
        number=28,
        oneof="dataset_metadata",
        message=text.TextExtractionDatasetMetadata,
    )
    text_sentiment_dataset_metadata = proto.Field(
        proto.MESSAGE,
        number=30,
        oneof="dataset_metadata",
        message=text.TextSentimentDatasetMetadata,
    )
    tables_dataset_metadata = proto.Field(
        proto.MESSAGE,
        number=33,
        oneof="dataset_metadata",
        message=tables.TablesDatasetMetadata,
    )
    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    example_count = proto.Field(proto.INT32, number=21,)
    create_time = proto.Field(
        proto.MESSAGE, number=14, message=timestamp_pb2.Timestamp,
    )
    etag = proto.Field(proto.STRING, number=17,)


__all__ = tuple(sorted(__protobuf__.manifest))
