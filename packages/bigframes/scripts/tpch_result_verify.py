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
line_item_ds = f"bigframes-dev-perf.{dataset_id}.LINEITEM"
region_ds = f"bigframes-dev-perf.{dataset_id}.REGION"
nation_ds = f"bigframes-dev-perf.{dataset_id}.NATION"
supplier_ds = f"bigframes-dev-perf.{dataset_id}.SUPPLIER"
part_ds = f"bigframes-dev-perf.{dataset_id}.PART"
part_supp_ds = f"bigframes-dev-perf.{dataset_id}.PARTSUPP"
customer_ds = f"bigframes-dev-perf.{dataset_id}.CUSTOMER"
orders_ds = f"bigframes-dev-perf.{dataset_id}.ORDERS"

q1_query = f"""
    select
        l_returnflag,
        l_linestatus,
        sum(l_quantity) as sum_qty,
        sum(l_extendedprice) as sum_base_price,
        sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
        sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
        avg(l_quantity) as avg_qty,
        avg(l_extendedprice) as avg_price,
        avg(l_discount) as avg_disc,
        count(*) as count_order
    from
        {line_item_ds}
    where
        l_shipdate <= '1998-09-02'
    group by
        l_returnflag,
        l_linestatus
    order by
        l_returnflag,
        l_linestatus
"""

q2_query = f"""
    select
        s_acctbal,
        s_name,
        n_name,
        p_partkey,
        p_mfgr,
        s_address,
        s_phone,
        s_comment
    from
        {part_ds},
        {supplier_ds},
        {part_supp_ds},
        {nation_ds},
        {region_ds}
    where
        p_partkey = ps_partkey
        and s_suppkey = ps_suppkey
        and p_size = 15
        and p_type like '%BRASS'
        and s_nationkey = n_nationkey
        and n_regionkey = r_regionkey
        and r_name = 'EUROPE'
        and ps_supplycost = (
            select
                min(ps_supplycost)
            from
                {part_supp_ds},
                {supplier_ds},
                {nation_ds},
                {region_ds}
            where
                p_partkey = ps_partkey
                and s_suppkey = ps_suppkey
                and s_nationkey = n_nationkey
                and n_regionkey = r_regionkey
                and r_name = 'EUROPE'
        )
    order by
        s_acctbal desc,
        n_name,
        s_name,
        p_partkey
    limit 100
"""

q3_query = f"""
    select
        l_orderkey,
        sum(l_extendedprice * (1 - l_discount)) as revenue,
        o_orderdate,
        o_shippriority
    from
        {customer_ds},
        {orders_ds},
        {line_item_ds}
    where
        c_mktsegment = 'BUILDING'
        and c_custkey = o_custkey
        and l_orderkey = o_orderkey
        and o_orderdate < '1995-03-15'
        and l_shipdate > '1995-03-15'
    group by
        l_orderkey,
        o_orderdate,
        o_shippriority
    order by
        revenue desc,
        o_orderdate
    limit 10
"""

q4_query = f"""
    select
        o_orderpriority,
        count(*) as order_count
    from
        {orders_ds}
    where
        o_orderdate >= date '1993-07-01'
        and o_orderdate < date '1993-10-01'
        and exists (
            select
                *
            from
                {line_item_ds}
            where
                l_orderkey = o_orderkey
                and l_commitdate < l_receiptdate
        )
    group by
        o_orderpriority
    order by
        o_orderpriority
"""

q5_query = f"""
    select
        n_name,
        sum(l_extendedprice * (1 - l_discount)) as revenue
    from
        {customer_ds},
        {orders_ds},
        {line_item_ds},
        {supplier_ds},
        {nation_ds},
        {region_ds}
    where
        c_custkey = o_custkey
        and l_orderkey = o_orderkey
        and l_suppkey = s_suppkey
        and c_nationkey = s_nationkey
        and s_nationkey = n_nationkey
        and n_regionkey = r_regionkey
        and r_name = 'ASIA'
        and o_orderdate >= date '1994-01-01'
        and o_orderdate < date '1995-01-01'
    group by
        n_name
    order by
        revenue desc
"""

q6_query = f"""
    select
        sum(l_extendedprice * l_discount) as revenue
    from
        {line_item_ds}
    where
        l_shipdate >= date '1994-01-01'
        and l_shipdate < date '1994-01-01' + interval '1' year
        and l_discount between .05 and .07
        and l_quantity < 24
"""

