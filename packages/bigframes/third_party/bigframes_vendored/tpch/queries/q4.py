# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/pandas/q4.py


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

    var1 = date(1993, 7, 1)
    var2 = date(1993, 10, 1)

    jn = lineitem.merge(orders, left_on="L_ORDERKEY", right_on="O_ORDERKEY")

    jn = jn[(jn["O_ORDERDATE"] >= var1) & (jn["O_ORDERDATE"] < var2)]
    jn = jn[jn["L_COMMITDATE"] < jn["L_RECEIPTDATE"]]

    jn = jn.groupby(["O_ORDERPRIORITY", "L_ORDERKEY"], as_index=False).agg("size")

    gb = jn.groupby("O_ORDERPRIORITY", as_index=False)
    agg = gb.agg(ORDER_COUNT=bpd.NamedAgg(column="L_ORDERKEY", aggfunc="count"))

    result_df = typing.cast(bpd.DataFrame, agg).sort_values(["O_ORDERPRIORITY"])
    next(result_df.to_pandas_batches(max_results=1500))
