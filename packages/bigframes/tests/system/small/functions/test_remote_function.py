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

import inspect
import re
import textwrap

import bigframes_vendored.constants as constants
import google.api_core.exceptions
from google.cloud import bigquery
import pandas as pd
import pyarrow
import pytest
import test_utils.prefixer

import bigframes
import bigframes.clients
import bigframes.dtypes
import bigframes.exceptions
from bigframes.functions import _utils as bff_utils
from bigframes.functions import function as bff
import bigframes.session._io.bigquery
from bigframes.testing.utils import assert_pandas_df_equal, get_function_name

_prefixer = test_utils.prefixer.Prefixer("bigframes", "")


@pytest.fixture(scope="module")
def bq_cf_connection() -> str:
    """Pre-created BQ connection in the test project in US location, used to
    invoke cloud function.

    $ bq show --connection --location=us --project_id=PROJECT_ID bigframes-rf-conn
    """
    return "bigframes-rf-conn"


@pytest.fixture(scope="module")
def bq_cf_connection_location() -> str:
    """Pre-created BQ connection in the test project in US location, in format
    PROJECT_ID.LOCATION.CONNECTION_NAME, used to invoke cloud function.

    $ bq show --connection --location=us --project_id=PROJECT_ID bigframes-rf-conn
    """
    return "us.bigframes-rf-conn"


@pytest.fixture(scope="module")
def bq_cf_connection_location_mismatched() -> str:
    """Pre-created BQ connection in the test project in EU location, in format
    LOCATION.CONNECTION_NAME, used to invoke cloud function.

    $ bq show --connection --location=us --project_id=PROJECT_ID bigframes-rf-conn
    """
    return "eu.bigframes-rf-conn"


@pytest.fixture(scope="module")
def bq_cf_connection_location_project(bigquery_client) -> str:
    """Pre-created BQ connection in the test project in US location, in format
    PROJECT_ID.LOCATION.CONNECTION_NAME, used to invoke cloud function.

    $ bq show --connection --location=us --project_id=PROJECT_ID bigframes-rf-conn
    """
    return f"{bigquery_client.project}.us.bigframes-rf-conn"


@pytest.fixture(scope="module")
def bq_cf_connection_location_project_mismatched() -> str:
    """Pre-created BQ connection in the bigframes-metrics project in US location,
    in format PROJECT_ID.LOCATION.CONNECTION_NAME, used to invoke cloud function.

    $ bq show --connection --location=us --project_id=PROJECT_ID bigframes-rf-conn
    """
    return "bigframes-metrics.eu.bigframes-rf-conn"


@pytest.fixture(scope="module")
def session_with_bq_connection(bq_cf_connection) -> bigframes.Session:
    session = bigframes.Session(
        bigframes.BigQueryOptions(bq_connection=bq_cf_connection, location="US")
    )
    return session


def get_bq_connection_id_path_format(connection_id_dot_format):
    fields = connection_id_dot_format.split(".")
    return f"projects/{fields[0]}/locations/{fields[1]}/connections/{fields[2]}"


