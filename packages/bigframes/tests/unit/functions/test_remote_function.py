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

import re

import pandas
import pytest

import bigframes.functions.function as bff
import bigframes.series
from bigframes.testing import mocks


@pytest.mark.parametrize(
    "series_type",
    (
        pytest.param(
            pandas.Series,
            id="pandas.Series",
        ),
        pytest.param(
            bigframes.series.Series,
            id="bigframes.series.Series",
        ),
    ),
)
def test_series_input_types_to_str(series_type):
    """Check that is_row_processor=True uses str as the input type to serialize a row."""
    session = mocks.create_bigquery_session()
    remote_function_decorator = bff.remote_function(
        session=session, cloud_function_service_account="default"
    )

    with pytest.warns(
        bigframes.exceptions.PreviewWarning,
        match=re.escape("input_types=Series is in preview."),
    ):

        @remote_function_decorator
        def axis_1_function(myparam: series_type) -> str:  # type: ignore
            return "Hello, " + myparam["str_col"] + "!"  # type: ignore

    # Still works as a normal function.
    assert axis_1_function(pandas.Series({"str_col": "World"})) == "Hello, World!"


def test_missing_input_types():
    session = mocks.create_bigquery_session()
    remote_function_decorator = bff.remote_function(
        session=session, cloud_function_service_account="default"
    )

    def function_without_parameter_annotations(myparam) -> str:
        return str(myparam)

    assert function_without_parameter_annotations(42) == "42"

    with pytest.raises(
        ValueError,
        match="'input_types' was not set .* 'myparam' is missing a type annotation",
    ):
        remote_function_decorator(function_without_parameter_annotations)


def test_missing_output_type():
    session = mocks.create_bigquery_session()
    remote_function_decorator = bff.remote_function(
        session=session, cloud_function_service_account="default"
    )

    def function_without_return_annotation(myparam: int):
        return str(myparam)

    assert function_without_return_annotation(42) == "42"

    with pytest.raises(
        ValueError,
        match="'output_type' was not set .* missing a return type annotation",
    ):
        remote_function_decorator(function_without_return_annotation)


def test_deploy_remote_function():
    session = mocks.create_bigquery_session()

    def my_remote_func(x: int) -> int:
        return x * 2

    deployed = session.deploy_remote_function(
        my_remote_func, cloud_function_service_account="test_sa@example.com"
    )

    # Test that the function would have been deployed somewhere.
    assert deployed.bigframes_bigquery_function


def test_deploy_remote_function_with_name():
    session = mocks.create_bigquery_session()

    def my_remote_func(x: int) -> int:
        return x * 2

    deployed = session.deploy_remote_function(
        my_remote_func,
        name="my_custom_name",
        cloud_function_service_account="test_sa@example.com",
    )

    # Test that the function would have been deployed somewhere.
    assert "my_custom_name" in deployed.bigframes_bigquery_function


def test_deploy_udf():
    session = mocks.create_bigquery_session()

    def my_remote_func(x: int) -> int:
        return x * 2

    deployed = session.deploy_udf(my_remote_func)

    # Test that the function would have been deployed somewhere.
    assert deployed.bigframes_bigquery_function


def test_deploy_udf_with_name():
    session = mocks.create_bigquery_session()

    def my_remote_func(x: int) -> int:
        return x * 2

    deployed = session.deploy_udf(my_remote_func, name="my_custom_name")

    # Test that the function would have been deployed somewhere.
    assert "my_custom_name" in deployed.bigframes_bigquery_function
