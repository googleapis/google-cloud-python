# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q15.py

from datetime import date

import bigframes
import bigframes.pandas as bpd


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    lineitem = session.read_gbq(
        f"{project_id}.{dataset_id}.LINEITEM",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    supplier = session.read_gbq(
        f"{project_id}.{dataset_id}.SUPPLIER",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    var1 = date(1996, 1, 1)
    var2 = date(1996, 4, 1)

    filtered_lineitem = lineitem[
        (lineitem["L_SHIPDATE"] >= var1) & (lineitem["L_SHIPDATE"] < var2)
    ]
    filtered_lineitem["REVENUE"] = filtered_lineitem["L_EXTENDEDPRICE"] * (
        1 - filtered_lineitem["L_DISCOUNT"]
    )

    grouped_revenue = (
        filtered_lineitem.groupby("L_SUPPKEY", as_index=False)
        .agg(TOTAL_REVENUE=bpd.NamedAgg(column="REVENUE", aggfunc="sum"))
        .rename(columns={"L_SUPPKEY": "SUPPLIER_NO"})
    )
    # Round earlier to prevent non-determinism in the later join due to
    # differences in distributed floating point operation sort order.
    grouped_revenue = grouped_revenue.assign(
        TOTAL_REVENUE=grouped_revenue["TOTAL_REVENUE"].round(2)
    )

    joined_data = bpd.merge(
        supplier, grouped_revenue, left_on="S_SUPPKEY", right_on="SUPPLIER_NO"
    )

    max_revenue = joined_data[["TOTAL_REVENUE"]].max().rename("MAX_REVENUE")

    joined_data = joined_data.merge(max_revenue, how="cross")

    max_revenue_suppliers = joined_data[
        joined_data["TOTAL_REVENUE"] == joined_data["MAX_REVENUE"]
    ]
    q_final = max_revenue_suppliers[
        ["S_SUPPKEY", "S_NAME", "S_ADDRESS", "S_PHONE", "TOTAL_REVENUE"]
    ].sort_values("S_SUPPKEY")
    next(q_final.to_pandas_batches(max_results=1500))
