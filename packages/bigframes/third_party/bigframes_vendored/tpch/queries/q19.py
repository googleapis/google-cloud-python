# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q19.py

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

    merged = bpd.merge(part, lineitem, left_on="P_PARTKEY", right_on="L_PARTKEY")

    filtered = merged[
        (merged["L_SHIPMODE"].isin(["AIR", "AIR REG"]))
        & (merged["L_SHIPINSTRUCT"] == "DELIVER IN PERSON")
        & (
            (
                (merged["P_BRAND"] == "Brand#12")
                & (
                    merged["P_CONTAINER"].isin(
                        ["SM CASE", "SM BOX", "SM PACK", "SM PKG"]
                    )
                )
                & (merged["L_QUANTITY"].between(1, 11, inclusive="both"))
                & (merged["P_SIZE"].between(1, 5, inclusive="both"))
            )
            | (
                (merged["P_BRAND"] == "Brand#23")
                & (
                    merged["P_CONTAINER"].isin(
                        ["MED BAG", "MED BOX", "MED PKG", "MED PACK"]
                    )
                )
                & (merged["L_QUANTITY"].between(10, 20, inclusive="both"))
                & (merged["P_SIZE"].between(1, 10, inclusive="both"))
            )
            | (
                (merged["P_BRAND"] == "Brand#34")
                & (
                    merged["P_CONTAINER"].isin(
                        ["LG CASE", "LG BOX", "LG PACK", "LG PKG"]
                    )
                )
                & (merged["L_QUANTITY"].between(20, 30, inclusive="both"))
                & (merged["P_SIZE"].between(1, 15, inclusive="both"))
            )
        )
    ]

    revenue = (filtered["L_EXTENDEDPRICE"] * (1 - filtered["L_DISCOUNT"])).sum()
    _ = round(revenue, 2)
