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

import datetime

import numpy as np
import pandas as pd
import pytest

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
        "with space",
    ]
    assert idx_ids == []


def test_get_standardized_ids_indexes():
    col_labels = ["duplicate"]
    idx_labels = ["string", 0, None, "duplicate", "duplicate", "with space"]

    col_ids, idx_ids = utils.get_standardized_ids(col_labels, idx_labels, strict=True)

    assert col_ids == ["duplicate_2"]
    assert idx_ids == [
        "string",
        "_0",
        utils.UNNAMED_INDEX_ID,
        "duplicate",
        "duplicate_1",
        "with_space",
    ]


def test_get_standardized_ids_tuple():
    col_labels = [("foo", 1), ("foo", 2), ("bar", 1)]

    col_ids, _ = utils.get_standardized_ids(col_labels)

    assert col_ids == ["_'foo'_ 1_", "_'foo'_ 2_", "_'bar'_ 1_"]


@pytest.mark.parametrize(
    "input",
    [
        datetime.timedelta(days=2, hours=3, seconds=4, milliseconds=5, microseconds=6),
        pd.Timedelta("2d3h4s5ms6us"),
        np.timedelta64(pd.Timedelta("2d3h4s5ms6us")),
    ],
)
def test_timedelta_to_micros(input):
    assert utils.timedelta_to_micros(input) == 183604005006
