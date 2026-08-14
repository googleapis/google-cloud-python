# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/pandas/q8.py

from datetime import date

import bigframes


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
    part = session.read_gbq(
        f"{project_id}.{dataset_id}.PART",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    region = session.read_gbq(
        f"{project_id}.{dataset_id}.REGION",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    supplier = session.read_gbq(
        f"{project_id}.{dataset_id}.SUPPLIER",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    var1 = "BRAZIL"
    var2 = "AMERICA"
    var3 = "ECONOMY ANODIZED STEEL"
    var4 = date(1995, 1, 1)
    var5 = date(1996, 12, 31)

    n1 = nation[["N_NATIONKEY", "N_REGIONKEY"]]
    n2 = nation[["N_NATIONKEY", "N_NAME"]]

    jn1 = part.merge(lineitem, left_on="P_PARTKEY", right_on="L_PARTKEY")
    jn2 = jn1.merge(supplier, left_on="L_SUPPKEY", right_on="S_SUPPKEY")
    jn3 = jn2.merge(orders, left_on="L_ORDERKEY", right_on="O_ORDERKEY")
    jn4 = jn3.merge(customer, left_on="O_CUSTKEY", right_on="C_CUSTKEY")
    jn5 = jn4.merge(n1, left_on="C_NATIONKEY", right_on="N_NATIONKEY")
    jn6 = jn5.merge(region, left_on="N_REGIONKEY", right_on="R_REGIONKEY")

    jn6 = jn6[(jn6["R_NAME"] == var2)]

    jn7 = jn6.merge(n2, left_on="S_NATIONKEY", right_on="N_NATIONKEY")

    jn7 = jn7[(jn7["O_ORDERDATE"] >= var4) & (jn7["O_ORDERDATE"] <= var5)]
    jn7 = jn7[jn7["P_TYPE"] == var3]

    jn7["O_YEAR"] = jn7["O_ORDERDATE"].dt.year
    jn7["VOLUME"] = jn7["L_EXTENDEDPRICE"] * (1.0 - jn7["L_DISCOUNT"])
    jn7 = jn7.rename(columns={"N_NAME": "NATION"})

    jn7["numerator"] = jn7["VOLUME"].where(jn7["NATION"] == var1, 0)
    jn7["denominator"] = jn7["VOLUME"]

    sums = jn7.groupby("O_YEAR")[["numerator", "denominator"]].sum()
    sums["MKT_SHARE"] = (sums["numerator"] / sums["denominator"]).round(2)

    result_df = sums["MKT_SHARE"].sort_index().rename("MKT_SHARE").reset_index()
    next(result_df.to_pandas_batches(max_results=1500))
