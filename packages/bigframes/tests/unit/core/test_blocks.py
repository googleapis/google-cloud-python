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

import pandas
import pandas.testing
import pytest

import bigframes.core.blocks as blocks


@pytest.mark.parametrize(
    ("data",),
    (
        pytest.param(
            {"test 1": [1, 2, 3], "test 2": [0.25, 0.5, 0.75]},
            id="dict_spaces_in_column_names",
        ),
        pytest.param(
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
            id="nested_list",
        ),
        pytest.param(
            pandas.concat(
                [
                    pandas.Series([1, 2, 3], name="some col"),
                    pandas.Series([2, 3, 4], name="some col"),
                ],
                axis="columns",
            ),
            id="duplicate_column_names",
        ),
        pytest.param(
            pandas.DataFrame(
                {"test": [1, 2, 3]},
                index=pandas.Index(["a", "b", "c"], name="string index"),
            ),
            id="string_index",
        ),
        pytest.param(
            pandas.DataFrame(
                [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]],
                columns=pandas.MultiIndex.from_tuples(
                    [(1, 1), (1, 2), (0, 0), (0, 1)],
                    names=["some level", "another level"],
                ),
            ),
            marks=[
                pytest.mark.skipif(
                    tuple(pandas.__version__.split()) < ("2", "0", "0"),
                    reason="pandas 1.5.3 treats column MultiIndex as Index of tuples",
                ),
            ],
            id="multiindex_columns",
        ),
        pytest.param(
            pandas.DataFrame(
                {"test": [1, 2, 3]},
                index=pandas.MultiIndex.from_tuples([(1, 1), (1, 2), (0, 0)]),
            ),
            id="multiindex_rows",
        ),
    ),
)
def test_block_from_local(data):
    expected = pandas.DataFrame(data)

    block = blocks.block_from_local(data)

    pandas.testing.assert_index_equal(block.column_labels, expected.columns)
    assert tuple(block.index_labels) == tuple(expected.index.names)
    assert block.shape == expected.shape
