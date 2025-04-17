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

from unittest import mock

import pytest

from bigframes.testing import mocks


@pytest.fixture
def mock_series(monkeypatch: pytest.MonkeyPatch):
    dataframe = mocks.create_dataframe(monkeypatch)
    series = dataframe["col"]
    monkeypatch.setattr(series, "to_pandas", mock.Mock())
    return series


@pytest.mark.parametrize(
    "api_name, kwargs",
    [
        ("to_csv", {"allow_large_results": True}),
        ("to_dict", {"allow_large_results": True}),
        ("to_excel", {"excel_writer": "abc", "allow_large_results": True}),
        ("to_json", {"allow_large_results": True}),
        ("to_latex", {"allow_large_results": True}),
        ("to_list", {"allow_large_results": True}),
        ("to_markdown", {"allow_large_results": True}),
        ("to_numpy", {"allow_large_results": True}),
        ("to_pickle", {"path": "abc", "allow_large_results": True}),
        ("to_string", {"allow_large_results": True}),
        ("to_xarray", {"allow_large_results": True}),
    ],
)
def test_series_allow_large_results_param_passing(mock_series, api_name, kwargs):
    getattr(mock_series, api_name)(**kwargs)
    mock_series.to_pandas.assert_called_once_with(
        allow_large_results=kwargs["allow_large_results"]
    )
