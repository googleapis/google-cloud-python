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
import unittest.mock as mock

from google.cloud import bigquery
import pytest

import bigframes.testing.mocks as mocks

freezegun = pytest.importorskip("freezegun")

TPCH_SCHEMAS = {
    "LINEITEM": [
        bigquery.SchemaField("L_ORDERKEY", "INTEGER"),
        bigquery.SchemaField("L_PARTKEY", "INTEGER"),
        bigquery.SchemaField("L_SUPPKEY", "INTEGER"),
        bigquery.SchemaField("L_LINENUMBER", "INTEGER"),
        bigquery.SchemaField("L_QUANTITY", "FLOAT"),
        bigquery.SchemaField("L_EXTENDEDPRICE", "FLOAT"),
        bigquery.SchemaField("L_DISCOUNT", "FLOAT"),
        bigquery.SchemaField("L_TAX", "FLOAT"),
        bigquery.SchemaField("L_RETURNFLAG", "STRING"),
        bigquery.SchemaField("L_LINESTATUS", "STRING"),
        bigquery.SchemaField("L_SHIPDATE", "DATE"),
        bigquery.SchemaField("L_COMMITDATE", "DATE"),
        bigquery.SchemaField("L_RECEIPTDATE", "DATE"),
        bigquery.SchemaField("L_SHIPINSTRUCT", "STRING"),
        bigquery.SchemaField("L_SHIPMODE", "STRING"),
        bigquery.SchemaField("L_COMMENT", "STRING"),
    ],
    "ORDERS": [
        bigquery.SchemaField("O_ORDERKEY", "INTEGER"),
        bigquery.SchemaField("O_CUSTKEY", "INTEGER"),
        bigquery.SchemaField("O_ORDERSTATUS", "STRING"),
        bigquery.SchemaField("O_TOTALPRICE", "FLOAT"),
        bigquery.SchemaField("O_ORDERDATE", "DATE"),
        bigquery.SchemaField("O_ORDERPRIORITY", "STRING"),
        bigquery.SchemaField("O_CLERK", "STRING"),
        bigquery.SchemaField("O_SHIPPRIORITY", "INTEGER"),
        bigquery.SchemaField("O_COMMENT", "STRING"),
    ],
    "PART": [
        bigquery.SchemaField("P_PARTKEY", "INTEGER"),
        bigquery.SchemaField("P_NAME", "STRING"),
        bigquery.SchemaField("P_MFGR", "STRING"),
        bigquery.SchemaField("P_BRAND", "STRING"),
        bigquery.SchemaField("P_TYPE", "STRING"),
        bigquery.SchemaField("P_SIZE", "INTEGER"),
        bigquery.SchemaField("P_CONTAINER", "STRING"),
        bigquery.SchemaField("P_RETAILPRICE", "FLOAT"),
        bigquery.SchemaField("P_COMMENT", "STRING"),
    ],
    "SUPPLIER": [
        bigquery.SchemaField("S_SUPPKEY", "INTEGER"),
        bigquery.SchemaField("S_NAME", "STRING"),
        bigquery.SchemaField("S_ADDRESS", "STRING"),
        bigquery.SchemaField("S_NATIONKEY", "INTEGER"),
        bigquery.SchemaField("S_PHONE", "STRING"),
        bigquery.SchemaField("S_ACCTBAL", "FLOAT"),
        bigquery.SchemaField("S_COMMENT", "STRING"),
    ],
    "PARTSUPP": [
        bigquery.SchemaField("PS_PARTKEY", "INTEGER"),
        bigquery.SchemaField("PS_SUPPKEY", "INTEGER"),
        bigquery.SchemaField("PS_AVAILQTY", "INTEGER"),
        bigquery.SchemaField("PS_SUPPLYCOST", "FLOAT"),
        bigquery.SchemaField("PS_COMMENT", "STRING"),
    ],
    "CUSTOMER": [
        bigquery.SchemaField("C_CUSTKEY", "INTEGER"),
        bigquery.SchemaField("C_NAME", "STRING"),
        bigquery.SchemaField("C_ADDRESS", "STRING"),
        bigquery.SchemaField("C_NATIONKEY", "INTEGER"),
        bigquery.SchemaField("C_PHONE", "STRING"),
        bigquery.SchemaField("C_ACCTBAL", "FLOAT"),
        bigquery.SchemaField("C_MKTSEGMENT", "STRING"),
        bigquery.SchemaField("C_COMMENT", "STRING"),
    ],
    "NATION": [
        bigquery.SchemaField("N_NATIONKEY", "INTEGER"),
        bigquery.SchemaField("N_NAME", "STRING"),
        bigquery.SchemaField("N_REGIONKEY", "INTEGER"),
        bigquery.SchemaField("N_COMMENT", "STRING"),
    ],
    "REGION": [
        bigquery.SchemaField("R_REGIONKEY", "INTEGER"),
        bigquery.SchemaField("R_NAME", "STRING"),
        bigquery.SchemaField("R_COMMENT", "STRING"),
    ],
}


@pytest.fixture(scope="session")
def tpch_session():
    from bigframes.testing import compiler_session

    anonymous_dataset = bigquery.DatasetReference.from_string("bigframes-dev.tpch")
    location = "us-central1"

    with freezegun.freeze_time("2026-03-10 18:00:00"):
        session = mocks.create_bigquery_session(
            anonymous_dataset=anonymous_dataset,
            location=location,
        )

        def get_table_mock(table_ref):
            if isinstance(table_ref, str):
                table_ref = bigquery.TableReference.from_string(table_ref)

            table_id = table_ref.table_id
            schema = TPCH_SCHEMAS.get(table_id, [])

            table = mock.create_autospec(bigquery.Table, instance=True)
            table._properties = {}
            # mocks.create_bigquery_session's CURRENT_TIMESTAMP() returns offset-naive datetime.now()
            # So we should also use offset-naive here to avoid comparison errors.
            now = datetime.datetime.now()
            type(table).schema = mock.PropertyMock(return_value=schema)
            type(table).project = table_ref.project
            type(table).dataset_id = table_ref.dataset_id
            type(table).table_id = table_id
            type(table).num_rows = mock.PropertyMock(return_value=1000000)
            type(table).num_bytes = mock.PropertyMock(return_value=1000000)
            type(table).location = mock.PropertyMock(return_value=location)
            type(table).table_type = mock.PropertyMock(return_value="TABLE")
            type(table).created = mock.PropertyMock(return_value=now)
            type(table).modified = mock.PropertyMock(return_value=now)
            type(table).range_partitioning = mock.PropertyMock(return_value=None)
            type(table).time_partitioning = mock.PropertyMock(return_value=None)
            type(table).clustering_fields = mock.PropertyMock(return_value=None)
            return table

        session.bqclient.get_table.side_effect = get_table_mock
        session._executor = compiler_session.SQLCompilerExecutor()
        return session
