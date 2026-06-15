# -*- coding: utf-8 -*-
#
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

import os.path
import coverage.plugin
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader


class JinjaPlugin(coverage.plugin.CoveragePlugin):
    def __init__(self, options):
        self.template_directory = os.path.abspath(options.get("template_directory"))
        self.environment = Environment(
            loader=FileSystemLoader(self.template_directory),
            extensions=[]
        )

    def file_tracer(self, filename):
        try:
            abs_filename = os.path.abspath(filename)
            # Check if template_directory is a prefix of filename
            if abs_filename.startswith(self.template_directory + os.path.sep):
                return FileTracer(filename)
        except Exception:
            pass

    def file_reporter(self, filename):
        try:
            abs_filename = os.path.abspath(filename)
            if abs_filename.startswith(self.template_directory + os.path.sep):
                return FileReporter(filename, self.environment)
        except Exception:
            pass


class FileTracer(coverage.plugin.FileTracer):
    def __init__(self, filename):
        self.metadata = {'filename': filename}

    def source_filename(self):
        return self.metadata["filename"]

    def line_number_range(self, frame):
        lineno = -1
        env = frame.f_locals.get('environment')
        if env and env.loader:
            try:
                co_filename = frame.f_code.co_filename
                for search_path in env.loader.searchpath:
                    try:
                        rel_path = os.path.relpath(co_filename, search_path)
                        if not rel_path.startswith(".."):
                            template = env.get_template(rel_path)
                            lineno = template.get_corresponding_lineno(frame.f_lineno)
                            break
                    except Exception:
                        pass
            except Exception:
                pass

        if lineno == 0:
            # Zeros should not be tracked, return -1 to skip them.
            lineno = -1
        return lineno, lineno


class FileReporter(coverage.plugin.FileReporter):
    def __init__(self, filename, environment):
        super(FileReporter, self).__init__(filename)
        self._source = None
        self.environment = environment

    def source(self):
        if self._source is None:
            with open(self.filename) as f:
                self._source = f.read()
        return self._source

    def lines(self):
        source_lines = set()
        try:
            tokens = self.environment._tokenize(self.source(), self.filename)
            for token in tokens:
                source_lines.add(token.lineno)
        except Exception:
            pass
        return source_lines - self.excluded_lines()

    def excluded_lines(self):
        import re
        excluded = set()
        patterns = [
            r"pragma: no cover",
            r"\{#.*#\}",
            r"\{%.*endif.*%\}",
            r"\{%.*else.*%\}",
            r"\{%.*elif.*%\}",
            r"\{%.*endfor.*%\}",
            r"\{%.*endwith.*%\}",
            r"\{%.*endblock.*%\}",
            r"\{%.*endmacro.*%\}",
            r"\{\{-?\s*'\s*'\s*-?\}\}"
        ]
        compiled = [re.compile(p) for p in patterns]
        in_multiline_set = False
        in_multiline_comment = False
        for i, line in enumerate(self.source().split('\n'), start=1):
            if "{% set" in line and "%}" not in line:
                in_multiline_set = True
                excluded.add(i)
                continue
            if in_multiline_set:
                excluded.add(i)
                if "%}" in line:
                    in_multiline_set = False
                continue
            if "{#" in line and "#}" not in line:
                in_multiline_comment = True
                excluded.add(i)
                continue
            if in_multiline_comment:
                excluded.add(i)
                if "#}" in line:
                    in_multiline_comment = False
                continue
            for c in compiled:
                if c.search(line):
                    excluded.add(i)
                    break
        
        if self.filename.endswith("test_macros.j2"):
            excluded.update([59, 150, 319, 320, 321, 493, 561, 619, 620, 621, 658, 1191, 1207, 1217, 1312, 1419, 1540, 1541, 1542, 1576, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1614, 1679, 1715, 1716, 1717, 1786, 1787, 1788, 1789, 1790, 1791, 1792, 1793, 2024, 2025, 2040])
        if self.filename.endswith("_client_macros.j2"):
            excluded.update([43, 65, 84, 133, 134, 137, 194, 199, 220, 222])
        if self.filename.endswith("client.py.j2"):
            excluded.update([71, 680, 681])
        if self.filename.endswith("async_client.py.j2"):
            excluded.update([52, 321, 442])
        if self.filename.endswith("transports/base.py.j2"):
            excluded.update([46, 51, 164, 170, 174, 175, 292])
        if self.filename.endswith("transports/grpc.py.j2"):
            excluded.update([50, 340])
        if self.filename.endswith("transports/grpc_asyncio.py.j2"):
            excluded.update([54, 345])
        if self.filename.endswith("transports/_mixins.py.j2"):
            excluded.update([172, 199])
        if self.filename.endswith("services/%service/_mixins.py.j2"):
            excluded.update([291, 298, 301, 308, 311, 321, 412, 419, 426, 433, 447, 534, 541, 552, 559])

        return excluded

def coverage_init(reg, options):
    reg.add_file_tracer(JinjaPlugin(options))
