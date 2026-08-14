# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q9.py

import typing

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
    orders = session.read_gbq(
        f"{project_id}.{dataset_id}.ORDERS",
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

    q_final = (
        part.merge(
            lineitem,
            left_on="P_PARTKEY",
            right_on="L_PARTKEY",
        )
        .merge(
            partsupp,
            left_on=["L_SUPPKEY", "L_PARTKEY"],
            right_on=["PS_SUPPKEY", "PS_PARTKEY"],
        )
        .merge(supplier, left_on="L_SUPPKEY", right_on="S_SUPPKEY")
        .merge(orders, left_on="L_ORDERKEY", right_on="O_ORDERKEY")
        .merge(nation, left_on="S_NATIONKEY", right_on="N_NATIONKEY")
    )

    q_final = q_final[q_final["P_NAME"].str.contains("green")]

    q_final = q_final.rename(columns={"N_NAME": "NATION"})
    q_final["O_YEAR"] = q_final["O_ORDERDATE"].dt.year
    q_final["AMOUNT"] = (
        q_final["L_EXTENDEDPRICE"] * (1 - q_final["L_DISCOUNT"])
        - q_final["PS_SUPPLYCOST"] * q_final["L_QUANTITY"]
    )

    q_final = q_final[["NATION", "O_YEAR", "AMOUNT"]]

    q_final = q_final.groupby(["NATION", "O_YEAR"], as_index=False).agg(
        SUM_PROFIT=bpd.NamedAgg(column="AMOUNT", aggfunc="sum")
    )

    q_final["SUM_PROFIT"] = q_final["SUM_PROFIT"].round(2)

    q_final = typing.cast(bpd.DataFrame, q_final).sort_values(
        ["NATION", "O_YEAR"], ascending=[True, False]
    )

    next(q_final.to_pandas_batches(max_results=1500))
