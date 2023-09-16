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

import pytest

IPython = pytest.importorskip("IPython")


def test_repr_cache(scalars_df_index):
    display_formatter = IPython.core.formatters.DisplayFormatter()
    # Make sure the df has a new block that the method return value
    # is not already cached.
    test_df = scalars_df_index.head()
    test_df._block.retrieve_repr_request_results.cache_clear()
    results = display_formatter.format(test_df)
    assert results[0].keys() == {"text/plain", "text/html"}
    assert test_df._block.retrieve_repr_request_results.cache_info().misses >= 1
    assert test_df._block.retrieve_repr_request_results.cache_info().hits >= 1
