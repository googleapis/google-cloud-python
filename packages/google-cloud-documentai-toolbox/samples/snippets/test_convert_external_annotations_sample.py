# Copyright 2023 Google LLC
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

import os

import pytest
from samples.snippets import convert_external_annotations_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_convert_external_annotations_sample(capsys: pytest.CaptureFixture) -> None:
    convert_external_annotations_sample.convert_external_annotations_sample(
        location=location,
        processor_id="52a38e080c1a7296",
        project_id=project_id,
        gcs_input_path="gs://documentai_toolbox_samples/converter/azure",
        gcs_output_path="gs://documentai_toolbox_samples/converter/output",
    )
    out, _ = capsys.readouterr()

    assert "-------- Finished Converting --------" in out
