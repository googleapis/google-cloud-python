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

from datetime import datetime
import importlib.util
import inspect
import math  # must keep this at top level to test udf referring global import
import os.path
import shutil
import tempfile
import textwrap

from google.api_core.exceptions import NotFound, ResourceExhausted
from google.cloud import bigquery, functions_v2
import pandas
import pytest
import test_utils.prefixer

import bigframes
from bigframes.remote_function import (
    get_cloud_function_name,
    get_remote_function_locations,
)
from tests.system.utils import assert_pandas_df_equal

# Use this to control the number of cloud functions being deleted in a single
# test session. This should help soften the spike of the number of mutations per
# minute tracked against a quota limit (default 60, increased to 120 for
# bigframes-dev project) by the Cloud Functions API
# We are running pytest with "-n 20". Let's say each session lasts about a
# minute, so we are setting a limit of 120/20 = 6 deletions per session.
_MAX_NUM_FUNCTIONS_TO_DELETE_PER_SESSION = 6

# NOTE: Keep this import at the top level to test global var behavior with
# remote functions
_team_pi = "Team Pi"
_team_euler = "Team Euler"


def get_remote_function_endpoints(bigquery_client, dataset_id):
    """Get endpoints used by the remote functions in a datset"""
    endpoints = set()
    routines = bigquery_client.list_routines(dataset=dataset_id)
    for routine in routines:
        rf_options = routine._properties.get("remoteFunctionOptions")
        if not rf_options:
            continue
        rf_endpoint = rf_options.get("endpoint")
        if rf_endpoint:
            endpoints.add(rf_endpoint)
    return endpoints


def get_cloud_functions(
    functions_client, project, location, name=None, name_prefix=None
):
    """Get the cloud functions in the given project and location."""

    assert (
        not name or not name_prefix
    ), f"At most one of the {name.__name__} or {name_prefix.__name__} can be passed."

    _, location = get_remote_function_locations(location)
    parent = f"projects/{project}/locations/{location}"
    request = functions_v2.ListFunctionsRequest(parent=parent)
    page_result = functions_client.list_functions(request=request)
    for response in page_result:
        # If name is provided and it does not match then skip
        if bool(name):
            full_name = parent + f"/functions/{name}"
            if response.name != full_name:
                continue
        # If name prefix is provided and it does not match then skip
        elif bool(name_prefix):
            full_name_prefix = parent + f"/functions/{name_prefix}"
            if not response.name.startswith(full_name_prefix):
                continue

        yield response


def delete_cloud_function(functions_client, full_name):
    """Delete a cloud function with the given fully qualified name."""
    request = functions_v2.DeleteFunctionRequest(name=full_name)
    operation = functions_client.delete_function(request=request)
    return operation


def cleanup_remote_function_assets(
    bigquery_client, functions_client, remote_udf, ignore_failures=True
):
    """Clean up the GCP assets behind a bigframes remote function."""

    # Clean up BQ remote function
    try:
        bigquery_client.delete_routine(remote_udf.bigframes_remote_function)
    except Exception:
        # By default don't raise exception in cleanup
        if not ignore_failures:
            raise

    # Clean up cloud function
    try:
        delete_cloud_function(functions_client, remote_udf.bigframes_cloud_function)
    except Exception:
        # By default don't raise exception in cleanup
        if not ignore_failures:
            raise


