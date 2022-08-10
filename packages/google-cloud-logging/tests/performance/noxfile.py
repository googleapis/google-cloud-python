# -*- coding: utf-8 -*-
#
# Copyright 2022 Google LLC
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

from __future__ import absolute_import
import os
import pathlib
import re
from colorlog.escape_codes import parse_colors

import nox


DEFAULT_PYTHON_VERSION = "3.8"

PERFORMANCE_TEST_PYTHON_VERSIONS = ["3.8"]

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
REPO_ROOT_DIRECTORY = CURRENT_DIRECTORY.parent.parent

REPO_URL = "https://github.com/googleapis/python-logging.git"
CLONE_REPO_DIR = "python-logging-main"

# 'docfx' is excluded since it only needs to run in 'docs-presubmit'
nox.options.sessions = ["performance", "performance_regression"]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True


@nox.session(python=PERFORMANCE_TEST_PYTHON_VERSIONS)
def performance(session):
    """Run the performance test suite."""
    # Use pre-release gRPC for performance tests.
    session.install("--pre", "grpcio")

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install(
        "mock",
        "pandas",
        "rich",
        "pytest",
        "google-cloud-testutils",
    )
    session.install("-e", str(REPO_ROOT_DIRECTORY))

    file_path = f"perf_{session.python}_sponge_log.xml"
    session.run(
        "py.test",
        f"--ignore={CLONE_REPO_DIR}",
        "-s",
        f"--junitxml={file_path}",
        str(CURRENT_DIRECTORY),
        *session.posargs,
    )
    get_junitxml_results(file_path)


@nox.session(python=PERFORMANCE_TEST_PYTHON_VERSIONS)
def print_last_results(session):
    """Print results from last performance test session."""
    file_path = f"perf_{session.python}_sponge_log.xml"
    get_junitxml_results(file_path)


def get_junitxml_results(file_path, print_results=True):
    """Print results from specified results file."""
    results = None
    if os.path.exists(file_path):
        if print_results:
            print(f"{file_path} results:")
        with open(file_path, "r") as file:
            data = file.read().replace("\n", "")
            total = 0
            results = {}
            for entry in data.split("testcase classname")[1:]:
                name = re.search(r'name="+(\w+)', entry)[1]
                time = re.search(r'time="+([0-9\.]+)', entry)[1]
                total += float(time)
                if print_results:
                    print(f"\t{name}: {time}s")
                results[name] = float(time)
            if print_results:
                print(f"\tTotal: {total:.3f}s")
    else:
        print(f"error: {file_path} not found")
    return results


@nox.session(python=PERFORMANCE_TEST_PYTHON_VERSIONS)
def performance_regression(session, percent_threshold=10):
    """Check performance against repo main."""

    clone_dir = os.path.join(CURRENT_DIRECTORY, CLONE_REPO_DIR)

    if not os.path.exists(clone_dir):
        print("downloading copy of repo at `main`")
        session.run("git", "clone", REPO_URL, CLONE_REPO_DIR)

    # Use pre-release gRPC for performance tests.
    session.install("--pre", "grpcio")

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install(
        "mock",
        "pandas",
        "rich",
        "pytest",
        "google-cloud-testutils",
    )

    main_file_name = f"main_perf_{session.python}_sponge_log.xml"
    head_file_name = f"head_perf_{session.python}_sponge_log.xml"
    # test against main
    print("testing against library at `main`...")
    session.install("-e", str(clone_dir))
    session.run(
        "py.test",
        f"--ignore={CLONE_REPO_DIR}",
        "-s",
        f"--junitxml={main_file_name}",
        str(CURRENT_DIRECTORY),
        *session.posargs,
        success_codes=[1, 0],  # don't report failures at this step
    )
    # test head
    print("testing against library at `HEAD`...")
    session.install("-e", str(REPO_ROOT_DIRECTORY))
    session.run(
        "py.test",
        f"--ignore={CLONE_REPO_DIR}",
        "-s",
        f"--junitxml={head_file_name}",
        str(CURRENT_DIRECTORY),
        *session.posargs,
        success_codes=[1, 0],  # don't report failures at this step
    )
    # print results
    main_results = get_junitxml_results(main_file_name, print_results=False)
    head_results = get_junitxml_results(head_file_name, print_results=False)
    all_pass = True
    for test, time in head_results.items():
        if test in main_results:
            prev_time = main_results[test]
            diff = time - prev_time
            percent_diff = diff / prev_time
            test_passes = percent_diff * 100 < percent_threshold
            all_pass = all_pass and test_passes
            if not test_passes:
                color = parse_colors("red")
            elif diff > 0:
                color = parse_colors("yellow")
            else:
                color = parse_colors("green")
            print(
                f"{test}: {color} {diff:+.3f}s ({percent_diff:+.1%}){parse_colors('reset')}"
            )
        else:
            print(f"{test}: ???")
    if not all_pass:
        session.error(f"performance degraded >{percent_threshold}%")
