# Copyright 2019, Google LLC All rights reserved.
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

"""System tests for VideoIntelligence API."""

import pytest

from google.cloud import videointelligence_v1
from test_utils.retry import RetryResult


INPUT_URI = "gs://cloud-samples-data/video/cat.mp4"


@pytest.fixture(scope="module")
def client():
    return videointelligence_v1.VideoIntelligenceServiceClient()


def test_annotate_video(client):
    features_element = videointelligence_v1.enums.Feature.LABEL_DETECTION
    features = [features_element]
    response = client.annotate_video(input_uri=INPUT_URI, features=features)

    retry = RetryResult(result_predicate=bool, max_tries=7)
    retry(response.done)()

    result = response.result()
    annotations = result.annotation_results[0]
    assert len(annotations.segment_label_annotations) > 0
