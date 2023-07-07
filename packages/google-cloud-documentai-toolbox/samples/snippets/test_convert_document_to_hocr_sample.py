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

from samples.snippets import convert_document_to_hocr_sample

document_path = "../../tests/unit/resources/0/toolbox_invoice_test-0.json"
document_title = "toolbox_invoice_test-0"


def test_convert_document_to_hocr_sample() -> None:
    actual = convert_document_to_hocr_sample.convert_document_to_hocr_sample(
        document_path=document_path, document_title=document_title
    )

    with open("../../tests/unit/resources/toolbox_invoice_test_0_hocr.xml", "r") as f:
        expected = f.read()

    assert actual == expected
