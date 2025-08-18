# Copyright 2025 Google LLC
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

import inspect
from unittest.mock import patch

from bigframes.functions._utils import (
    _package_existed,
    get_updated_package_requirements,
    has_conflict_output_type,
)


def test_get_updated_package_requirements_no_extra_package():
    """Tests with no extra package."""
    result = get_updated_package_requirements(capture_references=False)
    assert result is None

    initial_packages = ["xgboost"]
    result = get_updated_package_requirements(
        initial_packages, capture_references=False
    )
    assert result == initial_packages


@patch("bigframes.functions._utils.numpy.__version__", "1.24.4")
@patch("bigframes.functions._utils.pyarrow.__version__", "14.0.1")
@patch("bigframes.functions._utils.pandas.__version__", "2.0.3")
@patch("bigframes.functions._utils.cloudpickle.__version__", "2.2.1")
def test_get_updated_package_requirements_is_row_processor_with_versions():
    """Tests with is_row_processor=True and specific versions."""
    expected = [
        "cloudpickle==2.2.1",
        "numpy==1.24.4",
        "pandas==2.0.3",
        "pyarrow==14.0.1",
    ]
    result = get_updated_package_requirements(is_row_processor=True)
    assert result == expected


@patch("bigframes.functions._utils.warnings.warn")
@patch("bigframes.functions._utils.cloudpickle.__version__", "2.2.1")
def test_get_updated_package_requirements_ignore_version(mock_warn):
    """
    Tests with is_row_processor=True and ignore_package_version=True.
    Should add packages without versions and raise a warning.
    """
    expected = ["cloudpickle==2.2.1", "numpy", "pandas", "pyarrow"]
    result = get_updated_package_requirements(
        is_row_processor=True, ignore_package_version=True
    )
    assert result == expected
    # Verify that a warning was issued.
    mock_warn.assert_called_once()


@patch("bigframes.functions._utils.numpy.__version__", "1.24.4")
@patch("bigframes.functions._utils.pyarrow.__version__", "14.0.1")
@patch("bigframes.functions._utils.pandas.__version__", "2.0.3")
def test_get_updated_package_requirements_capture_references_false():
    """
    Tests with capture_references=False.
    Should not add cloudpickle but should add others if requested.
    """
    # Case 1: Only capture_references=False.
    result_1 = get_updated_package_requirements(capture_references=False)
    assert result_1 is None

    # Case 2: capture_references=False but is_row_processor=True.
    expected_2 = ["numpy==1.24.4", "pandas==2.0.3", "pyarrow==14.0.1"]
    result_2 = get_updated_package_requirements(
        is_row_processor=True, capture_references=False
    )
    assert result_2 == expected_2


@patch("bigframes.functions._utils.numpy.__version__", "1.24.4")
@patch("bigframes.functions._utils.pyarrow.__version__", "14.0.1")
@patch("bigframes.functions._utils.pandas.__version__", "2.0.3")
@patch("bigframes.functions._utils.cloudpickle.__version__", "2.2.1")
def test_get_updated_package_requirements_non_overlapping_packages():
    """Tests providing an initial list of packages that do not overlap."""
    initial_packages = ["scikit-learn==1.3.0", "xgboost"]
    expected = [
        "cloudpickle==2.2.1",
        "numpy==1.24.4",
        "pandas==2.0.3",
        "pyarrow==14.0.1",
        "scikit-learn==1.3.0",
        "xgboost",
    ]
    result = get_updated_package_requirements(
        package_requirements=initial_packages, is_row_processor=True
    )
    assert result == expected


@patch("bigframes.functions._utils.numpy.__version__", "1.24.4")
@patch("bigframes.functions._utils.pyarrow.__version__", "14.0.1")
@patch("bigframes.functions._utils.pandas.__version__", "2.0.3")
@patch("bigframes.functions._utils.cloudpickle.__version__", "2.2.1")
def test_get_updated_package_requirements_overlapping_packages():
    """Tests that packages are not added if they already exist."""
    # The function should respect the pre-existing pandas version.
    initial_packages = ["pandas==1.5.3", "numpy"]
    expected = [
        "cloudpickle==2.2.1",
        "numpy",
        "pandas==1.5.3",
        "pyarrow==14.0.1",
    ]
    result = get_updated_package_requirements(
        package_requirements=initial_packages, is_row_processor=True
    )
    assert result == expected


@patch("bigframes.functions._utils.cloudpickle.__version__", "2.2.1")
def test_get_updated_package_requirements_with_existing_cloudpickle():
    """Tests that cloudpickle is not added if it already exists."""
    initial_packages = ["cloudpickle==2.0.0"]
    expected = ["cloudpickle==2.0.0"]
    result = get_updated_package_requirements(package_requirements=initial_packages)
    assert result == expected


def test_package_existed_helper():
    """Tests the _package_existed helper function directly."""
    reqs = ["pandas==1.0", "numpy", "scikit-learn>=1.2.0"]
    # Exact match
    assert _package_existed(reqs, "pandas==1.0")
    # Different version
    assert _package_existed(reqs, "pandas==2.0")
    # No version specified
    assert _package_existed(reqs, "numpy")
    # Not in list
    assert not _package_existed(reqs, "xgboost")
    # Empty list
    assert not _package_existed([], "pandas")


def test_has_conflict_output_type_no_conflict():
    """Tests has_conflict_output_type with type annotation."""
    # Helper functions with type annotation for has_conflict_output_type.
    def _func_with_return_type(x: int) -> int:
        return x

    signature = inspect.signature(_func_with_return_type)

    assert has_conflict_output_type(signature, output_type=float)
    assert not has_conflict_output_type(signature, output_type=int)


def test_has_conflict_output_type_no_annotation():
    """Tests has_conflict_output_type without type annotation."""
    # Helper functions without type annotation for has_conflict_output_type.
    def _func_without_return_type(x):
        return x

    signature = inspect.signature(_func_without_return_type)

    assert not has_conflict_output_type(signature, output_type=int)
    assert not has_conflict_output_type(signature, output_type=float)
