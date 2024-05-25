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

import bigframes_vendored.ibis.backends.bigquery.datatypes as third_party_ibis_bqtypes
from ibis.expr import datatypes as ibis_types
import pytest

import bigframes.dtypes
import bigframes.functions.remote_function
from tests.unit import resources


def test_supported_types_correspond():
    # The same types should be representable by the supported Python and BigQuery types.
    ibis_types_from_python = {
        ibis_types.dtype(t) for t in bigframes.dtypes.SUPPORTED_IO_PYTHON_TYPES
    }
    ibis_types_from_bigquery = {
        third_party_ibis_bqtypes.BigQueryType.to_ibis(tk)
        for tk in bigframes.dtypes.SUPPORTED_IO_BIGQUERY_TYPEKINDS
    }

    assert ibis_types_from_python == ibis_types_from_bigquery


def test_missing_input_types():
    session = resources.create_bigquery_session()
    remote_function_decorator = bigframes.functions.remote_function.remote_function(
        session=session
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
    session = resources.create_bigquery_session()
    remote_function_decorator = bigframes.functions.remote_function.remote_function(
        session=session
    )

    def function_without_return_annotation(myparam: int):
        return str(myparam)

    assert function_without_return_annotation(42) == "42"

    with pytest.raises(
        ValueError,
        match="'output_type' was not set .* missing a return type annotation",
    ):
        remote_function_decorator(function_without_return_annotation)
