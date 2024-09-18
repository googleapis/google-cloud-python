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

    avg_acctbal = customer[
        (customer["CNTRYCODE"].isin(country_codes)) & (customer["C_ACCTBAL"] > 0)
    ]["C_ACCTBAL"].mean()

    if not session._strictly_ordered:
        orders = orders.sort_values(by="O_CUSTKEY")
    orders_unique = orders.drop_duplicates(subset=["O_CUSTKEY"])

    matched_customers = customer.merge(
        orders_unique, left_on="C_CUSTKEY", right_on="O_CUSTKEY"
    )
    matched_customers["IS_IN_ORDERS"] = True

    customer = customer.merge(
        matched_customers[["C_CUSTKEY", "IS_IN_ORDERS"]], on="C_CUSTKEY", how="left"
    )
    customer["IS_IN_ORDERS"] = customer["IS_IN_ORDERS"].fillna(False)

    filtered_customers = customer[
        (customer["CNTRYCODE"].isin(country_codes))
        & (customer["C_ACCTBAL"] > avg_acctbal)
        & (~customer["IS_IN_ORDERS"])
    ]

    result = filtered_customers.groupby("CNTRYCODE", as_index=False).agg(
        NUMCUST=bpd.NamedAgg(column="C_CUSTKEY", aggfunc="count"),
        TOTACCTBAL=bpd.NamedAgg(column="C_ACCTBAL", aggfunc="sum"),
    )

    result = result.sort_values(by="CNTRYCODE")

    result.to_gbq()