# @pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_direct_no_session_param(
    bigquery_client,
    bigqueryconnection_client,
    cloudfunctions_client,
    resourcemanager_client,
    scalars_dfs,
    dataset_id_permanent,
    bq_cf_connection,
):
    def square(x):
        return x * x

    square = bff.remote_function(
        input_types=int,
        output_type=int,
        bigquery_client=bigquery_client,
        bigquery_connection_client=bigqueryconnection_client,
        cloud_functions_client=cloudfunctions_client,
        resource_manager_client=resourcemanager_client,
        dataset=dataset_id_permanent,
        bigquery_connection=bq_cf_connection,
        # See e2e tests for tests that actually deploy the Cloud Function.
        reuse=True,
        name=get_function_name(square),
        cloud_function_service_account="default",
    )(square)

    # Function should still work normally.
    assert square(2) == 4

    # Function should have extra metadata attached for remote execution.
    assert hasattr(square, "bigframes_remote_function")
    assert hasattr(square, "bigframes_bigquery_function")
    assert hasattr(square, "bigframes_cloud_function")

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
    pd_result_col = pd_result_col.astype(pd.Int64Dtype())
    pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_connection_w_location(
    session,
    scalars_dfs,
    dataset_id_permanent,
    bq_cf_connection_location,
):
    def square(x):
        return x * x

    square = bff.remote_function(
        input_types=int,
        output_type=int,
        session=session,
        dataset=dataset_id_permanent,
        bigquery_connection=bq_cf_connection_location,
        # See e2e tests for tests that actually deploy the Cloud Function.
        reuse=True,
        name=get_function_name(square),
        cloud_function_service_account="default",
    )(square)

    # Function should still work normally.
    assert square(2) == 4

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
    pd_result_col = pd_result_col.astype(pd.Int64Dtype())
    pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_connection_w_location_mismatched(
    session,
    dataset_id_permanent,
    bq_cf_connection_location_mismatched,
):
    def square(x):
        # Not expected to reach this code, as the location of the
        # connection doesn't match the location of the dataset.
        return x * x  # pragma: NO COVER

    bq_cf_connection_location_mismatched_path_fmt = get_bq_connection_id_path_format(
        bigframes.clients.get_canonical_bq_connection_id(
            bq_cf_connection_location_mismatched,
            session.bqclient.project,
            session._location,
        )
    )
    connection_ids = [
        bq_cf_connection_location_mismatched,
        bq_cf_connection_location_mismatched_path_fmt,
    ]

    for connection_id in connection_ids:
        with pytest.raises(
            ValueError,
            match=re.escape(
                "The location does not match BigQuery connection location:"
            ),
        ):
            bff.remote_function(
                input_types=int,
                output_type=int,
                session=session,
                dataset=dataset_id_permanent,
                bigquery_connection=connection_id,
                # See e2e tests for tests that actually deploy the Cloud Function.
                reuse=True,
                name=get_function_name(square),
                cloud_function_service_account="default",
            )(square)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_connection_w_location_project(
    session,
    scalars_dfs,
    dataset_id_permanent,
    bq_cf_connection_location_project,
):
    def square(x):
        return x * x

    square = bff.remote_function(
        input_types=int,
        output_type=int,
        session=session,
        dataset=dataset_id_permanent,
        bigquery_connection=bq_cf_connection_location_project,
        # See e2e tests for tests that actually deploy the Cloud Function.
        reuse=True,
        name=get_function_name(square),
        cloud_function_service_account="default",
    )(square)

    # Function should still work normally.
    assert square(2) == 4

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
    pd_result_col = pd_result_col.astype(pd.Int64Dtype())
    pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_connection_w_project_mismatched(
    session,
    dataset_id_permanent,
    bq_cf_connection_location_project_mismatched,
):
    def square(x):
        # Not expected to reach this code, as the project of the
        # connection doesn't match the project of the dataset.
        return x * x  # pragma: NO COVER

    bq_cf_connection_location_project_mismatched_path_fmt = (
        get_bq_connection_id_path_format(
            bigframes.clients.get_canonical_bq_connection_id(
                bq_cf_connection_location_project_mismatched,
                session.bqclient.project,
                session._location,
            )
        )
    )
    connection_ids = [
        bq_cf_connection_location_project_mismatched,
        bq_cf_connection_location_project_mismatched_path_fmt,
    ]

    for connection_id in connection_ids:
        with pytest.raises(
            ValueError,
            match=re.escape(
                "The project_id does not match BigQuery connection gcp_project_id:"
            ),
        ):
            bff.remote_function(
                input_types=int,
                output_type=int,
                session=session,
                dataset=dataset_id_permanent,
                bigquery_connection=connection_id,
                # See e2e tests for tests that actually deploy the Cloud Function.
                reuse=True,
                name=get_function_name(square),
                cloud_function_service_account="default",
            )(square)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_direct_session_param(
    session_with_bq_connection, scalars_dfs, dataset_id_permanent
):
    def square(x):
        return x * x

    square = bff.remote_function(
        input_types=int,
        output_type=int,
        session=session_with_bq_connection,
        dataset=dataset_id_permanent,
        name=get_function_name(square),
        cloud_function_service_account="default",
    )(square)

    # Function should still work normally.
    assert square(2) == 4

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
    pd_result_col = pd_result_col.astype(pd.Int64Dtype())
    pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_via_session_default(
    session_with_bq_connection, scalars_dfs, dataset_id_permanent
):
    def square(x):
        return x * x

    # Session has bigquery connection initialized via context. Without an
    # explicit dataset the default dataset from the session would be used.
    # Without an explicit bigquery connection, the one present in Session set
    # through the explicit BigQueryOptions would be used. Without an explicit `reuse`
    # the default behavior of reuse=True will take effect. Please note that the
    # udf is same as the one used in other tests in this file so the underlying
    # cloud function would be common and quickly reused.
    square = session_with_bq_connection.remote_function(
        input_types=int,
        output_type=int,
        dataset=dataset_id_permanent,
        name=get_function_name(square),
        cloud_function_service_account="default",
    )(square)

    # Function should still work normally.
    assert square(2) == 4

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
    pd_result_col = pd_result_col.astype(pd.Int64Dtype())
    pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_via_session_with_overrides(
    session, scalars_dfs, dataset_id_permanent, bq_cf_connection
):
    def square(x):
        return x * x

    square = session.remote_function(
        input_types=int,
        output_type=int,
        dataset=dataset_id_permanent,
        bigquery_connection=bq_cf_connection,
        # See e2e tests for tests that actually deploy the Cloud Function.
        reuse=True,
        name=get_function_name(square),
        cloud_function_service_account="default",
    )(square)

    # Function should still work normally.
    assert square(2) == 4

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
    pd_result_col = pd_result_col.astype(pd.Int64Dtype())
    pd_result = pd_int64_col_filtered.to_frame().assign(result=pd_result_col)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.flaky(retries=2, delay=120)
def test_dataframe_applymap(
    session_with_bq_connection, scalars_dfs, dataset_id_permanent
):
    def add_one(x):
        return x + 1

    remote_add_one = session_with_bq_connection.remote_function(
        input_types=[int],
        output_type=int,
        dataset=dataset_id_permanent,
        name=get_function_name(add_one),
        cloud_function_service_account="default",
    )(add_one)

    scalars_df, scalars_pandas_df = scalars_dfs
    int64_cols = ["int64_col", "int64_too"]

    bf_int64_df = scalars_df[int64_cols]
    bf_int64_df_filtered = bf_int64_df.dropna()
    bf_result = bf_int64_df_filtered.applymap(remote_add_one).to_pandas()

    pd_int64_df = scalars_pandas_df[int64_cols]
    pd_int64_df_filtered = pd_int64_df.dropna()
    pd_result = pd_int64_df_filtered.applymap(add_one)
    # TODO(shobs): Figure why pandas .applymap() changes the dtype, i.e.
    # pd_int64_df_filtered.dtype is Int64Dtype()
    # pd_int64_df_filtered.applymap(lambda x: x).dtype is int64.
    # For this test let's force the pandas dtype to be same as input.
    for col in pd_result:
        pd_result[col] = pd_result[col].astype(pd_int64_df_filtered[col].dtype)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.flaky(retries=2, delay=120)
def test_dataframe_applymap_explicit_filter(
    session_with_bq_connection, scalars_dfs, dataset_id_permanent
):
    def add_one(x):
        return x + 1

    remote_add_one = session_with_bq_connection.remote_function(
        input_types=[int],
        output_type=int,
        dataset=dataset_id_permanent,
        name=get_function_name(add_one),
        cloud_function_service_account="default",
    )(add_one)

    scalars_df, scalars_pandas_df = scalars_dfs
    int64_cols = ["int64_col", "int64_too"]

    bf_int64_df = scalars_df[int64_cols]
    bf_int64_df_filtered = bf_int64_df[bf_int64_df["int64_col"].notnull()]
    bf_result = bf_int64_df_filtered.applymap(remote_add_one).to_pandas()

    pd_int64_df = scalars_pandas_df[int64_cols]
    pd_int64_df_filtered = pd_int64_df[pd_int64_df["int64_col"].notnull()]
    pd_result = pd_int64_df_filtered.applymap(add_one)
    # TODO(shobs): Figure why pandas .applymap() changes the dtype, i.e.
    # pd_int64_df_filtered.dtype is Int64Dtype()
    # pd_int64_df_filtered.applymap(lambda x: x).dtype is int64.
    # For this test let's force the pandas dtype to be same as input.
    for col in pd_result:
        pd_result[col] = pd_result[col].astype(pd_int64_df_filtered[col].dtype)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.flaky(retries=2, delay=120)
