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
# Unless required by applicable law or agreed to in writing, software/
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import pathlib
import nox

DEFAULT_PYTHON_VERSION = "3.14"
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
REPO_ROOT = CURRENT_DIRECTORY.parent.parent

# Hardcoded dictionary of documentation files.
# Format: {"Display Title": "filename.md" or absolute path}
DOCS_MAP = {
    "Getting started": str(REPO_ROOT / "README.rst"),
}

nox.options.sessions = [
    "lint",
    "docfx",
]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters."""
    session.install("ruff")
    session.run("ruff", "check", ".")

@nox.session(python="3.10")
def docfx(session):
    """Build the docfx yaml files for this library."""
    session.install("PyYAML", "pypandoc")
    
    # Construct arguments for the helper script
    args = [str(CURRENT_DIRECTORY), str(REPO_ROOT)]
    for title, source in DOCS_MAP.items():
        args.extend([title, str(source)])
    
    session.run("python", "docfx_helper.py", *args)