def make_uniq_udf(udf):
    """Transform a udf to another with same behavior but a unique name.
    Use this to test remote functions with reuse=True, in which case parallel
    instances of the same tests may evaluate same named cloud functions and BQ
    remote functions, therefore interacting with each other and causing unwanted
    failures. With this method one can transform a udf into another with the
    same behavior but a different name which will remain unique for the
    lifetime of one test instance.
    """

    prefixer = test_utils.prefixer.Prefixer(udf.__name__, "")
    udf_uniq_name = prefixer.create_prefix()
    udf_file_name = f"{udf_uniq_name}.py"

    # We are not using `tempfile.TemporaryDirectory()` because we want to keep
    # the temp code around, otherwise `inspect.getsource()` complains.
    tmpdir = tempfile.mkdtemp()
    udf_file_path = os.path.join(tmpdir, udf_file_name)
    with open(udf_file_path, "w") as f:
        # TODO(shobs): Find a better way of modifying the udf, maybe regex?
        source_key = f"def {udf.__name__}"
        target_key = f"def {udf_uniq_name}"
        source_code = textwrap.dedent(inspect.getsource(udf))
        target_code = source_code.replace(source_key, target_key, 1)
        f.write(target_code)
    spec = importlib.util.spec_from_file_location(udf_file_name, udf_file_path)
    udf_uniq = getattr(spec.loader.load_module(), udf_uniq_name)

    # This is a bit of a hack but we need to remove the reference to a foreign
    # module, otherwise the serialization would keep the foreign module
    # reference and deserialization would fail with error like following:
    #     ModuleNotFoundError: No module named 'add_one_2nxcmd9j'
    # TODO(shobs): Figure out if there is a better way of generating the unique
    # function object, but for now let's just set it to same module as the
    # original udf.
    udf_uniq.__module__ = udf.__module__

    return udf_uniq, tmpdir


@pytest.fixture(scope="module")
def bq_cf_connection() -> str:
    """Pre-created BQ connection to invoke cloud function for bigframes-dev
    $ bq show --connection --location=us --project_id=bigframes-dev bigframes-rf-conn
    """
    return "bigframes-rf-conn"


@pytest.fixture(scope="module")
def functions_client() -> functions_v2.FunctionServiceClient:
    """Cloud Functions client"""
    return functions_v2.FunctionServiceClient()


