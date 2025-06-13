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
import warnings

import google.api_core.exceptions
from google.cloud import bigquery, functions_v2, storage
import pandas
import pytest
import test_utils.prefixer

import bigframes
import bigframes.dataframe
import bigframes.dtypes
import bigframes.exceptions
import bigframes.functions._utils as bff_utils
import bigframes.pandas as bpd
import bigframes.series
from bigframes.testing.utils import (
    assert_pandas_df_equal,
    cleanup_function_assets,
    delete_cloud_function,
    get_cloud_functions,
)

# NOTE: Keep this import at the top level to test global var behavior with
# remote functions
_team_pi = "Team Pi"
_team_euler = "Team Euler"


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

    assert (spec is not None) and (spec.loader is not None)
    module = importlib.util.module_from_spec(spec)

    # exec_module fills the module object with all the functions, classes, and
    # variables defined in the module file.
    spec.loader.exec_module(module)
    udf_uniq = getattr(module, udf_uniq_name)

    return udf_uniq, tmpdir


@pytest.fixture(scope="module")
def bq_cf_connection() -> str:
    """Pre-created BQ connection in the test project in US location, used to
    invoke cloud function.

    $ bq show --connection --location=us --project_id=PROJECT_ID bigframes-rf-conn
    """
    return "bigframes-rf-conn"


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_binop(session, scalars_dfs, dataset_id, bq_cf_connection):
    try:

        def func(x, y):
            return x * abs(y % 4)

        remote_func = session.remote_function(
            # Make sure that the input/output types can be used positionally.
            # This avoids the worst of the breaking change from 1.x to 2.x.
            [str, int],
            str,
            dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
        )(func)

        scalars_df, scalars_pandas_df = scalars_dfs

        scalars_df = scalars_df.dropna()
        scalars_pandas_df = scalars_pandas_df.dropna()
        bf_result = (
            scalars_df["string_col"]
            .combine(scalars_df["int64_col"], remote_func)
            .to_pandas()
        )
        pd_result = scalars_pandas_df["string_col"].combine(
            scalars_pandas_df["int64_col"], func
        )
        pandas.testing.assert_series_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            remote_func, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_binop_array_output(
    session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:

        def func(x, y):
            return [len(x), abs(y % 4)]

        remote_func = session.remote_function(
            # Make sure that the input/output types can be used positionally.
            # This avoids the worst of the breaking change from 1.x to 2.x.
            [str, int],
            list[int],
            dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
        )(func)

        scalars_df, scalars_pandas_df = scalars_dfs

        scalars_df = scalars_df.dropna()
        scalars_pandas_df = scalars_pandas_df.dropna()
        bf_result = (
            scalars_df["string_col"]
            .combine(scalars_df["int64_col"], remote_func)
            .to_pandas()
        )
        pd_result = scalars_pandas_df["string_col"].combine(
            scalars_pandas_df["int64_col"], func
        )
        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            remote_func, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_decorator_with_bigframes_series(
    session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:

        @session.remote_function(
            # Make sure that the input/output types can be used positionally.
            # This avoids the worst of the breaking change from 1.x to 2.x.
            [int],
            int,
            dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(square, session.bqclient, session.cloudfunctionsclient)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_explicit_with_bigframes_series(
    session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:

        def add_one(x):
            return x + 1

        remote_add_one = session.remote_function(
            # Make sure that the input/output types can be used positionally.
            # This avoids the worst of the breaking change from 1.x to 2.x.
            [int],
            int,
            dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(
            remote_add_one, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    ("input_types"),
    [
        pytest.param([int], id="list-of-int"),
        pytest.param(int, id="int"),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_input_types(session, scalars_dfs, input_types):
    try:

        def add_one(x):
            return x + 1

        remote_add_one = session.remote_function(
            # Make sure that the input/output types can be used positionally.
            # This avoids the worst of the breaking change from 1.x to 2.x.
            input_types,
            int,
            reuse=False,
            cloud_function_service_account="default",
        )(add_one)
        assert remote_add_one.input_dtypes == (bigframes.dtypes.INT_DTYPE,)

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result = scalars_df.int64_too.map(remote_add_one).to_pandas()
        pd_result = scalars_pandas_df.int64_too.map(add_one)

        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            remote_add_one, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_explicit_dataset_not_created(
    session,
    scalars_dfs,
    dataset_id_not_created,
    bq_cf_connection,
):
    try:

        @session.remote_function(
            # Make sure that the input/output types can be used positionally.
            # This avoids the worst of the breaking change from 1.x to 2.x.
            [int],
            int,
            dataset=dataset_id_not_created,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(square, session.bqclient, session.cloudfunctionsclient)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_referring_outside_var(
    session, scalars_dfs, dataset_id, bq_cf_connection
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
            # Make sure that the input/output types can be used positionally.
            # This avoids the worst of the breaking change from 1.x to 2.x.
            [int],
            int,
            dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(
            remote_sign, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_referring_outside_import(
    session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:
        import math as mymath

        def circumference(radius):
            return 2 * mymath.pi * radius

        remote_circumference = session.remote_function(
            # Make sure that the input/output types can be used positionally.
            # This avoids the worst of the breaking change from 1.x to 2.x.
            [float],
            float,
            dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(
            remote_circumference, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_referring_global_var_and_import(
    session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:

        def find_team(num):
            boundary = (math.pi + math.e) / 2
            if num >= boundary:
                return _team_euler
            return _team_pi

        remote_find_team = session.remote_function(
            input_types=[float],
            output_type=str,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(
            remote_find_team, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_restore_with_bigframes_series(
    session,
    scalars_dfs,
    dataset_id,
    bq_cf_connection,
):
    try:

        def add_one(x):
            return x + 1

        # Make a unique udf
        add_one_uniq, add_one_uniq_dir = make_uniq_udf(add_one)

        # Expected cloud function name for the unique udf
        package_requirements = bff_utils._get_updated_package_requirements()
        add_one_uniq_hash = bff_utils._get_hash(add_one_uniq, package_requirements)
        add_one_uniq_cf_name = bff_utils.get_cloud_function_name(
            add_one_uniq_hash, session.session_id
        )

        # There should be no cloud function yet for the unique udf
        cloud_functions = list(
            get_cloud_functions(
                session.cloudfunctionsclient,
                session.bqclient.project,
                session.bqclient.location,
                name=add_one_uniq_cf_name,
            )
        )
        assert len(cloud_functions) == 0

        # The first time both the cloud function and the bq remote function don't
        # exist and would be created
        remote_add_one = session.remote_function(
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=True,
            cloud_function_service_account="default",
        )(add_one_uniq)

        # There should have been excactly one cloud function created at this point
        cloud_functions = list(
            get_cloud_functions(
                session.cloudfunctionsclient,
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
            session.cloudfunctionsclient, cloud_functions[0].name
        )
        delete_operation.result()
        assert delete_operation.done()

        # There should be no cloud functions at this point for the uniq udf
        cloud_functions = list(
            get_cloud_functions(
                session.cloudfunctionsclient,
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
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=True,
            cloud_function_service_account="default",
        )(add_one_uniq)

        # There should be excactly one cloud function again
        cloud_functions = list(
            get_cloud_functions(
                session.cloudfunctionsclient,
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
        cleanup_function_assets(
            remote_add_one, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_mask_default_value(
    session, scalars_dfs, dataset_id, bq_cf_connection
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
            input_types=[int],
            output_type=bool,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(
            is_odd_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_mask_custom_value(
    session, scalars_dfs, dataset_id, bq_cf_connection
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
            input_types=[int],
            output_type=bool,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(
            is_odd_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_udf_lambda(session, scalars_dfs, dataset_id, bq_cf_connection):
    try:
        add_one_lambda = lambda x: x + 1  # noqa: E731

        add_one_lambda_remote = session.remote_function(
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(
            add_one_lambda_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_with_explicit_name(
    session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:

        def square(x):
            return x * x

        prefixer = test_utils.prefixer.Prefixer(square.__name__, "")
        rf_name = prefixer.create_prefix()
        expected_remote_function = f"{dataset_id}.{rf_name}"

        # Initially the expected BQ remote function should not exist
        with pytest.raises(google.api_core.exceptions.NotFound):
            session.bqclient.get_routine(expected_remote_function)

        # Create the remote function with the name provided explicitly
        square_remote = session.remote_function(
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            name=rf_name,
            cloud_function_service_account="default",
        )(square)

        # The remote function should reflect the explicitly provided name
        assert square_remote.bigframes_remote_function == expected_remote_function
        assert square_remote.bigframes_bigquery_function == expected_remote_function

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
        cleanup_function_assets(
            square_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_with_external_package_dependencies(
    session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:

        def pd_np_foo(x):
            import numpy as mynp
            import pandas as mypd

            return mypd.Series([x, mynp.sqrt(mynp.abs(x))]).sum()

        # Create the remote function with the name provided explicitly
        pd_np_foo_remote = session.remote_function(
            input_types=[int],
            output_type=float,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            packages=["numpy", "pandas >= 2.0.0"],
            cloud_function_service_account="default",
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
        cleanup_function_assets(
            pd_np_foo_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_with_explicit_name_reuse(
    session, scalars_dfs, dataset_id, bq_cf_connection
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
        with pytest.raises(google.api_core.exceptions.NotFound):
            session.bqclient.get_routine(expected_remote_function)

        # Create a new remote function with the name provided explicitly
        square_remote1 = session.remote_function(
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            name=rf_name,
            cloud_function_service_account="default",
        )(square_uniq)

        # The remote function should reflect the explicitly provided name
        assert square_remote1.bigframes_remote_function == expected_remote_function
        assert square_remote1.bigframes_bigquery_function == expected_remote_function

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
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            name=rf_name,
            cloud_function_service_account="default",
        )(square_uniq)

        # The new remote function should still reflect the explicitly provided name
        assert square_remote2.bigframes_remote_function == expected_remote_function
        assert square_remote2.bigframes_bigquery_function == expected_remote_function

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
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            name=rf_name,
            cloud_function_service_account="default",
        )(plusone_uniq)

        # The new remote function should still reflect the explicitly provided name
        assert plusone_remote.bigframes_remote_function == expected_remote_function
        assert plusone_remote.bigframes_bigquery_function == expected_remote_function

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
        cleanup_function_assets(
            square_remote1, session.bqclient, session.cloudfunctionsclient
        )
        cleanup_function_assets(
            square_remote2, session.bqclient, session.cloudfunctionsclient
        )
        cleanup_function_assets(
            plusone_remote, session.bqclient, session.cloudfunctionsclient
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
        @session.remote_function(
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(square, session.bqclient, session.cloudfunctionsclient)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_default_connection(session, scalars_dfs, dataset_id):
    try:

        @session.remote_function(
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            reuse=False,
            cloud_function_service_account="default",
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
        cleanup_function_assets(square, session.bqclient, session.cloudfunctionsclient)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_runtime_error(session, scalars_dfs, dataset_id):
    try:

        @session.remote_function(
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            reuse=False,
            cloud_function_service_account="default",
        )
        def square(x):
            return x * x

        scalars_df, _ = scalars_dfs

        with pytest.raises(
            google.api_core.exceptions.BadRequest,
            match="400.*errorMessage.*unsupported operand type",
        ):
            # int64_col has nulls which should cause error in square
            scalars_df["int64_col"].apply(square).to_pandas()
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(square, session.bqclient, session.cloudfunctionsclient)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_anonymous_dataset(session, scalars_dfs):
    try:
        # This usage of remote_function is expected to create the remote
        # function in the bigframes session's anonymous dataset. Use reuse=False
        # param to make sure parallel instances of the test don't step over each
        # other due to the common anonymous dataset.
        @session.remote_function(
            input_types=[int],
            output_type=int,
            reuse=False,
            cloud_function_service_account="default",
        )
        def square(x):
            return x * x

        assert (
            bigquery.Routine(square.bigframes_bigquery_function).dataset_id
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
        cleanup_function_assets(square, session.bqclient, session.cloudfunctionsclient)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_via_session_custom_sa(scalars_dfs):
    # TODO(shobs): Automate the following set-up during testing in the test project.
    #
    # For upfront convenience, the following set up has been statically created
    # in the project bigfrmames-dev-perf via cloud console:
    #
    # 1. Create a service account bigframes-dev-perf-1@bigframes-dev-perf.iam.gserviceaccount.com as per
    #    https://cloud.google.com/iam/docs/service-accounts-create#iam-service-accounts-create-console
    # 2. Give necessary roles as per
    #    https://cloud.google.com/functions/docs/reference/iam/roles#additional-configuration
    #
    project = "bigframes-dev-perf"
    gcf_service_account = (
        "bigframes-dev-perf-1@bigframes-dev-perf.iam.gserviceaccount.com"
    )

    rf_session = bigframes.Session(context=bigframes.BigQueryOptions(project=project))

    try:

        # TODO(shobs): Figure out why the default ingress setting
        # (internal-only) does not work here
        @rf_session.remote_function(
            input_types=[int],
            output_type=int,
            reuse=False,
            cloud_function_service_account=gcf_service_account,
            cloud_function_ingress_settings="all",
        )
        def square_num(x):
            if x is None:
                return x
            return x * x

        # assert that the GCF is created with the intended SA
        gcf = rf_session.cloudfunctionsclient.get_function(
            name=square_num.bigframes_cloud_function
        )
        assert gcf.service_config.service_account_email == gcf_service_account

        # assert that the function works as expected on data
        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_result_col = bf_int64_col.apply(square_num)
        bf_result = bf_int64_col.to_frame().assign(result=bf_result_col).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_result_col = pd_int64_col.apply(lambda x: x if x is None else x * x)
        pd_result = pd_int64_col.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            square_num, rf_session.bqclient, rf_session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    ("set_build_service_account"),
    [
        pytest.param(
            "projects/bigframes-dev-perf/serviceAccounts/bigframes-dev-perf-1@bigframes-dev-perf.iam.gserviceaccount.com",
            id="fully-qualified-sa",
        ),
        pytest.param(
            "bigframes-dev-perf-1@bigframes-dev-perf.iam.gserviceaccount.com",
            id="just-sa-email",
        ),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_via_session_custom_build_sa(
    scalars_dfs, set_build_service_account
):
    # TODO(shobs): Automate the following set-up during testing in the test project.
    #
    # For upfront convenience, the following set up has been statically created
    # in the project bigfrmames-dev-perf via cloud console:
    #
    # 1. Create a service account bigframes-dev-perf-1@bigframes-dev-perf.iam.gserviceaccount.com as per
    #    https://cloud.google.com/iam/docs/service-accounts-create#iam-service-accounts-create-console
    # 2. Give "Cloud Build Service Account (roles/cloudbuild.builds.builder)" role as per
    #    https://cloud.google.com/build/docs/cloud-build-service-account#default_permissions_of_the_legacy_service_account
    #
    project = "bigframes-dev-perf"
    expected_build_service_account = "projects/bigframes-dev-perf/serviceAccounts/bigframes-dev-perf-1@bigframes-dev-perf.iam.gserviceaccount.com"

    rf_session = bigframes.Session(context=bigframes.BigQueryOptions(project=project))

    try:

        # TODO(shobs): Figure out why the default ingress setting
        # (internal-only) does not work here
        @rf_session.remote_function(
            input_types=[int],
            output_type=int,
            reuse=False,
            cloud_function_service_account="default",
            cloud_build_service_account=set_build_service_account,
            cloud_function_ingress_settings="all",
        )
        def square_num(x):
            if x is None:
                return x
            return x * x

        # assert that the GCF is created with the intended SA
        gcf = rf_session.cloudfunctionsclient.get_function(
            name=square_num.bigframes_cloud_function
        )
        assert gcf.build_config.service_account == expected_build_service_account

        # assert that the function works as expected on data
        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_result_col = bf_int64_col.apply(square_num)
        bf_result = bf_int64_col.to_frame().assign(result=bf_result_col).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_result_col = pd_int64_col.apply(lambda x: x if x is None else x * x)
        pd_result = pd_int64_col.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            square_num, rf_session.bqclient, rf_session.cloudfunctionsclient
        )


def test_remote_function_throws_none_cloud_function_service_account(session):
    with pytest.raises(
        ValueError,
        match='^You must provide a user managed cloud_function_service_account, or "default" if you would like to let the default service account be used.$',
    ):
        session.remote_function(cloud_function_service_account=None)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_with_gcf_cmek():
    # TODO(shobs): Automate the following set-up during testing in the test project.
    #
    # For upfront convenience, the following set up has been statically created
    # in the project bigfrmames-dev-perf via cloud console:
    #
    # 1. Created an encryption key and granting the necessary service accounts
    #    the required IAM permissions as per https://cloud.google.com/kms/docs/create-key
    # 2. Created a docker repository with CMEK (created in step 1) enabled as per
    #    https://cloud.google.com/artifact-registry/docs/repositories/create-repos#overview
    #
    project = "bigframes-dev-perf"
    cmek = "projects/bigframes-dev-perf/locations/us-central1/keyRings/bigframesKeyRing/cryptoKeys/bigframesKey"
    docker_repository = (
        "projects/bigframes-dev-perf/locations/us-central1/repositories/rf-artifacts"
    )

    session = bigframes.Session(context=bigframes.BigQueryOptions(project=project))
    try:

        @session.remote_function(
            input_types=[int],
            output_type=int,
            reuse=False,
            cloud_function_service_account="default",
            cloud_function_kms_key_name=cmek,
            cloud_function_docker_repository=docker_repository,
        )
        def square_num(x):
            if x is None:
                return x
            return x * x

        df = pandas.DataFrame({"num": [-1, 0, None, 1]}, dtype="Int64")
        bf = session.read_pandas(df)

        bf_result_col = bf["num"].apply(square_num)
        bf_result = bf.assign(result=bf_result_col).to_pandas()

        pd_result_col = df["num"].apply(lambda x: x if x is None else x * x)
        pd_result = df.assign(result=pd_result_col)

        assert_pandas_df_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )

        # Assert that the GCF is created with the intended SA
        gcf = session.cloudfunctionsclient.get_function(
            name=square_num.bigframes_cloud_function
        )
        assert gcf.kms_key_name == cmek

        # Assert that GCS artifact has CMEK applied
        storage_client = storage.Client()
        bucket = storage_client.bucket(gcf.build_config.source.storage_source.bucket)
        blob = bucket.get_blob(gcf.build_config.source.storage_source.object_)
        assert blob.kms_key_name.startswith(cmek)

    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            square_num, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_via_session_vpc(scalars_dfs):
    # TODO(shobs): Automate the following set-up during testing in the test project.
    #
    # For upfront convenience, the following set up has been statically created
    # in the project bigfrmames-dev-perf via cloud console:
    #
    # 1. Create a vpc connector as per
    #    https://cloud.google.com/vpc/docs/configure-serverless-vpc-access#gcloud
    #
    #    $ gcloud compute networks vpc-access connectors create bigframes-vpc --project=bigframes-dev-perf --region=us-central1 --range 10.8.0.0/28
    #    Create request issued for: [bigframes-vpc]
    #    Waiting for operation [projects/bigframes-dev-perf/locations/us-central1/operations/f9f90df6-7cf4-4420-8c2f-b3952775dcfb] to complete...done.
    #    Created connector [bigframes-vpc].
    #
    #    $ gcloud compute networks vpc-access connectors list --project=bigframes-dev-perf --region=us-central1
    #    CONNECTOR_ID   REGION       NETWORK  IP_CIDR_RANGE  SUBNET  SUBNET_PROJECT  MACHINE_TYPE  MIN_INSTANCES  MAX_INSTANCES  MIN_THROUGHPUT  MAX_THROUGHPUT  STATE
    #    bigframes-vpc  us-central1  default  10.8.0.0/28                            e2-micro      2              10             200             1000            READY

    project = "bigframes-dev-perf"
    gcf_vpc_connector = "bigframes-vpc"

    rf_session = bigframes.Session(context=bigframes.BigQueryOptions(project=project))

    try:

        def square_num(x):
            if x is None:
                return x
            return x * x

        # TODO(shobs): See if the test vpc can be configured to make this flow
        # work with the default ingress setting (internal-only)
        square_num_remote = rf_session.remote_function(
            input_types=[int],
            output_type=int,
            reuse=False,
            cloud_function_service_account="default",
            cloud_function_vpc_connector=gcf_vpc_connector,
            cloud_function_ingress_settings="all",
        )(square_num)

        # assert that the GCF is created with the intended vpc connector
        gcf = rf_session.cloudfunctionsclient.get_function(
            name=square_num_remote.bigframes_cloud_function
        )
        assert gcf.service_config.vpc_connector == gcf_vpc_connector

        # assert that the function works as expected on data
        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_col"]
        bf_result_col = bf_int64_col.apply(square_num_remote)
        bf_result = bf_int64_col.to_frame().assign(result=bf_result_col).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_col"]
        pd_result_col = pd_int64_col.apply(square_num)
        pd_result = pd_int64_col.to_frame().assign(result=pd_result_col)

        assert_pandas_df_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            square_num_remote, rf_session.bqclient, rf_session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    ("max_batching_rows"),
    [
        10_000,
        None,
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_max_batching_rows(session, scalars_dfs, max_batching_rows):
    try:

        def square(x):
            return x * x

        square_remote = session.remote_function(
            input_types=[int],
            output_type=int,
            reuse=False,
            max_batching_rows=max_batching_rows,
            cloud_function_service_account="default",
        )(square)

        bq_routine = session.bqclient.get_routine(
            square_remote.bigframes_bigquery_function
        )
        assert bq_routine.remote_function_options.max_batching_rows == max_batching_rows

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result = scalars_df["int64_too"].apply(square_remote).to_pandas()
        pd_result = scalars_pandas_df["int64_too"].apply(square)

        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            square_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    ("timeout_args", "effective_gcf_timeout"),
    [
        pytest.param({}, 600, id="no-set"),
        pytest.param({"cloud_function_timeout": None}, 60, id="set-None"),
        pytest.param({"cloud_function_timeout": 1200}, 1200, id="set-max-allowed"),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_gcf_timeout(
    session, scalars_dfs, timeout_args, effective_gcf_timeout
):
    try:

        def square(x):
            return x * x

        square_remote = session.remote_function(
            input_types=[int],
            output_type=int,
            reuse=False,
            cloud_function_service_account="default",
            **timeout_args,
        )(square)

        # Assert that the GCF is created with the intended maximum timeout
        gcf = session.cloudfunctionsclient.get_function(
            name=square_remote.bigframes_cloud_function
        )
        assert gcf.service_config.timeout_seconds == effective_gcf_timeout

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result = scalars_df["int64_too"].apply(square_remote).to_pandas()
        pd_result = scalars_pandas_df["int64_too"].apply(square)

        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            square_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_gcf_timeout_max_supported_exceeded(session):
    with pytest.raises(ValueError):

        @session.remote_function(
            input_types=[int],
            output_type=int,
            reuse=False,
            cloud_function_service_account="default",
            cloud_function_timeout=1201,
        )
        def square(x):
            return x * x


@pytest.mark.parametrize(
    ("max_instances_args", "expected_max_instances"),
    [
        pytest.param({}, 100, id="no-set"),
        pytest.param({"cloud_function_max_instances": None}, 100, id="set-None"),
        pytest.param({"cloud_function_max_instances": 1000}, 1000, id="set-explicit"),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_max_instances(
    session, scalars_dfs, max_instances_args, expected_max_instances
):
    try:

        def square(x):
            return x * x

        square_remote = session.remote_function(
            input_types=[int],
            output_type=int,
            reuse=False,
            cloud_function_service_account="default",
            **max_instances_args,
        )(square)

        # Assert that the GCF is created with the intended max instance count
        gcf = session.cloudfunctionsclient.get_function(
            name=square_remote.bigframes_cloud_function
        )
        assert gcf.service_config.max_instance_count == expected_max_instances

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result = scalars_df["int64_too"].apply(square_remote).to_pandas()
        pd_result = scalars_pandas_df["int64_too"].apply(square)

        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            square_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_axis_1(session, scalars_dfs):
    columns = ["bool_col", "int64_col", "int64_too", "float64_col", "string_col"]
    scalars_df, scalars_pandas_df = scalars_dfs
    try:

        def serialize_row(row):
            custom = {
                "name": row.name,
                "index": [idx for idx in row.index],
                "values": [
                    val.item() if hasattr(val, "item") else val for val in row.values
                ],
            }

            return str(
                {
                    "default": row.to_json(),
                    "split": row.to_json(orient="split"),
                    "records": row.to_json(orient="records"),
                    "index": row.to_json(orient="index"),
                    "table": row.to_json(orient="table"),
                    "custom": custom,
                }
            )

        serialize_row_remote = session.remote_function(
            input_types=bigframes.series.Series,
            output_type=str,
            reuse=False,
            cloud_function_service_account="default",
        )(serialize_row)

        assert getattr(serialize_row_remote, "is_row_processor")

        bf_result = scalars_df[columns].apply(serialize_row_remote, axis=1).to_pandas()
        pd_result = scalars_pandas_df[columns].apply(serialize_row, axis=1)

        # bf_result.dtype is 'string[pyarrow]' while pd_result.dtype is 'object'
        # , ignore this mismatch by using check_dtype=False.
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Let's make sure the read_gbq_function path works for this function
        serialize_row_reuse = session.read_gbq_function(
            serialize_row_remote.bigframes_bigquery_function, is_row_processor=True
        )
        bf_result = scalars_df[columns].apply(serialize_row_reuse, axis=1).to_pandas()
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            serialize_row_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_axis_1_aggregates(session, scalars_dfs):
    columns = ["int64_col", "int64_too", "float64_col"]
    scalars_df, scalars_pandas_df = scalars_dfs

    try:

        def analyze(row):
            return str(
                {
                    "dtype": row.dtype,
                    "count": row.count(),
                    "min": row.max(),
                    "max": row.max(),
                    "mean": row.mean(),
                    "std": row.std(),
                    "var": row.var(),
                }
            )

        analyze_remote = session.remote_function(
            input_types=bigframes.series.Series,
            output_type=str,
            reuse=False,
            cloud_function_service_account="default",
        )(analyze)

        assert getattr(analyze_remote, "is_row_processor")

        bf_result = (
            scalars_df[columns].dropna().apply(analyze_remote, axis=1).to_pandas()
        )
        pd_result = scalars_pandas_df[columns].dropna().apply(analyze, axis=1)

        # bf_result.dtype is 'string[pyarrow]' while pd_result.dtype is 'object'
        # , ignore this mismatch by using check_dtype=False.
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            analyze_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    ("pd_df"),
    [
        pytest.param(
            pandas.DataFrame(
                {
                    "2": [1, 2, 3],
                    2: [1.5, 3.75, 5],
                    "name, [with. special'- chars\")/\\": [10, 20, 30],
                    (3, 4): ["pq", "rs", "tu"],
                    (5.0, "six", 7): [8, 9, 10],
                    'raise Exception("hacked!")': [11, 12, 13],
                },
                # Default pandas index has non-numpy type, whereas bigframes is
                # always numpy-based type, so let's use the index compatible
                # with bigframes. See more details in b/369689696.
                index=pandas.Index([0, 1, 2], dtype=pandas.Int64Dtype()),
            ),
            id="all-kinds-of-column-names",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "x": [1, 2, 3],
                    "y": [1.5, 3.75, 5],
                    "z": ["pq", "rs", "tu"],
                },
                index=pandas.MultiIndex.from_frame(
                    pandas.DataFrame(
                        {
                            "idx0": pandas.Series(
                                ["a", "a", "b"], dtype=pandas.StringDtype()
                            ),
                            "idx1": pandas.Series(
                                [100, 200, 300], dtype=pandas.Int64Dtype()
                            ),
                        }
                    )
                ),
            ),
            id="multiindex",
            marks=pytest.mark.skip(
                reason="TODO: revert this skip after this pandas bug is fixed: https://github.com/pandas-dev/pandas/issues/59908"
            ),
        ),
        pytest.param(
            pandas.DataFrame(
                [
                    [10, 1.5, "pq"],
                    [20, 3.75, "rs"],
                    [30, 8.0, "tu"],
                ],
                # Default pandas index has non-numpy type, whereas bigframes is
                # always numpy-based type, so let's use the index compatible
                # with bigframes. See more details in b/369689696.
                index=pandas.Index([0, 1, 2], dtype=pandas.Int64Dtype()),
                columns=pandas.MultiIndex.from_arrays(
                    [
                        ["first", "last_two", "last_two"],
                        [1, 2, 3],
                    ]
                ),
            ),
            id="column-multiindex",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    datetime.now(): [1, 2, 3],
                }
            ),
            id="column-name-not-supported",
            marks=pytest.mark.xfail(raises=NameError),
        ),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_axis_1_complex(session, pd_df):
    bf_df = session.read_pandas(pd_df)

    try:

        def serialize_row(row):
            custom = {
                "name": row.name,
                "index": [idx for idx in row.index],
                "values": [
                    val.item() if hasattr(val, "item") else val for val in row.values
                ],
            }
            return str(
                {
                    "default": row.to_json(),
                    "split": row.to_json(orient="split"),
                    "records": row.to_json(orient="records"),
                    "index": row.to_json(orient="index"),
                    "custom": custom,
                }
            )

        serialize_row_remote = session.remote_function(
            input_types=bigframes.series.Series,
            output_type=str,
            reuse=False,
            cloud_function_service_account="default",
        )(serialize_row)

        assert getattr(serialize_row_remote, "is_row_processor")

        bf_result = bf_df.apply(serialize_row_remote, axis=1).to_pandas()
        pd_result = pd_df.apply(serialize_row, axis=1)

        # ignore known dtype difference between pandas and bigframes
        pandas.testing.assert_series_equal(
            pd_result, bf_result, check_dtype=False, check_index_type=False
        )
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            serialize_row_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_axis_1_na_nan_inf(session):
    """This test is for special cases of float values, to make sure any (nan,
    inf, -inf) produced by user code is honored.
    """
    bf_df = session.read_gbq(
        """\
SELECT "1" AS text, 1 AS num
UNION ALL
SELECT "2.5" AS text, 2.5 AS num
UNION ALL
SELECT "nan" AS text, IEEE_DIVIDE(0, 0) AS num
UNION ALL
SELECT "inf" AS text, IEEE_DIVIDE(1, 0) AS num
UNION ALL
SELECT "-inf" AS text, IEEE_DIVIDE(-1, 0) AS num
UNION ALL
SELECT "numpy nan" AS text, IEEE_DIVIDE(0, 0) AS num
UNION ALL
SELECT "pandas na" AS text, NULL AS num
                             """
    )

    pd_df = bf_df.to_pandas()

    try:

        def float_parser(row):
            import numpy as mynp
            import pandas as mypd

            if row["text"] == "pandas na":
                return mypd.NA
            if row["text"] == "numpy nan":
                return mynp.nan
            return float(row["text"])

        float_parser_remote = session.remote_function(
            input_types=bigframes.series.Series,
            output_type=float,
            reuse=False,
            cloud_function_service_account="default",
        )(float_parser)

        assert getattr(float_parser_remote, "is_row_processor")

        pd_result = pd_df.apply(float_parser, axis=1)
        bf_result = bf_df.apply(float_parser_remote, axis=1).to_pandas()

        # bf_result.dtype is 'Float64' while pd_result.dtype is 'object'
        # , ignore this mismatch by using check_dtype=False.
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Let's also assert that the data is consistent in this round trip
        # (BQ -> BigFrames -> BQ -> GCF -> BQ -> BigFrames) w.r.t. their
        # expected values in BQ
        bq_result = bf_df["num"].to_pandas()
        bq_result.name = None
        pandas.testing.assert_series_equal(bq_result, bf_result)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            float_parser_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    ("memory_mib_args", "expected_memory"),
    [
        pytest.param({}, "1024Mi", id="no-set"),
        pytest.param({"cloud_function_memory_mib": None}, "256M", id="set-None"),
        pytest.param({"cloud_function_memory_mib": 128}, "128Mi", id="set-128"),
        pytest.param({"cloud_function_memory_mib": 1024}, "1024Mi", id="set-1024"),
        pytest.param({"cloud_function_memory_mib": 4096}, "4096Mi", id="set-4096"),
        pytest.param({"cloud_function_memory_mib": 32768}, "32768Mi", id="set-32768"),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_gcf_memory(
    session, scalars_dfs, memory_mib_args, expected_memory
):
    try:

        def square(x: int) -> int:
            return x * x

        square_remote = session.remote_function(
            reuse=False, cloud_function_service_account="default", **memory_mib_args
        )(square)

        # Assert that the GCF is created with the intended memory
        gcf = session.cloudfunctionsclient.get_function(
            name=square_remote.bigframes_cloud_function
        )
        assert gcf.service_config.available_memory == expected_memory

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result = scalars_df["int64_too"].apply(square_remote).to_pandas()
        pd_result = scalars_pandas_df["int64_too"].apply(square)

        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            square_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    ("memory_mib",),
    [
        pytest.param(127, id="127-too-low"),
        pytest.param(32769, id="set-32769-too-high"),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_gcf_memory_unsupported(session, memory_mib):
    with pytest.raises(
        google.api_core.exceptions.InvalidArgument,
        match="Invalid value specified for container memory",
    ):

        @session.remote_function(
            reuse=False,
            cloud_function_service_account="default",
            cloud_function_memory_mib=memory_mib,
        )
        def square(x: int) -> int:
            return x * x


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_unnamed_removed_w_session_cleanup():
    # create a clean session
    session = bigframes.connect()

    # create an unnamed remote function in the session
    @session.remote_function(reuse=False, cloud_function_service_account="default")
    def foo(x: int) -> int:
        return x + 1

    # ensure that remote function artifacts are created
    assert foo.bigframes_remote_function is not None
    session.bqclient.get_routine(foo.bigframes_remote_function) is not None
    assert foo.bigframes_bigquery_function is not None
    session.bqclient.get_routine(foo.bigframes_bigquery_function) is not None
    assert foo.bigframes_cloud_function is not None
    session.cloudfunctionsclient.get_function(
        name=foo.bigframes_cloud_function
    ) is not None

    # explicitly close the session
    session.close()

    # ensure that the bq remote function is deleted
    with pytest.raises(google.cloud.exceptions.NotFound):
        session.bqclient.get_routine(foo.bigframes_bigquery_function)

    # the deletion of cloud function happens in a non-blocking way, ensure that
    # it either exists in a being-deleted state, or is already deleted
    try:
        gcf = session.cloudfunctionsclient.get_function(
            name=foo.bigframes_cloud_function
        )
        assert gcf.state is functions_v2.Function.State.DELETING
    except google.cloud.exceptions.NotFound:
        pass


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_named_perists_w_session_cleanup():
    try:
        # create a clean session
        session = bigframes.connect()

        # create a name for the remote function
        name = test_utils.prefixer.Prefixer("bigframes", "").create_prefix()

        # create an unnamed remote function in the session
        @session.remote_function(
            reuse=False, name=name, cloud_function_service_account="default"
        )
        def foo(x: int) -> int:
            return x + 1

        # ensure that remote function artifacts are created
        assert foo.bigframes_remote_function is not None
        session.bqclient.get_routine(foo.bigframes_remote_function) is not None
        assert foo.bigframes_bigquery_function is not None
        session.bqclient.get_routine(foo.bigframes_bigquery_function) is not None
        assert foo.bigframes_cloud_function is not None
        session.cloudfunctionsclient.get_function(
            name=foo.bigframes_cloud_function
        ) is not None

        # explicitly close the session
        session.close()

        # ensure that the bq remote function still exists
        session.bqclient.get_routine(foo.bigframes_bigquery_function) is not None

        # the deletion of cloud function happens in a non-blocking way, ensure
        # that it was not deleted and still exists in active state
        gcf = session.cloudfunctionsclient.get_function(
            name=foo.bigframes_cloud_function
        )
        assert gcf.state is functions_v2.Function.State.ACTIVE
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(foo, session.bqclient, session.cloudfunctionsclient)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_clean_up_by_session_id():
    # Use a brand new session to avoid conflict with other tests
    session = bigframes.Session()
    session_id = session.session_id
    try:
        # we will create remote functions, one with explicit name and another
        # without it, and later confirm that the former is deleted when the session
        # is cleaned up by session id, but the latter remains
        ## unnamed
        @session.remote_function(reuse=False, cloud_function_service_account="default")
        def foo_unnamed(x: int) -> int:
            return x + 1

        ## named
        rf_name = test_utils.prefixer.Prefixer("bigframes", "").create_prefix()

        @session.remote_function(
            reuse=False, name=rf_name, cloud_function_service_account="default"
        )
        def foo_named(x: int) -> int:
            return x + 2

        # check that BQ remote functiosn were created with corresponding cloud
        # functions
        for foo in [foo_unnamed, foo_named]:
            assert foo.bigframes_remote_function is not None
            session.bqclient.get_routine(foo.bigframes_remote_function) is not None
            assert foo.bigframes_bigquery_function is not None
            session.bqclient.get_routine(foo.bigframes_bigquery_function) is not None
            assert foo.bigframes_cloud_function is not None
            session.cloudfunctionsclient.get_function(
                name=foo.bigframes_cloud_function
            ) is not None

        # clean up using explicit session id
        bpd.clean_up_by_session_id(
            session_id, location=session._location, project=session._project
        )

        # ensure that the unnamed bq remote function is deleted along with its
        # corresponding cloud function
        with pytest.raises(google.cloud.exceptions.NotFound):
            session.bqclient.get_routine(foo_unnamed.bigframes_bigquery_function)
        try:
            gcf = session.cloudfunctionsclient.get_function(
                name=foo_unnamed.bigframes_cloud_function
            )
            assert gcf.state is functions_v2.Function.State.DELETING
        except google.cloud.exceptions.NotFound:
            pass

        # ensure that the named bq remote function still exists along with its
        # corresponding cloud function
        session.bqclient.get_routine(foo_named.bigframes_bigquery_function) is not None
        gcf = session.cloudfunctionsclient.get_function(
            name=foo_named.bigframes_cloud_function
        )
        assert gcf.state is functions_v2.Function.State.ACTIVE
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            foo_named, session.bqclient, session.cloudfunctionsclient
        )


def test_df_apply_axis_1_multiple_params(session):
    bf_df = bigframes.dataframe.DataFrame(
        {
            "Id": [1, 2, 3],
            "Age": [22.5, 23, 23.5],
            "Name": ["alpha", "beta", "gamma"],
        }
    )

    expected_dtypes = (
        bigframes.dtypes.INT_DTYPE,
        bigframes.dtypes.FLOAT_DTYPE,
        bigframes.dtypes.STRING_DTYPE,
    )

    # Assert the dataframe dtypes
    assert tuple(bf_df.dtypes) == expected_dtypes

    try:

        @session.remote_function(
            input_types=[int, float, str],
            output_type=str,
            reuse=False,
            cloud_function_service_account="default",
        )
        def foo(x, y, z):
            return f"I got {x}, {y} and {z}"

        assert getattr(foo, "is_row_processor") is False
        assert getattr(foo, "input_dtypes") == expected_dtypes

        # Fails to apply on dataframe with incompatible number of columns
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes 3 arguments but DataFrame has 2 columns\\.$",
        ):
            bf_df[["Id", "Age"]].apply(foo, axis=1)
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes 3 arguments but DataFrame has 4 columns\\.$",
        ):
            bf_df.assign(Country="lalaland").apply(foo, axis=1)

        # Fails to apply on dataframe with incompatible column datatypes
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes arguments of types .* but DataFrame dtypes are .*",
        ):
            bf_df.assign(Age=bf_df["Age"].astype("Int64")).apply(foo, axis=1)

        # Successfully applies to dataframe with matching number of columns
        # and their datatypes
        bf_result = bf_df.apply(foo, axis=1).to_pandas()

        # Since this scenario is not pandas-like, let's handcraft the
        # expected result
        expected_result = pandas.Series(
            [
                "I got 1, 22.5 and alpha",
                "I got 2, 23 and beta",
                "I got 3, 23.5 and gamma",
            ]
        )

        pandas.testing.assert_series_equal(
            expected_result, bf_result, check_dtype=False, check_index_type=False
        )

        # Let's make sure the read_gbq_function path works for this function
        foo_reuse = session.read_gbq_function(foo.bigframes_bigquery_function)
        bf_result = bf_df.apply(foo_reuse, axis=1).to_pandas()
        pandas.testing.assert_series_equal(
            expected_result, bf_result, check_dtype=False, check_index_type=False
        )
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(foo, session.bqclient, session.cloudfunctionsclient)


def test_df_apply_axis_1_multiple_params_array_output(session):
    bf_df = bigframes.dataframe.DataFrame(
        {
            "Id": [1, 2, 3],
            "Age": [22.5, 23, 23.5],
            "Name": ["alpha", "beta", "gamma"],
        }
    )

    expected_dtypes = (
        bigframes.dtypes.INT_DTYPE,
        bigframes.dtypes.FLOAT_DTYPE,
        bigframes.dtypes.STRING_DTYPE,
    )

    # Assert the dataframe dtypes
    assert tuple(bf_df.dtypes) == expected_dtypes

    try:

        @session.remote_function(
            input_types=[int, float, str],
            output_type=list[str],
            reuse=False,
            cloud_function_service_account="default",
        )
        def foo(x, y, z):
            return [str(x), str(y), z]

        assert getattr(foo, "is_row_processor") is False
        assert getattr(foo, "input_dtypes") == expected_dtypes
        assert (
            getattr(foo, "bigframes_bigquery_function_output_dtype")
            == bigframes.dtypes.STRING_DTYPE
        )

        # Fails to apply on dataframe with incompatible number of columns
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes 3 arguments but DataFrame has 2 columns\\.$",
        ):
            bf_df[["Id", "Age"]].apply(foo, axis=1)
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes 3 arguments but DataFrame has 4 columns\\.$",
        ):
            bf_df.assign(Country="lalaland").apply(foo, axis=1)

        # Fails to apply on dataframe with incompatible column datatypes
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes arguments of types .* but DataFrame dtypes are .*",
        ):
            bf_df.assign(Age=bf_df["Age"].astype("Int64")).apply(foo, axis=1)

        # Successfully applies to dataframe with matching number of columns
        # and their datatypes
        bf_result = bf_df.apply(foo, axis=1).to_pandas()

        # Since this scenario is not pandas-like, let's handcraft the
        # expected result
        expected_result = pandas.Series(
            [
                ["1", "22.5", "alpha"],
                ["2", "23", "beta"],
                ["3", "23.5", "gamma"],
            ]
        )

        pandas.testing.assert_series_equal(
            expected_result, bf_result, check_dtype=False, check_index_type=False
        )

        # Let's make sure the read_gbq_function path works for this function
        foo_reuse = session.read_gbq_function(foo.bigframes_bigquery_function)
        bf_result = bf_df.apply(foo_reuse, axis=1).to_pandas()
        pandas.testing.assert_series_equal(
            expected_result, bf_result, check_dtype=False, check_index_type=False
        )
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(foo, session.bqclient, session.cloudfunctionsclient)


def test_df_apply_axis_1_single_param_non_series(session):
    bf_df = bigframes.dataframe.DataFrame(
        {
            "Id": [1, 2, 3],
        }
    )

    expected_dtypes = (bigframes.dtypes.INT_DTYPE,)

    # Assert the dataframe dtypes
    assert tuple(bf_df.dtypes) == expected_dtypes

    try:

        @session.remote_function(
            input_types=[int],
            output_type=str,
            reuse=False,
            cloud_function_service_account="default",
        )
        def foo(x):
            return f"I got {x}"

        assert getattr(foo, "is_row_processor") is False
        assert getattr(foo, "input_dtypes") == expected_dtypes

        # Fails to apply on dataframe with incompatible number of columns
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes 1 arguments but DataFrame has 0 columns\\.$",
        ):
            bf_df[[]].apply(foo, axis=1)
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes 1 arguments but DataFrame has 2 columns\\.$",
        ):
            bf_df.assign(Country="lalaland").apply(foo, axis=1)

        # Fails to apply on dataframe with incompatible column datatypes
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes arguments of types .* but DataFrame dtypes are .*",
        ):
            bf_df.assign(Id=bf_df["Id"].astype("Float64")).apply(foo, axis=1)

        # Successfully applies to dataframe with matching number of columns
        # and their datatypes
        bf_result = bf_df.apply(foo, axis=1).to_pandas()

        # Since this scenario is not pandas-like, let's handcraft the
        # expected result
        expected_result = pandas.Series(
            [
                "I got 1",
                "I got 2",
                "I got 3",
            ]
        )

        pandas.testing.assert_series_equal(
            expected_result, bf_result, check_dtype=False, check_index_type=False
        )
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(foo, session.bqclient, session.cloudfunctionsclient)


@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_axis_1_array_output(session, scalars_dfs):
    columns = ["int64_col", "int64_too"]
    scalars_df, scalars_pandas_df = scalars_dfs
    try:

        @session.remote_function(reuse=False, cloud_function_service_account="default")
        def generate_stats(row: pandas.Series) -> list[int]:
            import pandas as pd

            sum = row["int64_too"]
            avg = row["int64_too"]
            if pd.notna(row["int64_col"]):
                sum += row["int64_col"]
                avg = round((avg + row["int64_col"]) / 2)
            return [sum, avg]

        assert getattr(generate_stats, "is_row_processor")

        bf_result = scalars_df[columns].apply(generate_stats, axis=1).to_pandas()
        pd_result = scalars_pandas_df[columns].apply(generate_stats, axis=1)

        # bf_result.dtype is 'list<item: int64>[pyarrow]' while pd_result.dtype
        # is 'object', ignore this mismatch by using check_dtype=False.
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Let's make sure the read_gbq_function path works for this function
        generate_stats_reuse = session.read_gbq_function(
            generate_stats.bigframes_bigquery_function,
            is_row_processor=True,
        )
        bf_result = scalars_df[columns].apply(generate_stats_reuse, axis=1).to_pandas()
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            generate_stats, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    (
        "ingress_settings_args",
        "effective_ingress_settings",
        "expect_default_ingress_setting_warning",
    ),
    [
        pytest.param(
            {},
            functions_v2.ServiceConfig.IngressSettings.ALLOW_INTERNAL_ONLY,
            False,
            id="no-set",
        ),
        pytest.param(
            {"cloud_function_ingress_settings": None},
            functions_v2.ServiceConfig.IngressSettings.ALLOW_INTERNAL_ONLY,
            True,
            id="set-none",
        ),
        pytest.param(
            {"cloud_function_ingress_settings": "all"},
            functions_v2.ServiceConfig.IngressSettings.ALLOW_ALL,
            False,
            id="set-all",
        ),
        pytest.param(
            {"cloud_function_ingress_settings": "internal-only"},
            functions_v2.ServiceConfig.IngressSettings.ALLOW_INTERNAL_ONLY,
            False,
            id="set-internal-only",
        ),
        pytest.param(
            {"cloud_function_ingress_settings": "internal-and-gclb"},
            functions_v2.ServiceConfig.IngressSettings.ALLOW_INTERNAL_AND_GCLB,
            False,
            id="set-internal-and-gclb",
        ),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_ingress_settings(
    session,
    scalars_dfs,
    ingress_settings_args,
    effective_ingress_settings,
    expect_default_ingress_setting_warning,
):
    try:
        # Verify the function raises the expected security warning message.
        with warnings.catch_warnings(record=True) as record:

            def square(x: int) -> int:
                return x * x

            square_remote = session.remote_function(
                reuse=False,
                cloud_function_service_account="default",
                **ingress_settings_args,
            )(square)

        default_ingress_setting_warnings = [
            warn
            for warn in record
            if isinstance(warn.message, UserWarning)
            and "The `cloud_function_ingress_settings` is being set to 'internal-only' by default."
        ]
        assert len(default_ingress_setting_warnings) == (
            1 if expect_default_ingress_setting_warning else 0
        )

        # Assert that the GCF is created with the intended maximum timeout
        gcf = session.cloudfunctionsclient.get_function(
            name=square_remote.bigframes_cloud_function
        )
        assert gcf.service_config.ingress_settings == effective_ingress_settings

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result = scalars_df["int64_too"].apply(square_remote).to_pandas()
        pd_result = scalars_pandas_df["int64_too"].apply(square)

        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            square_remote, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_ingress_settings_unsupported(session):
    with pytest.raises(
        ValueError, match="'unknown' not one of the supported ingress settings values"
    ):

        @session.remote_function(
            reuse=False,
            cloud_function_service_account="default",
            cloud_function_ingress_settings="unknown",
        )
        def square(x: int) -> int:
            return x * x


@pytest.mark.parametrize(
    ("session_creator"),
    [
        pytest.param(bigframes.Session, id="session-constructor"),
        pytest.param(bigframes.connect, id="connect-method"),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_w_context_manager_unnamed(
    scalars_dfs, dataset_id, bq_cf_connection, session_creator
):
    def add_one(x: int) -> int:
        return x + 1

    scalars_df, scalars_pandas_df = scalars_dfs
    pd_result = scalars_pandas_df["int64_too"].apply(add_one)

    temporary_bigquery_remote_function = None
    temporary_cloud_run_function = None

    try:
        with session_creator() as session:
            # create a temporary remote function
            add_one_remote_temp = session.remote_function(
                dataset=dataset_id,
                bigquery_connection=bq_cf_connection,
                reuse=False,
                cloud_function_service_account="default",
            )(add_one)

            temporary_bigquery_remote_function = (
                add_one_remote_temp.bigframes_bigquery_function
            )
            assert temporary_bigquery_remote_function is not None
            assert (
                session.bqclient.get_routine(temporary_bigquery_remote_function)
                is not None
            )

            temporary_cloud_run_function = add_one_remote_temp.bigframes_cloud_function
            assert temporary_cloud_run_function is not None
            assert (
                session.cloudfunctionsclient.get_function(
                    name=temporary_cloud_run_function
                )
                is not None
            )

            bf_result = scalars_df["int64_too"].apply(add_one_remote_temp).to_pandas()
            pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)

        # outside the with statement context manager the temporary BQ remote
        # function and the underlying cloud run function should have been
        # cleaned up
        assert temporary_bigquery_remote_function is not None
        with pytest.raises(google.api_core.exceptions.NotFound):
            session.bqclient.get_routine(temporary_bigquery_remote_function)
        # the deletion of cloud function happens in a non-blocking way, ensure that
        # it either exists in a being-deleted state, or is already deleted
        assert temporary_cloud_run_function is not None
        try:
            gcf = session.cloudfunctionsclient.get_function(
                name=temporary_cloud_run_function
            )
            assert gcf.state is functions_v2.Function.State.DELETING
        except google.cloud.exceptions.NotFound:
            pass
    finally:
        # clean up the gcp assets created for the temporary remote function,
        # just in case it was not explicitly cleaned up in the try clause due
        # to assertion failure or exception earlier than that
        cleanup_function_assets(
            add_one_remote_temp, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    ("session_creator"),
    [
        pytest.param(bigframes.Session, id="session-constructor"),
        pytest.param(bigframes.connect, id="connect-method"),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_w_context_manager_named(
    scalars_dfs, dataset_id, bq_cf_connection, session_creator
):
    def add_one(x: int) -> int:
        return x + 1

    scalars_df, scalars_pandas_df = scalars_dfs
    pd_result = scalars_pandas_df["int64_too"].apply(add_one)

    persistent_bigquery_remote_function = None
    persistent_cloud_run_function = None

    try:
        with session_creator() as session:
            # create a persistent remote function
            name = test_utils.prefixer.Prefixer("bigframes", "").create_prefix()
            add_one_remote_persist = session.remote_function(
                dataset=dataset_id,
                bigquery_connection=bq_cf_connection,
                reuse=False,
                name=name,
                cloud_function_service_account="default",
            )(add_one)

            persistent_bigquery_remote_function = (
                add_one_remote_persist.bigframes_bigquery_function
            )
            assert persistent_bigquery_remote_function is not None
            assert (
                session.bqclient.get_routine(persistent_bigquery_remote_function)
                is not None
            )

            persistent_cloud_run_function = (
                add_one_remote_persist.bigframes_cloud_function
            )
            assert persistent_cloud_run_function is not None
            assert (
                session.cloudfunctionsclient.get_function(
                    name=persistent_cloud_run_function
                )
                is not None
            )

            bf_result = (
                scalars_df["int64_too"].apply(add_one_remote_persist).to_pandas()
            )
            pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)

        # outside the with statement context manager the persistent BQ remote
        # function and the underlying cloud run function should still exist
        assert persistent_bigquery_remote_function is not None
        assert (
            session.bqclient.get_routine(persistent_bigquery_remote_function)
            is not None
        )
        assert persistent_cloud_run_function is not None
        assert (
            session.cloudfunctionsclient.get_function(
                name=persistent_cloud_run_function
            )
            is not None
        )
    finally:
        # clean up the gcp assets created for the persistent remote function
        cleanup_function_assets(
            add_one_remote_persist, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.parametrize(
    "array_dtype",
    [
        bool,
        int,
        float,
        str,
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_array_output(
    session, scalars_dfs, dataset_id, bq_cf_connection, array_dtype
):
    try:

        @session.remote_function(
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
        )
        def featurize(x: int) -> list[array_dtype]:  # type: ignore
            return [array_dtype(i) for i in [x, x + 1, x + 2]]

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_too"]
        bf_result = bf_int64_col.apply(featurize).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_too"]
        pd_result = pd_int64_col.apply(featurize)

        # ignore any dtype disparity
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Let's make sure the read_gbq_function path works for this function
        featurize_reuse = session.read_gbq_function(
            featurize.bigframes_bigquery_function  # type: ignore
        )
        bf_result = scalars_df["int64_too"].apply(featurize_reuse).to_pandas()
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            featurize, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_array_output_partial_ordering_mode(
    unordered_session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:

        @unordered_session.remote_function(
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
        )
        def featurize(x: float) -> list[float]:  # type: ignore
            return [x, x + 1, x + 2]

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["float64_col"].dropna()
        bf_result = bf_int64_col.apply(featurize).to_pandas()

        pd_int64_col = scalars_pandas_df["float64_col"].dropna()
        pd_result = pd_int64_col.apply(featurize)

        # ignore any dtype disparity
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Let's make sure the read_gbq_function path works for this function
        featurize_reuse = unordered_session.read_gbq_function(
            featurize.bigframes_bigquery_function  # type: ignore
        )
        bf_int64_col = scalars_df["float64_col"].dropna()
        bf_result = bf_int64_col.apply(featurize_reuse).to_pandas()
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            featurize,
            unordered_session.bqclient,
            unordered_session.cloudfunctionsclient,
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_array_output_multiindex(
    session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:

        @session.remote_function(
            dataset=dataset_id,
            bigquery_connection=bq_cf_connection,
            reuse=False,
            cloud_function_service_account="default",
        )
        def featurize(x: int) -> list[float]:
            return [x, x + 0.5, x + 0.33]

        scalars_df, scalars_pandas_df = scalars_dfs
        multiindex_cols = ["rowindex", "string_col"]
        scalars_df = scalars_df.reset_index().set_index(multiindex_cols)
        scalars_pandas_df = scalars_pandas_df.reset_index().set_index(multiindex_cols)

        bf_int64_col = scalars_df["int64_too"]
        bf_result = bf_int64_col.apply(featurize).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_too"]
        pd_result = pd_int64_col.apply(featurize)

        # ignore any dtype disparity
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(
            featurize, session.bqclient, session.cloudfunctionsclient
        )


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_connection_path_format(
    session, scalars_dfs, dataset_id, bq_cf_connection
):
    try:

        @session.remote_function(
            dataset=dataset_id,
            bigquery_connection=f"projects/{session.bqclient.project}/locations/{session._location}/connections/{bq_cf_connection}",
            reuse=False,
            cloud_function_service_account="default",
        )
        def foo(x: int) -> int:
            return x + 1

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_too"]
        bf_result = bf_int64_col.apply(foo).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_too"]
        pd_result = pd_int64_col.apply(foo)

        # ignore any dtype disparity
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)
    finally:
        # clean up the gcp assets created for the remote function
        cleanup_function_assets(foo, session.bqclient, session.cloudfunctionsclient)
