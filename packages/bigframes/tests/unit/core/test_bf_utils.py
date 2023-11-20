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

from bigframes.core import utils


def test_get_standardized_ids_columns():
    col_labels = ["string", 0, None, "duplicate", "duplicate", "with space"]

    col_ids, idx_ids = utils.get_standardized_ids(col_labels)

    assert col_ids == [
        "string",
        "0",
        utils.UNNAMED_COLUMN_ID,
        "duplicate",
        "duplicate_1",
        "with_space",
    ]
    assert idx_ids == []


def test_get_standardized_ids_indexes():
    col_labels = ["duplicate"]
    idx_labels = ["string", 0, None, "duplicate", "duplicate", "with space"]

    col_ids, idx_ids = utils.get_standardized_ids(col_labels, idx_labels)

    assert col_ids == ["duplicate_2"]
    assert idx_ids == [
        "string",
        "0",
        utils.UNNAMED_INDEX_ID,
        "duplicate",
        "duplicate_1",
        "with_space",
    ]


def test_get_standardized_ids_tuple():
    col_labels = [("foo", 1), ("foo", 2), ("bar", 1)]

    col_ids, _ = utils.get_standardized_ids(col_labels)

    assert col_ids == ["('foo',_1)", "('foo',_2)", "('bar',_1)"]
