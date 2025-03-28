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

import inspect
import re
import sys
import unittest.mock as mock

import pandas as pd
import pytest

import bigframes.core.global_session
import bigframes.dataframe
import bigframes.pandas as bpd
import bigframes.session

leading_whitespace = re.compile(r"^\s+", flags=re.MULTILINE)


def all_session_methods():
    session_attributes = set(
        attribute
        for attribute in dir(bigframes.session.Session)
        if not attribute.startswith("_")
    )
    session_attributes.remove("close")
    # streaming isn't in pandas
    session_attributes.remove("read_gbq_table_streaming")

    for attribute in sorted(session_attributes):
        session_method = getattr(bigframes.session.Session, attribute)
        if not callable(session_method):
            continue  # pragma: no cover
        yield attribute


@pytest.mark.parametrize(
    [
        "method_name",
    ],
    [(method_name,) for method_name in all_session_methods()],
)
def test_method_matches_session(method_name: str):
    if sys.version_info < (3, 10):
        pytest.skip(
            "Need Python 3.10 to reconcile deferred annotations."
        )  # pragma: no cover

    session_method = getattr(bigframes.session.Session, method_name)
    session_doc = inspect.getdoc(session_method)
    assert session_doc is not None, "docstrings are required"

    pandas_method = getattr(bigframes.pandas, method_name)
    pandas_doc = inspect.getdoc(pandas_method)
    assert pandas_doc is not None, "docstrings are required"
    assert re.sub(leading_whitespace, "", pandas_doc) == re.sub(
        leading_whitespace, "", session_doc
    )

    # Add `eval_str = True` so that deferred annotations are turned into their
    # corresponding type objects. Need Python 3.10 for eval_str parameter.
    session_signature = inspect.signature(
        session_method,
        eval_str=True,
        globals={**vars(bigframes.session), **{"dataframe": bigframes.dataframe}},
    )
    pandas_signature = inspect.signature(pandas_method, eval_str=True)
    assert [
        # Kind includes position, which will be an offset.
        parameter.replace(kind=inspect.Parameter.POSITIONAL_ONLY)
        for parameter in pandas_signature.parameters.values()
    ] == [
        # Kind includes position, which will be an offset.
        parameter.replace(kind=inspect.Parameter.POSITIONAL_ONLY)
        for parameter in session_signature.parameters.values()
        # Don't include the first parameter, which is `self: Session`
    ][
        1:
    ]
    assert pandas_signature.return_annotation == session_signature.return_annotation


@pytest.mark.parametrize(
    ("bins", "labels", "error_message"),
    [
        pytest.param(
            5,
            True,
            "Bin labels must either be False, None or passed in as a list-like argument",
            id="true",
        ),
        pytest.param(
            5,
            1.5,
            "Bin labels must either be False, None or passed in as a list-like argument",
            id="invalid_types",
        ),
        pytest.param(
            2,
            ["A"],
            "must be same as the value of bins",
            id="int_bins_mismatch",
        ),
        pytest.param(
            [1, 2, 3],
            ["A"],
            "must be same as the number of bin edges",
            id="iterator_bins_mismatch",
        ),
    ],
)
def test_cut_raises_with_invalid_labels(bins: int, labels, error_message: str):
    mock_series = mock.create_autospec(bigframes.pandas.Series, instance=True)
    with pytest.raises(ValueError, match=error_message):
        bigframes.pandas.cut(mock_series, bins, labels=labels)


def test_cut_raises_with_unsupported_labels():
    mock_series = mock.create_autospec(bigframes.pandas.Series, instance=True)
    labels = [1, 2]
    with pytest.raises(
        NotImplementedError, match=r".*only iterables of strings are supported.*"
    ):
        bigframes.pandas.cut(mock_series, 2, labels=labels)  # type: ignore


@pytest.mark.parametrize(
    ("bins", "error_message"),
    [
        pytest.param(1.5, "`bins` must be an integer or interable.", id="float"),
        pytest.param(0, "`bins` should be a positive integer.", id="zero_int"),
        pytest.param(-1, "`bins` should be a positive integer.", id="neg_int"),
        pytest.param(
            ["notabreak"],
            "`bins` iterable should contain tuples or numerics",
            id="iterable_w_wrong_type",
        ),
        pytest.param(
            [10, 3],
            "left side of interval must be <= right side",
            id="decreased_breaks",
        ),
        pytest.param(
            [(1, 10), (2, 25)],
            "Overlapping IntervalIndex is not accepted.",
            id="overlapping_intervals",
        ),
    ],
)
def test_cut_raises_with_invalid_bins(bins: int, error_message: str):
    mock_series = mock.create_autospec(bigframes.pandas.Series, instance=True)
    with pytest.raises(ValueError, match=error_message):
        bigframes.pandas.cut(mock_series, bins, labels=False)


def test_pandas_attribute():
    assert bpd.NA is pd.NA
    assert bpd.BooleanDtype is pd.BooleanDtype
    assert bpd.Float64Dtype is pd.Float64Dtype
    assert bpd.Int64Dtype is pd.Int64Dtype
    assert bpd.StringDtype is pd.StringDtype
    assert bpd.ArrowDtype is pd.ArrowDtype
