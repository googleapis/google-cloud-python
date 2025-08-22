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


def test_has_conflict_output_type_no_conflict():
    """Tests has_conflict_output_type with type annotation."""
    # Helper functions with type annotation for has_conflict_output_type.
    def _func_with_return_type(x: int) -> int:
        return x

    signature = inspect.signature(_func_with_return_type)

    assert _utils.has_conflict_output_type(signature, output_type=float)
    assert not _utils.has_conflict_output_type(signature, output_type=int)


def test_has_conflict_output_type_no_annotation():
    """Tests has_conflict_output_type without type annotation."""
    # Helper functions without type annotation for has_conflict_output_type.
    def _func_without_return_type(x):
        return x

    signature = inspect.signature(_func_without_return_type)

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
