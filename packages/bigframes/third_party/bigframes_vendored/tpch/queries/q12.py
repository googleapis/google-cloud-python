# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q12.py

from datetime import date
import typing

import bigframes
import bigframes.pandas as bpd


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    lineitem = session.read_gbq(
        f"{project_id}.{dataset_id}.LINEITEM",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    orders = session.read_gbq(
        f"{project_id}.{dataset_id}.ORDERS",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    var1 = "MAIL"
    var2 = "SHIP"
    var3 = date(1994, 1, 1)
    var4 = date(1995, 1, 1)

    q_final = orders.merge(lineitem, left_on="O_ORDERKEY", right_on="L_ORDERKEY")

    q_final = q_final[
        (q_final["L_SHIPMODE"].isin([var1, var2]))
        & (q_final["L_COMMITDATE"] < q_final["L_RECEIPTDATE"])
        & (q_final["L_SHIPDATE"] < q_final["L_COMMITDATE"])
        & (q_final["L_RECEIPTDATE"] >= var3)
        & (q_final["L_RECEIPTDATE"] < var4)
    ]

    q_final["HIGH_LINE_COUNT"] = (
        q_final["O_ORDERPRIORITY"].isin(["1-URGENT", "2-HIGH"])
    ).astype("Int64")
    q_final["LOW_LINE_COUNT"] = (
        ~q_final["O_ORDERPRIORITY"].isin(["1-URGENT", "2-HIGH"])
    ).astype("Int64")

    agg_results = q_final.groupby("L_SHIPMODE", as_index=False).agg(
        HIGH_LINE_COUNT=bpd.NamedAgg(column="HIGH_LINE_COUNT", aggfunc="sum"),
        LOW_LINE_COUNT=bpd.NamedAgg(column="LOW_LINE_COUNT", aggfunc="sum"),
    )

    agg_results = typing.cast(bpd.DataFrame, agg_results).sort_values("L_SHIPMODE")

    next(agg_results.to_pandas_batches(max_results=1500))
