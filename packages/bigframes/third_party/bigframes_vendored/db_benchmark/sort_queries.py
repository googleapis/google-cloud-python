# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/sort-pandas.py

import bigframes
import bigframes.session


def q1(
    project_id: str, dataset_id: str, table_id: str, session: bigframes.Session
) -> None:
    print("Sort benchmark 1: sort by int id2")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = x.sort_values("id2")
    print(ans.shape)

    chk = [ans["v1"].sum()]
    print(chk)
