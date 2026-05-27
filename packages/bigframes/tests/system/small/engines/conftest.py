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
import pathlib
from typing import Generator

import google.cloud.bigquery_storage_v1
import pandas as pd
import pytest
from google.cloud import bigquery

import bigframes
from bigframes.core import ArrayValue, events, local_data
from bigframes.session import (
    direct_gbq_execution,
    local_scan_executor,
    polars_executor,
    semi_executor,
)

CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent.parent.parent / "data"


@pytest.fixture(scope="module")
def fake_session() -> Generator[bigframes.Session, None, None]:
    import bigframes.core.global_session

    # its a "polars session", but we are bypassing session-provided execution
    # we just want a minimal placeholder session without expensive setup
    from bigframes.testing import polars_session

    session = polars_session.TestSession()
    with bigframes.core.global_session._GlobalSessionContext(session):
        yield session


@pytest.fixture(scope="session")
def pyarrow_engine():
    return local_scan_executor.LocalScanExecutor()


@pytest.fixture(scope="session")
def polars_engine():
    return polars_executor.PolarsExecutor()


@pytest.fixture(scope="session")
def bq_engine(
    bigquery_client: bigquery.Client,
    bigquery_storage_read_client: google.cloud.bigquery_storage_v1.BigQueryReadClient,
):
    return direct_gbq_execution.DirectGbqExecutor(
        bigquery_client,
        bqstoragereadclient=bigquery_storage_read_client,
        publisher=events.Publisher(),
        compiler="ibis",
    )


@pytest.fixture(scope="session")
def sqlglot_engine(
    bigquery_client: bigquery.Client,
    bigquery_storage_read_client: google.cloud.bigquery_storage_v1.BigQueryReadClient,
) -> semi_executor.SemiExecutor:
    return direct_gbq_execution.DirectGbqExecutor(
        bigquery_client,
        bqstoragereadclient=bigquery_storage_read_client,
        publisher=events.Publisher(),
    )


@pytest.fixture(scope="session", params=["pyarrow", "polars", "bq", "bq-sqlglot"])
def engine(
    request, pyarrow_engine, polars_engine, bq_engine, sqlglot_engine
) -> semi_executor.SemiExecutor:
    if request.param == "pyarrow":
        return pyarrow_engine
    if request.param == "polars":
        return polars_engine
    if request.param == "bq":
        return bq_engine
    if request.param == "bq-sqlglot":
        return sqlglot_engine
    raise ValueError(f"Unrecognized param: {request.param}")


@pytest.fixture(scope="module")
def managed_data_source(
    scalars_pandas_df_index: pd.DataFrame,
) -> local_data.ManagedArrowTable:
    return local_data.ManagedArrowTable.from_pandas(scalars_pandas_df_index)


@pytest.fixture(scope="module")
def scalars_array_value(
    managed_data_source: local_data.ManagedArrowTable, fake_session: bigframes.Session
):
    return ArrayValue.from_managed(managed_data_source, fake_session)


@pytest.fixture(scope="module")
def zero_row_source() -> local_data.ManagedArrowTable:
    return local_data.ManagedArrowTable.from_pandas(pd.DataFrame({"a": [], "b": []}))


@pytest.fixture(scope="module")
def nested_data_source(
    nested_pandas_df: pd.DataFrame,
) -> local_data.ManagedArrowTable:
    return local_data.ManagedArrowTable.from_pandas(nested_pandas_df)


@pytest.fixture(scope="module")
def repeated_data_source(
    repeated_pandas_df: pd.DataFrame,
) -> local_data.ManagedArrowTable:
    return local_data.ManagedArrowTable.from_pandas(repeated_pandas_df)


@pytest.fixture(scope="module")
def arrays_array_value(
    repeated_data_source: local_data.ManagedArrowTable, fake_session: bigframes.Session
):
    return ArrayValue.from_managed(repeated_data_source, fake_session)
