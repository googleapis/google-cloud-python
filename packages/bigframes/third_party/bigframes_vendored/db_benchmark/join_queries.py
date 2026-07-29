# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/join-pandas.py
# and https://github.com/duckdblabs/db-benchmark/blob/main/_helpers/helpers.py

import bigframes


def q1(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Join benchmark 1: small inner on int")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")
    small = session.read_gbq(
        f"{project_id}.{dataset_id}.{_get_join_table_id(table_id, 'small')}"
    )

    ans = x.merge(small, on="id1")
    print(ans.shape)

    chk = [ans["v1"].sum(), ans["v2"].sum()]
    print(chk)


def q2(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Join benchmark 2: medium inner on int")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")
    medium = session.read_gbq(
        f"{project_id}.{dataset_id}.{_get_join_table_id(table_id, 'medium')}"
    )

    ans = x.merge(medium, on="id2")
    print(ans.shape)

    chk = [ans["v1"].sum(), ans["v2"].sum()]
    print(chk)


def q3(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Join benchmark 3: medium outer on int")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")
    medium = session.read_gbq(
        f"{project_id}.{dataset_id}.{_get_join_table_id(table_id, 'medium')}"
    )

    ans = x.merge(medium, how="left", on="id2")
    print(ans.shape)

    chk = [ans["v1"].sum(), ans["v2"].sum()]
    print(chk)


def q4(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Join benchmark 4: medium inner on factor")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")
    medium = session.read_gbq(
        f"{project_id}.{dataset_id}.{_get_join_table_id(table_id, 'medium')}"
    )

    ans = x.merge(medium, on="id5")
    print(ans.shape)

    chk = [ans["v1"].sum(), ans["v2"].sum()]
    print(chk)


def q5(project_id: str, dataset_id: str, table_id: str, session: bigframes.Session):
    print("Join benchmark 5: big inner on int")

    x = session.read_gbq(f"{project_id}.{dataset_id}.{table_id}")
    big = session.read_gbq(
        f"{project_id}.{dataset_id}.{_get_join_table_id(table_id, 'big')}"
    )

    ans = x.merge(big, on="id3")
    print(ans.shape)

    chk = [ans["v1"].sum(), ans["v2"].sum()]
    print(chk)


def _get_join_table_id(table_id, join_size):
    x_n = int(float(table_id.split("_")[1]))

    if join_size == "small":
        y_n = "{:.0e}".format(x_n / 1e6)
    elif join_size == "medium":
        y_n = "{:.0e}".format(x_n / 1e3)
    else:
        y_n = "{:.0e}".format(x_n)
    return table_id.replace("NA", y_n).replace("+0", "")
