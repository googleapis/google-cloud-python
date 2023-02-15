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
from samples.snippets import split_pdf_sample

document_path = "../../tests/unit/resources/splitter/procurement_splitter_output.json"
pdf_path = "../../tests/unit/resources/procurement_multi_document.pdf"
output_path = "resources/output/"


def test_split_pdf_sample(capsys: pytest.CaptureFixture) -> None:
    os.makedirs(output_path)
    current_directory = os.path.dirname(__file__)
    rel_document_path = os.path.relpath(document_path, current_directory)
    rel_pdf_path = os.path.relpath(pdf_path, current_directory)

    split_pdf_sample.split_pdf_sample(
        document_path=rel_document_path, pdf_path=rel_pdf_path, output_path=output_path
    )
    out, _ = capsys.readouterr()

    assert "Document Successfully Split" in out
    assert "procurement_multi_document_pg1_invoice_statement.pdf" in out

    assert os.path.exists(output_path)
    shutil.rmtree(output_path)
