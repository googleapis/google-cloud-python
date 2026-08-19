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

"""Check that bpd and Session can be used interchangablely."""

from __future__ import annotations

from typing import cast

import numpy as np
import pandas.testing

import bigframes.pandas as bpd
import bigframes.session


def test_cut(session: bigframes.session.Session):
    sc = [30, 80, 40, 90, 60, 45, 95, 75, 55, 100, 65, 85]
    x = [20, 40, 60, 80, 100]

    bpd_result = bpd.cut(sc, x)
    session_result = session.cut(sc, x)

    global_session = bpd.get_global_session()
    assert global_session is not session
    assert bpd_result._session is global_session
    assert session_result._session is session

    bpd_pd = bpd_result.to_pandas()
    session_pd = session_result.to_pandas()
    pandas.testing.assert_series_equal(bpd_pd, session_pd)


def test_dataframe(session: bigframes.session.Session):
    data = {"col": ["local", None, "data"]}

    bpd_result = bpd.DataFrame(data)
    session_result = session.DataFrame(data)

    global_session = bpd.get_global_session()
    assert global_session is not session
    assert bpd_result._session is global_session
    assert session_result._session is session

    bpd_pd = bpd_result.to_pandas()
    session_pd = session_result.to_pandas()
    pandas.testing.assert_frame_equal(bpd_pd, session_pd)


def test_multiindex_from_arrays(session: bigframes.session.Session):
    arrays = [[1, 1, 2, 2], ["red", "blue", "red", "blue"]]

    bpd_result = bpd.MultiIndex.from_arrays(arrays, names=("number", "color"))
    session_result = session.MultiIndex.from_arrays(arrays, names=("number", "color"))

    global_session = bpd.get_global_session()
    assert global_session is not session
    assert bpd_result._session is global_session
    assert session_result._session is session

    bpd_pd = bpd_result.to_pandas()
    session_pd = session_result.to_pandas()
    pandas.testing.assert_index_equal(bpd_pd, session_pd)


def test_multiindex_from_tuples(session: bigframes.session.Session):
    tuples = [(1, "red"), (1, "blue"), (2, "red"), (2, "blue")]

    bpd_result = bpd.MultiIndex.from_tuples(tuples, names=("number", "color"))
    session_result = session.MultiIndex.from_tuples(tuples, names=("number", "color"))

    global_session = bpd.get_global_session()
    assert global_session is not session
    assert bpd_result._session is global_session
    assert session_result._session is session

    bpd_pd = bpd_result.to_pandas()
    session_pd = session_result.to_pandas()
    pandas.testing.assert_index_equal(bpd_pd, session_pd)


def test_index(session: bigframes.session.Session):
    index = [1, 2, 3]

    bpd_result = bpd.Index(index)
    session_result = session.Index(index)

    global_session = bpd.get_global_session()
    assert global_session is not session
    assert bpd_result._session is global_session
    assert session_result._session is session

    bpd_pd = bpd_result.to_pandas()
    session_pd = session_result.to_pandas()
    pandas.testing.assert_index_equal(bpd_pd, session_pd)


def test_series(session: bigframes.session.Session):
    series = [1, 2, 3]

    bpd_result = bpd.Series(series)
    session_result = session.Series(series)

    global_session = bpd.get_global_session()
    assert global_session is not session
    assert bpd_result._session is global_session
    assert session_result._session is session

    bpd_pd = bpd_result.to_pandas()
    session_pd = session_result.to_pandas()
    pandas.testing.assert_series_equal(bpd_pd, session_pd)


def test_to_datetime(session: bigframes.session.Session):
    datetimes = ["2018-10-26 12:00:00", "2018-10-26 13:00:15"]

    bpd_result = bpd.to_datetime(datetimes)
    session_result = cast(bpd.Series, session.to_datetime(datetimes))

    global_session = bpd.get_global_session()
    assert global_session is not session
    assert bpd_result._session is global_session
    assert session_result._session is session

    bpd_pd = bpd_result.to_pandas()
    session_pd = session_result.to_pandas()
    pandas.testing.assert_series_equal(bpd_pd, session_pd)


def test_to_timedelta(session: bigframes.session.Session):
    offsets = np.arange(5)

    bpd_result = bpd.to_timedelta(offsets, unit="s")
    session_result = session.to_timedelta(offsets, unit="s")

    global_session = bpd.get_global_session()
    assert global_session is not session
    assert bpd_result._session is global_session
    assert session_result._session is session

    bpd_pd = bpd_result.to_pandas()
    session_pd = session_result.to_pandas()
    pandas.testing.assert_series_equal(bpd_pd, session_pd)