def test_dataframe_applymap_na_ignore(
    session_with_bq_connection, scalars_dfs, dataset_id_permanent
):
    def add_one(x):
        return x + 1

    remote_add_one = session_with_bq_connection.remote_function(
        input_types=[int],
        output_type=int,
        dataset=dataset_id_permanent,
        name=get_function_name(add_one),
        cloud_function_service_account="default",
    )(add_one)

    scalars_df, scalars_pandas_df = scalars_dfs
    int64_cols = ["int64_col", "int64_too"]

    bf_int64_df = scalars_df[int64_cols]
    bf_result = bf_int64_df.applymap(remote_add_one, na_action="ignore").to_pandas()

    pd_int64_df = scalars_pandas_df[int64_cols]
    pd_result = pd_int64_df.applymap(add_one, na_action="ignore")
    # TODO(shobs): Figure why pandas .applymap() changes the dtype, i.e.
    # pd_int64_df_filtered.dtype is Int64Dtype()
    # pd_int64_df_filtered.applymap(lambda x: x).dtype is int64.
    # For this test let's force the pandas dtype to be same as input.
    for col in pd_result:
        pd_result[col] = pd_result[col].astype(pd_int64_df[col].dtype)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.flaky(retries=2, delay=120)
def test_series_map_bytes(
    session_with_bq_connection, scalars_dfs, dataset_id_permanent
):
    """Check that bytes is support as input and output."""
    scalars_df, scalars_pandas_df = scalars_dfs

    def bytes_to_hex(mybytes: bytes) -> bytes:
        import pandas

        return mybytes.hex().encode("utf-8") if pandas.notna(mybytes) else None  # type: ignore

    # TODO(b/345516010): the type: ignore is because "Optional" not yet
    # supported as a type annotation in @remote_function().
    assert bytes_to_hex(None) is None  # type: ignore
    assert bytes_to_hex(b"\x00\xdd\xba\x11") == b"00ddba11"
    pd_result = scalars_pandas_df.bytes_col.map(bytes_to_hex).astype(
        pd.ArrowDtype(pyarrow.binary())
    )

    packages = ["pandas"]
    remote_bytes_to_hex = session_with_bq_connection.remote_function(
        dataset=dataset_id_permanent,
        name=get_function_name(bytes_to_hex, package_requirements=packages),
        packages=packages,
        cloud_function_service_account="default",
    )(bytes_to_hex)
    bf_result = scalars_df.bytes_col.map(remote_bytes_to_hex).to_pandas()

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_skip_bq_connection_check(dataset_id_permanent):
    connection_name = "connection_does_not_exist"
    session = bigframes.Session(
        context=bigframes.BigQueryOptions(
            bq_connection=connection_name, skip_bq_connection_check=True
        )
    )

    # Make sure that the connection does not exist
    with pytest.raises(google.api_core.exceptions.NotFound):
        session.bqconnectionclient.get_connection(
            name=session.bqconnectionclient.connection_path(
                session._project, session._location, connection_name
            )
        )

    # Make sure that an attempt to create a remote function routine with
    # non-existent connection would result in an exception thrown by the BQ
    # service.
    # This is different from the exception throw by the BQ Connection service
    # if it was not able to create the connection because of lack of permission
    # when skip_bq_connection_check was not set to True:
    # google.api_core.exceptions.PermissionDenied: 403 Permission 'resourcemanager.projects.setIamPolicy' denied on resource
    with pytest.raises(
        google.api_core.exceptions.NotFound,
        match=f"Not found: Connection {connection_name}",
    ):

        def add_one(x):
            # Not expected to reach this code, as the connection doesn't exist.
            return x + 1  # pragma: NO COVER

        session.remote_function(
            input_types=[int],
            output_type=int,
            dataset=dataset_id_permanent,
            name=get_function_name(add_one),
            cloud_function_service_account="default",
        )(add_one)


def test_read_gbq_function_detects_invalid_function(session, dataset_id):
    dataset_ref = bigquery.DatasetReference.from_string(dataset_id)
    with pytest.raises(ValueError) as e:
        bff.read_gbq_function(
            str(dataset_ref.routine("not_a_function")),
            session=session,
        )

    assert "Unknown function" in str(e.value)


@pytest.mark.flaky(retries=2, delay=120)
def test_read_gbq_function_like_original(
    session,
    bigquery_client,
    bigqueryconnection_client,
    cloudfunctions_client,
    resourcemanager_client,
    scalars_df_index,
    dataset_id_permanent,
    bq_cf_connection,
):
    def square1(x):
        return x * x

    square1 = bff.remote_function(
        input_types=[int],
        output_type=int,
        bigquery_client=bigquery_client,
        bigquery_connection_client=bigqueryconnection_client,
        dataset=dataset_id_permanent,
        cloud_functions_client=cloudfunctions_client,
        resource_manager_client=resourcemanager_client,
        bigquery_connection=bq_cf_connection,
        reuse=True,
        name=get_function_name(square1),
        cloud_function_service_account="default",
    )(square1)

    # Function should still work normally.
    assert square1(2) == 4

    square2 = bff.read_gbq_function(
        function_name=square1.bigframes_bigquery_function,  # type: ignore
        session=session,
    )

    # The newly-created function (square1) should have a remote function AND a
    # cloud function associated with it, while the read-back version (square2)
    # should only have a remote function.
    assert square1.bigframes_remote_function  # type: ignore
    assert square1.bigframes_bigquery_function  # type: ignore
    assert square1.bigframes_cloud_function  # type: ignore

    assert square2.bigframes_remote_function
    assert square2.bigframes_bigquery_function
    assert square2.bigframes_cloud_function is None

    # They should point to the same function.
    assert square1.bigframes_remote_function == square2.bigframes_remote_function  # type: ignore
    assert square1.bigframes_bigquery_function == square2.bigframes_bigquery_function  # type: ignore
    assert square2.bigframes_remote_function == square2.bigframes_bigquery_function  # type: ignore

    # The result of applying them should be the same.
    int64_col = scalars_df_index["int64_col"]
    int64_col_filter = int64_col.notnull()
    int64_col_filtered = int64_col[int64_col_filter]

    s1_result_col = int64_col_filtered.apply(square1)
    s1_result = int64_col_filtered.to_frame().assign(result=s1_result_col)

    s2_result_col = int64_col_filtered.apply(square2)
    s2_result = int64_col_filtered.to_frame().assign(result=s2_result_col)

    assert_pandas_df_equal(s1_result.to_pandas(), s2_result.to_pandas())


