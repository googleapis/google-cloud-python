# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q20.py

from datetime import date

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
    part = session.read_gbq(
        f"{project_id}.{dataset_id}.PART",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    partsupp = session.read_gbq(
        f"{project_id}.{dataset_id}.PARTSUPP",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    supplier = session.read_gbq(
        f"{project_id}.{dataset_id}.SUPPLIER",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    var1 = date(1994, 1, 1)
    var2 = date(1995, 1, 1)
    var3 = "CANADA"
    var4 = "forest"

    q1 = lineitem[(lineitem["L_SHIPDATE"] >= var1) & (lineitem["L_SHIPDATE"] < var2)]
    q1 = q1.groupby(["L_PARTKEY", "L_SUPPKEY"], as_index=False).agg(
        SUM_QUANTITY=bpd.NamedAgg(column="L_QUANTITY", aggfunc="sum")
    )
    q1["SUM_QUANTITY"] = q1["SUM_QUANTITY"] * 0.5
    q2 = nation[nation["N_NAME"] == var3]

    q3 = supplier.merge(q2, left_on="S_NATIONKEY", right_on="N_NATIONKEY")

    filtered_parts = part[part["P_NAME"].str.startswith(var4)]

    filtered_parts = filtered_parts["P_PARTKEY"]
    joined_parts = partsupp[partsupp["PS_PARTKEY"].isin(filtered_parts)]

    final_join = q1.merge(
        joined_parts,
        left_on=["L_SUPPKEY", "L_PARTKEY"],
        right_on=["PS_SUPPKEY", "PS_PARTKEY"],
    )
    final_filtered = final_join[final_join["PS_AVAILQTY"] > final_join["SUM_QUANTITY"]][
        "PS_SUPPKEY"
    ]

    final_result = q3[q3["S_SUPPKEY"].isin(final_filtered)]
    final_result = final_result[["S_NAME", "S_ADDRESS"]].sort_values(by="S_NAME")

    next(final_result.to_pandas_batches(max_results=1500))
