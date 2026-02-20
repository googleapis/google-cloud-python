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

import os
import re

from google.cloud import bigquery
import pandas as pd
import pytest

TPCH_PATH = "third_party/bigframes_vendored/tpch"
PROJECT_ID = "bigframes-dev-perf"
DATASET_ID = "tpch_0001g"
DATASET = {
    "line_item_ds": f"{PROJECT_ID}.{DATASET_ID}.LINEITEM",
    "region_ds": f"{PROJECT_ID}.{DATASET_ID}.REGION",
    "nation_ds": f"{PROJECT_ID}.{DATASET_ID}.NATION",
    "supplier_ds": f"{PROJECT_ID}.{DATASET_ID}.SUPPLIER",
    "part_ds": f"{PROJECT_ID}.{DATASET_ID}.PART",
    "part_supp_ds": f"{PROJECT_ID}.{DATASET_ID}.PARTSUPP",
    "customer_ds": f"{PROJECT_ID}.{DATASET_ID}.CUSTOMER",
    "orders_ds": f"{PROJECT_ID}.{DATASET_ID}.ORDERS",
}


def _execute_sql_query(bigquery_client, sql_query):
    sql_query = sql_query.format(**DATASET)

    job_config = bigquery.QueryJobConfig(use_query_cache=False)
    query_job = bigquery_client.query(sql_query, job_config=job_config)
    query_job.result()
    df = query_job.to_dataframe()
    df.columns = df.columns.str.upper()
    return df


def _execute_bigframes_script(session, bigframes_script):
    bigframes_script = re.sub(
        r"next\((\w+)\.to_pandas_batches\((.*?)\)\)",
        r"return \1.to_pandas()",
        bigframes_script,
    )
    bigframes_script = re.sub(r"_\s*=\s*(\w+)", r"return \1", bigframes_script)

    bigframes_script = (
        bigframes_script
        + f"\nresult = q('{PROJECT_ID}', '{DATASET_ID}', _initialize_session)"
    )
    exec_globals = {"_initialize_session": session}
    exec(bigframes_script, exec_globals)
    bigframes_result = exec_globals.get("result")
    return bigframes_result


def _verify_result(bigframes_result, sql_result):
    if isinstance(bigframes_result, pd.DataFrame):
        pd.testing.assert_frame_equal(
            sql_result.reset_index(drop=True),
            bigframes_result.reset_index(drop=True),
            check_dtype=False,
        )
    else:
        assert sql_result.shape == (1, 1)
        sql_scalar = sql_result.iloc[0, 0]
        assert sql_scalar == bigframes_result


@pytest.mark.parametrize("query_num", range(1, 23))
@pytest.mark.parametrize("ordered", [True, False])
def test_tpch_correctness(session, unordered_session, query_num, ordered):
    """Runs verification of TPCH benchmark script outputs to ensure correctness."""
    # Execute SQL:
    sql_file_path = f"{TPCH_PATH}/sql_queries/q{query_num}.sql"
    assert os.path.exists(sql_file_path)
    with open(sql_file_path, "r") as f:
        sql_query = f.read()

    sql_result = _execute_sql_query(session.bqclient, sql_query)

    # Execute BigFrames:
    file_path = f"{TPCH_PATH}/queries/q{query_num}.py"
    assert os.path.exists(file_path)
    with open(file_path, "r") as file:
        bigframes_script = file.read()

    bigframes_result = _execute_bigframes_script(
        session if ordered else unordered_session, bigframes_script
    )

    _verify_result(bigframes_result, sql_result)