def test_read_gbq_function_runs_existing_udf(session):
    func = session.read_gbq_function("bqutil.fn.cw_lower_case_ascii_only")
    got = func("AURÉLIE")
    assert got == "aurÉlie"


def test_read_gbq_function_runs_existing_udf_4_params(session):
    func = session.read_gbq_function("bqutil.fn.cw_instr4")
    got = func("TestStr123456Str", "Str", 1, 2)
    assert got == 14


def test_read_gbq_function_runs_existing_udf_array_output(session, routine_id_unique):
    bigframes.session._io.bigquery.start_query_with_client(
        session.bqclient,
        textwrap.dedent(
            f"""
                CREATE OR REPLACE FUNCTION `{routine_id_unique}`(x STRING)
                RETURNS ARRAY<STRING>
                AS (
                    [x, x]
                )
            """
        ),
        job_config=bigquery.QueryJobConfig(),
        location=None,
        project=None,
        timeout=None,
        metrics=None,
        query_with_job=True,
    )
    func = session.read_gbq_function(routine_id_unique)

    # Test on scalar value
    got = func("hello")
    assert got == ["hello", "hello"]

    # Test on a series, assert pandas parity
    pd_s = pd.Series(["alpha", "beta", "gamma"])
    bf_s = session.read_pandas(pd_s)
    pd_result = pd_s.apply(func)
    bf_result = bf_s.apply(func)
    assert bigframes.dtypes.is_array_string_like(bf_result.dtype)
    pd.testing.assert_series_equal(
        pd_result, bf_result.to_pandas(), check_dtype=False, check_index_type=False
    )


def test_read_gbq_function_runs_existing_udf_2_params_array_output(
    session, routine_id_unique
):
    bigframes.session._io.bigquery.start_query_with_client(
        session.bqclient,
        textwrap.dedent(
            f"""
                CREATE OR REPLACE FUNCTION `{routine_id_unique}`(x STRING, y STRING)
                RETURNS ARRAY<STRING>
                AS (
                    [x, y]
                )
            """
        ),
        job_config=bigquery.QueryJobConfig(),
        location=None,
        project=None,
        timeout=None,
        metrics=None,
        query_with_job=True,
    )
    func = session.read_gbq_function(routine_id_unique)

    # Test on scalar value
    got = func("hello", "world")
    assert got == ["hello", "world"]

    # Test on series, assert pandas parity
    pd_df = pd.DataFrame(
        {"col0": ["alpha", "beta", "gamma"], "col1": ["delta", "theta", "phi"]}
    )
    bf_df = session.read_pandas(pd_df)
    pd_result = pd_df["col0"].combine(pd_df["col1"], func)
    bf_result = bf_df["col0"].combine(bf_df["col1"], func)
    assert bigframes.dtypes.is_array_string_like(bf_result.dtype)
    pd.testing.assert_series_equal(
        pd_result, bf_result.to_pandas(), check_dtype=False, check_index_type=False
    )


def test_read_gbq_function_runs_existing_udf_4_params_array_output(
    session, routine_id_unique
):
    bigframes.session._io.bigquery.start_query_with_client(
        session.bqclient,
        textwrap.dedent(
            f"""
                CREATE OR REPLACE FUNCTION `{routine_id_unique}`(x STRING, y BOOL, z INT64, w FLOAT64)
                RETURNS ARRAY<STRING>
                AS (
                    [x, CAST(y AS STRING), CAST(z AS STRING), CAST(w AS STRING)]
                )
            """
        ),
        job_config=bigquery.QueryJobConfig(),
        location=None,
        project=None,
        timeout=None,
        metrics=None,
        query_with_job=True,
    )
    func = session.read_gbq_function(routine_id_unique)

    # Test on scalar value
    got = func("hello", True, 1, 2.3)
    assert got == ["hello", "true", "1", "2.3"]

    # Test on a dataframe, assert pandas parity
    pd_df = pd.DataFrame(
        {
            "col0": ["alpha", "beta", "gamma"],
            "col1": [True, False, True],
            "col2": [1, 2, 3],
            "col3": [4.5, 6, 7.75],
        }
    )
    bf_df = session.read_pandas(pd_df)
    # Simulate the result directly, since the function cannot be applied
    # directly on a pandas dataframe with axis=1, as this is a special type of
    # function with multiple params supported only on bigframes dataframe.
    pd_result = pd.Series(
        [
            ["alpha", "true", "1", "4.5"],
            ["beta", "false", "2", "6"],
            ["gamma", "true", "3", "7.75"],
        ]
    )
    bf_result = bf_df.apply(func, axis=1)
    assert bigframes.dtypes.is_array_string_like(bf_result.dtype)
    pd.testing.assert_series_equal(
        pd_result, bf_result.to_pandas(), check_dtype=False, check_index_type=False
    )


def test_read_gbq_function_reads_udfs(session, bigquery_client, dataset_id):
    dataset_ref = bigquery.DatasetReference.from_string(dataset_id)
    arg = bigquery.RoutineArgument(
        name="x",
        data_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
    )
    sql_routine = bigquery.Routine(
        dataset_ref.routine("square_sql"),
        body="x * x",
        arguments=[arg],
        return_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
        type_=bigquery.RoutineType.SCALAR_FUNCTION,
    )
    js_routine = bigquery.Routine(
        dataset_ref.routine("square_js"),
        body="return x * x",
        language="JAVASCRIPT",
        arguments=[arg],
        return_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
        type_=bigquery.RoutineType.SCALAR_FUNCTION,
    )

    for routine in (sql_routine, js_routine):
        # Create the routine in BigQuery and read it back using read_gbq_function.
        bigquery_client.create_routine(routine, exists_ok=True)
        square = bff.read_gbq_function(
            str(routine.reference),
            session=session,
        )

        # It should point to the named routine and yield the expected results.
        assert square.bigframes_bigquery_function == str(routine.reference)
        assert square.input_dtypes == (bigframes.dtypes.INT_DTYPE,)
        assert square.output_dtype == bigframes.dtypes.INT_DTYPE
        assert (
            square.bigframes_bigquery_function_output_dtype
            == bigframes.dtypes.INT_DTYPE
        )

        src = {"x": [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]}

        routine_ref_str = bff_utils.routine_ref_to_string_for_query(routine.reference)
        direct_sql = " UNION ALL ".join(
            [f"SELECT {x} AS x, {routine_ref_str}({x}) AS y" for x in src["x"]]
        )
        direct_df = bigquery_client.query(direct_sql).to_dataframe()

        indirect_df = bigframes.dataframe.DataFrame(src)
        indirect_df = indirect_df.assign(y=indirect_df.x.apply(square))
        converted_indirect_df = indirect_df.to_pandas()

        assert_pandas_df_equal(
            direct_df, converted_indirect_df, ignore_order=True, check_index_type=False
        )


