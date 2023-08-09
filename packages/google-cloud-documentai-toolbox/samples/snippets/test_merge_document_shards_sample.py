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
import shutil

import pytest
from samples.snippets import merge_document_shards_sample

gcs_bucket_name = "documentai_toolbox_samples"
gcs_prefix = "output/987654321/1"
output_dir = "resources/output/"
output_path = f"{output_dir}merged_document.json"


def test_merge_document_shards_sample(capsys: pytest.CaptureFixture) -> None:
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

    merge_document_shards_sample.merge_document_shards_sample(
        gcs_bucket_name=gcs_bucket_name,
        gcs_prefix=gcs_prefix,
        output_file_name=output_path,
    )

    out, _ = capsys.readouterr()

    assert "Document with 5 shards successfully merged." in out

    assert os.path.exists(output_dir)
    shutil.rmtree(output_dir)
