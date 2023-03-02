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
from samples.snippets import quickstart_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
gcs_bucket_name = "documentai_toolbox_samples"
gcs_input_uri = "output/123456789/0"


def test_quickstart_sample(capsys: pytest.CaptureFixture) -> None:
    quickstart_sample.quickstart_sample(
        gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_input_uri
    )
    out, _ = capsys.readouterr()

    assert "Document structure in Cloud Storage" in out
    assert "Number of Pages: 1" in out
    assert "Number of Entities: 35" in out