@pytest.fixture(scope="module", autouse=True)
def cleanup_cloud_functions(session, functions_client, dataset_id_permanent):
    """Clean up stale cloud functions."""
    permanent_endpoints = get_remote_function_endpoints(
        session.bqclient, dataset_id_permanent
    )
    delete_count = 0
    for cloud_function in get_cloud_functions(
        functions_client,
        session.bqclient.project,
        session.bqclient.location,
        name_prefix="bigframes-",
    ):
        # Ignore bigframes cloud functions referred by the remote functions in
        # the permanent dataset
        if cloud_function.service_config.uri in permanent_endpoints:
            continue

        # Ignore the functions less than one day old
        age = datetime.now() - datetime.fromtimestamp(
            cloud_function.update_time.timestamp()
        )
        if age.days <= 0:
            continue

        # Go ahead and delete
        try:
            delete_cloud_function(functions_client, cloud_function.name)
            delete_count += 1
            if delete_count >= _MAX_NUM_FUNCTIONS_TO_DELETE_PER_SESSION:
                break
        except NotFound:
            # This can happen when multiple pytest sessions are running in
            # parallel. Two or more sessions may discover the same cloud
            # function, but only one of them would be able to delete it
            # successfully, while the other instance will run into this
            # exception. Ignore this exception.
            pass
        except ResourceExhausted:
            # This can happen if we are hitting GCP limits, e.g.
            # google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded
            # for quota metric 'Per project mutation requests' and limit
            # 'Per project mutation requests per minute per region' of service
            # 'cloudfunctions.googleapis.com' for consumer
            # 'project_number:1084210331973'.
            # [reason: "RATE_LIMIT_EXCEEDED" domain: "googleapis.com" ...
            # Let's stop further clean up and leave it to later.
            break


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_multiply_with_ibis(
    session,
    scalars_table_id,
    ibis_client,
    dataset_id,
    bq_cf_connection,
    functions_client,
):
    try:

        @session.remote_function(
            [int, int],
            int,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )
        def multiply(x, y):
            return x * y

        project_id, dataset_name, table_name = scalars_table_id.split(".")
        if not ibis_client.dataset:
            ibis_client.dataset = dataset_name

        col_name = "int64_col"
        table = ibis_client.tables[table_name]
        table = table.filter(table[col_name].notnull()).order_by("rowindex").head(10)
        pandas_df_orig = table.execute()

        col = table[col_name]
        col_2x = multiply(col, 2).name("int64_col_2x")
        col_square = multiply(col, col).name("int64_col_square")
        table = table.mutate([col_2x, col_square])
        pandas_df_new = table.execute()

        pandas.testing.assert_series_equal(
            pandas_df_orig[col_name] * 2,
            pandas_df_new["int64_col_2x"],
            check_names=False,
        )

        pandas.testing.assert_series_equal(
            pandas_df_orig[col_name] * pandas_df_orig[col_name],
            pandas_df_new["int64_col_square"],
            check_names=False,
        )
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(session.bqclient, functions_client, multiply)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_stringify_with_ibis(
    session,
    scalars_table_id,
    ibis_client,
    dataset_id,
    bq_cf_connection,
    functions_client,
):
    try:

        @session.remote_function(
            [int],
            str,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )
        def stringify(x):
            return f"I got {x}"

        project_id, dataset_name, table_name = scalars_table_id.split(".")
        if not ibis_client.dataset:
            ibis_client.dataset = dataset_name

        col_name = "int64_col"
        table = ibis_client.tables[table_name]
        table = table.filter(table[col_name].notnull()).order_by("rowindex").head(10)
        pandas_df_orig = table.execute()

        col = table[col_name]
        col_2x = stringify(col).name("int64_str_col")
        table = table.mutate([col_2x])
        pandas_df_new = table.execute()

        pandas.testing.assert_series_equal(
            pandas_df_orig[col_name].apply(lambda x: f"I got {x}"),
            pandas_df_new["int64_str_col"],
            check_names=False,
        )
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(session.bqclient, functions_client, stringify)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_decorator_with_bigframes_series(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:

        @session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )
        def square(x):
            return x * x

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_int64_col_filter = bf_int64_col.notnull()
        bf_int64_col_filtered = bf_int64_col[bf_int64_col_filter]
        bf_result_col = bf_int64_col_filtered.apply(square)
        bf_result = (
            bf_int64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_int64_col_filter = pd_int64_col.notnull()
        pd_int64_col_filtered = pd_int64_col[pd_int64_col_filter]
        pd_result_col = pd_int64_col_filtered.apply(lambda x: x * x)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, i.e.
        # pd_int64_col_filtered.dtype is Int64Dtype()
        # pd_int64_col_filtered.apply(lambda x: x * x).dtype is int64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
        pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(session.bqclient, functions_client, square)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_explicit_with_bigframes_series(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:

        def add_one(x):
            return x + 1

        remote_add_one = session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )(add_one)

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_int64_col_filter = bf_int64_col.notnull()
        bf_int64_col_filtered = bf_int64_col[bf_int64_col_filter]
        bf_result_col = bf_int64_col_filtered.apply(remote_add_one)
        bf_result = (
            bf_int64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_int64_col_filter = pd_int64_col.notnull()
        pd_int64_col_filtered = pd_int64_col[pd_int64_col_filter]
        pd_result_col = pd_int64_col_filtered.apply(add_one)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, e.g.
        # pd_int64_col_filtered.dtype is Int64Dtype()
        # pd_int64_col_filtered.apply(lambda x: x).dtype is int64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
        pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, remote_add_one
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_explicit_dataset_not_created(
    session, scalars_dfs, dataset_id_not_created, bq_cf_connection, functions_client
):
    try:

        @session.remote_function(
            [int],
            int,
            dataset_id_not_created,
            bq_cf_connection,
            reuse=False,
        )
        def square(x):
            return x * x

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_int64_col_filter = bf_int64_col.notnull()
        bf_int64_col_filtered = bf_int64_col[bf_int64_col_filter]
        bf_result_col = bf_int64_col_filtered.apply(square)
        bf_result = (
            bf_int64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_int64_col_filter = pd_int64_col.notnull()
        pd_int64_col_filtered = pd_int64_col[pd_int64_col_filter]
        pd_result_col = pd_int64_col_filtered.apply(lambda x: x * x)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, i.e.
        # pd_int64_col_filtered.dtype is Int64Dtype()
        # pd_int64_col_filtered.apply(lambda x: x * x).dtype is int64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
        pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(session.bqclient, functions_client, square)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_referring_outside_var(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:
        POSITIVE_SIGN = 1
        NEGATIVE_SIGN = -1
        NO_SIGN = 0

        def sign(num):
            if num > 0:
                return POSITIVE_SIGN
            elif num < 0:
                return NEGATIVE_SIGN
            return NO_SIGN

        remote_sign = session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )(sign)

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_int64_col_filter = bf_int64_col.notnull()
        bf_int64_col_filtered = bf_int64_col[bf_int64_col_filter]
        bf_result_col = bf_int64_col_filtered.apply(remote_sign)
        bf_result = (
            bf_int64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_int64_col_filter = pd_int64_col.notnull()
        pd_int64_col_filtered = pd_int64_col[pd_int64_col_filter]
        pd_result_col = pd_int64_col_filtered.apply(sign)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, e.g.
        # pd_int64_col_filtered.dtype is Int64Dtype()
        # pd_int64_col_filtered.apply(lambda x: x).dtype is int64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
        pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(session.bqclient, functions_client, remote_sign)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_referring_outside_import(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:
        import math as mymath

        def circumference(radius):
            return 2 * mymath.pi * radius

        remote_circumference = session.remote_function(
            [float],
            float,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )(circumference)

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_float64_col = scalars_df["float64_col"]
        bf_float64_col_filter = bf_float64_col.notnull()
        bf_float64_col_filtered = bf_float64_col[bf_float64_col_filter]
        bf_result_col = bf_float64_col_filtered.apply(remote_circumference)
        bf_result = (
            bf_float64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_float64_col = scalars_pandas_df["float64_col"]
        pd_float64_col_filter = pd_float64_col.notnull()
        pd_float64_col_filtered = pd_float64_col[pd_float64_col_filter]
        pd_result_col = pd_float64_col_filtered.apply(circumference)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, e.g.
        # pd_float64_col_filtered.dtype is Float64Dtype()
        # pd_float64_col_filtered.apply(lambda x: x).dtype is float64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Float64Dtype())
        pd_result = pd_float64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, remote_circumference
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_referring_global_var_and_import(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:

        def find_team(num):
            boundary = (math.pi + math.e) / 2
            if num >= boundary:
                return _team_euler
            return _team_pi

        remote_find_team = session.remote_function(
            [float],
            str,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )(find_team)

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_float64_col = scalars_df["float64_col"]
        bf_float64_col_filter = bf_float64_col.notnull()
        bf_float64_col_filtered = bf_float64_col[bf_float64_col_filter]
        bf_result_col = bf_float64_col_filtered.apply(remote_find_team)
        bf_result = (
            bf_float64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_float64_col = scalars_pandas_df["float64_col"]
        pd_float64_col_filter = pd_float64_col.notnull()
        pd_float64_col_filtered = pd_float64_col[pd_float64_col_filter]
        pd_result_col = pd_float64_col_filtered.apply(find_team)
        # TODO(shobs): Figure if the dtype mismatch is by design:
        # bf_result.dtype: string[pyarrow]
        # pd_result.dtype: dtype('O').
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.StringDtype(storage="pyarrow"))
        pd_result = pd_float64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, remote_find_team
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_restore_with_bigframes_series(
    session,
    scalars_dfs,
    dataset_id,
    bq_cf_connection,
    functions_client,
):
    try:

        def add_one(x):
            return x + 1

        # Make a unique udf
        add_one_uniq, add_one_uniq_dir = make_uniq_udf(add_one)

        # Expected cloud function name for the unique udf
        add_one_uniq_cf_name = get_cloud_function_name(add_one_uniq)

        # There should be no cloud function yet for the unique udf
        cloud_functions = list(
            get_cloud_functions(
                functions_client,
                session.bqclient.project,
                session.bqclient.location,
                name=add_one_uniq_cf_name,
            )
        )
        assert len(cloud_functions) == 0

        # The first time both the cloud function and the bq remote function don't
        # exist and would be created
        remote_add_one = session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            reuse=True,
        )(add_one_uniq)

        # There should have been excactly one cloud function created at this point
        cloud_functions = list(
            get_cloud_functions(
                functions_client,
                session.bqclient.project,
                session.bqclient.location,
                name=add_one_uniq_cf_name,
            )
        )
        assert len(cloud_functions) == 1

        # We will test this twice
        def inner_test():
            scalars_df, scalars_pandas_df = scalars_dfs

            bf_int64_col = scalars_df["int64_col"]
            bf_int64_col_filter = bf_int64_col.notnull()
            bf_int64_col_filtered = bf_int64_col[bf_int64_col_filter]
            bf_result_col = bf_int64_col_filtered.apply(remote_add_one)
            bf_result = (
                bf_int64_col_filtered.to_frame()
                .assign(result=bf_result_col)
                .to_pandas()
            )

            pd_int64_col = scalars_pandas_df["int64_col"]
            pd_int64_col_filter = pd_int64_col.notnull()
            pd_int64_col_filtered = pd_int64_col[pd_int64_col_filter]
            pd_result_col = pd_int64_col_filtered.apply(add_one_uniq)
            # TODO(shobs): Figure why pandas .apply() changes the dtype, i.e.
            # pd_int64_col_filtered.dtype is Int64Dtype()
            # pd_int64_col_filtered.apply(lambda x: x * x).dtype is int64.
            # For this test let's force the pandas dtype to be same as bigframes' dtype.
            pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
            pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

            assert_pandas_df_equal(bf_result, pd_result)

        # Test that the remote function works as expected
        inner_test()

        # Let's delete the cloud function while not touching the bq remote function
        delete_operation = delete_cloud_function(
            functions_client, cloud_functions[0].name
        )
        delete_operation.result()
        assert delete_operation.done()

        # There should be no cloud functions at this point for the uniq udf
        cloud_functions = list(
            get_cloud_functions(
                functions_client,
                session.bqclient.project,
                session.bqclient.location,
                name=add_one_uniq_cf_name,
            )
        )
        assert len(cloud_functions) == 0

        # The second time bigframes detects that the required cloud function doesn't
        # exist even though the remote function exists, and goes ahead and recreates
        # the cloud function
        remote_add_one = session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            reuse=True,
        )(add_one_uniq)

        # There should be excactly one cloud function again
        cloud_functions = list(
            get_cloud_functions(
                functions_client,
                session.bqclient.project,
                session.bqclient.location,
                name=add_one_uniq_cf_name,
            )
        )
        assert len(cloud_functions) == 1

        # Test again after the cloud function is restored that the remote function
        # works as expected
        inner_test()

        # clean up the temp code
        shutil.rmtree(add_one_uniq_dir)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, remote_add_one
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_mask_default_value(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:

        def is_odd(num):
            flag = False
            try:
                flag = num % 2 == 1
            except TypeError:
                pass
            return flag

        is_odd_remote = session.remote_function(
            [int],
            bool,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )(is_odd)

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_result_col = bf_int64_col.mask(is_odd_remote)
        bf_result = bf_int64_col.to_frame().assign(result=bf_result_col).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_result_col = pd_int64_col.mask(is_odd)
        pd_result = pd_int64_col.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, is_odd_remote
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_mask_custom_value(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:

        def is_odd(num):
            flag = False
            try:
                flag = num % 2 == 1
            except TypeError:
                pass
            return flag

        is_odd_remote = session.remote_function(
            [int],
            bool,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )(is_odd)

        scalars_df, scalars_pandas_df = scalars_dfs

        # TODO(shobs): Revisit this test when NA handling of pandas' Series.mask is
        # fixed https://github.com/pandas-dev/pandas/issues/52955,
        # for now filter out the nulls and test the rest
        bf_int64_col = scalars_df["int64_col"]
        bf_result_col = bf_int64_col[bf_int64_col.notnull()].mask(is_odd_remote, -1)
        bf_result = bf_int64_col.to_frame().assign(result=bf_result_col).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_result_col = pd_int64_col[pd_int64_col.notnull()].mask(is_odd, -1)
        pd_result = pd_int64_col.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, is_odd_remote
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_lambda(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:
        add_one_lambda = lambda x: x + 1  # noqa: E731

        add_one_lambda_remote = session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            reuse=False,
        )(add_one_lambda)

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_int64_col_filter = bf_int64_col.notnull()
        bf_int64_col_filtered = bf_int64_col[bf_int64_col_filter]
        bf_result_col = bf_int64_col_filtered.apply(add_one_lambda_remote)
        bf_result = (
            bf_int64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_int64_col_filter = pd_int64_col.notnull()
        pd_int64_col_filtered = pd_int64_col[pd_int64_col_filter]
        pd_result_col = pd_int64_col_filtered.apply(add_one_lambda)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, i.e.
        # pd_int64_col_filtered.dtype is Int64Dtype()
        # pd_int64_col_filtered.apply(lambda x: x).dtype is int64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
        pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, add_one_lambda_remote
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_with_explicit_name(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:

        def square(x):
            return x * x

        prefixer = test_utils.prefixer.Prefixer(square.__name__, "")
        rf_name = prefixer.create_prefix()
        expected_remote_function = f"{dataset_id}.{rf_name}"

        # Initially the expected BQ remote function should not exist
        with pytest.raises(NotFound):
            session.bqclient.get_routine(expected_remote_function)

        # Create the remote function with the name provided explicitly
        square_remote = session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            reuse=False,
            name=rf_name,
        )(square)

        # The remote function should reflect the explicitly provided name
        assert square_remote.bigframes_remote_function == expected_remote_function

        # Now the expected BQ remote function should exist
        session.bqclient.get_routine(expected_remote_function)

        # The behavior of the created remote function should be as expected
        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_too"]
        bf_result_col = bf_int64_col.apply(square_remote)
        bf_result = bf_int64_col.to_frame().assign(result=bf_result_col).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_too"]
        pd_result_col = pd_int64_col.apply(square)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, i.e.
        # pd_int64_col.dtype is Int64Dtype()
        # pd_int64_col.apply(square).dtype is int64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
        pd_result = pd_int64_col.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, square_remote
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_with_external_package_dependencies(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:

        def pd_np_foo(x):
            import numpy as mynp
            import pandas as mypd

            return mypd.Series([x, mynp.sqrt(mynp.abs(x))]).sum()

        # Create the remote function with the name provided explicitly
        pd_np_foo_remote = session.remote_function(
            [int],
            float,
            dataset_id,
            bq_cf_connection,
            reuse=False,
            packages=["numpy", "pandas >= 2.0.0"],
        )(pd_np_foo)

        # The behavior of the created remote function should be as expected
        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_too"]
        bf_result_col = bf_int64_col.apply(pd_np_foo_remote)
        bf_result = bf_int64_col.to_frame().assign(result=bf_result_col).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_too"]
        pd_result_col = pd_int64_col.apply(pd_np_foo)
        pd_result = pd_int64_col.to_frame().assign(result=pd_result_col)

        # pandas result is non-nullable type float64, make it Float64 before
        # comparing for the purpose of this test
        pd_result.result = pd_result.result.astype(pandas.Float64Dtype())

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, pd_np_foo_remote
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_with_explicit_name_reuse(
    session, scalars_dfs, dataset_id, bq_cf_connection, functions_client
):
    try:

        dirs_to_cleanup = []

        # Define a user code
        def square(x):
            return x * x

        # Make it a unique udf
        square_uniq, square_uniq_dir = make_uniq_udf(square)
        dirs_to_cleanup.append(square_uniq_dir)

        # Define a common routine which accepts a remote function and the
        # corresponding user defined function and tests that bigframes bahavior
        # on the former is in parity with the pandas behaviour on the latter
        def test_internal(rf, udf):
            # The behavior of the created remote function should be as expected
            scalars_df, scalars_pandas_df = scalars_dfs

            bf_int64_col = scalars_df["int64_too"]
            bf_result_col = bf_int64_col.apply(rf)
            bf_result = bf_int64_col.to_frame().assign(result=bf_result_col).to_pandas()

            pd_int64_col = scalars_pandas_df["int64_too"]
            pd_result_col = pd_int64_col.apply(udf)
            # TODO(shobs): Figure why pandas .apply() changes the dtype, i.e.
            # pd_int64_col.dtype is Int64Dtype()
            # pd_int64_col.apply(square).dtype is int64.
            # For this test let's force the pandas dtype to be same as bigframes' dtype.
            pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
            pd_result = pd_int64_col.to_frame().assign(result=pd_result_col)

            assert_pandas_df_equal(bf_result, pd_result)

        # Create an explicit name for the remote function
        prefixer = test_utils.prefixer.Prefixer("foo", "")
        rf_name = prefixer.create_prefix()
        expected_remote_function = f"{dataset_id}.{rf_name}"

        # Initially the expected BQ remote function should not exist
        with pytest.raises(NotFound):
            session.bqclient.get_routine(expected_remote_function)

        # Create a new remote function with the name provided explicitly
        square_remote1 = session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            name=rf_name,
        )(square_uniq)

        # The remote function should reflect the explicitly provided name
        assert square_remote1.bigframes_remote_function == expected_remote_function

        # Now the expected BQ remote function should exist
        routine = session.bqclient.get_routine(expected_remote_function)
        square_remote1_created = routine.created
        square_remote1_cf_updated = session.cloudfunctionsclient.get_function(
            name=square_remote1.bigframes_cloud_function
        ).update_time

        # Test pandas parity with square udf
        test_internal(square_remote1, square)

        # Now Create another remote function with the same name provided
        # explicitly. Since reuse is True by default, the previously created
        # remote function with the same name will be reused.
        square_remote2 = session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            name=rf_name,
        )(square_uniq)

        # The new remote function should still reflect the explicitly provided name
        assert square_remote2.bigframes_remote_function == expected_remote_function

        # The expected BQ remote function should still exist
        routine = session.bqclient.get_routine(expected_remote_function)
        square_remote2_created = routine.created
        square_remote2_cf_updated = session.cloudfunctionsclient.get_function(
            name=square_remote2.bigframes_cloud_function
        ).update_time

        # The new remote function should reflect that the previous BQ remote
        # function and the cloud function were reused instead of creating anew
        assert square_remote2_created == square_remote1_created
        assert (
            square_remote2.bigframes_cloud_function
            == square_remote1.bigframes_cloud_function
        )
        assert square_remote2_cf_updated == square_remote1_cf_updated

        # Test again that the new remote function is actually same as the
        # previous remote function
        test_internal(square_remote2, square)

        # Now define a different user code
        def plusone(x):
            return x + 1

        # Make it a unique udf
        plusone_uniq, plusone_uniq_dir = make_uniq_udf(plusone)
        dirs_to_cleanup.append(plusone_uniq_dir)

        # Now Create a third remote function with the same name provided
        # explicitly. Even though reuse is True by default, the previously
        # created remote function with the same name should not be reused since
        # this time it is a different user code.
        plusone_remote = session.remote_function(
            [int],
            int,
            dataset_id,
            bq_cf_connection,
            name=rf_name,
        )(plusone_uniq)

        # The new remote function should still reflect the explicitly provided name
        assert plusone_remote.bigframes_remote_function == expected_remote_function

        # The expected BQ remote function should still exist
        routine = session.bqclient.get_routine(expected_remote_function)
        plusone_remote_created = routine.created
        plusone_remote_cf_updated = session.cloudfunctionsclient.get_function(
            name=plusone_remote.bigframes_cloud_function
        ).update_time

        # The new remote function should reflect that the previous BQ remote
        # function and the cloud function were NOT reused, instead were created
        # anew
        assert plusone_remote_created > square_remote2_created
        assert (
            plusone_remote.bigframes_cloud_function
            != square_remote2.bigframes_cloud_function
        )
        assert plusone_remote_cf_updated > square_remote2_cf_updated

        # Test again that the new remote function is equivalent to the new user
        # defined function
        test_internal(plusone_remote, plusone)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, functions_client, square_remote1
        )
        cleanup_remote_function_assets(
            session.bqclient, functions_client, square_remote2
        )
        cleanup_remote_function_assets(
            session.bqclient, functions_client, plusone_remote
        )
        for dir_ in dirs_to_cleanup:
            shutil.rmtree(dir_)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_via_session_context_connection_setter(
    scalars_dfs, dataset_id, bq_cf_connection
):
    # Creating a session scoped only to this test as we would be setting a
    # property in it
    context = bigframes.BigQueryOptions()
    context.bq_connection = bq_cf_connection
    session = bigframes.connect(context)

    try:
        # Without an explicit bigquery connection, the one present in Session,
        # set via context setter would be used. Without an explicit `reuse` the
        # default behavior of reuse=True will take effect. Please note that the
        # udf is same as the one used in other tests in this file so the underlying
        # cloud function would be common with reuse=True. Since we are using a
        # unique dataset_id, even though the cloud function would be reused, the bq
        # remote function would still be created, making use of the bq connection
        # set in the BigQueryOptions above.
        @session.remote_function([int], int, dataset=dataset_id)
        def square(x):
            return x * x

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_int64_col_filter = bf_int64_col.notnull()
        bf_int64_col_filtered = bf_int64_col[bf_int64_col_filter]
        bf_result_col = bf_int64_col_filtered.apply(square)
        bf_result = (
            bf_int64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_int64_col_filter = pd_int64_col.notnull()
        pd_int64_col_filtered = pd_int64_col[pd_int64_col_filter]
        pd_result_col = pd_int64_col_filtered.apply(lambda x: x * x)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, i.e.
        # pd_int64_col_filtered.dtype is Int64Dtype()
        # pd_int64_col_filtered.apply(lambda x: x * x).dtype is int64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
        pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, session.cloudfunctionsclient, square
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_default_connection(session, scalars_dfs, dataset_id):
    try:

        @session.remote_function([int], int, dataset=dataset_id)
        def square(x):
            return x * x

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_int64_col_filter = bf_int64_col.notnull()
        bf_int64_col_filtered = bf_int64_col[bf_int64_col_filter]
        bf_result_col = bf_int64_col_filtered.apply(square)
        bf_result = (
            bf_int64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_int64_col_filter = pd_int64_col.notnull()
        pd_int64_col_filtered = pd_int64_col[pd_int64_col_filter]
        pd_result_col = pd_int64_col_filtered.apply(lambda x: x * x)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, i.e.
        # pd_int64_col_filtered.dtype is Int64Dtype()
        # pd_int64_col_filtered.apply(lambda x: x * x).dtype is int64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
        pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, session.cloudfunctionsclient, square
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_anonymous_dataset(session, scalars_dfs):
    try:
        # This usage of remote_function is expected to create the remote
        # function in the bigframes session's anonymous dataset. Use reuse=False
        # param to make sure parallel instances of the test don't step over each
        # other due to the common anonymous dataset.
        @session.remote_function([int], int, reuse=False)
        def square(x):
            return x * x

        assert (
            bigquery.Routine(square.bigframes_remote_function).dataset_id
            == session._anonymous_dataset.dataset_id
        )

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_int64_col_filter = bf_int64_col.notnull()
        bf_int64_col_filtered = bf_int64_col[bf_int64_col_filter]
        bf_result_col = bf_int64_col_filtered.apply(square)
        bf_result = (
            bf_int64_col_filtered.to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_int64_col_filter = pd_int64_col.notnull()
        pd_int64_col_filtered = pd_int64_col[pd_int64_col_filter]
        pd_result_col = pd_int64_col_filtered.apply(lambda x: x * x)
        # TODO(shobs): Figure why pandas .apply() changes the dtype, i.e.
        # pd_int64_col_filtered.dtype is Int64Dtype()
        # pd_int64_col_filtered.apply(lambda x: x * x).dtype is int64.
        # For this test let's force the pandas dtype to be same as bigframes' dtype.
        pd_result_col = pd_result_col.astype(pandas.Int64Dtype())
        pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_remote_function_assets(
            session.bqclient, session.cloudfunctionsclient, square
        )
