# Copyright 2024 Google LLC
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

import warnings

import pyarrow as pa
import pytest

import bigframes.exceptions
import bigframes.pandas as bpd


@pytest.fixture(scope="module")
def string_indexed_struct_series(session):
    return bpd.Series(
        [
            {"project": "pandas", "version": 1},
        ],
        dtype=bpd.ArrowDtype(
            pa.struct([("project", pa.string()), ("version", pa.int64())])
        ),
        index=["a"],
        session=session,
    )


@pytest.fixture(scope="module")
def number_series(session):
    return bpd.Series(
        [0],
        dtype=bpd.Int64Dtype,
        session=session,
    )


@pytest.fixture(scope="module")
def string_indexed_number_series(session):
    return bpd.Series(
        [0],
        dtype=bpd.Int64Dtype,
        index=["a"],
        session=session,
    )


@pytest.mark.parametrize(
    "series",
    [
        "string_indexed_struct_series",
        "string_indexed_number_series",
    ],
)
@pytest.mark.parametrize(
    "key",
    [
        0,
        "a",
    ],
)
def test_struct_series_indexers_should_not_warn(request, series, key):
    s = request.getfixturevalue(series)

    with warnings.catch_warnings():
        warnings.simplefilter(
            "error", category=bigframes.exceptions.BadIndexerKeyWarning
        )
        s[key]
