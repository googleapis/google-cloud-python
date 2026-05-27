# Copyright 2026 Google LLC
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

import unittest.mock as mock

import pandas as pd

import bigframes.core.col as col
import bigframes.core.expression as ex
import bigframes.core.global_session
import bigframes.core.googlesql as core_googlesql
import bigframes.series as series
from bigframes.operations import googlesql
from bigframes.testing import mocks

# Define a test op
_TEST_OP = googlesql.GoogleSqlScalarOp(
    "TEST_OP",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: None,
)


def test_apply_googlesql_scalar_op_expressions():
    # Only expressions
    result = core_googlesql.apply_googlesql_scalar_op(
        _TEST_OP,
        col.col("a"),
        col.col("b"),
    )
    assert isinstance(result, col.Expression)


def test_apply_googlesql_scalar_op_pandas_series_global_session(monkeypatch):
    # Setup mock session
    session = mocks.create_bigquery_session()
    monkeypatch.setattr(bigframes.core.global_session, "_global_session", session)
    bigframes.options.bigquery._session_started = True

    # Create a real-ish Series to return from read_pandas
    df = mocks.create_dataframe(monkeypatch, session=session, data={"col": [1, 2, 3]})
    bf_series = df["col"]

    # Mock read_pandas on the session
    mock_read_pandas = mock.MagicMock(return_value=bf_series)
    session.read_pandas = mock_read_pandas  # type: ignore

    # Mock _apply_nary_op on Series class to avoid real compilation/execution
    mock_apply_nary_op = mock.MagicMock(return_value=bf_series)
    monkeypatch.setattr(series.Series, "_apply_nary_op", mock_apply_nary_op)

    pd_series = pd.Series([1, 2, 3])

    # Call the function with a pandas Series and a literal
    result = core_googlesql.apply_googlesql_scalar_op(_TEST_OP, pd_series, 42)

    # Verify read_pandas was called on the global session
    mock_read_pandas.assert_called_once_with(pd_series)

    # Verify _apply_nary_op was called on the converted series
    mock_apply_nary_op.assert_called_once()
    # First arg to _apply_nary_op is the op, second is the processed_args
    assert mock_apply_nary_op.call_args[0][0] == _TEST_OP
    # processed_args should contain the converted bf_series and the literal 42
    processed_args = mock_apply_nary_op.call_args[0][1]
    assert processed_args[0] is bf_series
    assert processed_args[1] == 42

    # Verify result is a Series
    assert isinstance(result, series.Series)


def test_apply_googlesql_scalar_op_pandas_series_with_bf_series(monkeypatch):
    # Setup mock session 1 (global) and session 2 (associated with bf_series)
    global_session = mocks.create_bigquery_session(session_id="global")
    monkeypatch.setattr(
        bigframes.core.global_session, "_global_session", global_session
    )
    bigframes.options.bigquery._session_started = True

    bf_session = mocks.create_bigquery_session(session_id="bf_session")

    # Create a bf_series associated with bf_session
    df = mocks.create_dataframe(
        monkeypatch, session=bf_session, data={"col": [1, 2, 3]}
    )
    bf_series = df["col"]

    assert bf_series._session == bf_session

    # Mock read_pandas on both sessions
    mock_global_read_pandas = mock.MagicMock()
    global_session.read_pandas = mock_global_read_pandas  # type: ignore

    mock_bf_read_pandas = mock.MagicMock(return_value=bf_series)
    bf_session.read_pandas = mock_bf_read_pandas  # type: ignore

    # Mock _apply_nary_op
    mock_apply_nary_op = mock.MagicMock(return_value=bf_series)
    monkeypatch.setattr(series.Series, "_apply_nary_op", mock_apply_nary_op)

    pd_series = pd.Series([1, 2, 3])

    # Call with both pandas Series and BigFrames Series
    result = core_googlesql.apply_googlesql_scalar_op(_TEST_OP, pd_series, bf_series)

    # Verify read_pandas was called on bf_session, NOT global_session
    mock_bf_read_pandas.assert_called_once_with(pd_series)
    mock_global_read_pandas.assert_not_called()

    # Verify _apply_nary_op was called
    mock_apply_nary_op.assert_called_once()
    processed_args = mock_apply_nary_op.call_args[0][1]
    # Both arguments to the op should now be BigFrames Series
    assert processed_args[0] is bf_series
    assert processed_args[1] is bf_series

    assert isinstance(result, series.Series)