def test_read_gbq_function_requires_explicit_types(
    session, bigquery_client, dataset_id
):
    dataset_ref = bigquery.DatasetReference.from_string(dataset_id)
    typed_arg = bigquery.RoutineArgument(
        name="x",
        data_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
    )
    untyped_arg = bigquery.RoutineArgument(
        name="x",
        kind="ANY_TYPE",  # With this kind, data_type not required for SQL functions.
    )

    both_types_specified = bigquery.Routine(
        dataset_ref.routine("both_types_specified"),
        body="x * x",
        arguments=[typed_arg],
        return_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
        type_=bigquery.RoutineType.SCALAR_FUNCTION,
    )
    only_return_type_specified = bigquery.Routine(
        dataset_ref.routine("only_return_type_specified"),
        body="x * x",
        arguments=[untyped_arg],
        return_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
        type_=bigquery.RoutineType.SCALAR_FUNCTION,
    )
    only_arg_type_specified = bigquery.Routine(
        dataset_ref.routine("only_arg_type_specified"),
        body="x * x",
        arguments=[typed_arg],
        type_=bigquery.RoutineType.SCALAR_FUNCTION,
    )
    neither_type_specified = bigquery.Routine(
        dataset_ref.routine("neither_type_specified"),
        body="x * x",
        arguments=[untyped_arg],
        type_=bigquery.RoutineType.SCALAR_FUNCTION,
    )

    bigquery_client.create_routine(both_types_specified, exists_ok=True)
    bigquery_client.create_routine(only_return_type_specified, exists_ok=True)
    bigquery_client.create_routine(only_arg_type_specified, exists_ok=True)
    bigquery_client.create_routine(neither_type_specified, exists_ok=True)

    bff.read_gbq_function(
        str(both_types_specified.reference),
        session=session,
    )
    with pytest.warns(
        bigframes.exceptions.UnknownDataTypeWarning,
        match=r"missing input data types[\s\S]*assume default data type",
    ):
        bff.read_gbq_function(
            str(only_return_type_specified.reference),
            session=session,
        )
    with pytest.raises(ValueError):
        bff.read_gbq_function(
            str(only_arg_type_specified.reference),
            session=session,
        )
    with pytest.raises(ValueError):
        bff.read_gbq_function(
            str(neither_type_specified.reference),
            session=session,
        )


@pytest.mark.parametrize(
    ("session_fixture",),
    [
        pytest.param("session"),
        pytest.param("unordered_session"),
    ],
)
@pytest.mark.parametrize(
    ("array_type", "expected_data"),
    [
        pytest.param(None, ["[1,2,3]", "[10,11,12]", "[100,101,102]"], id="None"),
        pytest.param(
            list[str],
            [["1", "2", "3"], ["10", "11", "12"], ["100", "101", "102"]],
            id="list-str",
        ),
        pytest.param(
            list[int], [[1, 2, 3], [10, 11, 12], [100, 101, 102]], id="list-int"
        ),
    ],
)
def test_read_gbq_function_respects_python_output_type(
    request, session_fixture, bigquery_client, dataset_id, array_type, expected_data
):
    session = request.getfixturevalue(session_fixture)
    dataset_ref = bigquery.DatasetReference.from_string(dataset_id)
    arg = bigquery.RoutineArgument(
        name="x",
        data_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
    )
    sql_routine = bigquery.Routine(
        dataset_ref.routine(_prefixer.create_prefix()),
        body="TO_JSON_STRING([x, x+1, x+2])",
        arguments=[arg],
        return_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.STRING),
        description=bff_utils.get_bigframes_metadata(python_output_type=array_type),
        type_=bigquery.RoutineType.SCALAR_FUNCTION,
    )

    # Create the routine in BigQuery and read it back using read_gbq_function.
    bigquery_client.create_routine(sql_routine, exists_ok=True)
    func = bff.read_gbq_function(str(sql_routine.reference), session=session)

    # test that the function works as expected
    s = bigframes.series.Series([1, 10, 100])
    expected = pd.Series(expected_data)
    actual = s.apply(func).to_pandas()

    # ignore type disparities, e.g. "int64" in pandas v/s "Int64" in bigframes
    pd.testing.assert_series_equal(
        expected, actual, check_dtype=False, check_index_type=False
    )


@pytest.mark.parametrize(
    ("array_type",),
    [
        pytest.param(list[bool], id="list-bool"),
        pytest.param(list[float], id="list-float"),
        pytest.param(list[int], id="list-int"),
        pytest.param(list[str], id="list-str"),
    ],
)
def test_read_gbq_function_supports_python_output_type_only_for_string_outputs(
    session, bigquery_client, dataset_id, array_type
):
    dataset_ref = bigquery.DatasetReference.from_string(dataset_id)
    arg = bigquery.RoutineArgument(
        name="x",
        data_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
    )
    sql_routine = bigquery.Routine(
        dataset_ref.routine(_prefixer.create_prefix()),
        body="x+1",
        arguments=[arg],
        return_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
        description=bff_utils.get_bigframes_metadata(python_output_type=array_type),
        type_=bigquery.RoutineType.SCALAR_FUNCTION,
    )

    # Create the routine in BigQuery and read it back using read_gbq_function.
    bigquery_client.create_routine(sql_routine, exists_ok=True)

    # reading back will fail because we currently allow specifying an explicit
    # output_type for BQ functions with STRING output
    with pytest.raises(
        TypeError,
        match="An explicit output_type should be provided only for a BigQuery function with STRING output.",
    ):
        bff.read_gbq_function(str(sql_routine.reference), session=session)


