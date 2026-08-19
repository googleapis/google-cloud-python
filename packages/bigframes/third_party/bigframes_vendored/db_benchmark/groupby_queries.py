# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/groupby-pandas.py

import bigframes
import bigframes.session


def q1(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Groupby benchmark 1: sum v1 by id1")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = x.groupby("id1", as_index=False, dropna=False).agg({"v1": "sum"})
    print(ans.shape)
    chk = [ans["v1"].sum()]
    print(chk)


def q2(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Groupby benchmark 2: sum v1 by id1:id2")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = x.groupby(["id1", "id2"], as_index=False, dropna=False).agg({"v1": "sum"})
    print(ans.shape)
    chk = [ans["v1"].sum()]
    print(chk)


def q3(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Groupby benchmark 3: sum v1 mean v3 by id3")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = x.groupby("id3", as_index=False, dropna=False).agg(
        {"v1": "sum", "v3": "mean"}
    )
    print(ans.shape)
    chk = [ans["v1"].sum(), ans["v3"].sum()]
    print(chk)


def q4(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Groupby benchmark 4: mean v1:v3 by id4")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = x.groupby("id4", as_index=False, dropna=False).agg(
        {"v1": "mean", "v2": "mean", "v3": "mean"}
    )
    print(ans.shape)
    chk = [ans["v1"].sum(), ans["v2"].sum(), ans["v3"].sum()]
    print(chk)


def q5(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Groupby benchmark 5: sum v1:v3 by id6")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = x.groupby("id6", as_index=False, dropna=False).agg(
        {"v1": "sum", "v2": "sum", "v3": "sum"}
    )
    print(ans.shape)
    chk = [ans["v1"].sum(), ans["v2"].sum(), ans["v3"].sum()]
    print(chk)


def q6(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Groupby benchmark 6: median v3 sd v3 by id4 id5")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = x.groupby(["id4", "id5"], as_index=False, dropna=False).agg(
        {"v3": ["median", "std"]}
    )
    print(ans.shape)
    chk = [ans["v3"]["median"].sum(), ans["v3"]["std"].sum()]
    print(chk)


def q7(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Groupby benchmark 7: max v1 - min v2 by id3")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = (
        x.groupby("id3", as_index=False, dropna=False)
        .agg({"v1": "max", "v2": "min"})
        .assign(range_v1_v2=lambda x: x["v1"] - x["v2"])[["id3", "range_v1_v2"]]
    )
    print(ans.shape)
    chk = [ans["range_v1_v2"].sum()]
    print(chk)


def q8(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Groupby benchmark 8: largest two v3 by id6")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = (
        x[~x["v3"].isna()][["id6", "v3"]]
        .sort_values("v3", ascending=False)
        .groupby("id6", as_index=False, dropna=False)
        .head(2)
    )
    ans = ans.reset_index(drop=True)
    print(ans.shape)
    chk = [ans["v3"].sum()]
    print(chk)


def q10(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Groupby benchmark 10: sum v3 count by id1:id6")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")

    ans = x.groupby(
        ["id1", "id2", "id3", "id4", "id5", "id6"], as_index=False, dropna=False
    ).agg({"v3": "sum", "v1": "size"})
    print(ans.shape)
    chk = [ans["v3"].sum(), ans["v1"].sum()]
    print(chk)
