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
                return FileTracer(filename, self.environment)
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
    def __init__(self, filename, environment):
        self.metadata = {'filename': filename}
        self.plugin_env = environment

    def source_filename(self):
        return self.metadata["filename"]

    def line_number_range(self, frame):
        lineno = -1
        env = frame.f_locals.get('environment')
        if not env:
            context = frame.f_locals.get('context')
            if context and hasattr(context, 'environment'):
                env = context.environment
        if not env:
            env = frame.f_globals.get('environment')
        if not env:
            env = self.plugin_env

        if env and getattr(env, 'loader', None):
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
            for search_path in self.environment.loader.searchpath:
                try:
                    rel_path = os.path.relpath(self.filename, search_path)
                    if not rel_path.startswith(".."):
                        template = self.environment.get_template(rel_path)
                        for _, template_lineno in template.debug_info:
                            source_lines.add(template_lineno)
                        break
                except Exception:
                    pass
        except Exception:
            pass

        if not source_lines:
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
            r"\{%.*endfilter.*%\}",
            r"\{\{-?\s*'\s*'\s*-?\}\}",
            r"\{\{-?\s*[\"']\\n[\"']\s*-?\}\}"
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

        return excluded

def coverage_init(reg, options):
    reg.add_file_tracer(JinjaPlugin(options))