q7_query = f"""
    select
        supp_nation,
        cust_nation,
        l_year,
        sum(volume) as revenue
    from
        (
            select
                n1.n_name as supp_nation,
                n2.n_name as cust_nation,
                EXTRACT(YEAR FROM l_shipdate) as l_year,
                l_extendedprice * (1 - l_discount) as volume
            from
                {supplier_ds},
                {line_item_ds},
                {orders_ds},
                {customer_ds},
                {nation_ds} n1,
                {nation_ds} n2
            where
                s_suppkey = l_suppkey
                and o_orderkey = l_orderkey
                and c_custkey = o_custkey
                and s_nationkey = n1.n_nationkey
                and c_nationkey = n2.n_nationkey
                and (
                    (n1.n_name = 'FRANCE' and n2.n_name = 'GERMANY')
                    or (n1.n_name = 'GERMANY' and n2.n_name = 'FRANCE')
                )
                and l_shipdate between date '1995-01-01' and date '1996-12-31'
        ) as shipping
    group by
        supp_nation,
        cust_nation,
        l_year
    order by
        supp_nation,
        cust_nation,
        l_year
"""

q8_query = f"""
    select
        o_year,
        round(
            sum(case
                when nation = 'BRAZIL' then volume
                else 0
            end) / sum(volume)
        , 2) as mkt_share
    from
        (
            select
                extract(year from o_orderdate) as o_year,
                l_extendedprice * (1 - l_discount) as volume,
                n2.n_name as nation
            from
                {part_ds},
                {supplier_ds},
                {line_item_ds},
                {orders_ds},
                {customer_ds},
                {nation_ds} n1,
                {nation_ds} n2,
                {region_ds}
            where
                p_partkey = l_partkey
                and s_suppkey = l_suppkey
                and l_orderkey = o_orderkey
                and o_custkey = c_custkey
                and c_nationkey = n1.n_nationkey
                and n1.n_regionkey = r_regionkey
                and r_name = 'AMERICA'
                and s_nationkey = n2.n_nationkey
                and o_orderdate between date '1995-01-01' and date '1996-12-31'
                and p_type = 'ECONOMY ANODIZED STEEL'
        ) as all_nations
    group by
        o_year
    order by
        o_year
"""

q9_query = f"""
    select
        nation,
        o_year,
        round(sum(amount), 2) as sum_profit
    from
        (
            select
                n_name as nation,
                EXTRACT(YEAR FROM o_orderdate) as o_year,
                l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
            from
                {part_ds},
                {supplier_ds},
                {line_item_ds},
                {part_supp_ds},
                {orders_ds},
                {nation_ds}
            where
                s_suppkey = l_suppkey
                and ps_suppkey = l_suppkey
                and ps_partkey = l_partkey
                and p_partkey = l_partkey
                and o_orderkey = l_orderkey
                and s_nationkey = n_nationkey
                and p_name like '%green%'
        ) as profit
    group by
        nation,
        o_year
    order by
        nation,
        o_year desc
"""

q10_query = f"""
    select
        c_custkey,
        c_name,
        round(sum(l_extendedprice * (1 - l_discount)), 2) as revenue,
        c_acctbal,
        n_name,
        c_address,
        c_phone,
        c_comment
    from
        {customer_ds},
        {orders_ds},
        {line_item_ds},
        {nation_ds}
    where
        c_custkey = o_custkey
        and l_orderkey = o_orderkey
        and o_orderdate >= date '1993-10-01'
        and o_orderdate < date '1993-10-01' + interval '3' month
        and l_returnflag = 'R'
        and c_nationkey = n_nationkey
    group by
        c_custkey,
        c_name,
        c_acctbal,
        c_phone,
        n_name,
        c_address,
        c_comment
    order by
        revenue desc
    limit 20
"""

q11_query = f"""
    select
        ps_partkey,
        round(sum(ps_supplycost * ps_availqty), 2) as value
    from
        {part_supp_ds},
        {supplier_ds},
        {nation_ds}
    where
        ps_suppkey = s_suppkey
        and s_nationkey = n_nationkey
        and n_name = 'GERMANY'
    group by
        ps_partkey having
                sum(ps_supplycost * ps_availqty) > (
            select
                sum(ps_supplycost * ps_availqty) * 0.0001
            from
                {part_supp_ds},
                {supplier_ds},
                {nation_ds}
            where
                ps_suppkey = s_suppkey
                and s_nationkey = n_nationkey
                and n_name = 'GERMANY'
            )
        order by
            value desc
"""