@pytest.mark.parametrize(
    ("array_type",),
    [
        pytest.param(list[bool], id="list-bool"),
        pytest.param(list[float], id="list-float"),
        pytest.param(list[int], id="list-int"),
        pytest.param(list[str], id="list-str"),
    ],
)
def test_read_gbq_function_supported_python_output_type(
    session, bigquery_client, dataset_id, array_type
):
    dataset_ref = bigquery.DatasetReference.from_string(dataset_id)
    arg = bigquery.RoutineArgument(
        name="x",
        data_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.INT64),
    )
    sql_routine = bigquery.Routine(
        dataset_ref.routine(_prefixer.create_prefix()),
        body="CAST(x AS STRING)",
        arguments=[arg],
        return_type=bigquery.StandardSqlDataType(bigquery.StandardSqlTypeNames.STRING),
        description=bff_utils.get_bigframes_metadata(python_output_type=array_type),
        type_=bigquery.RoutineType.SCALAR_FUNCTION,
    )

    # Create the routine in BigQuery and read it back using read_gbq_function.
    bigquery_client.create_routine(sql_routine, exists_ok=True)
    bff.read_gbq_function(str(sql_routine.reference), session=session)


@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_scalar_func(session, scalars_dfs):
    scalars_df, _ = scalars_dfs
    bdf = bigframes.pandas.DataFrame(
        {
            "Column1": scalars_df["string_col"],
            "Column2": scalars_df["string_col"],
        }
    )

    # The "cw_lower_case_ascii_only" is a scalar function.
    func_ref = session.read_gbq_function("bqutil.fn.cw_lower_case_ascii_only")

    # DataFrame '.apply()' only supports series level application.
    with pytest.raises(NotImplementedError) as context:
        bdf.apply(func_ref)
    assert str(context.value) == (
        "BigFrames DataFrame '.apply()' does not support BigFrames BigQuery "
        "function for column-wise (i.e. with axis=0) operations, please use a "
        "regular python function instead. For element-wise operations of the "
        "BigFrames BigQuery function, please use '.map()'. "
        f"{constants.FEEDBACK_LINK}"
    )


def test_read_gbq_function_multiple_inputs_not_a_row_processor(session):
    with pytest.raises(ValueError) as context:
        # The remote function has two args, which cannot be row processed. Throw
        # a ValueError for it.
        session.read_gbq_function(
            function_name="bqutil.fn.cw_regexp_instr_2",
            is_row_processor=True,
        )
    assert str(context.value) == (
        "A multi-input function cannot be a row processor. A row processor function "
        f"takes in a single input representing the row. {constants.FEEDBACK_LINK}"
    )


@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_axis_1(session, scalars_dfs, dataset_id_permanent):
    columns = [
        "bool_col",
        "int64_col",
        "int64_too",
        "float64_col",
        "string_col",
        "bytes_col",
    ]
    scalars_df, scalars_pandas_df = scalars_dfs

    def add_ints(row):
        return row["int64_col"] + row["int64_too"]

    with pytest.warns(
        bigframes.exceptions.PreviewWarning,
        match="input_types=Series is in preview.",
    ):
        add_ints_remote = session.remote_function(
            input_types=bigframes.series.Series,
            output_type=int,
            dataset=dataset_id_permanent,
            name=get_function_name(add_ints, is_row_processor=True),
            cloud_function_service_account="default",
        )(add_ints)
        assert add_ints_remote.bigframes_remote_function  # type: ignore
        assert add_ints_remote.bigframes_bigquery_function  # type: ignore
        assert add_ints_remote.bigframes_cloud_function  # type: ignore

    with pytest.warns(
        bigframes.exceptions.PreviewWarning, match="axis=1 scenario is in preview."
    ):
        bf_result = scalars_df[columns].apply(add_ints_remote, axis=1).to_pandas()

    pd_result = scalars_pandas_df[columns].apply(add_ints, axis=1)

    # bf_result.dtype is 'Int64' while pd_result.dtype is 'object', ignore this
    # mismatch by using check_dtype=False.
    #
    # bf_result.to_numpy() produces an array of numpy.float64's
    # (in system_prerelease tests), while pd_result.to_numpy() produces an
    # array of ints, ignore this mismatch by using check_exact=False.
    pd.testing.assert_series_equal(
        pd_result, bf_result, check_dtype=False, check_exact=False
    )

    # Read back the deployed BQ remote function using read_gbq_function.
    func_ref = session.read_gbq_function(
        function_name=add_ints_remote.bigframes_bigquery_function,  # type: ignore
        is_row_processor=True,
    )

    assert func_ref.bigframes_remote_function == add_ints_remote.bigframes_remote_function  # type: ignore
    assert func_ref.bigframes_bigquery_function == add_ints_remote.bigframes_bigquery_function  # type: ignore
    assert func_ref.bigframes_remote_function == func_ref.bigframes_bigquery_function  # type: ignore

    bf_result_gbq = scalars_df[columns].apply(func_ref, axis=1).to_pandas()
    pd.testing.assert_series_equal(
        pd_result, bf_result_gbq, check_dtype=False, check_exact=False
    )


@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_axis_1_ordering(session, scalars_dfs, dataset_id_permanent):
    columns = ["bool_col", "int64_col", "int64_too", "float64_col", "string_col"]
    ordering_columns = ["bool_col", "int64_col"]
    scalars_df, scalars_pandas_df = scalars_dfs

    def add_ints(row):
        return row["int64_col"] + row["int64_too"]

    add_ints_remote = session.remote_function(
        input_types=bigframes.series.Series,
        output_type=int,
        dataset=dataset_id_permanent,
        name=get_function_name(add_ints, is_row_processor=True),
        cloud_function_service_account="default",
    )(add_ints)

    bf_result = (
        scalars_df[columns]
        .sort_values(ordering_columns)
        .apply(add_ints_remote, axis=1)
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df[columns].sort_values(ordering_columns).apply(add_ints, axis=1)
    )

    # bf_result.dtype is 'Int64' while pd_result.dtype is 'object', ignore this
    # mismatch by using check_dtype=False.
    #
    # bf_result.to_numpy() produces an array of numpy.float64's
    # (in system_prerelease tests), while pd_result.to_numpy() produces an
    # array of ints, ignore this mismatch by using check_exact=False.
    pd.testing.assert_series_equal(
        pd_result, bf_result, check_dtype=False, check_exact=False
    )


