# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q13.py

import typing

import bigframes
import bigframes.pandas as bpd


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    customer = session.read_gbq(
        f"{project_id}.{dataset_id}.CUSTOMER",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    orders = session.read_gbq(
        f"{project_id}.{dataset_id}.ORDERS",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    var1 = "special"
    var2 = "requests"

    regex_pattern = f"{var1}.*{var2}"
    orders = orders[~orders["O_COMMENT"].str.contains(regex_pattern, regex=True)]

    q_final = (
        customer.merge(orders, left_on="C_CUSTKEY", right_on="O_CUSTKEY", how="left")
        .groupby("C_CUSTKEY", as_index=False)
        .agg(C_COUNT=bpd.NamedAgg(column="O_ORDERKEY", aggfunc="count"))
        .groupby("C_COUNT", as_index=False)
        .agg("size")
        .rename(columns={"size": "CUSTDIST"})
    )
    q_final = typing.cast(bpd.DataFrame, q_final).sort_values(
        ["CUSTDIST", "C_COUNT"], ascending=[False, False]
    )

    next(q_final.to_pandas_batches(max_results=1500))
