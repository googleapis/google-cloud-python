# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/pandas/q2.py

import bigframes


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    region = session.read_gbq(
        f"{project_id}.{dataset_id}.REGION",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    nation = session.read_gbq(
        f"{project_id}.{dataset_id}.NATION",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    supplier = session.read_gbq(
        f"{project_id}.{dataset_id}.SUPPLIER",
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

    jn = (
        part.merge(partsupp, left_on="P_PARTKEY", right_on="PS_PARTKEY")
        .merge(supplier, left_on="PS_SUPPKEY", right_on="S_SUPPKEY")
        .merge(nation, left_on="S_NATIONKEY", right_on="N_NATIONKEY")
        .merge(region, left_on="N_REGIONKEY", right_on="R_REGIONKEY")
    )

    jn = jn[jn["P_SIZE"] == 15]
    jn = jn[jn["P_TYPE"].str.endswith("BRASS")]
    jn = jn[jn["R_NAME"] == "EUROPE"]

    gb = jn.groupby("P_PARTKEY", as_index=False)
    agg = gb["PS_SUPPLYCOST"].min()
    jn2 = agg.merge(jn, on=["P_PARTKEY", "PS_SUPPLYCOST"])

    sel = jn2[
        [
            "S_ACCTBAL",
            "S_NAME",
            "N_NAME",
            "P_PARTKEY",
            "P_MFGR",
            "S_ADDRESS",
            "S_PHONE",
            "S_COMMENT",
        ]
    ]

    sort = sel.sort_values(
        by=["S_ACCTBAL", "N_NAME", "S_NAME", "P_PARTKEY"],
        ascending=[False, True, True, True],
    )

    result_df = sort.head(100)
    next(result_df.to_pandas_batches(max_results=1500))