q12_query = f"""
    select
        l_shipmode,
        sum(case
            when o_orderpriority = '1-URGENT'
                or o_orderpriority = '2-HIGH'
                then 1
            else 0
        end) as high_line_count,
        sum(case
            when o_orderpriority <> '1-URGENT'
                and o_orderpriority <> '2-HIGH'
                then 1
            else 0
        end) as low_line_count
    from
        {orders_ds},
        {line_item_ds}
    where
        o_orderkey = l_orderkey
        and l_shipmode in ('MAIL', 'SHIP')
        and l_commitdate < l_receiptdate
        and l_shipdate < l_commitdate
        and l_receiptdate >= date '1994-01-01'
        and l_receiptdate < date '1994-01-01' + interval '1' year
    group by
        l_shipmode
    order by
        l_shipmode
"""

q13_query = f"""
    SELECT
        c_count, COUNT(*) AS custdist
    FROM (
        SELECT
            c_custkey,
            COUNT(o_orderkey) AS c_count
        FROM
            {customer_ds} LEFT OUTER JOIN {orders_ds} ON
            c_custkey = o_custkey
            AND o_comment NOT LIKE '%special%requests%'
        GROUP BY
            c_custkey
    ) AS c_orders
    GROUP BY
        c_count
    ORDER BY
        custdist DESC,
        c_count DESC
"""

q14_query = f"""
    select
        round(100.00 * sum(case
            when p_type like 'PROMO%'
                then l_extendedprice * (1 - l_discount)
            else 0
        end) / sum(l_extendedprice * (1 - l_discount)), 2) as promo_revenue
    from
        {line_item_ds},
        {part_ds}
    where
        l_partkey = p_partkey
        and l_shipdate >= date '1995-09-01'
        and l_shipdate < date '1995-09-01' + interval '1' month
"""

q15_query = f"""
    WITH revenue AS (
        SELECT
            l_suppkey AS supplier_no,
            SUM(l_extendedprice * (1 - l_discount)) AS total_revenue
        FROM
            {line_item_ds}
        WHERE
            l_shipdate >= DATE '1996-01-01'
            AND l_shipdate < DATE '1996-01-01' + INTERVAL '3' month
        GROUP BY
            l_suppkey
    )
    SELECT
        s.s_suppkey,
        s.s_name,
        s.s_address,
        s.s_phone,
        r.total_revenue
    FROM
        {supplier_ds} s
    JOIN
        revenue r ON s.s_suppkey = r.supplier_no
    WHERE
        r.total_revenue = (SELECT MAX(total_revenue) FROM revenue)
    ORDER BY
        s.s_suppkey;
"""

q16_query = f"""
    select
        p_brand,
        p_type,
        p_size,
        count(distinct ps_suppkey) as supplier_cnt
    from
        {part_supp_ds},
        {part_ds}
    where
        p_partkey = ps_partkey
        and p_brand <> 'Brand#45'
        and p_type not like 'MEDIUM POLISHED%'
        and p_size in (49, 14, 23, 45, 19, 3, 36, 9)
        and ps_suppkey not in (
            select
                s_suppkey
            from
                {supplier_ds}
            where
                s_comment like '%Customer%Complaints%'
        )
    group by
        p_brand,
        p_type,
        p_size
    order by
        supplier_cnt desc,
        p_brand,
        p_type,
        p_size
"""

q17_query = f"""
    select
        round(sum(l_extendedprice) / 7.0, 2) as avg_yearly
    from
        {line_item_ds},
        {part_ds}
    where
        p_partkey = l_partkey
        and p_brand = 'Brand#23'
        and p_container = 'MED BOX'
        and l_quantity < (
            select
                0.2 * avg(l_quantity)
            from
                {line_item_ds}
            where
                l_partkey = p_partkey
        )
"""

q18_query = f"""
    select
        c_name,
        c_custkey,
        o_orderkey,
        o_orderdate as o_orderdat,
        o_totalprice,
        sum(l_quantity) as col6
    from
        {customer_ds},
        {orders_ds},
        {line_item_ds}
    where
        o_orderkey in (
            select
                l_orderkey
            from
                {line_item_ds}
            group by
                l_orderkey having
                    sum(l_quantity) > 300
        )
        and c_custkey = o_custkey
        and o_orderkey = l_orderkey
    group by
        c_name,
        c_custkey,
        o_orderkey,
        o_orderdate,
        o_totalprice
    order by
        o_totalprice desc,
        o_orderdate
    limit 100
"""

