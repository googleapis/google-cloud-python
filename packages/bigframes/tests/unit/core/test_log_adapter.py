# Copyright 2023 Google LLC
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

from unittest import mock

from google.cloud import bigquery
import pytest

from bigframes.core import log_adapter

# The limit is 64 (https://cloud.google.com/bigquery/docs/labels-intro#requirements),
# but leave a few spare for internal labels to be added.
# See internal issue 386825477.
MAX_LABELS_COUNT = 56


@pytest.fixture
def mock_bqclient():
    mock_bqclient = mock.create_autospec(spec=bigquery.Client)
    return mock_bqclient


@pytest.fixture
def test_instance():
    # Create a simple class for testing
    @log_adapter.class_logger
    class TestClass:
        def method1(self):
            pass

        def method2(self):
            self.method3()

        def method3(self):
            pass

        @log_adapter.log_name_override("override_name")
        def method4(self):
            pass

        @property
        def my_field(self):
            return 0

    return TestClass()


@pytest.fixture
def test_method():
    @log_adapter.method_logger
    def method1():
        pass

    return method1


@pytest.fixture
def test_method_w_custom_base():
    def method1():
        pass

    _decorated_method = log_adapter.method_logger(method1, custom_base_name="pandas")

    return _decorated_method


def test_class_attribute_logging(test_instance):
    test_instance.method1()
    test_instance.method2()
    test_instance.method4()

    # Check if the methods were added to the _api_methods list
    api_methods = log_adapter.get_and_reset_api_methods()
    assert "testclass-method1" in api_methods
    assert "testclass-method2" in api_methods
    assert "testclass-method3" not in api_methods
    assert "testclass-method4" not in api_methods
    assert "testclass-override_name" in api_methods


def test_method_logging(test_method):
    test_method()
    api_methods = log_adapter.get_and_reset_api_methods()
    assert "locals-method1" in api_methods


def test_method_logging_with_custom_base_name(test_method_w_custom_base):
    test_method_w_custom_base()
    api_methods = log_adapter.get_and_reset_api_methods()
    assert "pandas-method1" in api_methods


def test_property_logging(test_instance):
    test_instance.my_field

    # Check if the properties were added to the _api_methods list
    api_methods = log_adapter.get_and_reset_api_methods()
    assert "testclass-my_field" in api_methods


def test_add_api_method_limit(test_instance):
    # Ensure that add_api_method correctly adds a method to _api_methods
    for i in range(70):
        test_instance.method2()
    assert len(log_adapter._api_methods) == MAX_LABELS_COUNT


def test_get_and_reset_api_methods(test_instance):
    # Ensure that get_and_reset_api_methods returns a copy and resets the list
    test_instance.method1()
    test_instance.method2()
    previous_methods = log_adapter.get_and_reset_api_methods()
    assert previous_methods is not None
    assert log_adapter._api_methods == []


@pytest.mark.parametrize(
    ("class_name", "method_name", "args", "kwargs", "task", "expected_labels"),
    (
        (
            "DataFrame",
            "resample",
            ["a", "b", "c"],
            {"aa": "bb", "rule": "1s"},
            log_adapter.PANDAS_API_TRACKING_TASK,
            {
                "task": log_adapter.PANDAS_API_TRACKING_TASK,
                "class_name": "dataframe",
                "method_name": "resample",
                "args_count": 3,
                "kwargs_0": "rule",
            },
        ),
        (
            "Series",
            "resample",
            [],
            {"aa": "bb", "rule": "1s"},
            log_adapter.PANDAS_PARAM_TRACKING_TASK,
            {
                "task": log_adapter.PANDAS_PARAM_TRACKING_TASK,
                "class_name": "series",
                "method_name": "resample",
                "args_count": 0,
                "kwargs_0": "rule",
            },
        ),
        (
            "DataFrame",
            "resample",
            [],
            {"aa": "bb"},
            log_adapter.PANDAS_API_TRACKING_TASK,
            {
                "task": log_adapter.PANDAS_API_TRACKING_TASK,
                "class_name": "dataframe",
                "method_name": "resample",
                "args_count": 0,
            },
        ),
        (
            "DataFrame",
            "resample",
            [],
            {},
            log_adapter.PANDAS_API_TRACKING_TASK,
            {
                "task": log_adapter.PANDAS_API_TRACKING_TASK,
                "class_name": "dataframe",
                "method_name": "resample",
                "args_count": 0,
            },
        ),
        (
            "pandas",
            "concat",
            [[None, None]],
            {"axis": 1},
            log_adapter.PANDAS_API_TRACKING_TASK,
            {
                "task": log_adapter.PANDAS_API_TRACKING_TASK,
                "class_name": "pandas",
                "method_name": "concat",
                "args_count": 1,
                "kwargs_0": "axis",
            },
        ),
    ),
)
def test_submit_pandas_labels(
    mock_bqclient, class_name, method_name, args, kwargs, task, expected_labels
):
    log_adapter.submit_pandas_labels(
        mock_bqclient, class_name, method_name, args, kwargs, task
    )

    mock_bqclient.query.assert_called_once()

    query_call_args = mock_bqclient.query.call_args_list[0]
    labels = query_call_args[1]["job_config"].labels
    assert labels == expected_labels


def test_submit_pandas_labels_without_valid_params_for_param_logging(mock_bqclient):
    log_adapter.submit_pandas_labels(
        mock_bqclient,
        "Series",
        "resample",
        task=log_adapter.PANDAS_PARAM_TRACKING_TASK,
    )

    # For param tracking task without kwargs, we won't submit labels
    mock_bqclient.query.assert_not_called()


@pytest.mark.parametrize(
    ("class_name", "method_name"),
    (
        ("Series", "_repr_latex_"),
        (
            "DataFrame",
            # __call__ should be excluded.
            # It's implemented on the pd.DataFrame class but not pd.DataFrame instances.
            "__call__",
        ),
        (
            "Series",
            # __call__ should be excluded.
            # It's implemented on the pd.Series class but not pd.Series instances.
            "__call__",
        ),
    ),
)
def test_submit_pandas_labels_with_internal_method(
    mock_bqclient, class_name, method_name
):
    log_adapter.submit_pandas_labels(
        mock_bqclient,
        class_name,
        method_name,
        task=log_adapter.PANDAS_API_TRACKING_TASK,
    )
    mock_bqclient.query.assert_not_called()
