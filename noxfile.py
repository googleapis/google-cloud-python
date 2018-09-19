# Copyright 2018 Google LLC
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

"""Build and test configuration file.

Assumes ``nox >= 2018.9.14`` is installed.
"""

import os

import nox


NOX_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_INTERPRETER = "3.7"
PYPY = "pypy3"
ALL_INTERPRETERS = ("3.5", "3.6", "3.7", PYPY)


def get_path(*names):
    return os.path.join(NOX_DIR, *names)


@nox.session(py=ALL_INTERPRETERS)
def unit(session):
    # Install all dependencies.
    session.install("pytest")
    session.install(".")
    # Run py.test against the unit tests.
    run_args = ["pytest"] + session.posargs + [get_path("tests", "unit")]
    session.run(*run_args)


@nox.session(python=DEFAULT_INTERPRETER)
def blacken(session):
    # Install all dependencies.
    session.install("black")
    # Run ``black``.
    session.run(
        "black",
        "--line-length=79",
        get_path("noxfile.py"),
        get_path("src"),
        get_path("tests"),
    )
