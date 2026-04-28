# Copyright 2025 Google LLC
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

import pytest

import bigframes.pandas as bpd
import bigframes.bigquery as bbq

pytest.skip("Skipping blob tests due to b/481790217", allow_module_level=True)


def test_blob_read_url(images_mm_df: bpd.DataFrame):
    access_json = bbq.obj.get_access_url(images_mm_df["blob_col"], mode="r")
    urls = bbq.json_value(access_json, "$.access_urls.read_url")

    assert urls.str.startswith("https://storage.googleapis.com/").all()


def test_blob_write_url(images_mm_df: bpd.DataFrame):
    access_json = bbq.obj.get_access_url(images_mm_df["blob_col"], mode="rw")
    urls = bbq.json_value(access_json, "$.access_urls.write_url")

    assert urls.str.startswith("https://storage.googleapis.com/").all()
