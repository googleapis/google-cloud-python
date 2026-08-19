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

import bigframes.core.indexes


def test_index_repr_with_uninitialized_object():
    """Ensures Index.__init__ can be paused in a visual debugger without crashing.

    Regression test for https://github.com/googleapis/python-bigquery-dataframes/issues/728
    """
    # Avoid calling __init__ to simulate pausing __init__ in a debugger.
    # https://stackoverflow.com/a/6384982/101923
    index = object.__new__(bigframes.core.indexes.Index)
    got = repr(index)
    assert "Index" in got


def test_multiindex_repr_with_uninitialized_object():
    """Ensures MultiIndex.__init__ can be paused in a visual debugger without crashing.

    Regression test for https://github.com/googleapis/python-bigquery-dataframes/issues/728
    """
    # Avoid calling __init__ to simulate pausing __init__ in a debugger.
    # https://stackoverflow.com/a/6384982/101923
    index = object.__new__(bigframes.core.indexes.MultiIndex)
    got = repr(index)
    assert "MultiIndex" in got
