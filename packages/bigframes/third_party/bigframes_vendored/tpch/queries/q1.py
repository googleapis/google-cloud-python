# Contains code from https://github.com/pola-rs/tpch/blob/main/queries/pandas/q1.py

from datetime import datetime
import typing

import bigframes
import bigframes.pandas as bpd


def q(project_id: str, dataset_id: str, session: bigframes.Session):
    lineitem = session.read_gbq(
        f"{project_id}.{dataset_id}.LINEITEM",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )

    var1 = datetime(1998, 9, 2)
    lineitem = lineitem[lineitem["L_SHIPDATE"] <= var1.date()]

    lineitem["DISC_PRICE"] = lineitem["L_EXTENDEDPRICE"] * (
        1.0 - lineitem["L_DISCOUNT"]
    )
    lineitem["CHARGE_PRICE"] = (
        lineitem["L_EXTENDEDPRICE"]
        * (1.0 - lineitem["L_DISCOUNT"])
        * (1.0 + lineitem["L_TAX"])
    )

    result = lineitem.groupby(["L_RETURNFLAG", "L_LINESTATUS"], as_index=False).agg(
        SUM_QTY=bpd.NamedAgg(column="L_QUANTITY", aggfunc="sum"),
        SUM_BASE_PRICE=bpd.NamedAgg(column="L_EXTENDEDPRICE", aggfunc="sum"),
        SUM_DISC_PRICE=bpd.NamedAgg(column="DISC_PRICE", aggfunc="sum"),
        SUM_CHARGE=bpd.NamedAgg(column="CHARGE_PRICE", aggfunc="sum"),
        AVG_QTY=bpd.NamedAgg(column="L_QUANTITY", aggfunc="mean"),
        AVG_PRICE=bpd.NamedAgg(column="L_EXTENDEDPRICE", aggfunc="mean"),
        AVG_DISC=bpd.NamedAgg(column="L_DISCOUNT", aggfunc="mean"),
        COUNT_ORDER=bpd.NamedAgg(column="L_QUANTITY", aggfunc="count"),
    )
    result = typing.cast(bpd.DataFrame, result).sort_values(
        ["L_RETURNFLAG", "L_LINESTATUS"]
    )

    next(result.to_pandas_batches(max_results=1500))
