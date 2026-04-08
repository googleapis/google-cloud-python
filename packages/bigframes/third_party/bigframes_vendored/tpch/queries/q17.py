# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q17.py

import bigframes
import bigframes.pandas as bpd


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    lineitem = session.read_gbq(
        f"{project_id}.{dataset_id}.LINEITEM",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    part = session.read_gbq(
        f"{project_id}.{dataset_id}.PART",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    VAR1 = "Brand#23"
    VAR2 = "MED BOX"

    filtered_part = part[(part["P_BRAND"] == VAR1) & (part["P_CONTAINER"] == VAR2)]
    q1 = bpd.merge(
        lineitem, filtered_part, how="right", left_on="L_PARTKEY", right_on="P_PARTKEY"
    )

    grouped = (
        q1.groupby("P_PARTKEY", as_index=False)
        .agg(AVG_QUANTITY=bpd.NamedAgg(column="L_QUANTITY", aggfunc="mean"))
        .rename(columns={"P_PARTKEY": "KEY"})
    )
    grouped["AVG_QUANTITY"] = grouped["AVG_QUANTITY"] * 0.2

    q_final = bpd.merge(grouped, q1, left_on="KEY", right_on="P_PARTKEY")

    q_final = q_final[q_final["L_QUANTITY"] < q_final["AVG_QUANTITY"]]

    q_final = (
        (q_final[["L_EXTENDEDPRICE"]].sum() / 7.0).round(2).to_frame(name="AVG_YEARLY")
    )

    next(q_final.to_pandas_batches(max_results=1500))
