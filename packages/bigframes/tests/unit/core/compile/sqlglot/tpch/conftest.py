# Copyright 2026 Google LLC
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

import datetime
import functools
import unittest.mock as mock

import pytest
from google.cloud import bigquery

import bigframes.testing.mocks as mocks
from bigframes.testing import compiler_session

freezegun = pytest.importorskip("freezegun")

PROJECT_NAME = "bigframes-dev-perf"
DATASET_NAME = "tpch_0001t"
LOCATION_NAME = "test-region"

TPCH_SCHEMAS = {
    "LINEITEM": [
        bigquery.SchemaField("L_ORDERKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("L_PARTKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("L_SUPPKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("L_LINENUMBER", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("L_QUANTITY", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("L_EXTENDEDPRICE", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("L_DISCOUNT", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("L_TAX", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("L_RETURNFLAG", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("L_LINESTATUS", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("L_SHIPDATE", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("L_COMMITDATE", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("L_RECEIPTDATE", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("L_SHIPINSTRUCT", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("L_SHIPMODE", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("L_COMMENT", "STRING"),
    ],
    "ORDERS": [
        bigquery.SchemaField("O_ORDERKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("O_CUSTKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("O_ORDERSTATUS", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("O_TOTALPRICE", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("O_ORDERDATE", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("O_ORDERPRIORITY", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("O_CLERK", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("O_SHIPPRIORITY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("O_COMMENT", "STRING"),
    ],
    "PART": [
        bigquery.SchemaField("P_PARTKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("P_NAME", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("P_MFGR", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("P_BRAND", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("P_TYPE", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("P_SIZE", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("P_CONTAINER", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("P_RETAILPRICE", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("P_COMMENT", "STRING"),
    ],
    "SUPPLIER": [
        bigquery.SchemaField("S_SUPPKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("S_NAME", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("S_ADDRESS", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("S_NATIONKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("S_PHONE", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("S_ACCTBAL", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("S_COMMENT", "STRING"),
    ],
    "PARTSUPP": [
        bigquery.SchemaField("PS_PARTKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("PS_SUPPKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("PS_AVAILQTY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("PS_SUPPLYCOST", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("PS_COMMENT", "STRING"),
    ],
    "CUSTOMER": [
        bigquery.SchemaField("C_CUSTKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("C_NAME", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("C_ADDRESS", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("C_NATIONKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("C_PHONE", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("C_ACCTBAL", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("C_MKTSEGMENT", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("C_COMMENT", "STRING"),
    ],
    "NATION": [
        bigquery.SchemaField("N_NATIONKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("N_NAME", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("N_REGIONKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("N_COMMENT", "STRING"),
    ],
    "REGION": [
        bigquery.SchemaField("R_REGIONKEY", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("R_NAME", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("R_COMMENT", "STRING"),
    ],
}


def _create_mock_bqclient():
    """Helper function to create a compiler session."""

    bqclient = mock.create_autospec(bigquery.Client, instance=True)
    bqclient.project = DATASET_NAME
    bqclient.location = LOCATION_NAME
    table_create_time = datetime.datetime.now()

    def get_table_mock(table_ref):
        if isinstance(table_ref, str):
            table_ref = bigquery.TableReference.from_string(table_ref)

        table_id = table_ref.table_id
        schema = TPCH_SCHEMAS.get(table_id, [])

        table = mock.create_autospec(bigquery.Table, instance=True)
        table._properties = {}
        type(table).created = mock.PropertyMock(return_value=table_create_time)
        type(table).location = mock.PropertyMock(return_value=LOCATION_NAME)
        type(table).schema = mock.PropertyMock(return_value=schema)
        type(table).project = table_ref.project
        type(table).dataset_id = table_ref.dataset_id
        type(table).table_id = table_id
        type(table).num_rows = mock.PropertyMock(return_value=1000000000)
        return table

    bqclient.get_table.side_effect = get_table_mock
    return bqclient


@pytest.fixture(scope="session")
def tpch_session():
    anonymous_dataset = bigquery.DatasetReference.from_string(
        f"{PROJECT_NAME}.{DATASET_NAME}"
    )
    session = mocks.create_bigquery_session(
        bqclient=_create_mock_bqclient(),
        anonymous_dataset=anonymous_dataset,
    )

    # Disable snapshotting for TPC-H tests to keep snapshots clean
    original_read_gbq_table = session._loader.read_gbq_table

    @functools.wraps(original_read_gbq_table)
    def read_gbq_table_no_snapshot(*args, **kwargs):
        kwargs["enable_snapshot"] = False
        return original_read_gbq_table(*args, **kwargs)

    session._loader.read_gbq_table = read_gbq_table_no_snapshot

    session._executor = compiler_session.SQLCompilerExecutor()
    return session
