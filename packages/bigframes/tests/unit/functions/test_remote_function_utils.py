# Copyright 2024 Google LLC
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
import sys
from unittest.mock import patch

import bigframes_vendored.constants as constants
import pytest

from bigframes.functions import _utils, function_typing


@pytest.mark.parametrize(
    ("input_location", "expected_bq_location", "expected_cf_region"),
    [
        (None, "us", "us-central1"),
        ("us", "us", "us-central1"),
        ("eu", "eu", "europe-west1"),
        ("US-east4", "us-east4", "us-east4"),
    ],
)
def test_get_remote_function_locations(
    input_location, expected_bq_location, expected_cf_region
):
    """Tests getting remote function locations for various locations."""
    bq_location, cf_region = _utils.get_remote_function_locations(input_location)

    assert bq_location == expected_bq_location
    assert cf_region == expected_cf_region


@pytest.mark.parametrize(
    "func_hash, session_id, uniq_suffix, expected_name",
    [
        (
            "hash123",
            None,
            None,
            "bigframes-hash123",
        ),
        (
            "hash456",
            "session789",
            None,
            "bigframes-session789-hash456",
        ),
        (
            "hash123",
            None,
            "suffixABC",
            "bigframes-hash123-suffixABC",
        ),
        (
            "hash456",
            "session789",
            "suffixDEF",
            "bigframes-session789-hash456-suffixDEF",
        ),
    ],
)
def test_get_cloud_function_name(func_hash, session_id, uniq_suffix, expected_name):
    """Tests the construction of the cloud function name from its parts."""
    result = _utils.get_cloud_function_name(func_hash, session_id, uniq_suffix)

    assert result == expected_name


@pytest.mark.parametrize(
    "function_hash, session_id, uniq_suffix, expected_name",
    [
        (
            "hash123",
            "session456",
            None,
            "bigframes_session456_hash123",
        ),
        (
            "hash789",
            "sessionABC",
            "suffixDEF",
            "bigframes_sessionABC_hash789_suffixDEF",
        ),
    ],
)
def test_get_bigframes_function_name(
    function_hash, session_id, uniq_suffix, expected_name
):
    """Tests the construction of the BigQuery function name from its parts."""
    result = _utils.get_bigframes_function_name(function_hash, session_id, uniq_suffix)

    assert result == expected_name


