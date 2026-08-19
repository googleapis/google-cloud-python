# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/polars/q22.py

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

    country_codes = ["13", "31", "23", "29", "30", "18", "17"]
    customer["CNTRYCODE"] = customer["C_PHONE"].str.slice(0, 2)
    customer = customer[customer["CNTRYCODE"].isin(country_codes)]

    avg_acctbal = (
        customer[customer["C_ACCTBAL"] > 0.0][["C_ACCTBAL"]]
        .mean()
        .rename("AVG_ACCTBAL")
    )
    customer = customer.merge(avg_acctbal, how="cross")

    filtered_customer = customer[customer["C_ACCTBAL"] > customer["AVG_ACCTBAL"]]

    filtered_customer = filtered_customer[
        ~filtered_customer["C_CUSTKEY"].isin(orders["O_CUSTKEY"])
    ]
    result = filtered_customer.groupby("CNTRYCODE", as_index=False).agg(
        NUMCUST=bpd.NamedAgg(column="C_CUSTKEY", aggfunc="count"),
        TOTACCTBAL=bpd.NamedAgg(column="C_ACCTBAL", aggfunc="sum"),
    )

    result = result.sort_values(by="CNTRYCODE")

    next(result.to_pandas_batches(max_results=1500))
