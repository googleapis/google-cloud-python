# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/pandas/q3.py

from datetime import date

import bigframes


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    customer = session.read_gbq(
        f"{project_id}.{dataset_id}.CUSTOMER",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    lineitem = session.read_gbq(
        f"{project_id}.{dataset_id}.LINEITEM",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    orders = session.read_gbq(
        f"{project_id}.{dataset_id}.ORDERS",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    date_var = date(1995, 3, 15)

    fcustomer = customer[customer["C_MKTSEGMENT"] == "BUILDING"]

    filtered_orders = orders[orders["O_ORDERDATE"] < date_var]
    filtered_lineitem = lineitem[lineitem["L_SHIPDATE"] > date_var]

    jn1 = filtered_lineitem.merge(
        filtered_orders, left_on="L_ORDERKEY", right_on="O_ORDERKEY"
    )
    jn2 = fcustomer.merge(jn1, left_on="C_CUSTKEY", right_on="O_CUSTKEY")
    jn2["REVENUE"] = jn2["L_EXTENDEDPRICE"] * (1 - jn2["L_DISCOUNT"])

    gb = jn2.groupby(["O_ORDERKEY", "O_ORDERDATE", "O_SHIPPRIORITY"], as_index=False)
    agg = gb["REVENUE"].sum()

    sel = agg[["O_ORDERKEY", "REVENUE", "O_ORDERDATE", "O_SHIPPRIORITY"]]
    sel = sel.rename(columns={"O_ORDERKEY": "L_ORDERKEY"})

    sorted_sel = sel.sort_values(by=["REVENUE", "O_ORDERDATE"], ascending=[False, True])
    result_df = sorted_sel.head(10)

    next(result_df.to_pandas_batches(max_results=1500))
