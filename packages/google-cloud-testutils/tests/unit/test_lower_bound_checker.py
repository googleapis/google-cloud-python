# Copyright 2021 Google LLC
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

from contextlib import contextmanager
from pathlib import Path
import re
import tempfile
from typing import List

from click.testing import CliRunner
import pytest

from test_utils.lower_bound_checker import lower_bound_checker

RUNNER = CliRunner()

PACKAGE_LIST_REGEX = re.compile(r"Error.*[\[\{](.+)[\]\}]")
DIFFERENT_VERSIONS_LIST_REGEX = re.compile("'(.*?)' lower bound is")

# These packages are installed into the environment by the nox session
# See 'resources/' for the setup.py files
GOOD_PACKAGE = "valid-package"
BAD_PACKAGE = "invalid-package"


def parse_error_msg(msg: str) -> List[str]:
    """Get package names from the error message.
    
    Example:
        Error: setup.py is missing explicit lower bounds for the following packages: ["requests", "grpcio"]
    """
    match = PACKAGE_LIST_REGEX.search(msg)

    reqs = []

    if match:
        reqs = match.groups(1)[0].split(",")
        reqs = [r.strip().replace("'", "").replace('"', "") for r in reqs]
    
    return reqs

def parse_diff_versions_error_msg(msg: str) -> List[str]:
    """Get package names from the error message listing different versions
    
    Example:
        'requests' lower bound is 1.2.0 in setup.py but constraints file has 1.3.0
        'grpcio' lower bound is 1.0.0 in setup.py but constraints file has 1.10.0
    """
    pattern = re.compile(DIFFERENT_VERSIONS_LIST_REGEX)
    pkg_names = pattern.findall(msg)

    return pkg_names

@contextmanager
def constraints_file(requirements: List[str]):
    """Write the list of requirements into a temporary file"""

    tmpdir = tempfile.TemporaryDirectory()
    constraints_path = Path(tmpdir.name) / "constraints.txt"

    constraints_path.write_text("\n".join(requirements))
    yield constraints_path

    tmpdir.cleanup()


def test_update_constraints():
    with tempfile.TemporaryDirectory() as tmpdir:
        constraints_path = Path(tmpdir) / "constraints.txt"

        result = RUNNER.invoke(
            lower_bound_checker.update, ["--package-name", GOOD_PACKAGE, "--constraints-file", str(constraints_path)]
        )

        assert result.exit_code == 0
        assert constraints_path.exists()
    
        output = constraints_path.read_text().split("\n")

        assert output == ["click==7.0.0", "grpcio==1.0.0", "packaging==14.0", "requests==1.0.0", "six==1.0.0",]



def test_update_constraints_overwrites_existing_file():
    constraints = [
        "requests==1.0.0",
        "packaging==13.0",
        "six==1.6.0",
        "click==5.0.0",
    ]
    with constraints_file(constraints) as c:
        result = RUNNER.invoke(
            lower_bound_checker.update, ["--package-name", GOOD_PACKAGE, "--constraints-file", c]
        )

        assert result.exit_code == 0

        output = c.read_text().split("\n")
        assert output == ["click==7.0.0", "grpcio==1.0.0", "packaging==14.0", "requests==1.0.0", "six==1.0.0",
        ]

def test_update_constraints_with_setup_py_missing_lower_bounds():
    constraints = [
        "requests==1.0.0",
        "packaging==14.0",
        "six==1.0.0",
        "click==7.0.0",
    ]
    with constraints_file(constraints) as c:
        result = RUNNER.invoke(
            lower_bound_checker.update, ["--package-name", BAD_PACKAGE, "--constraints-file", c]
        )

    assert result.exit_code == 2
    assert "setup.py is missing explicit lower bounds" in result.output

    invalid_pkg_list = parse_error_msg(result.output)
    assert set(invalid_pkg_list) == {"requests", "packaging", "six"}



def test_check():
    constraints = [
        "requests==1.0.0",
        "packaging==14.0",
        "six==1.0.0",
        "click==7.0.0",
        "grpcio==1.0.0"
    ]
    with constraints_file(constraints) as c:
        result = RUNNER.invoke(
            lower_bound_checker.check, ["--package-name", GOOD_PACKAGE, "--constraints-file", c]
        )

    assert result.exit_code == 0


def test_update_constraints_with_extra_constraints():
    constraints = [
        "requests==1.0.0",
        "packaging==14.0",
        "six==1.0.0",
        "click==7.0.0",
        "grpcio==1.0.0",
        "pytest==6.0.0",  # additional requirement
    ]
    with constraints_file(constraints) as c:
        result = RUNNER.invoke(
            lower_bound_checker.check, ["--package-name", GOOD_PACKAGE, "--constraints-file", c]
        )

    assert result.exit_code == 0


def test_check_with_missing_constraints_file():
    result = RUNNER.invoke(
        lower_bound_checker.check,
        [
            "--package-name",
            GOOD_PACKAGE,
            "--constraints-file",
            "missing_constraints.txt",
        ],
    )

    assert result.exit_code == 1
    assert isinstance(result.exception, FileNotFoundError)


def test_check_with_constraints_file_invalid_pins():
    constraints = [
        "requests==1.0.0",
        "packaging==14.0",
        "six==1.0.0, <2.0.0dev",  # should be ==
        "click>=7.0.0",  # should be ==
    ]
    with constraints_file(constraints) as c:
        result = RUNNER.invoke(
            lower_bound_checker.check, ["--package-name", GOOD_PACKAGE, "--constraints-file", c]
        )

    assert result.exit_code == 2

    invalid_pkg_list = parse_error_msg(result.output)

    assert set(invalid_pkg_list) == {"six", "click"}


def test_check_with_constraints_file_missing_packages():
    constraints = [
        "requests==1.0.0",
        "packaging==14.0",
        # missing 'six' and 'click' and extra 'grpcio'
    ]
    with constraints_file(constraints) as c:
        result = RUNNER.invoke(
            lower_bound_checker.check, ["--package-name", GOOD_PACKAGE, "--constraints-file", c]
        )

    assert result.exit_code == 2

    invalid_pkg_list = parse_error_msg(result.output)
    assert set(invalid_pkg_list) == {"six", "click", "grpcio"}


def test_check_with_constraints_file_different_versions():
    constraints = [
        "requests==1.2.0",  # setup.py has 1.0.0
        "packaging==14.1",  # setup.py has 14.0
        "six==1.4.0",  # setup.py has 1.0.0
        "click==7.0.0",
        "grpcio==1.0.0"
    ]
    with constraints_file(constraints) as c:
        result = RUNNER.invoke(
            lower_bound_checker.check, ["--package-name", GOOD_PACKAGE, "--constraints-file", c]
        )

    assert result.exit_code == 2

    invalid_pkg_list = parse_diff_versions_error_msg(result.output)
    assert set(invalid_pkg_list) == {"requests", "packaging", "six"}


def test_check_with_setup_py_missing_lower_bounds():
    constraints = [
        "requests==1.0.0",
        "packaging==14.0",
        "six==1.0.0",
        "click==7.0.0",
    ]
    with constraints_file(constraints) as c:
        result = RUNNER.invoke(
            lower_bound_checker.check, ["--package-name", BAD_PACKAGE, "--constraints-file", c]
        )

    assert result.exit_code == 2

    invalid_pkg_list = parse_error_msg(result.output)
    assert set(invalid_pkg_list) == {"requests", "packaging", "six"}
