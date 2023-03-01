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


import pytest
from samples.snippets import create_batches_sample

gcs_bucket_name = "cloud-samples-data"
gcs_input_uri = "documentai_toolbox/document_batches/"
batch_size = 50


def test_create_batches_sample(capsys: pytest.CaptureFixture) -> None:
    create_batches_sample.create_batches_sample(
        gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_input_uri, batch_size=batch_size
    )
    out, _ = capsys.readouterr()

    assert "2 batch(es) created." in out
    assert "50 files in batch." in out
    assert "47 files in batch." in out