def test_apply_googlesql_scalar_op_mixed_args(monkeypatch):
    session = mocks.create_bigquery_session()
    monkeypatch.setattr(bigframes.core.global_session, "_global_session", session)
    bigframes.options.bigquery._session_started = True

    df = mocks.create_dataframe(monkeypatch, session=session, data={"col": [1, 2, 3]})
    bf_series = df["col"]

    mock_read_pandas = mock.MagicMock(return_value=bf_series)
    session.read_pandas = mock_read_pandas  # type: ignore

    mock_apply_nary_op = mock.MagicMock(return_value=bf_series)
    monkeypatch.setattr(series.Series, "_apply_nary_op", mock_apply_nary_op)

    pd_series = pd.Series([1, 2, 3])
    expr = col.Expression(ex.const(10))

    # Call with pandas Series, Expression, and Literal
    result = core_googlesql.apply_googlesql_scalar_op(_TEST_OP, pd_series, expr, 42)

    # Verify pandas Series was converted
    mock_read_pandas.assert_called_once_with(pd_series)

    # Verify _apply_nary_op was called
    mock_apply_nary_op.assert_called_once()
    processed_args = mock_apply_nary_op.call_args[0][1]

    # Processed args should be:
    # 1. bf_series (converted from pd_series)
    # 2. A new Series (projected from the expression onto bf_series' block)
    # 3. Literal 42
    assert isinstance(processed_args[0], series.Series)
    assert processed_args[0] is bf_series

    assert isinstance(processed_args[1], series.Series)
    assert processed_args[1] is not bf_series

    assert processed_args[2] == 42

    assert isinstance(result, series.Series)


def test_apply_googlesql_scalar_op_pandas_series_with_bf_dataframe(monkeypatch):
    # Setup mock session 2 (associated with bf_dataframe)
    bf_session = mocks.create_bigquery_session(session_id="bf_session")

    # Create a bf_dataframe associated with bf_session
    bf_dataframe = mocks.create_dataframe(
        monkeypatch, session=bf_session, data={"col": [1, 2, 3]}
    )
    bf_series = bf_dataframe["col"]

    # Setup mock session 1 (global) AFTER creating the dataframe
    global_session = mocks.create_bigquery_session(session_id="global")
    monkeypatch.setattr(
        bigframes.core.global_session, "_global_session", global_session
    )
    bigframes.options.bigquery._session_started = True

    assert bf_dataframe._session == bf_session

    # Mock read_pandas on both sessions
    mock_global_read_pandas = mock.MagicMock()
    global_session.read_pandas = mock_global_read_pandas  # type: ignore

    mock_bf_read_pandas = mock.MagicMock(return_value=bf_series)
    bf_session.read_pandas = mock_bf_read_pandas  # type: ignore

    # Mock _apply_nary_op
    mock_apply_nary_op = mock.MagicMock(return_value=bf_series)
    monkeypatch.setattr(series.Series, "_apply_nary_op", mock_apply_nary_op)

    pd_series = pd.Series([1, 2, 3])

    # Call with pandas Series and BigFrames DataFrame
    result = core_googlesql.apply_googlesql_scalar_op(_TEST_OP, pd_series, bf_dataframe)

    # Verify read_pandas was called on bf_session, NOT global_session
    mock_bf_read_pandas.assert_called_once_with(pd_series)
    mock_global_read_pandas.assert_not_called()

    # Verify _apply_nary_op was called
    mock_apply_nary_op.assert_called_once()
    processed_args = mock_apply_nary_op.call_args[0][1]
    assert processed_args[0] is bf_series
    assert processed_args[1] is bf_dataframe

    assert isinstance(result, series.Series)


def test_apply_googlesql_scalar_op_pandas_series_with_bf_index(monkeypatch):
    # Setup mock session 2 (associated with bf_index)
    bf_session = mocks.create_bigquery_session(session_id="bf_session")

    # Create a bf_dataframe associated with bf_session to get an index
    bf_dataframe = mocks.create_dataframe(
        monkeypatch, session=bf_session, data={"col": [1, 2, 3]}
    )
    bf_index = bf_dataframe.index
    bf_series = bf_dataframe["col"]

    # Setup mock session 1 (global) AFTER creating the dataframe
    global_session = mocks.create_bigquery_session(session_id="global")
    monkeypatch.setattr(
        bigframes.core.global_session, "_global_session", global_session
    )
    bigframes.options.bigquery._session_started = True

    assert bf_index._session == bf_session

    # Mock read_pandas on both sessions
    mock_global_read_pandas = mock.MagicMock()
    global_session.read_pandas = mock_global_read_pandas  # type: ignore

    mock_bf_read_pandas = mock.MagicMock(return_value=bf_series)
    bf_session.read_pandas = mock_bf_read_pandas  # type: ignore

    # Mock _apply_nary_op
    mock_apply_nary_op = mock.MagicMock(return_value=bf_series)
    monkeypatch.setattr(series.Series, "_apply_nary_op", mock_apply_nary_op)

    pd_series = pd.Series([1, 2, 3])

    # Call with pandas Series and BigFrames Index
    result = core_googlesql.apply_googlesql_scalar_op(_TEST_OP, pd_series, bf_index)

    # Verify read_pandas was called on bf_session, NOT global_session
    mock_bf_read_pandas.assert_called_once_with(pd_series)
    mock_global_read_pandas.assert_not_called()

    # Verify _apply_nary_op was called
    mock_apply_nary_op.assert_called_once()
    processed_args = mock_apply_nary_op.call_args[0][1]
    assert processed_args[0] is bf_series
    assert processed_args[1] is bf_index

    assert isinstance(result, series.Series)
