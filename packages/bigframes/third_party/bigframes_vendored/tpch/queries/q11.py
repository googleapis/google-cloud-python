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

    merged_df = partsupp.merge(supplier, left_on="PS_SUPPKEY", right_on="S_SUPPKEY")
    merged_df = merged_df.merge(nation, left_on="S_NATIONKEY", right_on="N_NATIONKEY")

    filtered_df = merged_df[merged_df["N_NAME"] == "GERMANY"]

    filtered_df["VALUE"] = filtered_df["PS_SUPPLYCOST"] * filtered_df["PS_AVAILQTY"]
    grouped = filtered_df.groupby("PS_PARTKEY", as_index=False).agg(
        VALUE=bpd.NamedAgg(column="VALUE", aggfunc="sum")
    )

    grouped["VALUE"] = grouped["VALUE"].round(2)

    total_value = (filtered_df["PS_SUPPLYCOST"] * filtered_df["PS_AVAILQTY"]).sum()
    threshold = total_value * 0.0001

    result_df = grouped[grouped["VALUE"] > threshold]

    result_df = result_df.sort_values(by="VALUE", ascending=False)

    result_df.to_gbq()
