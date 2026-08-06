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

import contextlib
from typing import Generator, List, Optional, Tuple, Union


class CodeWriter:
    """Structured Python code writer for pure-Python code generation.

    Replaces Jinja templates by maintaining explicit indentation,
    PEP-8 blank line rules, and docstring formatting in pure Python.
    """

    def __init__(self, indent_str: str = "    ") -> None:
        self.indent_str = indent_str
        self._indent_level = 0
        self._lines: List[str] = []

    @property
    def indent_level(self) -> int:
        return self._indent_level

    def write_license_header(self, year: int = 2026) -> None:
        """Emits standard Apache 2.0 license header matching Jinja _license.j2."""
        self.write_line("# -*- coding: utf-8 -*-")
        self.write_line(f"# Copyright {year} Google LLC")
        self.write_line("#")
        self.write_line('# Licensed under the Apache License, Version 2.0 (the "License");')
        self.write_line("# you may not use this file except in compliance with the License.")
        self.write_line("# You may obtain a copy of the License at")
        self.write_line("#")
        self.write_line("#     http://www.apache.org/licenses/LICENSE-2.0")
        self.write_line("#")
        self.write_line("# Unless required by applicable law or agreed to in writing, software")
        self.write_line('# distributed under the License is distributed on an "AS IS" BASIS,')
        self.write_line("# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.")
        self.write_line("# See the License for the specific language governing permissions and")
        self.write_line("# limitations under the License.")
        self.write_line("#")

    def write_line(self, line: str = "") -> None:
        """Writes a single line of code with current indentation."""
        if not line:
            self._lines.append("")
        else:
            indent = self.indent_str * self._indent_level
            self._lines.append(f"{indent}{line}")

    def newline(self, count: int = 1) -> None:
        """Writes empty lines."""
        for _ in range(count):
            self._lines.append("")

    @contextlib.contextmanager
    def indent(self, levels: int = 1) -> Generator[None, None, None]:
        """Context manager to increase indentation level."""
        self._indent_level += levels
        try:
            yield
        finally:
            self._indent_level -= levels

    @contextlib.contextmanager
    def block(self, header: str, suffix: str = ":") -> Generator[None, None, None]:
        """Writes a block header (e.g. 'class Foo:' or 'if cond:') and indents children."""
        self.write_line(f"{header}{suffix}")
        with self.indent():
            yield

    def dump(self) -> str:
        """Returns the formatted Python source code with a single trailing newline."""
        content = "\n".join(self._lines).rstrip()
        return f"{content}\n"

    def write_docstring(self, doc: str) -> None:
        """Dedents and emits a PEP-257 compliant docstring at the current indentation level."""
        import textwrap
        cleaned = textwrap.dedent(doc).strip("\n")
        lines = cleaned.split("\n")
        if len(lines) == 1:
            self.write_line(f'"""{lines[0]}"""')
        else:
            self.write_line(f'"""{lines[0]}')
            for line in lines[1:]:
                self.write_line(line)
            self.write_line('"""')



    def write_imports(
        self,
        std: Optional[List[Union[str, Tuple[str, List[str]]]]] = None,
        third_party: Optional[List[Union[str, Tuple[str, List[str]]]]] = None,
        local: Optional[List[Union[str, Tuple[str, List[str]]]]] = None,
    ) -> None:
        """Emits PEP-8 compliant grouped import statements."""
        groups = [g for g in (std, third_party, local) if g]
        for i, group in enumerate(groups):
            straight_imports: List[str] = []
            from_imports: List[str] = []
            for item in group:
                if isinstance(item, str):
                    if item.startswith("from "):
                        from_imports.append(item)
                    elif item.startswith("import "):
                        straight_imports.append(item)
                    else:
                        straight_imports.append(f"import {item}")
                else:
                    module, symbols = item
                    sym_str = ", ".join(sorted(symbols))
                    from_imports.append(f"from {module} import {sym_str}")

            for imp in sorted(set(straight_imports)):
                self.write_line(imp)
            for imp in sorted(set(from_imports)):
                self.write_line(imp)

            if i < len(groups) - 1:
                self.newline()
