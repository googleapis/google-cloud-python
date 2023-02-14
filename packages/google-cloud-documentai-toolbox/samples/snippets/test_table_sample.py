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
from samples.snippets import table_sample

document_path = "resources/form_with_tables.json"
output_file_prefix = "resources/form_with_tables"


def test_table_sample(capsys: pytest.CaptureFixture) -> None:
    table_sample.table_sample(
        document_path=document_path, output_file_prefix=output_file_prefix
    )
    out, _ = capsys.readouterr()

    assert "Tables in Document" in out
    assert "Item 1" in out

    output_filename = f"{output_file_prefix}-0-0.csv"
    assert os.path.exists(output_filename)
    os.remove(output_filename)
