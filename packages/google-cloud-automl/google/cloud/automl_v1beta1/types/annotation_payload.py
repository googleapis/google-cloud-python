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

from google.cloud.automl_v1beta1.types import classification as gca_classification
from google.cloud.automl_v1beta1.types import detection
from google.cloud.automl_v1beta1.types import tables as gca_tables
from google.cloud.automl_v1beta1.types import text_extraction as gca_text_extraction
from google.cloud.automl_v1beta1.types import text_sentiment as gca_text_sentiment
from google.cloud.automl_v1beta1.types import translation as gca_translation


__protobuf__ = proto.module(
    package="google.cloud.automl.v1beta1", manifest={"AnnotationPayload",},
)


class AnnotationPayload(proto.Message):
    r"""Contains annotation information that is relevant to AutoML.
    Attributes:
        translation (google.cloud.automl_v1beta1.types.TranslationAnnotation):
            Annotation details for translation.
        classification (google.cloud.automl_v1beta1.types.ClassificationAnnotation):
            Annotation details for content or image
            classification.
        image_object_detection (google.cloud.automl_v1beta1.types.ImageObjectDetectionAnnotation):
            Annotation details for image object
            detection.
        video_classification (google.cloud.automl_v1beta1.types.VideoClassificationAnnotation):
            Annotation details for video classification.
            Returned for Video Classification predictions.
        video_object_tracking (google.cloud.automl_v1beta1.types.VideoObjectTrackingAnnotation):
            Annotation details for video object tracking.
        text_extraction (google.cloud.automl_v1beta1.types.TextExtractionAnnotation):
            Annotation details for text extraction.
        text_sentiment (google.cloud.automl_v1beta1.types.TextSentimentAnnotation):
            Annotation details for text sentiment.
        tables (google.cloud.automl_v1beta1.types.TablesAnnotation):
            Annotation details for Tables.
        annotation_spec_id (str):
            Output only . The resource ID of the
            annotation spec that this annotation pertains
            to. The annotation spec comes from either an
            ancestor dataset, or the dataset that was used
            to train the model in use.
        display_name (str):
            Output only. The value of
            [display_name][google.cloud.automl.v1beta1.AnnotationSpec.display_name]
            when the model was trained. Because this field returns a
            value at model training time, for different models trained
            using the same dataset, the returned value could be
            different as model owner could update the ``display_name``
            between any two model training.
    """

    translation = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="detail",
        message=gca_translation.TranslationAnnotation,
    )
    classification = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="detail",
        message=gca_classification.ClassificationAnnotation,
    )
    image_object_detection = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="detail",
        message=detection.ImageObjectDetectionAnnotation,
    )
    video_classification = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="detail",
        message=gca_classification.VideoClassificationAnnotation,
    )
    video_object_tracking = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="detail",
        message=detection.VideoObjectTrackingAnnotation,
    )
    text_extraction = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="detail",
        message=gca_text_extraction.TextExtractionAnnotation,
    )
    text_sentiment = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="detail",
        message=gca_text_sentiment.TextSentimentAnnotation,
    )
    tables = proto.Field(
        proto.MESSAGE, number=10, oneof="detail", message=gca_tables.TablesAnnotation,
    )
    annotation_spec_id = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=5,)


__all__ = tuple(sorted(__protobuf__.manifest))
