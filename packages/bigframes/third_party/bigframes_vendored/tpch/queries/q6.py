# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/pandas/q6.py

from datetime import date

import bigframes


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    lineitem = session.read_gbq(
        f"{project_id}.{dataset_id}.LINEITEM",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    var1 = date(1994, 1, 1)
    var2 = date(1995, 1, 1)
    var3 = 0.05
    var4 = 0.07
    var5 = 24

    filt = lineitem[(lineitem["L_SHIPDATE"] >= var1) & (lineitem["L_SHIPDATE"] < var2)]
    filt = filt[(filt["L_DISCOUNT"] >= var3) & (filt["L_DISCOUNT"] <= var4)]
    filt = filt[filt["L_QUANTITY"] < var5]
    result_df = (
        (filt["L_EXTENDEDPRICE"] * filt["L_DISCOUNT"])
        .agg(["sum"])
        .rename("REVENUE")
        .to_frame()
    )

    next(result_df.to_pandas_batches(max_results=1500))
