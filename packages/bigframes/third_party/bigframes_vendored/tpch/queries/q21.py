# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/duckdb/q21.py

import typing

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

    nation = nation[nation["N_NAME"] == "SAUDI ARABIA"]
    orders = orders[orders["O_ORDERSTATUS"] == "F"]

    l1 = lineitem[lineitem["L_RECEIPTDATE"] > lineitem["L_COMMITDATE"]][
        ["L_ORDERKEY", "L_SUPPKEY"]
    ]

    l2 = lineitem.groupby("L_ORDERKEY", as_index=False).agg(
        NUNIQUE_COL=bpd.NamedAgg(column="L_SUPPKEY", aggfunc="nunique")
    )
    l2 = l2[l2["NUNIQUE_COL"] > 1][["L_ORDERKEY"]]

    l3 = l1.groupby("L_ORDERKEY", as_index=False).agg(
        NUNIQUE_COL=bpd.NamedAgg(column="L_SUPPKEY", aggfunc="nunique")
    )
    l3 = l3[l3["NUNIQUE_COL"] == 1][["L_ORDERKEY"]]

    l1 = l1.merge(l2, on="L_ORDERKEY", how="inner").merge(
        l3, on="L_ORDERKEY", how="inner"
    )

    merged = supplier.merge(nation, left_on="S_NATIONKEY", right_on="N_NATIONKEY")
    merged = merged.merge(l1, left_on="S_SUPPKEY", right_on="L_SUPPKEY")
    merged = merged.merge(orders, left_on="L_ORDERKEY", right_on="O_ORDERKEY")

    result = merged.groupby("S_NAME", as_index=False).agg(
        NUMWAIT=bpd.NamedAgg(column="L_SUPPKEY", aggfunc="size")
    )

    result = (
        typing.cast(bpd.DataFrame, result)
        .sort_values(["NUMWAIT", "S_NAME"], ascending=[False, True])
        .head(100)
    )

    result.to_gbq()
