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

import pathlib
import runpy
import sys
import types
from unittest import mock


def test_docs_conf_executes_successfully():
    docs_dir = pathlib.Path(__file__).parent.parent.parent / "docs"
    conf_path = docs_dir / "conf.py"

    if not conf_path.exists():
        import pytest

        pytest.skip("docs/conf.py not found")

    res = runpy.run_path(str(conf_path))

    assert "project" in res
    assert res["project"] == "google-cloud-bigquery"


def test_docs_conf_patches_markdown_translator():
    docs_dir = pathlib.Path(__file__).parent.parent.parent / "docs"
    conf_path = docs_dir / "conf.py"

    if not conf_path.exists():
        import pytest

        pytest.skip("docs/conf.py not found")

    mock_orig_depart = mock.MagicMock(return_value="original_output")

    class FakeTranslator:
        depart_paragraph = mock_orig_depart
        depart_compact_paragraph = mock_orig_depart

    fake_module = types.ModuleType("sphinx_markdown_builder.markdown_writer")
    fake_module.MarkdownTranslator = FakeTranslator

    with mock.patch.dict(
        sys.modules,
        {
            "sphinx_markdown_builder": types.ModuleType("sphinx_markdown_builder"),
            "sphinx_markdown_builder.markdown_writer": fake_module,
        },
    ):
        runpy.run_path(str(conf_path))

    assert FakeTranslator.depart_paragraph is not mock_orig_depart
    assert FakeTranslator.depart_compact_paragraph is not mock_orig_depart

    translator_in_table = FakeTranslator()
    translator_in_table.table_entries = ["entry"]
    assert (
        FakeTranslator.depart_paragraph(translator_in_table, mock.MagicMock()) is None
    )
    assert (
        FakeTranslator.depart_compact_paragraph(translator_in_table, mock.MagicMock())
        is None
    )
    mock_orig_depart.assert_not_called()

    translator_outside_table = FakeTranslator()
    mock_node = mock.MagicMock()
    assert (
        FakeTranslator.depart_paragraph(translator_outside_table, mock_node)
        == "original_output"
    )
    mock_orig_depart.assert_called_once_with(translator_outside_table, mock_node)

    mock_orig_depart.reset_mock()
    assert (
        FakeTranslator.depart_compact_paragraph(translator_outside_table, mock_node)
        == "original_output"
    )
    mock_orig_depart.assert_called_once_with(translator_outside_table, mock_node)
