# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q10.py

from datetime import date
import typing

import bigframes
import bigframes.pandas as bpd


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    customer = session.read_gbq(
        f"{project_id}.{dataset_id}.CUSTOMER",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
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

    var1 = date(1993, 10, 1)
    var2 = date(1994, 1, 1)

    q_final = (
        customer.merge(orders, left_on="C_CUSTKEY", right_on="O_CUSTKEY")
        .merge(lineitem, left_on="O_ORDERKEY", right_on="L_ORDERKEY")
        .merge(nation, left_on="C_NATIONKEY", right_on="N_NATIONKEY")
    )

    q_final = typing.cast(
        bpd.DataFrame,
        q_final[
            (q_final["O_ORDERDATE"] >= var1)
            & (q_final["O_ORDERDATE"] < var2)
            & (q_final["L_RETURNFLAG"] == "R")
        ],
    )
    q_final["INTERMEDIATE_REVENUE"] = (
        q_final["L_EXTENDEDPRICE"] * (1 - q_final["L_DISCOUNT"])
    ).round(2)

    q_final = q_final.groupby(
        [
            "C_CUSTKEY",
            "C_NAME",
            "C_ACCTBAL",
            "C_PHONE",
            "N_NAME",
            "C_ADDRESS",
            "C_COMMENT",
        ],
        as_index=False,
    ).agg(REVENUE=bpd.NamedAgg(column="INTERMEDIATE_REVENUE", aggfunc="sum"))

    q_final = (
        q_final[
            [
                "C_CUSTKEY",
                "C_NAME",
                "REVENUE",
                "C_ACCTBAL",
                "N_NAME",
                "C_ADDRESS",
                "C_PHONE",
                "C_COMMENT",
            ]
        ]
        .sort_values(by="REVENUE", ascending=False)
        .head(20)
    )

    next(q_final.to_pandas_batches(max_results=1500))