@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_axis_1_multiindex(session, dataset_id_permanent):
    pd_df = pd.DataFrame(
        {"x": [1, 2, 3], "y": [1.5, 3.75, 5], "z": ["pq", "rs", "tu"]},
        index=pd.MultiIndex.from_tuples([("a", 100), ("a", 200), ("b", 300)]),
    )
    bf_df = session.read_pandas(pd_df)

    def add_numbers(row):
        return row["x"] + row["y"]

    add_numbers_remote = session.remote_function(
        input_types=bigframes.series.Series,
        output_type=float,
        dataset=dataset_id_permanent,
        name=get_function_name(add_numbers, is_row_processor=True),
        cloud_function_service_account="default",
    )(add_numbers)

    bf_result = bf_df.apply(add_numbers_remote, axis=1).to_pandas()
    pd_result = pd_df.apply(add_numbers, axis=1)

    # bf_result.dtype is 'Float64' while pd_result.dtype is 'float64', ignore this
    # mismatch by using check_dtype=False.
    #
    # bf_result.index[0].dtype is 'string[pyarrow]' while
    # pd_result.index[0].dtype is 'object', ignore this mismatch by using
    # check_index_type=False.
    pd.testing.assert_series_equal(
        pd_result, bf_result, check_dtype=False, check_index_type=False
    )


