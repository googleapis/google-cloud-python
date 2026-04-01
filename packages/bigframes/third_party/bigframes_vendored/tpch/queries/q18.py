# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q18.py

import typing

import bigframes
import bigframes.pandas as bpd


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

    var1 = 300

    # order with over 300 items
    q1 = lineitem.groupby("L_ORDERKEY", as_index=False).agg(
        SUM_QUANTITY=bpd.NamedAgg(column="L_QUANTITY", aggfunc="sum")
    )
    q1 = q1[q1["SUM_QUANTITY"] > var1]

    filtered_orders = orders[orders["O_ORDERKEY"].isin(q1["L_ORDERKEY"])]

    result = filtered_orders.merge(
        lineitem, left_on="O_ORDERKEY", right_on="L_ORDERKEY"
    )
    result = result.merge(customer, left_on="O_CUSTKEY", right_on="C_CUSTKEY")

    final_result = result.groupby(
        ["C_NAME", "C_CUSTKEY", "O_ORDERKEY", "O_ORDERDATE", "O_TOTALPRICE"],
        as_index=False,
    ).agg(COL6=bpd.NamedAgg(column="L_QUANTITY", aggfunc="sum"))

    final_result = final_result.rename(columns={"O_ORDERDATE": "O_ORDERDAT"})

    final_result = typing.cast(bpd.DataFrame, final_result).sort_values(
        ["O_TOTALPRICE", "O_ORDERDAT"], ascending=[False, True]
    )

    q_final = final_result.head(100)
    next(q_final.to_pandas_batches(max_results=1500))
