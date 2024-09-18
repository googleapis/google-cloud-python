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

    if not session._strictly_ordered:
        filtered_parts = filtered_parts[["P_PARTKEY"]].sort_values(by=["P_PARTKEY"])
    filtered_parts = filtered_parts[["P_PARTKEY"]].drop_duplicates()
    joined_parts = filtered_parts.merge(
        partsupp, left_on="P_PARTKEY", right_on="PS_PARTKEY"
    )

    final_join = joined_parts.merge(
        q1, left_on=["PS_SUPPKEY", "P_PARTKEY"], right_on=["L_SUPPKEY", "L_PARTKEY"]
    )
    final_filtered = final_join[final_join["PS_AVAILQTY"] > final_join["SUM_QUANTITY"]]

    final_filtered = final_filtered[["PS_SUPPKEY"]]
    if not session._strictly_ordered:
        final_filtered = final_filtered.sort_values(by="PS_SUPPKEY")
    final_filtered = final_filtered.drop_duplicates()

    final_result = final_filtered.merge(q3, left_on="PS_SUPPKEY", right_on="S_SUPPKEY")
    final_result = final_result[["S_NAME", "S_ADDRESS"]].sort_values(by="S_NAME")

    final_result.to_gbq()