def test_df_apply_axis_1_unsupported_callable(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    columns = ["bool_col", "int64_col", "int64_too", "float64_col", "string_col"]

    def add_ints(row):
        return row["int64_col"] + row["int64_too"]

    # pandas works
    scalars_pandas_df.apply(add_ints, axis=1)

    with pytest.raises(
        ValueError, match="For axis=1 a BigFrames BigQuery function must be used."
    ):
        scalars_df[columns].apply(add_ints, axis=1)


@pytest.mark.flaky(retries=2, delay=120)
def test_df_apply_axis_1_unsupported_dtype(session, scalars_dfs, dataset_id_permanent):
    columns_with_not_supported_dtypes = [
        "date_col",
        "datetime_col",
        "geography_col",
        "numeric_col",
        "time_col",
        "timestamp_col",
    ]

    scalars_df, scalars_pandas_df = scalars_dfs

    def echo_len(row):
        return len(row)

    echo_len_remote = session.remote_function(
        input_types=bigframes.series.Series,
        output_type=float,
        dataset=dataset_id_permanent,
        name=get_function_name(echo_len, is_row_processor=True),
        cloud_function_service_account="default",
    )(echo_len)

    for column in columns_with_not_supported_dtypes:
        # pandas works
        scalars_pandas_df[[column]].apply(echo_len, axis=1)

        dtype = scalars_df[column].dtype

        with pytest.raises(
            NotImplementedError,
            match=re.escape(
                f"DataFrame has a column of dtype '{dtype}' which is not supported with axis=1. Supported dtypes are ("
            ),
        ), pytest.warns(
            bigframes.exceptions.PreviewWarning, match="axis=1 scenario is in preview."
        ):
            scalars_df[[column]].apply(echo_len_remote, axis=1)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_application_repr(session, dataset_id_permanent):
    # This function deliberately has a param with name "name", this is to test
    # a specific ibis' internal handling of object names
    def should_mask(name: str) -> bool:
        hash = 0
        for char_ in name:
            hash += ord(char_)
        return hash % 2 == 0

    assert "name" in inspect.signature(should_mask).parameters

    should_mask = session.remote_function(
        dataset=dataset_id_permanent,
        name=get_function_name(should_mask),
        cloud_function_service_account="default",
    )(should_mask)

    s = bigframes.series.Series(["Alice", "Bob", "Caroline"])

    repr(s.apply(should_mask))
    repr(s.where(s.apply(should_mask)))
    repr(s.where(~s.apply(should_mask)))
    repr(s.mask(should_mask))
    repr(s.mask(should_mask, "REDACTED"))


def test_read_gbq_function_application_repr(
    session, routine_id_unique, scalars_df_index
):
    # This function deliberately has a param with name "name", this is to test
    # a specific ibis' internal handling of object names
    session.bqclient.query_and_wait(
        f"CREATE OR REPLACE FUNCTION `{routine_id_unique}`(name STRING) RETURNS BOOL AS (MOD(LENGTH(name), 2) = 1)"
    )
    routine = session.bqclient.get_routine(routine_id_unique)
    assert "name" in [arg.name for arg in routine.arguments]

    # read the function and apply to dataframe
    should_mask = session.read_gbq_function(routine_id_unique)

    s = scalars_df_index["string_col"]

    repr(s.apply(should_mask))
    repr(s.where(s.apply(should_mask)))
    repr(s.where(~s.apply(should_mask)))
    repr(s.mask(should_mask))
    repr(s.mask(should_mask, "REDACTED"))


@pytest.mark.parametrize(
    ("method",),
    [
        pytest.param("apply"),
        pytest.param("map"),
        pytest.param("mask"),
    ],
)
@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_unary_applied_after_filter(
    session, dataset_id_permanent, scalars_dfs, method
):
    # This function is deliberately written to not work with NA input
    def is_odd(x: int) -> bool:
        return x % 2 == 1

    scalars_df, scalars_pandas_df = scalars_dfs
    int_col_name_with_nulls = "int64_col"

    # make sure there are NA values in the test column
    assert any([pd.isna(val) for val in scalars_df[int_col_name_with_nulls]])

    # create a remote function
    is_odd_remote = session.remote_function(
        dataset=dataset_id_permanent,
        name=get_function_name(is_odd),
        cloud_function_service_account="default",
    )(is_odd)

    # with nulls in the series the remote function application would fail
    with pytest.raises(
        google.api_core.exceptions.BadRequest, match="unsupported operand"
    ):
        bf_method = getattr(scalars_df[int_col_name_with_nulls], method)
        bf_method(is_odd_remote).to_pandas()

    # after filtering out nulls the remote function application should work
    # similar to pandas
    pd_method = getattr(
        scalars_pandas_df[scalars_pandas_df[int_col_name_with_nulls].notnull()][
            int_col_name_with_nulls
        ],
        method,
    )
    pd_result = pd_method(is_odd)
    bf_method = getattr(
        scalars_df[scalars_df[int_col_name_with_nulls].notnull()][
            int_col_name_with_nulls
        ],
        method,
    )
    bf_result = bf_method(is_odd_remote).to_pandas()

    # ignore any dtype difference
    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_binary_applied_after_filter(
    session, dataset_id_permanent, scalars_dfs
):
    # This function is deliberately written to not work with NA input
    def add(x: int, y: int) -> int:
        return x + y

    scalars_df, scalars_pandas_df = scalars_dfs
    int_col_name_with_nulls = "int64_col"
    int_col_name_no_nulls = "int64_too"
    bf_df = scalars_df[[int_col_name_with_nulls, int_col_name_no_nulls]]
    pd_df = scalars_pandas_df[[int_col_name_with_nulls, int_col_name_no_nulls]]

    # make sure there are NA values in the test column
    assert any([pd.isna(val) for val in bf_df[int_col_name_with_nulls]])

    # create a remote function
    add_remote = session.remote_function(
        dataset=dataset_id_permanent,
        name=get_function_name(add),
        cloud_function_service_account="default",
    )(add)

    # with nulls in the series the remote function application would fail
    with pytest.raises(
        google.api_core.exceptions.BadRequest, match="unsupported operand"
    ):
        bf_df[int_col_name_with_nulls].combine(
            bf_df[int_col_name_no_nulls], add_remote
        ).to_pandas()

    # after filtering out nulls the remote function application should work
    # similar to pandas
    pd_filter = pd_df[int_col_name_with_nulls].notnull()
    pd_result = pd_df[pd_filter][int_col_name_with_nulls].combine(
        pd_df[pd_filter][int_col_name_no_nulls], add
    )
    bf_filter = bf_df[int_col_name_with_nulls].notnull()
    bf_result = (
        bf_df[bf_filter][int_col_name_with_nulls]
        .combine(bf_df[bf_filter][int_col_name_no_nulls], add_remote)
        .to_pandas()
    )

    # ignore any dtype difference
    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_nary_applied_after_filter(
    session, dataset_id_permanent, scalars_dfs
):
    # This function is deliberately written to not work with NA input
    def add(x: int, y: int, z: float) -> float:
        return x + y + z

    scalars_df, scalars_pandas_df = scalars_dfs
    int_col_name_with_nulls = "int64_col"
    int_col_name_no_nulls = "int64_too"
    float_col_name_with_nulls = "float64_col"
    bf_df = scalars_df[
        [int_col_name_with_nulls, int_col_name_no_nulls, float_col_name_with_nulls]
    ]
    pd_df = scalars_pandas_df[
        [int_col_name_with_nulls, int_col_name_no_nulls, float_col_name_with_nulls]
    ]

    # make sure there are NA values in the test columns
    assert any([pd.isna(val) for val in bf_df[int_col_name_with_nulls]])
    assert any([pd.isna(val) for val in bf_df[float_col_name_with_nulls]])

    # create a remote function
    add_remote = session.remote_function(
        dataset=dataset_id_permanent,
        name=get_function_name(add),
        cloud_function_service_account="default",
    )(add)

    # pandas does not support nary functions, so let's create a proxy function
    # for testing purpose that takes a series and in turn calls the naray function
    def add_pandas(s: pd.Series) -> float:
        return add(
            s[int_col_name_with_nulls],
            s[int_col_name_no_nulls],
            s[float_col_name_with_nulls],
        )

    # with nulls in the series the remote function application would fail
    with pytest.raises(
        google.api_core.exceptions.BadRequest, match="unsupported operand"
    ):
        bf_df.apply(add_remote, axis=1).to_pandas()

    # after filtering out nulls the remote function application should work
    # similar to pandas
    pd_filter = (
        pd_df[int_col_name_with_nulls].notnull()
        & pd_df[float_col_name_with_nulls].notnull()
    )
    pd_result = pd_df[pd_filter].apply(add_pandas, axis=1)
    bf_filter = (
        bf_df[int_col_name_with_nulls].notnull()
        & bf_df[float_col_name_with_nulls].notnull()
    )
    bf_result = bf_df[bf_filter].apply(add_remote, axis=1).to_pandas()

    # ignore any dtype difference
    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("method",),
    [
        pytest.param("apply"),
        pytest.param("map"),
        pytest.param("mask"),
    ],
)
def test_remote_function_unary_partial_ordering_mode_assign(
    unordered_session, dataset_id_permanent, method
):
    df = unordered_session.read_gbq("bigquery-public-data.baseball.schedules")[
        ["duration_minutes"]
    ]

    def is_long_duration(minutes: int) -> bool:
        return minutes >= 120

    is_long_duration = unordered_session.remote_function(
        dataset=dataset_id_permanent,
        name=get_function_name(is_long_duration),
        cloud_function_service_account="default",
    )(is_long_duration)

    method = getattr(df["duration_minutes"], method)

    df1 = df.assign(duration_meta=method(is_long_duration))
    repr(df1)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_binary_partial_ordering_mode_assign(
    unordered_session, dataset_id_permanent, scalars_df_index
):
    def combiner(x: int, y: int) -> int:
        if x is None:
            return y
        return x

    combiner = unordered_session.remote_function(
        dataset=dataset_id_permanent,
        name=get_function_name(combiner),
        cloud_function_service_account="default",
    )(combiner)

    df = scalars_df_index[["int64_col", "int64_too", "float64_col", "string_col"]]
    df1 = df.assign(int64_combined=df["int64_col"].combine(df["int64_too"], combiner))
    repr(df1)


@pytest.mark.flaky(retries=2, delay=120)
def test_remote_function_nary_partial_ordering_mode_assign(
    unordered_session, dataset_id_permanent, scalars_df_index
):
    def processor(x: int, y: int, z: float, w: str) -> str:
        return f"I got x={x}, y={y}, z={z} and w={w}"

    processor = unordered_session.remote_function(
        dataset=dataset_id_permanent,
        name=get_function_name(processor),
        cloud_function_service_account="default",
    )(processor)

    df = scalars_df_index[["int64_col", "int64_too", "float64_col", "string_col"]]
    df1 = df.assign(combined=df.apply(processor, axis=1))
    repr(df1)
