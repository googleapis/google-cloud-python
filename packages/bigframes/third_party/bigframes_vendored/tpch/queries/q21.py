# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q21.py

import bigframes
import bigframes.pandas as bpd


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    lineitem = session.read_gbq(
        f"{project_id}.{dataset_id}.LINEITEM",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    nation = session.read_gbq(
        f"{project_id}.{dataset_id}.NATION",
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

    var1 = "SAUDI ARABIA"

    q1 = lineitem.groupby("L_ORDERKEY", as_index=False).agg(
        N_SUPP_BY_ORDER=bpd.NamedAgg(column="L_SUPPKEY", aggfunc="size")
    )
    q1 = q1[q1["N_SUPP_BY_ORDER"] > 1]

    lineitem_filtered = lineitem[lineitem["L_RECEIPTDATE"] > lineitem["L_COMMITDATE"]]

    q1 = q1.merge(lineitem_filtered, on="L_ORDERKEY")

    q_final = q1.groupby("L_ORDERKEY", as_index=False).agg(
        N_SUPP_BY_ORDER_FINAL=bpd.NamedAgg(column="L_SUPPKEY", aggfunc="size")
    )

    q_final = q_final.merge(q1, on="L_ORDERKEY")
    q_final = q_final.merge(supplier, left_on="L_SUPPKEY", right_on="S_SUPPKEY")
    q_final = q_final.merge(nation, left_on="S_NATIONKEY", right_on="N_NATIONKEY")
    q_final = q_final.merge(orders, left_on="L_ORDERKEY", right_on="O_ORDERKEY")

    q_final = q_final[
        (q_final["N_SUPP_BY_ORDER_FINAL"] == 1)
        & (q_final["N_NAME"] == var1)
        & (q_final["O_ORDERSTATUS"] == "F")
    ]

    q_final = q_final.groupby("S_NAME", as_index=False).agg(
        NUMWAIT=bpd.NamedAgg(column="L_SUPPKEY", aggfunc="size")
    )

    q_final = q_final.sort_values(
        by=["NUMWAIT", "S_NAME"], ascending=[False, True]
    ).head(100)

    next(q_final.to_pandas_batches(max_results=1500))
