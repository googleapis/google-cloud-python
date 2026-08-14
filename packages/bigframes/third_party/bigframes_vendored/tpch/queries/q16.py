# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q16.py

import bigframes
import bigframes.pandas as bpd


def q(project_id: str, dataset_id: str, session: bigframes.Session):
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

    var1 = "Brand#45"

    supplier = supplier[
        ~supplier["S_COMMENT"].str.contains("Customer.*Complaints", regex=True)
    ]["S_SUPPKEY"]

    q_filtered = part.merge(partsupp, left_on="P_PARTKEY", right_on="PS_PARTKEY")
    q_filtered = q_filtered[q_filtered["P_BRAND"] != var1]
    q_filtered = q_filtered[~q_filtered["P_TYPE"].str.contains("MEDIUM POLISHED")]
    q_filtered = q_filtered[q_filtered["P_SIZE"].isin([49, 14, 23, 45, 19, 3, 36, 9])]

    final_df = q_filtered[q_filtered["PS_SUPPKEY"].isin(supplier)]

    grouped = final_df.groupby(["P_BRAND", "P_TYPE", "P_SIZE"], as_index=False)
    result = grouped.agg(
        SUPPLIER_CNT=bpd.NamedAgg(column="PS_SUPPKEY", aggfunc="nunique")
    )

    q_final = result.sort_values(
        by=["SUPPLIER_CNT", "P_BRAND", "P_TYPE", "P_SIZE"],
        ascending=[False, True, True, True],
    )

    next(q_final.to_pandas_batches(max_results=1500))
