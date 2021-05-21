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

from google.cloud.automl_v1beta1.types import text_segment as gca_text_segment


__protobuf__ = proto.module(
    package="google.cloud.automl.v1beta1",
    manifest={"TextExtractionAnnotation", "TextExtractionEvaluationMetrics",},
)


class TextExtractionAnnotation(proto.Message):
    r"""Annotation for identifying spans of text.
    Attributes:
        text_segment (google.cloud.automl_v1beta1.types.TextSegment):
            An entity annotation will set this, which is
            the part of the original text to which the
            annotation pertains.
        score (float):
            Output only. A confidence estimate between
            0.0 and 1.0. A higher value means greater
            confidence in correctness of the annotation.
    """

    text_segment = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="annotation",
        message=gca_text_segment.TextSegment,
    )
    score = proto.Field(proto.FLOAT, number=1,)


class TextExtractionEvaluationMetrics(proto.Message):
    r"""Model evaluation metrics for text extraction problems.
    Attributes:
        au_prc (float):
            Output only. The Area under precision recall
            curve metric.
        confidence_metrics_entries (Sequence[google.cloud.automl_v1beta1.types.TextExtractionEvaluationMetrics.ConfidenceMetricsEntry]):
            Output only. Metrics that have confidence
            thresholds. Precision-recall curve can be
            derived from it.
    """

    class ConfidenceMetricsEntry(proto.Message):
        r"""Metrics for a single confidence threshold.
        Attributes:
            confidence_threshold (float):
                Output only. The confidence threshold value
                used to compute the metrics. Only annotations
                with score of at least this threshold are
                considered to be ones the model would return.
            recall (float):
                Output only. Recall under the given
                confidence threshold.
            precision (float):
                Output only. Precision under the given
                confidence threshold.
            f1_score (float):
                Output only. The harmonic mean of recall and
                precision.
        """

        confidence_threshold = proto.Field(proto.FLOAT, number=1,)
        recall = proto.Field(proto.FLOAT, number=3,)
        precision = proto.Field(proto.FLOAT, number=4,)
        f1_score = proto.Field(proto.FLOAT, number=5,)

    au_prc = proto.Field(proto.FLOAT, number=1,)
    confidence_metrics_entries = proto.RepeatedField(
        proto.MESSAGE, number=2, message=ConfidenceMetricsEntry,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