def test_get_updated_package_requirements_no_extra_package():
    """Tests with no extra package."""
    result = _utils.get_updated_package_requirements(capture_references=False)

    assert result is None

    initial_packages = ["xgboost"]
    result = _utils.get_updated_package_requirements(
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
    result = _utils.get_updated_package_requirements(is_row_processor=True)

    assert result == expected


@patch("bigframes.functions._utils.warnings.warn")
@patch("bigframes.functions._utils.cloudpickle.__version__", "2.2.1")
def test_get_updated_package_requirements_ignore_version(mock_warn):
    """
    Tests with is_row_processor=True and ignore_package_version=True.
    Should add packages without versions and raise a warning.
    """
    expected = ["cloudpickle==2.2.1", "numpy", "pandas", "pyarrow"]
    result = _utils.get_updated_package_requirements(
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
    result_1 = _utils.get_updated_package_requirements(capture_references=False)

    assert result_1 is None

    # Case 2: capture_references=False but is_row_processor=True.
    expected_2 = ["numpy==1.24.4", "pandas==2.0.3", "pyarrow==14.0.1"]
    result_2 = _utils.get_updated_package_requirements(
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
    result = _utils.get_updated_package_requirements(
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
    result = _utils.get_updated_package_requirements(
        package_requirements=initial_packages, is_row_processor=True
    )

    assert result == expected


@patch("bigframes.functions._utils.cloudpickle.__version__", "2.2.1")
def test_get_updated_package_requirements_with_existing_cloudpickle():
    """Tests that cloudpickle is not added if it already exists."""
    initial_packages = ["cloudpickle==2.0.0"]
    expected = ["cloudpickle==2.0.0"]
    result = _utils.get_updated_package_requirements(
        package_requirements=initial_packages
    )

    assert result == expected


# Dynamically generate expected python versions for the test
_major = sys.version_info.major
_minor = sys.version_info.minor
_compat_version = f"python{_major}{_minor}"
_standard_version = f"python-{_major}.{_minor}"


@pytest.mark.parametrize(
    "is_compat, expected_version",
    [
        (True, _compat_version),
        (False, _standard_version),
    ],
)
def test_get_python_version(is_compat, expected_version):
    """Tests the python version for both standard and compat modes."""
    result = _utils.get_python_version(is_compat=is_compat)
    assert result == expected_version


def test_package_existed_helper():
    """Tests the _package_existed helper function directly."""
    reqs = ["pandas==1.0", "numpy", "scikit-learn>=1.2.0"]

    # Exact match
    assert _utils._package_existed(reqs, "pandas==1.0")
    # Different version
    assert _utils._package_existed(reqs, "pandas==2.0")
    # No version specified
    assert _utils._package_existed(reqs, "numpy")
    # Not in list
    assert not _utils._package_existed(reqs, "xgboost")
    # Empty list
    assert not _utils._package_existed([], "pandas")


def _function_add_one(x):
    return x + 1


def _function_add_two(x):
    return x + 2


@pytest.mark.parametrize(
    "func1, func2, should_be_equal, description",
    [
        (
            _function_add_one,
            _function_add_one,
            True,
            "Identical functions should have the same hash.",
        ),
        (
            _function_add_one,
            _function_add_two,
            False,
            "Different functions should have different hashes.",
        ),
    ],
)
def test_get_hash_without_package_requirements(
    func1, func2, should_be_equal, description
):
    """Tests function hashes without any requirements."""
    hash1 = _utils.get_hash(func1)
    hash2 = _utils.get_hash(func2)

    if should_be_equal:
        assert hash1 == hash2, f"FAILED: {description}"
    else:
        assert hash1 != hash2, f"FAILED: {description}"


@pytest.mark.parametrize(
    "reqs1, reqs2, should_be_equal, description",
    [
        (
            None,
            ["pandas>=1.0"],
            False,
            "Hash with or without requirements should differ from hash.",
        ),
        (
            ["pandas", "numpy", "scikit-learn"],
            ["numpy", "scikit-learn", "pandas"],
            True,
            "Same requirements should produce the same hash.",
        ),
        (
            ["pandas==1.0"],
            ["pandas==2.0"],
            False,
            "Different requirement versions should produce different hashes.",
        ),
    ],
)
def test_get_hash_with_package_requirements(reqs1, reqs2, should_be_equal, description):
    """Tests how package requirements affect the final hash."""
    hash1 = _utils.get_hash(_function_add_one, package_requirements=reqs1)
    hash2 = _utils.get_hash(_function_add_one, package_requirements=reqs2)

    if should_be_equal:
        assert hash1 == hash2, f"FAILED: {description}"
    else:
        assert hash1 != hash2, f"FAILED: {description}"


# Helper functions for signature inspection tests
def _func_one_arg_annotated(x: int) -> int:
    """A function with one annotated arg and an annotated return type."""
    return x


def _func_one_arg_unannotated(x):
    """A function with one unannotated arg and no return type annotation."""
    return x


def _func_two_args_annotated(x: int, y: str):
    """A function with two annotated args and no return type annotation."""
    return f"{x}{y}"


def _func_two_args_unannotated(x, y):
    """A function with two unannotated args and no return type annotation."""
    return f"{x}{y}"


def test_has_conflict_input_type_too_few_inputs():
    """Tests conflict when there are fewer input types than parameters."""
    signature = inspect.signature(_func_one_arg_annotated)
    assert _utils.has_conflict_input_type(signature, input_types=[])


def test_has_conflict_input_type_too_many_inputs():
    """Tests conflict when there are more input types than parameters."""
    signature = inspect.signature(_func_one_arg_annotated)
    assert _utils.has_conflict_input_type(signature, input_types=[int, str])


def test_has_conflict_input_type_type_mismatch():
    """Tests has_conflict_input_type with a conflicting type annotation."""
    signature = inspect.signature(_func_two_args_annotated)

    # The second type (bool) conflicts with the annotation (str).
    assert _utils.has_conflict_input_type(signature, input_types=[int, bool])


def test_has_conflict_input_type_no_conflict_annotated():
    """Tests that a matching, annotated signature is compatible."""
    signature = inspect.signature(_func_two_args_annotated)
    assert not _utils.has_conflict_input_type(signature, input_types=[int, str])


def test_has_conflict_input_type_no_conflict_unannotated():
    """Tests that a signature with no annotations is always compatible."""
    signature = inspect.signature(_func_two_args_unannotated)
    assert not _utils.has_conflict_input_type(signature, input_types=[int, float])


def test_has_conflict_output_type_no_conflict():
    """Tests has_conflict_output_type with type annotation."""
    signature = inspect.signature(_func_one_arg_annotated)

    assert _utils.has_conflict_output_type(signature, output_type=float)
    assert not _utils.has_conflict_output_type(signature, output_type=int)


def test_has_conflict_output_type_no_annotation():
    """Tests has_conflict_output_type without type annotation."""
    signature = inspect.signature(_func_one_arg_unannotated)

    assert not _utils.has_conflict_output_type(signature, output_type=int)
    assert not _utils.has_conflict_output_type(signature, output_type=float)


@pytest.mark.parametrize(
    ["metadata_options", "metadata_string"],
    (
        pytest.param(
            {},
            '{"value": {}}',
            id="empty",
        ),
        pytest.param(
            {"python_output_type": None},
            '{"value": {}}',
            id="None",
        ),
        pytest.param(
            {"python_output_type": list[bool]},
            '{"value": {"python_array_output_type": "bool"}}',
            id="list-bool",
        ),
        pytest.param(
            {"python_output_type": list[float]},
            '{"value": {"python_array_output_type": "float"}}',
            id="list-float",
        ),
        pytest.param(
            {"python_output_type": list[int]},
            '{"value": {"python_array_output_type": "int"}}',
            id="list-int",
        ),
        pytest.param(
            {"python_output_type": list[str]},
            '{"value": {"python_array_output_type": "str"}}',
            id="list-str",
        ),
    ),
)
def test_get_bigframes_metadata(metadata_options, metadata_string):

    assert _utils.get_bigframes_metadata(**metadata_options) == metadata_string


@pytest.mark.parametrize(
    ["output_type"],
    (
        pytest.param(bool),
        pytest.param(bytes),
        pytest.param(float),
        pytest.param(int),
        pytest.param(str),
        pytest.param(list),
        pytest.param(list[bytes], id="list-bytes"),
    ),
)
def test_get_bigframes_metadata_array_type_not_serializable(output_type):
    with pytest.raises(ValueError) as context:
        _utils.get_bigframes_metadata(python_output_type=output_type)

    assert str(context.value) == (
        f"python_output_type {output_type} is not serializable. {constants.FEEDBACK_LINK}"
    )


@pytest.mark.parametrize(
    ["metadata_string", "python_output_type"],
    (
        pytest.param(
            None,
            None,
            id="None",
        ),
        pytest.param(
            "",
            None,
            id="empty",
        ),
        pytest.param(
            "{}",
            None,
            id="empty-dict",
        ),
        pytest.param(
            '{"value": {}}',
            None,
            id="empty-value",
        ),
        pytest.param(
            '{"value": {"python_array_output_type": "bool"}}',
            list[bool],
            id="list-bool",
        ),
        pytest.param(
            '{"value": {"python_array_output_type": "float"}}',
            list[float],
            id="list-float",
        ),
        pytest.param(
            '{"value": {"python_array_output_type": "int"}}',
            list[int],
            id="list-int",
        ),
        pytest.param(
            '{"value": {"python_array_output_type": "str"}}',
            list[str],
            id="list-str",
        ),
    ),
)
def test_get_python_output_type_from_bigframes_metadata(
    metadata_string, python_output_type
):

    assert (
        _utils.get_python_output_type_from_bigframes_metadata(metadata_string)
        == python_output_type
    )


def test_metadata_roundtrip_supported_array_types():
    for array_of in function_typing.RF_SUPPORTED_ARRAY_OUTPUT_PYTHON_TYPES:
        ser = _utils.get_bigframes_metadata(python_output_type=list[array_of])  # type: ignore
        deser = _utils.get_python_output_type_from_bigframes_metadata(ser)

        assert deser == list[array_of]  # type: ignore
