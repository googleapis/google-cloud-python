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
from samples.snippets import export_images_sample

document_path = "../../tests/unit/resources/images/dl3-0.json"
output_path = "resources/output/"
output_file_prefix = "exported_photo"
output_file_extension = "png"


def test_export_images_sample(capsys: pytest.CaptureFixture) -> None:
    os.makedirs(output_path)
    current_directory = os.path.dirname(__file__)
    rel_document_path = os.path.relpath(document_path, current_directory)

    export_images_sample.export_images_sample(
        document_path=rel_document_path,
        output_path=output_path,
        output_file_prefix=output_file_prefix,
        output_file_extension=output_file_extension,
    )

    out, _ = capsys.readouterr()

    assert "Images Successfully Exported" in out
    assert "exported_photo_0_Portrait.png" in out

    assert os.path.exists(output_path)
    shutil.rmtree(output_path)
