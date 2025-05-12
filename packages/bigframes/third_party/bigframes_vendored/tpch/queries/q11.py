# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/duckdb/q11.py

import bigframes
import bigframes.pandas as bpd


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    supplier = session.read_gbq(
        f"{project_id}.{dataset_id}.SUPPLIER",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    partsupp = session.read_gbq(
        f"{project_id}.{dataset_id}.PARTSUPP",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    nation = session.read_gbq(
        f"{project_id}.{dataset_id}.NATION",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    nation = nation[nation["N_NAME"] == "GERMANY"]

    merged_df = nation.merge(supplier, left_on="N_NATIONKEY", right_on="S_NATIONKEY")
    merged_df = merged_df.merge(partsupp, left_on="S_SUPPKEY", right_on="PS_SUPPKEY")

    merged_df["VALUE"] = merged_df["PS_SUPPLYCOST"] * merged_df["PS_AVAILQTY"]
    grouped = merged_df.groupby("PS_PARTKEY", as_index=False).agg(
        VALUE=bpd.NamedAgg(column="VALUE", aggfunc="sum")
    )

    grouped["VALUE"] = grouped["VALUE"].round(2)

    total_value = (
        (merged_df["PS_SUPPLYCOST"] * merged_df["PS_AVAILQTY"]).to_frame().sum()
    )
    threshold = (total_value * 0.0001).rename("THRESHOLD")

    grouped = grouped.merge(threshold, how="cross")

    result_df = grouped[grouped["VALUE"] > grouped["THRESHOLD"]].drop(
        columns="THRESHOLD"
    )

    result_df = result_df.sort_values(by="VALUE", ascending=False)

    next(result_df.to_pandas_batches(max_results=1500))
