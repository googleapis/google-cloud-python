# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q14.py

from datetime import date

import bigframes


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    lineitem = session.read_gbq(
        f"{project_id}.{dataset_id}.LINEITEM",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    part = session.read_gbq(
        f"{project_id}.{dataset_id}.PART",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    var1 = date(1995, 9, 1)
    var2 = date(1995, 10, 1)

    merged = part.merge(lineitem, left_on="P_PARTKEY", right_on="L_PARTKEY")

    filtered = merged[(merged["L_SHIPDATE"] >= var1) & (merged["L_SHIPDATE"] < var2)]

    filtered["CONDI_REVENUE"] = (
        filtered["L_EXTENDEDPRICE"] * (1 - filtered["L_DISCOUNT"])
    ) * filtered["P_TYPE"].str.contains("PROMO").astype("Int64")

    total_revenue = (
        (filtered["L_EXTENDEDPRICE"] * (1 - filtered["L_DISCOUNT"]))
        .to_frame(name="TEMP")
        .sum()
    )

    promo_revenue = filtered["CONDI_REVENUE"].to_frame(name="TEMP").sum()

    promo_revenue_percent = (
        (100.00 * promo_revenue / total_revenue)
        .sort_index()
        .reset_index(drop=True)
        .round(2)
        .to_frame(name="PROMO_REVENUE")
    )

    next(promo_revenue_percent.to_pandas_batches(max_results=1500))