q19_query = f"""
    select
        round(sum(l_extendedprice* (1 - l_discount)), 2) as revenue
    from
        {line_item_ds},
        {part_ds}
    where
        (
            p_partkey = l_partkey
            and p_brand = 'Brand#12'
            and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
            and l_quantity >= 1 and l_quantity <= 1 + 10
            and p_size between 1 and 5
            and l_shipmode in ('AIR', 'AIR REG')
            and l_shipinstruct = 'DELIVER IN PERSON'
        )
        or
        (
            p_partkey = l_partkey
            and p_brand = 'Brand#23'
            and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
            and l_quantity >= 10 and l_quantity <= 20
            and p_size between 1 and 10
            and l_shipmode in ('AIR', 'AIR REG')
            and l_shipinstruct = 'DELIVER IN PERSON'
        )
        or
        (
            p_partkey = l_partkey
            and p_brand = 'Brand#34'
            and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
            and l_quantity >= 20 and l_quantity <= 30
            and p_size between 1 and 15
            and l_shipmode in ('AIR', 'AIR REG')
            and l_shipinstruct = 'DELIVER IN PERSON'
        )
"""

q20_query = f"""
    select
        s_name,
        s_address
    from
        {supplier_ds},
        {nation_ds}
    where
        s_suppkey in (
            select
                ps_suppkey
            from
                {part_supp_ds}
            where
                ps_partkey in (
                    select
                        p_partkey
                    from
                        {part_ds}
                    where
                        p_name like 'forest%'
                )
                and ps_availqty > (
                    select
                        0.5 * sum(l_quantity)
                    from
                        {line_item_ds}
                    where
                        l_partkey = ps_partkey
                        and l_suppkey = ps_suppkey
                        and l_shipdate >= date '1994-01-01'
                        and l_shipdate < date '1994-01-01' + interval '1' year
                )
        )
        and s_nationkey = n_nationkey
        and n_name = 'CANADA'
    order by
        s_name
"""


q21_query = f"""
    select
        s_name,
        count(*) as numwait
    from
        {supplier_ds},
        {line_item_ds} l1,
        {orders_ds},
        {nation_ds}
    where
        s_suppkey = l1.l_suppkey
        and o_orderkey = l1.l_orderkey
        and o_orderstatus = 'F'
        and l1.l_receiptdate > l1.l_commitdate
        and exists (
            select
                *
            from
                {line_item_ds} l2
            where
                l2.l_orderkey = l1.l_orderkey
                and l2.l_suppkey <> l1.l_suppkey
        )
        and not exists (
            select
                *
            from
                {line_item_ds} l3
            where
                l3.l_orderkey = l1.l_orderkey
                and l3.l_suppkey <> l1.l_suppkey
                and l3.l_receiptdate > l3.l_commitdate
        )
        and s_nationkey = n_nationkey
        and n_name = 'SAUDI ARABIA'
    group by
        s_name
    order by
        numwait desc,
        s_name
    limit 100
"""

q22_query = f"""
    select
        cntrycode,
        count(*) as numcust,
        sum(c_acctbal) as totacctbal
    from (
        select
            SUBSTR(c_phone, 1, 2) AS cntrycode,
            c_acctbal
        from
            {customer_ds}
        where
            SUBSTR(c_phone, 1, 2) in
                ('13', '31', '23', '29', '30', '18', '17')
            and c_acctbal > (
                select
                    avg(c_acctbal)
                from
                    {customer_ds}
                where
                    c_acctbal > 0.00
                    and SUBSTR(c_phone, 1, 2) in
                        ('13', '31', '23', '29', '30', '18', '17')
            )
            and not exists (
                select
                    *
                from
                    {orders_ds}
                where
                    o_custkey = c_custkey
            )
        ) as custsale
    group by
        cntrycode
    order by
        cntrycode
"""


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
        query_var_name = f"q{i}_query"
        sql_query = globals().get(query_var_name, "Query not defined")
        file_path = f"third_party/bigframes_vendored/tpch/queries/q{i}.py"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                file_content = file.read()

                file_content = re.sub(
                    r"(\w+)\.to_gbq\(\)", r"return \1.to_pandas()", file_content
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
