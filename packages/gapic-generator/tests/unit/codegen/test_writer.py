# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from gapic.codegen.writer import CodeWriter


def test_code_writer_basic_and_indentation():
    writer = CodeWriter()
    assert writer.indent_level == 0

    writer.write_license_header(2026)
    writer.write_line("")
    writer.write_line("x = 1")

    with writer.indent():
        assert writer.indent_level == 1
        writer.write_line("y = 2")
        with writer.indent(2):
            assert writer.indent_level == 3
            writer.write_line("z = 3")

    assert writer.indent_level == 0

    out = writer.dump()
    assert "# Copyright 2026 Google LLC" in out
    assert "\nx = 1\n    y = 2\n            z = 3\n" in out


def test_code_writer_block():
    writer = CodeWriter()
    with writer.block("class Foo"):
        writer.write_line('"""Foo docstring."""')
        with writer.block("def bar(self)", suffix=" -> None:"):
            writer.write_line("pass")

    out = writer.dump()
    expected = (
        "class Foo:\n"
        '    """Foo docstring."""\n'
        "    def bar(self) -> None:\n"
        "        pass\n"
    )
    assert out == expected





def test_code_writer_docstring():
    writer = CodeWriter()
    with writer.block("class Foo"):
        writer.write_docstring("Single-line docstring.")
        with writer.block("def bar(self)"):
            writer.write_docstring("""
                Multi-line docstring summary.

                Detailed description of method.
            """)

    out = writer.dump()
    expected = (
        "class Foo:\n"
        '    """Single-line docstring."""\n'
        "    def bar(self):\n"
        '        """Multi-line docstring summary.\n'
        "\n"
        "        Detailed description of method.\n"
        '        """\n'
    )
    assert out == expected


def test_code_writer_imports():
    writer = CodeWriter()
    writer.write_imports(
        std=[
            ("collections", ["OrderedDict"]),
            "json",
            "import os",
            ("typing", ["List", "Dict", "Callable"]),
        ],
        third_party=[
            "from google.api_core import gapic_v1",
        ],
        local=[
            "from .transports.base import FooTransport",
        ],
    )

    out = writer.dump()
    expected = (
        "import json\n"
        "import os\n"
        "from collections import OrderedDict\n"
        "from typing import Callable, Dict, List\n"
        "\n"
        "from google.api_core import gapic_v1\n"
        "\n"
        "from .transports.base import FooTransport\n"
    )
    assert out == expected
