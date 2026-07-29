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

from __future__ import annotations

import itertools
from typing import Sequence

import pytest

from bigframes.core import sequences

LARGE_LIST = list(range(100, 500))
SMALL_LIST = list(range(1, 5))
CHAINED_LIST = sequences.ChainedSequence([SMALL_LIST for i in range(100)])


def _build_reference(*parts):
    return tuple(itertools.chain(*parts))


def _check_equivalence(expected: Sequence, actual: Sequence):
    assert len(expected) == len(actual)
    assert tuple(expected) == tuple(actual)
    assert expected[10:1:-2] == actual[10:1:-2]
    if len(expected) > 0:
        assert expected[len(expected) - 1] == expected[len(actual) - 1]


@pytest.mark.parametrize(
    ("parts",),
    [
        ([],),
        ([[]],),
        ([[0, 1, 2]],),
        ([LARGE_LIST, SMALL_LIST, LARGE_LIST],),
        ([SMALL_LIST * 100],),
        ([CHAINED_LIST, LARGE_LIST, CHAINED_LIST, SMALL_LIST],),
    ],
)
def test_init_chained_sequence_single_slist(parts):
    value = sequences.ChainedSequence(*parts)
    expected = _build_reference(*parts)
    _check_equivalence(expected, value)
