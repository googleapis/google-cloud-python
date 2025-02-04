# Copyright 2024 Google LLC
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

import argparse
import os
import re

from google.cloud import bigquery
import pandas as pd
from tqdm import tqdm

import bigframes

project_id = "bigframes-dev-perf"
dataset_id = "tpch_0001g"
dataset = {
    "line_item_ds": f"bigframes-dev-perf.{dataset_id}.LINEITEM",
    "region_ds": f"bigframes-dev-perf.{dataset_id}.REGION",
    "nation_ds": f"bigframes-dev-perf.{dataset_id}.NATION",
    "supplier_ds": f"bigframes-dev-perf.{dataset_id}.SUPPLIER",
    "part_ds": f"bigframes-dev-perf.{dataset_id}.PART",
    "part_supp_ds": f"bigframes-dev-perf.{dataset_id}.PARTSUPP",
    "customer_ds": f"bigframes-dev-perf.{dataset_id}.CUSTOMER",
    "orders_ds": f"bigframes-dev-perf.{dataset_id}.ORDERS",
}


def _execute_query(query):
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig(use_query_cache=False)
    query_job = client.query(query, job_config=job_config)
    query_job.result()
    df = query_job.to_dataframe()
    df.columns = df.columns.str.upper()
    return df


def _initialize_session(ordered: bool):
    context = bigframes.BigQueryOptions(
        location="US", ordering_mode="strict" if ordered else "partial"
    )
    session = bigframes.Session(context=context)
    return session


def _verify_result(bigframes_query, sql_result):
    exec_globals = {"_initialize_session": _initialize_session}
    exec(bigframes_query, exec_globals)
    bigframes_result = exec_globals.get("result")
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


def verify(query_num=None):
    range_iter = range(1, 23) if query_num is None else [query_num]
    for i in tqdm(range_iter, desc="Processing queries"):
        if query_num is not None and i != query_num:
            continue

        # Execute SQL:
        sql_file_path = f"third_party/bigframes_vendored/tpch/sql_queries/q{i}.sql"
        with open(sql_file_path, "r") as f:
            sql_query = f.read()
            sql_query = sql_query.format(**dataset)
        file_path = f"third_party/bigframes_vendored/tpch/queries/q{i}.py"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                file_content = file.read()

                file_content = re.sub(
                    r"next\((\w+)\.to_pandas_batches\((.*?)\)\)",
                    r"return \1.to_pandas()",
                    file_content,
                )
                file_content = re.sub(r"_\s*=\s*(\w+)", r"return \1", file_content)
                sql_result = _execute_query(sql_query)

                print(f"Checking {file_path} in ordered session")
                bigframes_query = (
                    file_content
                    + f"\nresult = q('{project_id}', '{dataset_id}', _initialize_session(ordered=True))"
                )
                _verify_result(bigframes_query, sql_result)

                print(f"Checking {file_path} in unordered session")
                bigframes_query = (
                    file_content
                    + f"\nresult = q('{project_id}', '{dataset_id}', _initialize_session(ordered=False))"
                )
                _verify_result(bigframes_query, sql_result)

        else:
            raise FileNotFoundError(f"File {file_path} not found.")


if __name__ == "__main__":
    """
    Runs verification of TPCH benchmark script outputs to ensure correctness for a specified query or all queries
    with 1GB dataset.

    Example:
        python scripts/tpch_result_verify.py -q 15  # Verifies TPCH query number 15
        python scripts/tpch_result_verify.py       # Verifies all TPCH queries from 1 to 22
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query_number", type=int, default=None)
    args = parser.parse_args()

    verify(args.query_number)
