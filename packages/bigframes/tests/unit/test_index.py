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

from bigframes.testing import mocks


def test_index_rename(monkeypatch: pytest.MonkeyPatch):
    dataframe = mocks.create_dataframe(
        monkeypatch, data={"idx": [], "col": []}
    ).set_index("idx")
    index = dataframe.index
    assert index.name == "idx"
    renamed = index.rename("my_index_name")
    assert renamed.name == "my_index_name"


def test_index_rename_inplace_returns_none(monkeypatch: pytest.MonkeyPatch):
    dataframe = mocks.create_dataframe(
        monkeypatch, data={"idx": [], "col": []}
    ).set_index("idx")
    index = dataframe.index
    assert index.name == "idx"
    assert index.rename("my_index_name", inplace=True) is None

    # Make sure the linked DataFrame is updated, too.
    assert dataframe.index.name == "my_index_name"
    assert index.name == "my_index_name"
