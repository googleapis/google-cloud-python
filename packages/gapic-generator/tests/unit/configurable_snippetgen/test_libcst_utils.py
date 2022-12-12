# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

import libcst
import pytest

from gapic.configurable_snippetgen import libcst_utils


def _assert_code_equal(node: libcst.CSTNode, code: str) -> str:
    assert libcst.Module(body=[node]).code == code


@pytest.mark.parametrize(
    "is_sync,expected_code",
    [
        (True, 'def some_function():\n    ""\n'),
        (False, 'async def some_function():\n    ""\n'),
    ],
)
def test_base_function_def(is_sync, expected_code):
    node = libcst_utils.base_function_def("some_function", is_sync)

    expected_node = libcst.parse_statement(expected_code)

    # Whenever possible we try to control the shape of the nodes,
    # because we will be manipulating them during snippet generation.
    assert node.deep_equals(expected_node), (node, expected_node)

    # Sometimes it is more convenient to just verify the code.
    _assert_code_equal(node, expected_code)
