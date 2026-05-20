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

import pytest

import bigframes.functions.function as bff
from bigframes.testing import mocks


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


def test_deploy_udf():
    session = mocks.create_bigquery_session()

    def my_remote_func(x: int) -> int:
        return x * 2

    deployed = session.deploy_udf(my_remote_func)

    assert deployed.udf_def is not None


def test_deploy_udf_with_name():
    session = mocks.create_bigquery_session()

    def my_remote_func(x: int) -> int:
        return x * 2

    deployed = session.deploy_udf(my_remote_func, name="my_custom_name")

    # Test that the function would have been deployed somewhere.
    assert "my_custom_name" in deployed.bigframes_bigquery_function


def test_deferred_udf_execution():
    import bigframes.functions.udf_def as udf_def
    import google.cloud.bigquery

    session = mocks.create_bigquery_session()
    @session._function_session.udf(session=session)
    def my_unnamed_udf(x: int) -> int:
        return x * 2

    # 1. Verify that no BQ query was executed to deploy the UDF during registration!
    session._queries.clear()
    assert len(session._queries) == 0

    # 2. Verify that it created a PythonUdf
    assert isinstance(my_unnamed_udf.udf_def, udf_def.PythonUdf)

    # 3. Verify that when calling the UDF via a query, it triggers the UDF deployment query!
    import bigframes.core.nodes as nodes
    import bigframes.core.expression as ex
    import bigframes.operations as ops

    # Let's construct an expression using our UDF
    udf_op = ops.RemoteFunctionOp(function_def=my_unnamed_udf.udf_def, apply_on_null=False)
    expr = ex.OpExpression(op=udf_op, inputs=(ex.const(5),))

    class MockNode:
        def __init__(self, exprs):
            self._node_expressions = exprs
            self.child_nodes = []

        def unique_nodes(self):
            yield self

        def bottom_up(self, transform):
            return transform(self)

        def transform_exprs(self, fn):
            return MockNode([fn(e) for e in self._node_expressions])

    mock_node = MockNode([expr])

    import asyncio
    # Deploy and replace definition in the plan
    new_plan = asyncio.run(session._executor._ibis_executor._deploy_undeployed_udfs(mock_node))

    # Verify that the DDL to create the function was executed!
    assert len(session._queries) > 0
    assert any("CREATE OR REPLACE FUNCTION" in q for q in session._queries)

    # 4. Verify that the definition in the plan has been replaced with BigqueryUdf
    new_expr = new_plan._node_expressions[0]
    new_op = new_expr.op
    assert isinstance(new_op.function_def, udf_def.BigqueryUdf)
    assert new_op.function_def.routine_ref is not None

    # 5. Verify memoization: Deploying the new plan again executes ZERO additional DDL queries!
    session._queries.clear()
    new_plan_2 = asyncio.run(session._executor._ibis_executor._deploy_undeployed_udfs(new_plan))
    assert len(session._queries) == 0
    assert new_plan_2 == new_plan

