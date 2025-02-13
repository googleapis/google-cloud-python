# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/pandas/q5.py

from datetime import date

import bigframes


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    region = session.read_gbq(
        f"{project_id}.{dataset_id}.REGION",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    nation = session.read_gbq(
        f"{project_id}.{dataset_id}.NATION",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
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
    supplier = session.read_gbq(
        f"{project_id}.{dataset_id}.SUPPLIER",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    var1 = "ASIA"
    var2 = date(1994, 1, 1)
    var3 = date(1995, 1, 1)

    region = region[region["R_NAME"] == var1]
    orders = orders[(orders["O_ORDERDATE"] >= var2) & (orders["O_ORDERDATE"] < var3)]
    lineitem["REVENUE"] = lineitem["L_EXTENDEDPRICE"] * (1.0 - lineitem["L_DISCOUNT"])

    jn1 = region.merge(nation, left_on="R_REGIONKEY", right_on="N_REGIONKEY")
    jn2 = jn1.merge(customer, left_on="N_NATIONKEY", right_on="C_NATIONKEY")
    jn3 = orders.merge(jn2, left_on="O_CUSTKEY", right_on="C_CUSTKEY")
    jn4 = lineitem.merge(jn3, left_on="L_ORDERKEY", right_on="O_ORDERKEY")
    jn5 = jn4.merge(
        supplier,
        left_on=["L_SUPPKEY", "N_NATIONKEY"],
        right_on=["S_SUPPKEY", "S_NATIONKEY"],
    )

    gb = jn5.groupby("N_NAME", as_index=False)["REVENUE"].sum()
    result_df = gb.sort_values("REVENUE", ascending=False)

    next(result_df.to_pandas_batches(max_results=1500))
